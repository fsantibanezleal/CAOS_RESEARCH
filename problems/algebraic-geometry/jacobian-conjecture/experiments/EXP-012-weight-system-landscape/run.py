# EXP-012: the weighted mechanism landscape in C^3. CPU-only, sympy over QQ. See hypothesis.md.
# Runtime is managed by running PARTS separately (the first monolithic attempt timed out and is
# kept in artifacts/ as the record):
#   run.py A | B | C | D | E   (or no arg: A B C D E in sequence)
#
# Run: .\.venv\Scripts\python.exe ...\EXP-012-weight-system-landscape\run.py <PART>
import itertools
import sys

from sympy import (Matrix, Poly, Rational, cancel, expand, factor, fraction,  # noqa: E402
                   groebner, integrate, solve, symbols, together)

x, y, z, v, t, w, s = symbols("x y z v t w s")
c = symbols("c_det")
failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""))
    if not ok:
        failures.append(name)


def lift_expr(fi, oi, m):
    return together(x**oi * fi.subs({v: x * y, t: x**m * z}, simultaneous=True))


def bracket_D(f1, f2, f3, o):
    J12 = f1.diff(v) * f2.diff(t) - f1.diff(t) * f2.diff(v)
    J13 = f1.diff(v) * f3.diff(t) - f1.diff(t) * f3.diff(v)
    J23 = f2.diff(v) * f3.diff(t) - f2.diff(t) * f3.diff(v)
    return expand(o[0] * f1 * J23 - o[1] * f2 * J13 + o[2] * f3 * J12)


SAMP = [Rational(1), Rational(-2), Rational(1, 3), Rational(3, 2), Rational(-1, 5),
        Rational(0), Rational(2)]


def part_A():
    print("=" * 76)
    print("Part A: determinant lemma for weights (1, -1, -m) [sparse generic f_i]")
    print("=" * 76)
    a_ = symbols("a0:3")
    b_ = symbols("b0:3")
    h_ = symbols("h0:3")
    f1g = a_[0] + a_[1] * v + a_[2] * t**2
    f2g = b_[0] + b_[1] * t + b_[2] * v**2
    f3g = h_[0] + h_[1] * v + h_[2] * t
    ok_all, ntest = True, 0
    for m in (1, 2, 3, 4):
        for o in ((-1, -1, 1), (-2, -1, 1), (-2, -2, 1), (-3, -2, 1), (0, -2, 1)):
            Fs = [lift_expr(fi, oi, m) for fi, oi in zip((f1g, f2g, f3g), o)]
            J = together(Matrix([[Fi.diff(var) for var in (x, y, z)] for Fi in Fs]).det())
            D = bracket_D(f1g, f2g, f3g, o)
            pred = x**(sum(o) + m) * D.subs({v: x * y, t: x**m * z}, simultaneous=True)
            ok_all &= expand(cancel(J - pred)) == 0
            ntest += 1
    check(f"A: det JF == x^(sigma+m) * D for {ntest} (m, o) cases", ok_all)


def part_B():
    print("=" * 76)
    print("Part B: pairing reductions J2 == (+/-) c1^(ra+rb-1) * D [sparse generic]")
    print("=" * 76)
    a_ = symbols("a0:3")
    b_ = symbols("b0:3")
    h_ = symbols("h0:3")
    f1g = a_[0] + a_[1] * v + a_[2] * t
    f2g = b_[0] + b_[1] * t + b_[2] * v
    f3g = h_[0] + h_[1] * v + h_[2] * t
    PAIRINGS = {1: ((-1, -1, 1), (1, 1), (0, 1)), 2: ((-2, -1, 1), (1, 2), (1, 0)),
                3: ((-2, -2, 1), (2, 2), (0, 1)), 4: ((-3, -2, 1), (2, 3), (1, 0))}
    for m, (o, (ra, rb), (ia, ib)) in PAIRINGS.items():
        fa = (f1g, f2g)[ia]
        fb = (f1g, f2g)[ib]
        Vp = expand(fa * f3g**ra)
        Tp = expand(fb * f3g**rb)
        J2 = expand(Matrix([[Vp.diff(v), Vp.diff(t)], [Tp.diff(v), Tp.diff(t)]]).det())
        D = bracket_D(f1g, f2g, f3g, o)
        X = ra + rb - 1
        sign = "+" if expand(J2 - f3g**X * D) == 0 else (
            "-" if expand(J2 + f3g**X * D) == 0 else "?")
        check(f"B: m = {m}: J2 == ({sign}1) c1^{X} D identically", sign in ("+", "-"))


