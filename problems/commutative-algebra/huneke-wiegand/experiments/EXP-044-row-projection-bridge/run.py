"""EXP-044 exact row projections of the isolated Bockstein bridge.

CPU only. The runner verifies and reloads the frozen EXP-042 integer
matrices, projects their rows by semantic atom, and recomputes exact finite
field ranks and first Bocksteins without rebuilding the large ambient block.
"""

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
DEFAULT_OUTPUT = HERE / "artifacts" / "results.json"
DB_ATOM = '["row","D","B",[-2,-3,2,0,0,0,0,0,0,0]]'
KC0_ATOM = '["row","K","C0",[-2,-2,1,0,0,0,0,0,0,0]]'
EXPECTED_BETA = {8: 3, 9: 4, 10: 5, 11: 7}
PREMISES = {
    EXP042 / "run.py": "3a57fc52a6a1e10ba42d97c6ebe27062324b8c90b76df7a288db41dffabd69bf",
    EXP042 / "artifacts" / "results.json": (
        "3c4ae292fb17a5daf473aee0ed37e473000de686607b5da0a0f4c357a8216ee2"
    ),
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
}
PROJECTIONS = {
    "drop_db": lambda atom: atom != DB_ATOM,
    "drop_kc0": lambda atom: atom != KC0_ATOM,
    "drop_both": lambda atom: atom not in {DB_ATOM, KC0_ATOM},
    "only_union": lambda atom: atom in {DB_ATOM, KC0_ATOM},
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


def atom_values(matrix: dict[str, object]) -> list[str]:
    table = matrix["row_atom_table"]
    return [table[index] for index in matrix["row_atom_ids"]]


def project_matrix(
    matrix: dict[str, object], predicate: object, exp042: ModuleType
) -> dict[str, object]:
    atoms = atom_values(matrix)
    kept_rows = [row for row, atom in enumerate(atoms) if predicate(atom)]
    row_map = [-1] * len(atoms)
    for projected, original in enumerate(kept_rows):
        row_map[original] = projected
    signed_columns = [
        [(row_map[row], sign) for row, sign in entries if row_map[row] >= 0]
        for entries in matrix["signed_columns"]
    ]
    projected_atoms = [atoms[row] for row in kept_rows]
    row_atom_table, row_atom_ids = exp042.table_encode(projected_atoms)
    atom_counts = dict(sorted(Counter(projected_atoms).items()))
    return {
        "rows": len(kept_rows),
        "columns": len(signed_columns),
        "nonzero_columns": sum(bool(entries) for entries in signed_columns),
        "nonzeros": sum(map(len, signed_columns)),
        "kept_row_atom_counts": atom_counts,
        "row_atom_table": row_atom_table,
        "row_atom_ids": row_atom_ids,
        "signed_columns": signed_columns,
        "projection_hash": digest(
            {
                "kept_rows": kept_rows,
                "signed_columns": signed_columns,
                "row_atoms": projected_atoms,
            }
        ),
    }


def evaluate_projection(
    *, matrix: dict[str, object], name: str, exp042: ModuleType, exp037: ModuleType
) -> dict[str, object]:
    projected = project_matrix(matrix, PROJECTIONS[name], exp042)
    signed_columns = projected.pop("signed_columns")
    row_atom_table = projected.pop("row_atom_table")
    row_atom_ids = projected.pop("row_atom_ids")
    ranks = exp042.rank_fields(exp037, signed_columns)
    forward = exp042.bockstein_profile(
        signed_columns=signed_columns,
        row_count=projected["rows"],
        row_atom_table=row_atom_table,
        row_atom_ids=row_atom_ids,
        column_atom_table=matrix["column_atom_table"],
        column_atom_ids=matrix["column_atom_ids"],
        reverse=False,
    )
    reverse = exp042.bockstein_profile(
        signed_columns=signed_columns,
        row_count=projected["rows"],
        row_atom_table=row_atom_table,
        row_atom_ids=row_atom_ids,
        column_atom_table=matrix["column_atom_table"],
        column_atom_ids=matrix["column_atom_ids"],
        reverse=True,
    )
    rank_gap = int(ranks["3"]) - int(ranks["2"])
    projected.update(
        {
            "name": name,
            "ranks": ranks,
            "odd_rank_agreement": ranks["3"] == ranks["5"],
            "odd_minus_two_rank": rank_gap,
            "bockstein": {"forward": forward, "reverse": reverse},
            "order_agreement": forward["bockstein_rank"] == reverse["bockstein_rank"],
            "rank_gap_matches_bockstein": (
                ranks["3"] == ranks["5"] and rank_gap == forward["bockstein_rank"]
            ),
        }
    )
    return projected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p-min", type=int, default=8)
    parser.add_argument("--p-max", type=int, default=11)
    parser.add_argument("--budget-seconds", type=float, default=1200.0)
    parser.add_argument("--memory-gib", type=float, default=16.0)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if args.p_min < 8 or args.p_max > 11 or args.p_min > args.p_max:
        raise ValueError("declared range is 8<=p_min<=p_max<=11")

    premise_hashes = verify_premises()
    exp042 = load_module("exp042_frozen_for_exp044", EXP042 / "run.py")
    exp037 = exp042.load_module("exp037_frozen_for_exp044", exp042.EXP037 / "run.py")
    budget = exp037.Budget(args.budget_seconds, args.memory_gib)
    result: dict[str, object] = {
        "experiment": "EXP-044",
        "route": "row-projection localization of the signed Bockstein bridge",
        "status": "RUNNING",
        "parameters": {
            "p_min": args.p_min,
            "p_max": args.p_max,
            "budget_seconds": args.budget_seconds,
            "memory_gib": args.memory_gib,
        },
        "target_atoms": {"db": DB_ATOM, "kc0": KC0_ATOM},
        "premise_hashes": premise_hashes,
        "rows": [],
    }
    write_json_atomic(args.output, result)
    try:
        for p in range(args.p_min, args.p_max + 1):
            budget.check(f"p={p} load")
            path = EXP042 / "artifacts" / f"matrix-p{p}.json"
            matrix = json.loads(path.read_text(encoding="utf-8"))
            atoms = atom_values(matrix)
            atom_counts = Counter(atoms)
            if not atom_counts[DB_ATOM] or not atom_counts[KC0_ATOM]:
                raise AssertionError({"p": p, "missing_target_atoms": dict(atom_counts)})
            row: dict[str, object] = {
                "p": p,
                "source_matrix": path.name,
                "source_sha256": sha256(path),
                "source_dimensions": [matrix["rows"], matrix["columns"]],
                "source_ranks": matrix["ranks"],
                "source_bockstein_rank": matrix["bockstein"]["forward"]["bockstein_rank"],
                "target_atom_row_counts": {
                    "db": atom_counts[DB_ATOM],
                    "kc0": atom_counts[KC0_ATOM],
                },
                "projections": {},
            }
            for name in PROJECTIONS:
                print(f"p={p} projection={name}", flush=True)
                row["projections"][name] = evaluate_projection(
                    matrix=matrix, name=name, exp042=exp042, exp037=exp037
                )
                budget.check(f"p={p} projection={name}")
            result["rows"].append(row)
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

    full_range = {row["p"] for row in result["rows"]} == {8, 9, 10, 11}
    p1_matches = all(
        row["projections"][name]["bockstein"]["forward"]["bockstein_rank"] == 0
        for row in result["rows"]
        for name in ("drop_db", "drop_kc0", "drop_both")
    )
    p2_matches = all(
        row["projections"]["only_union"]["bockstein"]["forward"]["bockstein_rank"]
        == EXPECTED_BETA[row["p"]]
        for row in result["rows"]
    )
    p3_matches = all(
        projection["order_agreement"] and projection["rank_gap_matches_bockstein"]
        for row in result["rows"]
        for projection in row["projections"].values()
    )
    result["p1_status"] = (
        "PASS_FINITE" if full_range and p1_matches else "REFUTED" if full_range else "NOT_EVALUATED"
    )
    result["p2_status"] = (
        "PASS_FINITE" if full_range and p2_matches else "REFUTED" if full_range else "NOT_EVALUATED"
    )
    result["p3_status"] = (
        "PASS_FINITE" if full_range and p3_matches else "REFUTED" if full_range else "NOT_EVALUATED"
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
