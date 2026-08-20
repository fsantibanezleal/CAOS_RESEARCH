"""EXP-022 mini-chart M2: the collinear quadruple corner.

Blow-up of deep's corner {w < 1/64, rho < 1/32} (both pairs collapse onto
the axis while merged: the collinear limit): (2w, rho) = Rc (ct, st) with
(ct, st) = ((1 - tt^2), 2 tt)/(1 + tt^2), tt in [0, 1] (first quadrant).
Chart variables (Rc, tt, v, tau) in [0, 3/64] x [0, 1] x [-3, 3] x
[-1, 1]; two alpha-sign charts as in deep. Scaled positions:
u = Rc uh, uh = (ct + st alpha)/2; p = Rc ph, ph = (ct - st alpha)/2;
f = Rc st beta; cx = Rc CXd, CXd = sqrt(ct^2 + st^2 beta^2).

The apparent deepest singularity CXd = 0 (at tt = 1, tau = 0) is
UNPHYSICAL: it forces |alpha| st > ct, i.e. u < 0 or p < 0; on the closed
physical region {uh >= 0, ph >= 0}, CXd >= st(alpha^2 + beta^2)^(1/2)
= st on the boundary and CXd = ct = 1 at st = 0, so CXd > 0 throughout:
the cascade TERMINATES here. Discards: wholly-unphysical boxes
(uh.hi < 0 or ph.hi < 0) and the axis-body slabs {|v -+ 1| < 1/16}
(bicorner-same and its mirror, which cover d1A <= 7/32 > the 0.08 these
configurations reach).

Entries: deep.py's chart evaluated at (w, rho) = (Rc ct/2, Rc st) is
already analytic except row L35's mA/mB, whose XA/XB factors scale as
1/Rc^2; with F1 = Rc F1h, G1 = Rc G1h (F1h = -2 ct alpha +
st (beta^2 - alpha^2), G1h likewise with +) the row rescale L35 x Rc
clears everything:
  L35 mA -> -beta F1h XAh,  XAh = (CXd^2 + 2 uh CXd + 4 uh^2) /
                                   ((CXd + 2 uh) CXd^3),
  L35 mB -> +beta G1h XBh   (with ph).
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
            Rc, tt, v, tau = (IV.raw(*b) for b in args)
            one, two, m1_, Z = IV(1), IV(2), IV(-1), IV(0)
            four, eight = IV(4), IV(8)
            egt = IV(F(1, 8))
        else:
            Rc, tt, v, tau = args
            one, two, m1_, Z = DV(1), DV(2), DV(-1), DV(0)
            four, eight = DV(4), DV(8)
            egt = DV(F(1, 8))
        iot = K_inv(one + tt.sq())
        ct = (one - tt.sq()) * iot
        st = two * tt * iot
        iop = K_inv(one + tau.sq())
        alpha = (one - tau.sq()) * iop * sgn
        beta = two * tau * iop
        half = F(1, 2)
        uh = (ct + st * alpha) * half if mode == "iv" else (ct + st * alpha) * DV(half)
        ph = (ct - st * alpha) * half if mode == "iv" else (ct - st * alpha) * DV(half)
        u = Rc * uh
        p = Rc * ph
        w = Rc * ct * half if mode == "iv" else Rc * ct * DV(half)
        rho = Rc * st
        f_ = rho * beta
        h1 = one - v
        gam = m1_ - v
        g1 = h1 + f_
        g2 = gam + f_
        d1A = (u.sq() + h1.sq()).sqrt()
        d2A = (u.sq() + gam.sq()).sqrt()
        d1B = (p.sq() + g1.sq()).sqrt()
        d2B = (p.sq() + g2.sq()).sqrt()
        CXd = (ct.sq() + (st * beta).sq()).sqrt()
        def icube(x):
            return K_inv(x * x * x)
        i_d1A = icube(d1A); i_d2A = icube(d2A)
        i_d1B = icube(d1B); i_d2B = icube(d2B)
        cx = Rc * CXd
        i_cx = icube(cx)
        u3 = u * u * u
        p3_ = p * p * p
        hf = F(1, 2)
        D135 = alpha * h1 + beta * w + rho * alpha * beta * hf
        D235 = alpha * gam + beta * w + rho * alpha * beta * hf
        E1 = two * beta * h1 - two * alpha * w + rho * beta.sq()
        E2 = two * beta * gam - two * alpha * w + rho * beta.sq()
        F1h = m1_ * two * ct * alpha + st * (beta.sq() - alpha.sq())
        G1h = two * ct * alpha + st * (beta.sq() - alpha.sq())
        SD1 = (d1B.sq() + d1A * d1B + d1A.sq()) * K_inv(d1A + d1B) * i_d1A * i_d1B
        SD2 = (d2B.sq() + d2A * d2B + d2A.sq()) * K_inv(d2A + d2B) * i_d2A * i_d2B
        XAh = (CXd.sq() + two * uh * CXd + four * uh.sq()) \
            * K_inv(CXd + two * uh) * icube(CXd)
        XBh = (CXd.sq() + two * ph * CXd + four * ph.sq()) \
            * K_inv(CXd + two * ph) * icube(CXd)
        r2 = rho.sq()
        r3 = r2 * rho
        e12 = two
        D136 = m1_ * (u * g1 + p * h1)
        D154 = m1_ * (p * h1 + u * g1)
        D236 = m1_ * (u * g2 + p * gam)
        D254 = m1_ * (p * gam + u * g2)
        fourps = four * p.sq()
        fourus = four * u.sq()
        J = [[Z] * 4 for _ in range(6)]
        # L13 x rho^2 (as deep)
        J[0][1] = r2 * (m1_ * u * e12) * (egt - i_d2A)
        J[0][2] = r2 * h1 * (one - eight * u3 * i_d1A)
        J[0][3] = m1_ * r3 * i_d1B * D135 * fourps + fourps * D135 \
            + r2 * (i_d1B - i_cx) * D136 * fourps
        # L15 x rho^2
        J[1][1] = r2 * (m1_ * p * e12) * (egt - i_d2B)
        J[1][2] = fourus * (r3 * i_d1A * D135 - D135) \
            + r2 * fourus * (i_d1A - i_cx) * D154
        J[1][3] = r2 * g1 * (one - eight * p3_ * i_d1B)
        # L23 x rho^2
        J[2][0] = r2 * (u * e12) * (egt - i_d1A)
        J[2][2] = r2 * gam * (one - eight * u3 * i_d2A)
        J[2][3] = m1_ * r3 * i_d2B * D235 * fourps + fourps * D235 \
            + r2 * (i_d2B - i_cx) * D236 * fourps
        # L25 x rho^2
        J[3][0] = r2 * (p * e12) * (egt - i_d1B)
        J[3][2] = fourus * (r3 * i_d2A * D235 - D235) \
            + r2 * fourus * (i_d2A - i_cx) * D254
        J[3][3] = r2 * g2 * (one - eight * p3_ * i_d2B)
        # L35 / rho^2, x Rc (the extra clearing)
        J[4][0] = Rc * (m1_ * E1 * D135 * SD1)
        J[4][1] = Rc * (m1_ * E2 * D235 * SD2)
        J[4][2] = m1_ * beta * F1h * XAh
        J[4][3] = beta * G1h * XBh
        # L36 x rho^2
        J[5][0] = r3 * E1 * SD1 * D136
        J[5][1] = r3 * E2 * SD2 * D236
        J[5][2] = eight * beta * u3 - r3 * beta
        J[5][3] = eight * beta * p3_ - r3 * beta
        return J
    return entries

def crosscheck(sgn):
    import random
    random.seed(31 + sgn)
    ok = tried = 0
    while tried < 5:
        Rcv = F(random.randint(1, 6), 128)
        ttv = F(random.randint(1, 31), 32)
        vv = F(random.randint(-90, 90), 32)
        if abs(vv - 1) < F(3, 32) or abs(vv + 1) < F(3, 32):
            vv = F(1, 3)
        tv = F(random.randint(-30, 30), 32)
        ot = 1 + ttv * ttv
        ctv = (1 - ttv * ttv) / ot
        stv = 2 * ttv / ot
        opp = 1 + tv * tv
        al = sgn * (1 - tv * tv) / opp
        be = 2 * tv / opp
        uhv = (ctv + stv * al) / 2
        phv = (ctv - stv * al) / 2
        # stay clear of the 2^-40 grid floor of the REFERENCE evaluation
        if uhv < F(1, 64) or phv < F(1, 64):
            continue
        tried += 1
        uv = Rcv * uhv
        pv = Rcv * phv
        rhov = Rcv * stv
        fv = rhov * be
        qv = vv - fv
        pt = [(x, x) for x in (Rcv, ttv, vv, tv)]
        Jc = entry_factory(sgn, "iv")(pt)
        Jo = pl.r21.entry_matrix((uv, uv), (vv, vv), (pv, pv), (qv, qv))
        rowscale = [rhov**2] * 4 + [Rcv / rhov**2, rhov**2]
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
                wid = max(aiv.hi - aiv.lo, hi - lo, F(1, 1 << 20))
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
        Rcb, ttb, vb, tb = box
        if vb[0] >= 1 - SIXT and vb[1] <= 1 + SIXT:
            return True
        if vb[0] >= -1 - SIXT and vb[1] <= -1 + SIXT:
            return True
        tt, tau = IV.raw(*ttb), IV.raw(*tb)
        one, two = IV(1), IV(2)
        iot = (one + tt.sq()).inv()
        ct = (one - tt.sq()) * iot
        st = two * tt * iot
        iop = (one + tau.sq()).inv()
        alpha = (one - tau.sq()) * iop * sgn
        uh = (ct + st * alpha) * F(1, 2)
        ph = (ct - st * alpha) * F(1, 2)
        if uh.hi < 0 or ph.hi < 0:
            return True                  # unphysical (u < 0 or p < 0)
        return False
    return discard

def main():
    resume = "--resume" in sys.argv
    seed = [((F(0), F(3, 64)), (F(0), F(1)), (F(-3), F(3)), (F(-1), F(1)))]
    for sgn in (1, -1):
        if not resume and not crosscheck(sgn):
            print("crosscheck FAILED, aborting")
            return
        nm = f"m2-{'R' if sgn == 1 else 'L'}"
        pl.run_covering(
            nm, seed,
            entry_factory(sgn, "iv"), entry_factory(sgn, "dv"),
            HERE / "artifacts",
            "E:/_Datos/caos-research/central-configurations/EXP-022",
            discard=make_discard(sgn), depth=44, budget=21600, resume=resume)

if __name__ == "__main__":
    main()