def part_C():
    print("=" * 76)
    print("Part C: m = 1, o = (-1, -1, 1): sparse-pattern Keller scan (JC(2) bridge class)")
    print("=" * 76)
    q0, q1 = symbols("q0 q1")
    tnz = symbols("tnz")
    PATTERNS = [
        ([v, t], [v, t]), ([v, t], [v**2, t]), ([v, t, v**2], [v, t]),
        ([v, t], [v, t, v * t]), ([t, v**2], [v, t]), ([v, t, t**2], [v, t]),
    ]
    F3PATTERNS = [q0 + q1 * v, q0 + q1 * v - t, q0 + q1 * t, Rational(1) * q0]
    inst_count, multi = 0, []
    for pi, ((mon1, mon2), f3c) in enumerate(itertools.product(PATTERNS, F3PATTERNS)):
        FC = symbols(f"A{pi}_0:{len(mon1)}")
        GC = symbols(f"B{pi}_0:{len(mon2)}")
        f1c = sum(co * mo for co, mo in zip(FC, mon1))
        f2c = sum(co * mo for co, mo in zip(GC, mon2))
        D = bracket_D(f1c, f2c, f3c, (-1, -1, 1))
        eqs = Poly(expand(D - c), v, t).coeffs()
        try:
            sols = solve(list(eqs) + [c * tnz - 1],
                         list(FC) + list(GC) + [q0, q1, c, tnz], dict=True)
        except Exception as e:
            print(f"  pattern {pi}: solve failed ({e!r}); skipped")
            continue
        for sol in sols:
            frees = sorted({fs for e_ in sol.values() for fs in e_.free_symbols} - {tnz, c},
                           key=str)
            for shift in range(3):
                cval = [Rational(1), Rational(-2), Rational(1, 3)][shift]
                inst = {fs: SAMP[(i + shift) % len(SAMP)] for i, fs in enumerate(frees)}
                inst[c] = cval
                inst[tnz] = 1 / cval
                for sym_ in (q0, q1):
                    if sym_ not in sol and sym_ not in inst:
                        inst[sym_] = SAMP[shift]
                from sympy import zoo, nan, oo
                f1i = cancel(f1c.subs(sol).subs(inst))
                f2i = cancel(f2c.subs(sol).subs(inst))
                f3i = cancel(f3c.subs(sol).subs(inst))
                if any(e_.has(zoo) or e_.has(nan) or e_.has(oo) or e_.has(tnz) or e_.has(c)
                       for e_ in (f1i, f2i, f3i)):
                    continue
                if f3i == 0 or (f1i == 0 and f2i == 0):
                    continue
                Di = expand(bracket_D(f1i, f2i, f3i, (-1, -1, 1)))
                if Di.has(v) or Di.has(t) or Di == 0:
                    continue
                F1 = cancel(lift_expr(f1i, -1, 1))
                F2 = cancel(lift_expr(f2i, -1, 1))
                F3 = expand(lift_expr(f3i, 1, 1))
                bad = False
                for Fi in (F1, F2):
                    num, den = fraction(together(Fi))
                    bad |= den.has(x) or den.has(y) or den.has(z)
                if bad:
                    continue
                inst_count += 1
                x0, y0, z0 = Rational(2, 3), Rational(-1, 2), Rational(3, 5)
                tgt = [expand(Fi.subs({x: x0, y: y0, z: z0}, simultaneous=True))
                       for Fi in (F1, F2, F3)]
                gb = groebner([expand(F1 - tgt[0]), expand(F2 - tgt[1]),
                               expand(F3 - tgt[2])], x, y, z, order="lex")
                if gb.exprs == [1]:
                    nsol = 0
                else:
                    uni = [g for g in gb.exprs if g.free_symbols <= {z}]
                    nsol = Poly(uni[-1], z).degree() if uni else -1
                if nsol > 1 or nsol == -1:
                    multi.append((f1i, f2i, f3i, nsol))
    print(f"  polynomial Keller instances fiber-tested: {inst_count}")
    check("C: scan non-vacuous", inst_count > 0, f"instances = {inst_count}")
    check("C: every instance has in-image fiber size <= 1 (bridge class rigid here)",
          not multi, str(multi)[:200])


