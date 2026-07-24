# EXP-077: the C13 fork decision. Exact integer / Fraction arithmetic.
# Decides whether GGHV22's (8,32) sibling discard extends to C13's (8,40) chain.
# No mod-p reduction here (the modfrac hard rule does not apply); the regression
# gate re-runs the SIBLING through the identical path and requires GGHV22's
# published decision (q_1 = 4, d_0 = 4, corner (8,4), excluded).
# Run: run.py
import sys
from fractions import Fraction
from math import gcd

failures = []


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {detail}" if detail else ""),
          flush=True)
    if not ok:
        failures.append(name)


def vrs(rho, sig, pt):
    """v_{rho,sigma}(a,b) = rho*a + sig*b (l = 1; a may be a Fraction)."""
    a, b = pt
    return rho * a + sig * b


# ---------------------------------------------------------------------------
# Shared chain tail (identical for the sibling and C13):
A1 = (Fraction(8), Fraction(28))
A2 = (Fraction(11, 4), Fraction(7))
M, N = 3, 2                      # (m,n)-pair
RHO1, SIG1 = 4, -1               # direction of the edge A1--A2
RHO0, SIG0 = 1, 0                # the max-x (vertical) direction


def q1_from_case_II(corner, rho, sig):
    """[GGV1, Prop 'Case II' + Thm 7.6(3)]: en_{rho,sig}(F_1) = mu (abar,bbar),
    (abar,bbar) primitive of the regular corner; v_{rho,sig}(en F_1) = rho+sig;
    q_1 = d / gcd(mu, d).  Returns (q1, en_F1, mu, d)."""
    a, b = corner
    ai, bi = int(a), int(b)               # corner is integral here
    d = gcd(ai, bi)
    abar, bbar = ai // d, bi // d         # primitive direction of the corner
    # mu (rho*abar + sig*bbar) = rho + sig  ->  mu = (rho+sig) / v_{rho,sig}(prim)
    denom = rho * abar + sig * bbar
    mu = Fraction(rho + sig, denom)
    en_F1 = (mu * abar, mu * bbar)
    # q_1 = denominator of (p_1/q_1) = (mu/d) in lowest terms
    ratio = Fraction(int(mu), d) if mu.denominator == 1 else Fraction(mu, d)
    q1 = ratio.denominator
    return q1, en_F1, mu, d


def d0_perfect_power_bound(A0, A1_shared):
    """l_{1,0}(P) = R^{m d_0}. The (1,0) leading form is the max-x edge; its
    bottom vertex st_{1,0}(P) = A1_shared. d_0 * st_{1,0}(R) = st_{1,0}(P) forces
    st_{1,0}(R) integral, so d_0 | gcd(coords of st_{1,0}(P)). The top vertex A0
    only bounds via its own gcd (a strictly weaker bound here). Returns
    (bound_from_bottom, bound_from_top, feasible_divisors)."""
    xb, yb = int(A1_shared[0]), int(A1_shared[1])   # bottom vertex (8,28)
    xt, yt = int(A0[0]), int(A0[1])                 # top vertex A0
    g_bottom = gcd(xb, yb)
    g_top = gcd(xt, yt)
    # a divisor d is feasible iff BOTH endpoints are m*d multiples on the A-scale,
    # i.e. d | gcd(bottom coords) and d | gcd(top coords) (perfect (m d)-power).
    gall = gcd(g_bottom, g_top)
    feasible = [d for d in range(1, gall + 1) if gall % d == 0]
    return g_bottom, g_top, feasible


def R_shape(A0, A1_shared, d0):
    """R with l_{1,0}(P) = R^{m d0}: x-deg = 8/d0, y-bottom = 28/d0,
    y-top = A0_y/d0.  Returns (xdeg, y_bottom, y_top, tail_degree)."""
    xt, yt = int(A0[0]), int(A0[1])
    xb, yb = int(A1_shared[0]), int(A1_shared[1])
    xdeg = Fraction(xb, d0)
    yb_R = Fraction(yb, d0)
    yt_R = Fraction(yt, d0)
    tail = yt_R - yb_R
    return xdeg, yb_R, yt_R, tail


