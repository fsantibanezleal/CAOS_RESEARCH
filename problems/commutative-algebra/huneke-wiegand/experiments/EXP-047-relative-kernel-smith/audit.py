"""Independent modular-minor audit of EXP-047 relative Smith forms."""

from __future__ import annotations

import hashlib
import json
import math
import random
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXP042 = HERE.parent / "EXP-042-bockstein-normal-form"
RESULTS = HERE / "artifacts" / "results.json"
OUTPUT = HERE / "artifacts" / "audit-certificate.json"
EXPECTED_RUN_SHA256 = "3b8ce822b23175bddf255fb8c0203839be888bab4b54ff9d9040bc3ba6915408"
EXPECTED_RESULTS_SHA256 = (
    "c3bc7d7ec8acb6a096fc590457853db12ca7d2d87f33917039cb091ddb1047b9"
)
EXPECTED_MATRIX_SHA256 = {
    8: "7bffc81eeb39d637660a06a68fe314a573172e7249ab286f2e3fc7bb64e08cff",
    9: "00c20e30d81861a599448535c2ecc7625b56b1951fe863e64d40ce6f56ff218c",
    10: "c7d6bbf0ec655296a0dafe81ab41ce70300c0fa4a837e5c141f55811e29f6f4d",
    11: "69e8519a3b239ec90c3b5af526f806a9a0aabf003517ea28233167d7e2b68dd9",
}
EXPECTED_RELATIVE_SHA256 = {
    (8, 56, 58): "0f92c7337037be3efaed30bcd551c80d9c63b8eb4a283a3d369e60b9fbc594b0",
    (8, 58, 59): "41f4743099ed476a07f729935ec586896efe67a1cfa8b6570ed5c267e676e79f",
    (8, 58, 62): "b9eba962c688b571e6f7ce36a9a79d42ee80e47e1572f7abf87e71dc47dd39a7",
    (9, 56, 58): "ee745dade823cfac831bb956d60a11c810024e392df8a08a8459523e513f9fc6",
    (9, 58, 59): "cd5b68c70394111f236ae57eaaa05b504f37075e0cce16e0be86f83dbb816a74",
    (9, 58, 62): "7f5ababa3becf7f7dbe4a1bf3d98afd605ff85e3c89d09052fb7881a9f4a292f",
    (10, 56, 58): "79ac4ee7f9ab0e6bdeb7e3ea922fe4c8dd627f01ce6d4f4b4b2e2c981a4f6d59",
    (10, 58, 59): "94aff85d6b9735555a4205609149750bebea387f066259e7e289cc6873d59437",
    (10, 58, 62): "fd6c2966e92adc3308e9dee5aface95270d24f9ac6817526021a1780221d45d2",
    (11, 56, 58): "3e87286d14ad6ce596ee5646cf420db8c1d4f195109d68e514f4110cdcdb7600",
    (11, 58, 59): "e4e575fedf398c5b4c596431ffeabf35952785416a437046ea110050a2e39765",
    (11, 58, 62): "79b35ce1f4f7e556a33ee295618564179ef3e11d09ec624dd6f93342114ee4e2",
}
ATOM_ALIASES = {
    "R0": '["row","D","A",[-2,-3,1,0,1,0,0,0,0,0]]',
    "R1": '["row","D","A",[-3,-2,2,0,0,0,0,0,0,0]]',
    "R2": '["row","D","B",[-1,-4,1,0,1,0,0,0,0,0]]',
    "R3": '["row","D","B",[-2,-3,2,0,0,0,0,0,0,0]]',
    "R4": '["row","K","C0",[-2,-2,1,0,0,0,0,0,0,0]]',
    "R5": '["row","K","C2",[-1,-3,1,0,0,0,0,0,0,0]]',
}
ALIASES = tuple(ATOM_ALIASES)
PRIMES = (2305843009213693951, 2305843009213693921, 2305843009213693907)


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
    if number < 2:
        return False
    for prime in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if number % prime == 0:
            return number == prime
    exponent = number - 1
    power = 0
    while exponent % 2 == 0:
        power += 1
        exponent //= 2
    for base in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if base % number == 0:
            continue
        value = pow(base, exponent, number)
        if value in (1, number - 1):
            continue
        for _ in range(power - 1):
            value = value * value % number
            if value == number - 1:
                break
        else:
            return False
    return True


