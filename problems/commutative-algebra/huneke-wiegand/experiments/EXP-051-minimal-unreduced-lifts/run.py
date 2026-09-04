"""EXP-051 selects simple exact Bockstein lifts before quotient normalization."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import time
from pathlib import Path
from types import ModuleType


HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
EXP047 = EXPERIMENTS / "EXP-047-relative-kernel-smith"
EXP049 = EXPERIMENTS / "EXP-049-exact-chain-lifts"
EXP050 = EXPERIMENTS / "EXP-050-corrected-bockstein-lifts"
DEFAULT_OUTPUT = HERE / "artifacts" / "results.json"
INCLUSIONS = ((58, 59), (58, 62))
PREMISES = {
    EXP047 / "artifacts" / "results.json": (
        "f78d251ae1746a88d1190756572aa251b9daf70ceb103cef9765c6d73b26f46c"
    ),
    EXP049 / "artifacts" / "results.json": (
        "567f554abaa1456133a4c0cd475d1848dad92a36dd8b9412381fe2fab9fc39b7"
    ),
    EXP050 / "run.py": "9a7ccb9d5a1fcea24b4e9adaf7b8b1946635ad20233b7ac15301f46b8109a07e",
    EXP050 / "artifacts" / "results.json": (
        "2dc8f85097171e24f4080ce25684127914d86661a6291bab69fb334c2c987983"
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify_premises() -> dict[str, str]:
    actual = {str(path.relative_to(EXPERIMENTS)): sha256(path) for path in PREMISES}
    expected = {
        str(path.relative_to(EXPERIMENTS)): expected_hash
        for path, expected_hash in PREMISES.items()
    }
    if actual != expected:
        raise AssertionError({"premise_hash_mismatch": {"actual": actual, "expected": expected}})
    return actual


def sparse(values: list[int]) -> list[list[int]]:
    return [[index, value] for index, value in enumerate(values) if value]


def candidate_score(boundary: list[int], cycle: int) -> tuple[int, int, int, str]:
    return (
        sum(bool(value) for value in boundary),
        max(map(abs, boundary), default=0),
        cycle.bit_count(),
        digest(cycle),
    )


def select_pair(
    *, exp050: ModuleType, columns: list[list[list[int]]], row_count: int,
    formula_chains: list[list[int]], high: bool, reverse: bool
) -> dict[str, object]:
    bits = exp050.column_bits(columns)
    image_basis = exp050.canonical_rref(bits)
    best_by_class: dict[int, dict[str, object]] = {}
    candidate_count = 0
    for cycle in exp050.kernel_combinations(bits, high=high, reverse=reverse):
        doubled = exp050.column_sum(columns, cycle, row_count)
        if any(value & 1 for value in doubled):
            raise AssertionError("binary kernel cycle has odd boundary")
        boundary = [value // 2 for value in doubled]
        parity = sum(1 << row for row, value in enumerate(boundary) if value & 1)
        quotient = exp050.reduce_quotient(parity, image_basis)
        if not quotient:
            continue
        candidate_count += 1
        score = candidate_score(boundary, cycle)
        current = best_by_class.get(quotient)
        if current is None or score < tuple(current["score"]):
            best_by_class[quotient] = {
                "quotient_class": quotient,
                "score": list(score),
                "cycle": cycle,
                "boundary": boundary,
            }
    if len(best_by_class) < 2:
        raise AssertionError({"nonzero_classes": len(best_by_class)})

    pair_options = []
    for left, right in itertools.combinations(best_by_class.values(), 2):
        quotient_basis = exp050.canonical_rref(
            [int(left["quotient_class"]), int(right["quotient_class"])]
        )
        if len(quotient_basis) != 2:
            continue
        aggregate = (
            int(left["score"][0]) + int(right["score"][0]),
            max(int(left["score"][1]), int(right["score"][1])),
            int(left["score"][2]) + int(right["score"][2]),
            str(left["score"][3]) + str(right["score"][3]),
        )
        pair_options.append((aggregate, left, right, quotient_basis))
    if not pair_options:
        raise AssertionError("no independent quotient pair")
    _, left, right, quotient_basis = min(pair_options, key=lambda item: item[0])

    formula_quotients = [
        exp050.reduce_quotient(sum(1 << row for row in chain), image_basis)
        for chain in formula_chains
    ]
    if quotient_basis != exp050.canonical_rref(formula_quotients):
        raise AssertionError("selected pair does not span the EXP-049 formula classes")

    selected = []
    for record in sorted((left, right), key=lambda item: tuple(item["score"])):
        cycle = int(record["cycle"])
        boundary = list(record["boundary"])
        cycle_vector = [int((cycle >> column) & 1) for column in range(len(columns))]
        if exp050.multiply(columns, cycle_vector, row_count) != [2 * value for value in boundary]:
            raise AssertionError("selected exact identity fails")
        selected.append(
            {
                "quotient_class_rows": list(exp050.bit_indices(int(record["quotient_class"]))),
                "quotient_class_hash": digest(int(record["quotient_class"])),
                "cycle_columns": list(exp050.bit_indices(cycle)),
                "cycle_hash": digest(cycle),
                "cycle_support_size": cycle.bit_count(),
                "boundary": sparse(boundary),
                "boundary_hash": digest(boundary),
                "boundary_support_size": sum(bool(value) for value in boundary),
                "boundary_max_abs": max(map(abs, boundary), default=0),
                "exact_identity": True,
            }
        )
    return {
        "order": "high-reverse" if high and reverse else "low-forward",
        "kernel_dimension": len(exp050.kernel_combinations(bits, high=high, reverse=reverse)),
        "nonzero_candidate_count": candidate_count,
        "nonzero_quotient_classes_seen": len(best_by_class),
        "selected": selected,
        "selected_subspace_hash": digest(quotient_basis),
    }


def affine(values: list[int]) -> list[int] | None:
    for slope in range(-100, 101):
        intercept = values[0] - 8 * slope
        if all(value == slope * p + intercept for p, value in zip(range(8, 12), values, strict=True)):
            return [slope, intercept]
    return None


def classify(rows: list[dict[str, object]]) -> dict[str, object]:
    full = [int(row["p"]) for row in rows] == [8, 9, 10, 11]
    if not full:
        return {
            "p1_status": "NOT_EVALUATED",
            "p2_status": "NOT_EVALUATED",
            "p3_status": "NOT_EVALUATED",
            "p3_details": {},
        }
    primary_selections = [
        selected
        for row in rows
        for inclusion in row["inclusions"]
        for selected in inclusion["primary"]["selected"]
    ]
    audit_selections = [
        selected
        for row in rows
        for inclusion in row["inclusions"]
        for selected in inclusion["audit"]["selected"]
    ]
    selections = primary_selections + audit_selections
    p1 = all(
        selected["exact_identity"]
        and int(selected["boundary_support_size"]) <= 8 * int(selected["p"])
        and int(selected["boundary_max_abs"]) <= 2
        for selected in selections
    )
    p2 = all(int(selected["cycle_support_size"]) <= 4 * int(selected["p"]) for selected in selections)
    details: dict[str, object] = {}
    p3 = True
    for source, target in INCLUSIONS:
        groups = [
            sorted(
                next(
                    inclusion for inclusion in row["inclusions"]
                    if (int(inclusion["source_mask"]), int(inclusion["target_mask"])) == (source, target)
                )["primary"]["selected"],
                key=lambda selected: (
                    int(selected["boundary_support_size"]),
                    int(selected["cycle_support_size"]),
                ),
            )
            for row in rows
        ]
        boundary_series = [
            [int(group[index]["boundary_support_size"]) for group in groups] for index in range(2)
        ]
        cycle_series = [
            [int(group[index]["cycle_support_size"]) for group in groups] for index in range(2)
        ]
        boundary_affine = [affine(series) for series in boundary_series]
        cycle_affine = [affine(series) for series in cycle_series]
        passes = all(value is not None for value in boundary_affine + cycle_affine)
        p3 &= passes
        details[f"{source}->{target}"] = {
            "boundary_support_series": boundary_series,
            "boundary_affine_slope_intercept": boundary_affine,
            "cycle_support_series": cycle_series,
            "cycle_affine_slope_intercept": cycle_affine,
            "passes": passes,
        }
    return {
        "p1_status": "PASS_FINITE" if p1 else "REFUTED",
        "p2_status": "PASS_FINITE" if p2 else "REFUTED",
        "p3_status": "PASS_FINITE" if p3 else "REFUTED",
        "p3_details": details,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p-min", type=int, default=8)
    parser.add_argument("--p-max", type=int, default=11)
    parser.add_argument("--budget-seconds", type=float, default=60.0)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if args.p_min < 8 or args.p_max > 11 or args.p_min > args.p_max:
        raise ValueError("declared range is 8<=p_min<=p_max<=11")
    started = time.monotonic()
    premises = verify_premises()
    exp050 = load_module("exp050_for_exp051", EXP050 / "run.py")
    exp049 = json.loads((EXP049 / "artifacts" / "results.json").read_text(encoding="utf-8"))
    formula_records = {
        (int(row["p"]), int(inclusion["source_mask"]), int(inclusion["target_mask"])): inclusion
        for row in exp049["rows"]
        for inclusion in row["inclusions"]
    }
    result: dict[str, object] = {
        "experiment": "EXP-051",
        "route": "minimum-complexity exact lifts before quotient normalization",
        "status": "RUNNING",
        "parameters": {
            "p_min": args.p_min,
            "p_max": args.p_max,
            "budget_seconds": args.budget_seconds,
        },
        "premise_hashes": premises,
        "rows": [],
    }
    write_json_atomic(args.output, result)
    for p in range(args.p_min, args.p_max + 1):
        p_record: dict[str, object] = {"p": p, "inclusions": []}
        for source, target in INCLUSIONS:
            print(f"p={p} {source}->{target} enumerate exact binary lifts", flush=True)
            path = EXP047 / "artifacts" / f"relative-p{p}-m{source}-m{target}.json"
            relative = json.loads(path.read_text(encoding="utf-8"))
            columns = relative["matrix_columns"]
            formulas = [
                list(map(int, chain["chain_rows"]))
                for chain in formula_records[p, source, target]["chains"]
            ]
            primary = select_pair(
                exp050=exp050,
                columns=columns,
                row_count=int(relative["matrix_shape"][0]),
                formula_chains=formulas,
                high=False,
                reverse=False,
            )
            audit = select_pair(
                exp050=exp050,
                columns=columns,
                row_count=int(relative["matrix_shape"][0]),
                formula_chains=formulas,
                high=True,
                reverse=True,
            )
            for route in (primary, audit):
                for selected in route["selected"]:
                    selected["p"] = p
            p_record["inclusions"].append(
                {
                    "source_mask": source,
                    "target_mask": target,
                    "relative_sha256": sha256(path),
                    "primary": primary,
                    "audit": audit,
                }
            )
            result["status"] = "CHECKPOINT"
            result["elapsed_seconds"] = time.monotonic() - started
            write_json_atomic(args.output, result | {"rows": result["rows"] + [p_record]})
            if time.monotonic() - started > args.budget_seconds:
                result["status"] = "INCONCLUSIVE_RESOURCE_BUDGET"
                result["rows"].append(p_record)
                result["elapsed_seconds"] = time.monotonic() - started
                result["artifact_hash"] = digest(result)
                write_json_atomic(args.output, result)
                return 2
        result["rows"].append(p_record)

    result.update(classify(result["rows"]))
    result["status"] = "COMPLETE"
    result["elapsed_seconds"] = time.monotonic() - started
    result["artifact_hash"] = digest(result)
    write_json_atomic(args.output, result)
    selected = [
        item
        for row in result["rows"]
        for inclusion in row["inclusions"]
        for item in inclusion["primary"]["selected"]
    ]
    audit_selected = [
        item
        for row in result["rows"]
        for inclusion in row["inclusions"]
        for item in inclusion["audit"]["selected"]
    ]
    print(
        json.dumps(
            {
                "experiment": result["experiment"],
                "status": result["status"],
                "p1_status": result["p1_status"],
                "p2_status": result["p2_status"],
                "p3_status": result["p3_status"],
                "boundary_supports": [item["boundary_support_size"] for item in selected],
                "boundary_max_abs": [item["boundary_max_abs"] for item in selected],
                "cycle_supports": [item["cycle_support_size"] for item in selected],
                "audit_boundary_supports": [
                    item["boundary_support_size"] for item in audit_selected
                ],
                "audit_boundary_max_abs": [
                    item["boundary_max_abs"] for item in audit_selected
                ],
                "audit_cycle_supports": [
                    item["cycle_support_size"] for item in audit_selected
                ],
                "elapsed_seconds": result["elapsed_seconds"],
                "artifact_hash": result["artifact_hash"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