def excluded_casos_imposibles(a, b):
    """[GGV2 = arXiv 1605.09430, Prop 'casos imposibles' (tex 1009) + remark
    (tex 1053)]: wp(n', n'-1) with n' >= 2 is NOT a possible last lower corner.
    Explicit excluded list in the remark: (2,1),(3,2),(6,3),(8,4)."""
    a, b = int(a), int(b)
    if not (a > b > 0):
        return False, "not of the form a>b>0"
    g = a - b                       # candidate wp
    if g <= 0 or b % g != 0:
        return False, f"(a-b)={g} does not divide b={b}"
    nprime_minus_1 = b // g
    nprime = nprime_minus_1 + 1
    if nprime < 2:
        return False, f"n'={nprime} < 2"
    wp = g
    ok = (a, b) == (wp * nprime, wp * (nprime - 1))
    return ok, f"= {wp}*({nprime},{nprime-1}), n'={nprime}>=2"


def run_chain(label, A0):
    print(f"\n---- chain {label}: A0 = "
          f"({int(A0[0])},{int(A0[1])}), A1 = (8,28), A2 = (11/4,7) ----",
          flush=True)
    out = {}
    # (a) direction (4,-1) well-defined from A1,A2
    ok_dir = vrs(RHO1, SIG1, A1) == vrs(RHO1, SIG1, A2) == 4
    check(f"{label}: v_{{4,-1}}(A1)=v_{{4,-1}}(A2)=4 (edge direction)", ok_dir,
          f"{vrs(RHO1,SIG1,A1)}, {vrs(RHO1,SIG1,A2)}")
    # A0 sits strictly below the (4,-1) leading edge -> not in the leading form
    vA0 = vrs(RHO1, SIG1, A0)
    check(f"{label}: v_{{4,-1}}(A0)={vA0} < 4 (A0 not in the (4,-1) leading form)",
          vA0 < 4, f"leading form = shared edge A1--A2")
    out["vA0_4m1"] = vA0
    # (b) q_1 via Case II (depends only on the shared corner A1)
    q1, en_F1, mu, d = q1_from_case_II(A1, RHO1, SIG1)
    check(f"{label}: q_1 = 4 (Case II: en(F_1)=mu*(2,7), mu=3, d=4)", q1 == 4,
          f"en(F_1)=({en_F1[0]},{en_F1[1]}), mu={mu}, d={d}, q_1={q1}")
    # cross-check the Thm 7.6(3) ratio en(F_1) = (p/q)(1/m)en(P), (1/m)en(P)=A1
    ratio = (Fraction(en_F1[0], A1[0]), Fraction(en_F1[1], A1[1]))
    ok_ratio = ratio[0] == ratio[1] == Fraction(3, 4) and ratio[0].denominator == 4
    check(f"{label}: en(F_1) = (3/4)(1/m)en(P), q_1 = denom = 4", ok_ratio,
          f"ratio {ratio[0]}")
    out["q1"] = q1
    # (c) d_0 perfect-power bound from the SHARED bottom vertex
    gb, gt, feas = d0_perfect_power_bound(A0, A1)
    check(f"{label}: st_{{1,0}}(P)=(8,28) shared -> d_0 | gcd(8,28)=4", gb == 4,
          f"gcd bottom={gb}, gcd top A0={gt}, feasible d_0 divisors={feas}")
    d0_ub = max(feas)
    out["d0_upper"] = d0_ub
    # (d) forcing: q_1 | d_0 and d_0 <= bound
    forced = [d for d in feas if d % q1 == 0]
    ok_unique = forced == [4]
    check(f"{label}: q_1=4 | d_0 and d_0<=4 -> d_0 = 4 UNIQUELY (no fork)",
          ok_unique, f"d_0 candidates with 4|d_0 and d_0<=bound: {forced}")
    d0 = forced[-1] if forced else None
    out["d0"] = d0
    # (e) R shape
    xdeg, yb_R, yt_R, tail = R_shape(A0, A1, d0)
    ok_int = xdeg.denominator == 1 and yb_R.denominator == 1 and yt_R.denominator == 1
    check(f"{label}: R = x^{int(xdeg)} y^{int(yb_R)} * (deg-{int(tail)} tail), "
          f"bidegree ({int(xdeg)},{int(yt_R)})", ok_int,
          f"x-deg={xdeg}, y in [{yb_R},{yt_R}], tail deg={tail}")
    out["R_bidegree"] = (int(xdeg), int(yt_R))
    out["tail_deg"] = int(tail)
    # (f) single-root shift -> candidate last corner d_0*(2,1)=(8,4)
    corner = (d0 * 2, d0 * 1)
    ok_excl, why = excluded_casos_imposibles(*corner)
    check(f"{label}: single-root shift corner = ({corner[0]},{corner[1]}); "
          f"excluded by casos imposibles", ok_excl,
          f"({corner[0]},{corner[1]}) {why}")
    out["shift_corner"] = corner
    return out


