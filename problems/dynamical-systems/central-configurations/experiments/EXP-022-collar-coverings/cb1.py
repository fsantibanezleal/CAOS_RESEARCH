"""EXP-022 part (d), chart CB1: pair B collides with axis body 1, A bounded.

Chart variables (rhoc, tauc, u, v): d1B = rhoc EXACTLY,
(csig, ssig) = ((1 - tauc^2), 2 tauc)/(1 + tauc^2), p = rhoc csig,
q = 1 + rhoc ssig. Region: rhoc in [0, 3/32] (covers the discarded corner
tubes: sqrt2/16 < 3/32), tauc in [-1, 1], u in [0, 3], v in [-3, 3].
Discards: {u <= 1/8 and |v - 1| <= 1/8} (the A-B double cluster near body
1, where cs can vanish; deferred, declared) and {u <= 1/16 and
|v + 1| <= 1/16} (the standard A-corner at body 2, ditto).

Row scalings (1, 1/rhoc, 1, rhoc^2, rhoc^2, rhoc^2) for (L13, L15, L23,
L25, L35, L36); columns mA x 4u^2, mB x 4p^2. Exact clearings:
  g1 = -rhoc ssig,     Delta135 = rhoc D^135,  D^135 = csig h1 + u ssig,
  Delta136 = -rhoc D^136,  D^136 = csig h1 - u ssig,  p^3/rhoc^3 = csig^3.
Face rank at rhoc = 0 is 4 off codimension-1 sets ({csig = 0}, {ssig = 0},
{csig = 1/2}, equidistance sets): rows collapse to
(0,-2u s(r12,d2A), h1(...), 8 csig^2 u ssig), (0,0,0,-ssig(1-8csig^3)),
(2u s(r12,d1A), 0, gam(...), 0), (-2csig,0,0,0), which is generically
independent. The mirror image (B at body 2) is free by piece 9e; the swap
images (A at an axis body) by piece 9d; the far-(u,v) composition is the
separate chart CB1F (next).
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
            rc, tc, u, v = (IV.raw(*b) for b in args)
            one, two, m1_, Z = IV(1), IV(2), IV(-1), IV(0)
            four, eight = IV(4), IV(8)
            egt = IV(F(1, 8))
        else:
            rc, tc, u, v = args
            one, two, m1_, Z = DV(1), DV(2), DV(-1), DV(0)
            four, eight = DV(4), DV(8)
            egt = DV(F(1, 8))
        iop = K_inv(one + tc.sq())
        csig = (one - tc.sq()) * iop
        ssig = two * tc * iop
        p = rc * csig
        h1 = one - v
        gam = m1_ - v
        g2 = m1_ * two - rc * ssig          # -2 - rhoc ssig
        fmb = (v - one) - rc * ssig          # f = v - q
        d1A = (u.sq() + h1.sq()).sqrt()
        d2A = (u.sq() + gam.sq()).sqrt()
        d2B = ((rc * csig).sq() + (two + rc * ssig).sq()).sqrt()
        cs = ((u - p).sq() + fmb.sq()).sqrt()
        cx = ((u + p).sq() + fmb.sq()).sqrt()
        def icube(x):
            return K_inv(x * x * x)
        id1A = icube(d1A); id2A = icube(d2A); id2B = icube(d2B)
        ics = icube(cs); icx = icube(cx)
        rc2 = rc.sq()
        rc3 = rc2 * rc
        u3 = u * u * u
        u2_4 = four * u.sq()
        cs3 = csig * csig * csig
        D135 = csig * h1 + u * ssig
        D136 = csig * h1 - u * ssig
        # Delta235 = p gam - u g2 = rhoc csig gam + u (2 + rhoc ssig)
        Dl235 = rc * csig * gam + u * (two + rc * ssig)
        # Delta236 = -(u g2 + p gam) = u (2 + rhoc ssig) - rhoc csig gam
        Dl236 = u * (two + rc * ssig) - rc * csig * gam
        s12_d2A = egt - id2A
        s12_d1A = egt - id1A
        s12_d2B = egt - id2B
        sd2Ad2B = id2A - id2B
        J = [[Z] * 4 for _ in range(6)]
        # L13 (x 1)
        J[0][1] = m1_ * two * u * s12_d2A
        J[0][2] = h1 * (one - eight * u3 * id1A)
        J[0][3] = four * csig.sq() * (D135 - D136) \
            - four * rc3 * csig.sq() * (ics * D135 - icx * D136)
        # L15 (/ rhoc)
        J[1][1] = m1_ * two * csig * s12_d2B
        J[1][2] = m1_ * u2_4 * ((id1A - ics) * D135 + (id1A - icx) * D136)
        J[1][3] = m1_ * ssig * (one - eight * cs3)
        # L23 (x 1)
        J[2][0] = two * u * s12_d1A
        J[2][2] = gam * (one - eight * u3 * id2A)
        J[2][3] = four * rc2 * csig.sq() * ((id2B - ics) * Dl235 + (id2B - icx) * Dl236)
        # L25 (x rhoc^2)
        J[3][0] = csig * (rc3 * F(1, 4) - two) if mode == "iv" else \
            csig * (rc3 * DV(F(1, 4)) - two)
        J[3][2] = rc2 * u2_4 * (m1_ * (id2A - ics) * Dl235 + (id2A - icx) * Dl236)
        J[3][3] = rc2 * g2 * (one - eight * rc3 * cs3 * id2B)
        # L35 (x rhoc^2)
        J[4][0] = rc3 * id1A * D135 - D135
        J[4][1] = rc2 * sd2Ad2B * Dl235
        J[4][2] = rc2 * fmb * (eight * u3 * icx - one)
        J[4][3] = rc2 * fmb * (one - eight * rc3 * cs3 * icx)
        # L36 (x rhoc^2)
        J[5][0] = D136 - rc3 * id1A * D136
        J[5][1] = rc2 * sd2Ad2B * Dl236
        J[5][2] = rc2 * fmb * (eight * u3 * ics - one)
        J[5][3] = rc2 * fmb * (eight * rc3 * cs3 * ics - one)
        return J
    return entries

def crosscheck():
    import random
    random.seed(53)
    ok = 0
    for _ in range(5):
        rcv = F(random.randint(1, 12), 128)
        tcv = F(random.randint(-30, 30), 32)
        uv = F(random.randint(20, 90), 32)
        vv = F(random.randint(-90, 90), 32)
        opp = 1 + tcv * tcv
        csv = (1 - tcv * tcv) / opp
        ssv = 2 * tcv / opp
        pv = rcv * csv
        qv = 1 + rcv * ssv
        if pv == 0:
            continue
        pt = [(x, x) for x in (rcv, tcv, uv, vv)]
        Jc = entry_factory("iv")(pt)
        Jo = pl.r21.entry_matrix((uv, uv), (vv, vv), (pv, pv), (qv, qv))
        rowscale = [1, F(1, 1) / rcv, 1, rcv**2, rcv**2, rcv**2]
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
                wid = max(aiv.hi - aiv.lo, hi - lo, F(1, 1 << 26))
                if abs(mid_c - mid_o) > 8 * wid:
                    print(f"MISMATCH row {i} col {j}: {float(mid_c)} vs {float(mid_o)}")
                    good = False
        ok += good
    print(f"crosscheck: {ok}/5 points OK", flush=True)
    return ok == 5

def discard(box):
    rcb, tcb, ub, vb = box
    if ub[1] <= F(1, 8) and vb[0] >= F(7, 8) and vb[1] <= F(9, 8):
        return True                      # A-B double cluster near body 1
    if ub[1] <= F(1, 16) and vb[0] >= F(-17, 16) and vb[1] <= F(-15, 16):
        return True                      # A-corner at body 2
    return False

def main():
    resume = "--resume" in sys.argv
    if not resume and not crosscheck():
        print("crosscheck FAILED, aborting")
        return
    seed = [((F(0), F(3, 32)), (F(-1), F(1)), (F(0), F(3)), (F(-3), F(3)))]
    pl.run_covering(
        "cb1", seed,
        entry_factory("iv"), entry_factory("dv"),
        HERE / "artifacts",
        "E:/_Datos/caos-research/central-configurations/EXP-022",
        discard=discard, depth=44, budget=43200, resume=resume)

if __name__ == "__main__":
    main()
