"""EXP-023: the B/C merge chart for the (0,3) stratum.

Pairs B and C run into each other. By the mirror symmetry this is TWO
simultaneous collisions, B+ with C+ and B- with C-, so the distance
    s23 = |B+ - C+| = |B- - C-|
goes to zero while x23 = |B+ - C-| stays bounded below. Chart variables
(rho, tau, wu, wv): the B/C midpoint is (wu, wv), the difference is
(u2 - u3, v2 - v3) = rho (alpha, beta) with (alpha, beta) the rational
circle in tau, so s23 = rho EXACTLY.

Measured row orders (merge-probe.py): rows L13, L14, L15, L16, L36 blow
up like rho^-2 and row L35 vanishes like rho^2, exactly tube.py's pattern
in EXP-022, so the row scalings are rho^2 on the first five and 1/rho^2 on
L35. The 1/rho^3 terms cancel ALGEBRAICALLY against vanishing areas: for
any triangle spanning both merging bodies,

    Delta(A+, B+, C+) = rho * (d x W),   d = (alpha, beta),
                                         W = midpoint - A+

carries exactly one rho, so

    rho^2 * (R - 1/rho^3) * rho (d x W)  =  rho^3 R (d x W) - (d x W)

is analytic at rho = 0 and equals -(d x W) there. sigma_3 of the rescaled
face stays in [3.3e-3, 4.6e-1] as rho -> 0 (30 samples at each of three
scales), so the merge face is FULL RANK: this stratum still needs no
face lemma.
"""
import json, sys, time
from fractions import Fraction as F
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
s = importlib.util.spec_from_file_location("cov", HERE / "cover.py")
cov = importlib.util.module_from_spec(s); s.loader.exec_module(cov)
pl, IV, DV, K_inv = cov.pl, cov.IV, cov.DV, cov.K_inv

SMALL_PAIRS = (frozenset((2, 4)), frozenset((3, 5)))   # B+C+ and B-C-

def perm_sign(seq):
    """sign of the permutation taking sorted(seq) to seq."""
    s = 1
    a = list(seq)
    for i in range(len(a)):
        for j in range(i + 1, len(a)):
            if a[i] > a[j]:
                s = -s
    return s

def entry_factory(mode):
    def entries(args):
        if mode == "iv":
            rho, tau, wu, wv = (IV.raw(*b) for b in args)
            one, Z, two = IV(1), IV(0), IV(2)
        else:
            rho, tau, wu, wv = args
            one, Z, two = DV(1), DV(0), DV(2)
        iop = K_inv(one + tau.sq())
        al = (one - tau.sq()) * iop
        be = two * tau * iop
        half = F(1, 2)
        u2 = wu + rho * al * half; v2 = wv + rho * be * half
        u3 = wu - rho * al * half; v3 = wv - rho * be * half
        P = [(one, Z), (Z - one, Z), (u2, v2), (Z - u2, v2), (u3, v3), (Z - u3, v3)]
        # difference vectors of the two merging couples, rho factored out:
        DIFF = {(2, 4): (al, be), (3, 5): (Z - al, be)}     # P_b - P_a = -rho*D
        icu = {}
        for i in range(6):
            for j in range(i + 1, 6):
                if frozenset((i, j)) in SMALL_PAIRS:
                    continue
                dx = P[i][0] - P[j][0]; dy = P[i][1] - P[j][1]
                d = (dx.sq() + dy.sq()).sqrt()
                icu[(i, j)] = icu[(j, i)] = K_inv(d * d * d)
        def area2(i, j, k):
            return ((P[j][0] - P[i][0]) * (P[k][1] - P[i][1])
                    - (P[j][1] - P[i][1]) * (P[k][0] - P[i][0]))
        def area_over_rho(i, j, k):
            """area2(i,j,k)/rho, exact, when {i,j,k} contains a merging couple."""
            for (a, b), D in DIFF.items():
                if a in (i, j, k) and b in (i, j, k):
                    x = ({i, j, k} - {a, b}).pop()
                    # canonical order (x, a, b): area2 = (Pa-Px) x (Pb-Pa)
                    #   Pb - Pa = -rho * D
                    base = ((P[a][0] - P[x][0]) * (Z - D[1])
                            - (P[a][1] - P[x][1]) * (Z - D[0]))
                    can = [x, a, b]
                    return base * perm_sign([can.index(v) for v in (i, j, k)])
            return None
        def sdiff_over_rho(i, j, k):
            """(1/r_ik^3 - 1/r_jk^3)/rho, exact, when (i,j) is a merging couple."""
            for (a, b), D in DIFF.items():
                if {i, j} == {a, b}:
                    A2 = (P[i][0] - P[k][0]).sq() + (P[i][1] - P[k][1]).sq()
                    B2 = (P[j][0] - P[k][0]).sq() + (P[j][1] - P[k][1]).sq()
                    A = A2.sqrt(); B = B2.sqrt()
                    sgn = one if (i, j) == (a, b) else Z - one
                    # B^2 - A^2 = -2 rho [ D . (midpoint - Pk) ] * sgn
                    md = (D[0] * (wu - P[k][0]) + D[1] * (wv - P[k][1]))
                    b2a2_hat = (Z - two) * md * sgn
                    num = b2a2_hat * (B2 + A * B + A2)
                    den = (B + A) * (A * A2) * (B * B2)
                    return num * K_inv(den)
            return None
        rho2 = rho.sq(); rho3 = rho2 * rho
        J = []
        for (i, j) in cov.ROWS:
            row = [Z, Z, Z]
            isL35 = frozenset((i, j)) in SMALL_PAIRS
            for k in range(6):
                if k == i or k == j:
                    continue
                pk = cov.PAIR_OF[k]
                if isL35:
                    # both factors carry rho: (sdiff/rho) * (area/rho)
                    sd = sdiff_over_rho(i, j, k)
                    ah = area_over_rho(i, j, k)
                    row[pk] = row[pk] + sd * ah
                    continue
                sm_i = frozenset((i, k)) in SMALL_PAIRS
                sm_j = frozenset((j, k)) in SMALL_PAIRS
                if sm_i or sm_j:
                    ah = area_over_rho(i, j, k)
                    other = icu[(j, k)] if sm_i else icu[(i, k)]
                    # (R_ik - R_jk) = (+-1/rho^3) -+ other ; times rho*ah ; x rho^2
                    if sm_i:
                        row[pk] = row[pk] + ah - rho3 * other * ah
                    else:
                        row[pk] = row[pk] + rho3 * other * ah - ah
                else:
                    row[pk] = row[pk] + rho2 * (icu[(i, k)] - icu[(j, k)]) * area2(i, j, k)
            J.append(row)
        return J
    return entries