def aliases(mask: int) -> list[str]:
    return [alias for bit, alias in enumerate(ALIASES) if mask & (1 << bit)]


def atom_values(matrix: dict[str, object]) -> list[str]:
    table = matrix["row_atom_table"]
    return [table[int(index)] for index in matrix["row_atom_ids"]]


def rows_for_mask(row_atoms: list[str], mask: int) -> list[int]:
    selected = {ATOM_ALIASES[alias] for alias in aliases(mask)}
    return [row for row, atom in enumerate(row_atoms) if atom in selected]


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


def modular_basis(
    columns: list[list[list[int]]],
    prime: int,
    order: list[int],
    *,
    high_pivot: bool,
) -> tuple[int, list[int], list[int]]:
    pivots: dict[int, dict[int, int]] = {}
    selected_columns: list[int] = []
    selected_rows: list[int] = []
    for column in order:
        vector = {
            int(row): int(value) % prime
            for row, value in columns[column]
            if int(value) % prime
        }
        while vector:
            pivot = max(vector) if high_pivot else min(vector)
            coefficient = vector[pivot]
            if pivot not in pivots:
                inverse = pow(coefficient, -1, prime)
                pivots[pivot] = {
                    row: value * inverse % prime for row, value in vector.items()
                }
                selected_columns.append(column)
                selected_rows.append(pivot)
                break
            basis = pivots[pivot]
            for row, value in basis.items():
                replacement = (vector.get(row, 0) - coefficient * value) % prime
                if replacement:
                    vector[row] = replacement
                else:
                    vector.pop(row, None)
    return len(pivots), selected_rows, selected_columns


def bareiss_determinant(matrix: list[list[int]]) -> int:
    size = len(matrix)
    if size == 0:
        return 1
    work = [row[:] for row in matrix]
    sign = 1
    previous = 1
    for pivot_index in range(size - 1):
        if work[pivot_index][pivot_index] == 0:
            swap = next(
                (
                    row
                    for row in range(pivot_index + 1, size)
                    if work[row][pivot_index]
                ),
                None,
            )
            if swap is None:
                return 0
            work[pivot_index], work[swap] = work[swap], work[pivot_index]
            sign *= -1
        pivot = work[pivot_index][pivot_index]
        for row in range(pivot_index + 1, size):
            for column in range(pivot_index + 1, size):
                numerator = (
                    work[row][column] * pivot
                    - work[row][pivot_index] * work[pivot_index][column]
                )
                if numerator % previous:
                    raise AssertionError("Bareiss division is not exact")
                work[row][column] = numerator // previous
            work[row][pivot_index] = 0
        previous = pivot
    return sign * work[-1][-1]


def rank_upper_certificate(
    columns: list[list[list[int]]], expected_rank: int
) -> dict[str, object]:
    norm_squares = [sum(int(value) ** 2 for _, value in entries) for entries in columns]
    bound_square = math.prod(sorted(norm_squares, reverse=True)[: expected_rank + 1])
    product = 1
    tests: list[dict[str, object]] = []
    for prime in PRIMES:
        rank, _, _ = modular_basis(
            columns, prime, list(range(len(columns))), high_pivot=False
        )
        product *= prime
        tests.append({"prime": str(prime), "rank": rank})
        if product * product > bound_square:
            break
    return {
        "prime_tests": tests,
        "prime_product": str(product),
        "prime_product_square_exceeds_hadamard_square": product * product > bound_square,
        "hadamard_bound_square": str(bound_square),
        "rank_upper": expected_rank,
        "all_modular_ranks_at_most_upper": all(
            int(test["rank"]) <= expected_rank for test in tests
        ),
    }


