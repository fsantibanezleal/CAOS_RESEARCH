# EXP-013: the leading-form cascade. CPU-only, sympy over QQ. See hypothesis.md.
# Parts: 1 dependence at the top ray (library) | 2 ray sweep | 3 exhaustive small-degree JC(2).
#
# Run: .\.venv\Scripts\python.exe ...\EXP-013-leading-form-cascade\run.py [1|2|3]
import sys

from sympy import (Poly, Rational, cancel, expand, factor_list, fraction, gcd,  # noqa: E402
                   groebner, solve, symbols, together)

x, y = symbols("x y")
c = symbols("c_det")
failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def jac2(P, Q):
    return expand(P.diff(x) * Q.diff(y) - P.diff(y) * Q.diff(x))


# Deterministic Keller-map library: compositions of elementary and affine unimodular maps.
COEFS = [Rational(1), Rational(-2), Rational(1, 2), Rational(3), Rational(-1, 3), Rational(2)]


def library():
    maps = []
    specs = [
        [("ey", [0, 2]), ("ex", [1, 3])],
        [("ex", [2]), ("ey", [0, 0, 1]), ("aff", None)],
        [("ey", [1, 0, 2]), ("ex", [0, 3]), ("ey", [2])],
        [("aff", None), ("ex", [0, 0, 4]), ("ey", [1, 2])],
        [("ey", [0, 5]), ("ex", [3, 0, 1]), ("aff", None), ("ey", [0, 0, 0, 2])],
        [("ex", [0, 1, 0, 2]), ("ey", [4])],
        [("ey", [0, 0, 3]), ("ex", [0, 2]), ("ey", [1, 1])],
        [("ex", [5, 1]), ("ey", [0, 2, 2]), ("ex", [0, 0, 1])],
    ]
    ci = 0
    for spec in specs:
        P, Q = x, y
        for kind, dat in spec:
            if kind == "ex":     # x -> x + p(y)
                pol = sum(Rational(d) * y**i for i, d in enumerate(dat))
                P, Q = P.subs({x: x + pol, y: y}, simultaneous=True), Q.subs({x: x + pol, y: y}, simultaneous=True)
            elif kind == "ey":   # y -> y + q(x)
                pol = sum(Rational(d) * x**i for i, d in enumerate(dat))
                P, Q = P.subs({y: y + pol}, simultaneous=True), Q.subs({y: y + pol}, simultaneous=True)
            else:                # unimodular affine
                a1, a2 = COEFS[ci % 6], COEFS[(ci + 1) % 6]
                ci += 2
                Pn = a1 * x + a2 * y + 1
                Qn = ((a1 * a2 - 1) / a2) * x + a2 * y if a2 != 0 else x
                # ensure det 1: use [[a1, a2], [b1, b2]] with a1 b2 - a2 b1 = 1
                b2 = Rational(1)
                b1 = (a1 * b2 - 1) / a2
                Pn = a1 * x + a2 * y
                Qn = b1 * x + b2 * y + 2
                P, Q = P.subs({x: Pn, y: Qn}, simultaneous=True), Q.subs({x: Pn, y: Qn}, simultaneous=True)
        maps.append((expand(P), expand(Q)))
    return maps


def omega_top(expr, w1, w2):
    p = Poly(expand(expr), x, y)
    dmax = max(w1 * i + w2 * j for (i, j), _ in p.terms())
    return expand(sum(co * x**i * y**j for (i, j), co in p.terms() if w1 * i + w2 * j == dmax)), dmax


def sqf_radical(expr):
    """Product of distinct irreducible factors (content dropped)."""
    _, facs = factor_list(expand(expr), x, y)
    out = Rational(1)
    for f, _ in facs:
        out *= f
    return expand(out)


def part1():
    print("=" * 76)
    print("Part 1: dependence + common-form structure at the top ray (library)")
    print("=" * 76)
    lib = library()
    nontrivial = 0
    for i, (P, Q) in enumerate(lib):
        J = jac2(P, Q)
        okK = J.is_number and J != 0
        m = Poly(P, x, y).total_degree()
        n = Poly(Q, x, y).total_degree()
        check(f"map {i}: Keller (det = {J}), degrees ({m}, {n})", bool(okK))
        if m + n <= 2:
            continue
        Pt, _ = omega_top(P, 1, 1)
        Qt, _ = omega_top(Q, 1, 1)
        dep = jac2(Pt, Qt) == 0
        radP, radQ = sqf_radical(Pt), sqf_radical(Qt)
        ratio = cancel(radP / radQ)
        common = ratio.is_number and ratio != 0
        nontrivial += 1
        check(f"map {i}: J(P_+, Q_+) == 0 and common radical form", dep and bool(common),
              f"radical ratio = {ratio}")
    check("Part 1 scanned nontrivially", nontrivial >= 6, f"nontrivial = {nontrivial}")


