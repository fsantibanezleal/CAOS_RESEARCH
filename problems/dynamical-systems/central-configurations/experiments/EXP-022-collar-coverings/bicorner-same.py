"""EXP-022 part (d5): bi-corner chart, SAME body (A and B both at body 1).

Chart variables (rhoa, taua, rr, taub): d1A = rhoa, d1B = rr rhoa EXACTLY
(rr = rhob/rhoa in [0, 1]; rr > 1 is the swap image): (u, v) = (rhoa ca,
1 + rhoa sa), (p, q) = (rr rhoa cb, 1 + rr rhoa sb). Region rhoa in
[0, 3/16] (covers cb1's double-cluster discard, d1A <= sqrt2/8 < 3/16),
taua, taub in [-1, 1]. The internal separations scale exactly:
cs = rhoa CSc, CSc = |dirA - rr dirB|; cx = rhoa CXc,
CXc = |dirA + rr dirB^m|; both vanish only on the quadruple-cluster set
(rr = 1, dirA = dirB and the vertical corner): DISCARDED as
{CSc < 1/16} u {CXc < 1/16} (the quadruple-cluster chart, declared
pending). Exact brackets (Wronskian forms):
  Delta135 = rr rhoa^2 W1,  W1 = ca sb - cb sa,
  Delta136 = Delta154 = rr rhoa^2 W2,  W2 = ca sb + cb sa  (signs below),
  Delta235 = rhoa K5, K5 = 2(ca - rr cb) + rr rhoa W1,
  Delta254 = rhoa K6, K6 = 2(ca + rr cb) + rr rhoa W2,
  f = rhoa Fc, Fc = sa - rr sb,  u^3/d1A^3 = ca^3, p^3/d1B^3 = cb^3.
Row scalings (1/rhoa, 1/rhoa, rhoa^2, rr^2 rhoa^2, rhoa rr^2,
rhoa rr^2); columns mA x 4u^2, mB x 4p^2.
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
            ra, ta, rr, tb = (IV.raw(*b) for b in args)
            one, two, m1_, Z = IV(1), IV(2), IV(-1), IV(0)
            four, eight = IV(4), IV(8)
            quarter, egt = IV(F(1, 4)), IV(F(1, 8))
        else:
            ra, ta, rr, tb = args
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
        h1 = m1_ * ra * sa                    # 1 - v = -rhoa sa
        gam = m1_ * two - ra * sa
        g2 = m1_ * two - rr * ra * sb
        d2A = (u.sq() + gam.sq()).sqrt()
        p = rr * ra * cb
        d2B = (p.sq() + (two + rr * ra * sb).sq()).sqrt()
        CSc = ((ca - rr * cb).sq() + (sa - rr * sb).sq()).sqrt()
        CXc = ((ca + rr * cb).sq() + (sa - rr * sb).sq()).sqrt()
        def icube(x):
            return K_inv(x * x * x)
        id2A = icube(d2A); id2B = icube(d2B)
        iCSc = icube(CSc); iCXc = icube(CXc)
        ra2 = ra.sq(); ra3 = ra2 * ra
        rr2 = rr.sq(); rr3 = rr2 * rr
        ca3 = ca * ca * ca
        cb3 = cb * cb * cb
        W1 = ca * sb - cb * sa
        W2 = ca * sb + cb * sa
        K5 = two * (ca - rr * cb) + rr * ra * W1
        K6 = two * (ca + rr * cb) + rr * ra * W2
        Fc = sa - rr * sb
        J = [[Z] * 4 for _ in range(6)]
        # L13 (/ rhoa)
        J[0][1] = m1_ * two * ca * (egt - id2A)
        J[0][2] = m1_ * sa * (one - eight * ca3)
        J[0][3] = four * cb.sq() * ((one - rr3 * iCSc) * W1
                                    + (one - rr3 * iCXc) * W2)
        # L15 (/ rhoa)
        J[1][1] = m1_ * two * rr * cb * (egt - id2B)
        J[1][2] = four * rr * ca.sq() * ((iCSc - one) * W1 + (one - iCXc) * W2)
        J[1][3] = m1_ * rr * sb * (one - eight * cb3)
        # L23 (x rhoa^2)
        J[2][0] = ra3 * ca * quarter - two * ca
        J[2][2] = ra2 * gam * (one - eight * ra3 * ca3 * id2A)
        # 4p^2 [s(d2B,cs) D235 + s(d2B,cx) D236] x rhoa^2, D235 = rhoa K5,
        # D236 = rhoa K6, s(d2B,cs) = id2B - iCSc/rhoa^3:
        J[2][3] = ra2 * four * rr2 * cb.sq() * (
            ra3 * id2B * (K5 + K6) - (iCSc * K5 + iCXc * K6))
        # L25 (x rr^2 rhoa^2)
        J[3][0] = rr3 * ra3 * cb * quarter - two * cb
        J[3][2] = rr2 * ra2 * (four * ca.sq() * (iCSc * K5 - iCXc * K6)
                               + four * ra3 * ca.sq() * id2A * (K6 - K5))
        J[3][3] = rr2 * ra2 * g2 * (one - eight * rr3 * ra3 * cb3 * id2B)
        # L35 (x rhoa rr^2)
        J[4][0] = (rr3 - one) * W1
        J[4][1] = ra2 * rr2 * (id2A - id2B) * K5
        J[4][2] = ra2 * rr2 * Fc * (eight * ca3 * iCXc - one)
        J[4][3] = ra2 * rr2 * Fc * (one - eight * rr3 * cb3 * iCXc)
        # L36 (x rhoa rr^2)
        J[5][0] = (rr3 - one) * W2
        J[5][1] = ra2 * rr2 * (id2A - id2B) * K6
        J[5][2] = ra2 * rr2 * Fc * (eight * ca3 * iCSc - one)
        J[5][3] = ra2 * rr2 * Fc * (eight * rr3 * cb3 * iCSc - one)
        return J
    return entries

def crosscheck():
    import random
    random.seed(101)
    ok = 0
    for _ in range(5):
        rav = F(random.randint(1, 20), 128)
        tav = F(random.randint(-30, 30), 32)
        rrv = F(random.randint(1, 31), 32)
        tbv = F(random.randint(-30, 30), 32)
        oa = 1 + tav * tav
        cav = (1 - tav * tav) / oa
        sav = 2 * tav / oa
        ob = 1 + tbv * tbv
        cbv = (1 - tbv * tbv) / ob
        sbv = 2 * tbv / ob
        if cav == 0 or cbv == 0:
            continue
        csc2 = (cav - rrv * cbv)**2 + (sav - rrv * sbv)**2
        if csc2 < F(1, 64):
            continue
        uv = rav * cav
        vv = 1 + rav * sav
        pv = rrv * rav * cbv
        qv = 1 + rrv * rav * sbv
        pt = [(x, x) for x in (rav, tav, rrv, tbv)]
        Jc = entry_factory("iv")(pt)
        Jo = pl.r21.entry_matrix((uv, uv), (vv, vv), (pv, pv), (qv, qv))
        rowscale = [F(1, 1) / rav, F(1, 1) / rav, rav**2, rrv**2 * rav**2,
                    rav * rrv**2, rav * rrv**2]
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
                wid = max(aiv.hi - aiv.lo, hi - lo, F(1, 1 << 22))
                if abs(mid_c - mid_o) > 8 * wid:
                    print(f"MISMATCH row {i} col {j}: {float(mid_c)} vs {float(mid_o)}")
                    good = False
        ok += good
    print(f"crosscheck: {ok}/5 points OK", flush=True)
    return ok == 5

SIXT = F(1, 16)

def discard(box):
    rab, tab, rrb, tbb = box
    ta, rr, tb = IV.raw(*tab), IV.raw(*rrb), IV.raw(*tbb)
    one, two = IV(1), IV(2)
    ioa = (one + ta.sq()).inv()
    ca = (one - ta.sq()) * ioa
    sa = two * ta * ioa
    iob = (one + tb.sq()).inv()
    cb = (one - tb.sq()) * iob
    sb = two * tb * iob
    CSc = ((ca - rr * cb).sq() + (sa - rr * sb).sq()).sqrt()
    if CSc.hi < SIXT:
        return True
    CXc = ((ca + rr * cb).sq() + (sa - rr * sb).sq()).sqrt()
    if CXc.hi < SIXT:
        return True
    return False

def main():
    resume = "--resume" in sys.argv
    if not resume and not crosscheck():
        print("crosscheck FAILED, aborting")
        return
    seed = [((F(0), F(7, 32)), (F(-1), F(1)), (F(0), F(1)), (F(-1), F(1)))]
    pl.run_covering(
        "bicorner-same", seed,
        entry_factory("iv"), entry_factory("dv"),
        HERE / "artifacts",
        "E:/_Datos/caos-research/central-configurations/EXP-022",
        discard=discard, depth=44, budget=10800 if resume else 21600, resume=resume)

if __name__ == "__main__":
    main()
