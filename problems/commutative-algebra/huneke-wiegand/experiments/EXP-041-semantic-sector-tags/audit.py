"""Independent deterministic audit of EXP-041 semantic profiles."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
from types import ModuleType


HERE = Path(__file__).resolve().parent
EXP037 = HERE.parent / "EXP-037-connecting-quasipolynomial"
PRIMARY = HERE / "artifacts" / "results.json"
REVERSE = HERE / "artifacts" / "reverse-tag-results.json"
OUTPUT = HERE / "artifacts" / "audit-certificate.json"
EXPECTED_HASHES = {
    "primary": "069e587b779bd1571d72e1a47bf74f4d1640dae5fbbf09907d2bf798c4941534",
    "reverse": "eafad05553cb7401c27ebeafcf686da6b436a25031dbc0f89e638096a6e02a1b",
}
EXPECTED_PARTITIONS = {8: [20, 4, 4, 3], 9: [45, 4], 10: [67, 5], 11: [95, 7]}
GENERATOR_TAGS = ("L0", "L1", "H0", "H1", "H2", "H3", "H4", "H5", "H6", "H7")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def interval(first: int, last: int) -> set[int]:
    return set(range(first, last + 1)) if first <= last else set()


def generator_blocks(p: int) -> dict[str, set[int]]:
    return {
        "L0": interval(1, p),
        "L1": interval(3 * p, 4 * p - 2),
        "H0": interval(6 * p, 8 * p - 2),
        "H1": interval(8 * p, 10 * p - 2),
        "H2": {10 * p},
        "H3": interval(11 * p - 1, 12 * p - 1),
        "H4": interval(13 * p + 1, 14 * p - 2),
        "H5": interval(14 * p, 15 * p - 1),
        "H6": {16 * p},
        "H7": interval(17 * p - 1, 18 * p - 1),
    }


def degree_two_blocks(p: int) -> dict[str, set[int]]:
    return {
        "C0": {8 * p - 1},
        "C1": {10 * p - 1},
        "C2": interval(10 * p + 1, 11 * p - 2),
        "C3": interval(12 * p, 13 * p),
        "C4": {14 * p - 1},
        "C5": interval(15 * p, 16 * p - 1),
        "C6": interval(16 * p + 1, 17 * p - 2),
        "C7": interval(18 * p, 24 * p - 1),
    }


def pairwise_disjoint(blocks: dict[str, set[int]]) -> bool:
    names = list(blocks)
    return all(
        not (blocks[names[left]] & blocks[names[right]])
        for left in range(len(names))
        for right in range(left + 1, len(names))
    )


def union(blocks: dict[str, set[int]]) -> set[int]:
    answer: set[int] = set()
    for block in blocks.values():
        answer.update(block)
    return answer


def profile_view(profile: dict[str, object]) -> dict[str, object]:
    keys = (
        "component",
        "support_hash",
        "rows",
        "columns",
        "vertices",
        "defect",
        "selected_row_present",
        "coefficient_tag_support",
        "coefficient_tag_support_hash",
        "semantic_atom_count",
        "semantic_histogram",
        "semantic_histogram_hash",
    )
    return {key: profile[key] for key in keys}


def normalized_atom_support(profile: dict[str, object], p: int) -> set[str]:
    support: set[str] = set()
    for encoded in profile["semantic_histogram"]:
        atom = json.loads(encoded)
        counts = list(atom[3])
        counts[0] -= p
        counts[1] -= p
        atom[3] = counts
        support.add(json.dumps(atom, separators=(",", ":")))
    return support


def main() -> int:
    actual_hashes = {"primary": sha256(PRIMARY), "reverse": sha256(REVERSE)}
    if actual_hashes != EXPECTED_HASHES:
        raise AssertionError({"artifact_hashes": actual_hashes})
    primary = json.loads(PRIMARY.read_text(encoding="utf-8"))
    reverse = json.loads(REVERSE.read_text(encoding="utf-8"))
    exp037 = load_module("exp037_frozen_for_exp041_audit", EXP037 / "run.py")
    exp036 = exp037.load_exp036()
    primary_rows = {int(row["p"]): row for row in primary["rows"]}
    reverse_rows = {int(row["p"]): row for row in reverse["rows"]}
    checks: dict[str, bool] = {
        "primary_complete": primary["status"] == "COMPLETE",
        "reverse_complete": reverse["status"] == "COMPLETE",
        "primary_p1_passes": primary["p1_status"] == "PASS_FINITE",
        "primary_p2_refuted": primary["p2_status"] == "REFUTED",
        "primary_p3_refuted": primary["p3_status"] == "REFUTED",
        "decision_agreement": all(
            primary[key] == reverse[key]
            for key in (
                "p1_status",
                "p1_checks",
                "p2_status",
                "p2_checks",
                "p3_status",
                "selected_components",
                "anchor_hashes",
                "isolated_hashes",
            )
        ),
        "parameter_coverage": set(primary_rows) == set(reverse_rows) == {8, 9, 10, 11},
    }
    for p in sorted(primary_rows):
        generators = generator_blocks(p)
        degree_two = degree_two_blocks(p)
        checks[f"p{p}_generator_blocks_disjoint"] = pairwise_disjoint(generators)
        checks[f"p{p}_degree_two_blocks_disjoint"] = pairwise_disjoint(degree_two)
        checks[f"p{p}_generator_partition"] = union(generators) == (
            exp036.degree_one_offsets(p) - {0}
        )
        checks[f"p{p}_degree_two_partition"] = union(degree_two) == exp036.degree_two_offsets(p)
        p_row = primary_rows[p]
        r_row = reverse_rows[p]
        checks[f"p{p}_frozen_component_agreement"] = (
            p_row["component_regression_hash"] == r_row["component_regression_hash"]
        )
        checks[f"p{p}_partition"] = (
            p_row["defect_partition"] == r_row["defect_partition"] == EXPECTED_PARTITIONS[p]
        )
        primary_profiles = [profile_view(profile) for profile in p_row["defective_profiles"]]
        reverse_profiles = [profile_view(profile) for profile in r_row["defective_profiles"]]
        checks[f"p{p}_reverse_profile_agreement"] = primary_profiles == reverse_profiles
        for profile in primary_profiles:
            histogram = profile["semantic_histogram"]
            decoded = [(json.loads(atom), count) for atom, count in histogram.items()]
            row_total = sum(count for atom, count in decoded if atom[0] == "row")
            column_total = sum(count for atom, count in decoded if atom[0] == "column")
            component = profile["component"]
            checks[f"p{p}_c{component}_histogram_sum"] = (
                row_total == profile["rows"] and column_total == profile["columns"]
            )
            checks[f"p{p}_c{component}_atom_shape"] = all(
                len(atom) == 4
                and len(atom[3]) == len(GENERATOR_TAGS)
                and sum(atom[3]) == (2 * p - 3 if atom[0] == "row" else 2 * p - 2)
                for atom, _ in decoded
            )
            support = sorted({":".join(atom[:3]) for atom, _ in decoded})
            checks[f"p{p}_c{component}_support"] = (
                support == profile["coefficient_tag_support"]
                and digest(support) == profile["coefficient_tag_support_hash"]
            )
            checks[f"p{p}_c{component}_histogram_hash"] = (
                digest(histogram) == profile["semantic_histogram_hash"]
            )
    isolated_profiles = {
        p: min(
            primary_rows[p]["defective_profiles"],
            key=lambda profile: int(profile["vertices"]),
        )
        for p in primary_rows
    }
    isolated_skeletons = {
        p: normalized_atom_support(profile, p)
        for p, profile in isolated_profiles.items()
    }
    checks["isolated_normalized_atom_skeleton_persists"] = all(
        skeleton == isolated_skeletons[8]
        for skeleton in isolated_skeletons.values()
    )
    checks["isolated_skeleton_has_twelve_atoms"] = all(
        len(skeleton) == 12 for skeleton in isolated_skeletons.values()
    )
    checks["isolated_omits_h1_c1"] = all(
        "column:K:H1" not in profile["coefficient_tag_support"]
        and "row:K:C1" not in profile["coefficient_tag_support"]
        for profile in isolated_profiles.values()
    )
    if not all(checks.values()):
        raise AssertionError({key: value for key, value in checks.items() if not value})
    certificate = {
        "experiment": "EXP-041",
        "status": "PASS",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "artifact_hashes": actual_hashes,
        "checks": checks,
        "result": {
            "p1_status": primary["p1_status"],
            "p2_status": primary["p2_status"],
            "p3_status": primary["p3_status"],
            "isolated_support_persists_through_p11": (
                primary["p2_checks"]["p9_matches_r_support"]
                and primary["p2_checks"]["p10_matches_r_support"]
                and not primary["p2_checks"]["p11_loses_r_support"]
            ),
            "isolated_normalized_atom_skeleton_persists_through_p11": checks[
                "isolated_normalized_atom_skeleton_persists"
            ],
            "isolated_normalized_atom_skeleton_hash": digest(
                sorted(isolated_skeletons[8])
            ),
        },
        "scope": (
            "exact finite semantic support through p=11; no chain-level sector, recurrence, "
            "or all-parameter theorem is claimed"
        ),
    }
    certificate["certificate_hash"] = digest(certificate)
    OUTPUT.write_text(
        json.dumps(certificate, indent=2) + "\n", encoding="utf-8", newline="\n"
    )
    print(json.dumps(certificate, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
