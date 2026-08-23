"""EXP-023 MERGE face charts in the compact gauge.

Two of the three pairs run into each other. By the mirror that is TWO
simultaneous collisions (the + bodies and the - bodies), so writing the
midpoint of the merging couple as (wu, wv) and their difference as
rho * (alpha, beta) makes the vanishing distance exactly rho.

Compact gauge: v1 = 0 and the scale fixed by the maximum coordinate. This
file covers the case where the maximum is the width of the THIRD
(non-merging) pair, set to 1; by the S3 symmetry that one shape serves all
three pair-pairs, and the other maximum-cases are separate shapes.

Free parameters (rho, tau, wu, wv) in [0,1/8] x [-1,1] x [0,1] x [-1,1]:
ALL BOUNDED, which is the point of the compact gauge (finding 15).

Clearing, exactly as the retired mergeBC validated: rows carrying a
1/rho^3 term are multiplied by rho^2, the row between the merging couple
is divided by rho^2, and both singular factors cancel algebraically. Each
mass column is additionally multiplied by 4 u_i^2 so that a pair
collapsing onto the axis stays analytic.
"""
import sys
from fractions import Fraction as F
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
_s = importlib.util.spec_from_file_location("cov", HERE / "cover.py")
cov = importlib.util.module_from_spec(_s); _s.loader.exec_module(cov)
pl, IV, DV, K_inv = cov.pl, cov.IV, cov.DV, cov.K_inv


def bodies(p):
    return (2 * p, 2 * p + 1)


def psign(seq):
    sg = 1
    for m in range(len(seq)):
        for n in range(m + 1, len(seq)):
            if seq[m] > seq[n]:
                sg = -sg
    return sg


def build(mi, mj, mode):
    mk = 3 - mi - mj

    def entries(args):
        if mode == "iv":
            rho, tau, wu, wv = (IV.raw(*x) for x in args)
            one, Z, two, four, eight = IV(1), IV(0), IV(2), IV(4), IV(8)
        else:
            rho, tau, wu, wv = args
            one, Z, two, four, eight = DV(1), DV(0), DV(2), DV(4), DV(8)
        iop = K_inv(one + tau.sq())
        al = (one - tau.sq()) * iop
        be = two * tau * iop
        half = F(1, 2)
        u = [None] * 3
        v = [None] * 3
        u[mi] = wu + rho * al * half
        v[mi] = wv + rho * be * half
        u[mj] = wu - rho * al * half
        v[mj] = wv - rho * be * half
        u[mk] = one
        v[mk] = Z
        P = []
        for p in range(3):
            P.append((u[p], v[p]))
            P.append((Z - u[p], v[p]))
        SELFP = tuple(frozenset(bodies(p)) for p in range(3))
        bi, bim = bodies(mi)
        bj, bjm = bodies(mj)
        SMALL = (frozenset((bi, bj)), frozenset((bim, bjm)))
        DIFF = {(min(bi, bj), max(bi, bj)): (al, be),
                (min(bim, bjm), max(bim, bjm)): (Z - al, be)}
        icu = {}
        for i in range(6):
            for j in range(i + 1, 6):
                fs = frozenset((i, j))
                if fs in SELFP or fs in SMALL:
                    continue
                dx = P[i][0] - P[j][0]
                dy = P[i][1] - P[j][1]
                d = (dx.sq() + dy.sq()).sqrt()
                icu[(i, j)] = icu[(j, i)] = K_inv(d * d * d)

        def area2(i, j, k):
            return ((P[j][0] - P[i][0]) * (P[k][1] - P[i][1])
                    - (P[j][1] - P[i][1]) * (P[k][0] - P[i][0]))

        def area_over_rho(i, j, k):
            for (a, b), D in DIFF.items():
                if a in (i, j, k) and b in (i, j, k):
                    x = ({i, j, k} - {a, b}).pop()
                    base = ((P[a][0] - P[x][0]) * (Z - D[1])
                            - (P[a][1] - P[x][1]) * (Z - D[0]))
                    can = [x, a, b]
                    return base * psign([can.index(t) for t in (i, j, k)])
            return None

        def sdiff_over_rho(i, j, k):
            for (a, b), D in DIFF.items():
                if {i, j} == {a, b}:
                    A2 = (P[i][0] - P[k][0]).sq() + (P[i][1] - P[k][1]).sq()
                    B2 = (P[j][0] - P[k][0]).sq() + (P[j][1] - P[k][1]).sq()
                    A = A2.sqrt()
                    B = B2.sqrt()
                    sgn = one if (i, j) == (a, b) else Z - one
                    md = (D[0] * (wu - P[k][0]) + D[1] * (wv - P[k][1]))
                    b2a2 = (Z - two) * md * sgn
                    return b2a2 * (B2 + A * B + A2) * \
                        K_inv((B + A) * (A * A2) * (B * B2))
            return None

        def hfac(i, j, k):
            for p in range(3):
                pr = tuple(sorted(bodies(p)))
                if pr[0] in (i, j, k) and pr[1] in (i, j, k):
                    x = ({i, j, k} - set(pr)).pop()
                    base = P[pr[0]][1] - P[x][1]
                    can = [x, pr[0], pr[1]]
                    return (base * psign([can.index(t) for t in (i, j, k)])), p
            return None, None

        u3s = [x * x * x for x in u]
        colscale = [four * u[0].sq(), four * u[1].sq(), four * u[2].sq()]
        rho2 = rho.sq()
        rho3 = rho2 * rho
        irho2 = K_inv(rho2)
        J = []
        for (i, j) in cov.ROWS:
            row = [Z, Z, Z]
            isM = frozenset((i, j)) in SMALL
            for k in range(6):
                if k == i or k == j:
                    continue
                pk = cov.PAIR_OF[k]
                fi = frozenset((i, k))
                fj = frozenset((j, k))
                if isM:
                    sd = sdiff_over_rho(i, j, k)
                    ah = area_over_rho(i, j, k)
                    if sd is not None and ah is not None:
                        row[pk] = row[pk] + colscale[pk] * sd * ah
                    elif fi in SELFP or fj in SELFP:
                        D, p = hfac(i, j, k)
                        other = icu[(j, k)] if fi in SELFP else icu[(i, k)]
                        base = ((one - eight * u3s[p] * other) * D
                                if fi in SELFP
                                else (eight * u3s[p] * other - one) * D)
                        row[pk] = row[pk] + base * irho2
                    else:
                        row[pk] = row[pk] + colscale[pk] * irho2 * \
                            (icu[(i, k)] - icu[(j, k)]) * area2(i, j, k)
                    continue
                if fi in SMALL or fj in SMALL:
                    ah = area_over_rho(i, j, k)
                    other = icu[(j, k)] if fi in SMALL else icu[(i, k)]
                    sgn = one if fi in SMALL else Z - one
                    row[pk] = row[pk] + colscale[pk] * sgn * \
                        (ah - rho3 * other * ah)
                elif fi in SELFP or fj in SELFP:
                    D, p = hfac(i, j, k)
                    other = icu[(j, k)] if fi in SELFP else icu[(i, k)]
                    base = ((one - eight * u3s[p] * other) * D if fi in SELFP
                            else (eight * u3s[p] * other - one) * D)
                    row[pk] = row[pk] + rho2 * base
                else:
                    row[pk] = row[pk] + rho2 * colscale[pk] * \
                        (icu[(i, k)] - icu[(j, k)]) * area2(i, j, k)
            J.append(row)
        return J
    return entries