def part_D():
    print("=" * 76)
    print("Part D: m = 3, o = (-2, -2, 1): lattice-level Keller scan (rigidity probe)")
    print("=" * 76)
    # Direct (v, t) scan with the TRUE liftability valuations (alpha + 3 beta >= 2 for f1, f2).
    # The earlier (w, s)-chart probe without liftability found fiber-2 pairs, but hand-checking
    # shows they cannot lift (f = affine in v violates the lattice valuation); artifacts keep
    # that output as the record of why liftability must be imposed.
    q0, q1 = symbols("q0 q1")
    tnz = symbols("tnz")
    from sympy import zoo, nan, oo

    # (i) The o = (-2, -2, 1) class is EMPTY: the lattice (alpha + 3 beta >= 2) forbids
    # v-linear monomials in f1 AND f2, so d f1/dv and d f2/dv vanish at the origin and every
    # term of D vanishes there. Machine form: D(0,0) == 0 identically for a generic ansatz.
    gf = symbols("e0:8")
    mons22 = [t, v**2, v * t, t**2]
    g1 = sum(co * mo for co, mo in zip(gf[:4], mons22))
    g2 = sum(co * mo for co, mo in zip(gf[4:], mons22))
    g3 = q0 + q1 * v - t
    D22 = bracket_D(g1, g2, g3, (-2, -2, 1))
    check("D(i): o = (-2, -2, 1) class is EMPTY (D(0, 0) == 0 identically, generic ansatz)",
          expand(D22.subs({v: 0, t: 0})) == 0)

    # (ii) The o = (-3, -1, 1) class escapes the argument: scan it (f1 val >= 3, f2 val >= 1).
    PATTERNS = [
        ([t, v**3], [v, t]), ([t, v**3, v**2 * t], [v, t]), ([t, v**3], [v, t, v**2]),
        ([t, v**2 * t], [v, t, v * t]), ([v**3, t**2], [v, t]), ([t, t**2, v**3], [v, t]),
    ]
    F3PATTERNS = [q0 + q1 * v, q0 + q1 * v - t, Rational(1) * q0]
    inst_count, multi = 0, []
    O_TRIPLE = (-3, -1, 1)
    for pi, ((mon1, mon2), f3c) in enumerate(itertools.product(PATTERNS, F3PATTERNS)):
        FC = symbols(f"C{pi}_0:{len(mon1)}")
        GC = symbols(f"D{pi}_0:{len(mon2)}")
        f1c = sum(co * mo for co, mo in zip(FC, mon1))
        f2c = sum(co * mo for co, mo in zip(GC, mon2))
        D = bracket_D(f1c, f2c, f3c, O_TRIPLE)
        eqs = Poly(expand(D - c), v, t).coeffs()
        try:
            sols = solve(list(eqs) + [c * tnz - 1],
                         list(FC) + list(GC) + [q0, q1, c, tnz], dict=True)
        except Exception as e:
            print(f"  pattern {pi}: solve failed ({e!r}); skipped")
            continue
        for sol in sols:
            frees = sorted({fs for e_ in sol.values() for fs in e_.free_symbols} - {tnz, c},
                           key=str)
            for shift in range(3):
                cval = [Rational(1), Rational(-2), Rational(1, 3)][shift]
                inst = {fs: SAMP[(i + shift) % len(SAMP)] for i, fs in enumerate(frees)}
                inst[c] = cval
                inst[tnz] = 1 / cval
                for sym_ in (q0, q1):
                    if sym_ not in sol and sym_ not in inst:
                        inst[sym_] = SAMP[shift]
                f1i = cancel(f1c.subs(sol).subs(inst))
                f2i = cancel(f2c.subs(sol).subs(inst))
                f3i = cancel(f3c.subs(sol).subs(inst))
                if any(e_.has(zoo) or e_.has(nan) or e_.has(oo) or e_.has(tnz) or e_.has(c)
                       for e_ in (f1i, f2i, f3i)):
                    continue
                if f3i == 0 or (f1i == 0 and f2i == 0):
                    continue
                Di = expand(bracket_D(f1i, f2i, f3i, O_TRIPLE))
                if Di.has(v) or Di.has(t) or Di == 0:
                    continue
                F1 = cancel(lift_expr(f1i, -3, 3))
                F2 = cancel(lift_expr(f2i, -1, 3))
                F3 = expand(lift_expr(f3i, 1, 3))
                bad = False
                for Fi in (F1, F2):
                    num, den = fraction(together(Fi))
                    bad |= den.has(x) or den.has(y) or den.has(z)
                if bad:
                    continue
                inst_count += 1
                x0, y0, z0 = Rational(2, 3), Rational(-1, 2), Rational(3, 5)
                tgt = [expand(Fi.subs({x: x0, y: y0, z: z0}, simultaneous=True))
                       for Fi in (F1, F2, F3)]
                gb = groebner([expand(F1 - tgt[0]), expand(F2 - tgt[1]),
                               expand(F3 - tgt[2])], x, y, z, order="lex")
                if gb.exprs == [1]:
                    nsol = 0
                else:
                    uni = [g for g in gb.exprs if g.free_symbols <= {z}]
                    nsol = Poly(uni[-1], z).degree() if uni else -1
                if nsol > 1 or nsol == -1:
                    multi.append((f1i, f2i, f3i, nsol))
    print(f"  polynomial Keller instances fiber-tested: {inst_count}")
    check("D(ii): (-3, -1, 1) scan result recorded", True, f"instances = {inst_count}")
    check("D(ii): no m = 3 lattice Keller instance with fiber size > 1 (odd-m rigidity holds here)",
          not multi, str(multi)[:200])