def determinantal_divisor_certificate(
    matrix_rows: list[list[int]],
    columns: list[list[list[int]]],
    rank: int,
    even_factors: int,
    seed: int,
) -> dict[str, object]:
    target = 1 << even_factors
    column_count = len(columns)
    base_orders = [
        list(range(column_count)),
        list(range(column_count - 1, -1, -1)),
        sorted(range(column_count), key=lambda column: (len(columns[column]), column)),
        sorted(
            range(column_count),
            key=lambda column: (-len(columns[column]), column),
        ),
    ]
    generator = random.Random(seed)
    for _ in range(24):
        order = list(range(column_count))
        generator.shuffle(order)
        base_orders.append(order)
    determinant_gcd = 0
    witnesses: list[dict[str, object]] = []
    primes = (3, 5, *PRIMES)
    for index, order in enumerate(base_orders):
        prime = primes[index % len(primes)]
        high_pivot = bool(index % 2)
        modular_rank, selected_rows, selected_columns = modular_basis(
            columns, prime, order, high_pivot=high_pivot
        )
        if modular_rank != rank:
            continue
        minor = [
            [matrix_rows[row][column] for column in selected_columns]
            for row in selected_rows
        ]
        determinant = bareiss_determinant(minor)
        if determinant == 0:
            raise AssertionError("selected modular basis has zero integer determinant")
        determinant_gcd = math.gcd(determinant_gcd, abs(determinant))
        witnesses.append(
            {
                "prime": str(prime),
                "high_pivot": high_pivot,
                "rows": selected_rows,
                "columns": selected_columns,
                "determinant": str(determinant),
            }
        )
        if determinant_gcd == target:
            break
    return {
        "target_determinantal_divisor": target,
        "sampled_minor_gcd": determinant_gcd,
        "target_reached": determinant_gcd == target,
        "witnesses": witnesses,
    }


