"""Which faces of the (0,3) stratum drop rank?

Faces of the gauged region (v1=0, u1=1, free u2,u3 in (0,1], v2,v3):
  F1  u2 -> 0        pair B collapses onto the axis
  F2  u3 -> 0        pair C collapses onto the axis
  F3  (u2,v2)->(u3,v3)   pairs B and C merge
  F4  (u2,v2)->(1,0)     pair B merges with pair A
  F5  u2 -> 0 AND u3 -> 0    both collapse

For each, evaluate the 6x3 matrix ON the face at interior samples and
report whether a 3x3 minor certifies rank 3 (full rank: no masses, so no
central configurations there at all).
"""
import importlib.util, random
from pathlib import Path
from fractions import Fraction as F
HERE = Path(__file__).resolve().parent
s = importlib.util.spec_from_file_location("cov", HERE / "cover.py")
cov = importlib.util.module_from_spec(s); s.loader.exec_module(cov)

rnd = random.Random(77)
def r(a, b, den=64):
    return F(rnd.randint(int(a*den)+1, int(b*den)-1), den)

FACES = {
  "F1 u2=0":        lambda: (F(0), r(0.1,0.95), r(-2.9,2.9), r(-2.9,2.9)),
  "F2 u3=0":        lambda: (r(0.1,0.95), F(0), r(-2.9,2.9), r(-2.9,2.9)),
  "F5 u2=u3=0":     lambda: (F(0), F(0), r(-2.9,2.9), r(-2.9,2.9)),
  "F3 B=C merge":   lambda: (lambda u,v: (u,u,v,v))(r(0.1,0.95), r(-2.9,2.9)),
  "F4 B=A merge":   lambda: (F(1), r(0.1,0.95), F(0), r(-2.9,2.9)),
}
for name, samp in FACES.items():
    ok = tot = 0
    for _ in range(40):
        pt = samp()
        try:
            J = cov.entry_factory("iv")([(x, x) for x in pt])
        except AssertionError:
            continue
        tot += 1
        if cov.rank3_plain(J) is not None:
            ok += 1
    verdict = ("FULL RANK on the face: no chart needed" if tot and ok == tot
               else "rank drops: needs a chart or lemma" if tot else "undefined on the face")
    print(f"  {name:16s} {ok:3d}/{tot:3d} certify rank 3   {verdict}")
