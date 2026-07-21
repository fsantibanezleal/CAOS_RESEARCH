# EXP-025: staged certificates at (4,6); the (4, <= 10) window. CPU-only, sympy over QQ.
# Run: .\.venv\Scripts\python.exe ...\EXP-025-staged-certificates\run.py [A [slice...]|B]
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "code"))

from jclib.keller2lib import jac2, x, y  # noqa: E402
from sympy import Matrix, Poly, cancel, expand, factor, gcd, lcm, symbols  # noqa: E402

failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def mons(dmin, dmax):
    return [x**i * y**(d - i) for d in range(dmin, dmax + 1) for i in range(d + 1)]


def system(Pexpr, MQ, B):
    Q0 = y + sum(b * m for b, m in zip(B, MQ))
    eqs = [e for e in Poly(expand(jac2(Pexpr, Q0) - 1), x, y).coeffs() if e != 0]
    M = Matrix([[expand(e.diff(b)) for b in B] for e in eqs])
    rhs = Matrix([-expand(e.subs({b: 0 for b in B})) for e in eqs])
    return M, rhs


def pairings(Pexpr, MQ, B, tag):
    """Cleared left-null certificate pairings (sound at every parameter point)."""
    t0 = time.time()
    M, rhs = system(Pexpr, MQ, B)
    ns = M.T.nullspace()
    fs = []
    for c in ns:
        den = lcm([cancel(e).as_numer_denom()[1] for e in c])
        cc = Matrix([expand(cancel(e * den)) for e in c])
        assert all(expand(v) == 0 for v in (cc.T * M)), "cleared vector not left-null"
        f = expand((cc.T * rhs)[0, 0])
        if f != 0:
            fs.append(f)
    print(f"  {tag}: {M.rows} eqs, {M.cols} unknowns, {len(ns)} null vectors, "
          f"{len(fs)} nonzero pairings, {time.time() - t0:.1f} s")
    return fs


def gcd_all(fs):
    g = fs[0]
    for f in fs[1:]:
        g = gcd(g, f)
    return factor(g)


def pure_a_power(g, a, others):
    p = Poly(expand(g), a, *others)
    ms = p.monoms()
    return len(ms) == 1 and all(all(m[i] == 0 for i in range(1, 1 + len(others)))
                                for m in ms)


SLICES = {
    "p20": x**2, "p11": x * y, "p02": y**2,
    "p30": x**3, "p21": x**2 * y, "p12": x * y**2, "p03": y**3,
}


def partA(selected=None):
    print("=" * 76)
    print("Part A: two-parameter slice certificates at (4, <= 6)")
    print("=" * 76)
    a, s = symbols("a_ s_")
    MQ = mons(2, 6)
    B = symbols(f"B0:{len(MQ)}")
    names = selected or list(SLICES)
    allok = True
    for nm in names:
        P = x + s * SLICES[nm] + a * (x * y) ** 2
        fs = pairings(P, MQ, B, f"A[{nm}]")
        if not fs:
            allok = False
            print(f"  A[{nm}]: NO nonzero pairings (inconclusive)")
            continue
        g = gcd_all(fs)
        ok = pure_a_power(g, a, (s,))
        print(f"  A[{nm}]: gcd = {g}  -> {'ALL (a != 0, s) empty' if ok else 'S-DEPENDENT'}")
        if not ok:
            # Union analysis: the unresolved locus is the COMMON zero set of the pairings
            # (with a inverted). If it lies inside {s = 0}, then EXP-024's pure-slice
            # certificate (-8 a^2, all a != 0) covers it and the slice is empty by union.
            from sympy import groebner
            t = symbols("t_r")
            gb = groebner([expand(f) for f in fs] + [a * t - 1], a, s, t, order="lex")
            inside = False
            for k in range(1, 9):
                if expand(gb.reduce(s**k)[1]) == 0:
                    print(f"  A[{nm}]: s^{k} lies in the ideal: unresolved locus is inside "
                          f"{{s = 0, a != 0}}, which EXP-024 emptied. Slice covered by union.")
                    inside = True
                    break
            if not inside:
                print(f"  A[{nm}]: unresolved locus NOT inside {{s = 0}}: candidate stratum")
            ok = inside
        allok &= ok
    check("A: every run slice certified empty for ALL (a != 0, s arbitrary)", allok,
          f"slices: {', '.join(names)}")


