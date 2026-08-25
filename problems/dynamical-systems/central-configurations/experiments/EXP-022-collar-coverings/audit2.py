"""ADVERSARIAL AUDIT, second pass.

Three blocks: the two the first pass failed to test properly, and a
coverage verification for the new chart done the right way from the start,
because the same check done the wrong way produced a false alarm earlier.
"""
import json
import random
from fractions import Fraction as F
from pathlib import Path
import importlib.util
import mpmath as mp

mp.mp.dps = 50

ROWS = [(0, 2), (0, 4), (1, 2), (1, 4), (2, 4), (2, 5)]
COL = [0, 1, 2, 2, 3, 3]


def matrix(u, v, p, q):
    P = [(mp.mpf(0), mp.mpf(1)), (mp.mpf(0), mp.mpf(-1)),
         (u, v), (-u, v), (p, q), (-p, q)]
    M = []
    for (i, j) in ROWS:
        c = [mp.mpf(0)] * 4
        for k in range(6):
            if k == i or k == j:
                continue
            rik = mp.sqrt((P[i][0] - P[k][0]) ** 2 + (P[i][1] - P[k][1]) ** 2)
            rjk = mp.sqrt((P[j][0] - P[k][0]) ** 2 + (P[j][1] - P[k][1]) ** 2)
            area = ((P[j][0] - P[i][0]) * (P[k][1] - P[i][1])
                    - (P[j][1] - P[i][1]) * (P[k][0] - P[i][0]))
            c[COL[k]] += (rik ** -3 - rjk ** -3) * area
        M.append(c)
    return M


def svals(u, v, p, q):
    M = matrix(u, v, p, q)
    A = mp.matrix(6, 4)
    for i in range(6):
        n = max(abs(x) for x in M[i]) or mp.mpf(1)
        for j in range(4):
            A[i, j] = M[i][j] / n
    U, S, V = mp.svd_r(A)
    return [S[i] for i in range(4)], V


print("=" * 72)
print("A2. What the sextic 32a^6 - 32a^3 + 7 = 0 actually pins down")
print("=" * 72)
for x in ((32 - mp.sqrt(128)) / 64, (32 + mp.sqrt(128)) / 64):
    a = x ** (mp.mpf(1) / 3)
    h = a / 2
    B = [(h, h), (-h, h), (-h, -h), (h, -h)]
    ax = mp.mpf(0)
    for j in range(1, 4):
        dx, dy = B[j][0] - B[0][0], B[j][1] - B[0][1]
        ax += dx / ((dx * dx + dy * dy) ** mp.mpf("1.5"))
    lam = -ax / B[0][0]
    I = sum(bx * bx + by * by for (bx, by) in B)
    print(f"   a = {mp.nstr(a, 14)}   lambda = {mp.nstr(lam, 12)}   "
          f"I = {mp.nstr(I, 12)}   diagonal = {mp.nstr(a * mp.sqrt(2), 12)}")
print()
print("   BOTH roots give an exact central configuration, because every")
print("   square of equal masses does. The sextic is therefore a statement")
print("   about the NORMALISED distance system, not about which square is")
print("   central, so the word unique is only meaningful together with")
print("   that normalisation.")
print("   VERDICT: not refuted, but UNDER-SPECIFIED as printed.")

print()
print("=" * 72)
print("D2. THE PAIR-EQUALITY LEMMA, attacked with constructed rank-3 shapes")
print("=" * 72)


def s4(x):
    u, v, p, q = x
    if u <= mp.mpf("0.05") or p <= mp.mpf("0.05"):
        return mp.mpf(10)
    if abs(v - q) < mp.mpf("0.15"):
        return mp.mpf(10)
    if (u - p) ** 2 + (v - q) ** 2 < mp.mpf("0.01"):
        return mp.mpf(10)
    for (uu, vv) in ((u, v), (p, q)):
        if uu ** 2 + (vv - 1) ** 2 < mp.mpf("0.01"):
            return mp.mpf(10)
        if uu ** 2 + (vv + 1) ** 2 < mp.mpf("0.01"):
            return mp.mpf(10)
    S, _ = svals(u, v, p, q)
    return S[3] / S[0]


rnd = random.Random(20260825)
found = []
for trial in range(50):
    x = [mp.mpf(rnd.randint(30, 260)) / 100,
         mp.mpf(rnd.randint(-260, 260)) / 100,
         mp.mpf(rnd.randint(30, 260)) / 100,
         mp.mpf(rnd.randint(-260, 260)) / 100]
    best = s4(x)
    step = mp.mpf(1) / 8
    for it in range(900):
        y = [x[i] + step * (mp.mpf(rnd.random()) - mp.mpf(1) / 2)
             for i in range(4)]
        val = s4(y)
        if val < best:
            best, x = val, y
        if it % 150 == 149:
            step /= 2.2
    if best < mp.mpf(10) ** -11:
        found.append((best, x))

