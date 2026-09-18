"""EXP-022 part (d2): the double-collapse covering A_uplow.

Region: u, p BOTH in [0, 1/4], v, q in [-3, 3]. Both mass columns rescaled
(mA x 4u^2, mB x 4p^2), which makes both collapse faces u = 0 and p = 0
(and their intersection) analytic; rows unrescaled. Discards:
  - the four collision corners {u <= 1/16, |v -+ 1| <= 1/16} and
    {p <= 1/16, |q -+ 1| <= 1/16} (single corners: covered by CB1 and its
    Klein images; double clusters: the bi-corner charts),
  - the collision band {|u - p| <= 1/16 and |f| <= 1/16}: its w >= 1/8
    part goes to the tube-extension run (tube.py seed w in [1/8, 7/32]),
    its w < 1/8 part to the deep-tube chart (both declared pending).
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
            u, v, p, q = (IV.raw(*b) for b in args)
            one, two, m1_, Z = IV(1), IV(2), IV(-1), IV(0)
            four, eight = IV(4), IV(8)
            egt = IV(F(1, 8))
        else:
            u, v, p, q = args
            one, two, m1_, Z = DV(1), DV(2), DV(-1), DV(0)
            four, eight = DV(4), DV(8)
            egt = DV(F(1, 8))
        h1 = one - v
        gam = m1_ - v
        g1 = one - q
        g2 = m1_ - q
        f = v - q
        d1A = (u.sq() + h1.sq()).sqrt()
        d2A = (u.sq() + gam.sq()).sqrt()
        d1B = (p.sq() + g1.sq()).sqrt()
        d2B = (p.sq() + g2.sq()).sqrt()
        cs = ((u - p).sq() + f.sq()).sqrt()
        cx = ((u + p).sq() + f.sq()).sqrt()
        def icube(x):
            return K_inv(x * x * x)
        i_d1A = icube(d1A); i_d2A = icube(d2A)
        i_d1B = icube(d1B); i_d2B = icube(d2B)
        i_cs = icube(cs); i_cx = icube(cx)
        u3 = u * u * u
        p3_ = p * p * p
        u2_4 = four * u.sq()
        p2_4 = four * p.sq()
        D135 = p * h1 - u * g1
        D136 = m1_ * (u * g1 + p * h1)
        D153 = u * g1 - p * h1
        D154 = m1_ * (p * h1 + u * g1)
        D235 = p * gam - u * g2
        D236 = m1_ * (u * g2 + p * gam)
        D253 = u * g2 - p * gam
        D254 = m1_ * (p * gam + u * g2)
        J = [[Z] * 4 for _ in range(6)]
        # L13
        J[0][1] = (egt - i_d2A) * (m1_ * two * u)
        J[0][2] = h1 - eight * u3 * h1 * i_d1A
        J[0][3] = p2_4 * ((i_d1B - i_cs) * D135 + (i_d1B - i_cx) * D136)
        # L15
        J[1][1] = (egt - i_d2B) * (m1_ * two * p)
        J[1][2] = u2_4 * ((i_d1A - i_cs) * D153 + (i_d1A - i_cx) * D154)
        J[1][3] = g1 - eight * p3_ * g1 * i_d1B
        # L23
        J[2][0] = (egt - i_d1A) * (two * u)
        J[2][2] = gam - eight * u3 * gam * i_d2A
        J[2][3] = p2_4 * ((i_d2B - i_cs) * D235 + (i_d2B - i_cx) * D236)
        # L25
        J[3][0] = (egt - i_d1B) * (two * p)
        J[3][2] = u2_4 * ((i_d2A - i_cs) * D253 + (i_d2A - i_cx) * D254)
        J[3][3] = g2 - eight * p3_ * g2 * i_d2B
        # L35
        J[4][0] = (i_d1A - i_d1B) * D135
        J[4][1] = (i_d2A - i_d2B) * D235
        J[4][2] = m1_ * f + eight * f * u3 * i_cx
        J[4][3] = f - eight * f * p3_ * i_cx
        # L36
        J[5][0] = (i_d1A - i_d1B) * D136
        J[5][1] = (i_d2A - i_d2B) * D236
        J[5][2] = m1_ * f + eight * f * u3 * i_cs
        J[5][3] = eight * f * p3_ * i_cs - f
        return J
    return entries

def crosscheck():
    import random
    random.seed(61)
    ok = 0
    for _ in range(5):
        uv = F(random.randint(1, 8), 32)
        vv = F(random.randint(-90, 90), 32)
        pv = F(random.randint(1, 8), 32)
        qv = F(random.randint(-90, 90), 32)
        if abs(uv - pv) < F(1, 12) and abs(vv - qv) < F(1, 12):
            qv = vv + F(1, 2)
        pt = [(x, x) for x in (uv, vv, pv, qv)]
        Jc = entry_factory("iv")(pt)
        Jo = pl.r21.entry_matrix((uv, uv), (vv, vv), (pv, pv), (qv, qv))
        colscale = [1, 1, 4 * uv**2, 4 * pv**2]
        good = True
        for i in range(6):
            for j in range(4):
                aiv = Jc[i][j]
                o = Jo[i][j]
                lo = o.lo * colscale[j]
                hi = o.hi * colscale[j]
                if lo > hi:
                    lo, hi = hi, lo
                mid_c = (aiv.lo + aiv.hi) / 2
                mid_o = (lo + hi) / 2
                wid = max(aiv.hi - aiv.lo, hi - lo, F(1, 1 << 30))
                if abs(mid_c - mid_o) > 8 * wid:
                    print(f"MISMATCH row {i} col {j}: {float(mid_c)} vs {float(mid_o)}")
                    good = False
        ok += good
    print(f"crosscheck: {ok}/5 points OK", flush=True)
    return ok == 5

SIXT = F(1, 16)

def discard(box):
    ub, vb, pb, qb = box
    if ub[1] <= SIXT:
        if (vb[0] >= 1 - SIXT and vb[1] <= 1 + SIXT) or \
           (vb[0] >= -1 - SIXT and vb[1] <= -1 + SIXT):
            return True
    if pb[1] <= SIXT:
        if (qb[0] >= 1 - SIXT and qb[1] <= 1 + SIXT) or \
           (qb[0] >= -1 - SIXT and qb[1] <= -1 + SIXT):
            return True
    tlo, thi = ub[0] - pb[1], ub[1] - pb[0]
    flo, fhi = vb[0] - qb[1], vb[1] - qb[0]
    if (thi < SIXT and tlo > -SIXT) and (fhi < SIXT and flo > -SIXT):
        return True                      # collision band: tube-ext / deep-tube
    return False

def main():
    resume = "--resume" in sys.argv
    if not resume and not crosscheck():
        print("crosscheck FAILED, aborting")
        return
    seed = [((F(0), F(1, 4)), (F(-3), F(3)), (F(0), F(1, 4)), (F(-3), F(3)))]
    pl.run_covering(
        "uplow", seed,
        entry_factory("iv"), entry_factory("dv"),
        HERE / "artifacts",
        "E:/_Datos/caos-research/central-configurations/EXP-022",
        discard=discard, depth=44, budget=43200, resume=resume)

if __name__ == "__main__":
    main()