def crosscheck():
    import random
    random.seed(909)
    ok = tried = 0
    while tried < 5:
        rv = F(random.randint(2, 30), 512)
        tv = F(random.randint(-40, 40), 64)
        wuv = F(random.randint(12, 56), 64)
        wvv = F(random.randint(-150, 150), 64)
        o = 1 + tv * tv
        alv = (1 - tv * tv) / o; bev = 2 * tv / o
        u2 = wuv + rv * alv / 2; v2 = wvv + rv * bev / 2
        u3 = wuv - rv * alv / 2; v3 = wvv - rv * bev / 2
        if u2 <= 0 or u3 <= 0:
            continue
        tried += 1
        Jc = entry_factory("iv")([(x, x) for x in (rv, tv, wuv, wvv)])
        Jo = cov.entry_factory("iv")([(u2, u2), (u3, u3), (v2, v2), (v3, v3)])
        rowscale = [rv**2, rv**2, rv**2, rv**2, F(1,1)/rv**2, rv**2]
        good = True
        for i in range(6):
            for j in range(3):
                a = Jc[i][j]
                lo = Jo[i][j].lo * rowscale[i]; hi = Jo[i][j].hi * rowscale[i]
                if lo > hi: lo, hi = hi, lo
                mc = (a.lo + a.hi) / 2; mo = (lo + hi) / 2
                wid = max(a.hi - a.lo, hi - lo, F(1, 1 << 24))
                if abs(mc - mo) > 8 * wid:
                    print(f"MISMATCH row {i} col {j}: {float(mc)} vs {float(mo)}")
                    good = False
        ok += good
    print(f"crosscheck: {ok}/5 points OK", flush=True)
    return ok == 5

if __name__ == "__main__":
    crosscheck()


# ---------------------------------------------------------------- covering
SIXT = F(1, 16)

def discard(box):
    """Keep the B/C merge collar; the pairs must stay clear of pair A."""
    rhob, taub, wub, wvb = box
    # the merged cluster meeting pair A at (1, 0)
    if wub[0] > 1 - SIXT and wub[1] < 1 + SIXT and wvb[0] > -SIXT and wvb[1] < SIXT:
        return True
    return False

def main():
    seed = ((F(0), F(1, 8)), (F(-1), F(1)), (F(1, 8), F(1)), (F(-3), F(3)))
    cov.run_cover("mergeBC", seed, entry_factory("iv"), entry_factory("dv"),
                  discard, budget=21600, resume="--resume" in sys.argv)

if __name__ == "__main__" and "--cover" in sys.argv:
    main()
