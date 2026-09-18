"""EXP-023 chart V2 of the compact gauge: the maximum is a HEIGHT.

Compact gauge (finding 15): translation v1 = 0, scale
max(u1, u2, u3, |v2|, |v3|) = 1. This chart is the case where the maximum
is attained by |v2|, and the mirror lets us take v2 = +1. Then

    v1 = 0,  v2 = 1,  v3 in [-1, 1],  u1, u2, u3 in [0, 1]

which is a COMPACT 4-box in the free parameters (u1, u2, u3, v3), with
geometric boundaries: a face of this box is where some other coordinate
ties the maximum, and the corresponding chart owns the other side.

The matrix is assembled generically from the six positions, as in cover.py,
with each mass column multiplied by 4 u_i^2 so that a pair collapsing onto
the axis (u_i -> 0) stays analytic - the same clearing collapseB and
narrow use, and the reason no face lemma is needed anywhere in this
stratum.
"""
import sys
from fractions import Fraction as F
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
s = importlib.util.spec_from_file_location("cov", HERE / "cover.py")
cov = importlib.util.module_from_spec(s); s.loader.exec_module(cov)
pl, IV, DV, K_inv = cov.pl, cov.IV, cov.DV, cov.K_inv

SELFP = (frozenset((0, 1)), frozenset((2, 3)), frozenset((4, 5)))

def entry_factory(mode):
    def entries(args):
        if mode == "iv":
            u1, u2, u3, v3 = (IV.raw(*b) for b in args)
            one, Z, four, eight = IV(1), IV(0), IV(4), IV(8)
        else:
            u1, u2, u3, v3 = args
            one, Z, four, eight = DV(1), DV(0), DV(4), DV(8)
        u = [u1, u2, u3]
        v = [Z, one, v3]
        P = [(u[0], v[0]), (Z - u[0], v[0]),
             (u[1], v[1]), (Z - u[1], v[1]),
             (u[2], v[2]), (Z - u[2], v[2])]
        icu = {}
        for i in range(6):
            for j in range(i + 1, 6):
                if frozenset((i, j)) in SELFP:
                    continue
                dx = P[i][0] - P[j][0]; dy = P[i][1] - P[j][1]
                d = (dx.sq() + dy.sq()).sqrt()
                icu[(i, j)] = icu[(j, i)] = K_inv(d * d * d)
        def area2(i, j, k):
            return ((P[j][0] - P[i][0]) * (P[k][1] - P[i][1])
                    - (P[j][1] - P[i][1]) * (P[k][0] - P[i][0]))
        def height_factor(i, j, k):
            for p, sp in enumerate(SELFP):
                pair = tuple(sorted(sp))
                if pair[0] in (i, j, k) and pair[1] in (i, j, k):
                    x = ({i, j, k} - set(pair)).pop()
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
    """Against cover.py (gauge u1 = 1) by the exact rescaling lambda = 1/u1:
    entries scale by lambda^-1 and column j additionally by 4 u_j^2, so
    V2[i][j] / cover[i][j] = 4 * u1 * (u_j/u1)^2 ."""
    import random
    random.seed(4242)
    ok = tried = 0
    while tried < 5:
        a1 = F(random.randint(20, 64), 64)
        a2 = F(random.randint(10, 64), 64)
        a3 = F(random.randint(10, 64), 64)
        h = F(random.randint(-60, 60), 64)
        if abs(h) < F(1, 8) or abs(h - 1) < F(1, 8):
            continue
        tried += 1
        Jc = entry_factory("iv")([(x, x) for x in (a1, a2, a3, h)])
        # cover.py's gauge: divide all lengths by a1
        Jo = cov.entry_factory("iv")([(a2 / a1, a2 / a1), (a3 / a1, a3 / a1),
                                      (F(1) / a1, F(1) / a1), (h / a1, h / a1)])
        avec = [a1, a2, a3]
        good = True
        for i in range(6):
            for j in range(3):
                x = (Jc[i][j].lo + Jc[i][j].hi) / 2
                y = (Jo[i][j].lo + Jo[i][j].hi) / 2
                if abs(y) < F(1, 10**9):
                    continue
                want = 4 * a1 * (avec[j] / a1) ** 2
                if abs(x - y * want) > abs(y * want) / 1000 + F(1, 10**9):
                    print(f"  MISMATCH row {i} col {j}: {float(x)} vs {float(y*want)}")
                    good = False
        ok += good
    print(f"chart V2 crosscheck: {ok}/5 OK", flush=True)
    return ok == 5

def discard(box):
    """chartV2's coordinates are (u1, u2, u3, v3) with v1 = 0 and v2 = 1."""
    u1b, u2b, u3b, v3b = box
    return cov.collision_discard([
        (u1b[0], u1b[1], F(0), F(0)),
        (u2b[0], u2b[1], F(1), F(1)),
        (u3b[0], u3b[1], v3b[0], v3b[1]),
    ])

def main():
    seed = ((F(0), F(1)), (F(0), F(1)), (F(0), F(1)), (F(-1), F(1)))
    cov.run_cover("chartV2", seed, entry_factory("iv"), entry_factory("dv"),
                  discard, budget=43200, resume="--resume" in sys.argv)

if __name__ == "__main__":
    if "--cover" in sys.argv:
        main()
    else:
        crosscheck()
