"""At an E = 0 point of the merge face, does the TRAP fire?

Lemma piece 13: the face's rank floor E vanishes on a surface, so no
amount of bisection makes a rank-3 certificate appear there. That is fine
if the trap fires instead, because the trap does not need a nonzero minor
-- it needs a nonzero 2x2 minor (which columns 1 and 2 supply, at 0.037
and 1.96) plus two 3x3 minors whose gradients are independent, which
confines rank <= 2 to a smooth codimension-2 manifold.

If the trap fires on a thin box AT the face and at E = 0, then the whole
merge collar closes: bisection resolves E wherever it is nonzero, and the
trap covers the thin neighbourhood of the surface where it is not.
"""
import importlib.util
from fractions import Fraction as F
from pathlib import Path
import mpmath as mp

mp.mp.dps = 40
HERE = Path(__file__).resolve().parent
_s = importlib.util.spec_from_file_location("mg", HERE / "mergeBC.py")
mg = importlib.util.module_from_spec(_s)
_s.loader.exec_module(mg)
cov = mg.cov
eiv, edv = mg.entry_factory("iv"), mg.entry_factory("dv")

_f = importlib.util.spec_from_file_location("fl", HERE / "face-lemma-merge03.py")


def E_closed(tau, wu, wv):
    o = 1 + tau * tau
    n = ((1 - tau * tau) / o, 2 * tau / o)
    tot = mp.mpf(0)
    for Pk in ((mp.mpf(1), mp.mpf(0)), (mp.mpf(-1), mp.mpf(0))):
        g = (wu - Pk[0], wv - Pk[1])
        dot = n[0] * g[0] + n[1] * g[1]
        crs = n[0] * g[1] - n[1] * g[0]
        gn = mp.sqrt(g[0] ** 2 + g[1] ** 2)
        tot += dot * crs / gn ** 5
    return -3 * tot


def find_root(wu, wv, lo, hi):
    a, b = mp.mpf(lo), mp.mpf(hi)
    fa = E_closed(a, wu, wv)
    for _ in range(200):
        m = (a + b) / 2
        fm = E_closed(m, wu, wv)
        if fa * fm <= 0:
            b = m
        else:
            a, fa = m, fm
    return (a + b) / 2


print("locating E = 0 points on the merge face, then testing the trap")
print("on a THIN box at rho = 0 centred on each\n")
cases = [(mp.mpf("0.97"), mp.mpf("0.99")),
         (mp.mpf("0.5"), mp.mpf("0.25")),
         (mp.mpf("0.2"), mp.mpf("-0.7")),
         (mp.mpf("0.75"), mp.mpf("0.4"))]
W = F(1, 2 ** 20)
for (wu, wv) in cases:
    tr = None
    for (lo, hi) in ((-2, -0.5), (-0.5, 0.5), (0.5, 2)):
        a, b = E_closed(mp.mpf(lo), wu, wv), E_closed(mp.mpf(hi), wu, wv)
        if a * b < 0:
            tr = find_root(wu, wv, lo, hi)
            break
    if tr is None:
        print(f"  w=({float(wu):.2f},{float(wv):+.2f}): no sign change found")
        continue
    tq = F(int(tr * 2 ** 30), 2 ** 30)
    wuq = F(int(wu * 2 ** 30), 2 ** 30)
    wvq = F(int(wv * 2 ** 30), 2 ** 30)
    box = ((F(0), F(0)),
           (tq - W, tq + W), (wuq - W, wuq + W), (wvq - W, wvq + W))
    Ev = float(E_closed(mp.mpf(tq.numerator) / tq.denominator, wu, wv))
    J = eiv([tuple(x) for x in box])
    e = J[4][0]
    r3 = bool(cov.rank3_plain(J)) or bool(cov.rank3_mv(edv, box))
    tp = bool(cov.trap(eiv, edv, box))
    print(f"  w=({float(wu):.2f},{float(wv):+.2f})  tau*={float(tr):+.8f}"
          f"  E={Ev:+.2e}")
    print(f"     chart entry row(2,4)col0 = [{float(e.lo):+.3e}, "
          f"{float(e.hi):+.3e}]   rank3={r3}   TRAP={tp}")
