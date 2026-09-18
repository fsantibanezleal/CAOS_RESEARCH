"""EXP-023 charts U2, U3 and V3 of the compact gauge.

The compact gauge (finding 15) is: translation v1 = 0, scale
max(u1, u2, u3, |v2|, |v3|) = 1. Five charts, one per coordinate that
attains the maximum. U1 is cover.py and V2 is chartV2.py; this file
supplies the remaining three, all by the same construction:

    U2:  u2 = 1,  free (u1, u3, v2, v3) in [0,1]^2 x [-1,1]^2
    U3:  u3 = 1,  free (u1, u2, v2, v3) in [0,1]^2 x [-1,1]^2
    V3:  v3 = 1,  free (u1, u2, u3, v2) in [0,1]^3 x [-1,1]

Each assembles the 6 x 3 matrix generically from the six positions with
each mass column multiplied by 4 u_i^2, and each uses the shared
collision discard so the genuine collision faces are left to the face
charts. Every one is crosschecked against cover.py by the exact
rescaling before it runs.
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

def build(kind, mode):
    """kind in {'U2','U3','V3'}; returns an entry function over 4 args."""
    def entries(args):
        if mode == "iv":
            a, b, c, d = (IV.raw(*x) for x in args)
            one, Z, four, eight = IV(1), IV(0), IV(4), IV(8)
        else:
            a, b, c, d = args
            one, Z, four, eight = DV(1), DV(0), DV(4), DV(8)
        if kind == "U2":      # (u1, u3, v2, v3), u2 = 1
            u = [a, one, b]; v = [Z, c, d]
        elif kind == "U3":    # (u1, u2, v2, v3), u3 = 1
            u = [a, b, one]; v = [Z, c, d]
        else:                 # V3: (u1, u2, u3, v2), v3 = 1
            u = [a, b, c]; v = [Z, d, one]
        P = [(u[0], v[0]), (Z - u[0], v[0]),
             (u[1], v[1]), (Z - u[1], v[1]),
             (u[2], v[2]), (Z - u[2], v[2])]
        icu = {}
        for i in range(6):
            for j in range(i + 1, 6):
                if frozenset((i, j)) in SELFP:
                    continue
                dx = P[i][0] - P[j][0]; dy = P[i][1] - P[j][1]
                dd = (dx.sq() + dy.sq()).sqrt()
                icu[(i, j)] = icu[(j, i)] = K_inv(dd * dd * dd)
        def area2(i, j, k):
            return ((P[j][0] - P[i][0]) * (P[k][1] - P[i][1])
                    - (P[j][1] - P[i][1]) * (P[k][0] - P[i][0]))
        def hfac(i, j, k):
            for p, sp in enumerate(SELFP):
                pr = tuple(sorted(sp))
                if pr[0] in (i, j, k) and pr[1] in (i, j, k):
                    x = ({i, j, k} - set(pr)).pop()
                    base = P[pr[0]][1] - P[x][1]
                    can = [x, pr[0], pr[1]]
                    seq = [can.index(t) for t in (i, j, k)]
                    sg = 1
                    for m in range(3):
                        for n in range(m + 1, 3):
                            if seq[m] > seq[n]:
                                sg = -sg
                    return (base if sg > 0 else Z - base), p
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
                si = frozenset((i, k)) in SELFP
                sj = frozenset((j, k)) in SELFP
                if si or sj:
                    D, p = hfac(i, j, k)
                    other = icu[(j, k)] if si else icu[(i, k)]
                    if si:
                        row[pk] = row[pk] + (one - eight * u3s[p] * other) * D
                    else:
                        row[pk] = row[pk] + (eight * u3s[p] * other - one) * D
                else:
                    row[pk] = row[pk] + colscale[pk] * \
                        (icu[(i, k)] - icu[(j, k)]) * area2(i, j, k)
            J.append(row)
        return J
    return entries

def geom(kind, a, b, c, d):
    if kind == "U2":  return [a, F(1), b], [F(0), c, d]
    if kind == "U3":  return [a, b, F(1)], [F(0), c, d]
    return [a, b, c], [F(0), d, F(1)]

def crosscheck(kind):
    import random
    random.seed({"U2": 71, "U3": 73, "V3": 79}[kind])
    ok = tried = 0
    while tried < 5:
        a = F(random.randint(20, 64), 64); b = F(random.randint(20, 64), 64)
        c = F(random.randint(-60, 60), 64); d = F(random.randint(-60, 60), 64)
        u, v = geom(kind, a, b, c, d)
        if min(u) <= 0: continue
        hs = [v[1] - v[0], v[2] - v[0], v[2] - v[1]]
        if any(abs(h) < F(1, 8) for h in hs): continue
        tried += 1
        Jc = build(kind, "iv")([(x, x) for x in (a, b, c, d)])
        # cover.py's gauge: v1 = 0 already; divide all lengths by u[0]
        s0 = u[0]
        Jo = cov.entry_factory("iv")([(u[1]/s0, u[1]/s0), (u[2]/s0, u[2]/s0),
                                      (v[1]/s0, v[1]/s0), (v[2]/s0, v[2]/s0)])
        good = True
        for i in range(6):
            for j in range(3):
                x = (Jc[i][j].lo + Jc[i][j].hi) / 2
                y = (Jo[i][j].lo + Jo[i][j].hi) / 2
                if abs(y) < F(1, 10**9): continue
                want = 4 * s0 * (u[j] / s0) ** 2
                if abs(x - y * want) > abs(y * want) / 1000 + F(1, 10**9):
                    print(f"  {kind} MISMATCH row {i} col {j}: {float(x)} vs {float(y*want)}")
                    good = False
        ok += good
    print(f"chart {kind} crosscheck: {ok}/5 OK", flush=True)
    return ok == 5

def make_discard(kind):
    def disc(box):
        a, b, c, d = box
        if kind == "U2":
            uvs = [(a[0], a[1], F(0), F(0)), (F(1), F(1), c[0], c[1]),
                   (b[0], b[1], d[0], d[1])]
        elif kind == "U3":
            uvs = [(a[0], a[1], F(0), F(0)), (b[0], b[1], c[0], c[1]),
                   (F(1), F(1), d[0], d[1])]
        else:
            uvs = [(a[0], a[1], F(0), F(0)), (b[0], b[1], d[0], d[1]),
                   (c[0], c[1], F(1), F(1))]
        return cov.collision_discard(uvs)
    return disc

SEEDS = {
    "U2": ((F(0), F(1)), (F(0), F(1)), (F(-1), F(1)), (F(-1), F(1))),
    "U3": ((F(0), F(1)), (F(0), F(1)), (F(-1), F(1)), (F(-1), F(1))),
    "V3": ((F(0), F(1)), (F(0), F(1)), (F(0), F(1)), (F(-1), F(1))),
}

if __name__ == "__main__":
    kind = sys.argv[1] if len(sys.argv) > 1 else "U2"
    if "--cover" in sys.argv:
        cov.run_cover(f"chart{kind}", SEEDS[kind], build(kind, "iv"),
                      build(kind, "dv"), make_discard(kind),
                      budget=43200, resume="--resume" in sys.argv)
    else:
        crosscheck(kind)
