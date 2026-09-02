"""EXP-047 exact relative kernel images and Smith forms."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path

import flint
from flint import fmpz_mat


HERE = Path(__file__).resolve().parent
EXP042 = HERE.parent / "EXP-042-bockstein-normal-form"
EXP045 = HERE.parent / "EXP-045-row-atom-carrier-lattice"
DEFAULT_OUTPUT = HERE / "artifacts" / "results.json"
INCLUSIONS = ((58, 59), (58, 62), (56, 58))
ATOM_ALIASES = {
    "R0": '["row","D","A",[-2,-3,1,0,1,0,0,0,0,0]]',
    "R1": '["row","D","A",[-3,-2,2,0,0,0,0,0,0,0]]',
    "R2": '["row","D","B",[-1,-4,1,0,1,0,0,0,0,0]]',
    "R3": '["row","D","B",[-2,-3,2,0,0,0,0,0,0,0]]',
    "R4": '["row","K","C0",[-2,-2,1,0,0,0,0,0,0,0]]',
    "R5": '["row","K","C2",[-1,-3,1,0,0,0,0,0,0,0]]',
}
ALIASES = tuple(ATOM_ALIASES)
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
    EXP045 / "artifacts" / "results.json": (
        "569220667e9d82f0806ea96cb8f60c49e94cb6317817170c39f2e574e619bcb8"
    ),
}


class BudgetStop(RuntimeError):
    """Raised between exact operations after the declared budget expires."""


class Budget:
    def __init__(self, seconds: float) -> None:
        self.started = time.monotonic()
        self.seconds = seconds

    @property
    def elapsed(self) -> float:
        return time.monotonic() - self.started

    def check(self, stage: str) -> None:
        if self.elapsed > self.seconds:
            raise BudgetStop(f"time budget exceeded after {stage}: {self.elapsed:.3f}s")


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


def verify_premises() -> dict[str, str]:
    actual = {str(path.relative_to(HERE.parent)): sha256(path) for path in PREMISES}
    expected = {
        str(path.relative_to(HERE.parent)): expected_hash
        for path, expected_hash in PREMISES.items()
    }
    if actual != expected:
        raise AssertionError({"premise_hash_mismatch": {"actual": actual, "expected": expected}})
    return actual


def atom_values(matrix: dict[str, object], side: str) -> list[str]:
    table = matrix[f"{side}_atom_table"]
    return [table[int(index)] for index in matrix[f"{side}_atom_ids"]]


def aliases(mask: int) -> list[str]:
    return [alias for bit, alias in enumerate(ALIASES) if mask & (1 << bit)]


def rows_for_mask(row_atoms: list[str], mask: int) -> list[int]:
    selected = {ATOM_ALIASES[alias] for alias in aliases(mask)}
    return [row for row, atom in enumerate(row_atoms) if atom in selected]


def build_transposed_source(
    signed_columns: list[list[list[int]]], source_rows: list[int]
) -> fmpz_mat:
    row_map = {original: projected for projected, original in enumerate(source_rows)}
    transposed = fmpz_mat(len(signed_columns), len(source_rows))
    for column, entries in enumerate(signed_columns):
        for row, sign in entries:
            projected = row_map.get(int(row))
            if projected is not None:
                transposed[column, projected] = int(sign)
    return transposed


def bottom_zero_count(hnf: fmpz_mat) -> int:
    zero_count = 0
    for row in range(hnf.nrows() - 1, -1, -1):
        if any(hnf[row, column] for column in range(hnf.ncols())):
            break
        zero_count += 1
    return zero_count


def saturated_kernel(
    signed_columns: list[list[list[int]]], source_rows: list[int]
) -> tuple[list[list[int]], dict[str, object]]:
    transposed = build_transposed_source(signed_columns, source_rows)
    hnf, transform = transposed.hnf(transform=True)
    nullity = bottom_zero_count(hnf)
    rank = hnf.nrows() - nullity
    if rank and not any(hnf[rank - 1, column] for column in range(hnf.ncols())):
        raise AssertionError("HNF rank boundary is zero")
    kernel_rows = [
        [int(transform[row, column]) for column in range(transform.ncols())]
        for row in range(rank, transform.nrows())
    ]
    return kernel_rows, {
        "source_rows": len(source_rows),
        "columns": len(signed_columns),
        "rank_q": rank,
        "kernel_nullity": nullity,
        "kernel_basis_hash": digest(kernel_rows),
        "annihilation_from_zero_hnf_rows": True,
    }


def added_row_entries(
    signed_columns: list[list[list[int]]], added_rows: list[int]
) -> list[list[list[int]]]:
    row_map = {original: projected for projected, original in enumerate(added_rows)}
    entries_by_row: list[list[list[int]]] = [[] for _ in added_rows]
    for column, entries in enumerate(signed_columns):
        for row, sign in entries:
            projected = row_map.get(int(row))
            if projected is not None:
                entries_by_row[projected].append([column, int(sign)])
    return entries_by_row


def relative_rows(
    kernel_rows: list[list[int]], entries_by_row: list[list[list[int]]]
) -> list[list[int]]:
    return [
        [
            sum(sign * kernel[column] for column, sign in entries)
            for kernel in kernel_rows
        ]
        for entries in entries_by_row
    ]


def sparse_columns(matrix_rows: list[list[int]]) -> list[list[list[int]]]:
    column_count = len(matrix_rows[0]) if matrix_rows else 0
    return [
        [
            [row, int(matrix_rows[row][column])]
            for row in range(len(matrix_rows))
            if matrix_rows[row][column]
        ]
        for column in range(column_count)
    ]


def modular_rank(columns: list[list[list[int]]], prime: int) -> int:
    pivots: dict[int, dict[int, int]] = {}
    for entries in columns:
        vector = {
            int(row): int(value) % prime
            for row, value in entries
            if int(value) % prime
        }
        while vector:
            pivot = max(vector)
            coefficient = vector[pivot]
            if pivot not in pivots:
                inverse = pow(coefficient, -1, prime)
                pivots[pivot] = {
                    row: value * inverse % prime for row, value in vector.items()
                }
                break
            basis = pivots[pivot]
            for row, value in basis.items():
                replacement = (vector.get(row, 0) - coefficient * value) % prime
                if replacement:
                    vector[row] = replacement
                else:
                    vector.pop(row, None)
    return len(pivots)


def smith_record(matrix_rows: list[list[int]]) -> dict[str, object]:
    row_count = len(matrix_rows)
    column_count = len(matrix_rows[0]) if matrix_rows else 0
    relation = fmpz_mat(matrix_rows) if row_count and column_count else fmpz_mat(row_count, column_count)
    smith = relation.snf()
    diagonal = [abs(int(smith[index, index])) for index in range(min(row_count, column_count))]
    nonzero_diagonal = [value for value in diagonal if value]
    units = sum(value == 1 for value in nonzero_diagonal)
    torsion = [value for value in nonzero_diagonal if value > 1]
    columns = sparse_columns(matrix_rows)
    ranks = {str(prime): modular_rank(columns, prime) for prime in (2, 3, 5)}
    return {
        "rows": row_count,
        "columns": column_count,
        "nonzeros": sum(bool(value) for row in matrix_rows for value in row),
        "max_entry_bits": max(
            (abs(value).bit_length() for row in matrix_rows for value in row), default=0
        ),
        "matrix_hash": digest(matrix_rows),
        "rank_q": len(nonzero_diagonal),
        "ranks": ranks,
        "unit_invariant_count": units,
        "torsion_invariants": torsion,
        "free_rank": row_count - len(nonzero_diagonal),
        "smith_diagonal_hash": digest(diagonal),
        "rank_from_smith_matches_mod_odd": (
            len(nonzero_diagonal) == ranks["3"] == ranks["5"]
        ),
        "rank_mod_two_from_smith": sum(value % 2 for value in nonzero_diagonal)
        == ranks["2"],
    }


def relative_module(
    *,
    p: int,
    source_mask: int,
    target_mask: int,
    signed_columns: list[list[list[int]]],
    row_atoms: list[str],
    kernel_rows: list[list[int]],
    source_kernel: dict[str, object],
    stored_subsets: dict[int, dict[str, object]],
) -> dict[str, object]:
    source_rows = rows_for_mask(row_atoms, source_mask)
    target_rows = rows_for_mask(row_atoms, target_mask)
    source_set = set(source_rows)
    added_rows = [row for row in target_rows if row not in source_set]
    entries = added_row_entries(signed_columns, added_rows)
    matrix_rows = relative_rows(kernel_rows, entries)
    relative = smith_record(matrix_rows)
    artifact: dict[str, object] = {
        "experiment": "EXP-047",
        "p": p,
        "source_mask": source_mask,
        "target_mask": target_mask,
        "source_rows_hash": digest(source_rows),
        "added_rows_hash": digest(added_rows),
        "kernel_basis_hash": source_kernel["kernel_basis_hash"],
        "matrix_rows": matrix_rows,
    }
    artifact["artifact_hash"] = digest(artifact)
    artifact_path = HERE / "artifacts" / f"relative-p{p}-m{source_mask}-m{target_mask}.json"
    write_json_atomic(artifact_path, artifact)
    source_stored = stored_subsets[source_mask]
    target_stored = stored_subsets[target_mask]
    exact_target_rank = int(source_kernel["rank_q"]) + int(relative["rank_q"])
    return {
        "source_mask": source_mask,
        "target_mask": target_mask,
        "source_aliases": aliases(source_mask),
        "target_aliases": aliases(target_mask),
        "added_aliases": sorted(set(aliases(target_mask)) - set(aliases(source_mask))),
        "source_rows": len(source_rows),
        "added_rows": len(added_rows),
        "added_rows_hash": digest(added_rows),
        "source_kernel": source_kernel,
        "relative": relative,
        "relative_artifact": str(artifact_path.relative_to(HERE)),
        "relative_artifact_sha256": sha256(artifact_path),
        "relative_artifact_internal_hash": artifact["artifact_hash"],
        "exact_target_rank_q": exact_target_rank,
        "source_rank_matches_stored_odd": int(source_kernel["rank_q"])
        == int(source_stored["ranks"]["3"])
        == int(source_stored["ranks"]["5"]),
        "target_rank_matches_stored_odd": exact_target_rank
        == int(target_stored["ranks"]["3"])
        == int(target_stored["ranks"]["5"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p-min", type=int, default=8)
    parser.add_argument("--p-max", type=int, default=11)
    parser.add_argument("--budget-seconds", type=float, default=3600.0)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if args.p_min < 8 or args.p_max > 11 or args.p_min > args.p_max:
        raise ValueError("declared range is 8<=p_min<=p_max<=11")
    if flint.__version__ != "0.9.0":
        raise RuntimeError(f"python-flint 0.9.0 required, found {flint.__version__}")

    premises = verify_premises()
    exp045 = json.loads((EXP045 / "artifacts" / "results.json").read_text(encoding="utf-8"))
    stored_rows = {int(row["p"]): row for row in exp045["rows"]}
    budget = Budget(args.budget_seconds)
    result: dict[str, object] = {
        "experiment": "EXP-047",
        "route": "saturated integer kernel images and exact relative Smith forms",
        "status": "RUNNING",
        "engine": {"python_flint": flint.__version__},
        "parameters": {
            "p_min": args.p_min,
            "p_max": args.p_max,
            "inclusions": [list(pair) for pair in INCLUSIONS],
            "budget_seconds": args.budget_seconds,
        },
        "premise_hashes": premises,
        "rows": [],
    }
    write_json_atomic(args.output, result)
    try:
        for p in range(args.p_min, args.p_max + 1):
            print(f"p={p} load", flush=True)
            matrix_path = EXP042 / "artifacts" / f"matrix-p{p}.json"
            matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
            signed_columns = matrix["signed_columns"]
            row_atoms = atom_values(matrix, "row")
            stored_subsets = {
                int(subset["mask"]): subset for subset in stored_rows[p]["subsets"]
            }
            kernels: dict[int, tuple[list[list[int]], dict[str, object]]] = {}
            for source_mask in sorted({source for source, _ in INCLUSIONS}):
                print(f"p={p} source={source_mask} transformed HNF", flush=True)
                kernels[source_mask] = saturated_kernel(
                    signed_columns, rows_for_mask(row_atoms, source_mask)
                )
                budget.check(f"p={p} source={source_mask} HNF")
            records: list[dict[str, object]] = []
            for source_mask, target_mask in INCLUSIONS:
                print(f"p={p} {source_mask}->{target_mask} Smith", flush=True)
                kernel_rows, source_kernel = kernels[source_mask]
                records.append(
                    relative_module(
                        p=p,
                        source_mask=source_mask,
                        target_mask=target_mask,
                        signed_columns=signed_columns,
                        row_atoms=row_atoms,
                        kernel_rows=kernel_rows,
                        source_kernel=source_kernel,
                        stored_subsets=stored_subsets,
                    )
                )
                budget.check(f"p={p} {source_mask}->{target_mask} Smith")
            result["rows"].append(
                {
                    "p": p,
                    "source_matrix_sha256": sha256(matrix_path),
                    "inclusions": records,
                }
            )
            result["status"] = "CHECKPOINT"
            result["elapsed_seconds"] = budget.elapsed
            write_json_atomic(args.output, result)
    except BudgetStop as error:
        result["status"] = "INCONCLUSIVE_RESOURCE_BUDGET"
        result["resource_stop"] = str(error)
        result["elapsed_seconds"] = budget.elapsed
        result["artifact_hash"] = digest(result)
        write_json_atomic(args.output, result)
        return 2

    records_by_key = {
        (int(row["p"]), int(record["source_mask"]), int(record["target_mask"])): record
        for row in result["rows"]
        for record in row["inclusions"]
    }
    full_range = {int(row["p"]) for row in result["rows"]} == {8, 9, 10, 11}
    p1 = all(
        records_by_key[p, 58, 59]["relative"]["torsion_invariants"] == [2, 2]
        and records_by_key[p, 58, 59]["relative"]["free_rank"]
        == (p - 2) * (p - 3) // 2
        and records_by_key[p, 58, 62]["relative"]["torsion_invariants"] == [2, 2]
        and records_by_key[p, 58, 62]["relative"]["free_rank"] == p * p - 4 * p - 3
        for p in range(8, 12)
    ) if full_range else False
    p2 = all(
        records_by_key[p, source, target]["relative"]["torsion_invariants"] == [2, 2]
        for p in range(8, 12)
        for source, target in ((58, 59), (58, 62))
    ) if full_range else False
    p3 = all(
        records_by_key[p, 56, 58]["relative"]["torsion_invariants"] == [2] * (p - 7)
        and records_by_key[p, 56, 58]["relative"]["free_rank"]
        == int(records_by_key[p, 56, 58]["added_rows"]) - (3 * p - 7)
        for p in range(8, 12)
    ) if full_range else False
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
                "torsion": {
                    f"p{p}_{source}_{target}": records_by_key[p, source, target][
                        "relative"
                    ]["torsion_invariants"]
                    for p in range(8, 12)
                    for source, target in INCLUSIONS
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