def part2():
    print("=" * 76)
    print("Part 2: ray sweep: the local model at every sampled ray (library)")
    print("=" * 76)
    RAYS = [(1, 1), (2, 1), (1, 2), (3, 1), (1, 3), (3, 2), (2, 3)]
    lib = library()
    bad = []
    checked = 0
    for i, (P, Q) in enumerate(lib):
        for (w1, w2) in RAYS:
            Pt, dP = omega_top(P, w1, w2)
            Qt, dQ = omega_top(Q, w1, w2)
            Jt = jac2(Pt, Qt)
            if dP + dQ - w1 - w2 > 0:
                ok = Jt == 0
                if ok:
                    ratio = cancel(sqf_radical(Pt) / sqf_radical(Qt))
                    ok = ratio.is_number and ratio != 0
                if not ok:
                    bad.append((i, w1, w2))
            checked += 1
    print(f"  (map, ray) pairs checked: {checked}")
    check("every positive-degree top pair is dependent with a common radical form", not bad,
          str(bad)[:120])


def part3():
    print("=" * 76)
    print("Part 3: exhaustive small-degree JC(2) (direct exact solves)")
    print("=" * 76)
    tnz = symbols("tnz")
    SAMP = [Rational(1), Rational(-2), Rational(1, 3), Rational(3, 2), Rational(-1, 5),
            Rational(0), Rational(2)]
    # Gauge (WLOG, documented): the linear part of a Keller map is invertible, so composing
    # with affine automorphisms on both sides normalizes F = (x + higher, y + higher), c = 1.
    import os
    pairs = {"22": (2, 2), "23": (2, 3), "33": (3, 3)}
    sel = os.environ.get("P3_PAIR", "22")
    for (m, n) in [pairs[sel]]:
        monsrange = lambda lo, d: [x**i * y**j for i in range(d + 1) for j in range(d + 1 - i)
                                   if i + j >= lo]
        MP = monsrange(2, m)
        MQ = monsrange(2, n)
        A = symbols(f"a{m}{n}_0:{len(MP)}")
        B = symbols(f"b{m}{n}_0:{len(MQ)}")
        P = x + sum(co * mo for co, mo in zip(A, MP))
        Q = y + sum(co * mo for co, mo in zip(B, MQ))
        eqs = Poly(expand(jac2(P, Q) - 1), x, y).coeffs()
        sols = solve([e for e in eqs if e != 0], list(A) + list(B), dict=True)
        print(f"  ({m},{n}): Keller branches: {len(sols)}")
        multi = []
        inst_count = 0
        for sol in sols:
            frees = sorted({fs for e in sol.values() for fs in e.free_symbols} - {tnz, c}, key=str)
            for shift in range(3):
                inst = {fs: SAMP[(k + shift) % len(SAMP)] for k, fs in enumerate(frees)}
                from sympy import zoo, nan, oo
                Pi = cancel(P.subs(sol).subs(inst))
                Qi = cancel(Q.subs(sol).subs(inst))
                if any(e.has(zoo) or e.has(nan) or e.has(oo) or e.has(tnz) or e.has(c)
                       for e in (Pi, Qi)):
                    continue
                Ji = jac2(Pi, Qi)
                if not Ji.is_number or Ji == 0:
                    continue
                inst_count += 1
                x0, y0 = Rational(2, 3), Rational(-1, 2)
                tgt = [Pi.subs({x: x0, y: y0}), Qi.subs({x: x0, y: y0})]
                gb = groebner([expand(Pi - tgt[0]), expand(Qi - tgt[1])], x, y, order="lex")
                if gb.exprs == [1]:
                    nsol = 0
                else:
                    uni = [g for g in gb.exprs if g.free_symbols <= {y}]
                    nsol = Poly(uni[-1], y).degree() if uni else -1
                if nsol > 1 or nsol == -1:
                    multi.append((Pi, Qi, nsol))
        print(f"  ({m},{n}): instances fiber-tested: {inst_count}")
        check(f"({m},{n}): scan non-vacuous", inst_count > 0)
        check(f"({m},{n}): every Keller instance has in-image fiber <= 1 (JC(2) holds here)",
              not multi, str(multi)[:160])


PARTS = {"1": part1, "2": part2, "3": part3}
todo = sys.argv[1:] if len(sys.argv) > 1 else ["1", "2", "3"]
for p_ in todo:
    PARTS[p_]()
    print()
if failures:
    print(f"RESULT: {len(failures)} FAILED: {failures}")
    sys.exit(1)
print("RESULT: ALL CHECKS PASS.")
