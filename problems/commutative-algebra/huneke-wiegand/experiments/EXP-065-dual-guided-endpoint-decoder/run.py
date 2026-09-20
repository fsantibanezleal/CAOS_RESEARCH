"""Exact dual-guided decoding of the two mask-58 endpoint rows.

CPU only. Exact Fraction and integer HNF arithmetic. No global normal form.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
from fractions import Fraction
from pathlib import Path
from types import ModuleType

from flint import fmpz_mat


HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
EXP036 = EXPERIMENTS / "EXP-036-factor-two-torsion-anatomy"
EXP037 = EXPERIMENTS / "EXP-037-connecting-quasipolynomial"
EXP042 = EXPERIMENTS / "EXP-042-bockstein-normal-form"
EXP048 = EXPERIMENTS / "EXP-048-semantic-relative-bockstein"
EXP053 = EXPERIMENTS / "EXP-053-labelled-source-pullback"
EXP058 = EXPERIMENTS / "EXP-058-local-endpoint-source"
EXP063 = EXPERIMENTS / "EXP-063-triangle-isolated-comparison"
EXP064 = EXPERIMENTS / "EXP-064-exact-carrier-two-primary"
OUTPUT = HERE / "artifacts" / "results.json"
CHECKPOINT = HERE / "artifacts" / "checkpoint.json"
MASK = 58
MATRIX_SHA256 = {
    8: "7bffc81eeb39d637660a06a68fe314a573172e7249ab286f2e3fc7bb64e08cff",
    9: "00c20e30d81861a599448535c2ecc7625b56b1951fe863e64d40ce6f56ff218c",
    10: "c7d6bbf0ec655296a0dafe81ab41ce70300c0fa4a837e5c141f55811e29f6f4d",
}
PREMISES = {
    HERE / "hypothesis.md": "9497374dc88acfD4c4e7175cb45296b18bd51d7d0eca07840f1b339a1a1d8b73".lower(),
    EXP036 / "run.py": "1c6923c7c6456673402b5bdd3dada137970f6d01985690f29c960af65a981d03",
    EXP037 / "run.py": "1abebc24c99398dded97aa08216211db089889e154736ed9eb5a7202de0b5df0",
    EXP042 / "run.py": "3a57fc52a6a1e10ba42d97c6ebe27062324b8c90b76df7a288db41dffabd69bf",
    EXP048 / "run.py": "ec245859931cf1b3992630c8faab207a158ae5b72a3283783ec938cd3b76e70a",
    EXP053 / "extract_training.py": "cd1ff29b95944224a4d05265ce175926fcf60c08b34c4d4bff8b5884b729fc90",
    EXP058 / "proof.md": "5fdafaaf478626972e452949106dca708b3877b0939b7cf29273e8daddd4e7df",
    EXP063 / "artifacts" / "results.json": (
        "c219ce4c4549d970063a787227793bb5f7141e8f4d6e14c614f62085ecc8059a"
    ),
    EXP064 / "artifacts" / "results.json": (
        "9304c81487b29688c9fcf3524998db15f6faf7b50a9448cff197b6177bc4f5c4"
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


def verify_premises(parameters: tuple[int, ...]) -> dict[str, str]:
    actual = {str(path.relative_to(EXPERIMENTS)): sha256(path) for path in PREMISES}
    expected = {
        str(path.relative_to(EXPERIMENTS)): expected_hash
        for path, expected_hash in PREMISES.items()
    }
    if actual != expected:
        raise AssertionError({"premise_hash_mismatch": {"actual": actual, "expected": expected}})
    for p in parameters:
        path = EXP042 / "artifacts" / f"matrix-p{p}.json"
        if sha256(path) != MATRIX_SHA256[p]:
            raise AssertionError({"matrix_hash_mismatch": {"p": p, "actual": sha256(path)}})
    return actual


def axpy(
    destination: dict[int, Fraction], source: dict[int, Fraction], scale: Fraction
) -> None:
    for index, value in source.items():
        updated = destination.get(index, Fraction(0)) + scale * value
        if updated:
            destination[index] = updated
        else:
            destination.pop(index, None)


def integerize(vector: dict[int, Fraction]) -> dict[int, int]:
    denominator = math.lcm(*(value.denominator for value in vector.values()))
    result = {index: int(value * denominator) for index, value in vector.items()}
    common = math.gcd(*(abs(value) for value in result.values()))
    return {index: value // common for index, value in result.items()}


def solve_qq(
    columns: list[list[tuple[int, int]]], active: set[int], target_row: int,
    *, reverse: bool = False, budget: object | None = None,
) -> dict[str, object]:
    """Solve in the active rational column span and retain original-column provenance."""
    order = sorted(
        active,
        key=lambda index: (
            len(columns[index]) != 1,
            len(columns[index]),
            index,
        ),
        reverse=reverse,
    )
    basis: list[tuple[int, dict[int, Fraction], dict[int, Fraction]]] = []
    unit_pivots = 0
    for position, column_index in enumerate(order):
        if budget is not None and position % 64 == 0:
            budget.check(f"rational elimination column {position}/{len(order)}")
        vector = {row: Fraction(value) for row, value in columns[column_index]}
        provenance = {column_index: Fraction(1)}
        for pivot, reduced, source in basis:
            factor = vector.get(pivot)
            if factor:
                axpy(vector, reduced, -factor)
                axpy(provenance, source, -factor)
        if not vector:
            continue
        units = [row for row, value in vector.items() if abs(value) == 1]
        pivot = (max if reverse else min)(units if units else vector)
        divisor = vector[pivot]
        unit_pivots += abs(divisor) == 1
        normalized = {row: value / divisor for row, value in vector.items()}
        normalized_source = {
            index: value / divisor for index, value in provenance.items()
        }
        basis.append((pivot, normalized, normalized_source))

    residual = {target_row: Fraction(1)}
    particular: dict[int, Fraction] = {}
    for pivot, vector, source in basis:
        factor = residual.get(pivot)
        if factor:
            axpy(residual, vector, -factor)
            axpy(particular, source, factor)

    common = {
        "rank_qq": len(basis),
        "unit_pivots": unit_pivots,
        "nonunit_pivots": len(basis) - unit_pivots,
        "active_columns": len(active),
    }
    if not residual:
        return {
            **common,
            "classification": (
                "INTEGRAL_SECTION"
                if all(value.denominator == 1 for value in particular.values())
                else "RATIONAL_SECTION"
            ),
            "particular": particular,
            "denominator_lcm": math.lcm(
                *(value.denominator for value in particular.values()), 1
            ),
        }

    free_row = min(residual)
    dual: dict[int, Fraction] = {free_row: Fraction(1)}
    for pivot, vector, _ in reversed(basis):
        value = -sum(
            coefficient * dual.get(row, 0)
            for row, coefficient in vector.items()
            if row != pivot
        )
        if value:
            dual[pivot] = value
    dual_integer = integerize(dual)
    pairing = dual_integer.get(target_row, 0)
    if not pairing:
        raise AssertionError("constructed dual has zero target pairing")
    if pairing < 0:
        dual_integer = {row: -value for row, value in dual_integer.items()}
        pairing = -pairing
    for column_index in active:
        if sum(dual_integer.get(row, 0) * value for row, value in columns[column_index]):
            raise AssertionError("constructed dual does not annihilate the active columns")
    return {
        **common,
        "classification": "QQ_INCONSISTENT",
        "dual": dual_integer,
        "dual_target_pairing": pairing,
        "residual_support": len(residual),
    }


def hnf_integer_solution(
    columns: list[list[tuple[int, int]]], active: set[int], target_row: int,
    row_count: int,
) -> dict[int, int] | None:
    ordered = sorted(active)
    transposed = fmpz_mat(len(ordered), row_count)
    for local, column_index in enumerate(ordered):
        for row, value in columns[column_index]:
            transposed[local, row] = value
    hnf, transform = transposed.hnf(transform=True)
    pivots: list[int] = []
    for row in range(hnf.nrows()):
        pivot = next((column for column in range(hnf.ncols()) if hnf[row, column]), None)
        if pivot is None:
            break
        pivots.append(pivot)
    residual = [0] * row_count
    residual[target_row] = 1
    coordinates = [0] * hnf.nrows()
    for row, pivot in enumerate(pivots):
        quotient, remainder = divmod(residual[pivot], int(hnf[row, pivot]))
        if remainder:
            return None
        coordinates[row] = quotient
        if quotient:
            for column in range(row_count):
                residual[column] -= quotient * int(hnf[row, column])
    if any(residual):
        return None
    local_solution = [
        sum(coordinates[row] * int(transform[row, column]) for row in range(len(pivots)))
        for column in range(transform.ncols())
    ]
    return {
        ordered[local]: value
        for local, value in enumerate(local_solution)
        if value
    }


def multiply(
    columns: list[list[tuple[int, int]]], witness: dict[int, int], row_count: int
) -> list[int]:
    result = [0] * row_count
    for column, coefficient in witness.items():
        for row, value in columns[column]:
            result[row] += coefficient * value
    return result


def escaping_columns(
    columns: list[list[tuple[int, int]]], active: set[int], dual: dict[int, int]
) -> list[tuple[int, int]]:
    result = []
    for column, entries in enumerate(columns):
        if column in active:
            continue
        pairing = sum(dual.get(row, 0) * value for row, value in entries)
        if pairing:
            result.append((column, pairing))
    return sorted(result, key=lambda item: (-abs(item[1]), item[0]))


def target_triangles(p: int) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    return (0, 1, p - 3), (0, 2, p - 4)


def parameter_model(
    p: int, modules: dict[str, ModuleType], budget: object
) -> dict[str, object]:
    model = modules["exp053"].make_component_model(
        exp036=modules["exp036"],
        exp037=modules["exp037"],
        exp042=modules["exp042"],
        exp048=modules["exp048"],
        p=p,
        budget=budget,
    )
    if not model["unique_mapping"]:
        raise AssertionError({"p": p, "semantic_column_map": model["ambiguous"]})
    labelled = model["labelled"]
    selected = modules["exp048"].rows_for_mask(labelled["row_atoms"], MASK)
    row_position = {row: position for position, row in enumerate(selected)}
    projected = [
        [
            (row_position[int(row)], int(value))
            for row, value in entries
            if int(row) in row_position
        ]
        for entries in model["frozen"]["signed_columns"]
    ]
    label_index = {
        json.dumps(label, separators=(",", ":")): index
        for index, label in enumerate(labelled["row_labels"])
    }
    targets = []
    for triangle in target_triangles(p):
        label = modules["exp063"].triangle_label(p, triangle)
        component_row = label_index[json.dumps(label, separators=(",", ":"))]
        targets.append({
            "p": p,
            "triangle": list(triangle),
            "label": label,
            "component_row": component_row,
            "projected_row": row_position[component_row],
        })
    return {
        "model": model,
        "selected_rows": selected,
        "projected_columns": projected,
        "targets": targets,
    }


def witness_record(
    witness: dict[int, int], labels: list[list[object]], p: int,
    exp053: ModuleType,
) -> dict[str, object]:
    support = [
        {
            "column": column,
            "coefficient": coefficient,
            "exact_label": labels[column],
            "normalized_label": exp053.normalize_column(labels[column], p),
        }
        for column, coefficient in sorted(witness.items())
    ]
    skeletons = sorted({
        json.dumps(exp053.numeric_skeleton(item["normalized_label"]), sort_keys=True)
        for item in support
    })
    return {
        "support_size": len(support),
        "max_abs_coefficient": max((abs(value) for value in witness.values()), default=0),
        "skeleton_count": len(skeletons),
        "skeletons": [json.loads(value) for value in skeletons],
        "support": support,
        "witness_hash": digest(support),
    }


def solve_target(
    *, p: int, target: dict[str, object], projected: list[list[tuple[int, int]]],
    labels: list[list[object]], exp053: ModuleType, budget: object,
    row_count: int, max_rounds: int, max_columns: int, checkpoint,
) -> dict[str, object]:
    target_row = int(target["projected_row"])
    active = {
        column for column, entries in enumerate(projected)
        if any(row == target_row for row, _ in entries)
    }
    if not active:
        raise AssertionError({"p": p, "target": target["triangle"], "no_incident_columns": True})
    record: dict[str, object] = {**target, "rounds": [], "status": "RUNNING"}
    for round_index in range(1, max_rounds + 1):
        budget.check(f"p={p} target={target['triangle']} round={round_index}")
        if len(active) > max_columns:
            record.update({"status": "INCONCLUSIVE_COLUMN_CAP", "active_columns": len(active)})
            checkpoint()
            return record
        solved = solve_qq(projected, active, target_row, budget=budget)
        reverse = solve_qq(projected, active, target_row, reverse=True, budget=budget)
        if (
            solved["classification"] == "QQ_INCONSISTENT"
        ) != (
            reverse["classification"] == "QQ_INCONSISTENT"
        ):
            raise AssertionError("forward/reverse rational classification disagreement")
        round_record = {
            key: value for key, value in solved.items()
            if key not in {"particular", "dual"}
        }
        round_record["round"] = round_index
        if solved["classification"] == "QQ_INCONSISTENT":
            dual = solved["dual"]
            escaping = escaping_columns(projected, active, dual)
            round_record.update({
                "dual_support": len(dual),
                "dual_hash": digest(sorted(dual.items())),
                "escaping_columns": len(escaping),
                "escaping_pairing_abs_max": max((abs(value) for _, value in escaping), default=0),
            })
            record["rounds"].append(round_record)
            if not escaping:
                raise AssertionError("full matrix has no escaping column despite known membership")
            active.update(column for column, _ in escaping)
            checkpoint()
            print(
                f"p={p} target={target['triangle']} round={round_index} "
                f"QQ obstruction, add={len(escaping)}, active={len(active)}",
                flush=True,
            )
            continue

        particular = solved["particular"]
        if solved["classification"] == "INTEGRAL_SECTION":
            witness = {index: int(value) for index, value in particular.items() if value}
            route = "unit-first-rational-section"
        else:
            budget.check(f"p={p} local HNF start")
            witness = hnf_integer_solution(
                projected, active, target_row, row_count
            )
            if witness is None:
                record["rounds"].append(round_record)
                record.update({
                    "status": "INCONCLUSIVE_LOCAL_LATTICE_OBSTRUCTION",
                    "active_columns": len(active),
                    "rational_denominator_lcm": solved["denominator_lcm"],
                })
                checkpoint()
                return record
            route = "local-transformed-hnf"
        actual = multiply(projected, witness, row_count)
        expected = [0] * len(actual)
        expected[target_row] = 1
        if actual != expected:
            raise AssertionError("witness does not reproduce the exact projected target")
        mutated = dict(witness)
        first = min(mutated)
        mutated[first] += 1
        if multiply(projected, mutated, len(actual)) == expected:
            raise AssertionError("witness coefficient mutation was not rejected")
        mutated_target = [0] * len(actual)
        mutated_target[(target_row + 1) % len(actual)] = 1
        if actual == mutated_target:
            raise AssertionError("target-row mutation was not rejected")
        round_record["solution_route"] = route
        record["rounds"].append(round_record)
        record.update({
            "status": "INTEGRAL_WITNESS",
            "active_columns": len(active),
            "reverse_order_membership_agrees": True,
            "target_mutation_rejected": True,
            "witness_mutation_rejected": True,
            "witness": witness_record(witness, labels, p, exp053),
        })
        checkpoint()
        print(
            f"p={p} target={target['triangle']} round={round_index} "
            f"witness={record['witness']['support_size']} route={route}",
            flush=True,
        )
        return record
    record.update({"status": "INCONCLUSIVE_ROUND_CAP", "active_columns": len(active)})
    checkpoint()
    return record


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p-min", type=int, default=8)
    parser.add_argument("--p-max", type=int, default=10)
    parser.add_argument("--budget-seconds", type=float, default=900.0)
    parser.add_argument("--memory-gib", type=float, default=8.0)
    parser.add_argument("--max-rounds", type=int, default=6)
    parser.add_argument("--max-columns", type=int, default=900)
    parser.add_argument("--target-limit", type=int, choices=(1, 2), default=2)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--checkpoint", type=Path, default=CHECKPOINT)
    args = parser.parse_args()
    parameters = tuple(range(args.p_min, args.p_max + 1))
    if not parameters or any(p not in (8, 9, 10) for p in parameters):
        raise ValueError("EXP-065 training parameters are exactly a subset of 8,9,10")
    if args.max_rounds > 6 or args.max_columns > 900:
        raise ValueError("requested caps exceed the frozen hypothesis")

    premises = verify_premises(parameters)
    modules = {
        "exp036": load_module("exp036_for_exp065", EXP036 / "run.py"),
        "exp037": load_module("exp037_for_exp065", EXP037 / "run.py"),
        "exp042": load_module("exp042_for_exp065", EXP042 / "run.py"),
        "exp048": load_module("exp048_for_exp065", EXP048 / "run.py"),
        "exp053": load_module("exp053_for_exp065", EXP053 / "extract_training.py"),
        "exp063": load_module("exp063_for_exp065", EXP063 / "run.py"),
    }
    result: dict[str, object] = {
        "experiment": "EXP-065",
        "route": "dual-guided exact column generation",
        "parameters": list(parameters),
        "mask": MASK,
        "premises": premises,
        "rows": [],
        "status": "RUNNING",
    }

    def checkpoint() -> None:
        payload = dict(result)
        payload["artifact_hash"] = digest(payload)
        write_json_atomic(args.checkpoint, payload)

    try:
        for p in parameters:
            budget = modules["exp048"].Budget(args.budget_seconds, args.memory_gib)
            print(f"p={p} reconstruct semantic component", flush=True)
            model = parameter_model(p, modules, budget)
            row = {
                "p": p,
                "selected_rows": len(model["selected_rows"]),
                "component_columns": len(model["projected_columns"]),
                "semantic_column_map_unique": model["model"]["unique_mapping"],
                "targets": [],
            }
            result["rows"].append(row)
            checkpoint()
            for target in model["targets"][: args.target_limit]:
                target_record = solve_target(
                    p=p,
                    target=target,
                    projected=model["projected_columns"],
                    labels=model["model"]["column_labels"],
                    exp053=modules["exp053"],
                    budget=budget,
                    row_count=len(model["selected_rows"]),
                    max_rounds=args.max_rounds,
                    max_columns=args.max_columns,
                    checkpoint=checkpoint,
                )
                row["targets"].append(target_record)
                checkpoint()
    except modules["exp048"].BudgetStop as stop:
        result.update({"status": "INCONCLUSIVE_RESOURCE", "resource_stop": str(stop)})
        checkpoint()
        print(str(stop), flush=True)
        return 2

    targets = [target for row in result["rows"] for target in row["targets"]]
    p1 = len(targets) == 2 * len(parameters) and all(
        target["status"] == "INTEGRAL_WITNESS" for target in targets
    )
    witnesses = [target["witness"] for target in targets if "witness" in target]
    skeleton_union = {
        json.dumps(skeleton, sort_keys=True)
        for witness in witnesses for skeleton in witness["skeletons"]
    }
    p2 = p1 and all(
        witness["max_abs_coefficient"] <= 4
        and witness["support_size"] <= 40 * target["p"]
        for target, witness in zip(targets, witnesses, strict=True)
    ) and len(skeleton_union) <= 80
    p3 = p1 and all(
        target["reverse_order_membership_agrees"]
        and target["target_mutation_rejected"]
        and target["witness_mutation_rejected"]
        for target in targets
    )
    result.update({
        "p1_status": "PASS_FINITE" if p1 else "REFUTED_OR_INCONCLUSIVE",
        "p2_status": "PASS_FINITE" if p2 else "REFUTED_OR_INCONCLUSIVE",
        "p3_status": "PASS" if p3 else "FAIL_OR_INCONCLUSIVE",
        "semantic_skeleton_union": len(skeleton_union),
        "status": "COMPLETE" if p1 and p3 else "INCONCLUSIVE_OR_REFUTED",
    })
    result["artifact_hash"] = digest(result)
    write_json_atomic(args.output, result)
    checkpoint()
    print(json.dumps({
        "status": result["status"],
        "p1": result["p1_status"],
        "p2": result["p2_status"],
        "p3": result["p3_status"],
        "targets": len(targets),
        "skeletons": result["semantic_skeleton_union"],
        "artifact_hash": result["artifact_hash"],
    }, indent=2), flush=True)
    return 0 if p1 and p3 else 1


if __name__ == "__main__":
    raise SystemExit(main())
