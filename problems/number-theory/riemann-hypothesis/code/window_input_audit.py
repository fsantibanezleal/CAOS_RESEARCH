"""Independent scalar window evaluation for EXP-019 using native Arb sinc."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from flint import arb, ctx, fmpq

CODE = Path(__file__).resolve().parent
PACKET = CODE.parent/"experiments/EXP-018-nine-point-distinct-transfer/artifacts/input/nine-point-final.json"
PACKET_SHA = "9f113eb52fba9c3a1fd7d5f2714e925ef19d3104b8fdaa982661fa96794d0c0d"


def certify_window(subdivisions=4096, precision=256):
    if subdivisions < 4096 or precision < 256:
        raise ValueError("audit requires the declared cell/precision minimum")
    ctx.prec = precision
    raw = PACKET.read_bytes()
    if hashlib.sha256(raw).hexdigest() != PACKET_SHA:
        raise ValueError("window packet mismatch")
    packet = json.loads(raw)
    coefficients = [arb(fmpq(n, packet["window_coefficient_denominator"]))
                    for n in packet["window_coefficient_numerators"]]
    frequencies = [arb(2).sqrt()]+[2*j*arb.pi() for j in range(1, 7)]

    def inner(a, b):
        return (((a-b)/2).sinc()+((a+b)/2).sinc())/2

    def absolute_inner(a, b):
        # u_a(t)''=2cos(at), u_a even, u_a'(1/2)=integral cos(as)ds.
        # Thus u_a(t)=sin(a/2)/a+2cos(a/2)/a^2-2cos(at)/a^2.
        return ((a/2).sin()/a+2*(a/2).cos()/(a*a))*(b/2).sinc()-2*inner(a, b)/(a*a)

    i1 = sum((c*(a/2).sinc() for c, a in zip(coefficients, frequencies)), arb(0))
    i2 = j = arb(0)
    symmetry_checks = 0
    for ci, ai in zip(coefficients, frequencies):
        for cj, aj in zip(coefficients, frequencies):
            i2 += ci*cj*inner(ai, aj)
            ab, ba = absolute_inner(ai, aj), absolute_inner(aj, ai)
            if not (ab-ba).contains(0):
                raise ValueError("absolute-integral symmetry failed")
            j += ci*cj*(ab+ba)/2
            symmetry_checks += 1
    if not (i1 > 0 and i2+j > 0):
        raise ValueError("nonpositive normalization")
    h = 2-(i2+j)/(i1*i1)
    h0 = fmpq(3362285207, 5000000000)
    if not h >= arb(h0):
        raise ValueError("window energy coefficient failed")

    minimum = math.inf
    derivative_factor_upper = -math.inf
    for index in range(subdivisions):
        cell = arb(fmpq(2*index+1, 4*subdivisions), fmpq(1, 4*subdivisions))
        value = sum((c*(a*cell).cos() for c, a in zip(coefficients, frequencies)), arb(0))
        factor = sum((-c*a*a*(a*cell).sinc() for c, a in zip(coefficients, frequencies)), arb(0))
        minimum = min(minimum, math.nextafter(float(value.lower()), -math.inf))
        derivative_factor_upper = max(derivative_factor_upper,
                                      math.nextafter(float(factor.upper()), math.inf))
    if not minimum >= 0.75 or not derivative_factor_upper <= 0:
        raise ValueError({"minimum": minimum, "derivative_factor_upper": derivative_factor_upper})
    maximum = sum(coefficients, arb(0))  # monotonicity puts max at zero
    if not maximum <= 1:
        raise ValueError("window upper bound failed")
    return {"schema": "exp019-window-audit-v1", "passed": True,
            "packet_sha256": PACKET_SHA, "code_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "precision": precision, "subdivisions": subdivisions, "symmetry_checks": symmetry_checks,
            "normalization": i1.str(60), "I2": i2.str(60), "J": j.str(60),
            "H": h.str(60), "H_cert": str(h0), "H_slack": (h-arb(h0)).str(40),
            "window_lower_binary64": minimum.hex(), "window_upper": maximum.str(40),
            "derivative_factor_upper_binary64": derivative_factor_upper.hex(),
            "method": "native Arb sinc; independently symmetrized ODE-derived integral; complete interval cell cover",
            "analytic_pair_correlation_theorem": "attributed, not established by this scalar certificate"}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = certify_window()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes((json.dumps(result, indent=2)+"\n").encode())
    print(json.dumps(result, indent=2), flush=True)
