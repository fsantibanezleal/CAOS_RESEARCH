"""Independent audit for EXP-024 extremal Betti data."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from copy import deepcopy
from pathlib import Path
from typing import Callable


HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
DEFAULT_RESULTS = HERE / "artifacts" / "results.json"
DEFAULT_AUDIT = HERE / "artifacts" / "audit.json"
DEFAULT_CHECKPOINT = HERE / "artifacts" / "checkpoint.json"
SAMPLES = (4, 5, 17, 73, 151, 300)

EXP021_AUDIT = EXPERIMENTS / "EXP-021-conductor-fiber-cone" / "artifacts" / "audit.json"
EXP023_RESULTS = EXPERIMENTS / "EXP-023-one-cubic-defining-ideal" / "artifacts" / "results.json"

PREMISE_PATHS = {
    "exp021_results": EXPERIMENTS / "EXP-021-conductor-fiber-cone" / "artifacts" / "results.json",
    "exp021_audit": EXPERIMENTS / "EXP-021-conductor-fiber-cone" / "artifacts" / "audit.json",
    "exp021_proof": EXPERIMENTS / "EXP-021-conductor-fiber-cone" / "proof.md",
    "exp023_results": EXPERIMENTS / "EXP-023-one-cubic-defining-ideal" / "artifacts" / "results.json",
    "exp023_audit": EXPERIMENTS / "EXP-023-one-cubic-defining-ideal" / "artifacts" / "audit.json",
    "exp023_symbolic": (
        EXPERIMENTS
        / "EXP-023-one-cubic-defining-ideal"
        / "artifacts"
        / "symbolic-certificate.json"
    ),
    "exp023_proof": EXPERIMENTS / "EXP-023-one-cubic-defining-ideal" / "proof.md",
}

PREMISE_SHA256 = {
    "exp021_results": "1fa45248cd8160af6539a26069e21d74023c39ebd18bff796660532766429e7c",
    "exp021_audit": "d479ffa6be2db2a1e2b465603b65e53fe6e4135fe025e37f45d97abbfe5a2571",
    "exp021_proof": "463e609b256fc2e39a7f0056a5aa92d17e20d16c1f6861692a1ce7a18f88fe38",
    "exp023_results": "e91a4e6acd9bbc243642c028eaba755b3cebf1a647f162634e579e6598944f44",
    "exp023_audit": "30deabe2aceb1791f2fe8458c7c78ffa2db6da3c87586cf1932545d7cae62180",
    "exp023_symbolic": "c2dd364126eb059f22c9356d4b99d0b4ae8a2c54db5e1dbff1d0ebfc43a48a6d",
    "exp023_proof": "4f24c8bacf3ea4a7691142b6fbb2a79b40a1c200ec5051df3c79c3dc45bed084",
}


def digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def verify_recorded_premises(recorded: object) -> None:
    if recorded != PREMISE_SHA256:
        raise AssertionError("recorded premise hashes do not match the frozen manifest")
    actual = {name: file_hash(path) for name, path in PREMISE_PATHS.items()}
    if actual != PREMISE_SHA256:
        raise AssertionError("current premise files do not match the frozen manifest")


def polynomial_coefficient(p: int, degree: int) -> int:
    """Independent coefficient extraction for (1-z)^(10p-1) h_p(z)."""
    c = 10 * p - 1
    h = (1, c, 12 * p, 2 * p - 1, 1)
    total = 0
    for h_degree, value in enumerate(h):
        choose = degree - h_degree
        if 0 <= choose <= c:
            total += value * ((-1) ** choose) * math.comb(c, choose)
    return total


def rebuild(p: int) -> dict[str, object]:
    n = 10 * p
    c = n - 1
    h = [1, c, 12 * p, 2 * p - 1, 1]
    socle = [0, 0, 10 * p, 0, 1]

    dimension_c_2 = 22 * p
    beta_1_2 = math.comb(n + 1, 2) - dimension_c_2
    beta_1_3 = 1
    dimension_j_3 = math.comb(n + 2, 3) - (24 * p - 1)
    beta_2_3 = n * beta_1_2 + beta_1_3 - dimension_j_3

    numerator_formula = 2 * p * (500 * p * p - 330 * p + 31)
    if numerator_formula % 3:
        raise AssertionError(f"p={p}: independent closed formula is not integral")
    closed_beta_2_3 = numerator_formula // 3
    coefficient_beta_2_3 = polynomial_coefficient(p, 3) + beta_1_3
    if beta_2_3 != closed_beta_2_3 or beta_2_3 != coefficient_beta_2_3:
        raise AssertionError(f"p={p}: independent beta_(2,3) routes disagree")

    penultimate = abs(polynomial_coefficient(p, c + 3))
    if penultimate != 8 * p:
        raise AssertionError(f"p={p}: independent penultimate coefficient mismatch")
    if polynomial_coefficient(p, c + 4) != (-1) ** c:
        raise AssertionError(f"p={p}: independent top coefficient mismatch")

    result: dict[str, object] = {
        "p": p,
        "variable_count": n,
        "codimension": c,
        "projective_dimension": c,
        "regularity": len(h) - 1,
        "h_vector": h,
        "socle_vector": socle,
        "beta_1_2": beta_1_2,
        "beta_1_3": beta_1_3,
        "beta_2_3": beta_2_3,
        "last_row": [[c, c + 2, 10 * p], [c, c + 4, 1]],
        "penultimate": [c - 1, c + 3, penultimate],
        "canonical_generator_degrees": {"-3": 1, "-1": 10 * p},
    }
    result["audit_row_hash"] = digest(result)
    return result


def validate_campaign_row(row: dict[str, object]) -> None:
    p = int(row["p"])
    expected = rebuild(p)
    observed = {
        "p": p,
        "variable_count": row["variable_count"],
        "codimension": row["codimension"],
        "projective_dimension": row["projective_dimension"],
        "regularity": row["regularity"],
        "h_vector": row["h_vector"],
        "socle_vector": row["socle_vector"],
        "beta_1_2": row["first_betti"]["beta_1_2"],
        "beta_1_3": row["first_betti"]["beta_1_3"],
        "beta_2_3": row["linear_first_syzygies"]["closed_formula"],
        "last_row": [
            [item["homological_degree"], item["internal_degree"], item["rank"]]
            for item in row["last_betti_row_nonzero_entries"]
        ],
        "penultimate": [
            row["penultimate_extremal"]["homological_degree"],
            row["penultimate_extremal"]["internal_degree"],
            row["penultimate_extremal"]["rank"],
        ],
        "canonical_generator_degrees": row["canonical_module_minimal_generator_degrees"],
    }
    expected_without_hash = expected.copy()
    expected_without_hash.pop("audit_row_hash")
    if observed != expected_without_hash:
        raise AssertionError(f"p={p}: independent row mismatch")
    if not all(row["comparisons"].values()) or not all(row["controls"].values()):
        raise AssertionError(f"p={p}: recorded comparison/control failure")
    if row["interior_betti_table_determined"] is not False:
        raise AssertionError(f"p={p}: full Betti table is overclaimed")


def verify_campaign(data: dict[str, object]) -> dict[int, dict[str, object]]:
    if data.get("status") != "COMPUTATIONAL_PASS":
        raise AssertionError("campaign is not a computational pass")
    rows = data.get("rows")
    if not isinstance(rows, list):
        raise AssertionError("campaign rows missing")
    by_p: dict[int, dict[str, object]] = {}
    row_hashes: list[str] = []
    for item in rows:
        if not isinstance(item, dict):
            raise AssertionError("invalid campaign row")
        unhashed = item.copy()
        recorded = unhashed.pop("row_hash", None)
        actual = digest(unhashed)
        if actual != recorded:
            raise AssertionError(f"p={item.get('p')}: campaign row hash mismatch")
        validate_campaign_row(item)
        p = int(item["p"])
        by_p[p] = item
        row_hashes.append(actual)
    if sorted(by_p) != list(range(4, 301)):
        raise AssertionError("campaign range is not exactly p=4,...,300")
    if digest(row_hashes) != data.get("campaign_aggregate"):
        raise AssertionError("campaign aggregate mismatch")
    return by_p


def expect_rejection(row: dict[str, object], mutate: Callable[[dict[str, object]], None]) -> bool:
    corrupted = deepcopy(row)
    mutate(corrupted)
    try:
        validate_campaign_row(corrupted)
    except AssertionError:
        return True
    return False


def verify_imported_selected(by_p: dict[int, dict[str, object]]) -> dict[str, object]:
    exp021 = json.loads(EXP021_AUDIT.read_text(encoding="utf-8"))
    selected021 = {int(item["p"]): item for item in exp021["selected"]}
    if sorted(selected021) != list(SAMPLES):
        raise AssertionError("EXP-021 audit samples changed")
    for p in SAMPLES:
        row = by_p[p]
        source = selected021[p]
        if source["artinian_h_vector_through_degree_5"][:5] != row["h_vector"]:
            raise AssertionError(f"p={p}: selected EXP-021 h-vector mismatch")
        if source["socle_vector_through_degree_5"][:5] != row["socle_vector"]:
            raise AssertionError(f"p={p}: selected EXP-021 socle mismatch")

    exp023 = json.loads(EXP023_RESULTS.read_text(encoding="utf-8"))
    checked023 = 0
    for source in exp023["rows"]:
        p = int(source["p"])
        target = by_p[p]["first_betti"]
        source_betti = source["first_betti_row_degrees_2_to_5"]
        if target != {"beta_1_2": source_betti["2"], "beta_1_3": source_betti["3"]}:
            raise AssertionError(f"p={p}: EXP-023 first Betti mismatch")
        checked023 += 1
    return {"exp021_selected_rows": len(SAMPLES), "exp023_campaign_rows": checked023}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--output", type=Path, default=DEFAULT_AUDIT)
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
    args = parser.parse_args()

    data = json.loads(args.results.read_text(encoding="utf-8"))
    verify_recorded_premises(data.get("premise_sha256"))
    by_p = verify_campaign(data)
    checkpoint = json.loads(args.checkpoint.read_text(encoding="utf-8"))
    expected_row_hashes = [str(by_p[p]["row_hash"]) for p in sorted(by_p)]
    if checkpoint != {
        "experiment": "EXP-024-extremal-betti-data",
        "status": "COMPLETE",
        "range": {"first": 4, "last": 300},
        "completed_through": 300,
        "row_hashes": expected_row_hashes,
    }:
        raise AssertionError("campaign checkpoint does not match the complete results")
    imported = verify_imported_selected(by_p)
    base = by_p[4]
    controls = {
        "false_regularity_rejected": expect_rejection(
            base, lambda row: row.__setitem__("regularity", 3)
        ),
        "false_projective_dimension_rejected": expect_rejection(
            base, lambda row: row.__setitem__("projective_dimension", 38)
        ),
        "perturbed_beta_2_3_rejected": expect_rejection(
            base,
            lambda row: row["linear_first_syzygies"].__setitem__("closed_formula", 17897),
        ),
        "deleted_last_socle_entry_rejected": expect_rejection(
            base, lambda row: row["last_betti_row_nonzero_entries"].pop()
        ),
        "perturbed_penultimate_rejected": expect_rejection(
            base, lambda row: row["penultimate_extremal"].__setitem__("rank", 31)
        ),
        "full_table_overclaim_rejected": expect_rejection(
            base, lambda row: row.__setitem__("interior_betti_table_determined", True)
        ),
    }
    corrupted_premises = deepcopy(data["premise_sha256"])
    corrupted_premises["exp021_results"] = "0" * 64
    try:
        verify_recorded_premises(corrupted_premises)
    except AssertionError:
        controls["corrupted_premise_hash_rejected"] = True
    else:
        controls["corrupted_premise_hash_rejected"] = False
    if not all(controls.values()):
        raise AssertionError(f"audit control failure: {controls}")

    selected = [rebuild(p) for p in SAMPLES]
    result = {
        "experiment": "EXP-024-extremal-betti-data",
        "status": "INDEPENDENT_AUDIT_PASS",
        "campaign_file_sha256": file_hash(args.results),
        "checkpoint_file_sha256": file_hash(args.checkpoint),
        "campaign_rows_rehashed_and_rebuilt": len(by_p),
        "selected_parameters": list(SAMPLES),
        "selected": selected,
        "imported_premise_cross_checks": imported,
        "premise_sha256": data["premise_sha256"],
        "controls": controls,
        "audit_aggregate": digest([item["audit_row_hash"] for item in selected]),
    }
    write_json_atomic(args.output, result)
    print(
        "EXP-024 independent audit pass: "
        f"{len(by_p)} rows; aggregate={result['audit_aggregate']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
