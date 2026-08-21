"""EXP-022 part (d3), chart CB1F: pair B at axis body 1, pair A FAR.

Composition of fa1 (A-side inversion: eps = 1/R_A, direction (a, b) =
((1-tau^2), 2tau)/(1+tau^2), rows L13/L23/L35/L36 x eps, mA x 4u^2) with
CB1 (B-side corner blow-up: d1B = rhoc exactly, (csig, ssig) from tauc,
p = rhoc csig, q = 1 + rhoc ssig, mB x 4p^2, L15 / rhoc, L25/L35/L36
x rhoc^2). Region: rhoc in [0, 3/32], tauc in [-1, 1], eps in [0, 1/3],
tau in [-1, 1]. Exact clearings (both verified in the crosscheck):
  g1 = -rhoc ssig,
  T135 = p(eps - b) - a g1 = rhoc T^135,  T^135 = csig(eps - b) + a ssig,
  T136 = T154 = -(p(eps-b) + a g1) = -rhoc T^136, T^136 = csig(eps-b) - a ssig.
Row scalings (eps, 1/rhoc, eps, rhoc^2, eps rhoc^2, eps rhoc^2); columns
mA x 4u^2, mB x 4p^2. Face rank 4 off codimension-1 sets. No discards:
the region's other singular sets (A-corners, A-B cluster) cannot occur
(A is at radius >= 3, B within 3/32 of body 1, so cs, cx >= 2 in the
unrescaled geometry; Cs, Cx >= 1 - eps R_B > 0.9 in chart form).
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
            rc, tc, eps, tau = (IV.raw(*b) for b in args)
            one, two, m1_, Z = IV(1), IV(2), IV(-1), IV(0)
            four, eight = IV(4), IV(8)
            quarter, egt = IV(F(1, 4)), IV(F(1, 8))
        else:
            rc, tc, eps, tau = args
            one, two, m1_, Z = DV(1), DV(2), DV(-1), DV(0)
            four, eight = DV(4), DV(8)
            quarter, egt = DV(F(1, 4)), DV(F(1, 8))
        ioc = K_inv(one + tc.sq())
        csig = (one - tc.sq()) * ioc
        ssig = two * tc * ioc
        iop = K_inv(one + tau.sq())
        a = (one - tau.sq()) * iop
        b = two * tau * iop
        emb = eps - b
        # B-side quantities
        g2 = m1_ * two - rc * ssig
        # A-side normalized distances (fa1 forms with (p, q) = corner)
        D1A = (a.sq() + emb.sq()).sqrt()
        D2A = (a.sq() + (eps + b).sq()).sqrt()
        p_ = rc * csig
        q_ = one + rc * ssig
        bq = b - eps * q_                 # eps * f
        Cs = ((a - eps * p_).sq() + bq.sq()).sqrt()
        Cx = ((a + eps * p_).sq() + bq.sq()).sqrt()
        d2B = (p_.sq() + (two + rc * ssig).sq()).sqrt()
        def icube(x):
            return K_inv(x * x * x)
        iD1A = icube(D1A); iD2A = icube(D2A)
        iCs = icube(Cs); iCx = icube(Cx)
        id2B = icube(d2B)
        e3 = eps * eps * eps
        rc2 = rc.sq()
        rc3 = rc2 * rc
        a3 = a * a * a
        cs3 = csig * csig * csig
        a2_4 = four * a.sq()
        Th135 = csig * emb + a * ssig
        Th136 = csig * emb - a * ssig
        # T235 = p gam ... in fa1 chart form: T235 = -p(eps+b) - a g2 -> here
        # T235 = eps eps_B... : use fa1's bracket with corner values:
        # fa1 T235 = m1_*p*epb - a*g2  (epb = eps + b)
        T235 = m1_ * p_ * (eps + b) - a * g2
        T236 = m1_ * a * g2 + p_ * (eps + b)
        J = [[Z] * 4 for _ in range(6)]
        # L13 (x eps)
        J[0][1] = m1_ * a * quarter + two * a * e3 * iD2A
        J[0][2] = emb * (one - eight * a3 * iD1A)
        J[0][3] = eight * csig.sq() * a * ssig \
            - four * rc3 * e3 * csig.sq() * (iCs * Th135 - iCx * Th136)
        # L15 (/ rhoc)
        # cancellation-free (d2B -> 2 on the corner face); d2B^2 - 4 exact:
        s12_d2B = pl.s_r12_factored(rc * (four * ssig + rc), d2B,
                                    K_inv, one, two, four, eight)
        J[1][1] = m1_ * two * csig * s12_d2B
        J[1][2] = m1_ * a2_4 * ((iD1A - iCs) * Th135 + (iD1A - iCx) * Th136)
        J[1][3] = m1_ * ssig * (one - eight * cs3)
        # L23 (x eps)
        J[2][0] = a * quarter - two * a * e3 * iD1A
        J[2][2] = m1_ * (eps + b) * (one - eight * a3 * iD2A)
        J[2][3] = four * rc2 * csig.sq() * ((id2B - e3 * iCs) * T235 + (id2B - e3 * iCx) * T236)
        # L25 (x rhoc^2)
        J[3][0] = csig * (rc3 * quarter - two)
        J[3][2] = rc2 * a2_4 * (m1_ * (iD2A - iCs) * T235 + (iD2A - iCx) * T236)
        J[3][3] = rc2 * g2 * (one - eight * rc3 * cs3 * id2B)
        # L35 (x eps rhoc^2)
        J[4][0] = e3 * iD1A * rc3 * Th135 - Th135
        J[4][1] = rc2 * (e3 * iD2A - id2B) * T235
        J[4][2] = rc2 * bq * (eight * a3 * iCx - one)
        J[4][3] = rc2 * bq * (one - eight * rc3 * cs3 * e3 * iCx)
        # L36 (x eps rhoc^2)
        J[5][0] = Th136 - e3 * iD1A * rc3 * Th136
        J[5][1] = rc2 * (e3 * iD2A - id2B) * T236
        J[5][2] = rc2 * bq * (eight * a3 * iCs - one)
        J[5][3] = rc2 * bq * (eight * rc3 * cs3 * e3 * iCs - one)
        return J
    return entries

def crosscheck():
    import random
    random.seed(71)
    ok = 0
    for _ in range(5):
        rcv = F(random.randint(1, 12), 128)
        tcv = F(random.randint(-30, 30), 32)
        ev = F(random.randint(1, 10), 32)
        tv = F(random.randint(-30, 30), 32)
        opp = 1 + tcv * tcv
        csv = (1 - tcv * tcv) / opp
        ssv = 2 * tcv / opp
        opp2 = 1 + tv * tv
        av = (1 - tv * tv) / opp2
        bv = 2 * tv / opp2
        if av == 0 or csv == 0:
            continue
        pv = rcv * csv
        qv = 1 + rcv * ssv
        uv = av / ev
        vv = bv / ev
        pt = [(x, x) for x in (rcv, tcv, ev, tv)]
        Jc = entry_factory("iv")(pt)
        Jo = pl.r21.entry_matrix((uv, uv), (vv, vv), (pv, pv), (qv, qv))
        rowscale = [ev, F(1, 1) / rcv, ev, rcv**2, ev * rcv**2, ev * rcv**2]
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
    seed = [((F(0), F(3, 32)), (F(-1), F(1)), (F(0), F(1, 3)), (F(-1), F(1)))]
    pl.run_covering(
        "cb1f", seed,
        entry_factory("iv"), entry_factory("dv"),
        HERE / "artifacts",
        "E:/_Datos/caos-research/central-configurations/EXP-022",
        depth=44, budget=43200, resume=resume)

if __name__ == "__main__":
    main()
