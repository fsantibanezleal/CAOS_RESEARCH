"""EXP-023: the pair-B collapse chart (u2 -> 0) for the (0,3) stratum.

Pair B collapses onto the symmetry axis. The self-interaction 1/w2^3 with
w2 = 2 u2 blows up, and the cure is the same one the (2,2) campaign used:
multiply the mB COLUMN by 4 u2^2. Unlike the (2,2) stratum, NO further
division is needed - measured directly (face-probe2.py): with just this
rescale the face keeps sigma_3 between 3e-2 and 8e-1 as u2 -> 0, whereas
adding the piece-11 division drives sigma_3 to zero. The (0,3) stratum has
no axis-body mass columns to vanish, which is why its collapse face is
simpler.

The cancellation is algebraic. Every area factor spanning B+ and B-
carries an explicit 2 u2:

    Delta(A+, B+, B-) = 2 u2 v2          Delta(A+, B-, B+) = -2 u2 v2
    Delta(B+, C+, B-) = 2 u2 (v3 - v2)   Delta(B+, C-, B-) = 2 u2 (v3 - v2)

so, writing the rescaled term for a row whose mB contribution involves w2,

    4 u2^2 (1/r^3 - 1/w2^3) (2 u2 D)  =  (8 u2^3 / r^3 - 1) D

which is ANALYTIC at u2 = 0 and equals -D there. The four affected rows
are L13 (r = r_{A+B-}), L14 (r = r_{A+B+}), L35 (r = r_{C+B-}) and L36
(r = r_{C-B-}); rows L15 and L16 take their mB contribution from both B
bodies with no w2 involved, and simply carry the 4 u2^2 factor.
"""
import json, sys, time
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
s = importlib.util.spec_from_file_location("cov", HERE / "cover.py")
cov = importlib.util.module_from_spec(s); s.loader.exec_module(cov)
pl, IV, DV, K_inv = cov.pl, cov.IV, cov.DV, cov.K_inv
MENU3, PAIRS2 = cov.MENU3, cov.PAIRS2

def entry_factory(mode):
    def entries(args):
        if mode == "iv":
            u2, u3, v2, v3 = (IV.raw(*b) for b in args)
            one, Z, four, eight = IV(1), IV(0), IV(4), IV(8)
        else:
            u2, u3, v2, v3 = args
            one, Z, four, eight = DV(1), DV(0), DV(4), DV(8)
        P = [(one, Z), (Z - one, Z), (u2, v2), (Z - u2, v2), (u3, v3), (Z - u3, v3)]
        icu = {}
        for i in range(6):
            for j in range(i + 1, 6):
                if {i, j} == {2, 3}:            # w2: handled algebraically
                    continue
                dx = P[i][0] - P[j][0]; dy = P[i][1] - P[j][1]
                d = (dx.sq() + dy.sq()).sqrt()
                icu[(i, j)] = icu[(j, i)] = K_inv(d * d * d)
        def area2(i, j, k):
            return ((P[j][0] - P[i][0]) * (P[k][1] - P[i][1])
                    - (P[j][1] - P[i][1]) * (P[k][0] - P[i][0]))
        u2c = u2 * u2 * u2
        s4 = four * u2.sq()
        J = []
        for (i, j) in cov.ROWS:
            row = [Z, Z, Z]
            for k in range(6):
                if k == i or k == j:
                    continue
                pk = cov.PAIR_OF[k]
                if pk == 1 and (i in (2, 3) or j in (2, 3)):
                    # the w2 term: use the exact cancelled form (8u2^3/r^3 - 1) D
                    other = 2 if 3 in (i, j, k) and 2 not in (i, j) else None
                    # r is the distance from the NON-B vertex to body k
                    nb = i if i not in (2, 3) else j
                    D = area2(i, j, k)          # = +-2 u2 * (height factor)
                    # D / (2 u2) computed exactly:
                    if (i, j) == (0, 2):    Dh = v2
                    elif (i, j) == (0, 3):  Dh = Z - v2
                    elif (i, j) == (2, 4):  Dh = v3 - v2
                    elif (i, j) == (2, 5):  Dh = v3 - v2
                    else:                   Dh = None
                    if Dh is None:
                        row[pk] = row[pk] + s4 * (icu[(i, k)] - icu[(j, k)]) * D
                        continue
                    if i in (2, 3):
                        # (R_ik - R_jk) with R_ik = 1/w2^3 : sign +
                        term = (one - eight * u2c * icu[(j, k)]) * Dh
                    else:
                        # R_jk = 1/w2^3 : sign -
                        term = (eight * u2c * icu[(i, k)] - one) * Dh
                    row[pk] = row[pk] + term
                else:
                    sc = s4 if pk == 1 else one
                    row[pk] = row[pk] + sc * (icu[(i, k)] - icu[(j, k)]) * area2(i, j, k)
            J.append(row)
        return J
    return entries

def crosscheck():
    import random
    random.seed(313)
    ok = 0
    for _ in range(5):
        u2 = F(random.randint(4, 40), 256)
        u3 = F(random.randint(8, 60), 64)
        v2 = F(random.randint(-150, 150), 64)
        v3 = F(random.randint(-150, 150), 64)
        pt = [(x, x) for x in (u2, u3, v2, v3)]
        Jc = entry_factory("iv")(pt)
        Jo = cov.entry_factory("iv")(pt)
        colscale = [1, 4 * u2**2, 1]
        good = True
        for i in range(6):
            for j in range(3):
                a = Jc[i][j]
                lo = Jo[i][j].lo * colscale[j]; hi = Jo[i][j].hi * colscale[j]
                if lo > hi: lo, hi = hi, lo
                mc = (a.lo + a.hi) / 2; mo = (lo + hi) / 2
                wid = max(a.hi - a.lo, hi - lo, F(1, 1 << 26))
                if abs(mc - mo) > 8 * wid:
                    print(f"MISMATCH row {i} col {j}: {float(mc)} vs {float(mo)}")
                    good = False
        ok += good
    print(f"crosscheck: {ok}/5 points OK", flush=True)
    return ok == 5

if __name__ == "__main__":
    if crosscheck():
        # decisive: does the FACE u2 = 0 certify?
        import random
        random.seed(5)
        ok = tot = 0
        for _ in range(30):
            u3 = F(random.randint(8, 60), 64)
            v2 = F(random.randint(-150, 150), 64)
            v3 = F(random.randint(-150, 150), 64)
            if abs(v2) < F(1, 8) or abs(v2 - v3) < F(1, 8):
                continue
            tot += 1
            J = entry_factory("iv")([(F(0), F(0)), (u3, u3), (v2, v2), (v3, v3)])
            if cov.rank3_plain(J) is not None:
                ok += 1
        print(f"FACE u2=0: {ok}/{tot} sample points certify rank 3 (full rank)")
