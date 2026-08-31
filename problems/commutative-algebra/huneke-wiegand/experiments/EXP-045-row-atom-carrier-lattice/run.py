"""EXP-045 complete subset lattice of the six isolated row atoms."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from collections import Counter
from pathlib import Path
from types import ModuleType


HERE = Path(__file__).resolve().parent
EXP042 = HERE.parent / "EXP-042-bockstein-normal-form"
EXP044 = HERE.parent / "EXP-044-row-projection-bridge"
DEFAULT_OUTPUT = HERE / "artifacts" / "results.json"
ATOM_ALIASES = {
    "R0": '["row","D","A",[-2,-3,1,0,1,0,0,0,0,0]]',
    "R1": '["row","D","A",[-3,-2,2,0,0,0,0,0,0,0]]',
    "R2": '["row","D","B",[-1,-4,1,0,1,0,0,0,0,0]]',
    "R3": '["row","D","B",[-2,-3,2,0,0,0,0,0,0,0]]',
    "R4": '["row","K","C0",[-2,-2,1,0,0,0,0,0,0,0]]',
    "R5": '["row","K","C2",[-1,-3,1,0,0,0,0,0,0,0]]',
}
ALIASES = tuple(ATOM_ALIASES)
FULL_MASK = (1 << len(ALIASES)) - 1
EXPECTED_BETA = {8: 3, 9: 4, 10: 5, 11: 7}
PREMISES = {
    EXP042 / "artifacts" / "matrix-p8.json": (
        "7bffc81eeb39d637660a06a68fe314a573172e7249ab286f2e3fc7bb64e08cff"
    ),
    EXP042 / "artifacts" / "matrix-p9.json": (
        "00c20e30d81861a599448535c2ecc7625b56b1951fe863e64d40ce6f56ff218c"
    ),
    EXP042 / "artifacts" / "matrix-p10.json": (
        "c7d6bbf0ec655296a0dafe81ab41ce70300c0fa4a837e5c141f55811e29f6f4d"
    ),
    EXP042 / "artifacts" / "matrix-p11.json": (
        "69e8519a3b239ec90c3b5af526f806a9a0aabf003517ea28233167d7e2b68dd9"
    ),
    EXP044 / "artifacts" / "results.json": (
        "6766b6ca249f1b02ba9a83a6fb8434eea4e511172c982840fc3c6db6a192e886"
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
    actual = {str(path.relative_to(HERE.parent)): sha256(path) for path in PREMISES}
    expected = {
        str(path.relative_to(HERE.parent)): expected_hash
        for path, expected_hash in PREMISES.items()
    }
    if actual != expected:
        raise AssertionError({"premise_hash_mismatch": {"actual": actual, "expected": expected}})
    return actual


def bit_indices(value: int):
    while value:
        least = value & -value
        yield least.bit_length() - 1
        value ^= least


def pivot_of(vector: int, high: bool) -> int:
    if high:
        return vector.bit_length() - 1
    return (vector & -vector).bit_length() - 1


def bockstein_rank(
    signed_columns: list[list[list[int]]],
    row_count: int,
    *,
    reverse_columns: bool,
    high_pivot: bool,
) -> dict[str, int]:
    column_count = len(signed_columns)
    column_bits = [sum(1 << int(row) for row, _ in entries) for entries in signed_columns]
    order = range(column_count - 1, -1, -1) if reverse_columns else range(column_count)
    pivots: dict[int, int] = {}
    combinations: dict[int, int] = {}
    kernel: list[int] = []
    for column in order:
        vector = column_bits[column]
        combination = 1 << column
        while vector:
            pivot = pivot_of(vector, high_pivot)
            if pivot not in pivots:
                pivots[pivot] = vector
                combinations[pivot] = combination
                break
            vector ^= pivots[pivot]
            combination ^= combinations[pivot]
        if not vector:
            kernel.append(combination)

    quotient_order = sorted(pivots, reverse=high_pivot)
    beta_pivots: dict[int, int] = {}
    for combination in kernel:
        boundary = [0] * row_count
        for column in bit_indices(combination):
            for row, sign in signed_columns[column]:
                boundary[int(row)] += int(sign)
        if any(value & 1 for value in boundary):
            raise AssertionError("projected kernel lift is not even")
        vector = sum(1 << row for row, value in enumerate(boundary) if (value // 2) & 1)
        for pivot in quotient_order:
            if (vector >> pivot) & 1:
                vector ^= pivots[pivot]
        while vector:
            pivot = pivot_of(vector, high_pivot)
            if pivot not in beta_pivots:
                beta_pivots[pivot] = vector
                break
            vector ^= beta_pivots[pivot]
    return {
        "rank_mod_two": len(pivots),
        "kernel_dimension": len(kernel),
        "bockstein_rank": len(beta_pivots),
    }


def atom_values(matrix: dict[str, object]) -> list[str]:
    table = matrix["row_atom_table"]
    return [table[int(index)] for index in matrix["row_atom_ids"]]


def subset_aliases(mask: int) -> list[str]:
    return [alias for index, alias in enumerate(ALIASES) if mask & (1 << index)]


def project_matrix(
    matrix: dict[str, object], mask: int
) -> tuple[list[int], list[str], list[list[list[int]]]]:
    selected = {ATOM_ALIASES[alias] for alias in subset_aliases(mask)}
    atoms = atom_values(matrix)
    kept_rows = [row for row, atom in enumerate(atoms) if atom in selected]
    row_map = {original: projected for projected, original in enumerate(kept_rows)}
    signed_columns = [
        [[row_map[int(row)], int(sign)] for row, sign in entries if int(row) in row_map]
        for entries in matrix["signed_columns"]
    ]
    return kept_rows, [atoms[row] for row in kept_rows], signed_columns


def minimal_masks(carriers: set[int]) -> list[int]:
    return sorted(mask for mask in carriers if not any(other & mask == other for other in carriers if other != mask))


def evaluate_subset(
    *, matrix: dict[str, object], mask: int, exp042: ModuleType, exp037: ModuleType
) -> dict[str, object]:
    kept_rows, atoms, signed_columns = project_matrix(matrix, mask)
    ranks = exp042.rank_fields(exp037, signed_columns)
    high = bockstein_rank(
        signed_columns, len(kept_rows), reverse_columns=False, high_pivot=True
    )
    low = bockstein_rank(
        signed_columns, len(kept_rows), reverse_columns=True, high_pivot=False
    )
    gap = int(ranks["3"]) - int(ranks["2"])
    return {
        "mask": mask,
        "aliases": subset_aliases(mask),
        "atom_count": mask.bit_count(),
        "rows": len(kept_rows),
        "columns": len(signed_columns),
        "nonzero_columns": sum(bool(entries) for entries in signed_columns),
        "nonzeros": sum(map(len, signed_columns)),
        "row_atom_counts": dict(sorted(Counter(atoms).items())),
        "ranks": ranks,
        "odd_rank_agreement": ranks["3"] == ranks["5"],
        "odd_minus_two_rank": gap,
        "bockstein_high_forward": high,
        "bockstein_low_reverse": low,
        "opposite_agreement": high == low,
        "rank_gap_matches_bockstein": (
            ranks["3"] == ranks["5"] and gap == high["bockstein_rank"]
        ),
        "projection_hash": digest(
            {"kept_rows": kept_rows, "row_atoms": atoms, "signed_columns": signed_columns}
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p-min", type=int, default=8)
    parser.add_argument("--p-max", type=int, default=11)
    parser.add_argument("--budget-seconds", type=float, default=1800.0)
    parser.add_argument("--memory-gib", type=float, default=20.0)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if args.p_min < 8 or args.p_max > 11 or args.p_min > args.p_max:
        raise ValueError("declared range is 8<=p_min<=p_max<=11")

    premise_hashes = verify_premises()
    exp042 = load_module("exp042_frozen_for_exp045", EXP042 / "run.py")
    exp037 = exp042.load_module("exp037_frozen_for_exp045", exp042.EXP037 / "run.py")
    budget = exp037.Budget(args.budget_seconds, args.memory_gib)
    result: dict[str, object] = {
        "experiment": "EXP-045",
        "route": "complete subset lattice of the six normalized row atoms",
        "status": "RUNNING",
        "parameters": {
            "p_min": args.p_min,
            "p_max": args.p_max,
            "budget_seconds": args.budget_seconds,
            "memory_gib": args.memory_gib,
        },
        "atom_aliases": ATOM_ALIASES,
        "premise_hashes": premise_hashes,
        "rows": [],
    }
    write_json_atomic(args.output, result)
    try:
        for p in range(args.p_min, args.p_max + 1):
            matrix_path = EXP042 / "artifacts" / f"matrix-p{p}.json"
            matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
            if set(atom_values(matrix)) != set(ATOM_ALIASES.values()):
                raise AssertionError({"p": p, "row_atom_universe_mismatch": matrix["row_atom_table"]})
            subsets: list[dict[str, object]] = []
            for mask in range(FULL_MASK + 1):
                if mask % 8 == 0:
                    print(f"p={p} subsets={mask}/64", flush=True)
                subsets.append(
                    evaluate_subset(
                        matrix=matrix, mask=mask, exp042=exp042, exp037=exp037
                    )
                )
                budget.check(f"p={p} mask={mask}")
            nonzero = {
                int(row["mask"])
                for row in subsets
                if int(row["bockstein_high_forward"]["bockstein_rank"]) > 0
            }
            full_rank = {
                int(row["mask"])
                for row in subsets
                if int(row["bockstein_high_forward"]["bockstein_rank"])
                == EXPECTED_BETA[p]
            }
            result["rows"].append(
                {
                    "p": p,
                    "source_matrix_sha256": sha256(matrix_path),
                    "source_bockstein_rank": EXPECTED_BETA[p],
                    "subsets": subsets,
                    "nonzero_carrier_masks": sorted(nonzero),
                    "minimal_nonzero_carrier_masks": minimal_masks(nonzero),
                    "full_carrier_masks": sorted(full_rank),
                    "minimal_full_carrier_masks": minimal_masks(full_rank),
                }
            )
            result["status"] = "CHECKPOINT"
            result["elapsed_seconds"] = budget.elapsed
            write_json_atomic(args.output, result)
    except exp037.BudgetStop as error:
        result["status"] = "INCONCLUSIVE_RESOURCE_BUDGET"
        result["resource_stop"] = str(error)
        result["elapsed_seconds"] = budget.elapsed
        result["artifact_hash"] = digest(result)
        write_json_atomic(args.output, result)
        return 2

    full_range = {int(row["p"]) for row in result["rows"]} == {8, 9, 10, 11}
    p1 = all(
        next(
            subset for subset in row["subsets"] if int(subset["mask"]) == FULL_MASK ^ (1 << bit)
        )["bockstein_high_forward"]["bockstein_rank"]
        == 0
        for row in result["rows"]
        for bit in range(len(ALIASES))
    )
    p2 = all(row["nonzero_carrier_masks"] == [FULL_MASK] for row in result["rows"])
    antichains = {
        (
            tuple(row["minimal_nonzero_carrier_masks"]),
            tuple(row["minimal_full_carrier_masks"]),
        )
        for row in result["rows"]
    }
    p3 = (
        len(antichains) == 1
        and all(
            subset["opposite_agreement"] and subset["rank_gap_matches_bockstein"]
            for row in result["rows"]
            for subset in row["subsets"]
        )
    )
    result["p1_status"] = (
        "PASS_FINITE" if full_range and p1 else "REFUTED" if full_range else "NOT_EVALUATED"
    )
    result["p2_status"] = (
        "PASS_FINITE" if full_range and p2 else "REFUTED" if full_range else "NOT_EVALUATED"
    )
    result["p3_status"] = (
        "PASS_FINITE" if full_range and p3 else "REFUTED" if full_range else "NOT_EVALUATED"
    )
    result["status"] = "COMPLETE"
    result["elapsed_seconds"] = budget.elapsed
    result["artifact_hash"] = digest(result)
    write_json_atomic(args.output, result)
    print(
        json.dumps(
            {
                "experiment": result["experiment"],
                "status": result["status"],
                "p1_status": result["p1_status"],
                "p2_status": result["p2_status"],
                "p3_status": result["p3_status"],
                "minimal_nonzero": {
                    str(row["p"]): row["minimal_nonzero_carrier_masks"]
                    for row in result["rows"]
                },
                "minimal_full": {
                    str(row["p"]): row["minimal_full_carrier_masks"]
                    for row in result["rows"]
                },
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