print(f"   rank-3 shapes constructed with v != q: {len(found)} of 50")
viol = 0
for best, x in sorted(found)[:12]:
    u, v, p, q = x
    S, V = svals(u, v, p, q)
    k = [V[3, j] for j in range(4)]
    n = max(abs(t) for t in k)
    k = [t / n for t in k]
    d = abs(k[2] - k[3])
    bad = d > mp.mpf(10) ** -9
    viol += bad
    tag = "  <== VIOLATION" if bad else ""
    print(f"     v-q={float(v - q):+8.4f} s4/s1={float(best):.1e}  "
          f"mA={float(k[2]):+.10f} mB={float(k[3]):+.10f} "
          f"|mA-mB|={float(d):.1e}{tag}")
print()
if not found:
    print("   INCONCLUSIVE: still no rank-3 shape constructed.")
elif viol:
    print(f"   REFUTED: {viol} shapes with v != q have mA != mB.")
else:
    print("   SURVIVES: every constructed rank-3 shape with v != q has")
    print("   mA = mB. The central lemma holds where tested.")
    print("   Recording m1 vs m2, on which the lemma says nothing:")
    for best, x in sorted(found)[:5]:
        S, V = svals(*x)
        k = [V[3, j] for j in range(4)]
        n = max(abs(t) for t in k)
        k = [t / n for t in k]
        pos = all(t > 0 for t in k) or all(t < 0 for t in k)
        print(f"     m1={float(k[0]):+.7f} m2={float(k[1]):+.7f} "
              f"|m1-m2|={float(abs(k[0] - k[1])):.1e}  all-positive={pos}")

print()
print("=" * 72)
print("M2W. Is the new chart residue covered by the bi-corner chart?")
print("     Checked through the real map, per box.")
print("=" * 72)
HERE = Path(__file__).resolve().parent
_s = importlib.util.spec_from_file_location("pipeline", HERE / "pipeline.py")
pl = importlib.util.module_from_spec(_s)
_s.loader.exec_module(pl)
IV = pl.IV

CERT = Path("E:/_Datos/caos-research/central-configurations/EXP-022"
            "/m2w-P-certificates.jsonl")
boxes, seen = [], set()
if CERT.exists():
    for line in CERT.open(encoding="utf-8"):
        if "FAILED" not in line:
            continue
        raw = json.loads(line)["box"]
        k = json.dumps(raw)
        if k in seen:
            continue
        seen.add(k)
        boxes.append(tuple(tuple(F(x) for x in ax) for ax in raw))

print(f"   m2w-P residual boxes on file: {len(boxes)}")
inside = outside = qc = 0
worst = None
for b in boxes:
    Rcb, ttb, vb, Wb = b
    Rc, tt, W = IV.raw(*Rcb), IV.raw(*ttb), IV.raw(*Wb)
    v = IV.raw(*vb)
    one, two = IV(1), IV(2)
    iot = (one + tt.sq()).inv()
    ct = (one - tt.sq()) * iot
    st = two * tt * iot
    alpha = ct * W * st.inv()
    beta = (one - alpha.sq()).sqrt()
    half = F(1, 2)
    u = Rc * ct * (one + W) * half
    p = Rc * ct * (one - W) * half
    q = v - Rc * st * beta
    d1A = (u.sq() + (v - one).sq()).sqrt()
    d1B = (p.sq() + (q - one).sq()).sqrt()
    cs = ((u - p).sq() + (v - q).sq()).sqrt()
    cx = ((u + p).sq() + (v - q).sq()).sqrt()
    if d1A.hi > F(7, 32) or d1B.hi > F(7, 32):
        outside += 1
        continue
    CSc = cs.lo / d1A.hi if d1A.hi > 0 else F(0)
    CXc = cx.lo / d1A.hi if d1A.hi > 0 else F(0)
    if CSc < F(1, 16) or CXc < F(1, 16):
        qc += 1
        continue
    inside += 1
    if worst is None or d1A.hi > worst:
        worst = d1A.hi
print(f"   covered by bi-corner: {inside}")
print(f"   OUTSIDE the bi-corner radius 7/32: {outside}")
print(f"   inside but in the quadruple-cluster discard: {qc}")
if worst is not None:
    print(f"   largest d1A among covered: {float(worst):.6f} (limit 0.21875)")