def crosscheck(mi, mj):
    import random
    random.seed(800 + 10 * mi + mj)
    mk = 3 - mi - mj
    ok = tried = 0
    while tried < 5:
        rv = F(random.randint(2, 12), 256)
        tv = F(random.randint(-40, 40), 64)
        wuv = F(random.randint(20, 60), 64)
        wvv = F(random.randint(-55, 55), 64)
        o = 1 + tv * tv
        alv = (1 - tv * tv) / o
        bev = 2 * tv / o
        u = [None] * 3
        v = [None] * 3
        u[mi] = wuv + rv * alv / 2
        v[mi] = wvv + rv * bev / 2
        u[mj] = wuv - rv * alv / 2
        v[mj] = wvv - rv * bev / 2
        u[mk] = F(1)
        v[mk] = F(0)
        if min(u) <= 0:
            continue
        hs = [v[1] - v[0], v[2] - v[0], v[2] - v[1]]
        if any(abs(h) < F(1, 8) for h in hs):
            continue
        tried += 1
        Jc = build(mi, mj, "iv")([(x, x) for x in (rv, tv, wuv, wvv)])
        vs = [x - v[0] for x in v]
        s0 = u[0]
        Jo = cov.entry_factory("iv")([(u[1] / s0, u[1] / s0),
                                      (u[2] / s0, u[2] / s0),
                                      (vs[1] / s0, vs[1] / s0),
                                      (vs[2] / s0, vs[2] / s0)])
        bi, bim = bodies(mi)
        bj, bjm = bodies(mj)
        SM = (frozenset((bi, bj)), frozenset((bim, bjm)))
        rowsc = [F(1) / rv ** 2 if frozenset((i, j)) in SM else rv ** 2
                 for (i, j) in cov.ROWS]
        good = True
        for i in range(6):
            for j in range(3):
                x = (Jc[i][j].lo + Jc[i][j].hi) / 2
                y = (Jo[i][j].lo + Jo[i][j].hi) / 2
                if abs(y) < F(1, 10 ** 9):
                    continue
                want = rowsc[i] * 4 * s0 * (u[j] / s0) ** 2
                if abs(x - y * want) > abs(y * want) / 500 + F(1, 10 ** 9):
                    print(f"  merge({mi},{mj}) MISMATCH row {i} col {j}: "
                          f"{float(x)} vs {float(y * want)}")
                    good = False
        ok += good
    print(f"merge({mi},{mj}) crosscheck: {ok}/5 OK", flush=True)
    return ok == 5


def make_discard(mi, mj):
    """Keep only this merge collar; other collisions go to their charts."""
    mk = 3 - mi - mj

    def disc(box):
        rb, tb, wub, wvb = box
        uvs = [None] * 3
        uvs[mi] = (wub[0], wub[1], wvb[0], wvb[1])
        uvs[mj] = (wub[0], wub[1], wvb[0], wvb[1])
        uvs[mk] = (F(1), F(1), F(0), F(0))
        # do not discard the merge we are covering: mask it out
        uvs2 = list(uvs)
        uvs2[mj] = (F(1), F(1), F(2), F(2))
        return cov.collision_discard(uvs2)
    return disc


SEED = ((F(0), F(1, 8)), (F(-1), F(1)), (F(0), F(1)), (F(-1), F(1)))

if __name__ == "__main__":
    if "--cover" in sys.argv:
        mi, mj = int(sys.argv[1]), int(sys.argv[2])
        cov.run_cover(f"merge{mi}{mj}", SEED, build(mi, mj, "iv"),
                      build(mi, mj, "dv"), make_discard(mi, mj),
                      budget=21600, resume="--resume" in sys.argv)
    else:
        for (a, b) in ((0, 1), (0, 2), (1, 2)):
            crosscheck(a, b)
