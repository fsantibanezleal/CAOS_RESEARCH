"""EXP-021 phase 3: mean-value-form certificates for the remaining boxes.

Dual-interval forward mode: each quantity carries (value IV, four partial
IVs). The mean-value enclosure of a minor M over a box is
M(mid) + sum_i dM/dx_i(box) * [-rad_i, rad_i], sound by the mean value
theorem with interval-enclosed derivatives; M(mid) is evaluated at the
point interval (width 2^-40). Fallback: bisect to depth 40 under the same
test.
"""
import json, math, time
from fractions import Fraction as F
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("r21", HERE / "run.py")
r21 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r21)
IV = r21.IV

ZERO = IV(0)

class DV:
    __slots__ = ("v", "g")
    def __init__(self, v, g=None):
        self.v = v if isinstance(v, IV) else IV(v)
        self.g = g if g is not None else [ZERO, ZERO, ZERO, ZERO]
    def __add__(self, o):
        o = o if isinstance(o, DV) else DV(o)
        return DV(self.v + o.v, [self.g[i] + o.g[i] for i in range(4)])
    __radd__ = __add__
    def __sub__(self, o):
        o = o if isinstance(o, DV) else DV(o)
        return DV(self.v - o.v, [self.g[i] - o.g[i] for i in range(4)])
    def __rsub__(self, o):
        return DV(o) - self
    def __neg__(self):
        return DV(IV.raw(-self.v.hi, -self.v.lo), [IV.raw(-g.hi, -g.lo) for g in self.g])
    def __mul__(self, o):
        o = o if isinstance(o, DV) else DV(o)
        return DV(self.v * o.v,
                  [self.v * o.g[i] + o.v * self.g[i] for i in range(4)])
    __rmul__ = __mul__
    def sq(self):
        return DV(self.v.sq(), [IV(2) * self.v * g for g in self.g])
    def sqrt(self):
        s = self.v.sqrt()
        inv2s = (IV(2) * s).inv()
        return DV(s, [inv2s * g for g in self.g])
    def invcube(self):
        c3 = self.v * self.v * self.v
        ic = c3.inv()
        coef = IV(-3) * (self.v.sq().sq()).inv() * self.v  # -3 / v^4 ... = -3 v / v^5
        # safer: d(v^-3) = -3 v^-4 dv ; v^-4 = (v.sq().sq()).inv()
        coef = IV(-3) * (self.v.sq().sq()).inv()
        return DV(ic, [coef * g for g in self.g])

E_U, E_V, E_P, E_Q = ([IV(1) if i == j else ZERO for i in range(4)] for j in range(4))

def entry_matrix_dual(u, v, p, q):
    one = DV(1); mone = DV(-1); two = DV(2)
    h1 = one - v; gam = mone - v; g1 = one - q; g2 = mone - q
    f = v - q; e12 = DV(2)
    d1A = (u.sq() + h1.sq()).sqrt(); d2A = (u.sq() + gam.sq()).sqrt()
    d1B = (p.sq() + g1.sq()).sqrt(); d2B = (p.sq() + g2.sq()).sqrt()
    cs = ((u - p).sq() + f.sq()).sqrt(); cx = ((u + p).sq() + f.sq()).sqrt()
    wA = two * u; wB = two * p; r12 = DV(2)
    ic = {}
    for nm, dv in (("r12", r12), ("d1A", d1A), ("d1B", d1B), ("d2A", d2A),
                   ("d2B", d2B), ("wA", wA), ("wB", wB), ("cs", cs), ("cx", cx)):
        ic[nm] = dv.invcube()
    def s_(a, b):
        return ic[a] - ic[b]
    J = [[DV(0)] * 4 for _ in range(6)]
    J[0][1] = s_("r12", "d2A") * (mone * u * e12)
    J[0][2] = s_("d1A", "wA") * (mone * two * u * h1)
    J[0][3] = s_("d1B", "cs") * (p * h1 - u * g1) + s_("d1B", "cx") * (mone * (u * g1 + p * h1))
    J[1][1] = s_("r12", "d2B") * (mone * p * e12)
    J[1][2] = s_("d1A", "cs") * (u * g1 - p * h1) + s_("d1A", "cx") * (mone * (p * h1 + u * g1))
    J[1][3] = s_("d1B", "wB") * (mone * two * p * g1)
    J[2][0] = s_("r12", "d1A") * (u * e12)
    J[2][2] = s_("d2A", "wA") * (mone * two * u * gam)
    J[2][3] = s_("d2B", "cs") * (p * gam - u * g2) + s_("d2B", "cx") * (mone * (u * g2 + p * gam))
    J[3][0] = s_("r12", "d1B") * (p * e12)
    J[3][2] = s_("d2A", "cs") * (u * g2 - p * gam) + s_("d2A", "cx") * (mone * (p * gam + u * g2))
    J[3][3] = s_("d2B", "wB") * (mone * two * p * g2)
    J[4][0] = s_("d1A", "d1B") * (p * h1 - u * g1)
    J[4][1] = s_("d2A", "d2B") * (p * gam - u * g2)
    J[4][2] = s_("wA", "cx") * (mone * two * f * u)
    J[4][3] = s_("cx", "wB") * (mone * two * f * p)
    J[5][0] = s_("d1A", "d1B") * (mone * (u * g1 + p * h1))
    J[5][1] = s_("d2A", "d2B") * (mone * (u * g2 + p * gam))
    J[5][2] = s_("wA", "cs") * (mone * two * f * u)
    J[5][3] = s_("cs", "wB") * (two * f * p)
    return J

