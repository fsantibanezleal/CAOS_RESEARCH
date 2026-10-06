"""Exact remainder controls and one actual-window isolation witness."""
import argparse
from fractions import Fraction as F
import hashlib
import importlib.util
from itertools import product
import json
from pathlib import Path
import time

from flint import arb, ctx, fmpq

HERE = Path(__file__).resolve().parent
E25 = HERE.parent / "EXP-025-vector-pressure-distinct-lift"


def as_arb(x):
    return arb(fmpq(x.numerator, x.denominator))


def exact_controls():
    vectors = [(F(1), F()), (F(), F(1)), (F(3, 5), F(4, 5)), (F(-3, 5), F(4, 5))]
    count = 0
    for vs in product(vectors, repeat=3):
        u = [[sum((a*b for a, b in zip(vs[i], vs[j])), F()) for j in range(3)] for i in range(3)]
        # For these 3-point PSD Grams tau>2, so C=X without spectral approximation.
        c = [[u[i][j]-F(i == j) for j in range(3)] for i in range(3)]
        for ds in product((1, 2), repeat=3):
            gamma = sum(((1-F(1, ds[i]*ds[j]))*c[i][j]**2 for i in range(3) for j in range(3)), F())
            coloured = sum((c[i][j]**2 for i in range(3) for j in range(3) if ds[i] == 2), F())
            crossing = sum((c[i][j]**2 for i in range(3) for j in range(3) if ds[i] == 2 and ds[j] == 1), F())
            assert gamma == F(3, 4)*coloured+F(1, 4)*crossing
            assert gamma >= F(1, 2)*coloured
            count += 1
    energy = 2*F(3, 5)**2
    witness_slack = energy-F(31, 30)*energy
    assert witness_slack == -F(3, 125)
    # An all-doubled nonzero remainder rejects increasing its sharp 3/4 coefficient.
    sharp_c2 = 2*F(1, 10)**2
    assert F(3, 4)*sharp_c2 < F(4, 5)*sharp_c2
    return {"exact_colouring_cases": count, "generic_orthogonal_witness_slack": str(witness_slack),
            "inflated_remainder_coefficient_rejected": True, "count_only_factor_rejected": True}


def actual_window():
    spec = importlib.util.spec_from_file_location("exp025_source_reader", E25 / "run.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    raw = (E25 / "artifacts/input/Solution.lean").read_bytes()
    coefficients, _, _ = module.source_packet(raw)
    ctx.prec = 256
    cs = [as_arb(x) for x in coefficients]
    theta = arb(2).sqrt()/2
    frequencies = [2*theta]+[2*j*arb.pi() for j in range(1, 13)]
    norm = sum((c*(a/2).sinc() for c, a in zip(cs, frequencies)), arb(0))
    assert norm > 0

    def kernel(x):
        x = arb(x)
        return sum((c*(((a+2*arb.pi()*x)/2).sinc()+((a-2*arb.pi()*x)/2).sinc())/2
                    for c, a in zip(cs, frequencies)), arb(0))/norm

    r = 1000
    a, b, d = kernel(arb(1)/2), kernel(r), kernel(arb(r)+arb(1)/2)
    assert a > 0 and a < 1
    # Independent closed trig forms at integer/half-integer frequencies.
    b_closed = theta*theta.sin()/(theta**2-arb.pi()**2*r*r)/norm
    x = arb(r)+arb(1)/2
    d_closed = (arb.pi()*x*theta.cos()/(arb.pi()**2*x*x-theta**2)
                +sum((cs[j]*((-1)**j)*x/(arb.pi()*(x*x-j*j)) for j in range(1, 13)), arb(0)))/norm
    assert (b-b_closed).contains(0) and (d-d_closed).contains(0)
    row_bounds = [2+arb(2).sqrt()*(b.abs_upper()+d.abs_upper()),
                  1+a.abs_upper()+arb(2).sqrt()*b.abs_upper(),
                  1+a.abs_upper()+arb(2).sqrt()*d.abs_upper()]
    c = as_arb(F(17043, 5000))
    assert all(x < c for x in row_bounds)
    small = b*b+d*d
    psi = 2*(a*a+small)
    omega = 2*a*a+4*small
    ratio = omega/psi
    assert ratio < as_arb(F(31, 30))
    return {"source_sha256": hashlib.sha256(raw).hexdigest(), "precision_bits": 256,
            "points": [-r, "0", "1/2"], "multiplicities": [2, 1, 1],
            "K_half": str(a), "K_integer": str(b), "K_half_integer": str(d),
            "closed_formula_checks": 2, "weighted_gram_row_upper_bounds": [str(x) for x in row_bounds],
            "clipping_inactive_certified": True, "psi": str(psi), "omega": str(omega),
            "ratio": str(ratio), "proposed_factor": "31/30", "strict_counterexample": True,
            "arithmetic_trust": "Both scalar paths share FLINT/Arb; limiting-family proof is analytic."}


def run():
    start = time.monotonic()
    exact = exact_controls()
    print(json.dumps({"event": "exact-controls", "cases": exact["exact_colouring_cases"]}), flush=True)
    window = actual_window()
    elapsed = time.monotonic()-start
    assert elapsed < 30
    return {"schema": "exp026-multiplicity-retention-v1", "passed": True,
            "hypothesis_sha256": hashlib.sha256((HERE / "hypothesis.md").read_bytes()).hexdigest(),
            "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "exact_controls": exact, "actual_window_witness": window, "elapsed_seconds": elapsed,
            "scope": "Retained algebra and an isolation obstruction; no new zero bound or effective height."}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    if args.receipt.exists():
        raise SystemExit("Preserve the previous receipt")
    result = run()
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(result, indent=2), flush=True)
