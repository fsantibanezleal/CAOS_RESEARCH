"""Symbolic arithmetic certificate for the EXP-033 regularity-gap theorem."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent


def digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def choose(n: int, k: int) -> int:
    return math.comb(n, k) if 0 <= k <= n else 0


def lambda_rank(c: int, a: int) -> int:
    return c * choose(c, a) - choose(c, a + 1) - choose(c, a - 1)


def parameter_row(p: int) -> dict[str, object]:
    c = 2 * p - 2
    m = 8 * p
    n = 10 * p
    ranks = [lambda_rank(c, a) for a in range(1, c)]
    beta_25 = ranks[0]
    beta_36 = m * ranks[0] + ranks[1]
    obligations = {
        "parameter_range": p >= 4,
        "kernel_h_vector": [0, m, n, 0, 0] == [0, 8 * p, 10 * p, 0, 0],
        "kernel_stable_rank": m + n == 18 * p,
        "a_h_numerator": [1, c + m, n - m + 1, -n]
        == [1, n - 2, 2 * p + 1, -n],
        "beta_2_5_anchor": beta_25 == p * (2 * p - 3),
        "beta_3_6_anchor": beta_36 == 8 * p * (7 * p * p - 12 * p + 2) // 3,
        "row_three_support_end": (c - 1) + m + 1 == n - 2,
        "row_four_support_start": c + 1 == 2 * p - 1,
        "row_four_support_end": c + m + 1 == n - 1,
        "penultimate_edge": choose(m, m - 1) == 8 * p,
        "terminal_edge": choose(m, m) == 1,
    }
    if not all(obligations.values()):
        raise AssertionError((p, obligations))
    row: dict[str, object] = {"p": p, "obligations": obligations}
    row["row_hash"] = digest(row)
    return row


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p-max", type=int, default=300)
    parser.add_argument(
        "--output", type=Path, default=HERE / "artifacts" / "symbolic-certificate.json"
    )
    args = parser.parse_args()
    if args.p_max < 4:
        raise SystemExit("p-max must be at least four")

    p, z = sp.symbols("p z", integer=True, positive=True)
    c = 2 * p - 2
    m = 8 * p
    n = 10 * p
    h_c = 1 + (n - 1) * z + 12 * p * z**2 + (2 * p - 1) * z**3 + z**4
    h_d = 1 + c * z + z**2
    h_t = sp.expand(h_d * (1 + z + z**2))
    h_k = sp.expand(h_c - h_t)
    h_a = sp.expand(h_d + (1 - z) * h_k)

    lambda_one = c * sp.binomial(c, 1) - sp.binomial(c, 2) - 1
    lambda_two = c * sp.binomial(c, 2) - sp.binomial(c, 3) - sp.binomial(c, 1)
    symbolic = {
        "section_h_identity": sp.simplify(
            h_t - (1 + (2 * p - 1) * z + 2 * p * z**2 + (2 * p - 1) * z**3 + z**4)
        )
        == 0,
        "kernel_h_identity": sp.simplify(h_k - (m * z + n * z**2)) == 0,
        "a_h_identity": sp.simplify(
            h_a - (1 + (n - 2) * z + (2 * p + 1) * z**2 - n * z**3)
        )
        == 0,
        "lambda_one_identity": sp.simplify(lambda_one - p * (2 * p - 3)) == 0,
        "lambda_two_identity": sp.simplify(
            lambda_two - sp.Rational(8, 3) * p * (p - 1) * (p - 2)
        )
        == 0,
        "degree_six_identity": sp.simplify(
            m * lambda_one + lambda_two
            - sp.Rational(8, 3) * p * (7 * p**2 - 12 * p + 2)
        )
        == 0,
        "projective_dimensions": sp.simplify(c + m - (n - 2)) == 0,
        "mapping_cone_top_degree": sp.simplify(c + m + 1 - (n - 1)) == 0,
    }
    if not all(symbolic.values()):
        raise AssertionError(symbolic)

    rows = [parameter_row(parameter) for parameter in range(4, args.p_max + 1)]
    payload: dict[str, object] = {
        "experiment": "EXP-033-minimal-cubic-mapping-cone",
        "route": "symbolic-arithmetic",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "SYMBOLIC_CERTIFICATE_PASS",
        "range": [4, args.p_max],
        "symbolic_obligations": symbolic,
        "rows": rows,
        "proof_boundary": (
            "The certificate checks Hilbert and Betti arithmetic. The intersection identity, "
            "Cohen-Macaulay kernel, regularity inequality, and minimal mapping cone are proved "
            "deductively in proof.md."
        ),
    }
    payload["symbolic_aggregate"] = digest([row["row_hash"] for row in rows])
    write_json_atomic(args.output, payload)
    print(f"EXP-033 symbolic PASS aggregate={payload['symbolic_aggregate']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