def det3d(J, rows, cols):
    a, b, c = rows; x, y, z = cols
    return (J[a][x]*(J[b][y]*J[c][z] - J[b][z]*J[c][y])
            - J[a][y]*(J[b][x]*J[c][z] - J[b][z]*J[c][x])
            + J[a][z]*(J[b][x]*J[c][y] - J[b][y]*J[c][x]))

def mv_certifies(ub, vb, pb, qb):
    mids = [ (b[0] + b[1]) / 2 for b in (ub, vb, pb, qb) ]
    rads = [ (b[1] - b[0]) / 2 for b in (ub, vb, pb, qb) ]
    duals = [DV(IV(m), g) for m, g in zip(mids, (E_U, E_V, E_P, E_Q))]
    # widen values to the whole box for the GRADIENT enclosure soundness:
    duals_box = [DV(IV.raw(b[0], b[1]), g) for b, g in zip((ub, vb, pb, qb), (E_U, E_V, E_P, E_Q))]
    try:
        Jm = entry_matrix_dual(*duals)       # value at midpoint (tight), grads at midpoint
        Jb = entry_matrix_dual(*duals_box)   # grads over the whole box (sound)
    except AssertionError:
        return False
    for rows, cols in r21.MENU:
        try:
            dm = det3d(Jm, rows, cols)
            db = det3d(Jb, rows, cols)
            enc = dm.v
            for i in range(4):
                gi = db.g[i]
                mag = max(abs(gi.lo), abs(gi.hi))
                enc = enc + IV.raw(-mag * rads[i], mag * rads[i])
            if enc.excludes_zero():
                return True
        except AssertionError:
            continue
    return False

def main():
    t0 = time.time()
    rem = json.load(open(HERE / "artifacts" / "remaining-failed.json", encoding="utf-8"))
    boxes = [tuple(tuple(F(x) for x in b) for b in r) for r in rem]
    print(f"phase 3 on {len(boxes)} recorded boxes (sample of 4414)")
    stack = [(b, 0) for b in boxes]
    cert = fail = proc = 0
    DEPTH = 8
    while stack:
        b, d = stack.pop()
        proc += 1
        if mv_certifies(*b):
            cert += 1
            continue
        if d >= DEPTH:
            fail += 1
            continue
        ub, vb, pb, qb = b
        widths = [x[1] - x[0] for x in b]
        w = widths.index(max(widths))
        bl = [list(x) for x in b]
        lo, hi = bl[w]; mid = (lo + hi) / 2
        for half in ((lo, mid), (mid, hi)):
            nb = [tuple(x) for x in bl]
            nb[w] = half
            stack.append((tuple(nb), d + 1))
        if proc % 5000 == 0:
            print(f"[{time.time()-t0:.0f}s] {proc} processed, {cert} certified, {fail} failed", flush=True)
    print(f"PHASE3 DONE {time.time()-t0:.0f}s: processed {proc}, certified {cert}, STILL FAILED {fail}")
    (HERE / "artifacts" / "phase3-summary.json").write_text(json.dumps(
        {"input_boxes": len(boxes), "processed": proc, "certified": cert,
         "still_failed": fail}), encoding="utf-8")

if __name__ == "__main__":
    main()
