"""EXP-038 exact p=11 falsifier for the first degree-six correction."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
from types import ModuleType


HERE = Path(__file__).resolve().parent
EXP037 = HERE.parent / "EXP-037-connecting-quasipolynomial"
DEFAULT_OUTPUT = HERE / "artifacts" / "target-t2-p11.json"
PREMISES = {
    "EXP-037 proof": (
        EXP037 / "proof.md",
        "ae2c3be4ec509264717fef48dd2cd73a47fe51c46a37240372a7a117ff5cc330",
    ),
    "EXP-037 verdict": (
        EXP037 / "verdict.md",
        "ccc185190e885c334bcf6f401d47c2f4b1f44d8a3931226b240b3528e07b70bb",
    ),
    "EXP-037 run.py": (
        EXP037 / "run.py",
        "1abebc24c99398dded97aa08216211db089889e154736ed9eb5a7202de0b5df0",
    ),
    "EXP-037 p=10 target": (
        EXP037 / "artifacts" / "target-t2-p10.json",
        "ca97087466fdd705e22f69e79cdfecfc7dbce0684475b98bd99757cfed030d7b",
    ),
    "EXP-037 audit": (
        EXP037 / "artifacts" / "audit-certificate.json",
        "03682871743842bb8a3224b70aee72436ed21056de3d83dfb178f9023c7ad088",
    ),
}
KNOWN_EXCESS = {4: 1, 5: 4, 6: 9, 7: 18, 8: 31, 9: 49, 10: 72}


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def verify_premises() -> dict[str, str]:
    actual = {name: file_hash(path) for name, (path, _) in PREMISES.items()}
    expected = {name: expected for name, (_, expected) in PREMISES.items()}
    if actual != expected:
        raise AssertionError({"premise_hash_mismatch": {"actual": actual, "expected": expected}})
    return actual


def load_exp037() -> ModuleType:
    path = EXP037 / "run.py"
    spec = importlib.util.spec_from_file_location("exp037_frozen", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def denominator_coefficient(n: int) -> int:
    if n < 0:
        return 0
    total = 0
    for c_value in range(n // 3 + 1):
        after_c = n - 3 * c_value
        for b_value in range(after_c // 2 + 1):
            total += after_c - 2 * b_value + 1
    return total


def corrected_coefficient(p: int, exp037: ModuleType) -> int:
    n = p - 4
    return exp037.candidate_lattice(p) - denominator_coefficient(n - 6)


def formula_certificate(exp037: ModuleType) -> dict[str, object]:
    checks = {str(p): corrected_coefficient(p, exp037) for p in KNOWN_EXCESS}
    if checks != {str(p): value for p, value in KNOWN_EXCESS.items()}:
        raise AssertionError({"known_formula_mismatch": checks})
    coefficients = [corrected_coefficient(p, exp037) for p in range(4, 41)]
    corrections = [denominator_coefficient(p - 10) for p in range(4, 41)]
    return {
        "known_checks": checks,
        "predictions": {"11": corrected_coefficient(11, exp037), "12": corrected_coefficient(12, exp037)},
        "coefficients_p4_p40": coefficients,
        "shifted_denominator_corrections_p4_p40": corrections,
        "coefficient_hash": digest(coefficients),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p", type=int, default=11)
    parser.add_argument("--fields", default="2,3")
    parser.add_argument(
        "--core-order",
        choices=("low-degree", "canonical", "reverse-low-degree"),
        default="low-degree",
    )
    parser.add_argument("--formula-only", action="store_true")
    parser.add_argument("--budget-seconds", type=float, default=3600.0)
    parser.add_argument("--memory-gib", type=float, default=40.0)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if args.p < 4:
        raise ValueError("require p>=4")
    fields = tuple(int(value) for value in args.fields.split(",") if value)
    if any(value < 2 for value in fields):
        raise ValueError("fields must be prime integers")

    exp037 = load_exp037()
    budget = exp037.Budget(args.budget_seconds, args.memory_gib)
    result: dict[str, object] = {
        "experiment": "EXP-038",
        "route": "degree-six-relation falsifier with frozen two-sided exact ranks",
        "status": "RUNNING",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "parameters": {
            "p": args.p,
            "t": 2,
            "fields": list(fields),
            "core_order": args.core_order,
            "budget_seconds": args.budget_seconds,
            "memory_gib": args.memory_gib,
        },
        "premise_hashes": verify_premises(),
        "formula_certificate": formula_certificate(exp037),
        "rows": [],
    }
    exp037.write_json_atomic(args.output, result)
    predicted = corrected_coefficient(args.p, exp037)
    print(f"corrected formula gate: PASS; predicted e_{args.p}={predicted}", flush=True)
    if args.formula_only:
        result["status"] = "PASS_FORMULA_ONLY"
        result["elapsed_seconds"] = round(budget.elapsed, 6)
        result["artifact_sha256"] = digest(result)
        exp037.write_json_atomic(args.output, result)
        return 0

    frozen_exp036 = exp037.load_exp036()
    try:
        budget.check("basis start")
        basis = exp037.build_basis(frozen_exp036, args.p, 2)
        print(
            f"basis ({args.p},2): K rows={len(basis['codomain'])}, "
            f"K cols={len(basis['kernel_domain'])}, D cols={len(basis['source'])}",
            flush=True,
        )
        d_rows = exp037.d_rows_for_basis(frozen_exp036, basis, budget)
        row = exp037.compact_basis_record(basis, d_rows)
        row["predicted_excess"] = predicted
        result["rows"].append(row)
        result["elapsed_seconds"] = round(budget.elapsed, 6)
        exp037.write_json_atomic(args.output, result)
        print(f"basis checkpoint: D rows={len(d_rows)}", flush=True)

        field_rows, profiles = exp037.peeling_field_ranks(
            frozen_exp036, basis, d_rows, fields, args.core_order, budget
        )
        row["structural_profiles"] = profiles
        for prime, field_row in field_rows.items():
            row["field_rows"][str(prime)] = field_row
            print(
                f"GF({prime}) complete: K={field_row['kernel_cokernel_dimension']}, "
                f"image={field_row['connecting_image_dimension_in_kernel_cokernel']}, "
                f"A={field_row['surviving_a_dimension']}",
                flush=True,
            )

        odd_fields = [prime for prime in fields if prime != 2]
        if 2 in fields and odd_fields:
            odd = odd_fields[0]
            actual = (
                row["field_rows"]["2"]["surviving_a_dimension"]
                - row["field_rows"][str(odd)]["surviving_a_dimension"]
            )
            row["actual_excess"] = actual
            row["candidate_matches"] = actual == predicted
            result["status"] = (
                "PASS_FINITE_OUT_OF_SAMPLE"
                if row["candidate_matches"]
                else "REFUTED_DEGREE_SIX_CORRECTION"
            )
        else:
            result["status"] = "PASS_RANKS_WITHOUT_EXCESS_COMPARISON"
        row["row_hash"] = digest(row)
    except exp037.BudgetStop as error:
        result["status"] = "INCONCLUSIVE_RESOURCE_BUDGET"
        result["stop_reason"] = str(error)
        result["private_bytes_at_stop"] = exp037.private_bytes()
        result["elapsed_seconds"] = round(budget.elapsed, 6)
        result["artifact_sha256"] = digest(result)
        exp037.write_json_atomic(args.output, result)
        print(f"INCONCLUSIVE_RESOURCE_BUDGET: {error}", flush=True)
        return 2

    result["elapsed_seconds"] = round(budget.elapsed, 6)
    result["artifact_sha256"] = digest(result)
    exp037.write_json_atomic(args.output, result)
    print(json.dumps(result, indent=2), flush=True)
    return 0 if result["status"] != "REFUTED_DEGREE_SIX_CORRECTION" else 1


if __name__ == "__main__":
    raise SystemExit(main())
