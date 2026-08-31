"""EXP-040 exact p=10/11 component-partition falsifier.

CPU only.  This imports the frozen EXP-039 component decomposition, adds the
already audited complete-rank gates for p=10 and p=11, and tests the declared
merged-sector partitions over GF(2), GF(3), and GF(5).
"""

from __future__ import annotations

import argparse
import gc
import hashlib
import importlib.util
import json
from pathlib import Path
from types import ModuleType


HERE = Path(__file__).resolve().parent
EXP039 = HERE.parent / "EXP-039-core-component-stabilization"
DEFAULT_OUTPUT = HERE / "artifacts" / "results.json"
PREMISES = {
    "EXP-039 proof": (
        EXP039 / "proof.md",
        "43071ff8b6a3c23acc319798aab3fdac78610665ec95506e32ff2e5053fb28da",
    ),
    "EXP-039 verdict": (
        EXP039 / "verdict.md",
        "61376ab683151239c7c6f446f2d0cf55afe76e00b2fcad32fa69baf27621042e",
    ),
    "EXP-039 run.py": (
        EXP039 / "run.py",
        "8ab5678829094a2b314a23889201b06f555aafc5af176500ef62a5eb30e4a352",
    ),
    "EXP-039 result": (
        EXP039 / "artifacts" / "results-p9.json",
        "831a4300cac10bf44753050a686a7993fabef09bf28b4332c6bb1fb9881c9e2c",
    ),
    "EXP-039 audit": (
        EXP039 / "artifacts" / "audit-certificate.json",
        "55e3159dd01f9c412ad56a5808eda1f428672341b57ce5dd6eb4e2f266051534",
    ),
}
EXPECTED_COMPLETE_RANKS = {
    10: {2: 738459, 3: 738531, 5: 738531},
    11: {2: 1683307, 3: 1683409, 5: 1683409},
}
EXPECTED_PARTITIONS = {10: [67, 5], 11: [96, 6]}


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
    actual = {name: sha256(path) for name, (path, _) in PREMISES.items()}
    expected = {name: expected_hash for name, (_, expected_hash) in PREMISES.items()}
    if actual != expected:
        raise AssertionError({"premise_hash_mismatch": {"actual": actual, "expected": expected}})
    return actual


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def defect_partition(row: dict[str, object]) -> list[int]:
    return sorted(
        (
            int(component["odd_minus_two_rank_defect"])
            for component in row["components"]
            if component["odd_minus_two_rank_defect"]
        ),
        reverse=True,
    )


def componentwise_odd_agreement(row: dict[str, object]) -> bool:
    return all(
        component["ranks"]["3"] == component["ranks"]["5"]
        for component in row["components"]
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p-max", type=int, choices=(10, 11), default=11)
    parser.add_argument("--budget-seconds", type=float, default=2400.0)
    parser.add_argument("--memory-gib", type=float, default=36.0)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    premise_hashes = verify_premises()
    exp039 = load_module("exp039_frozen_for_exp040", EXP039 / "run.py")
    exp037 = exp039.load_module(
        "exp037_frozen_for_exp040", exp039.EXP037 / "run.py"
    )
    exp036 = exp037.load_exp036()
    exp039.exp037_exp036 = exp036
    exp039.EXPECTED_COMBINED_RANKS.update(EXPECTED_COMPLETE_RANKS)
    budget = exp037.Budget(args.budget_seconds, args.memory_gib)
    result: dict[str, object] = {
        "experiment": "EXP-040",
        "route": "merged-sector component partitions over GF(2), GF(3), and GF(5)",
        "status": "RUNNING",
        "parameters": {
            "p_min": 10,
            "p_max": args.p_max,
            "t": 2,
            "fields": [2, 3, 5],
            "budget_seconds": args.budget_seconds,
            "memory_gib": args.memory_gib,
        },
        "premise_hashes": premise_hashes,
        "predictions": {str(p): value for p, value in EXPECTED_PARTITIONS.items()},
        "rows": [],
    }
    write_json_atomic(args.output, result)
    try:
        for p in range(10, args.p_max + 1):
            print(f"building complete basis for p={p}", flush=True)
            basis = exp037.build_basis(exp036, p, 2)
            d_rows = exp037.d_rows_for_basis(exp036, basis, budget)
            row = exp039.analyze_combined_core(
                exp037=exp037,
                basis=basis,
                d_rows=d_rows,
                fields=(2, 3, 5),
                budget=budget,
            )
            partition = defect_partition(row)
            row["declared_partition"] = EXPECTED_PARTITIONS[p]
            row["partition_matches"] = partition == EXPECTED_PARTITIONS[p]
            row["componentwise_gf3_gf5_agreement"] = componentwise_odd_agreement(row)
            result["rows"].append(row)
            result["status"] = "CHECKPOINT"
            result["elapsed_seconds"] = budget.elapsed
            write_json_atomic(args.output, result)
            print(
                f"p={p} declared partition={EXPECTED_PARTITIONS[p]}, observed={partition}, "
                f"odd agreement={row['componentwise_gf3_gf5_agreement']}",
                flush=True,
            )
            if not row["partition_matches"] or not row["componentwise_gf3_gf5_agreement"]:
                result["status"] = "REFUTED"
                result["stopped_after_p"] = p
                break
            del basis, d_rows
            gc.collect()
    except exp037.BudgetStop as error:
        result["status"] = "RESOURCE_STOP"
        result["resource_stop"] = str(error)
        result["elapsed_seconds"] = budget.elapsed
        result["artifact_hash"] = digest(result)
        write_json_atomic(args.output, result)
        print(json.dumps({"status": result["status"], "error": str(error)}, indent=2))
        return 2

    rows = result["rows"]
    if result["status"] != "REFUTED":
        result["status"] = "PASS_FINITE" if len(rows) == args.p_max - 9 else "INCONCLUSIVE"
    result["p1_status"] = (
        "PASS_FINITE"
        if rows and rows[0]["partition_matches"] and rows[0]["componentwise_gf3_gf5_agreement"]
        else "REFUTED"
    )
    if args.p_max == 11 and len(rows) == 2:
        result["p2_status"] = (
            "PASS_FINITE"
            if rows[1]["partition_matches"] and rows[1]["componentwise_gf3_gf5_agreement"]
            else "REFUTED"
        )
    else:
        result["p2_status"] = "NOT_RUN"
    result["p3_status"] = "NOT_ATTEMPTED"
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
                "completed_parameters": [row["p"] for row in rows],
                "elapsed_seconds": result["elapsed_seconds"],
                "artifact_hash": result["artifact_hash"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
