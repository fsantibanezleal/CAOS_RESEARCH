"""EXP-022 part (d4): bi-corner chart, OPPOSITE bodies (A at 2, B at 1).

Chart variables (rhoa, taua, rhob, taub): d2A = rhoa and d1B = rhob
EXACTLY: (u, v) = (rhoa ca, -1 + rhoa sa), (p, q) = (rhob cb, 1 + rhob sb)
with (cX, sX) = ((1 - tauX^2), 2 tauX)/(1 + tauX^2). Region rhoa, rhob in
[0, 3/32], tauX in [-1, 1]. The pairs sit near OPPOSITE axis bodies, so
cs, cx ~ 2: no internal collision and no deeper level. The region is
self-paired under swap-mirror, so one chart covers it; the same-body
bi-corner is separate.

Row scalings (rhoa^2, 1/rhob, 1/rhoa, rhob^2, rhoa^2 rhob^2,
rhoa^2 rhob^2); columns mA x 4u^2, mB x 4p^2. Exact clearings:
  h1 = 2 - rhoa sa, gam = -rhoa sa, g1 = -rhob sb, g2 = -2 - rhob sb,
  Delta135 =  rhob K135,  K135 = cb h1 + rhoa ca sb,
  Delta136 = -rhob K154,  K154 = cb h1 - rhoa ca sb,
  Delta235 =  rhoa K235,  K235 = ca (2 + rhob sb) - rhob cb sa,
  Delta236 =  rhoa K236,  K236 = ca (2 + rhob sb) + rhob cb sa,
  u^3/d2A^3 = ca^3,  p^3/d1B^3 = cb^3.
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
            ra, ta, rb, tb = (IV.raw(*b) for b in args)
            one, two, m1_, Z = IV(1), IV(2), IV(-1), IV(0)
            four, eight = IV(4), IV(8)
            quarter, egt = IV(F(1, 4)), IV(F(1, 8))
        else:
            ra, ta, rb, tb = args
            one, two, m1_, Z = DV(1), DV(2), DV(-1), DV(0)
            four, eight = DV(4), DV(8)
            quarter, egt = DV(F(1, 4)), DV(F(1, 8))
        ioa = K_inv(one + ta.sq())
        ca = (one - ta.sq()) * ioa
        sa = two * ta * ioa
        iob = K_inv(one + tb.sq())
        cb = (one - tb.sq()) * iob
        sb = two * tb * iob
        u = ra * ca
        p = rb * cb
        h1 = two - ra * sa
        g2 = m1_ * two - rb * sb
        f = m1_ * two + ra * sa - rb * sb
        d1A = (u.sq() + h1.sq()).sqrt()
        d2B = (p.sq() + (two + rb * sb).sq()).sqrt()
        cs = ((u - p).sq() + f.sq()).sqrt()
        cx = ((u + p).sq() + f.sq()).sqrt()
        def icube(x):
            return K_inv(x * x * x)
        id1A = icube(d1A); id2B = icube(d2B)
        ics = icube(cs); icx = icube(cx)
        ra2 = ra.sq(); ra3 = ra2 * ra
        rb2 = rb.sq(); rb3 = rb2 * rb
        ca3 = ca * ca * ca
        cb3 = cb * cb * cb
        K135 = cb * h1 + ra * ca * sb
        K154 = cb * h1 - ra * ca * sb
        K235 = ca * (two + rb * sb) - rb * cb * sa
        K236 = ca * (two + rb * sb) + rb * cb * sa
        u2_4 = four * u.sq()
        cb2_4 = four * cb.sq()
        ca2_4 = four * ca.sq()
        J = [[Z] * 4 for _ in range(6)]
        # L13 (x rhoa^2)
        J[0][1] = two * ca - ra3 * ca * quarter
        J[0][2] = ra2 * h1 * (one - eight * ra3 * ca3 * id1A)
        J[0][3] = ra2 * (cb2_4 * (K135 - K154)
                         - rb3 * cb2_4 * (ics * K135 - icx * K154))
        # L15 (/ rhob)
        J[1][1] = m1_ * two * cb * (egt - id2B)
        J[1][2] = m1_ * u2_4 * ((id1A - ics) * K135 + (id1A - icx) * K154)
        J[1][3] = m1_ * sb * (one - eight * cb3)
        # L23 (/ rhoa)
        J[2][0] = two * ca * (egt - id1A)
        J[2][2] = m1_ * sa * (one - eight * ca3)
        J[2][3] = rb2 * cb2_4 * ((id2B - ics) * K235 + (id2B - icx) * K236)
        # L25 (x rhob^2)
        J[3][0] = rb3 * cb * quarter - two * cb
        J[3][2] = rb2 * (ca2_4 * (K236 - K235)
                         + ra3 * ca2_4 * (ics * K235 - icx * K236))
        J[3][3] = rb2 * g2 * (one - eight * rb3 * cb3 * id2B)
        # L35 (x rhoa^2 rhob^2)
        J[4][0] = ra2 * (rb3 * id1A * K135 - K135)
        J[4][1] = rb2 * (K235 - ra3 * id2B * K235)
        J[4][2] = ra2 * rb2 * f * (eight * ra3 * ca3 * icx - one)
        J[4][3] = ra2 * rb2 * f * (one - eight * rb3 * cb3 * icx)
        # L36 (x rhoa^2 rhob^2)
        J[5][0] = ra2 * (K154 - rb3 * id1A * K154)
        J[5][1] = rb2 * (K236 - ra3 * id2B * K236)
        J[5][2] = ra2 * rb2 * f * (eight * ra3 * ca3 * ics - one)
        J[5][3] = ra2 * rb2 * f * (eight * rb3 * cb3 * ics - one)
        return J
    return entries

def crosscheck():
    import random
    random.seed(97)
    ok = 0
    for _ in range(5):
        rav = F(random.randint(1, 12), 128)
        tav = F(random.randint(-30, 30), 32)
        rbv = F(random.randint(1, 12), 128)
        tbv = F(random.randint(-30, 30), 32)
        oa = 1 + tav * tav
        cav = (1 - tav * tav) / oa
        sav = 2 * tav / oa
        ob = 1 + tbv * tbv
        cbv = (1 - tbv * tbv) / ob
        sbv = 2 * tbv / ob
        if cav == 0 or cbv == 0:
            continue
        uv = rav * cav
        vv = -1 + rav * sav
        pv = rbv * cbv
        qv = 1 + rbv * sbv
        pt = [(x, x) for x in (rav, tav, rbv, tbv)]
        Jc = entry_factory("iv")(pt)
        Jo = pl.r21.entry_matrix((uv, uv), (vv, vv), (pv, pv), (qv, qv))
        rowscale = [rav**2, F(1, 1) / rbv, F(1, 1) / rav, rbv**2,
                    rav**2 * rbv**2, rav**2 * rbv**2]
        colscale = [1, 1, 4 * uv**2, 4 * pv**2]
        good = True
        for i in range(6):
            for j in range(4):
                aiv = Jc[i][j]
                o = Jo[i][j]
                lo = o.lo * rowscale[i] * colscale[j]
                hi = o.hi * rowscale[i] * colscale[j]
                if lo > hi:
                    lo, hi = hi, lo
                mid_c = (aiv.lo + aiv.hi) / 2
                mid_o = (lo + hi) / 2
                wid = max(aiv.hi - aiv.lo, hi - lo, F(1, 1 << 24))
                if abs(mid_c - mid_o) > 8 * wid:
                    print(f"MISMATCH row {i} col {j}: {float(mid_c)} vs {float(mid_o)}")
                    good = False
        ok += good
    print(f"crosscheck: {ok}/5 points OK", flush=True)
    return ok == 5

def main():
    resume = "--resume" in sys.argv
    if not resume and not crosscheck():
        print("crosscheck FAILED, aborting")
        return
    seed = [((F(0), F(3, 32)), (F(-1), F(1)), (F(0), F(3, 32)), (F(-1), F(1)))]
    pl.run_covering(
        "bicorner-opp", seed,
        entry_factory("iv"), entry_factory("dv"),
        HERE / "artifacts",
        "E:/_Datos/caos-research/central-configurations/EXP-022",
        depth=44, budget=21600, resume=resume)

if __name__ == "__main__":
    main()
