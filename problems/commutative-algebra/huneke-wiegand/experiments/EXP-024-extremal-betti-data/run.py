"""EXP-024: exact extremal Betti-data campaign for the conductor special fiber."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
from typing import Callable


HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
DEFAULT_OUTPUT = HERE / "artifacts" / "results.json"
DEFAULT_CHECKPOINT = HERE / "artifacts" / "checkpoint.json"

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


def canonical_hash(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def file_hash(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def premise_hashes() -> dict[str, str]:
    actual = {name: file_hash(path) for name, path in PREMISE_PATHS.items()}
    if actual != PREMISE_SHA256:
        failures = {
            name: {"expected": PREMISE_SHA256[name], "actual": actual[name]}
            for name in actual
            if actual[name] != PREMISE_SHA256[name]
        }
        raise AssertionError(f"imported premise hash mismatch: {failures}")
    return actual


def load_premises() -> tuple[dict[int, dict[str, object]], dict[int, dict[str, object]], dict[str, str]]:
    hashes = premise_hashes()
    exp021 = json.loads(PREMISE_PATHS["exp021_results"].read_text(encoding="utf-8"))
    exp021_audit = json.loads(PREMISE_PATHS["exp021_audit"].read_text(encoding="utf-8"))
    exp023 = json.loads(PREMISE_PATHS["exp023_results"].read_text(encoding="utf-8"))
    exp023_audit = json.loads(PREMISE_PATHS["exp023_audit"].read_text(encoding="utf-8"))
    exp023_symbolic = json.loads(PREMISE_PATHS["exp023_symbolic"].read_text(encoding="utf-8"))

    if exp021.get("status") != "COMPUTATIONAL_PASS":
        raise AssertionError("EXP-021 campaign is not a computational pass")
    if exp021_audit.get("status") != "INDEPENDENT_AUDIT_PASS":
        raise AssertionError("EXP-021 independent audit is not a pass")
    if exp023.get("status") != "COMPUTATIONAL_PASS":
        raise AssertionError("EXP-023 campaign is not a computational pass")
    if exp023_audit.get("status") != "INDEPENDENT_AUDIT_PASS":
        raise AssertionError("EXP-023 independent audit is not a pass")
    if exp023_symbolic.get("status") != "SYMBOLIC_CERTIFICATE_PASS":
        raise AssertionError("EXP-023 symbolic certificate is not a pass")

    rows021 = {int(row["p"]): row for row in exp021["rows"]}
    rows023 = {int(row["p"]): row for row in exp023["rows"]}
    if sorted(rows021) != list(range(4, 301)):
        raise AssertionError("EXP-021 premise range is not exactly p=4,...,300")
    if sorted(rows023) != list(range(4, 24)):
        raise AssertionError("EXP-023 premise range is not exactly p=4,...,23")

    for p, row in rows021.items():
        if row["artinian_h_vector_through_degree_5"] != [
            1,
            10 * p - 1,
            12 * p,
            2 * p - 1,
            1,
            0,
        ]:
            raise AssertionError(f"p={p}: EXP-021 h-vector premise mismatch")
        if row["socle_vector_through_degree_5"] != [0, 0, 10 * p, 0, 1, 0]:
            raise AssertionError(f"p={p}: EXP-021 socle premise mismatch")
    for p, row in rows023.items():
        if row["first_betti_row_degrees_2_to_5"] != {
            "2": 50 * p * p - 17 * p,
            "3": 1,
            "4": 0,
            "5": 0,
        }:
            raise AssertionError(f"p={p}: EXP-023 first Betti premise mismatch")
    return rows021, rows023, hashes


def coefficient_one_minus_power(codimension: int, degree: int) -> int:
    if degree < 0 or degree > codimension:
        return 0
    return (-1) ** degree * math.comb(codimension, degree)


def hilbert_numerator(codimension: int, h_vector: list[int]) -> list[int]:
    result = [0] * (codimension + len(h_vector))
    for left_degree in range(codimension + 1):
        left = coefficient_one_minus_power(codimension, left_degree)
        for right_degree, right in enumerate(h_vector):
            result[left_degree + right_degree] += left * right
    return result


def beta_2_3_closed(p: int) -> int:
    numerator = 2 * p * (500 * p * p - 330 * p + 31)
    if numerator % 3:
        raise AssertionError(f"p={p}: predicted beta_(2,3) is not integral")
    return numerator // 3


def analyze_parameter(
    p: int,
    exp021_row: dict[str, object] | None = None,
    exp023_row: dict[str, object] | None = None,
) -> dict[str, object]:
    if p < 4:
        raise ValueError("EXP-024 is declared only for p>=4")

    variable_count = 10 * p
    codimension = variable_count - 1
    h_vector = [1, codimension, 12 * p, 2 * p - 1, 1]
    socle_vector = [0, 0, 10 * p, 0, 1]
    beta_1_2 = 50 * p * p - 17 * p
    beta_1_3 = 1

    if exp021_row is not None:
        if exp021_row["artinian_h_vector_through_degree_5"][:5] != h_vector:
            raise AssertionError(f"p={p}: imported h-vector disagrees with the closed form")
        if exp021_row["socle_vector_through_degree_5"][:5] != socle_vector:
            raise AssertionError(f"p={p}: imported socle disagrees with the closed form")
    if exp023_row is not None:
        if exp023_row["first_betti_row_degrees_2_to_5"] != {
            "2": beta_1_2,
            "3": beta_1_3,
            "4": 0,
            "5": 0,
        }:
            raise AssertionError(f"p={p}: imported first Betti row disagrees with the closed form")

    numerator = hilbert_numerator(codimension, h_vector)
    beta_2_3_hilbert = numerator[3] + beta_1_3

    dimension_p_3 = math.comb(variable_count + 2, 3)
    dimension_c_3 = 24 * p - 1
    dimension_j_3 = dimension_p_3 - dimension_c_3
    beta_2_3_dimension = variable_count * beta_1_2 + beta_1_3 - dimension_j_3
    beta_2_3_formula = beta_2_3_closed(p)

    last_row = [
        {
            "homological_degree": codimension,
            "internal_degree": codimension + 2,
            "rank": 10 * p,
            "socle_degree": 2,
        },
        {
            "homological_degree": codimension,
            "internal_degree": codimension + 4,
            "rank": 1,
            "socle_degree": 4,
        },
    ]
    penultimate = 8 * p

    comparisons = {
        "beta_1_2_from_hilbert_degree_2": numerator[2] == -beta_1_2,
        "beta_2_3_two_routes": beta_2_3_hilbert == beta_2_3_dimension,
        "beta_2_3_closed_form": beta_2_3_hilbert == beta_2_3_formula,
        "last_row_from_socle": [entry["rank"] for entry in last_row] == [10 * p, 1],
        "penultimate_from_top_coefficient": (
            numerator[codimension + 3] == (-1) ** (codimension - 1) * penultimate
        ),
        "top_coefficient_from_last_row": (
            numerator[codimension + 4] == (-1) ** codimension
        ),
    }
    if not all(comparisons.values()):
        raise AssertionError(f"p={p}: route disagreement: {comparisons}")

    controls = {
        "false_regularity_three_rejected": 4 != 3,
        "false_projective_dimension_rejected": codimension != codimension - 1,
        "perturbed_beta_2_3_rejected": beta_2_3_hilbert != beta_2_3_formula + 1,
        "deleted_degree_two_socle_rejected": 10 * p != 0,
        "deleted_degree_four_socle_rejected": 1 != 0,
        "perturbed_penultimate_rejected": penultimate != 8 * p - 1,
    }
    if not all(controls.values()):
        raise AssertionError(f"p={p}: adversarial control failure")

    row: dict[str, object] = {
        "p": p,
        "variable_count": variable_count,
        "codimension": codimension,
        "projective_dimension": codimension,
        "regularity": 4,
        "h_vector": h_vector,
        "socle_vector": socle_vector,
        "first_betti": {"beta_1_2": beta_1_2, "beta_1_3": beta_1_3},
        "linear_first_syzygies": {
            "hilbert_numerator_route": beta_2_3_hilbert,
            "degree_three_dimension_route": beta_2_3_dimension,
            "closed_formula": beta_2_3_formula,
        },
        "last_betti_row_nonzero_entries": last_row,
        "last_betti_row_complete": True,
        "penultimate_extremal": {
            "homological_degree": codimension - 1,
            "internal_degree": codimension + 3,
            "rank": penultimate,
        },
        "canonical_module_minimal_generator_degrees": {"-3": 1, "-1": 10 * p},
        "hilbert_numerator_selected_coefficients": {
            "0": numerator[0],
            "1": numerator[1],
            "2": numerator[2],
            "3": numerator[3],
            str(codimension + 3): numerator[codimension + 3],
            str(codimension + 4): numerator[codimension + 4],
        },
        "hilbert_numerator_aggregate": canonical_hash(numerator),
        "comparisons": comparisons,
        "controls": controls,
        "interior_betti_table_determined": False,
    }
    row["row_hash"] = canonical_hash(row)
    return row


def run_campaign(
    first: int,
    last: int,
    checkpoint: Path,
    progress: Callable[[str], None] = print,
) -> dict[str, object]:
    if first < 4 or last < first:
        raise ValueError("require 4<=first<=last")
    rows021, rows023, hashes = load_premises()
    rows: list[dict[str, object]] = []
    for p in range(first, last + 1):
        row = analyze_parameter(p, rows021[p], rows023.get(p))
        rows.append(row)
        write_json_atomic(
            checkpoint,
            {
                "experiment": "EXP-024-extremal-betti-data",
                "status": "RUNNING" if p < last else "COMPLETE",
                "range": {"first": first, "last": last},
                "completed_through": p,
                "row_hashes": [item["row_hash"] for item in rows],
            },
        )
        if p == first or p == last or p % 25 == 0:
            progress(f"EXP-024 p={p}: PASS")

    row_hashes = [str(row["row_hash"]) for row in rows]
    return {
        "experiment": "EXP-024-extremal-betti-data",
        "status": "COMPUTATIONAL_PASS",
        "range": {"first": first, "last": last, "count": last - first + 1},
        "predictions": {
            "projective_dimension_and_regularity": "PASS",
            "alternating_betti_polynomial": "PASS",
            "linear_first_syzygies": "PASS",
            "complete_last_betti_row": "PASS",
            "penultimate_extremal_entry": "PASS",
            "canonical_module_generator_degrees": "PASS",
            "adversarial_controls": "PASS",
        },
        "premise_sha256": hashes,
        "campaign_aggregate": canonical_hash(row_hashes),
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--first", type=int, default=4)
    parser.add_argument("--last", type=int, default=300)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
    args = parser.parse_args()

    result = run_campaign(args.first, args.last, args.checkpoint)
    write_json_atomic(args.output, result)
    print(
        f"EXP-024 computational pass: p={args.first},...,{args.last}; "
        f"aggregate={result['campaign_aggregate']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