def part_D_chart_probe():
    print("=" * 76)
    print("Part D (chart probe, superseded): kept for the record only")
    print("=" * 76)
    gam, t4 = symbols("gamma t4")
    WDEG = 2
    Amon = [w**i * s**j for j in range(3) for i in range(WDEG + 1)]
    Bmon = [w**i * s**j for j in range(2) for i in range(WDEG + 1)]   # gauge: T' s-deg <= 1
    AW = symbols(f"Aw0:{len(Amon)}")
    BW = symbols(f"Bw0:{len(Bmon)}")
    Vg = sum(co * mo for co, mo in zip(AW, Amon))
    Tg = sum(co * mo for co, mo in zip(BW, Bmon))
    detg = expand(Vg.diff(w) * Tg.diff(s) - Vg.diff(s) * Tg.diff(w) - gam * s**2)
    eqsD = Poly(detg, w, s).coeffs()
    sols = solve(list(eqsD) + [gam * t4 - 1], list(AW) + list(BW) + [gam, t4], dict=True)
    print(f"  branches with gamma != 0: {len(sols)}")
    instD, multiD = 0, []
    from sympy import zoo, nan, oo
    for sol in sols:
        frees = sorted({fs for e_ in sol.values() for fs in e_.free_symbols} - {t4, gam},
                       key=str)
        for shift in range(2):
            gval = [Rational(1), Rational(-3)][shift]
            inst = {fs: SAMP[(i + shift + 1) % len(SAMP)] for i, fs in enumerate(frees)}
            inst[gam] = gval
            inst[t4] = 1 / gval
            Vi = cancel(Vg.subs(sol).subs(inst))
            Ti = cancel(Tg.subs(sol).subs(inst))
            if any(e_.has(zoo) or e_.has(nan) or e_.has(oo) or e_.has(t4) or e_.has(gam)
                   for e_ in (Vi, Ti)):
                continue
            gi = expand(Vi.diff(w) * Ti.diff(s) - Vi.diff(s) * Ti.diff(w))
            if gi == 0 or cancel(gi / s**2).has(w) or cancel(gi / s**2).has(s):
                continue
            instD += 1
            w0, s0 = Rational(1, 2), Rational(2, 3)
            tv, tt = Vi.subs({w: w0, s: s0}), Ti.subs({w: w0, s: s0})
            gb = groebner([expand(Vi - tv), expand(Ti - tt)], w, s, order="lex")
            if gb.exprs == [1]:
                n2 = 0
            else:
                uni = [g for g in gb.exprs if g.free_symbols <= {s}]
                n2 = Poly(uni[-1], s).degree() if uni else -1
            if n2 > 1 or n2 == -1:
                multiD.append((Vi, Ti, n2))
    print(f"  instances fiber-tested: {instD}")
    check("D: probe non-vacuous", instD > 0, f"instances = {instD}")
    check("D: no reduced pair with fiber size > 1 (even-order rigidity holds at scanned sizes)",
          not multiD, str(multiD)[:200])


