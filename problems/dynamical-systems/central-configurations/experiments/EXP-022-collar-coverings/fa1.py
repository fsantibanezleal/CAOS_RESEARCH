"""EXP-022 part (e), chart F_A1: pair A far, pair B bounded.

Chart variables (eps, tau, p, q):
  eps = 1/R_A in [0, 1/3], direction (a, b) = ((1-tau^2), 2 tau)/(1+tau^2),
  tau in [-1, 1] (a >= 0), u = a/eps, v = b/eps; p in [0, 3/2],
  q in [-3/2, 3/2] (so R_B <= 3 sqrt2 / 2 < 3: the A-B separation obeys
  Cs, Cx >= 1 - eps * R_B > 0.29, no far-tube inside this chart).

Scalings: rows (L13, L23, L35, L36) x eps; columns mA x 4u^2, mB x 4p^2.
Every entry is then a polynomial in (a, b, eps, p, q, g1, g2) over the
radicals D1A, D2A, Cs, Cx, d1B, d2B (all certified-positive per box), with
NO division by eps, u, or p anywhere: the chart matrix is analytic on the
CLOSED chart including the eps = 0 (infinity), a = 0 (vertical escape),
and p = 0 (B-collapse) faces. Scalings are positive on the open chart, so
rank is preserved there; the faces are outside the configuration space.
Discards: the B-corner tubes {p <= 1/16, |q -+ 1| <= 1/16} (part (d)).

Derivation recorded in approaches-evaluation-2026-08-19.md (amendment) and
verified by the 5-point crosscheck below before any covering run.
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
            eps, tau, p, q = (IV.raw(*b) for b in args)
            one, two, m1_, Z = IV(1), IV(2), IV(-1), IV(0)
            four, eight = IV(4), IV(8)
        else:
            eps, tau, p, q = args
            one, two, m1_, Z = DV(1), DV(2), DV(-1), DV(0)
            four, eight = DV(4), DV(8)
        opp = one + tau * tau
        iop = K_inv(opp)
        a = (one - tau * tau) * iop
        b = two * tau * iop
        g1 = one - q
        g2 = m1_ - q
        emb = eps - b            # eps - b  (= eps * h1)
        epb = eps + b            # eps + b  (= -eps * gam)
        bq = b - eps * q         # b - eps q (= eps * f)
        D1A = (a.sq() + emb.sq()).sqrt()
        D2A = (a.sq() + epb.sq()).sqrt()
        Cs = ((a - eps * p).sq() + bq.sq()).sqrt()
        Cx = ((a + eps * p).sq() + bq.sq()).sqrt()
        d1B = (p.sq() + g1.sq()).sqrt()
        d2B = (p.sq() + g2.sq()).sqrt()
        def icube(x):
            return K_inv(x * x * x)
        iD1A = icube(D1A); iD2A = icube(D2A)
        iCs = icube(Cs); iCx = icube(Cx)
        id1B = icube(d1B); id2B = icube(d2B)
        e3 = eps * eps * eps
        a3 = a * a * a
        p3_ = p * p * p
        a2_4 = four * a.sq()
        p2_4 = four * p.sq()
        egt = one * F(1, 8) if mode == "iv" else DV(F(1, 8))
        # T-brackets (eps * Delta, exact)
        T135 = p * emb - a * g1
        T136 = m1_ * (a * g1 + p * emb)
        T235 = m1_ * p * epb - a * g2
        T236 = m1_ * a * g2 + p * epb
        T154 = m1_ * (p * emb + a * g1)
        T254 = p * epb - a * g2
        # s-factors in chart form
        S1s = id1B - e3 * iCs
        S1x = id1B - e3 * iCx
        S2s = id2B - e3 * iCs
        S2x = id2B - e3 * iCx
        J = [[Z] * 4 for _ in range(6)]
        # L13 (x eps)
        J[0][1] = m1_ * a * F(1, 4) + two * a * e3 * iD2A if mode == "iv" else \
                  DV(F(-1, 4)) * a + two * a * e3 * iD2A
        J[0][2] = emb * (one - eight * a3 * iD1A)
        J[0][3] = p2_4 * (S1s * T135 + S1x * T136)
        # L23 (x eps)
        J[2][0] = a * F(1, 4) - two * a * e3 * iD1A if mode == "iv" else \
                  DV(F(1, 4)) * a - two * a * e3 * iD1A
        J[2][2] = m1_ * epb * (one - eight * a3 * iD2A)
        J[2][3] = p2_4 * (S2s * T235 + S2x * T236)
        # L15 (x 1)
        J[1][1] = m1_ * two * p * (egt - id2B)
        J[1][2] = m1_ * a2_4 * (iD1A - iCs) * T135 + a2_4 * (iD1A - iCx) * T154
        J[1][3] = g1 - eight * p3_ * g1 * id1B
        # L25 (x 1)
        J[3][0] = two * p * (egt - id1B)
        J[3][2] = m1_ * a2_4 * (iD2A - iCs) * T235 + a2_4 * (iD2A - iCx) * T254
        J[3][3] = g2 - eight * p3_ * g2 * id2B
        # L35 (x eps)
        J[4][0] = (e3 * iD1A - id1B) * T135
        J[4][1] = (e3 * iD2A - id2B) * T235
        J[4][2] = bq * (eight * a3 * iCx - one)
        J[4][3] = bq * (one - eight * p3_ * e3 * iCx)
        # L36 (x eps)
        J[5][0] = (e3 * iD1A - id1B) * T136
        J[5][1] = (e3 * iD2A - id2B) * T236
        J[5][2] = bq * (eight * a3 * iCs - one)
        J[5][3] = bq * (eight * p3_ * e3 * iCs - one)
        return J
    return entries

def crosscheck():
    import random
    random.seed(23)
    ok = 0
    for _ in range(5):
        ev = F(random.randint(1, 10), 32)
        tv = F(random.randint(-30, 30), 32)
        pv = F(random.randint(1, 47), 32)
        qv = F(random.randint(-47, 47), 32)
        opp = 1 + tv * tv
        av = (1 - tv * tv) / opp
        bv = 2 * tv / opp
        if av == 0:
            tv = F(1, 2); opp = 1 + tv * tv
            av = (1 - tv * tv) / opp; bv = 2 * tv / opp
        uv = av / ev
        vv = bv / ev
        pt = [(x, x) for x in (ev, tv, pv, qv)]
        Jc = entry_factory("iv")(pt)
        Jo = pl.r21.entry_matrix((uv, uv), (vv, vv), (pv, pv), (qv, qv))
        # rows order in J: L13, L15, L23, L25, L35, L36
        rowscale = [ev, 1, ev, 1, ev, ev]
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
                wid = max(aiv.hi - aiv.lo, hi - lo, F(1, 1 << 30))
                if abs(mid_c - mid_o) > 8 * wid:
                    print(f"MISMATCH row {i} col {j}: {float(mid_c)} vs {float(mid_o)}")
                    good = False
        ok += good
    print(f"crosscheck: {ok}/5 points OK", flush=True)
    return ok == 5

SIXT = F(1, 16)

def discard(box):
    eb, tb, pb, qb = box
    if pb[1] <= SIXT:
        if qb[0] >= 1 - SIXT and qb[1] <= 1 + SIXT:
            return True
        if qb[0] >= -1 - SIXT and qb[1] <= -1 + SIXT:
            return True
    return False

def main():
    resume = "--resume" in sys.argv
    if not resume and not crosscheck():
        print("crosscheck FAILED, aborting")
        return
    seed = [((F(0), F(1, 3)), (F(-1), F(1)), (F(0), F(3, 2)), (F(-3, 2), F(3, 2)))]
    pl.run_covering(
        "fa1", seed,
        entry_factory("iv"), entry_factory("dv"),
        HERE / "artifacts",
        "E:/_Datos/caos-research/central-configurations/EXP-022",
        discard=discard, depth=44, budget=43200, resume=resume)

if __name__ == "__main__":
    main()
