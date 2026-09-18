"""EXP-022: the DOUBLE-COLLAPSE chart (lemma piece 11, made effective).

Piece 11 proves rank >= 3 on the punctured collar where both mirror pairs
collapse onto the axis, but as a limit statement ("for all sufficiently
small eps"). This chart turns it into certificates: it covers the collar
INCLUDING its face, so no threshold is left implicit.

Chart variables (eps, t, v, q):  u = eps c,  p = eps s,  with
(c, s) = ((1 - t^2), 2t)/(1 + t^2) the rational quarter-circle, t in
[0, 1] (c, s >= 0), and eps = |(u, p)| in [0, 3/8]. Heights v, q free in
[-3, 3].

Column scalings: m1 and m2 by 1/eps (piece 11's mechanism), mA by 4u^2,
mB by 4p^2. Every entry is then analytic on the CLOSED region, because
each carries its eps factor explicitly:

  (L13,m2)/eps = -2c (1/8 - 1/d1A'^3)      d2A = sqrt(eps^2 c^2 + gam^2)
  (L25,m1)/eps =  2s (1/8 - 1/d1B^3)
  (L35,m1)/eps = s(d1A,d1B) (s h1 - c g1)  [Delta135 = eps (s h1 - c g1)]
  (L13,mA)     = h1 - 8 eps^3 c^3 h1 / d1A^3
  (L15,mA)     = 4 eps^3 c^2 [ s(d1A,cs) (c g1 - s h1)
                               - s(d1A,cx) (s h1 + c g1) ]
  (L35,mA)     = -f + 8 f eps^3 c^3 / cx^3        etc.

and cs = sqrt(eps^2 (c-s)^2 + f^2), cx = sqrt(eps^2 (c+s)^2 + f^2) stay
bounded below whenever EITHER of their two contributions does. Discards:
cs < 1/32 (the collision tube's job) and |v -+ 1| < 1/16 or
|q -+ 1| < 1/16 (a pair meeting an axis body: the corner charts' job).
The cs test replaced an earlier |f| < 1/16 test that was too aggressive:
it rejected precisely the region m2's residue occupies, which this chart
certifies directly.
"""
import sys
from fractions import Fraction as F
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("pipeline", HERE / "pipeline.py")
pl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pl)
IV, DV = pl.IV, pl.DV

def dv_inv(x):
    iv = x.v.inv()
    isq = (x.v * x.v).inv()
    return DV(iv, [IV(-1) * isq * g for g in x.g])

def K_inv(x):
    return x.inv() if isinstance(x, IV) else dv_inv(x)

def entry_factory(mode):
    def entries(args):
        if mode == "iv":
            eps, t, v, q = (IV.raw(*b) for b in args)
            one, two, m1_, Z = IV(1), IV(2), IV(-1), IV(0)
            four, eight = IV(4), IV(8)
            egt = IV(F(1, 8))
        else:
            eps, t, v, q = args
            one, two, m1_, Z = DV(1), DV(2), DV(-1), DV(0)
            four, eight = DV(4), DV(8)
            egt = DV(F(1, 8))
        iop = K_inv(one + t.sq())
        c = (one - t.sq()) * iop
        s = two * t * iop
        u = eps * c
        p = eps * s
        h1 = one - v
        gam = m1_ - v
        g1 = one - q
        g2 = m1_ - q
        f = v - q
        d1A = (u.sq() + h1.sq()).sqrt()
        d2A = (u.sq() + gam.sq()).sqrt()
        d1B = (p.sq() + g1.sq()).sqrt()
        d2B = (p.sq() + g2.sq()).sqrt()
        cs = ((eps * (c - s)).sq() + f.sq()).sqrt()
        cx = ((eps * (c + s)).sq() + f.sq()).sqrt()
        def icube(x):
            return K_inv(x * x * x)
        i_d1A = icube(d1A); i_d2A = icube(d2A)
        i_d1B = icube(d1B); i_d2B = icube(d2B)
        i_cs = icube(cs); i_cx = icube(cx)
        e2 = eps.sq()
        e3 = e2 * eps
        c2, s2 = c.sq(), s.sq()
        c3, s3 = c2 * c, s2 * s
        # eps-cleared brackets: Delta135 = eps * B135, etc.
        B135 = s * h1 - c * g1
        B136 = m1_ * (c * g1 + s * h1)
        B153 = c * g1 - s * h1
        B154 = m1_ * (s * h1 + c * g1)
        B235 = s * gam - c * g2
        B236 = m1_ * (c * g2 + s * gam)
        B253 = c * g2 - s * gam
        B254 = m1_ * (s * gam + c * g2)
        J = [[Z] * 4 for _ in range(6)]
        # L13   (m1, m2 columns already divided by eps)
        J[0][1] = m1_ * two * c * (egt - i_d2A)
        J[0][2] = h1 - eight * e3 * c3 * h1 * i_d1A
        J[0][3] = four * e3 * s2 * ((i_d1B - i_cs) * B135 + (i_d1B - i_cx) * B136)
        # L15
        J[1][1] = m1_ * two * s * (egt - i_d2B)
        J[1][2] = four * e3 * c2 * ((i_d1A - i_cs) * B153 + (i_d1A - i_cx) * B154)
        J[1][3] = g1 - eight * e3 * s3 * g1 * i_d1B
        # L23
        J[2][0] = two * c * (egt - i_d1A)
        J[2][2] = gam - eight * e3 * c3 * gam * i_d2A
        J[2][3] = four * e3 * s2 * ((i_d2B - i_cs) * B235 + (i_d2B - i_cx) * B236)
        # L25
        J[3][0] = two * s * (egt - i_d1B)
        J[3][2] = four * e3 * c2 * ((i_d2A - i_cs) * B253 + (i_d2A - i_cx) * B254)
        J[3][3] = g2 - eight * e3 * s3 * g2 * i_d2B
        # L35
        J[4][0] = (i_d1A - i_d1B) * B135
        J[4][1] = (i_d2A - i_d2B) * B235
        J[4][2] = m1_ * f + eight * f * e3 * c3 * i_cx
        J[4][3] = f - eight * f * e3 * s3 * i_cx
        # L36
        J[5][0] = (i_d1A - i_d1B) * B136
        J[5][1] = (i_d2A - i_d2B) * B236
        J[5][2] = m1_ * f + eight * f * e3 * c3 * i_cs
        J[5][3] = eight * f * e3 * s3 * i_cs - f
        return J
    return entries