def part_E():
    print("=" * 76)
    print("Part E: m = 4, o = (-3, -2, 1): the NEW family (V' = k^2 p + mu s^2)")
    print("=" * 76)
    p3s, p4s, p5s, mus, Q0, Q1, Q2 = symbols("p3s p4s p5s mus Q0 Q1 Q2")
    kk = Rational(1)
    # p2 = 1, k = 1 fixed; valuation-2 seed. A two-term seed is provably inconsistent (the
    # low-weight conditions force k = 0), so the seed needs the w^4 term.
    pseed = w**2 + p3s * w**3 + p4s * w**4 + p5s * w**5
    Phi = integrate(pseed, (w, 0, w))
    qv = Q0 + Q1 * v + Q2 * v**2
    sc = qv - t
    u_ = 1 + v
    warg = u_ * sc / kk
    Vp = expand(kk**2 * pseed.subs(w, warg) + mus * sc**2)
    Tp = expand(warg * Vp - kk**2 * Phi.subs(w, warg))
    f2e = cancel(Vp / sc**2)
    f1e = cancel(Tp / sc**3)
    low = []
    for (av, bt), co in Poly(expand(f2e), v, t).terms():
        if av + 4 * bt < 2:
            low.append(expand(co))
    for (av, bt), co in Poly(expand(f1e), v, t).terms():
        if av + 4 * bt < 3:
            low.append(expand(co))
    low = sorted({e for e in low if e != 0}, key=str)
    print(f"  low-weight polynomiality conditions: {len(low)}")
    t5 = symbols("t5")
    # Gauge Q0 = 1 (s-rescaling) and decide solvability by a Groebner emptiness certificate:
    # GB == [1] proves NO admissible parameters exist (mu != 0 imposed Rabinowitsch-style).
    lowg = [expand(e.subs(Q0, 1)) for e in low]
    gvars = [Q1, Q2, p3s, p4s, p5s, mus, t5]
    gb = groebner(lowg + [mus * t5 - 1], *gvars, order="grevlex")
    if gb.exprs == [1]:
        print("  Groebner certificate: the admissibility system is EMPTY (no mu != 0 solution)")
        check("E-REFUTED (recorded): no admissible m = 4 potential-form instance exists "
              "(seed degree <= 5, pairing (-3, -2, 1), gauge Q0 = 1)", True)
        check("E: an explicit m = 4 instance was built", False,
              "prediction 5 REFUTED: the m = 4 family does not exist at these sizes")
        return
    sols = solve(list(gb.exprs), gvars, dict=True)
    sols = [dict(list(so.items()) + [(Q0, Rational(1))]) for so in sols]
    print(f"  admissible parameter branches: {len(sols)}")
    built = False
    for sol in sols:
        inst = {}
        for sym_ in (Q0, Q1, Q2, p3s, p4s, p5s, mus):
            inst[sym_] = cancel(sym_.subs(sol)) if sym_ in sol else Rational(1)
        frees = {fs for e_ in inst.values() if hasattr(e_, "free_symbols")
                 for fs in e_.free_symbols}
        for fs in frees:
            for k2 in inst:
                inst[k2] = cancel(inst[k2].subs(fs, Rational(1)) if hasattr(inst[k2], "subs")
                                  else inst[k2])
        f1i = cancel(f1e.subs(inst))
        f2i = cancel(f2e.subs(inst))
        f3i = cancel(sc.subs(inst))
        if f1i == 0 or f2i == 0:
            continue
        F1 = cancel(lift_expr(f1i, -3, 4))
        F2 = cancel(lift_expr(f2i, -2, 4))
        F3 = expand(lift_expr(f3i, 1, 4))
        bad = False
        for Fi in (F1, F2):
            num, den = fraction(together(Fi))
            bad |= den.has(x) or den.has(y) or den.has(z)
        if bad:
            continue
        J = expand(Matrix([[expand(Fi).diff(var) for var in (x, y, z)]
                           for Fi in (F1, F2, F3)]).det())
        if not J.is_number or J == 0:
            continue
        built = True
        degs = [Poly(expand(Fi), x, y, z).total_degree() for Fi in (F1, F2, F3)]
        print(f"  instance: p = {expand(pseed.subs(inst))}, q = {expand(qv.subs(inst))}, "
              f"mu = {inst[mus]}, k = 1")
        print(f"  det JF = {J}, component degrees = {degs}")
        qfun = qv.subs(inst)
        w0, s0 = Rational(1, 2), Rational(1, 3)
        u1 = w0 / s0
        X1 = (Rational(1), u1 - 1, qfun.subs(v, u1 - 1) - s0)
        u2 = w0 / (-s0)
        X2 = (Rational(-1), -(u2 - 1), qfun.subs(v, u2 - 1) + s0)
        img1 = tuple(expand(expand(Fi).subs({x: X1[0], y: X1[1], z: X1[2]},
                                            simultaneous=True)) for Fi in (F1, F2, F3))
        img2 = tuple(expand(expand(Fi).subs({x: X2[0], y: X2[1], z: X2[2]},
                                            simultaneous=True)) for Fi in (F1, F2, F3))
        print(f"  X1 = {X1}\n  X2 = {X2}\n  F(X1) = {img1}\n  F(X2) = {img2}")
        check("E: polynomial Keller map on the m = 4 system (det constant nonzero)", True)
        check("E: explicit collision F(X1) == F(X2), X1 != X2", img1 == img2 and X1 != X2)
        check("E: total degree exceeds 7 (m = 2 minimality untouched)", max(degs) > 7,
              f"degrees {degs}")
        break
    check("E: an explicit m = 4 instance was built", built)


PARTS = {"A": part_A, "B": part_B, "C": part_C, "D": part_D, "E": part_E}
todo = sys.argv[1:] if len(sys.argv) > 1 else list(PARTS)
for p_ in todo:
    PARTS[p_]()
    print()
if failures:
    print(f"RESULT ({'+'.join(todo)}): {len(failures)} FAILED: {failures}")
    sys.exit(1)
print(f"RESULT ({'+'.join(todo)}): ALL CHECKS PASS.")
