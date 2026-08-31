"""EXP-043 exact rational-rank certificates from modular ranks and Hadamard bounds."""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import json
import os
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXP042 = HERE.parent / "EXP-042-bockstein-normal-form"
DEFAULT_OUTPUT = HERE / "artifacts" / "results.json"
PREMISES = {
    "EXP-042 results": (
        EXP042 / "artifacts" / "results.json",
        "3c4ae292fb17a5daf473aee0ed37e473000de686607b5da0a0f4c357a8216ee2",
    ),
    "EXP-042 audit": (
        EXP042 / "artifacts" / "audit-certificate.json",
        "e35f38a86c4d6ab807d32cb3e8cd99b348e310df1d1a6840818a9ab84157cb8a",
    ),
    "EXP-042 p8": (
        EXP042 / "artifacts" / "matrix-p8.json",
        "7bffc81eeb39d637660a06a68fe314a573172e7249ab286f2e3fc7bb64e08cff",
    ),
    "EXP-042 p9": (
        EXP042 / "artifacts" / "matrix-p9.json",
        "00c20e30d81861a599448535c2ecc7625b56b1951fe863e64d40ce6f56ff218c",
    ),
    "EXP-042 p10": (
        EXP042 / "artifacts" / "matrix-p10.json",
        "c7d6bbf0ec655296a0dafe81ab41ce70300c0fa4a837e5c141f55811e29f6f4d",
    ),
    "EXP-042 p11": (
        EXP042 / "artifacts" / "matrix-p11.json",
        "69e8519a3b239ec90c3b5af526f806a9a0aabf003517ea28233167d7e2b68dd9",
    ),
}
EXPECTED_RANKS = {8: 1002, 9: 1607, 10: 2450, 11: 3586}
EXPECTED_TWO_PRIMARY_RANKS = {8: 3, 9: 4, 10: 5, 11: 7}
MILLER_RABIN_BASES_64 = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)


class BudgetStop(RuntimeError):
    pass


class Budget:
    def __init__(self, seconds: float, memory_gib: float) -> None:
        self.started = time.perf_counter()
        self.seconds = seconds
        self.memory_bytes = int(memory_gib * 1024**3)

    @property
    def elapsed(self) -> float:
        return time.perf_counter() - self.started

    def check(self, stage: str) -> None:
        if self.elapsed > self.seconds:
            raise BudgetStop(f"time budget crossed during {stage}")
        private = private_bytes()
        if private is not None and private > self.memory_bytes:
            raise BudgetStop(f"memory budget crossed during {stage}: {private} bytes")


def private_bytes() -> int | None:
    if os.name != "nt":
        return None

    class ProcessMemoryCountersEx(ctypes.Structure):
        _fields_ = [
            ("cb", ctypes.c_ulong),
            ("PageFaultCount", ctypes.c_ulong),
            ("PeakWorkingSetSize", ctypes.c_size_t),
            ("WorkingSetSize", ctypes.c_size_t),
            ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
            ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
            ("PagefileUsage", ctypes.c_size_t),
            ("PeakPagefileUsage", ctypes.c_size_t),
            ("PrivateUsage", ctypes.c_size_t),
        ]

    counters = ProcessMemoryCountersEx()
    counters.cb = ctypes.sizeof(counters)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    get_process = kernel32.GetCurrentProcess
    get_process.restype = ctypes.c_void_p
    memory_info = kernel32.K32GetProcessMemoryInfo
    memory_info.argtypes = [
        ctypes.c_void_p,
        ctypes.POINTER(ProcessMemoryCountersEx),
        ctypes.c_ulong,
    ]
    if not memory_info(get_process(), ctypes.byref(counters), counters.cb):
        return None
    return int(counters.PrivateUsage)


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


def is_prime_64(number: int) -> bool:
    if number < 2:
        return False
    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for prime in small_primes:
        if number % prime == 0:
            return number == prime
    odd_part = number - 1
    power = 0
    while odd_part % 2 == 0:
        odd_part //= 2
        power += 1
    for base in MILLER_RABIN_BASES_64:
        if base % number == 0:
            continue
        value = pow(base, odd_part, number)
        if value in (1, number - 1):
            continue
        for _ in range(power - 1):
            value = value * value % number
            if value == number - 1:
                break
        else:
            return False
    return True


def descending_primes(count: int) -> list[int]:
    candidate = (1 << 61) - 1
    primes: list[int] = []
    while len(primes) < count:
        if is_prime_64(candidate):
            primes.append(candidate)
        candidate -= 2
    return primes


def modular_rank(
    columns: list[list[list[int]]], prime: int, *, high_pivot: bool, budget: Budget, stage: str
) -> int:
    pivots: dict[int, dict[int, int]] = {}
    for column_index, entries in enumerate(columns):
        vector = {int(row): int(value) % prime for row, value in entries if int(value) % prime}
        while vector:
            pivot = max(vector) if high_pivot else min(vector)
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
        if column_index and column_index % 500 == 0:
            budget.check(stage)
    return len(pivots)


def hadamard_covered(product: int, maximum_column_degree: int, rank: int) -> bool:
    return product * product > 4 * maximum_column_degree ** (rank + 1)


