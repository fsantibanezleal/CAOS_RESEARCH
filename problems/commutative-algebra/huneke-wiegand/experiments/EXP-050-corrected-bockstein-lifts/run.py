"""EXP-050 provenance-preserving corrected Bockstein representatives.

CPU only. Exact integer and bit-packed GF(2) arithmetic.
"""

from __future__ import annotations

import argparse
import gc
import hashlib
import importlib.util
import json
from pathlib import Path
from types import ModuleType
from typing import Iterable


HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
EXP036 = EXPERIMENTS / "EXP-036-factor-two-torsion-anatomy"
EXP037 = EXPERIMENTS / "EXP-037-connecting-quasipolynomial"
EXP042 = EXPERIMENTS / "EXP-042-bockstein-normal-form"
EXP047 = EXPERIMENTS / "EXP-047-relative-kernel-smith"
EXP048 = EXPERIMENTS / "EXP-048-semantic-relative-bockstein"
EXP049 = EXPERIMENTS / "EXP-049-exact-chain-lifts"
DEFAULT_OUTPUT = HERE / "artifacts" / "results.json"
INCLUSIONS = ((58, 59), (58, 62))
PREMISES = {
    EXP047 / "artifacts" / "results.json": (
        "f78d251ae1746a88d1190756572aa251b9daf70ceb103cef9765c6d73b26f46c"
    ),
    EXP048 / "run.py": "ec245859931cf1b3992630c8faab207a158ae5b72a3283783ec938cd3b76e70a",
    EXP048 / "artifacts" / "results.json": (
        "ba44eae4c9193bc941411b059dc7a7d7a4c69dff3d818e05d3395338e125a400"
    ),
    EXP049 / "run.py": "83a6f0b248516aea77bd0af15c716eccb01ec1ad84260a75e21bb632986dc130",
    EXP049 / "artifacts" / "results.json": (
        "567f554abaa1456133a4c0cd475d1848dad92a36dd8b9412381fe2fab9fc39b7"
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


def bit_indices(value: int) -> Iterable[int]:
    while value:
        least = value & -value
        yield least.bit_length() - 1
        value ^= least


def sparse(values: list[int]) -> list[list[int]]:
    return [[index, value] for index, value in enumerate(values) if value]


def column_bits(columns: list[list[list[int]]]) -> list[int]:
    return [
        sum(1 << int(row) for row, value in entries if int(value) & 1)
        for entries in columns
    ]


def column_sum(
    columns: list[list[list[int]]], combination: int, row_count: int
) -> list[int]:
    result = [0] * row_count
    for column in bit_indices(combination):
        for row, value in columns[column]:
            result[int(row)] += int(value)
    return result


def multiply(columns: list[list[list[int]]], vector: list[int], row_count: int) -> list[int]:
    result = [0] * row_count
    for column, coefficient in enumerate(vector):
        if coefficient:
            for row, value in columns[column]:
                result[int(row)] += coefficient * int(value)
    return result


def rref_with_combinations(
    vectors: list[int], *, high: bool, reverse: bool
) -> list[tuple[int, int]]:
    basis: dict[int, tuple[int, int]] = {}
    order = list(range(len(vectors)))
    if reverse:
        order.reverse()
    for column in order:
        vector = vectors[column]
        combination = 1 << column
        while vector:
            pivot = vector.bit_length() - 1 if high else (vector & -vector).bit_length() - 1
            existing = basis.get(pivot)
            if existing is None:
                for other, (other_vector, other_combination) in list(basis.items()):
                    if (other_vector >> pivot) & 1:
                        basis[other] = (
                            other_vector ^ vector,
                            other_combination ^ combination,
                        )
                basis[pivot] = (vector, combination)
                break
            vector ^= existing[0]
            combination ^= existing[1]
    return [basis[pivot] for pivot in sorted(basis, reverse=high)]


def kernel_combinations(vectors: list[int], *, high: bool, reverse: bool) -> list[int]:
    pivots: dict[int, tuple[int, int]] = {}
    kernel: list[int] = []
    order = list(range(len(vectors)))
    if reverse:
        order.reverse()
    for column in order:
        vector = vectors[column]
        combination = 1 << column
        while vector:
            pivot = vector.bit_length() - 1 if high else (vector & -vector).bit_length() - 1
            existing = pivots.get(pivot)
            if existing is None:
                pivots[pivot] = (vector, combination)
                break
            vector ^= existing[0]
            combination ^= existing[1]
        if not vector:
            kernel.append(combination)
    return kernel


def exact_bockstein_basis(
    columns: list[list[list[int]]], row_count: int, *, high: bool, reverse: bool
) -> list[dict[str, object]]:
    bits = column_bits(columns)
    image = rref_with_combinations(bits, high=high, reverse=reverse)
    image_records = [
        (vector, combination, column_sum(columns, combination, row_count))
        for vector, combination in image
    ]
    candidates: list[dict[str, object]] = []
    for cycle in kernel_combinations(bits, high=high, reverse=reverse):
        boundary = column_sum(columns, cycle, row_count)
        if any(value & 1 for value in boundary):
            raise AssertionError("binary cycle has odd integral boundary")
        exact = [value // 2 for value in boundary]
        witness = [int((cycle >> column) & 1) for column in range(len(columns))]
        quotient = sum(1 << row for row, value in enumerate(exact) if value & 1)
        for image_vector, image_combination, image_boundary in image_records:
            pivot = (
                image_vector.bit_length() - 1
                if high
                else (image_vector & -image_vector).bit_length() - 1
            )
            if (quotient >> pivot) & 1:
                quotient ^= image_vector
                exact = [value - delta for value, delta in zip(exact, image_boundary, strict=True)]
                for column in bit_indices(image_combination):
                    witness[column] -= 2
        if quotient:
            if any((value & 1) != ((quotient >> row) & 1) for row, value in enumerate(exact)):
                raise AssertionError("exact quotient parity mismatch")
            if multiply(columns, witness, row_count) != [2 * value for value in exact]:
                raise AssertionError("candidate exact witness mismatch")
            candidates.append({"parity": quotient, "exact": exact, "witness": witness})

    basis: dict[int, dict[str, object]] = {}
    for candidate in candidates:
        parity = int(candidate["parity"])
        exact = list(candidate["exact"])
        witness = list(candidate["witness"])
        while parity:
            pivot = parity.bit_length() - 1 if high else (parity & -parity).bit_length() - 1
            existing = basis.get(pivot)
            if existing is None:
                for other, record in list(basis.items()):
                    if (int(record["parity"]) >> pivot) & 1:
                        record["parity"] = int(record["parity"]) ^ parity
                        record["exact"] = [
                            left + right
                            for left, right in zip(record["exact"], exact, strict=True)
                        ]
                        record["witness"] = [
                            left + right
                            for left, right in zip(record["witness"], witness, strict=True)
                        ]
                basis[pivot] = {"parity": parity, "exact": exact, "witness": witness}
                break
            parity ^= int(existing["parity"])
            exact = [left + right for left, right in zip(exact, existing["exact"], strict=True)]
            witness = [
                left + right for left, right in zip(witness, existing["witness"], strict=True)
            ]
    records = [basis[pivot] for pivot in sorted(basis, reverse=high)]
    for record in records:
        if multiply(columns, record["witness"], row_count) != [
            2 * value for value in record["exact"]
        ]:
            raise AssertionError("basis exact witness mismatch")
    return records


def canonical_rref(vectors: Iterable[int]) -> list[int]:
    basis: dict[int, int] = {}
    for raw in vectors:
        vector = raw
        for pivot in sorted(basis):
            if (vector >> pivot) & 1:
                vector ^= basis[pivot]
        if not vector:
            continue
        pivot = (vector & -vector).bit_length() - 1
        for other in list(basis):
            if (basis[other] >> pivot) & 1:
                basis[other] ^= vector
        basis[pivot] = vector
    return [basis[pivot] for pivot in sorted(basis)]


def fit_affine(values: list[int], parameters: list[int]) -> list[int] | None:
    for slope in range(-100, 101):
        intercept = values[0] - slope * parameters[0]
        if all(value == slope * p + intercept for p, value in zip(parameters, values, strict=True)):
            return [slope, intercept]
    return None


def classify(rows: list[dict[str, object]]) -> dict[str, object]:
    full = [int(row["p"]) for row in rows] == [8, 9, 10, 11]
    primary = [
        record
        for row in rows
        for inclusion in row["inclusions"]
        for record in inclusion["primary_records"]
    ]
    p1 = full and len(primary) == 16 and all(
        record["exact_identity"] and record["nonzero_correction"] for record in primary
    )
    p2 = p1 and all(
        int(record["correction_max_abs"]) <= 1
        and int(record["correction_support_size"]) <= 4 * int(record["p"])
        for record in primary
    )
    p3_details: dict[str, object] = {}
    p3 = full
    for source, target in INCLUSIONS:
        groups = [
            sorted(
                (
                    record
                    for record in next(
                        inclusion
                        for inclusion in row["inclusions"]
                        if (int(inclusion["source_mask"]), int(inclusion["target_mask"]))
                        == (source, target)
                    )["primary_records"]
                ),
                key=lambda record: int(record["correction_support_size"]),
            )
            for row in rows
        ]
        support_series = [
            [int(group[index]["correction_support_size"]) for group in groups]
            for index in range(2)
        ]
        affine = [fit_affine(series, [8, 9, 10, 11]) for series in support_series]
        histograms = [
            [group[index]["correction_atom_histogram"] for group in groups]
            for index in range(2)
        ]
        hist_stable = all(len({json.dumps(value, sort_keys=True) for value in series}) == 1 for series in histograms)
        passes = all(value is not None for value in affine) and hist_stable
        p3 &= passes
        p3_details[f"{source}->{target}"] = {
            "support_series": support_series,
            "affine_slope_intercept": affine,
            "histograms_stable": hist_stable,
            "passes": passes,
        }
    return {
        "p1_status": "PASS_FINITE" if p1 else "REFUTED" if full else "NOT_EVALUATED",
        "p2_status": "PASS_FINITE" if p2 else "REFUTED" if full else "NOT_EVALUATED",
        "p3_status": "PASS_FINITE" if p3 else "REFUTED" if full else "NOT_EVALUATED",
        "p3_details": p3_details,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p-min", type=int, default=8)
    parser.add_argument("--p-max", type=int, default=11)
    parser.add_argument("--budget-seconds", type=float, default=900.0)
    parser.add_argument("--memory-gib", type=float, default=12.0)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if args.p_min < 8 or args.p_max > 11 or args.p_min > args.p_max:
        raise ValueError("declared range is 8<=p_min<=p_max<=11")

    premises = verify_premises()
    exp036 = load_module("exp036_for_exp050", EXP036 / "run.py")
    exp037 = load_module("exp037_for_exp050", EXP037 / "run.py")
    exp042 = load_module("exp042_for_exp050", EXP042 / "run.py")
    exp047 = load_module("exp047_for_exp050", EXP047 / "run.py")
    exp048 = load_module("exp048_for_exp050", EXP048 / "run.py")
    exp049 = load_module("exp049_for_exp050", EXP049 / "run.py")
    stored048 = json.loads((EXP048 / "artifacts" / "results.json").read_text(encoding="utf-8"))
    stored048_records = {
        (int(row["p"]), int(record["source_mask"]), int(record["target_mask"])): record
        for row in stored048["rows"]
        for record in row["inclusions"]
    }
    budget = exp048.Budget(args.budget_seconds, args.memory_gib)
    result: dict[str, object] = {
        "experiment": "EXP-050",
        "route": "provenance-preserving exact Bockstein quotient reduction",
        "status": "RUNNING",
        "parameters": {
            "p_min": args.p_min,
            "p_max": args.p_max,
            "budget_seconds": args.budget_seconds,
            "memory_gib": args.memory_gib,
        },
        "premise_hashes": premises,
        "rows": [],
    }
    write_json_atomic(args.output, result)
    try:
        for p in range(args.p_min, args.p_max + 1):
            print(f"p={p} reconstruct semantic component", flush=True)
            component = exp048.reconstruct_labelled_component(
                exp036=exp036, exp037=exp037, exp042=exp042, p=p, budget=budget
            )
            p_record: dict[str, object] = {"p": p, "inclusions": []}
            for source, target in INCLUSIONS:
                print(f"p={p} {source}->{target} retain exact Bockstein provenance", flush=True)
                relative_path = EXP047 / "artifacts" / f"relative-p{p}-m{source}-m{target}.json"
                relative = json.loads(relative_path.read_text(encoding="utf-8"))
                added_rows, tokens, semantic_order = exp049.semantic_rows(
                    exp047=exp047,
                    exp048=exp048,
                    component=component,
                    p=p,
                    source=source,
                    target=target,
                )
                semantic_position = {old: new for new, old in enumerate(semantic_order)}
                ordered_tokens = [tokens[old] for old in semantic_order]
                columns = [
                    sorted(
                        [semantic_position[int(row)], int(value)] for row, value in entries
                    )
                    for entries in relative["matrix_columns"]
                ]
                added_labels = [component["row_labels"][row] for row in added_rows]
                formula_raw = exp049.formula_chains(
                    p=p, source=source, target=target, added_labels=added_labels
                )
                formula_semantic = [
                    sorted(semantic_position[row] for row in chain) for chain in formula_raw
                ]
                formula_bits = [sum(1 << row for row in chain) for chain in formula_semantic]
                primary_basis = exact_bockstein_basis(
                    columns, len(added_rows), high=False, reverse=False
                )
                primary_by_parity = {int(record["parity"]): record for record in primary_basis}
                if set(primary_by_parity) != set(formula_bits):
                    raise AssertionError({"p": p, "inclusion": [source, target], "formula_basis": False})
                if digest(canonical_rref(primary_by_parity)) != stored048_records[
                    p, source, target
                ]["bockstein_subspace_hash"]:
                    raise AssertionError({"p": p, "inclusion": [source, target], "frozen_subspace": False})
                records = []
                for index, (parity, chain) in enumerate(zip(formula_bits, formula_semantic, strict=True), start=1):
                    record = primary_by_parity[parity]
                    exact = list(record["exact"])
                    witness = list(record["witness"])
                    chain_set = set(chain)
                    correction = []
                    for row, value in enumerate(exact):
                        difference = value - int(row in chain_set)
                        if difference & 1:
                            raise AssertionError("correction is not integral")
                        correction.append(difference // 2)
                    if multiply(columns, witness, len(added_rows)) != [2 * value for value in exact]:
                        raise AssertionError("stored exact identity fails")
                    correction_rows = [row for row, value in enumerate(correction) if value]
                    atom_histogram: dict[str, int] = {}
                    for row in correction_rows:
                        atom = str(ordered_tokens[row]["kind"])
                        atom_histogram[atom] = atom_histogram.get(atom, 0) + 1
                    records.append(
                        {
                            "p": p,
                            "chain_index": index,
                            "parity_rows": chain,
                            "parity_hash": digest(chain),
                            "exact_representative": sparse(exact),
                            "exact_representative_hash": digest(exact),
                            "relative_witness": sparse(witness),
                            "relative_witness_hash": digest(witness),
                            "exact_identity": True,
                            "correction": sparse(correction),
                            "correction_hash": digest(correction),
                            "correction_support_size": len(correction_rows),
                            "correction_max_abs": max(map(abs, correction), default=0),
                            "correction_atom_histogram": atom_histogram,
                            "correction_semantic_support": [ordered_tokens[row] for row in correction_rows],
                            "nonzero_correction": any(correction),
                        }
                    )
                audit_basis = exact_bockstein_basis(
                    columns, len(added_rows), high=True, reverse=True
                )
                audit_canonical = canonical_rref(int(record["parity"]) for record in audit_basis)
                if audit_canonical != canonical_rref(formula_bits):
                    raise AssertionError({"p": p, "inclusion": [source, target], "audit_subspace": False})
                p_record["inclusions"].append(
                    {
                        "source_mask": source,
                        "target_mask": target,
                        "relative_sha256": sha256(relative_path),
                        "added_rows": len(added_rows),
                        "semantic_row_hash": digest(ordered_tokens),
                        "primary_records": records,
                        "primary_rank": len(primary_basis),
                        "audit_rank": len(audit_basis),
                        "audit_exact_identities": all(
                            multiply(columns, record["witness"], len(added_rows))
                            == [2 * value for value in record["exact"]]
                            for record in audit_basis
                        ),
                        "audit_subspace_hash": digest(audit_canonical),
                    }
                )
                result["status"] = "CHECKPOINT"
                result["elapsed_seconds"] = budget.elapsed
                write_json_atomic(args.output, result | {"rows": result["rows"] + [p_record]})
                budget.check(f"p={p} {source}->{target}")
            result["rows"].append(p_record)
            result["elapsed_seconds"] = budget.elapsed
            write_json_atomic(args.output, result)
            del component
            gc.collect()
    except exp048.BudgetStop as error:
        result["status"] = "INCONCLUSIVE_RESOURCE_BUDGET"
        result["resource_stop"] = str(error)
        result["elapsed_seconds"] = budget.elapsed
        result["artifact_hash"] = digest(result)
        write_json_atomic(args.output, result)
        return 2

    result.update(classify(result["rows"]))
    result["status"] = "COMPLETE"
    result["elapsed_seconds"] = budget.elapsed
    result["artifact_hash"] = digest(result)
    write_json_atomic(args.output, result)
    records = [
        record
        for row in result["rows"]
        for inclusion in row["inclusions"]
        for record in inclusion["primary_records"]
    ]
    print(
        json.dumps(
            {
                "experiment": result["experiment"],
                "status": result["status"],
                "p1_status": result["p1_status"],
                "p2_status": result["p2_status"],
                "p3_status": result["p3_status"],
                "correction_supports": [record["correction_support_size"] for record in records],
                "correction_max_abs": [record["correction_max_abs"] for record in records],
                "elapsed_seconds": result["elapsed_seconds"],
                "artifact_hash": result["artifact_hash"],
            },
            indent=2,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
