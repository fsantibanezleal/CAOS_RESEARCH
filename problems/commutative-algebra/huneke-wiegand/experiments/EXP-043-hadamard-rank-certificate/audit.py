"""Independent opposite-pivot audit of EXP-043 rational-rank certificates."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXP042 = HERE.parent / "EXP-042-bockstein-normal-form"
RESULTS = HERE / "artifacts" / "results.json"
OUTPUT = HERE / "artifacts" / "audit-certificate.json"
EXPECTED_RESULTS_SHA256 = "612d481eff7e00f5c5128d450a5eb05f79aacccb27bcd88c106dc0d5bf7426e6"
EXPECTED_MATRIX_SHA256 = {
    8: "7bffc81eeb39d637660a06a68fe314a573172e7249ab286f2e3fc7bb64e08cff",
    9: "00c20e30d81861a599448535c2ecc7625b56b1951fe863e64d40ce6f56ff218c",
    10: "c7d6bbf0ec655296a0dafe81ab41ce70300c0fa4a837e5c141f55811e29f6f4d",
    11: "69e8519a3b239ec90c3b5af526f806a9a0aabf003517ea28233167d7e2b68dd9",
}
EXPECTED_RANKS = {8: 1002, 9: 1607, 10: 2450, 11: 3586}
EXPECTED_PRIME_COUNTS = {8: 31, 9: 52, 10: 83, 11: 125}
EXPECTED_TWO_PRIMARY_RANKS = {8: 3, 9: 4, 10: 5, 11: 7}
MILLER_RABIN_BASES_64 = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def write_json_atomic(path: Path, value: object) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def is_prime_64(number: int) -> bool:
    if not 2 <= number < 1 << 64:
        return False
    for prime in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if number % prime == 0:
            return number == prime
    odd_part = number - 1
    power = 0
    while not odd_part & 1:
        odd_part >>= 1
        power += 1
    for base in MILLER_RABIN_BASES_64:
        value = pow(base % number, odd_part, number)
        if value in (1, number - 1):
            continue
        for _ in range(power - 1):
            value = pow(value, 2, number)
            if value == number - 1:
                break
        else:
            return False
    return True


def modular_rank_low_pivot(columns: list[list[list[int]]], prime: int) -> int:
    pivots: dict[int, dict[int, int]] = {}
    for entries in columns:
        vector = {int(row): int(value) % prime for row, value in entries if int(value) % prime}
        while vector:
            pivot = min(vector)
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


def covered(product: int, maximum_column_degree: int, rank: int) -> bool:
    return product * product > 4 * maximum_column_degree ** (rank + 1)


def main() -> int:
    results = json.loads(RESULTS.read_text(encoding="utf-8"))
    without_hash = dict(results)
    internal_hash = without_hash.pop("artifact_hash")
    rows = {int(row["p"]): row for row in results["rows"]}
    checks: dict[str, bool] = {
        "results_external_hash": sha256(RESULTS) == EXPECTED_RESULTS_SHA256,
        "results_internal_hash": digest(without_hash) == internal_hash,
        "parameter_coverage": set(rows) == set(EXPECTED_RANKS),
        "primary_complete": results["status"] == "COMPLETE",
        "primary_predictions_pass": all(
            results[key] == "PASS_FINITE" for key in ("p1_status", "p2_status", "p3_status")
        ),
    }
    audit_rows: list[dict[str, object]] = []
    for p in sorted(EXPECTED_RANKS):
        row = rows[p]
        matrix_path = EXP042 / "artifacts" / f"matrix-p{p}.json"
        matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
        columns = matrix["signed_columns"]
        target_rank = EXPECTED_RANKS[p]
        primes = [int(test["prime"]) for test in row["prime_tests"]]
        stored_ranks = [int(test["rank"]) for test in row["prime_tests"]]
        product = 1
        opposite_ranks: list[int] = []
        for index, prime in enumerate(primes, start=1):
            product *= prime
            rank = modular_rank_low_pivot(columns, prime)
            opposite_ranks.append(rank)
            if index % 10 == 0:
                print(f"audit p={p}: {index}/{len(primes)} primes", flush=True)
        maximum_column_degree = max(map(len, columns))
        prior_product = product // primes[-1]
        rank_three = modular_rank_low_pivot(columns, 3)
        bockstein_rank = int(matrix["bockstein"]["forward"]["bockstein_rank"])
        checks.update(
            {
                f"p{p}_matrix_hash": sha256(matrix_path) == EXPECTED_MATRIX_SHA256[p],
                f"p{p}_matrix_pointer": row["matrix_artifact_sha256"] == sha256(matrix_path),
                f"p{p}_prime_count": len(primes) == EXPECTED_PRIME_COUNTS[p],
                f"p{p}_primes_distinct": len(primes) == len(set(primes)),
                f"p{p}_primes_verified": all(is_prime_64(prime) for prime in primes),
                f"p{p}_stored_ranks": all(rank == target_rank for rank in stored_ranks),
                f"p{p}_opposite_pivot_ranks": all(
                    rank == target_rank for rank in opposite_ranks
                ),
                f"p{p}_prime_product": int(row["prime_product_hex"], 16) == product,
                f"p{p}_maximum_column_degree": (
                    int(row["maximum_column_degree"]) == maximum_column_degree
                ),
                f"p{p}_exact_coverage": covered(product, maximum_column_degree, target_rank),
                f"p{p}_minimal_prefix": not covered(
                    prior_product, maximum_column_degree, target_rank
                ),
                f"p{p}_rational_lower_bound": rank_three == target_rank,
                f"p{p}_rational_rank_conclusion": bool(row["rational_rank_certified"]),
                f"p{p}_bockstein_closes_even_factors": (
                    target_rank - int(matrix["ranks"]["2"])
                    == bockstein_rank
                    == EXPECTED_TWO_PRIMARY_RANKS[p]
                ),
                f"p{p}_complete_two_primary_type": (
                    row["complete_two_primary_torsion"]
                    and row["two_primary_type"]
                    == f"(Z/2)^{EXPECTED_TWO_PRIMARY_RANKS[p]}"
                ),
            }
        )
        audit_rows.append(
            {
                "p": p,
                "rank_over_q": target_rank,
                "rank_mod_two": int(matrix["ranks"]["2"]),
                "first_bockstein_rank": bockstein_rank,
                "prime_count": len(primes),
                "prime_product_bits": product.bit_length(),
                "maximum_column_degree": maximum_column_degree,
                "minor_order": target_rank + 1,
                "two_primary_type": row["two_primary_type"],
                "opposite_rank_digest": digest(opposite_ranks),
            }
        )

    certificate: dict[str, object] = {
        "experiment": "EXP-043",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "artifact_hashes": {
            "results": EXPECTED_RESULTS_SHA256,
            "matrices": {str(p): value for p, value in EXPECTED_MATRIX_SHA256.items()},
        },
        "checks": checks,
        "rows": audit_rows,
        "result": {
            "p1_status": results["p1_status"],
            "p2_status": results["p2_status"],
            "p3_status": results["p3_status"],
            "rational_ranks": {str(row["p"]): row["rank_over_q"] for row in audit_rows},
            "complete_two_primary_types": {
                str(row["p"]): row["two_primary_type"] for row in audit_rows
            },
        },
        "scope": (
            "exact rational ranks and complete finite 2-primary torsion for the isolated "
            "p=8,...,11 matrices; no recurrence or all-parameter theorem is claimed"
        ),
    }
    certificate["certificate_hash"] = digest(certificate)
    write_json_atomic(OUTPUT, certificate)
    print(json.dumps(certificate, indent=2))
    return 0 if certificate["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
