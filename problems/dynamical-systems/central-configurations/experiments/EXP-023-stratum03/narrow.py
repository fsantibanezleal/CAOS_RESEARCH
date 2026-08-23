"""EXP-023: the ALL-NARROW chart, which is also the OUTER region.

A configuration whose heights are large compared with the pair widths
rescales (divide by the height scale) onto one where all three widths are
small and the heights are order 1. So the outer region of the (v1 = 0,
u1 = 1) gauge and the all-narrow region are the SAME region, and one chart
covers both (findings 8 and 11).

Chart variables (eps, c1, c2, h): the three widths are u_i = eps * a_i with
(a1, a2, a3) = (1, c1, c2) and c1, c2 in [0, 1] (pair A widest by the S3
symmetry), the heights are v1 = 0, v2 = 1 (the height scale, fixed by the
remaining scale freedom) and v3 = h in [-2, 2]. eps in [0, 1/4].

Each mass column is multiplied by 4 u_i^2, which clears that pair's own
1/w_i^3 exactly as in collapseB: for any row whose mass coefficient
involves w_i, the area spanning that pair carries a factor 2 u_i, so

    4 u_i^2 (1/r^3 - 1/w_i^3)(2 u_i D) = (8 u_i^3 / r^3 - 1) D

is analytic at u_i = 0. Measured (outer-probe.py): with these rescales
sigma_3 of the row-normalised matrix is 2.0 at eps = 1e-2, 1e-4 and 1e-6,
flat, so the face is full rank and no lemma is needed.
"""
import sys
from fractions import Fraction as F
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
s = importlib.util.spec_from_file_location("cov", HERE / "cover.py")
cov = importlib.util.module_from_spec(s); s.loader.exec_module(cov)
pl, IV, DV, K_inv = cov.pl, cov.IV, cov.DV, cov.K_inv

# height of each pair, and the self-pair index
SELF = {0: 0, 1: 0, 2: 1, 3: 1, 4: 2, 5: 2}

def entry_factory(mode):
    def entries(args):
        if mode == "iv":
            eps, c1, c2, h = (IV.raw(*b) for b in args)
            one, Z, two, four, eight = IV(1), IV(0), IV(2), IV(4), IV(8)
        else:
            eps, c1, c2, h = args
            one, Z, two, four, eight = DV(1), DV(0), DV(2), DV(4), DV(8)
        a = [one, c1, c2]                      # width shape factors
        u = [eps * a[0], eps * a[1], eps * a[2]]
        v = [Z, one, h]
        P = [(u[0], v[0]), (Z - u[0], v[0]),
             (u[1], v[1]), (Z - u[1], v[1]),
             (u[2], v[2]), (Z - u[2], v[2])]
        SELFP = (frozenset((0, 1)), frozenset((2, 3)), frozenset((4, 5)))
        icu = {}
        for i in range(6):
            for j in range(i + 1, 6):
                if frozenset((i, j)) in SELFP:
                    continue                    # 1/w^3, cleared algebraically
                dx = P[i][0] - P[j][0]; dy = P[i][1] - P[j][1]
                d = (dx.sq() + dy.sq()).sqrt()
                icu[(i, j)] = icu[(j, i)] = K_inv(d * d * d)
        def area2(i, j, k):
            return ((P[j][0] - P[i][0]) * (P[k][1] - P[i][1])
                    - (P[j][1] - P[i][1]) * (P[k][0] - P[i][0]))
        def height_factor(i, j, k):
            """area2(i,j,k) / (2 u_p) when {i,j,k} spans pair p exactly."""
            for p, sp in enumerate(SELFP):
                pair = tuple(sorted(sp))
                if pair[0] in (i, j, k) and pair[1] in (i, j, k):
                    x = ({i, j, k} - set(pair)).pop()
                    # canonical (x, lo, hi): area = (P_lo - P_x) x (P_hi - P_lo)
                    # P_hi - P_lo = (-2 u_p, 0)  =>  area = 2 u_p * (P_lo.y - P_x.y)
                    base = P[pair[0]][1] - P[x][1]
                    can = [x, pair[0], pair[1]]
                    seq = [can.index(t) for t in (i, j, k)]
                    sgn = 1
                    for m in range(3):
                        for n in range(m + 1, 3):
                            if seq[m] > seq[n]:
                                sgn = -sgn
                    return (base if sgn > 0 else Z - base), p
            return None, None
        u3s = [x * x * x for x in u]
        colscale = [four * u[0].sq(), four * u[1].sq(), four * u[2].sq()]
        J = []
        for (i, j) in cov.ROWS:
            row = [Z, Z, Z]
            for k in range(6):
                if k == i or k == j:
                    continue
                pk = cov.PAIR_OF[k]
                sm_i = frozenset((i, k)) in SELFP
                sm_j = frozenset((j, k)) in SELFP
                if sm_i or sm_j:
                    D, p = height_factor(i, j, k)
                    other = icu[(j, k)] if sm_i else icu[(i, k)]
                    if sm_i:
                        row[pk] = row[pk] + (one - eight * u3s[p] * other) * D
                    else:
                        row[pk] = row[pk] + (eight * u3s[p] * other - one) * D
                else:
                    row[pk] = row[pk] + colscale[pk] * \
                        (icu[(i, k)] - icu[(j, k)]) * area2(i, j, k)
            J.append(row)
        return J
    return entries

