"""Symbolic and exact arithmetic certificate for EXP-032."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from math import comb
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def rank(c: int, a: int) -> int:
    return c * comb(c, a) - comb(c, a + 1) - comb(c, a - 1)


def binomial_row(n: int) -> list[int]:
    row = [1]
    for k in range(n):
        row.append(row[-1] * (n - k) // (k + 1))
    return row


def parameter_row(parameter: int) -> dict[str, object]:
    c = 2 * parameter - 2
    binomials = binomial_row(c)
    values = [
        c * binomials[a] - binomials[a + 1] - binomials[a - 1]
        for a in range(1, c)
    ]
    obligations = {
        "parameter_range": parameter >= 4,
        "even_codimension": c % 2 == 0,
        "positive_linear_ranks": all(value > 0 for value in values),
        "rank_symmetry": all(values[a - 1] == values[c - a - 1] for a in range(1, c)),
        "first_known_coefficient": values[0] == parameter * (2 * parameter - 3),
        "second_known_coefficient": (
            values[1] == 8 * parameter * (parameter - 1) * (parameter - 2) // 3
        ),
        "linear_rank_sum": sum(values) == (c - 2) * 2**c + 2,
        "low_total_rank": 2 + sum(values) == (c - 2) * 2**c + 4,
        "full_endpoint": c + 8 * parameter == 10 * parameter - 2,
    }
    if not all(obligations.values()):
        raise AssertionError((parameter, obligations))
    row: dict[str, object] = {"p": parameter, "c": c, "obligations": obligations}
    row["row_hash"] = digest(row)
    return row


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p-max", type=int, default=300)
    parser.add_argument(
        "--output", type=Path, default=HERE / "artifacts" / "symbolic-certificate.json"
    )
    args = parser.parse_args()

    c, a, p = sp.symbols("c a p", integer=True, positive=True)
    closed = c * sp.binomial(c, a) - sp.binomial(c, a + 1) - sp.binomial(c, a - 1)
    factored = sp.factor(sp.combsimp(closed / sp.binomial(c, a)))
    expected_factor = sp.factor(a * (c - a) * (c + 2) / ((a + 1) * (c - a + 1)))
    symbolic = {
        "positive_factor_identity": sp.simplify(factored - expected_factor) == 0,
        "first_rank_identity": sp.simplify(closed.subs({c: 2 * p - 2, a: 1}) - p * (2 * p - 3)) == 0,
        "second_rank_identity": sp.simplify(
            closed.subs({c: 2 * p - 2, a: 2})
            - sp.Rational(8, 3) * p * (p - 1) * (p - 2)
        ) == 0,
        "symmetry_identity": sp.simplify(
            closed - closed.xreplace({a: c - a})
        ) == 0,
    }
    # Separate the endpoints explicitly.  A direct SymPy summation with a
    # symbolic upper bound incorrectly leaves residual c-1 for this expression.
    # The three sums below are immediate from sum_a binom(c,a)=2^c.
    sum_identity = sp.simplify(
        c * (2**c - 2)
        - (2**c - 1 - c)
        - (2**c - c - 1)
        - ((c - 2) * 2**c + 2)
    )
    symbolic["linear_sum_identity"] = sum_identity == 0
    if not all(symbolic.values()):
        raise AssertionError({"symbolic": symbolic, "sum_residual": str(sum_identity)})

    rows = [parameter_row(parameter) for parameter in range(4, args.p_max + 1)]
    payload: dict[str, object] = {
        "experiment": "EXP-032-complete-colon-resolution",
        "route": "symbolic-arithmetic",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "PASS",
        "range": [4, args.p_max],
        "symbolic_obligations": symbolic,
        "positive_factor": "binom(c,a)*a*(c-a)*(c+2)/((a+1)*(c-a+1))",
        "linear_rank_sum": "(c-2)*2^c+2",
        "rows": rows,
        "proof_boundary": (
            "Symbolic identities certify the arithmetic consequences. Gorenstein self-duality, "
            "minimality, regularity, and the Koszul tensor argument are proved in proof.md."
        ),
    }
    payload["symbolic_aggregate"] = digest([row["row_hash"] for row in rows])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    save_path = args.output
    temporary = save_path.with_suffix(save_path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(save_path)
    print(f"PASS aggregate={payload['symbolic_aggregate']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