def main() -> int:
    results = json.loads(RESULTS.read_text(encoding="utf-8"))
    without_hash = dict(results)
    internal_hash = without_hash.pop("artifact_hash")
    checks: dict[str, bool] = {
        "run_hash": sha256(HERE / "run.py") == EXPECTED_RUN_SHA256,
        "results_external_hash": sha256(RESULTS) == EXPECTED_RESULTS_SHA256,
        "results_internal_hash": digest(without_hash) == internal_hash,
        "primary_complete": results["status"] == "COMPLETE",
        "predictions_pass": all(
            results[key] == "PASS_FINITE" for key in ("p1_status", "p2_status", "p3_status")
        ),
        "prime_pool": len(set(PRIMES)) == len(PRIMES)
        and all(is_prime_64(prime) for prime in PRIMES),
    }
    audit_rows: list[dict[str, object]] = []
    for row in results["rows"]:
        p = int(row["p"])
        matrix_path = EXP042 / "artifacts" / f"matrix-p{p}.json"
        matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
        row_atoms = atom_values(matrix)
        checks[f"p{p}_matrix_hash"] = sha256(matrix_path) == EXPECTED_MATRIX_SHA256[p]
        audit_inclusions: list[dict[str, object]] = []
        for record in row["inclusions"]:
            source = int(record["source_mask"])
            target = int(record["target_mask"])
            key = (p, source, target)
            artifact_path = HERE / str(record["relative_artifact"])
            artifact = json.loads(artifact_path.read_text(encoding="utf-8"))
            artifact_without_hash = dict(artifact)
            artifact_internal_hash = artifact_without_hash.pop("artifact_hash")
            matrix_rows = artifact["matrix_rows"]
            columns = sparse_columns(matrix_rows)
            relative = record["relative"]
            rank = int(relative["rank_q"])
            expected_torsion = (
                [2] * (p - 7) if (source, target) == (56, 58) else [2, 2]
            )
            even_factors = len(expected_torsion)
            source_rows = rows_for_mask(row_atoms, source)
            source_set = set(source_rows)
            added_rows = [
                item for item in rows_for_mask(row_atoms, target) if item not in source_set
            ]
            ranks = {
                str(prime): modular_basis(
                    columns,
                    prime,
                    list(range(len(columns) - 1, -1, -1)),
                    high_pivot=False,
                )[0]
                for prime in (2, 3, 5)
            }
            upper = rank_upper_certificate(columns, rank)
            divisor = determinantal_divisor_certificate(
                matrix_rows,
                columns,
                rank,
                even_factors,
                seed=10000 * p + 100 * source + target,
            )
            prefix = f"p{p}_{source}_{target}"
            checks.update(
                {
                    f"{prefix}_artifact_hash": sha256(artifact_path)
                    == EXPECTED_RELATIVE_SHA256[key]
                    == record["relative_artifact_sha256"],
                    f"{prefix}_artifact_internal": digest(artifact_without_hash)
                    == artifact_internal_hash
                    == record["relative_artifact_internal_hash"],
                    f"{prefix}_metadata": (
                        int(artifact["p"]) == p
                        and int(artifact["source_mask"]) == source
                        and int(artifact["target_mask"]) == target
                    ),
                    f"{prefix}_source_rows": digest(source_rows)
                    == artifact["source_rows_hash"],
                    f"{prefix}_added_rows": digest(added_rows)
                    == artifact["added_rows_hash"]
                    == record["added_rows_hash"],
                    f"{prefix}_kernel_basis_hash": artifact["kernel_basis_hash"]
                    == record["source_kernel"]["kernel_basis_hash"],
                    f"{prefix}_dimensions": (
                        len(matrix_rows) == int(relative["rows"]) == len(added_rows)
                        and len(columns) == int(relative["columns"])
                    ),
                    f"{prefix}_matrix_hash": digest(matrix_rows)
                    == relative["matrix_hash"],
                    f"{prefix}_modular_ranks": ranks == relative["ranks"],
                    f"{prefix}_rank_lower": ranks["3"] == ranks["5"] == rank,
                    f"{prefix}_rank_upper": (
                        bool(upper["prime_product_square_exceeds_hadamard_square"])
                        and bool(upper["all_modular_ranks_at_most_upper"])
                    ),
                    f"{prefix}_even_factor_count": rank - ranks["2"]
                    == even_factors,
                    f"{prefix}_determinantal_divisor": bool(divisor["target_reached"]),
                    f"{prefix}_torsion": relative["torsion_invariants"]
                    == expected_torsion,
                    f"{prefix}_free_rank": int(relative["free_rank"])
                    == len(added_rows) - rank,
                    f"{prefix}_source_target_rank": (
                        bool(record["source_rank_matches_stored_odd"])
                        and bool(record["target_rank_matches_stored_odd"])
                    ),
                }
            )
            audit_inclusions.append(
                {
                    "source_mask": source,
                    "target_mask": target,
                    "relative_rank": rank,
                    "free_rank": relative["free_rank"],
                    "torsion_invariants": expected_torsion,
                    "ranks": ranks,
                    "rank_upper_certificate": upper,
                    "determinantal_divisor_certificate": divisor,
                }
            )
            print(f"audit p={p} {source}->{target}", flush=True)
        audit_rows.append({"p": p, "inclusions": audit_inclusions})

    certificate: dict[str, object] = {
        "experiment": "EXP-047",
        "status": "PASS" if all(checks.values()) else "FAIL",
        "audit_route": (
            "independent low-pivot modular ranks, exact Hadamard rank ceilings, and "
            "Bareiss minor-gcd determinantal divisors"
        ),
        "artifact_hashes": {
            "run": EXPECTED_RUN_SHA256,
            "results": EXPECTED_RESULTS_SHA256,
            "relative": {
                f"p{p}_{source}_{target}": value
                for (p, source, target), value in EXPECTED_RELATIVE_SHA256.items()
            },
        },
        "checks": checks,
        "rows": audit_rows,
        "result": {
            "stable_completion_torsion": [2, 2],
            "threshold_torsion_rank": "p-7",
            "higher_two_power_or_odd_torsion": False,
        },
        "scope": (
            "finite exact relative modules for p=8,...,11; transformed-HNF kernel "
            "saturation remains in the primary engine trust boundary"
        ),
    }
    certificate["certificate_hash"] = digest(certificate)
    write_json_atomic(OUTPUT, certificate)
    print(json.dumps({"status": certificate["status"], "checks": len(checks)}, indent=2))
    return 0 if certificate["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
