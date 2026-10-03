"""Independent divisibility and rational-identity audit, no producer imports."""

import argparse
from fractions import Fraction as F
import hashlib
import json
from math import isqrt
from pathlib import Path


def squarefree(n):
    return all(n % (d*d) for d in range(2, isqrt(n)+1))


def audit(data):
    M, r, h, k, m, n = (data[x] for x in ("M", "r", "h", "k", "m", "n"))
    assert M == 1000000 and r == 1000000
    assert (M+1)//2 <= h <= 3*M//4 and k == h-1
    assert squarefree(h) and squarefree(k)
    assert 1 < k < h < M
    assert m == k*r+1 and n == h*r+1 and h*m-k*n == 1
    assert data["hm_minus_kn"] == 1 and int(data["T"]) == 16*(M*r)**2
    assert m*n < 2*(M*r)**2
    assert F(M*M*r, 5) <= k*n < M*M*r
    S = F(1, 4)+F(1, 9)+F(1, 25)+F(1, 49)+F(1, 121)+F(1, 22)
    assert F(data["prime_square_sum_upper"]) == S < F(12, 25)
    assert F(data["uniform_count_lower_at_M"]) == F(M, 100)-F(1, 25)-2*isqrt(M) > 0
    assert data["nonzero_mobius_weights"] is True
    assert data["nonzero_basic_polynomial_coefficients"] is True
    assert data["summed_mollifier_barrier_established"] is False
    assert data["uniform_comparison"] == "(1/5) M^2 r <= kn < M^2 r for M>=1000000,r>=2"
    assert [int(row["H"]) for row in data["phase_cases"]] == [10**16, 10**18, 10**20]
    for row in data["phase_cases"]:
        H = int(row["H"])
        assert F(row["lower"]) == F(H, h*m)
        assert F(row["upper"]) == F(H, k*n)
    return {"schema": "exp015-independent-audit-v1", "passed": True,
            "route": "trial square division and independent integer/rational substitution",
            "squarefree_twists": [h, k], "summed_mollifier_barrier_established": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw = args.artifact.read_bytes()
    data = json.loads(raw)
    root = Path(__file__).resolve().parents[5]
    for path, expected in data["bindings"].items():
        assert hashlib.sha256((root/path).read_bytes()).hexdigest() == expected
    result = audit(data)
    result["result_sha256"] = hashlib.sha256(raw).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes((json.dumps(result, indent=2, sort_keys=True)+"\n").encode())
    print("EXP-015 independent audit passed", flush=True)


if __name__ == "__main__":
    main()
