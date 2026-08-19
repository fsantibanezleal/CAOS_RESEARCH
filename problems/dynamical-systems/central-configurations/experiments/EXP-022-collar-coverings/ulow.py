"""EXP-022 part (c): the pair-collapse covering A_ulow.

Region: u in [0, 1/4], p in [1/4, 3], v, q in [-3, 3], minus
  - the corner tubes {u <= 1/16, |v - 1| <= 1/16} and
    {u <= 1/16, |v + 1| <= 1/16} (pair A collides with an axis body;
    part (d)'s job), and
  - the A_tube sliver {|u - p| < 1/16 and |f| < 1/16} (part (b)'s job;
    its w-range starts exactly at the tube's 7/32).

Chart matrix: the mA column is multiplied by 4u^2, which cancels the
wA^-3 = (2u)^-3 singularity ALGEBRAICALLY (dossier, THE COVERING
PROGRAMME RESTRUCTURE):
  J~[L13][mA] = h1  - 8u^3 h1  d1A^-3      (analytic at u = 0)
  J~[L23][mA] = gam - 8u^3 gam d2A^-3
  J~[L15][mA] = 4u^2 [s(d1A,cs) D153 + s(d1A,cx) D154]
  J~[L25][mA] = 4u^2 [s(d2A,cs) D253 + s(d2A,cx) D254]
  J~[L35][mA] = -f + 8 f u^3 cx^-3
  J~[L36][mA] = -f + 8 f u^3 cs^-3
All other entries are the original formulas (wA appears only in the mA
column). Column scaling by 4u^2 != 0 preserves rank at u > 0; u = 0 is the
collapse face (pair A on the axis), outside the stratum's configuration
space, so certificates on boxes touching u = 0 certify the punctured
collar. A_plow (p -> 0) is the pair-swap image (lemma piece 9d): no run.
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
            eight = IV(8); four = IV(4)
        else:
            u, v, p, q = args
            one, two, m1_, Z = DV(1), DV(2), DV(-1), DV(0)
            eight = DV(8); four = DV(4)
        h1 = one - v
        gam = m1_ - v
        g1 = one - q
        g2 = m1_ - q
        f = v - q
        e12 = two
        d1A = (u.sq() + h1.sq()).sqrt()
        d2A = (u.sq() + gam.sq()).sqrt()
        d1B = (p.sq() + g1.sq()).sqrt()
        d2B = (p.sq() + g2.sq()).sqrt()
        cs = ((u - p).sq() + f.sq()).sqrt()
        cx = ((u + p).sq() + f.sq()).sqrt()
        wB = two * p
        r12 = two
        def icube(x):
            return K_inv(x * x * x)
        i_r12 = icube(r12); i_d1A = icube(d1A); i_d2A = icube(d2A)
        i_d1B = icube(d1B); i_d2B = icube(d2B); i_cs = icube(cs)
        i_cx = icube(cx); i_wB = icube(wB)
        u3 = u * u * u
        D153 = u * g1 - p * h1
        D154 = m1_ * (p * h1 + u * g1)
        D135 = p * h1 - u * g1
        D136 = m1_ * (u * g1 + p * h1)
        D253 = u * g2 - p * gam
        D254 = m1_ * (p * gam + u * g2)
        D235 = p * gam - u * g2
        D236 = m1_ * (u * g2 + p * gam)
        J = [[Z] * 4 for _ in range(6)]
        # L13
        J[0][1] = (i_r12 - i_d2A) * (m1_ * u * e12)
        J[0][2] = h1 - eight * u3 * h1 * i_d1A
        J[0][3] = (i_d1B - i_cs) * D135 + (i_d1B - i_cx) * D136
        # L15
        J[1][1] = (i_r12 - i_d2B) * (m1_ * p * e12)
        J[1][2] = four * u.sq() * ((i_d1A - i_cs) * D153 + (i_d1A - i_cx) * D154)
        J[1][3] = (i_d1B - i_wB) * (m1_ * two * p * g1)
        # L23
        J[2][0] = (i_r12 - i_d1A) * (u * e12)
        J[2][2] = gam - eight * u3 * gam * i_d2A
        J[2][3] = (i_d2B - i_cs) * D235 + (i_d2B - i_cx) * D236
        # L25
        J[3][0] = (i_r12 - i_d1B) * (p * e12)
        J[3][2] = four * u.sq() * ((i_d2A - i_cs) * D253 + (i_d2A - i_cx) * D254)
        J[3][3] = (i_d2B - i_wB) * (m1_ * two * p * g2)
        # L35
        J[4][0] = (i_d1A - i_d1B) * D135
        J[4][1] = (i_d2A - i_d2B) * D235
        J[4][2] = m1_ * f + eight * f * u3 * i_cx
        J[4][3] = (i_cx - i_wB) * (m1_ * two * f * p)
        # L36
        J[5][0] = (i_d1A - i_d1B) * D136
        J[5][1] = (i_d2A - i_d2B) * D236
        J[5][2] = m1_ * f + eight * f * u3 * i_cs
        J[5][3] = (i_cs - i_wB) * (two * f * p)
        return J
    return entries

def crosscheck():
    import random
    random.seed(11)
    ok = 0
    for _ in range(5):
        uv = F(random.randint(1, 8), 32)
        vv = F(random.randint(-90, 90), 32)
        pv = F(random.randint(9, 90), 32)
        qv = F(random.randint(-90, 90), 32)
        if abs(vv - qv) < F(1, 8) and abs(uv - pv) < F(1, 8):
            qv = vv + F(1, 2)
        pt = [(x, x) for x in (uv, vv, pv, qv)]
        Jc = entry_factory("iv")(pt)
        Jo = pl.r21.entry_matrix((uv, uv), (vv, vv), (pv, pv), (qv, qv))
        good = True
        for i in range(6):
            for j in range(4):
                a = Jc[i][j]
                o = Jo[i][j]
                if j == 2:
                    lo, hi = o.lo * 4 * uv**2, o.hi * 4 * uv**2
                else:
                    lo, hi = o.lo, o.hi
                mid_c = (a.lo + a.hi) / 2
                mid_o = (lo + hi) / 2
                wid = max(a.hi - a.lo, hi - lo, F(1, 1 << 34))
                if abs(mid_c - mid_o) > 4 * wid:
                    print(f"MISMATCH row {i} col {j}: {float(mid_c)} vs {float(mid_o)}")
                    good = False
        ok += good
    print(f"crosscheck: {ok}/5 points OK", flush=True)
    return ok == 5

SIXT = F(1, 16)

def discard(box):
    ub, vb, pb, qb = box
    # corner tubes: u <= 1/16 and v within 1/16 of +-1
    if ub[1] <= SIXT:
        if vb[0] >= 1 - SIXT and vb[1] <= 1 + SIXT:
            return True
        if vb[0] >= -1 - SIXT and vb[1] <= -1 + SIXT:
            return True
    # the A_tube sliver
    tlo, thi = ub[0] - pb[1], ub[1] - pb[0]
    flo, fhi = vb[0] - qb[1], vb[1] - qb[0]
    if (thi < SIXT and tlo > -SIXT) and (fhi < SIXT and flo > -SIXT):
        return True
    return False

def main():
    resume = "--resume" in sys.argv
    if not resume and not crosscheck():
        print("crosscheck FAILED, aborting")
        return
    seed = [((F(0), F(1, 4)), (F(-3), F(3)), (F(1, 4), F(3)), (F(-3), F(3)))]
    pl.run_covering(
        "ulow", seed,
        entry_factory("iv"), entry_factory("dv"),
        HERE / "artifacts",
        "E:/_Datos/caos-research/central-configurations/EXP-022",
        discard=discard, depth=44, budget=43200, resume=resume)

if __name__ == "__main__":
    main()
