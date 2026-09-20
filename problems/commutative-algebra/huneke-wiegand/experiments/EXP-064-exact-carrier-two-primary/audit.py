"""Independent low-pivot audit of EXP-064 carrier certificates."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
EXP042 = EXPERIMENTS / "EXP-042-bockstein-normal-form"
EXP045 = EXPERIMENTS / "EXP-045-row-atom-carrier-lattice"
EXP063 = EXPERIMENTS / "EXP-063-triangle-isolated-comparison"
RESULTS = HERE / "artifacts" / "results.json"
DEFAULT_OUTPUT = HERE / "artifacts" / "audit-results.json"
MASKS = (56, 58, 59, 62)
ALIASES = ("R0", "R1", "R2", "R3", "R4", "R5")
ATOM_ALIASES = {
    "R0": '["row","D","A",[-2,-3,1,0,1,0,0,0,0,0]]',
    "R1": '["row","D","A",[-3,-2,2,0,0,0,0,0,0,0]]',
    "R2": '["row","D","B",[-1,-4,1,0,1,0,0,0,0,0]]',
    "R3": '["row","D","B",[-2,-3,2,0,0,0,0,0,0,0]]',
    "R4": '["row","K","C0",[-2,-2,1,0,0,0,0,0,0,0]]',
    "R5": '["row","K","C2",[-1,-3,1,0,0,0,0,0,0,0]]',
}
PINS = {
    HERE / "hypothesis.md": "cd246184ae3075fb0bc6fad12d26959728bcac23d350888f02c5c507c0a6cf97",
    HERE / "run.py": "833ef690eecabbd8c065b4b0d1b340256957133b60675e6c0bb2ebdaf5576586",
    RESULTS: "9304c81487b29688c9fcf3524998db15f6faf7b50a9448cff197b6177bc4f5c4",
    EXP045 / "artifacts" / "results.json":
        "569220667e9d82f0806ea96cb8f60c49e94cb6317817170c39f2e574e619bcb8",
    EXP063 / "artifacts" / "results.json":
        "c219ce4c4549d970063a787227793bb5f7141e8f4d6e14c614f62085ecc8059a",
}
MATRIX_SHA256 = {
    8: "7bffc81eeb39d637660a06a68fe314a573172e7249ab286f2e3fc7bb64e08cff",
    9: "00c20e30d81861a599448535c2ecc7625b56b1951fe863e64d40ce6f56ff218c",
    10: "c7d6bbf0ec655296a0dafe81ab41ce70300c0fa4a837e5c141f55811e29f6f4d",
    11: "69e8519a3b239ec90c3b5af526f806a9a0aabf003517ea28233167d7e2b68dd9",
}
MILLER_RABIN_BASES = (2, 325, 9375, 28178, 450775, 9780504, 1795265022)


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


def is_prime(number: int) -> bool:
    if number < 2:
        return False
    for prime in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if number % prime == 0:
            return number == prime
    odd = number - 1
    power = 0
    while odd % 2 == 0:
        odd //= 2
        power += 1
    for base in MILLER_RABIN_BASES:
        if base % number == 0:
            continue
        value = pow(base, odd, number)
        if value in (1, number - 1):
            continue
        for _ in range(power - 1):
            value = value * value % number
            if value == number - 1:
                break
        else:
            return False
    return True


class Budget:
    def __init__(self, seconds: float) -> None:
        self.started = time.monotonic()
        self.seconds = seconds

    def check(self, stage: str) -> None:
        if time.monotonic() - self.started > self.seconds:
            raise RuntimeError(f"audit budget exceeded during {stage}")


def project(matrix: dict[str, object], mask: int) -> tuple[list[int], list[str], list[list[list[int]]]]:
    selected_aliases = [alias for bit, alias in enumerate(ALIASES) if mask & (1 << bit)]
    selected_atoms = {ATOM_ALIASES[alias] for alias in selected_aliases}
    atoms = [matrix["row_atom_table"][int(index)] for index in matrix["row_atom_ids"]]
    kept = [index for index, atom in enumerate(atoms) if atom in selected_atoms]
    positions = {original: new for new, original in enumerate(kept)}
    columns = [
        [[positions[int(row)], int(value)] for row, value in entries if int(row) in positions]
        for entries in matrix["signed_columns"]
    ]
    return kept, [atoms[row] for row in kept], columns


def modular_rank_low(
    columns: list[list[list[int]]], prime: int, budget: Budget, stage: str
) -> int:
    pivots: dict[int, dict[int, int]] = {}
    for index, entries in enumerate(reversed(columns)):
        vector = {int(row): int(value) % prime for row, value in entries if int(value) % prime}
        while vector:
            pivot = min(vector)
            coefficient = vector[pivot]
            if pivot not in pivots:
                inverse = pow(coefficient, -1, prime)
                pivots[pivot] = {row: value * inverse % prime for row, value in vector.items()}
                break
            basis = pivots[pivot]
            for row, value in basis.items():
                replacement = (vector.get(row, 0) - coefficient * value) % prime
                if replacement:
                    vector[row] = replacement
                else:
                    vector.pop(row, None)
        if index and index % 500 == 0:
            budget.check(stage)
    return len(pivots)


def covered(product: int, squared_norm: int, rank: int) -> bool:
    return product * product > 4 * squared_norm ** (rank + 1)


def diagonal_first_bockstein(entry: int) -> int:
    if entry % 2:
        return 0
    return (entry // 2) % 2


def audit_certificate(
    *, p: int, saved: dict[str, object], matrix: dict[str, object], budget: Budget
) -> dict[str, object]:
    mask = int(saved["mask"])
    kept, atoms, columns = project(matrix, mask)
    projection_hash = digest(
        {"kept_rows": kept, "row_atoms": atoms, "signed_columns": columns}
    )
    if projection_hash != saved["projection_hash"]:
        raise AssertionError({"p": p, "mask": mask, "projection_hash": False})
    primes = [int(test["prime"]) for test in saved["prime_tests"]]
    if len(primes) != len(set(primes)) or not all(is_prime(prime) for prime in primes):
        raise AssertionError({"p": p, "mask": mask, "primes": False})
    target = int(saved["target_rational_rank"])
    ranks = []
    for index, prime in enumerate(primes, start=1):
        rank = modular_rank_low(
            columns, prime, budget, f"p={p} mask={mask} prime={index}"
        )
        ranks.append(rank)
        if rank != target:
            raise AssertionError({"p": p, "mask": mask, "prime": str(prime), "rank": rank})
    product = 1
    for prime in primes:
        product *= prime
    squared_norm = max(map(len, columns))
    if hex(product) != saved["prime_product_hex"] or squared_norm != saved["maximum_squared_column_norm"]:
        raise AssertionError({"p": p, "mask": mask, "product_or_norm": False})
    if not covered(product, squared_norm, target):
        raise AssertionError({"p": p, "mask": mask, "coverage": False})
    previous = product // primes[-1]
    if covered(previous, squared_norm, target):
        raise AssertionError({"p": p, "mask": mask, "nonminimal_prime_prefix": True})
    gap = target - int(saved["rank_mod_two"])
    beta = int(saved["first_bockstein_rank"])
    if gap != beta or saved["complete_two_primary_type"] != f"(Z/2)^{beta}":
        raise AssertionError({"p": p, "mask": mask, "smith_implication": False})

    mutated = [[list(entry) for entry in column] for column in columns]
    first = next(column for column in mutated if column)
    first[0][1] = int(first[0][1]) + 1
    mutated_hash = digest({"kept_rows": kept, "row_atoms": atoms, "signed_columns": mutated})
    if mutated_hash == projection_hash:
        raise AssertionError({"p": p, "mask": mask, "mutation_control": False})
    return {
        "mask": mask,
        "prime_count": len(primes),
        "all_primes_verified": True,
        "all_low_pivot_ranks": target,
        "minimal_coverage_prefix": True,
        "rank_gap": gap,
        "first_bockstein_rank": beta,
        "elementary_two_primary_verified": True,
        "mutated_projection_rejected": True,
    }


def verify_triangle_consequences(producer: dict[str, object]) -> int:
    comparison = json.loads((EXP063 / "artifacts" / "results.json").read_text(encoding="utf-8"))
    comparison_rows = {int(row["p"]): row for row in comparison["rows"]}
    checks = 0
    for row in producer["rows"]:
        p = int(row["p"])
        comparison_masks = {
            int(item["mask"]): item for item in comparison_rows[p]["masks"]
        }
        for consequence in row["triangle_consequences"]:
            mask = int(consequence["mask"])
            relations = comparison_masks[mask]["relations"]
            expected_zero = [item["triangles"][0] for item in relations]
            if any(len(item["triangles"]) != 1 for item in relations):
                raise AssertionError({"p": p, "mask": mask, "relation_not_singleton": True})
            if consequence["integrally_zero_triangles"] != expected_zero:
                raise AssertionError({"p": p, "mask": mask, "zero_set": False})
            beta = next(
                int(item["first_bockstein_rank"])
                for item in row["certificates"] if int(item["mask"]) == mask
            )
            if len(consequence["complete_two_primary_generators"]) != beta:
                raise AssertionError({"p": p, "mask": mask, "generator_count": False})
            checks += 1
    return checks


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--budget-seconds", type=float, default=1200.0)
    parser.add_argument("--memory-gib", type=float, default=12.0)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if args.memory_gib <= 0:
        raise ValueError("memory cap must be positive")
    actual = {str(path.relative_to(EXPERIMENTS)): sha256(path) for path in PINS}
    expected = {
        str(path.relative_to(EXPERIMENTS)): expected_hash for path, expected_hash in PINS.items()
    }
    if actual != expected:
        raise AssertionError({"pin_mismatch": {"actual": actual, "expected": expected}})
    producer = json.loads(RESULTS.read_text(encoding="utf-8"))
    unsigned = dict(producer)
    artifact_hash = unsigned.pop("artifact_hash")
    if digest(unsigned) != artifact_hash:
        raise AssertionError("producer self-hash mismatch")
    if diagonal_first_bockstein(2) != 1 or diagonal_first_bockstein(4) != 0:
        raise AssertionError("synthetic exponent controls failed")

    budget = Budget(args.budget_seconds)
    rows = []
    for producer_row in producer["rows"]:
        p = int(producer_row["p"])
        matrix_path = EXP042 / "artifacts" / f"matrix-p{p}.json"
        if sha256(matrix_path) != MATRIX_SHA256[p]:
            raise AssertionError({"p": p, "matrix_hash": False})
        matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
        certificates = []
        for saved in producer_row["certificates"]:
            print(f"audit p={p} mask={saved['mask']}", flush=True)
            certificates.append(
                audit_certificate(p=p, saved=saved, matrix=matrix, budget=budget)
            )
        rows.append({"p": p, "certificates": certificates})
        write_json_atomic(
            args.output,
            {
                "experiment": "EXP-064-audit",
                "status": "PARTIAL",
                "completed": [row["p"] for row in rows],
                "rows": rows,
                "elapsed_seconds": time.monotonic() - budget.started,
            },
        )
        budget.check(f"p={p} checkpoint")

    consequence_checks = verify_triangle_consequences(producer)
    result = {
        "experiment": "EXP-064-audit",
        "status": "COMPLETE",
        "pins": actual,
        "producer_artifact_hash": artifact_hash,
        "checks": {
            "parameters": len(rows),
            "carrier_certificates": sum(len(row["certificates"]) for row in rows),
            "prime_rank_recomputations": sum(
                item["prime_count"] for row in rows for item in row["certificates"]
            ),
            "minimal_coverage_controls": sum(len(row["certificates"]) for row in rows),
            "mutated_projection_controls": sum(len(row["certificates"]) for row in rows),
            "synthetic_exponent_controls": 2,
            "triangle_consequence_checks": consequence_checks,
        },
        "rows": rows,
        "elapsed_seconds": time.monotonic() - budget.started,
    }
    result["artifact_hash"] = digest(result)
    write_json_atomic(args.output, result)
    print(json.dumps({"status": result["status"], "checks": result["checks"],
                      "elapsed_seconds": result["elapsed_seconds"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
