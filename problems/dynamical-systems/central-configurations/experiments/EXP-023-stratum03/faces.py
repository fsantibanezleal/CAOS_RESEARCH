"""EXP-023 FACE charts in the compact gauge.

The five interior charts (U1, U2, U3, V2, V3) discard collision
neighbourhoods to these. In the compact gauge
(v1 = 0, max(u1, u2, u3, |v2|, |v3|) = 1) there are exactly two kinds:

  COLLAPSE(i):  pair i falls onto the axis, u_i -> 0. Cured by multiplying
      that pair's mass column by 4 u_i^2, which cancels its own 1/w_i^3
      exactly, because every area spanning the pair carries a factor 2 u_i:
          4 u_i^2 (1/r^3 - 1/w_i^3)(2 u_i D) = (8 u_i^3/r^3 - 1) D .
      Measured full rank on the face (finding 4).

  MERGE(i,j):  pairs i and j run into each other, which by the mirror is
      TWO simultaneous collisions (the + bodies and the - bodies). Blown up
      with the difference as rho times a direction, so the vanishing
      distance is exactly rho; rows carrying 1/rho^3 are multiplied by
      rho^2 and the row between the merging pair is divided by rho^2, and
      both singular factors clear algebraically. Measured full rank on the
      face (finding 6).

Both were validated in the OLD gauge; this file re-expresses them in the
compact one, where the reference pair is whichever coordinate attains the
maximum and every parameter range is bounded, so no arbitrary truncation
can create an uncertifiable corner (finding 15).

Parametrisation, collapse(i): the OTHER two pairs and the heights are free
in the compact ranges and u_i in [0, 1/8]; the maximum is attained by one
of the free coordinates, which the caller fixes to 1 exactly as the
interior charts do.
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

def matrix_from(u, v, one, Z, four, eight):
    """6x3 matrix with every mass column j scaled by 4 u_j^2, entries
    analytic at every u_j = 0 by the exact clearing above."""
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

def collapse_factory(which, mode):
    """which in {0,1,2}: that pair collapses; the reference pair is the
    next one cyclically, fixed to width 1 by the compact scale gauge."""
    ref = (which + 1) % 3
    def entries(args):
        if mode == "iv":
            a, b, c, d = (IV.raw(*x) for x in args)
            one, Z, four, eight = IV(1), IV(0), IV(4), IV(8)
        else:
            a, b, c, d = args
            one, Z, four, eight = DV(1), DV(0), DV(4), DV(8)
        third = 3 - which - ref
        u = [None] * 3; v = [None] * 3
        u[which] = a; u[ref] = one; u[third] = b
        v[0] = Z
        rest = [i for i in (1, 2)]
        v[rest[0]] = c; v[rest[1]] = d
        return matrix_from(u, v, one, Z, four, eight)
    return entries

def crosscheck_collapse(which):
    import random
    random.seed(500 + which)
    ref = (which + 1) % 3
    third = 3 - which - ref
    ok = tried = 0
    while tried < 5:
        a = F(random.randint(1, 8), 64)
        b = F(random.randint(20, 64), 64)
        c = F(random.randint(-60, 60), 64)
        d = F(random.randint(-60, 60), 64)
        u = [None]*3; v = [None]*3
        u[which] = a; u[ref] = F(1); u[third] = b
        v[0] = F(0); v[1] = c; v[2] = d
        if min(u) <= 0: continue
        hs = [v[1]-v[0], v[2]-v[0], v[2]-v[1]]
        if any(abs(h) < F(1,8) for h in hs): continue
        tried += 1
        Jc = collapse_factory(which, "iv")([(x, x) for x in (a, b, c, d)])
        s0 = u[0]
        Jo = cov.entry_factory("iv")([(u[1]/s0, u[1]/s0), (u[2]/s0, u[2]/s0),
                                      (v[1]/s0, v[1]/s0), (v[2]/s0, v[2]/s0)])
        good = True
        for i in range(6):
            for j in range(3):
                x = (Jc[i][j].lo + Jc[i][j].hi)/2
                y = (Jo[i][j].lo + Jo[i][j].hi)/2
                if abs(y) < F(1, 10**9): continue
                want = 4 * s0 * (u[j]/s0)**2
                if abs(x - y*want) > abs(y*want)/1000 + F(1, 10**9):
                    print(f"  collapse{which} MISMATCH row {i} col {j}")
                    good = False
        ok += good
    print(f"collapse chart {which} crosscheck: {ok}/5 OK", flush=True)
    return ok == 5

def make_discard(which):
    """Keep only this pair's collapse collar; the other collisions belong
    to their own face charts. Coordinates are (u_which, u_third, v2, v3)."""
    ref = (which + 1) % 3
    third = 3 - which - ref
    def disc(box):
        a, b, c, d = box
        u = [None]*3; v = [None]*3
        u[which] = (a[0], a[1]); u[ref] = (F(1), F(1)); u[third] = (b[0], b[1])
        v[0] = (F(0), F(0)); v[1] = (c[0], c[1]); v[2] = (d[0], d[1])
        uvs = [(u[i][0], u[i][1], v[i][0], v[i][1]) for i in range(3)]
        # do NOT discard this pair's own collapse: that is what we cover
        uvs2 = list(uvs)
        uvs2[which] = (F(1), F(1), v[which][0], v[which][1])
        return cov.collision_discard(uvs2)
    return disc

SEED = ((F(0), F(1, 8)), (F(0), F(1)), (F(-1), F(1)), (F(-1), F(1)))

def cover_collapse(which, resume=False):
    cov.run_cover(f"collapse{which}", SEED, collapse_factory(which, "iv"),
                  collapse_factory(which, "dv"), make_discard(which),
                  budget=21600, resume=resume)

if __name__ == "__main__" and "--cover" in sys.argv:
    w = int(sys.argv[1])
    cover_collapse(w, resume="--resume" in sys.argv)
elif __name__ == "__main__":
    for w in (0, 1, 2):
        crosscheck_collapse(w)
    # face test: does u_which = 0 certify?
    import random
    for w in (0, 1, 2):
        random.seed(9 + w); ok = tot = 0
        for _ in range(40):
            b = F(random.randint(20, 64), 64)
            c = F(random.randint(-60, 60), 64); d = F(random.randint(-60, 60), 64)
            if abs(c) < F(1,8) or abs(d) < F(1,8) or abs(c-d) < F(1,8): continue
            tot += 1
            J = collapse_factory(w, "iv")([(F(0),F(0)),(b,b),(c,c),(d,d)])
            if cov.rank3_plain(J) is not None: ok += 1
        print(f"collapse{w} FACE u=0: {ok}/{tot} certify rank 3")
