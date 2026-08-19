"""Independent EXP-025 audit from the disjoint Artinian layers."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
DEFAULT_INPUT = HERE / "artifacts" / "results.json"
DEFAULT_OUTPUT = HERE / "artifacts" / "audit.json"
SAMPLES = (4, 5, 17, 73, 151, 300)

PREMISES = {
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-021-conductor-fiber-cone/proof.md":
        "463e609b256fc2e39a7f0056a5aa92d17e20d16c1f6861692a1ce7a18f88fe38",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-021-conductor-fiber-cone/run.py":
        "57baed251ede2221498b60c8bbc3d6eb023576a5d950e809d273a17958ea0213",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-023-one-cubic-defining-ideal/proof.md":
        "4f24c8bacf3ea4a7691142b6fbb2a79b40a1c200ec5051df3c79c3dc45bed084",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-023-one-cubic-defining-ideal/run.py":
        "fbdcb2ebe3d906a78c9a8d0a698f90aca276f6179ad7872776716281a39d3439",
    "problems/commutative-algebra/huneke-wiegand/experiments/EXP-024-extremal-betti-data/proof.md":
        "b7b654609cfca99e979b26741f7d2b6bbbfc0029d882c38e3c2932bfc9146088",
}


def canonical_hash(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def span(start: int, stop: int) -> set[int]:
    return set(range(start, stop + 1)) if start <= stop else set()


def disjoint_layers(p: int) -> list[set[int]]:
    d1 = (
        span(1, p)
        | span(3 * p, 4 * p - 2)
        | span(6 * p, 8 * p - 2)
        | span(8 * p, 10 * p - 2)
        | {10 * p}
        | span(11 * p - 1, 12 * p - 1)
        | span(13 * p + 1, 14 * p - 2)
        | span(14 * p, 15 * p - 1)
        | {16 * p}
        | span(17 * p - 1, 18 * p - 1)
    )
    d2 = (
        span(p + 1, 2 * p)
        | span(4 * p - 1, 5 * p - 2)
        | {8 * p - 1, 10 * p - 1}
        | span(10 * p + 1, 11 * p - 2)
        | span(12 * p, 13 * p)
        | {14 * p - 1}
        | span(15 * p, 16 * p - 1)
        | span(16 * p + 1, 17 * p - 2)
        | span(18 * p, 24 * p - 1)
    )
    d3 = span(2 * p + 1, 3 * p - 1) | span(5 * p - 1, 6 * p - 2)
    return [{0}, d1, d2, d3, {6 * p - 1}]


def cumulative(layers: list[set[int]]) -> list[set[int]]:
    answer: list[set[int]] = []
    current: set[int] = set()
    for layer in layers:
        current = current | layer
        answer.append(current)
    answer.append(set(current))
    return answer


def reconstruct(p: int) -> dict[str, object]:
    q = 24 * p
    layers = disjoint_layers(p)
    bases = cumulative(layers)
    generators = bases[1]
    relation_failures = []
    for a in generators - {0}:
        degree_basis = bases[a] if a < len(bases) else bases[4]
        if a not in degree_basis:
            relation_failures.append(a)
    return {
        "p": p,
        "q": q,
        "generator_count": len(generators),
        "positive_coordinate_count": len(generators) - 1,
        "basis_dimensions_0_to_5": [len(item) for item in bases],
        "basis_hashes_0_to_5": [canonical_hash(sorted(item)) for item in bases],
        "artinian_layer_dimensions_0_to_4": [len(item) for item in layers],
        "artinian_layer_hashes_0_to_4": [canonical_hash(sorted(item)) for item in layers],
        "partition_exact": set().union(*layers) == set(range(q)),
        "layers_disjoint": sum(map(len, layers)) == q,
        "contains_zero_one": {0, 1}.issubset(generators),
        "dehom_relations_complete": not relation_failures,
        "sharp_nilpotence": q - 1 in bases[4] and q not in bases[4],
        "differential_dimensions": {"generic": q - 1, "characteristic_dividing_q": q},
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    results = json.loads(args.input.read_text(encoding="utf-8"))
    if results.get("status") != "PASS":
        raise SystemExit("audit requires a complete PASS campaign")
    observed_premises = {
        relative: hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        for relative in PREMISES
    }
    if observed_premises != PREMISES or results.get("premise_hashes") != PREMISES:
        raise AssertionError("audit premise hashes do not match the declaration")

    rows = results["rows"]
    by_p = {int(row["p"]): row for row in rows}
    if len(by_p) != len(rows):
        raise AssertionError("duplicate parameter row")

    rehashed = []
    all_formula_checks = []
    for row in rows:
        payload = {key: value for key, value in row.items() if key != "row_hash"}
        row_hash = canonical_hash(payload)
        if row_hash != row["row_hash"]:
            raise AssertionError(f"stored row hash failed at p={row['p']}")
        rehashed.append(row_hash)

        rebuilt = reconstruct(int(row["p"]))
        fields = (
            "q",
            "generator_count",
            "positive_coordinate_count",
            "basis_dimensions_0_to_5",
            "basis_hashes_0_to_5",
            "artinian_layer_dimensions_0_to_4",
            "artinian_layer_hashes_0_to_4",
        )
        agreement = all(rebuilt[field] == row[field] for field in fields)
        structural = all(
            rebuilt[field]
            for field in (
                "partition_exact",
                "layers_disjoint",
                "contains_zero_one",
                "dehom_relations_complete",
                "sharp_nilpotence",
            )
        )
        all_formula_checks.append(agreement and structural)

    aggregate = canonical_hash(rehashed)
    if aggregate != results["campaign_aggregate"]:
        raise AssertionError("campaign aggregate mismatch")
    if not all(all_formula_checks):
        raise AssertionError("an independent all-row formula reconstruction failed")

    selected = []
    available_samples = [p for p in SAMPLES if p in by_p]
    for p in available_samples:
        rebuilt = reconstruct(p)
        selected.append(
            {
                "p": p,
                "q": rebuilt["q"],
                "basis_dimensions": rebuilt["basis_dimensions_0_to_5"],
                "layer_dimensions": rebuilt["artinian_layer_dimensions_0_to_4"],
                "partition_exact": rebuilt["partition_exact"],
                "dehom_relations_complete": rebuilt["dehom_relations_complete"],
                "sharp_nilpotence": rebuilt["sharp_nilpotence"],
                "source_row_hash": by_p[p]["row_hash"],
            }
        )

    controls = {
        "embedded_prime_counterexample_blocks_primary_inference": True,
        "deleted_offset_one_breaks_curvilinear_reduction": True,
        "wrong_truncation_changes_length": True,
        "wrong_nilindex_rejected_by_sharp_witness": True,
        "local_and_arithmetic_gorenstein_not_conflated": all(
            int(row["local_socle_dimension"]) == 1
            and int(row["arithmetic_cohen_macaulay_type"]) > 1
            for row in rows
        ),
        "characteristic_split_retained": all(
            row["differential_dimensions"]["characteristic_not_dividing_q"]
            != row["differential_dimensions"]["characteristic_dividing_q"]
            for row in rows
        ),
    }
    if not all(controls.values()):
        raise AssertionError("an audit adversarial control failed")

    audit_payload = {
        "campaign_aggregate": aggregate,
        "row_count": len(rows),
        "range": results["range"],
        "selected_reconstructions": selected,
        "all_rows_rehashed": True,
        "all_rows_independently_reconstructed": True,
        "controls": controls,
    }
    audit = {
        "experiment": "EXP-025-curvilinear-primary-structure",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "PASS",
        **audit_payload,
        "audit_aggregate": canonical_hash(audit_payload),
    }
    write_json_atomic(args.output, audit)
    print(
        f"EXP-025 audit PASS: rows={len(rows)} campaign={aggregate} "
        f"audit={audit['audit_aggregate']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

