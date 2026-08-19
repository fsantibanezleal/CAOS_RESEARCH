"""EXP-021: verified covering of the core by rational interval certificates.

Sound by construction: Fraction endpoints, outward rounding to 2^-40 grid,
isqrt bracketing for square roots, reciprocals on sign-definite intervals
only. The certified minor is {L13,L15,L23} x {m1,m2,mA} = a23 * C1.
"""
import json, math, time
from fractions import Fraction as F
from pathlib import Path

ART = Path(__file__).resolve().parent / "artifacts"
ART.mkdir(exist_ok=True)
GRID = 1 << 40
G2 = 1 << 80

def rdown(x):
    return F(math.floor(x * GRID), GRID)

def rup(x):
    return F(math.ceil(x * GRID), GRID)

class IV:
    __slots__ = ("lo", "hi")
    def __init__(self, lo, hi=None):
        if hi is None: hi = lo
        self.lo, self.hi = rdown(F(lo)), rup(F(hi))
    @staticmethod
    def raw(lo, hi):
        iv = IV.__new__(IV); iv.lo, iv.hi = rdown(lo), rup(hi); return iv
    def __add__(self, o):
        o = o if isinstance(o, IV) else IV(o)
        return IV.raw(self.lo + o.lo, self.hi + o.hi)
    def __sub__(self, o):
        o = o if isinstance(o, IV) else IV(o)
        return IV.raw(self.lo - o.hi, self.hi - o.lo)
    def __mul__(self, o):
        o = o if isinstance(o, IV) else IV(o)
        c = (self.lo*o.lo, self.lo*o.hi, self.hi*o.lo, self.hi*o.hi)
        return IV.raw(min(c), max(c))
    __radd__ = __add__
    __rmul__ = __mul__
    def __rsub__(self, o):
        return IV(o) - self
    def __neg__(self):
        return IV.raw(-self.hi, -self.lo)
    def sq(self):
        return self * self
    def sqrt(self):
        assert self.lo > 0, "sqrt needs positive interval"
        nlo = math.isqrt((self.lo.numerator * G2) // self.lo.denominator)
        nhi = math.isqrt(-(-(self.hi.numerator * G2) // self.hi.denominator)) + 1
        return IV.raw(F(nlo, GRID), F(nhi, GRID))
    def inv(self):
        assert self.lo > 0 or self.hi < 0, "inv needs sign-definite interval"
        return IV.raw(1 / self.hi, 1 / self.lo)
    def invcube(self):
        c = self * self * self
        return c.inv()
    def excludes_zero(self):
        return self.lo > 0 or self.hi < 0

A1, A2 = F(1), F(-1)

def minor_interval(ub, vb, pb, qb):
    """[boxes as (lo,hi) Fraction pairs] -> IV of the chosen minor."""
    u = IV.raw(*ub); v = IV.raw(*vb); p = IV.raw(*pb); q = IV.raw(*qb)
    one = IV(1); mone = IV(-1)
    h1 = one - v            # a1 - v
    gam = mone - v          # a2 - v
    g1 = one - q            # a1 - q
    e12 = IV(2)             # a1 - a2
    d1A = (u.sq() + h1.sq()).sqrt()
    d2A = (u.sq() + gam.sq()).sqrt()
    d1B = (p.sq() + g1.sq()).sqrt()
    r12 = IV(2)
    cs = ((u - p).sq() + (v - q).sq()).sqrt()
    cx = ((u + p).sq() + (v - q).sq()).sqrt()
    wA = IV(2) * u
    i_r12 = r12.invcube(); i_d1A = d1A.invcube(); i_d2A = d2A.invcube()
    i_d1B = d1B.invcube(); i_cs = cs.invcube(); i_cx = cx.invcube()
    i_wA = wA.invcube()
    s_r12_d2A = i_r12 - i_d2A
    s_r12_d2B = i_r12 - (p.sq() + (mone - q).sq()).sqrt().invcube()
    s_d1A_wA = i_d1A - i_wA
    s_d1A_cs = i_d1A - i_cs
    s_d1A_cx = i_d1A - i_cx
    s_r12_d1A = i_r12 - i_d1A
    a23 = s_r12_d1A * u * e12
    b13 = IV(-1) * s_r12_d2A * u * e12
    b15 = IV(-1) * s_r12_d2B * p * e12
    JL13mA = IV(-1) * s_d1A_wA * IV(2) * u * h1
    D153 = u * g1 - p * h1
    D154 = IV(-1) * (p * h1 + u * g1)
    JL15mA = s_d1A_cs * D153 + s_d1A_cx * D154
    C1 = b13 * JL15mA - b15 * JL13mA
    return a23 * C1

def main():
    t0 = time.time()
    core = (F(1,4), F(3)), (F(-3), F(3)), (F(1,4), F(3)), (F(-3), F(3))
    stack = [ (core, 0) ]
    certified = discarded = failed = processed = 0
    DEPTH = 14
    certs = []
    while stack:
        (ub, vb, pb, qb), d = stack.pop()
        processed += 1
        # discard boxes wholly inside the excluded band |q - v| < 1/4
        dmin_lo = qb[0] - vb[1]; dmax_hi = qb[1] - vb[0]
        if dmax_hi < F(1,4) and dmin_lo > F(-1,4):
            discarded += 1
            continue
        try:
            M = minor_interval(ub, vb, pb, qb)
            if M.excludes_zero():
                certified += 1
                if len(certs) < 200000:
                    certs.append([[str(x) for x in ub], [str(x) for x in vb],
                                  [str(x) for x in pb], [str(x) for x in qb],
                                  str(M.lo), str(M.hi)])
                continue
        except AssertionError:
            pass  # interval hit a non-sign-definite denominator: bisect
        if d >= DEPTH:
            failed += 1
            continue
        widths = [ub[1]-ub[0], vb[1]-vb[0], pb[1]-pb[0], qb[1]-qb[0]]
        w = widths.index(max(widths))
        boxes = [list(x) for x in (ub, vb, pb, qb)]
        lo, hi = boxes[w]; mid = (lo + hi) / 2
        for half in ((lo, mid), (mid, hi)):
            nb = [tuple(b) for b in boxes]
            nb[w] = half
            stack.append((tuple(nb), d + 1))
        if processed % 20000 == 0:
            print(f"[{time.time()-t0:.0f}s] processed {processed} certified {certified} "
                  f"discarded {discarded} failed {failed} stack {len(stack)}", flush=True)
        if processed > 5_000_000:
            print("P1 BUDGET EXCEEDED"); break
    print(f"DONE {time.time()-t0:.0f}s: processed {processed} certified {certified} "
          f"discarded {discarded} FAILED {failed}")
    (ART / "covering-summary.json").write_text(json.dumps(
        {"processed": processed, "certified": certified, "discarded": discarded,
         "failed": failed, "depth_cap": DEPTH, "seconds": round(time.time()-t0)}),
        encoding="utf-8")
    (ART / "certificates-sample.json").write_text(json.dumps(certs[:5000]), encoding="utf-8")

if __name__ == "__main__":
    main()
