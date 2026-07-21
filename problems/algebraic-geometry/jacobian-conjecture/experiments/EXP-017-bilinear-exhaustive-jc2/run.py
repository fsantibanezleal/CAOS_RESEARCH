# EXP-017: bilinear exhaustive-in-Q JC(2) certificates. CPU-only, sympy over QQ.
# Run: .\.venv\Scripts\python.exe ...\EXP-017-bilinear-exhaustive-jc2\run.py [23|33]
import itertools
import sys

from sympy import Poly, Rational, cancel, expand, groebner, nan, oo, solve, symbols, zoo

x, y = symbols("x y")
failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def jac2(P, Q):
    return expand(P.diff(x) * Q.diff(y) - P.diff(y) * Q.diff(x))


def monsrange(lo, d):
    return [x**i * y**j for i in range(d + 1) for j in range(d + 1 - i) if i + j >= lo]


def fiber_size(Pi, Qi):
    x0, y0 = Rational(2, 3), Rational(-1, 2)
    t0, t1 = Pi.subs({x: x0, y: y0}), Qi.subs({x: x0, y: y0})
    gb = groebner([expand(Pi - t0), expand(Qi - t1)], x, y, order="lex")
    if gb.exprs == [1]:
        return 0
    uni = [g for g in gb.exprs if g.free_symbols <= {y}]
    return Poly(uni[-1], y).degree() if uni else -1


def run_pair(m, n, Asamples, label):
    print("=" * 76)
    print(f"{label}: degrees ({m}, {n}), {len(Asamples)} A-samples, exhaustive in B per sample")
    print("=" * 76)
    MP = monsrange(2, m)
    MQ = monsrange(2, n)
    B = symbols(f"B_0:{len(MQ)}")
    stats = {"consistent": 0, "inconsistent": 0, "instances": 0, "triangular_seen": 0}
    multi = []
    SAMP = [Rational(1), Rational(-2), Rational(1, 3), Rational(0), Rational(3, 2)]
    for Avec in Asamples:
        P = x + sum(Rational(a) * mo for a, mo in zip(Avec, MP))
        Q = y + sum(co * mo for co, mo in zip(B, MQ))
        eqs = [e for e in Poly(expand(jac2(P, Q) - 1), x, y).coeffs() if e != 0]
        sols = solve(eqs, list(B), dict=True)
        if not sols:
            stats["inconsistent"] += 1
            continue
        stats["consistent"] += 1
        for sol in sols:
            frees = sorted({fs for e in sol.values() for fs in e.free_symbols}, key=str)
            for shift in range(2):
                inst = {fs: SAMP[(k + shift) % len(SAMP)] for k, fs in enumerate(frees)}
                Qi = cancel(Q.subs(sol).subs(inst))
                if Qi.has(zoo) or Qi.has(nan) or Qi.has(oo):
                    continue
                Ji = jac2(P, Qi)
                if not Ji.is_number or Ji == 0:
                    continue
                stats["instances"] += 1
                if all(a == 0 for a in Avec):
                    stats["triangular_seen"] += 1
                ns = fiber_size(P, Qi)
                if ns > 1 or ns == -1:
                    multi.append((P, Qi, ns))
    for k, v_ in stats.items():
        print(f"  {k}: {v_}")
    check(f"{label}: scan non-vacuous", stats["instances"] > 0)
    check(f"{label}: triangular witnesses appear (A = 0 sample consistent)",
          stats["triangular_seen"] > 0)
    check(f"{label}: every Keller instance has in-image fiber <= 1 (JC(2) holds here)",
          not multi, str(multi)[:160])


def pair23():
    vals = [Rational(-2), Rational(-1), Rational(0), Rational(1), Rational(2), Rational(1, 2)]
    Asamples = list(itertools.product(vals, repeat=3))
    run_pair(2, 3, Asamples, "(2,3)")


def pair33():
    vals = [Rational(-1), Rational(0), Rational(1), Rational(2), Rational(-1, 2)]
    base = [Rational(1), Rational(-2), Rational(1, 3), Rational(3, 2), Rational(-1, 5),
            Rational(2), Rational(-1)]
    Asamples = []
    # structured zero patterns: exactly one/two nonzero entries
    for i in range(7):
        for v_ in (Rational(1), Rational(-2)):
            a = [Rational(0)] * 7
            a[i] = v_
            Asamples.append(tuple(a))
    # mixed deterministic vectors
    for shift in range(30):
        Asamples.append(tuple(base[(k + shift) % 7] * (1 if (k + shift) % 2 == 0 else -1)
                              for k in range(7)))
    Asamples.append(tuple([Rational(0)] * 7))
    run_pair(3, 3, Asamples, "(3,3)")


PARTS = {"23": pair23, "33": pair33}
todo = sys.argv[1:] if len(sys.argv) > 1 else ["23", "33"]
for p_ in todo:
    PARTS[p_]()
    print()
if failures:
    print(f"RESULT: {len(failures)} FAILED: {failures}")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS.")