def main():
    print("=" * 76, flush=True)
    print("EXP-077: the C13 fork decision (exact arithmetic)", flush=True)
    print("=" * 76, flush=True)

    # REGRESSION GATE: the SIBLING (8,32) chain must reproduce GGHV22's published
    # decision through the identical code path (q_1=4, d_0=4, corner (8,4)).
    sib = run_chain("SIBLING(8,32)", (Fraction(8), Fraction(32)))
    gate_ok = (sib["q1"] == 4 and sib["d0"] == 4
               and sib["R_bidegree"] == (2, 8) and sib["tail_deg"] == 1
               and sib["shift_corner"] == (8, 4))
    check("REGRESSION GATE: sibling reproduces GGHV22 (q1=4, d0=4, (2,8), (8,4))",
          gate_ok, f"{sib}")
    if not gate_ok:
        print("RESULT: ABORT (regression gate failed)", flush=True)
        sys.exit(1)

    # THE C13 (8,40) CHAIN through the identical path.
    c13 = run_chain("C13(8,40)", (Fraction(8), Fraction(40)))

    # The fork decision.
    print("\n" + "=" * 76, flush=True)
    fork_collapses = (c13["q1"] == 4 and c13["d0"] == 4)
    check("FORK DECISION: q_1=4 AND d_0=4 uniquely -> the d_0 fork COLLAPSES",
          fork_collapses,
          f"dossier feared d_0 in {{4,8}}; d_0=8 is impossible "
          f"(28/8 not integer); d_0 upper bound = {c13['d0_upper']}")
    tail_differs = c13["tail_deg"] == 3 and sib["tail_deg"] == 1
    check("ENDGAME SHAPE: C13 R has a degree-3 y-tail vs sibling's degree-1",
          tail_differs,
          f"C13 R bidegree {c13['R_bidegree']} vs sibling {sib['R_bidegree']}")
    corner_same = c13["shift_corner"] == (8, 4)
    check("SINGLE-ROOT SHIFT: C13's naive shift corner is also (8,4), excluded",
          corner_same, f"{c13['shift_corner']}")

    # exclusion criterion sanity (the GGV2 explicit list) + a non-exclusion.
    for pt, want in [((2, 1), True), ((3, 2), True), ((6, 3), True),
                     ((8, 4), True), ((8, 12), False), ((5, 3), False)]:
        ok, why = excluded_casos_imposibles(*pt)
        check(f"casos imposibles: ({pt[0]},{pt[1]}) excluded == {want}",
              ok == want, why)

    print("\n" + "=" * 76, flush=True)
    print("DERIVATION NEEDED (source-dependent, NO floor claim): whether C13's "
          "degree-3 tail shift terminates at (8,4) as the LAST lower corner "
          "(vs a longer admissible sub-chain) needs GGHV22 section-3's exact "
          "(8,32) endgame adapted to a cubic tail. Any floor-moving statement "
          "routes to the main session.", flush=True)
    print("RESULT: " + ("ALL CHECKS PASS." if not failures
                        else f"{len(failures)} FAILED: {failures}"), flush=True)


if __name__ == "__main__":
    main()
    if failures:
        sys.exit(1)