def partB():
    print("=" * 76)
    print("Part B: the pure-slice (4, <= 10) window, all a != 0")
    print("=" * 76)
    a = symbols("a_")
    MQ = mons(2, 10)
    B = symbols(f"B0:{len(MQ)}")
    fs = pairings(x + a * (x * y) ** 2, MQ, B, "B")
    ok = False
    if fs:
        g = gcd_all(fs)
        print(f"  gcd of pairings: {g}")
        ok = pure_a_power(g, a, ())
    check("B: NO Keller partner of degree <= 10 for ANY a != 0 (the (4,10) rung dies on "
          "the pure slice)", ok)


def partC():
    print("=" * 76)
    print("Part C: wider pure-slice windows (kill the (4,14) and (4,18) rungs)")
    print("=" * 76)
    a = symbols("a_")
    allok = True
    for dmax in (14, 18):
        MQ = mons(2, dmax)
        B = symbols(f"B0:{len(MQ)}")
        fs = pairings(x + a * (x * y) ** 2, MQ, B, f"C[<= {dmax}]")
        ok = False
        if fs:
            g = gcd_all(fs)
            print(f"  C[<= {dmax}]: gcd = {g}")
            ok = pure_a_power(g, a, ())
        check(f"C: NO Keller partner of degree <= {dmax} for ANY a != 0", ok)
        allok &= ok


def partD(selected=None):
    print("=" * 76)
    print("Part D: three-parameter slice certificates at (4, <= 6) (pairs of lower coeffs)")
    print("=" * 76)
    from itertools import combinations
    from sympy import groebner
    a, s, u = symbols("a_ s_ u_")
    MQ = mons(2, 6)
    B = symbols(f"B0:{len(MQ)}")
    names = selected or [f"{m}+{n}" for m, n in combinations(SLICES, 2)]
    allok = True
    for nm in names:
        m1, m2 = nm.split("+")
        P = x + s * SLICES[m1] + u * SLICES[m2] + a * (x * y) ** 2
        fs = pairings(P, MQ, B, f"D[{nm}]")
        if not fs:
            allok = False
            print(f"  D[{nm}]: NO nonzero pairings (inconclusive)")
            continue
        g = gcd_all(fs)
        ok = pure_a_power(g, a, (s, u))
        if ok:
            print(f"  D[{nm}]: gcd = {g}  -> ALL (a != 0, s, u) empty")
        else:
            # Union analysis: unresolved locus = common zeros with a inverted; check it
            # lies inside {s = 0} u {u = 0}, i.e. s*u is nilpotent on it: each point then
            # belongs to a 2-parameter slice already certified in part A (or EXP-024).
            t = symbols("t_r")
            gb = groebner([expand(f) for f in fs] + [a * t - 1], a, s, u, t, order="lex")
            inside = False
            for k in range(1, 9):
                if expand(gb.reduce((s * u) ** k)[1]) == 0:
                    print(f"  D[{nm}]: gcd = {g}; (s*u)^{k} in the ideal: unresolved locus "
                          f"inside the union of certified 2-param slices. Covered.")
                    inside = True
                    break
            if not inside:
                print(f"  D[{nm}]: gcd = {g}; locus NOT inside the slice union: candidate")
            ok = inside
        allok &= ok
    check("D: every run pair-slice certified empty for ALL (a != 0, s, u arbitrary)",
          allok, f"{len(names)} pair slices")


def partE(selected=None):
    print("=" * 76)
    print("Part E: four-parameter slice certificates (triples of lower coeffs)")
    print("=" * 76)
    from itertools import combinations
    from sympy import groebner
    a, s, u, w = symbols("a_ s_ u_ w_")
    MQ = mons(2, 6)
    B = symbols(f"B0:{len(MQ)}")
    names = selected or [f"{m}+{n}+{q}" for m, n, q in combinations(SLICES, 3)]
    allok = True
    done = 0
    for nm in names:
        m1, m2, m3 = nm.split("+")
        P = (x + s * SLICES[m1] + u * SLICES[m2] + w * SLICES[m3] + a * (x * y) ** 2)
        fs = pairings(P, MQ, B, f"E[{nm}]")
        if not fs:
            allok = False
            print(f"  E[{nm}]: NO nonzero pairings (inconclusive)")
            continue
        g = gcd_all(fs)
        ok = pure_a_power(g, a, (s, u, w))
        if ok:
            print(f"  E[{nm}]: gcd = {g}  -> ALL (a != 0, s, u, w) empty")
        else:
            t = symbols("t_r")
            gb = groebner([expand(f) for f in fs] + [a * t - 1], a, s, u, w, t,
                          order="lex")
            inside = False
            for k in range(1, 9):
                if expand(gb.reduce((s * u * w) ** k)[1]) == 0:
                    print(f"  E[{nm}]: gcd = {g}; (s*u*w)^{k} in the ideal: locus inside "
                          f"the union of certified pair slices. Covered.")
                    inside = True
                    break
            if not inside:
                print(f"  E[{nm}]: gcd = {g}; locus NOT inside the pair-slice union: "
                      f"candidate")
            ok = inside
        allok &= ok
        done += 1
        print(f"  E progress: {done}/{len(names)}")
    check("E: every run triple-slice certified empty for ALL (a != 0, s, u, w)", allok,
          f"{done}/{len(names)} triple slices completed")