def crosscheck():
    import random
    random.seed(1234)
    ok = tried = 0
    while tried < 5:
        ev = F(random.randint(2, 14), 64)
        c1 = F(random.randint(20, 64), 64)
        c2 = F(random.randint(20, 64), 64)
        hv = F(random.randint(-120, 120), 64)
        if abs(hv) < F(1, 8) or abs(hv - 1) < F(1, 8):
            continue
        tried += 1
        u1, u2, u3 = ev, ev * c1, ev * c2
        Jc = entry_factory("iv")([(x, x) for x in (ev, c1, c2, hv)])
        # the reference matrix in cover.py's gauge needs u1 = 1: rescale by 1/ev
        P = [(u1, F(0)), (u2, F(1)), (u3, hv)]
        Jo = cov.entry_factory("iv")([(u2 / u1, u2 / u1), (u3 / u1, u3 / u1),
                                      (F(1) / u1, F(1) / u1), (hv / u1, hv / u1)])
        # cover.py's gauge is u1 = 1, so its lengths are ours divided by u1:
        # the matrix scales by u1^(-4) overall (1/r^3 x area), and its column
        # j carries our colscale[j] / u1^2 ... verified numerically here.
        # Under the length rescale lambda = 1/eps taking this gauge to
        # cover.py's (u1 = 1), an entry (1/r^3 - 1/r'^3) * area scales by
        # lambda^-1, and this chart additionally carries the column factor
        # 4 u_j^2. So the expected ratio is column-dependent:
        #     narrow[i][j] / cover[i][j] = 4 * eps * a_j^2 .
        avec = [F(1), c1, c2]
        good = True
        for i in range(6):
            for j in range(3):
                a = (Jc[i][j].lo + Jc[i][j].hi) / 2
                b = (Jo[i][j].lo + Jo[i][j].hi) / 2
                if abs(b) < F(1, 10**9):
                    continue
                want = 4 * ev * avec[j] ** 2
                if abs(a - b * want) > abs(b * want) / 1000 + F(1, 10**9):
                    print(f"  MISMATCH row {i} col {j}: {float(a)} vs {float(b*want)}")
                    good = False
        ok += good
    print(f"crosscheck vs cover.py (per-column factor 4 eps a_j^2): {ok}/5 OK", flush=True)
    return ok == 5

SIXT = F(1, 16)

def discard(box):
    return False

def main():
    # Seed widened 2026-08-20 to CLOSE THE SEAM with mergeBC. The seam
    # check maps every mergeBC residue box into this gauge and reports the
    # range needed: eps up to 0.2501, c1 and c2 up to 1.2500, h ~ 1. The
    # box below contains all of that with room to spare. Note c > 1 means
    # the first pair is not the widest, so the S3 reduction is given up
    # here in exchange for the seam; that costs work, not correctness.
    seed = ((F(0), F(1, 2)), (F(0), F(2)), (F(0), F(2)), (F(-2), F(2)))
    cov.run_cover("narrow", seed, entry_factory("iv"), entry_factory("dv"),
                  discard, budget=21600, resume="--resume" in sys.argv)

if __name__ == "__main__":
    if "--cover" in sys.argv:
        main()
    else:
        crosscheck()
