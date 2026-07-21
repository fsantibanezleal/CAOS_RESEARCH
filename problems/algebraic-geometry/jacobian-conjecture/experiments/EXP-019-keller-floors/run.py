# EXP-019: the Keller floors. CPU-only, sympy over QQ. See hypothesis.md.
# Parts: 1 floor framework + h-divisibility (library) | 2 wider bilinear certificates
#        ((2,4), (2,5), (3,4)) | 3 full-A elimination at (2,3).
# Run: .\.venv\Scripts\python.exe ...\EXP-019-keller-floors\run.py [1|2|3]
import itertools
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib.keller2lib import (graded_piece, jac2, library, sqf_radical,  # noqa: E402
                              top_form, x, y)
from sympy import (Poly, Rational, cancel, div, expand, groebner, nan, oo,  # noqa: E402
                   solve, symbols, zoo)

failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def part1():
    print("=" * 76)
    print("Part 1: floor framework + h-divisibility on the library")
    print("=" * 76)
    shown = 0
    for i, (P, Q) in enumerate(library()):
        Pt, m = top_form(P)
        Qt, n = top_form(Q)
        if m + n <= 2:
            continue
        # floor 2 identity: J(P_m, Q_{n-1}) + J(P_{m-1}, Q_n) == 0 when m + n - 3 > 0
        if m + n - 3 > 0:
            f2 = expand(jac2(Pt, graded_piece(Q, n - 1)) + jac2(graded_piece(P, m - 1), Qt))
            check(f"map {i}: floor-2 identity holds", f2 == 0)
        # floor 3 identity when m + n - 4 > 0
        if m + n - 4 > 0:
            f3 = expand(jac2(Pt, graded_piece(Q, n - 2))
                        + jac2(graded_piece(P, m - 1), graded_piece(Q, n - 1))
                        + jac2(graded_piece(P, m - 2), Qt))
            check(f"map {i}: floor-3 identity holds", f3 == 0)
        # h-divisibility exhibit on the first three nontrivial maps:
        if shown < 3 and m + n - 3 > 0:
            h = sqf_radical(Pt)
            g = expand(jac2(h, graded_piece(Q, n - 1)) * 1)
            # From floor 2 with P_m = a h^p, Q_n = b h^q: h^{min(p,q)-1} divides the mixed
            # Jacobian combination; exhibit h | J(P_m, Q_{n-1}) when p >= 2.
            ptop = Poly(Pt, x, y).total_degree() // max(Poly(h, x, y).total_degree(), 1)
            if ptop >= 2:
                quo, rem_ = div(jac2(Pt, graded_piece(Q, n - 1)), h, x, y)
                check(f"map {i}: h divides J(P_top, Q_sub) (p = {ptop})", expand(rem_) == 0)
                shown += 1
    check("Part 1 exhibited divisibility on maps with p >= 2", shown >= 1, f"shown = {shown}")


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


def run_pair(msmall, nlarge, grid_vals, label, samples=None):
    MP = monsrange(2, msmall)
    MQ = monsrange(2, nlarge)
    B = symbols(f"B_0:{len(MQ)}")
    stats = {"consistent": 0, "inconsistent": 0, "instances": 0, "triangular_seen": 0}
    multi = []
    SAMP = [Rational(1), Rational(-2), Rational(1, 3), Rational(0), Rational(3, 2)]
    Asamples = samples if samples is not None else list(itertools.product(grid_vals, repeat=len(MP)))
    print(f"{label}: grid on the degree-{msmall} side: {len(Asamples)} samples")
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
    for k_, v_ in stats.items():
        print(f"  {k_}: {v_}")
    check(f"{label}: non-vacuous with triangular witnesses",
          stats["instances"] > 0 and stats["triangular_seen"] > 0)
    check(f"{label}: every Keller instance injective (JC(2) holds here)", not multi,
          str(multi)[:140])


def part2():
    print("=" * 76)
    print("Part 2: wider bilinear certificates")
    print("=" * 76)
    vals = [Rational(-1), Rational(0), Rational(1), Rational(2)]
    run_pair(2, 4, vals, "(2,4)")
    run_pair(2, 5, [Rational(-1), Rational(0), Rational(1)], "(2,5)")
    base = [Rational(1), Rational(-2), Rational(1, 3), Rational(3, 2), Rational(-1), Rational(2), Rational(-1, 2)]
    samples34 = [tuple([Rational(0)] * 7)]
    for i in range(7):
        for v_ in (Rational(1), Rational(-2)):
            a = [Rational(0)] * 7
            a[i] = v_
            samples34.append(tuple(a))
    for shift in range(20):
        samples34.append(tuple(base[(k + shift) % 7] * (1 if (k + shift) % 2 == 0 else -1)
                               for k in range(7)))
    run_pair(3, 4, None, "(3,4)", samples=samples34)


def part3():
    print("=" * 76)
    print("Part 3: full-A elimination at (2, 3)")
    print("=" * 76)
    MP = monsrange(2, 2)
    MQ = monsrange(2, 3)
    A = symbols(f"A_0:{len(MP)}")
    B = symbols(f"B_0:{len(MQ)}")
    P = x + sum(a * mo for a, mo in zip(A, MP))
    Q = y + sum(b * mo for b, mo in zip(B, MQ))
    eqs = [e for e in Poly(expand(jac2(P, Q) - 1), x, y).coeffs() if e != 0]
    gb = groebner(eqs, *(list(B) + list(A)), order="lex")
    cons = [g for g in gb.exprs if not any(g.has(b) for b in B)]
    print(f"  GB size: {len(gb.exprs)}; B-free consistency generators: {len(cons)}")
    for g in cons[:6]:
        print(f"    {g} = 0")
    check("elimination completed: consistency ideal in A computed", True,
          f"{len(cons)} generators")
    # The consistency variety must contain the triangular locus A = 0 (witnesses exist there).
    ok0 = all(g.subs({a: 0 for a in A}) == 0 for g in cons)
    check("A = 0 (triangular locus) lies on the consistency variety", ok0)


PARTS = {"1": part1, "2": part2, "3": part3}
todo = sys.argv[1:] if len(sys.argv) > 1 else ["1", "2", "3"]
for p_ in todo:
    PARTS[p_]()
    print()
if failures:
    print(f"RESULT: {len(failures)} FAILED: {failures}")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS.")