def certify_parameter(
    *, p: int, matrix: dict[str, object], primes: list[int], budget: Budget
) -> dict[str, object]:
    columns = matrix["signed_columns"]
    target_rank = EXPECTED_RANKS[p]
    maximum_column_degree = max(map(len, columns))
    product = 1
    tests: list[dict[str, object]] = []
    for index, prime in enumerate(primes, start=1):
        rank = modular_rank(
            columns,
            prime,
            high_pivot=True,
            budget=budget,
            stage=f"p={p} prime {index}",
        )
        tests.append({"prime": str(prime), "rank": rank})
        if rank > target_rank:
            break
        product *= prime
        if index % 10 == 0:
            print(
                f"p={p}: {index} primes, rank={rank}, product_bits={product.bit_length()}",
                flush=True,
            )
        if hadamard_covered(product, maximum_column_degree, target_rank):
            break
        budget.check(f"p={p} certificate")

    all_ranks_match = all(int(test["rank"]) == target_rank for test in tests)
    coverage = hadamard_covered(product, maximum_column_degree, target_rank)
    rational_rank_certified = all_ranks_match and coverage
    bockstein_rank = int(matrix["bockstein"]["forward"]["bockstein_rank"])
    two_primary_complete = (
        rational_rank_certified
        and target_rank - int(matrix["ranks"]["2"]) == bockstein_rank
        and bockstein_rank == EXPECTED_TWO_PRIMARY_RANKS[p]
    )
    return {
        "p": p,
        "matrix_artifact_sha256": sha256(EXP042 / "artifacts" / f"matrix-p{p}.json"),
        "rows": int(matrix["rows"]),
        "columns": int(matrix["columns"]),
        "nonzeros": int(matrix["nonzeros"]),
        "target_rank": target_rank,
        "maximum_column_degree": maximum_column_degree,
        "minor_order": target_rank + 1,
        "prime_tests": tests,
        "prime_count": len(tests),
        "prime_product_hex": hex(product),
        "prime_product_bits": product.bit_length(),
        "exact_squared_hadamard_coverage": coverage,
        "all_modular_ranks_match": all_ranks_match,
        "rational_rank_certified": rational_rank_certified,
        "rank_mod_two": int(matrix["ranks"]["2"]),
        "first_bockstein_rank": bockstein_rank,
        "complete_two_primary_torsion": two_primary_complete,
        "two_primary_type": f"(Z/2)^{bockstein_rank}" if two_primary_complete else None,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p-min", type=int, default=8)
    parser.add_argument("--p-max", type=int, default=11)
    parser.add_argument("--budget-seconds", type=float, default=1200.0)
    parser.add_argument("--memory-gib", type=float, default=12.0)
    parser.add_argument("--prime-pool", type=int, default=160)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if args.p_min < 8 or args.p_max > 11 or args.p_min > args.p_max:
        raise ValueError("declared range is 8<=p_min<=p_max<=11")

    premise_hashes = verify_premises()
    budget = Budget(args.budget_seconds, args.memory_gib)
    primes = descending_primes(args.prime_pool)
    if len(primes) != len(set(primes)) or not all(is_prime_64(prime) for prime in primes):
        raise AssertionError("prime pool verification failed")
    result: dict[str, object] = {
        "experiment": "EXP-043",
        "route": "distinct-prime modular ranks plus exact Hadamard minor bound",
        "status": "RUNNING",
        "parameters": {
            "p_min": args.p_min,
            "p_max": args.p_max,
            "budget_seconds": args.budget_seconds,
            "memory_gib": args.memory_gib,
            "prime_pool": args.prime_pool,
            "prime_bits": 61,
        },
        "premise_hashes": premise_hashes,
        "rows": [],
    }
    write_json_atomic(args.output, result)
    try:
        for p in range(args.p_min, args.p_max + 1):
            matrix_path = EXP042 / "artifacts" / f"matrix-p{p}.json"
            matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
            print(f"certifying rational rank for p={p}", flush=True)
            row = certify_parameter(p=p, matrix=matrix, primes=primes, budget=budget)
            result["rows"].append(row)
            result["status"] = "CHECKPOINT"
            result["elapsed_seconds"] = budget.elapsed
            write_json_atomic(args.output, result)
            if not row["all_modular_ranks_match"]:
                break
            if not row["exact_squared_hadamard_coverage"]:
                raise BudgetStop(f"prime pool exhausted before p={p} Hadamard coverage")
    except BudgetStop as error:
        result["status"] = "INCONCLUSIVE_RESOURCE_BUDGET"
        result["resource_stop"] = str(error)
        result["elapsed_seconds"] = budget.elapsed
        result["artifact_hash"] = digest(result)
        write_json_atomic(args.output, result)
        print(json.dumps({"status": result["status"], "error": str(error)}, indent=2))
        return 2

    full_range = {int(row["p"]) for row in result["rows"]} == {8, 9, 10, 11}
    result["p1_status"] = (
        "PASS_FINITE"
        if full_range and all(row["all_modular_ranks_match"] for row in result["rows"])
        else "REFUTED" if any(not row["all_modular_ranks_match"] for row in result["rows"])
        else "NOT_EVALUATED"
    )
    result["p2_status"] = (
        "PASS_FINITE"
        if full_range and all(row["rational_rank_certified"] for row in result["rows"])
        else "NOT_EVALUATED"
    )
    result["p3_status"] = (
        "PASS_FINITE"
        if full_range and all(row["complete_two_primary_torsion"] for row in result["rows"])
        else "NOT_EVALUATED"
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
                "rational_ranks": {
                    str(row["p"]): row["target_rank"] for row in result["rows"]
                },
                "prime_counts": {
                    str(row["p"]): row["prime_count"] for row in result["rows"]
                },
                "two_primary_types": {
                    str(row["p"]): row["two_primary_type"] for row in result["rows"]
                },
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
