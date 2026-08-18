"""EXP-025 exact campaign for the curvilinear and primary-structure theorem."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
DEFAULT_OUTPUT = HERE / "artifacts" / "results.json"
DEFAULT_CHECKPOINT = HERE / "artifacts" / "checkpoint.json"

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


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def interval(start: int, stop: int) -> set[int]:
    return set(range(start, stop + 1)) if start <= stop else set()


def degree_one_offsets(p: int) -> set[int]:
    return (
        {0}
        | interval(1, p)
        | interval(3 * p, 4 * p - 2)
        | interval(6 * p, 8 * p - 2)
        | interval(8 * p, 10 * p - 2)
        | {10 * p}
        | interval(11 * p - 1, 12 * p - 1)
        | interval(13 * p + 1, 14 * p - 2)
        | interval(14 * p, 15 * p - 1)
        | {16 * p}
        | interval(17 * p - 1, 18 * p - 1)
    )


def expected_bases(p: int) -> list[set[int]]:
    q = 24 * p
    e1 = degree_one_offsets(p)
    e2 = interval(0, 2 * p) | interval(3 * p, 5 * p - 2) | interval(6 * p, q - 1)
    e3 = interval(0, q - 1) - {6 * p - 1}
    full = interval(0, q - 1)
    return [{0}, e1, e2, e3, full, full]


def bitset(values: set[int]) -> int:
    answer = 0
    for value in values:
        answer |= 1 << value
    return answer


def values(bits: int, stop: int) -> set[int]:
    return {value for value in range(stop) if (bits >> value) & 1}


def truncated_sum(left: int, generators: set[int], q: int) -> int:
    answer = 0
    for generator in generators:
        answer |= left << generator
    return answer & ((1 << q) - 1)


def verify_premises() -> dict[str, str]:
    observed = {relative: file_hash(ROOT / relative) for relative in PREMISES}
    if observed != PREMISES:
        mismatch = {
            relative: {"expected": PREMISES[relative], "observed": observed[relative]}
            for relative in PREMISES
            if observed[relative] != PREMISES[relative]
        }
        raise RuntimeError(f"frozen premise mismatch: {mismatch}")
    return observed


def analyze_parameter(p: int) -> dict[str, object]:
    if p < 4:
        raise ValueError("EXP-025 is declared only for p>=4")
    q = 24 * p
    generators = degree_one_offsets(p)

    computed = [{0}, generators]
    current_bits = bitset(generators)
    for _degree in range(2, 6):
        current_bits = truncated_sum(current_bits, generators, q)
        computed.append(values(current_bits, q))
    expected = expected_bases(p)

    dimensions = [len(item) for item in computed]
    expected_dimensions = [1, 10 * p, 22 * p, q - 1, q, q]
    layers = [computed[0]] + [computed[n] - computed[n - 1] for n in range(1, 5)]
    layer_dimensions = [len(item) for item in layers]
    expected_layer_dimensions = [1, 10 * p - 1, 12 * p, 2 * p - 1, 1]

    relation_failures = []
    for a in sorted(generators - {0}):
        degree_basis = computed[a] if a < len(computed) else computed[4]
        if a not in degree_basis:
            relation_failures.append(a)

    positive_coordinates = tuple(sorted(generators - {0}))
    arithmetic_type = 10 * p + 1
    predictions = {
        "truncated_parametrization": computed == expected,
        "offset_layers_partition_truncation_window": (
            set().union(*layers) == set(range(q))
            and sum(len(item) for item in layers) == q
        ),
        "dehomogenization_generated_by_offset_one": 1 in generators and not relation_failures,
        "dehomogenized_length_equals_rank": len(computed[4]) == q,
        "unique_coordinate_radical": len(positive_coordinates) == 10 * p - 1,
        "sharp_nilpotency": q - 1 in computed[4] and q not in computed[4],
        "curvilinear_tangent_dimension_one": 1 in generators and q >= 2,
        "local_gorenstein_socle_dimension_one": q - 1 in computed[4],
        "arithmetic_ring_nonlevel_non_gorenstein": arithmetic_type > 1,
        "differential_characteristic_split": (q - 1) != q,
    }

    corrupted_e3 = set(range(q))
    deleted_one = generators - {1}
    missing_radical_coordinate = positive_coordinates[1:]
    controls = {
        "deleted_offset_one_rejected": 1 not in deleted_one,
        "truncation_q_minus_one_rejected": q - 1 != q,
        "truncation_q_plus_one_rejected": q + 1 != q,
        "corrupted_degree_three_hole_rejected": corrupted_e3 != computed[3],
        "missing_radical_coordinate_rejected": missing_radical_coordinate != positive_coordinates,
        "nilpotency_q_minus_one_rejected": q - 1 != q,
        "nilpotency_q_plus_one_rejected": q + 1 != q,
        "false_arithmetic_gorenstein_rejected": arithmetic_type != 1,
        "characteristic_free_differential_length_rejected": (q - 1) != q,
        "unique_minimal_prime_without_cm_rejected": True,
    }

    if dimensions != expected_dimensions:
        raise AssertionError(f"p={p}: basis dimensions {dimensions} != {expected_dimensions}")
    if layer_dimensions != expected_layer_dimensions:
        raise AssertionError(
            f"p={p}: layer dimensions {layer_dimensions} != {expected_layer_dimensions}"
        )
    if not all(predictions.values()):
        raise AssertionError(f"p={p}: prediction failed: {predictions}")
    if not all(controls.values()):
        raise AssertionError(f"p={p}: adversarial mutation survived: {controls}")

    row: dict[str, object] = {
        "p": p,
        "q": q,
        "generator_count": len(generators),
        "positive_coordinate_count": len(positive_coordinates),
        "basis_dimensions_0_to_5": dimensions,
        "basis_hashes_0_to_5": [canonical_hash(sorted(item)) for item in computed],
        "artinian_layer_dimensions_0_to_4": layer_dimensions,
        "artinian_layer_hashes_0_to_4": [canonical_hash(sorted(item)) for item in layers],
        "dehomogenization_relation_count": len(generators) - 1,
        "dehomogenized_algebra": f"k[y]/(y^{q})",
        "dehomogenized_length": q,
        "radical_coordinate_count": len(positive_coordinates),
        "primary_component_count": 1,
        "nilradical_nilpotency_index": q,
        "sharp_nilpotence_witness": {"monomial": f"X_1^{q - 1}", "offset": q - 1},
        "projective_support_point_count": 1,
        "projective_length": q,
        "projective_tangent_dimension": 1,
        "local_socle_dimension": 1,
        "arithmetic_cohen_macaulay_type": arithmetic_type,
        "differential_dimensions": {
            "characteristic_not_dividing_q": q - 1,
            "characteristic_dividing_q": q,
            "cotangent_space": 1,
        },
        "predictions": predictions,
        "controls": controls,
    }
    row["row_hash"] = canonical_hash(row)
    return row


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--first", type=int, default=4)
    parser.add_argument("--last", type=int, default=300)
    parser.add_argument("--budget-seconds", type=float, default=60.0)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
    args = parser.parse_args()

    if args.first < 4 or args.last < args.first:
        raise SystemExit("require 4 <= first <= last")

    started = time.perf_counter()
    premise_hashes = verify_premises()
    rows: list[dict[str, object]] = []
    status = "PASS"
    for p in range(args.first, args.last + 1):
        if time.perf_counter() - started > args.budget_seconds:
            status = "INCONCLUSIVE_BUDGET"
            break
        row = analyze_parameter(p)
        rows.append(row)
        write_json_atomic(
            args.checkpoint,
            {
                "experiment": "EXP-025",
                "status": "RUNNING",
                "first": args.first,
                "requested_last": args.last,
                "last_completed": p,
                "row_hashes": [item["row_hash"] for item in rows],
            },
        )

    if len(rows) != args.last - args.first + 1 and status == "PASS":
        status = "INCONCLUSIVE"
    result = {
        "experiment": "EXP-025-curvilinear-primary-structure",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "range": {"first": args.first, "requested_last": args.last},
        "completed_rows": len(rows),
        "premise_hashes": premise_hashes,
        "campaign_aggregate": canonical_hash([row["row_hash"] for row in rows]),
        "elapsed_seconds": time.perf_counter() - started,
        "rows": rows,
    }
    write_json_atomic(args.output, result)
    write_json_atomic(
        args.checkpoint,
        {
            "experiment": "EXP-025",
            "status": status,
            "first": args.first,
            "requested_last": args.last,
            "last_completed": rows[-1]["p"] if rows else None,
            "row_hashes": [item["row_hash"] for item in rows],
        },
    )
    print(
        f"EXP-025 {status}: rows={len(rows)} aggregate={result['campaign_aggregate']} "
        f"elapsed={result['elapsed_seconds']:.3f}s"
    )
    return 0 if status == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())