def partF():
    print("=" * 76)
    print("Part F: probe the E-candidate locus {4 a s = u^2} on p20+p21+p03")
    print("=" * 76)
    # Structure first: on the locus, s x^2 + u x^2 y + a x^2 y^2 = a x^2 (y + u/(2a))^2,
    # so P is the TRANSLATION conjugate (y -> y + c) of a pure-slice-plus-tail point. The
    # slice family does not contain those translated points, so the pairing degeneration is
    # expected; the question is whether the system is ACTUALLY consistent there.
    from sympy import Rational, linsolve
    a, w = symbols("a_ w_")
    MQ = mons(2, 6)
    B = symbols(f"B0:{len(MQ)}")
    # (i) direct consistency at numeric locus points (several w), via plain linsolve.
    allempty = True
    for (av, uv, sv) in ((1, 2, 1), (1, 4, 4), (Rational(1, 2), 1, Rational(1, 2))):
        assert 4 * av * sv == uv**2
        for wv in (1, -2, Rational(1, 3)):
            P = (x + sv * x**2 + uv * x**2 * y + wv * y**3 + av * (x * y) ** 2)
            Q0 = y + sum(b * m for b, m in zip(B, MQ))
            eqs = [e for e in Poly(expand(jac2(P, Q0) - 1), x, y).coeffs() if e != 0]
            ls = linsolve(eqs, list(B))
            tag = "INCONSISTENT" if not ls else "CONSISTENT (escalate!)"
            print(f"  F locus (a={av}, u={uv}, s={sv}, w={wv}): {tag}")
            allempty &= not ls
    check("F(i): the locus is empty at every probed numeric point", allempty)
    # (ii) certificates over QQ(w) at the locus point (a, u, s) = (1, 2, 1): all w at once.
    P = x + x**2 + 2 * x**2 * y + w * y**3 + (x * y) ** 2
    fs = pairings(P, MQ, B, "F[w symbolic]")
    ok = False
    if fs:
        g = gcd_all(fs)
        print(f"  F: gcd over QQ(w) = {g}")
        ok = pure_a_power(g, w, ()) or (Poly(expand(g), w).total_degree() == 0
                                        and expand(g) != 0)
    check("F(ii): certificate over QQ(w): the locus point family is empty for ALL w", ok)
    # (iii) the WHOLE locus at once: the polynomial parametrization a = al^2, u = 2 al be,
    # s = be^2 covers {4 a s = u^2, a != 0} (al != 0); certificates over QQ(al, be, w).
    al, be = symbols("al_ be_")
    P = (x + be**2 * x**2 + 2 * al * be * x**2 * y + w * y**3
         + al**2 * (x * y) ** 2)
    fs = pairings(P, MQ, B, "F[locus, 3-param]")
    ok = False
    if fs:
        g = gcd_all(fs)
        print(f"  F: gcd over QQ(al, be, w) = {factor(g)}")
        ok = pure_a_power(g, al, (be, w))
    check("F(iii): the ENTIRE locus is empty for all (al != 0, be, w): part E closes "
          "completely", ok)


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        partA()
        print()
        partB()
    elif args[0] == "A":
        partA(args[1:] or None)
    elif args[0] == "B":
        partB()
    elif args[0] == "C":
        partC()
    elif args[0] == "D":
        partD(args[1:] or None)
    elif args[0] == "E":
        partE(args[1:] or None)
    elif args[0] == "F":
        partF()
    if failures:
        print(f"RESULT: {len(failures)} FAILED: {failures}")
        sys.exit(1)
    print("RESULT: ALL CHECKS PASS.")