def crosscheck():
    import random
    random.seed(211)
    ok = tried = 0
    while tried < 5:
        ev = F(random.randint(1, 24), 64)
        tv = F(random.randint(1, 60), 64)
        vv = F(random.randint(-90, 90), 32)
        qv = F(random.randint(-90, 90), 32)
        o = 1 + tv * tv
        cv = (1 - tv * tv) / o
        sv = 2 * tv / o
        if cv <= 0 or sv <= 0 or abs(vv - qv) < F(1, 8):
            continue
        uv, pv = ev * cv, ev * sv
        if uv <= 0 or pv <= 0:
            continue
        tried += 1
        pt = [(x, x) for x in (ev, tv, vv, qv)]
        Jc = entry_factory("iv")(pt)
        Jo = pl.r21.entry_matrix((uv, uv), (vv, vv), (pv, pv), (qv, qv))
        colscale = [F(1, 1) / ev, F(1, 1) / ev, 4 * uv**2, 4 * pv**2]
        good = True
        for i in range(6):
            for j in range(4):
                a = Jc[i][j]
                o2 = Jo[i][j]
                lo = o2.lo * colscale[j]
                hi = o2.hi * colscale[j]
                if lo > hi:
                    lo, hi = hi, lo
                mid_c = (a.lo + a.hi) / 2
                mid_o = (lo + hi) / 2
                wid = max(a.hi - a.lo, hi - lo, F(1, 1 << 28))
                if abs(mid_c - mid_o) > 8 * wid:
                    print(f"MISMATCH row {i} col {j}: {float(mid_c)} vs {float(mid_o)}")
                    good = False
        ok += good
    print(f"crosscheck: {ok}/5 points OK", flush=True)
    return ok == 5

SIXT = F(1, 16)

def discard(box):
    """Discard only the TRUE cs-collision (a body of pair A meeting one of
    pair B), not every small |f|: cs^2 = eps^2 (c - s)^2 + f^2 stays
    bounded below whenever EITHER factor does. The earlier |f| < 1/16 test
    was too aggressive and rejected exactly the region m2's residue lives
    in (u ~ p ~ 2e-5 with the heights separated by 0.037)."""
    eb, tb, vb, qb = box
    e, tt = IV.raw(*eb), IV.raw(*tb)
    one, two = IV(1), IV(2)
    iop = (one + tt.sq()).inv()
    c = (one - tt.sq()) * iop
    s = two * tt * iop
    fiv = IV.raw(vb[0], vb[1]) - IV.raw(qb[0], qb[1])
    cs2 = (e * (c - s)).sq() + fiv.sq()
    if cs2.hi < F(1, 1024):              # cs < 1/32 : the collision tube
        return True
    for xb in (vb, qb):
        if xb[0] >= 1 - SIXT and xb[1] <= 1 + SIXT:
            return True                  # a pair at an axis body: corner charts
        if xb[0] >= -1 - SIXT and xb[1] <= -1 + SIXT:
            return True
    return False

def main():
    resume = "--resume" in sys.argv
    if not resume and not crosscheck():
        print("crosscheck FAILED, aborting")
        return
    seed = [((F(0), F(3, 8)), (F(0), F(1)), (F(-3), F(3)), (F(-3), F(3)))]
    pl.run_covering(
        "collapse", seed,
        entry_factory("iv"), entry_factory("dv"),
        HERE / "artifacts",
        "E:/_Datos/caos-research/central-configurations/EXP-022",
        discard=discard, depth=44, budget=43200, resume=resume)

if __name__ == "__main__":
    main()
