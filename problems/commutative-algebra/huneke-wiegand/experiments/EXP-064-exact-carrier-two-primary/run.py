"""Exact rational-rank and 2-primary certificates for four carrier masks."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import time
from pathlib import Path
from types import ModuleType


HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
EXP042 = EXPERIMENTS / "EXP-042-bockstein-normal-form"
EXP043 = EXPERIMENTS / "EXP-043-hadamard-rank-certificate"
EXP045 = EXPERIMENTS / "EXP-045-row-atom-carrier-lattice"
EXP062 = EXPERIMENTS / "EXP-062-triangle-torsion-family"
EXP063 = EXPERIMENTS / "EXP-063-triangle-isolated-comparison"
DEFAULT_OUTPUT = HERE / "artifacts" / "results.json"
DEFAULT_CHECKPOINT = HERE / "artifacts" / "checkpoint.json"
MASKS = (56, 58, 59, 62)
EXPECTED_RANKS = {
    8: {56: 963, 58: 980, 59: 993, 62: 1002},
    9: {56: 1561, 58: 1581, 59: 1596, 62: 1607},
    10: {56: 2397, 58: 2420, 59: 2437, 62: 2450},
    11: {56: 3526, 58: 3552, 59: 3571, 62: 3586},
}
EXPECTED_BETA = {
    8: {56: 0, 58: 1, 59: 3, 62: 3},
    9: {56: 0, 58: 2, 59: 4, 62: 4},
    10: {56: 0, 58: 3, 59: 5, 62: 5},
    11: {56: 1, 58: 5, 59: 7, 62: 7},
}
PREMISES = {
    HERE / "hypothesis.md": "cd246184ae3075fb0bc6fad12d26959728bcac23d350888f02c5c507c0a6cf97",
    EXP043 / "run.py": "1f4c5c25e5238322dc458e0232c0a80f72ee1b62544bbcbda8a773af24403418",
    EXP045 / "run.py": "2ae864d472e470869673eb1cd2ffd25ef6d0e2da6530cd6c675d335f860e2109",
    EXP045 / "artifacts" / "results.json":
        "569220667e9d82f0806ea96cb8f60c49e94cb6317817170c39f2e574e619bcb8",
    EXP062 / "artifacts" / "results.json":
        "09aef05e577e58b11c4ccc363ed47ccf1ed1598deb1b156a33bb3b6e49ae638d",
    EXP063 / "run.py": "97a9e7511ff9d004b091f244df653f02182e1d9304c9042fefe47ce241a89461",
    EXP063 / "artifacts" / "results.json":
        "c219ce4c4549d970063a787227793bb5f7141e8f4d6e14c614f62085ecc8059a",
    EXP063 / "artifacts" / "audit-results.json":
        "e3560323a54ace1c7ef8aa31919535e0856098216784a004ce11f7413a83c675",
}
MATRIX_SHA256 = {
    8: "7bffc81eeb39d637660a06a68fe314a573172e7249ab286f2e3fc7bb64e08cff",
    9: "00c20e30d81861a599448535c2ecc7625b56b1951fe863e64d40ce6f56ff218c",
    10: "c7d6bbf0ec655296a0dafe81ab41ce70300c0fa4a837e5c141f55811e29f6f4d",
    11: "69e8519a3b239ec90c3b5af526f806a9a0aabf003517ea28233167d7e2b68dd9",
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


def verify_premises(p_min: int, p_max: int) -> dict[str, str]:
    actual = {str(path.relative_to(EXPERIMENTS)): sha256(path) for path in PREMISES}
    expected = {
        str(path.relative_to(EXPERIMENTS)): expected_hash
        for path, expected_hash in PREMISES.items()
    }
    if actual != expected:
        raise AssertionError({"premise_hash_mismatch": {"actual": actual, "expected": expected}})
    for p in range(p_min, p_max + 1):
        matrix = EXP042 / "artifacts" / f"matrix-p{p}.json"
        if sha256(matrix) != MATRIX_SHA256[p]:
            raise AssertionError({"p": p, "matrix_hash_mismatch": sha256(matrix)})
    return actual


def frozen_subsets() -> dict[tuple[int, int], dict[str, object]]:
    payload = json.loads((EXP045 / "artifacts" / "results.json").read_text(encoding="utf-8"))
    return {
        (int(row["p"]), int(subset["mask"])): subset
        for row in payload["rows"]
        for subset in row["subsets"]
        if int(subset["mask"]) in MASKS
    }


def exp063_rows() -> dict[int, dict[str, object]]:
    payload = json.loads((EXP063 / "artifacts" / "results.json").read_text(encoding="utf-8"))
    unsigned = dict(payload)
    artifact_hash = unsigned.pop("artifact_hash")
    if digest(unsigned) != artifact_hash or payload["claims"] != {"P1": True, "P2": True, "P3": True}:
        raise AssertionError("EXP-063 artifact integrity or claims failed")
    return {int(row["p"]): row for row in payload["rows"]}


def certify_projection(
    *, p: int, mask: int, matrix: dict[str, object], frozen: dict[str, object],
    exp043: ModuleType, exp045: ModuleType, primes: list[int], budget: object,
) -> dict[str, object]:
    kept_rows, atoms, columns = exp045.project_matrix(matrix, mask)
    projection_hash = digest(
        {"kept_rows": kept_rows, "row_atoms": atoms, "signed_columns": columns}
    )
    if projection_hash != frozen["projection_hash"]:
        raise AssertionError({"p": p, "mask": mask, "projection_hash": False})
    target_rank = EXPECTED_RANKS[p][mask]
    rank_two = int(frozen["ranks"]["2"])
    rank_three = int(frozen["ranks"]["3"])
    rank_five = int(frozen["ranks"]["5"])
    bockstein = int(frozen["bockstein_high_forward"]["bockstein_rank"])
    if rank_three != target_rank or rank_five != target_rank:
        raise AssertionError({"p": p, "mask": mask, "frozen_odd_rank": False})
    if bockstein != EXPECTED_BETA[p][mask] or frozen["bockstein_high_forward"] != frozen["bockstein_low_reverse"]:
        raise AssertionError({"p": p, "mask": mask, "frozen_bockstein": False})

    maximum_squared_column_norm = max(map(len, columns))
    product = 1
    prime_tests: list[dict[str, object]] = []
    for index, prime in enumerate(primes, start=1):
        rank = exp043.modular_rank(
            columns, prime, high_pivot=True, budget=budget,
            stage=f"p={p} mask={mask} prime={index}",
        )
        prime_tests.append({"prime": str(prime), "rank": rank})
        if rank != target_rank:
            raise AssertionError({"p": p, "mask": mask, "prime": str(prime), "rank": rank})
        product *= prime
        if index % 20 == 0:
            print(
                f"p={p} mask={mask}: primes={index}, product_bits={product.bit_length()}",
                flush=True,
            )
        if exp043.hadamard_covered(product, maximum_squared_column_norm, target_rank):
            break
        budget.check(f"p={p} mask={mask} certificate")
    coverage = exp043.hadamard_covered(product, maximum_squared_column_norm, target_rank)
    if not coverage:
        raise exp043.BudgetStop(f"prime pool exhausted at p={p}, mask={mask}")
    rank_gap = target_rank - rank_two
    complete_elementary = rank_gap == bockstein == EXPECTED_BETA[p][mask]
    if not complete_elementary:
        raise AssertionError({"p": p, "mask": mask, "rank_gap": rank_gap, "bockstein": bockstein})
    return {
        "mask": mask,
        "rows": len(kept_rows),
        "columns": len(columns),
        "nonzero_columns": sum(bool(entries) for entries in columns),
        "nonzeros": sum(map(len, columns)),
        "projection_hash": projection_hash,
        "target_rational_rank": target_rank,
        "rank_mod_two": rank_two,
        "first_bockstein_rank": bockstein,
        "rank_gap": rank_gap,
        "maximum_squared_column_norm": maximum_squared_column_norm,
        "prime_tests": prime_tests,
        "prime_count": len(prime_tests),
        "prime_product_hex": hex(product),
        "prime_product_bits": product.bit_length(),
        "exact_squared_hadamard_coverage": True,
        "rational_rank_certified": True,
        "complete_two_primary_type": f"(Z/2)^{bockstein}",
    }


def triangle_consequence(
    *, p: int, certificate: dict[str, object], comparison: dict[str, object]
) -> dict[str, object]:
    mask = int(certificate["mask"])
    comparison_mask = next(item for item in comparison["masks"] if int(item["mask"]) == mask)
    beta = int(certificate["first_bockstein_rank"])
    if int(comparison_mask["triangle_span_rank"]) != beta:
        raise AssertionError({"p": p, "mask": mask, "triangle_span_not_complete": True})
    relations = comparison_mask["relations"]
    if any(len(item["triangles"]) != 1 for item in relations):
        raise AssertionError({"p": p, "mask": mask, "nonsingleton_zero_relation": True})
    zero_triangles = [item["triangles"][0] for item in relations]
    all_triangles = comparison["triangles"]
    zero_keys = {tuple(item) for item in zero_triangles}
    generators = [item for item in all_triangles if tuple(item) not in zero_keys]
    if len(generators) != beta:
        raise AssertionError({"p": p, "mask": mask, "generator_count": len(generators)})
    if mask == 58 and zero_triangles != [[0, 1, p - 3], [0, 2, p - 4]]:
        raise AssertionError({"p": p, "mask": mask, "endpoint_zero_set": zero_triangles})
    return {
        "mask": mask,
        "reason": "elementary 2-primary torsion injects into cokernel modulo two",
        "integrally_zero_triangles": zero_triangles,
        "complete_two_primary_generators": generators,
        "generator_count": len(generators),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p-min", type=int, default=8)
    parser.add_argument("--p-max", type=int, default=11)
    parser.add_argument("--budget-seconds", type=float, default=1200.0)
    parser.add_argument("--memory-gib", type=float, default=12.0)
    parser.add_argument("--prime-pool", type=int, default=160)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
    args = parser.parse_args()
    if not (8 <= args.p_min <= args.p_max <= 11):
        raise ValueError("EXP-064 is frozen to 8 <= p_min <= p_max <= 11")

    started = time.monotonic()
    premise_hashes = verify_premises(args.p_min, args.p_max)
    exp043 = load_module("exp043_for_064", EXP043 / "run.py")
    exp045 = load_module("exp045_for_064", EXP045 / "run.py")
    budget = exp043.Budget(args.budget_seconds, args.memory_gib)
    primes = exp043.descending_primes(args.prime_pool)
    if len(primes) != len(set(primes)) or not all(exp043.is_prime_64(prime) for prime in primes):
        raise AssertionError("prime pool verification failed")
    subsets = frozen_subsets()
    comparison_rows = exp063_rows()
    rows: list[dict[str, object]] = []
    for p in range(args.p_min, args.p_max + 1):
        matrix_path = EXP042 / "artifacts" / f"matrix-p{p}.json"
        matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
        certificates = []
        for mask in MASKS:
            print(f"certify p={p} mask={mask}", flush=True)
            certificates.append(
                certify_projection(
                    p=p, mask=mask, matrix=matrix, frozen=subsets[p, mask],
                    exp043=exp043, exp045=exp045, primes=primes, budget=budget,
                )
            )
        consequences = [
            triangle_consequence(p=p, certificate=item, comparison=comparison_rows[p])
            for item in certificates
        ]
        rows.append(
            {
                "p": p,
                "source_matrix_sha256": sha256(matrix_path),
                "certificates": certificates,
                "triangle_consequences": consequences,
            }
        )
        write_json_atomic(
            args.checkpoint,
            {
                "experiment": "EXP-064",
                "status": "PARTIAL",
                "scope": {"p_min": args.p_min, "p_max": args.p_max},
                "completed": [row["p"] for row in rows],
                "rows": rows,
                "elapsed_seconds": time.monotonic() - started,
            },
        )
        budget.check(f"p={p} checkpoint")

    result = {
        "experiment": "EXP-064",
        "status": "COMPLETE",
        "scope": {"p_min": args.p_min, "p_max": args.p_max},
        "premise_hashes": premise_hashes,
        "resource_caps": {
            "budget_seconds": args.budget_seconds,
            "memory_gib": args.memory_gib,
            "prime_pool": args.prime_pool,
            "processes": 1,
        },
        "claims": {"P1": True, "P2": True, "P3": True},
        "rows": rows,
        "elapsed_seconds": time.monotonic() - started,
    }
    result["artifact_hash"] = digest(result)
    write_json_atomic(args.output, result)
    print(
        json.dumps(
            {
                "status": result["status"],
                "claims": result["claims"],
                "elapsed_seconds": result["elapsed_seconds"],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
