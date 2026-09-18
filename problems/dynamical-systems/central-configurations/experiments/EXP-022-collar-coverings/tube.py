"""EXP-022 part (b): the collision-tube blow-up covering.

Chart variables (w, v, tau, rho): u = w + t/2, p = w - t/2, q = v - f,
t = rho*alpha, f = rho*beta, (alpha, beta) = (sgn*(1-tau^2), 2*tau)/(1+tau^2),
cs = rho EXACTLY. Two charts sgn = +1 / -1 cover the full circle.
Region: w in [7/32, 3], v in [-3, 3], tau in [-1, 1], rho in [0, 3/32]
(3/32 > sqrt(2)/16 covers the square |t|,|f| <= 1/16).

Rescaled rows (verified in verify-tube-blowup.py): L13, L15, L23, L25, L36
multiplied by rho^2; L35 divided by rho^2 using the EXACT factorizations
  Delta135 = -rho*D135, Delta235 = -rho*D235,
  s(d1A,d1B) = rho*E1*SD1, s(d2A,d2B) = rho*E2*SD2,
  s(wA,cx) = rho*F1*SXA,   s(cx,wB) = -rho*G1*SXB,
so every 1/rho^3 cancels algebraically; the chart matrix is analytic on
the CLOSED region including rho = 0. Row scalings by nonzero factors
preserve rank at rho > 0; rho = 0 is the collision blow-up face (not in
the stratum), so certificates on boxes touching rho = 0 certify the
punctured tube. The face carries a known rank-2 degeneracy curve
(w^2 + v^2 = 1 with alpha = beta*gam/w): the trap certificate covers it.
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

# Division helper: IV has inv(); DV needs a reciprocal. Add one here rather
# than editing phase3: d(1/x) = -dx/x^2.
def dv_inv(x):
    iv = x.v.inv()
    isq = (x.v * x.v).inv()
    return DV(iv, [IV(-1) * isq * g for g in x.g])

def K_inv(x):
    return x.inv() if isinstance(x, IV) else dv_inv(x)

def entry_factory(sgn, mode):
    """mode 'iv': args are (lo,hi) tuples -> IV matrix.
       mode 'dv': args are DV duals -> DV matrix."""
    def entries(args):
        if mode == "iv":
            w, v, tau, rho = (IV.raw(*b) for b in args)
        else:
            w, v, tau, rho = args
        one = IV(1) if mode == "iv" else DV(1)
        two = IV(2) if mode == "iv" else DV(2)
        opp = one + tau * tau
        iop = K_inv(opp)
        alpha = (one - tau * tau) * iop * sgn
        beta = two * tau * iop
        t_ = rho * alpha
        f_ = rho * beta
        u = w + t_ * F(1, 2) if mode == "iv" else w + t_ * DV(F(1, 2))
        p = w - t_ * F(1, 2) if mode == "iv" else w - t_ * DV(F(1, 2))
        h1 = one - v
        gam = (IV(-1) if mode == "iv" else DV(-1)) - v
        g1 = h1 + f_
        g2 = gam + f_
        d1A = (u.sq() + h1.sq()).sqrt()
        d2A = (u.sq() + gam.sq()).sqrt()
        d1B = (p.sq() + g1.sq()).sqrt()
        d2B = (p.sq() + g2.sq()).sqrt()
        wA = two * u
        wB = two * p
        cx = ((u + p).sq() + f_.sq()).sqrt()
        r12 = IV(2) if mode == "iv" else DV(2)
        def icube(x):
            return K_inv(x * x * x)
        i_r12 = icube(r12); i_d1A = icube(d1A); i_d2A = icube(d2A)
        i_d1B = icube(d1B); i_d2B = icube(d2B); i_wA = icube(wA)
        i_wB = icube(wB); i_cx = icube(cx)
        def s(a, b):
            return a - b
        # exact rho-factored auxiliaries
        hf = F(1, 2)
        D135 = alpha * h1 + beta * w + rho * alpha * beta * hf
        D235 = alpha * gam + beta * w + rho * alpha * beta * hf
        E1 = two * beta * h1 - two * alpha * w + rho * beta.sq()
        E2 = two * beta * gam - two * alpha * w + rho * beta.sq()
        F1 = (IV(-4) if mode == "iv" else DV(-4)) * w * alpha + rho * (beta.sq() - alpha.sq())
        G1 = (IV(4) if mode == "iv" else DV(4)) * w * alpha + rho * (beta.sq() - alpha.sq())
        SD1 = (d1B.sq() + d1A * d1B + d1A.sq()) * K_inv((d1A + d1B)) * i_d1A * i_d1B
        SD2 = (d2B.sq() + d2A * d2B + d2A.sq()) * K_inv((d2A + d2B)) * i_d2A * i_d2B
        SXA = (cx.sq() + cx * wA + wA.sq()) * K_inv((cx + wA)) * i_wA * i_cx
        SXB = (cx.sq() + cx * wB + wB.sq()) * K_inv((cx + wB)) * i_wB * i_cx
        r2 = rho.sq()
        r3 = r2 * rho
        e12 = two
        m1_ = IV(-1) if mode == "iv" else DV(-1)
        D136 = m1_ * (u * g1 + p * h1)
        D154 = m1_ * (p * h1 + u * g1)
        D236 = m1_ * (u * g2 + p * gam)
        D254 = m1_ * (p * gam + u * g2)
        Z = IV(0) if mode == "iv" else DV(0)
        J = [[Z] * 4 for _ in range(6)]
        # L13 x rho^2
        J[0][1] = r2 * (m1_ * u * e12) * s(i_r12, i_d2A)
        J[0][2] = r2 * (m1_ * two * u * h1) * s(i_d1A, i_wA)
        J[0][3] = m1_ * r3 * i_d1B * D135 + D135 + r2 * s(i_d1B, i_cx) * D136
        # L15 x rho^2
        J[1][1] = r2 * (m1_ * p * e12) * s(i_r12, i_d2B)
        J[1][2] = r3 * i_d1A * D135 - D135 + r2 * s(i_d1A, i_cx) * D154
        J[1][3] = r2 * (m1_ * two * p * g1) * s(i_d1B, i_wB)
        # L23 x rho^2
        J[2][0] = r2 * (u * e12) * s(i_r12, i_d1A)
        J[2][2] = r2 * (m1_ * two * u * gam) * s(i_d2A, i_wA)
        J[2][3] = m1_ * r3 * i_d2B * D235 + D235 + r2 * s(i_d2B, i_cx) * D236
        # L25 x rho^2
        J[3][0] = r2 * (p * e12) * s(i_r12, i_d1B)
        J[3][2] = r3 * i_d2A * D235 - D235 + r2 * s(i_d2A, i_cx) * D254
        J[3][3] = r2 * (m1_ * two * p * g2) * s(i_d2B, i_wB)
        # L35 / rho^2
        J[4][0] = m1_ * E1 * D135 * SD1
        J[4][1] = m1_ * E2 * D235 * SD2
        J[4][2] = m1_ * two * beta * u * F1 * SXA
        J[4][3] = two * beta * p * G1 * SXB
        # L36 x rho^2
        J[5][0] = r3 * E1 * SD1 * D136
        J[5][1] = r3 * E2 * SD2 * D236
        J[5][2] = two * beta * u - r3 * two * beta * u * i_wA
        J[5][3] = two * beta * p - r3 * two * beta * p * i_wB
        return J
    return entries

def crosscheck(sgn):
    """Gate: at rational interior points, the chart matrix must equal the
    original entry matrix with the row scalings applied."""
    import random
    random.seed(7)
    ok = 0
    for _ in range(5):
        wv = F(random.randint(8, 90), 32)
        vv = F(random.randint(-90, 90), 32)
        tv = F(random.randint(-30, 30), 32)
        rv = F(random.randint(1, 90), 1024)
        args_pt = [(x, x) for x in (wv, vv, tv, rv)]
        Jc = entry_factory(sgn, "iv")(args_pt)
        opp = 1 + tv * tv
        al = sgn * (1 - tv * tv) / opp
        be = 2 * tv / opp
        t_, f_ = rv * al, rv * be
        u, p = wv + t_ / 2, wv - t_ / 2
        v_, q_ = vv, vv - f_
        Jo = pl.r21.entry_matrix((u, u), (v_, v_), (p, p), (q_, q_))
        good = True
        for i in range(6):
            for j in range(4):
                a = Jc[i][j]
                o = Jo[i][j]
                if i == 4:
                    lo, hi = o.lo / rv**2, o.hi / rv**2
                else:
                    lo, hi = o.lo * rv**2, o.hi * rv**2
                mid_c = (a.lo + a.hi) / 2
                mid_o = (lo + hi) / 2
                wid = max(a.hi - a.lo, hi - lo, F(1, 1 << 34))
                if abs(mid_c - mid_o) > 4 * wid:
                    print(f"MISMATCH sgn={sgn} row {i} col {j}: {float(mid_c)} vs {float(mid_o)}")
                    good = False
        ok += good
    print(f"crosscheck sgn={sgn}: {ok}/5 points OK", flush=True)
    return ok == 5

def main():
    resume = "--resume" in sys.argv
    seed = [((F(7, 32), F(3)), (F(-3), F(3)), (F(-1), F(1)), (F(0), F(3, 32)))]
    for sgn in (1, -1):
        if not resume and not crosscheck(sgn):
            print("crosscheck FAILED, aborting")
            return
        nm = f"tube-{'R' if sgn == 1 else 'L'}"
        pl.run_covering(
            nm, seed,
            entry_factory(sgn, "iv"),
            entry_factory(sgn, "dv"),
            HERE / "artifacts",
            "E:/_Datos/caos-research/central-configurations/EXP-022",
            depth=44, budget=21600, resume=resume)

if __name__ == "__main__":
    main()
