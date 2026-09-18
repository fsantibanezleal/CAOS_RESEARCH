"""EXP-022 part (d6): the deep tube (collision band at small w).

Region: the collision band {|u-p| <= 1/16, |f| <= 1/16} for
w = (u+p)/2 in [0, 1/8] (the tube and its extension cover w >= 1/8).
Chart = tube.py's blow-up (t = rho alpha, f = rho beta, cs = rho, both
angle charts) COMPOSED with both column rescales (mA x 4u^2, mB x 4p^2),
which cancels every wA^-3 and wB^-3 algebraically:
  4u^2 x (tube L13 mA) = rho^2 h1 (1 - 8u^3/d1A^3),
  4u^2 x (tube L35 mA) = -beta F1 (cx^2+cx wA+wA^2)/((cx+wA) cx^3),
  4u^2 x (tube L36 mA) = 8 beta u^3 - rho^3 beta,   etc.
Row scalings as in tube.py: (rho^2, rho^2, rho^2, rho^2, 1/rho^2, rho^2).
Discards: {|v - 1| < 1/16} and {|v + 1| < 1/16} (both pairs near an axis
body: bicorner-same and its mirror, widened to 7/32) and the quadruple
corner {w < 1/32 and rho < 1/16} (all four pair bodies collapse onto the
axis: the collinear limit; its own chart, declared pending).
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

def entry_factory(sgn, mode):
    def entries(args):
        if mode == "iv":
            w, v, tau, rho = (IV.raw(*b) for b in args)
            one, two, m1_, Z = IV(1), IV(2), IV(-1), IV(0)
            four, eight = IV(4), IV(8)
        else:
            w, v, tau, rho = args
            one, two, m1_, Z = DV(1), DV(2), DV(-1), DV(0)
            four, eight = DV(4), DV(8)
        opp = one + tau.sq()
        iop = K_inv(opp)
        alpha = (one - tau.sq()) * iop * sgn
        beta = two * tau * iop
        t_ = rho * alpha
        f_ = rho * beta
        half = F(1, 2)
        u = w + t_ * half if mode == "iv" else w + t_ * DV(half)
        p = w - t_ * half if mode == "iv" else w - t_ * DV(half)
        h1 = one - v
        gam = m1_ - v
        g1 = h1 + f_
        g2 = gam + f_
        d1A = (u.sq() + h1.sq()).sqrt()
        d2A = (u.sq() + gam.sq()).sqrt()
        d1B = (p.sq() + g1.sq()).sqrt()
        d2B = (p.sq() + g2.sq()).sqrt()
        wA = two * u
        wB = two * p
        cx = ((u + p).sq() + f_.sq()).sqrt()
        def icube(x):
            return K_inv(x * x * x)
        i_d1A = icube(d1A); i_d2A = icube(d2A)
        i_d1B = icube(d1B); i_d2B = icube(d2B)
        i_cx = icube(cx)
        i_r12 = IV(F(1, 8)) if mode == "iv" else DV(F(1, 8))
        u3 = u * u * u
        p3_ = p * p * p
        hf = F(1, 2)
        D135 = alpha * h1 + beta * w + rho * alpha * beta * hf
        D235 = alpha * gam + beta * w + rho * alpha * beta * hf
        E1 = two * beta * h1 - two * alpha * w + rho * beta.sq()
        E2 = two * beta * gam - two * alpha * w + rho * beta.sq()
        F1 = (IV(-4) if mode == "iv" else DV(-4)) * w * alpha + rho * (beta.sq() - alpha.sq())
        G1 = (IV(4) if mode == "iv" else DV(4)) * w * alpha + rho * (beta.sq() - alpha.sq())
        SD1 = (d1B.sq() + d1A * d1B + d1A.sq()) * K_inv(d1A + d1B) * i_d1A * i_d1B
        SD2 = (d2B.sq() + d2A * d2B + d2A.sq()) * K_inv(d2A + d2B) * i_d2A * i_d2B
        # wA/wB-free cross factors (the 4u^2 / 4p^2 rescales absorbed):
        # 4u^2 * s(wA,cx)(-2fu)/rho^2-etc. handled per entry below via
        # XA = (cx^2 + cx wA + wA^2)/((cx + wA) cx^3),
        # XB = (cx^2 + cx wB + wB^2)/((cx + wB) cx^3).
        XA = (cx.sq() + cx * wA + wA.sq()) * K_inv(cx + wA) * i_cx
        XB = (cx.sq() + cx * wB + wB.sq()) * K_inv(cx + wB) * i_cx
        r2 = rho.sq()
        r3 = r2 * rho
        e12 = two
        D136 = m1_ * (u * g1 + p * h1)
        D154 = m1_ * (p * h1 + u * g1)
        D236 = m1_ * (u * g2 + p * gam)
        D254 = m1_ * (p * gam + u * g2)
        J = [[Z] * 4 for _ in range(6)]
        # L13 x rho^2 (mA x 4u^2)
        J[0][1] = r2 * (m1_ * u * e12) * (i_r12 - i_d2A)
        J[0][2] = r2 * h1 * (one - eight * u3 * i_d1A)
        J[0][3] = m1_ * r3 * i_d1B * D135 * (four * p.sq()) \
            + (four * p.sq()) * D135 + r2 * (i_d1B - i_cx) * D136 * (four * p.sq())
        # L15 x rho^2 (mA x 4u^2, mB x 4p^2)
        J[1][1] = r2 * (m1_ * p * e12) * (i_r12 - i_d2B)
        J[1][2] = four * u.sq() * (r3 * i_d1A * D135 - D135) \
            + r2 * four * u.sq() * (i_d1A - i_cx) * D154
        J[1][3] = r2 * g1 * (one - eight * p3_ * i_d1B)
        # L23 x rho^2
        J[2][0] = r2 * (u * e12) * (i_r12 - i_d1A)
        J[2][2] = r2 * gam * (one - eight * u3 * i_d2A)
        J[2][3] = m1_ * r3 * i_d2B * D235 * (four * p.sq()) \
            + (four * p.sq()) * D235 + r2 * (i_d2B - i_cx) * D236 * (four * p.sq())
        # L25 x rho^2
        J[3][0] = r2 * (p * e12) * (i_r12 - i_d1B)
        J[3][2] = four * u.sq() * (r3 * i_d2A * D235 - D235) \
            + r2 * four * u.sq() * (i_d2A - i_cx) * D254
        J[3][3] = r2 * g2 * (one - eight * p3_ * i_d2B)
        # L35 / rho^2 (columns rescaled)
        J[4][0] = m1_ * E1 * D135 * SD1
        J[4][1] = m1_ * E2 * D235 * SD2
        J[4][2] = m1_ * beta * F1 * XA
        J[4][3] = beta * G1 * XB
        # L36 x rho^2
        J[5][0] = r3 * E1 * SD1 * D136
        J[5][1] = r3 * E2 * SD2 * D236
        J[5][2] = eight * beta * u3 - r3 * beta
        J[5][3] = eight * beta * p3_ - r3 * beta
        return J
    return entries

def crosscheck(sgn):
    import random
    random.seed(7 + sgn)
    ok = 0
    for _ in range(5):
        wv = F(random.randint(2, 16), 128)
        vv = F(random.randint(-90, 90), 32)
        if abs(vv - 1) < F(3, 32) or abs(vv + 1) < F(3, 32):
            vv = F(1, 3)
        tv = F(random.randint(-30, 30), 32)
        rv = F(random.randint(1, 10), 256)
        pt = [(x, x) for x in (wv, vv, tv, rv)]
        Jc = entry_factory(sgn, "iv")(pt)
        opp = 1 + tv * tv
        al = sgn * (1 - tv * tv) / opp
        be = 2 * tv / opp
        t_, f_ = rv * al, rv * be
        uv, pv = wv + t_ / 2, wv - t_ / 2
        if uv <= 0 or pv <= 0:
            continue
        qv = vv - f_
        Jo = pl.r21.entry_matrix((uv, uv), (vv, vv), (pv, pv), (qv, qv))
        rowscale = [rv**2] * 4 + [F(1, 1) / rv**2, rv**2]
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
                    print(f"MISMATCH sgn={sgn} row {i} col {j}: "
                          f"{float(mid_c)} vs {float(mid_o)}")
                    good = False
        ok += good
    print(f"crosscheck sgn={sgn}: {ok}/5 points OK", flush=True)
    return ok == 5

SIXT = F(1, 16)

def make_discard(sgn):
    def discard(box):
        wb, vb, tb, rb = box
        if vb[0] >= 1 - SIXT and vb[1] <= 1 + SIXT:
            return True
        if vb[0] >= -1 - SIXT and vb[1] <= -1 + SIXT:
            return True
        if wb[1] < F(1, 32) and rb[1] < F(1, 16):
            return True                  # quadruple collinear corner -> M2
        # UNPHYSICAL (2026-08-20): the chart's box product contains
        # (w, rho) pairs with rho |alpha| > 2w, where p = w - rho alpha / 2
        # or u = w + rho alpha / 2 is NEGATIVE: not a configuration at all.
        # deep's residue was entirely of this kind; M2 always had the test.
        w, tau, rho = IV.raw(*wb), IV.raw(*tb), IV.raw(*rb)
        one, two = IV(1), IV(2)
        iop = (one + tau.sq()).inv()
        alpha = (one - tau.sq()) * iop * sgn
        half = F(1, 2)
        u = w + rho * alpha * half
        p = w - rho * alpha * half
        if u.hi <= 0 or p.hi <= 0:
            return True
        return False
    return discard

def main():
    resume = "--resume" in sys.argv
    seed = [((F(0), F(1, 8)), (F(-3), F(3)), (F(-1), F(1)), (F(0), F(3, 32)))]
    for sgn in (1, -1):
        if not resume and not crosscheck(sgn):
            print("crosscheck FAILED, aborting")
            return
        nm = f"deep-{'R' if sgn == 1 else 'L'}"
        pl.run_covering(
            nm, seed,
            entry_factory(sgn, "iv"), entry_factory(sgn, "dv"),
            HERE / "artifacts",
            "E:/_Datos/caos-research/central-configurations/EXP-022",
            discard=make_discard(sgn), depth=44, budget=21600, resume=resume)

if __name__ == "__main__":
    main()
