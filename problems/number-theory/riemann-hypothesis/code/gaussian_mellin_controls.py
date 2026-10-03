"""EXP-024 normalization controls with two enclosed integrals and proven tails."""

import argparse
import hashlib
import json
import math
from pathlib import Path
import time

from flint import acb, arb, ctx, fmpq
import sympy as sp


def gaussian_moment(c, z):
    return sum((z**(c-2*r)*fmpq(math.factorial(c),
               2**c*math.factorial(c-2*r)*math.factorial(r))
               for r in range(c//2+1)), acb(0))


def finite_kernel(x, t, h, beta, order):
    total = acb(0)
    ii, pi = acb(0, 1), arb.pi()
    for sign in [-1, 1]:
        outer = (sign*ii*2*pi*x).exp()
        for j in range(order):
            inner = acb(0)
            for a in range(j+1):
                for b in range(j-a+1):
                    c = j-a-b
                    z = (1-2*beta+2*ii*t+sign*4*pi*ii*x+2*a)/h
                    coefficient = (fmpq(math.factorial(j), math.factorial(a)*
                                   math.factorial(b)*math.factorial(c))*
                                   (-1)**(b+c)*(arb(2)/h)**c)
                    inner += coefficient*gaussian_moment(c, z)*(z*z/4).exp()
            total += outer*(sign*ii*2*pi*x)**j/math.factorial(j)*inner
    return (-beta*x.log()).exp()*total


def error_bound(x, h, order):
    # Controls use purely imaginary beta, hence B=1 and x^-Re beta=1.
    double_factorial = math.prod(range(1, 2*order, 2))
    return (2*arb(2).sqrt()*double_factorial/math.factorial(order)*
            (arb((1+2*order)**2)/(2*h*h)).exp()*(4*arb.pi()*x/(h*h))**order)


def enclosed_kernels(x, t, h, beta):
    pi, ii, radius = arb.pi(), acb(0, 1), arb(8)

    def direct(y, analytic):
        # Entire functions: no branch-dependent operation on y.
        return (-y*y+(1-2*beta+2*ii*t)*y/h).exp()*(2*pi*x*(2*y/h).exp()).cos()

    gaussian = acb.integral(direct, -radius, radius, abs_tol=arb(2)**-100,
                            rel_tol=arb(2)**-100, eval_limit=200000)
    gaussian *= 2*(-beta*x.log()).exp()/pi.sqrt()
    tail = 4/pi.sqrt()/(2*radius-1/h)*(-radius*radius+radius/h).exp()
    gaussian += acb(arb(0, tail.upper()), arb(0, tail.upper()))

    def mellin(v, analytic):
        # Gamma is meromorphic and returns non-finite balls at poles.
        s = arb(fmpq(1, 2))+ii*v
        z = s-beta
        chi = 2*(-z*(2*pi).log()).exp()*z.gamma()*(pi*z/2).cos()
        return chi*(-((v-t)/h)**2-s*x.log()).exp()/(2*pi)

    transformed = acb.integral(mellin, t-radius*h, t+radius*h,
                               abs_tol=arb(2)**-100, rel_tol=arb(2)**-100,
                               eval_limit=200000)
    # |chi(1-(1/2+it)+i*b)|=1 for real b; all controls use Re beta=0.
    tail = h/x.sqrt()*(-radius*radius).exp()/(2*pi*radius)
    transformed += acb(arb(0, tail.upper()), arb(0, tail.upper()))
    if not gaussian.is_finite() or not transformed.is_finite():
        raise ValueError("integrator did not produce a finite enclosure")
    if not gaussian.overlaps(transformed):
        raise ValueError("independently enclosed kernels disagree")
    return gaussian, transformed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    ctx.prec = 192
    started = time.monotonic()
    z = sp.Symbol("z")
    for c in range(9):
        polynomial = sum(sp.Rational(math.factorial(c),
                         2**c*math.factorial(c-2*r)*math.factorial(r))*z**(c-2*r)
                         for r in range(c//2+1))
        assert sp.simplify(sp.diff(sp.exp(z*z/4), z, c)/sp.exp(z*z/4)-polynomial) == 0
    print("nine independent symbolic Gaussian moments PASS", flush=True)
    cases = []
    for xq, t, h in [(fmpq(1, 2), 4, 8), (fmpq(1), 6, 16),
                     (fmpq(2), 12, 16), (fmpq(1), 6, 32)]:
        for beta in [acb(0), acb(0, fmpq(1, 8))]:
            x = arb(xq)
            direct, transformed = enclosed_kernels(x, t, h, beta)
            errors = []
            for order in [1, 2, 3, 4]:
                approx = finite_kernel(x, t, h, beta, order)
                difference = abs(direct-approx)
                bound = error_bound(x, h, order)
                if not difference.upper() <= bound.lower():
                    raise ValueError(f"invalid remainder order={order}")
                errors.append({"order": order, "absolute_difference": str(difference),
                               "proved_upper_bound": str(bound), "passed": True})
            cases.append({"x": str(xq), "T": t, "H": h, "beta": str(beta),
                          "gaussian_enclosure": str(direct), "mellin_enclosure": str(transformed),
                          "overlap": True, "remainders": errors})
            print(f"kernel x={xq} T={t} H={h} beta={beta}: enclosed overlap and four remainders PASS", flush=True)
            if time.monotonic()-started > 600:
                raise RuntimeError("ten-minute planning budget reached; incomplete controls")
    experiment = Path(__file__).resolve().parents[1]/"experiments/EXP-024-gaussian-mellin-reduction"
    paths = [Path(__file__), experiment/"hypothesis.md", experiment/"proof.md"]
    result = {"schema": "exp024-gaussian-mellin-controls-v1", "passed": True,
              "precision": ctx.prec, "symbolic_moments": 9, "integral_cases": cases,
              "elapsed_seconds": time.monotonic()-started,
              "source_sha256": {str(p.relative_to(experiment.parents[1])):
                                hashlib.sha256(p.read_bytes()).hexdigest() for p in paths},
              "scope": "normalization, independent enclosed integrals and explicit phase remainders; no asymptotic moment or zero proportion inferred from finite controls"}
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")


if __name__ == "__main__":
    main()
