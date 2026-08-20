"""Independent Hilbert-coefficient audit for EXP-032.

This module intentionally imports no canonical experiment code and does not use
the declared closed formula for the linear strand.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from datetime import datetime, timezone
from math import comb
from pathlib import Path


HERE = Path(__file__).resolve().parent


def digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def save(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def polynomial_product(left: list[int], right: list[int]) -> list[int]:
    output = [0] * (len(left) + len(right) - 1)
    for i, x in enumerate(left):
        for j, y in enumerate(right):
            output[i + j] += x * y
    return output


def binomial_row(n: int) -> list[int]:
    row = [1]
    for k in range(n):
        row.append(row[-1] * (n - k) // (k + 1))
    return row


def audit_parameter(parameter: int, claimed: dict[str, object]) -> tuple[dict[str, object], dict[str, object]]:
    c = 2 * parameter - 2
    m = 8 * parameter
    total = c + m
    low_binomials = binomial_row(c)
    alternating_binomial = [(-1) ** k * value for k, value in enumerate(low_binomials)]
    numerator = polynomial_product([1, c, 1], alternating_binomial)

    # In degree a+1, minimality, regularity two, and the terminal-shift shape
    # leave only (-1)^a beta_(a,a+1).  Read the ranks from those coefficients.
    linear = [0] * (c + 1)
    for a in range(1, c):
        linear[a] = (-1) ** a * numerator[a + 1]
    diagonal = [1] + [0] * c
    quadratic = [0] * c + [1]
    koszul = binomial_row(m)
    full_diagonal = koszul
    full_quadratic = [0] * c + koszul
    full_numerator = polynomial_product(
        [1, c, 1], [(-1) ** k * value for k, value in enumerate(binomial_row(total))]
    )
    full_linear = [0] * (total + 1)
    for i in range(1, total):
        diagonal_contribution = (
            (-1) ** (i + 1) * full_diagonal[i + 1]
            if i + 1 < len(full_diagonal)
            else 0
        )
        quadratic_contribution = (
            (-1) ** (i - 1) * full_quadratic[i - 1] if i >= 1 else 0
        )
        full_linear[i] = (-1) ** i * (
            full_numerator[i + 1]
            - diagonal_contribution
            - quadratic_contribution
        )

    observed_hashes = {
        "low_linear_hash": digest(linear),
        "full_diagonal_hash": digest(full_diagonal),
        "full_linear_hash": digest(full_linear),
        "full_quadratic_hash": digest(full_quadratic),
        "hilbert_numerator_hash": digest(full_numerator),
    }
    comparisons = {
        name: observed == claimed[name] for name, observed in observed_hashes.items()
    }
    checks = {
        "coefficient_inference_positive": all(value > 0 for value in linear[1:c]),
        "terminal_coefficients": numerator[0] == 1 and numerator[-1] == 1,
        "silent_degrees": numerator[1] == 0 and numerator[c + 1] == 0,
        "claimed_hashes_match": all(comparisons.values()),
        "claimed_projective_dimension": claimed["projective_dimension"] == total,
        "claimed_regularity": claimed["regularity"] == 2,
        "literal_small_koszul_convolution": (
            parameter > 12 or full_linear == polynomial_product(linear, koszul)
        ),
    }
    if not all(checks.values()):
        raise AssertionError((parameter, checks, comparisons))
    row: dict[str, object] = {
        "p": parameter,
        "coefficient_numerator_hash": digest(numerator),
        "observed_hashes": observed_hashes,
        "comparisons": comparisons,
        "checks": checks,
    }
    row["row_hash"] = digest(row)
    table = {
        "p": parameter,
        "low": {"diagonal": diagonal, "linear": linear, "quadratic": quadratic},
        "over_P": {
            "diagonal": full_diagonal,
            "linear": full_linear,
            "quadratic": full_quadratic,
        },
    }
    return row, table


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=HERE / "artifacts" / "results.json")
    parser.add_argument("--output", type=Path, default=HERE / "artifacts" / "audit.json")
    parser.add_argument("--budget-seconds", type=float, default=120.0)
    args = parser.parse_args()
    started = time.perf_counter()
    canonical = json.loads(args.input.read_text(encoding="utf-8"))
    if canonical.get("status") != "PASS":
        raise RuntimeError("canonical result is not PASS")
    rows = []
    small_tables: dict[str, object] = {}
    for claimed in canonical["rows"]:
        parameter = claimed["p"]
        row, table = audit_parameter(parameter, claimed)
        rows.append(row)
        if parameter <= 6:
            small_tables[str(parameter)] = table
            if table != canonical["small_tables"][str(parameter)]:
                raise AssertionError(f"p={parameter}: exact small table disagreement")
        if parameter in (4, 5, 6, 10, 25, 50, 100, 200, canonical["range"][1]):
            print(f"audit p={parameter}: coefficient reconstruction agrees", flush=True)
        if time.perf_counter() - started > args.budget_seconds:
            save(
                args.output,
                {
                    "experiment": "EXP-032-complete-colon-resolution",
                    "route": "independent-coefficient-reconstruction",
                    "status": "INCONCLUSIVE_BUDGET",
                    "completed": [item["p"] for item in rows],
                    "elapsed_seconds": time.perf_counter() - started,
                },
            )
            return 2
    payload: dict[str, object] = {
        "experiment": "EXP-032-complete-colon-resolution",
        "route": "independent-coefficient-reconstruction",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "PASS",
        "range": canonical["range"],
        "canonical_aggregate": canonical["canonical_aggregate"],
        "rows": rows,
        "small_tables": small_tables,
        "elapsed_seconds": time.perf_counter() - started,
    }
    payload["audit_aggregate"] = digest([row["row_hash"] for row in rows])
    save(args.output, payload)
    print(f"PASS aggregate={payload['audit_aggregate']}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
