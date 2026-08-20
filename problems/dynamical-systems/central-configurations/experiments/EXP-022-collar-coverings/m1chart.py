"""EXP-022 mini-chart M1: the quadruple cluster at body 1.

Blow-up of bicorner-same's center {rr = 1, taua = taub} (pair A meets
pair B while both sit near axis body 1): rr = 1 + rhoq alpha,
taua = taub + rhoq beta, (alpha, beta) from tauq (alpha <= 0; the other
half is the swap image). Chart variables (rhoa, taub, rhoq, tauq) in
[0, 7/32] x [-1, 1] x [0, 1/4] x [-1, 1].

SEAM (exact, as for fartube): a bicorner-same point with CSc <= 1/16 has
|1 - rr| <= 1/16 and |taua - taub| <= 1/8 (chord formula, both tau in
[-1, 1]), so rhoq < 0.09 < 1/4. The CXc <= 1/16 discard also lands here
(CXc small forces (rr, taua, taub) near (1, +-1, +-1), hence rhoq small);
within M1 the vertical corner {CXc < 1/32} is re-discarded (M1-vert, the
cascade's last level, declared).

Factorizations: CSc = rhoq Ch, Ch^2 = Qn/Qd and CXc^2 = CXn/CXd and
Fc = rhoq Fhn/Fhd REUSED from fartube_gen (the (c, s) <-> (a, b)
identification, verified in verify-m1.py); NEW: W1 = rhoq W1n/W1d,
G5 = rhoq G5n/G5d (m1_gen). K5 = rhoq K5hat, K5hat = 2 G5hat +
rr rhoa W1hat; rr^3 - 1 = rhoq R3hat, R3hat = 3 alpha + 3 rhoq alpha^2 +
rhoq^2 alpha^3 (exact). Row scalings on top of bicorner-same's:
(rhoq^2, rhoq^2, rhoq^2, rhoq^2, 1/rhoq, rhoq^2).
"""
import sys
from fractions import Fraction as F
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent

def _load(name, fname):
    spec = importlib.util.spec_from_file_location(name, HERE / fname)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

pl = _load("pipeline", "pipeline.py")
gen = _load("fartube_gen", "fartube_gen.py")
g1n = _load("m1_gen", "m1_gen.py")
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
            ra, tb, rq, tq = (IV.raw(*b) for b in args)
            one, two, m1_, Z = IV(1), IV(2), IV(-1), IV(0)
            four, eight = IV(4), IV(8)
            quarter, egt = IV(F(1, 4)), IV(F(1, 8))
            Frac = lambda a, b: IV(F(a, b))
        else:
            ra, tb, rq, tq = args
            one, two, m1_, Z = DV(1), DV(2), DV(-1), DV(0)
            four, eight = DV(4), DV(8)
            quarter, egt = DV(F(1, 4)), DV(F(1, 8))
            Frac = lambda a, b: DV(F(a, b))
        ioq = K_inv(one + tq.sq())
        alpha = m1_ * (one - tq.sq()) * ioq
        beta = two * tq * ioq
        rr = one + rq * alpha
        ta = tb + rq * beta
        ioa = K_inv(one + ta.sq())
        ca = (one - ta.sq()) * ioa
        sa = two * ta * ioa
        iob = K_inv(one + tb.sq())
        cb = (one - tb.sq()) * iob
        sb = two * tb * iob
        u = ra * ca
        gam = m1_ * two - ra * sa
        g2 = m1_ * two - rr * ra * sb
        d2A = (u.sq() + gam.sq()).sqrt()
        p = rr * ra * cb
        d2B = (p.sq() + (two + rr * ra * sb).sq()).sqrt()
        def icube(x):
            return K_inv(x * x * x)
        id2A = icube(d2A); id2B = icube(d2B)
        Ch = (gen.Qn(rq, tq, Z, tb, Frac) * K_inv(gen.Qd(rq, tq, Z, tb, Frac))).sqrt()
        iCh = icube(Ch)
        CXc = (gen.CXn(rq, tq, Z, tb, Frac) * K_inv(gen.CXd(rq, tq, Z, tb, Frac))).sqrt()
        iCXc = icube(CXc)
        Fch = gen.Fhn(rq, tq, Z, tb, Frac) * K_inv(gen.Fhd(rq, tq, Z, tb, Frac))
        W1h = g1n.W1n(rq, tq, tb, Frac) * K_inv(g1n.W1d(rq, tq, tb, Frac))
        G5h = g1n.G5n(rq, tq, tb, Frac) * K_inv(g1n.G5d(rq, tq, tb, Frac))
        K5h = two * G5h + rr * ra * W1h
        K5v = rq * K5h
        W2 = ca * sb + cb * sa
        K6 = two * (ca + rr * cb) + rr * ra * W2
        R3h = (IV(3) if mode == "iv" else DV(3)) * alpha \
            + (IV(3) if mode == "iv" else DV(3)) * rq * alpha.sq() \
            + rq.sq() * alpha * alpha.sq()
        ra2 = ra.sq(); ra3 = ra2 * ra
        rr2 = rr.sq(); rr3 = rr2 * rr
        ca3 = ca * ca * ca
        cb3 = cb * cb * cb
        q2 = rq.sq()
        q3 = q2 * rq
        J = [[Z] * 4 for _ in range(6)]
        # L13 (x rhoq^2)
        J[0][1] = q2 * (m1_ * two * ca * (egt - id2A))
        J[0][2] = q2 * (m1_ * sa * (one - eight * ca3))
        J[0][3] = four * cb.sq() * (q3 * W1h - rr3 * W1h * iCh
                                    + q2 * (one - rr3 * iCXc) * W2)
        # L15 (x rhoq^2)
        J[1][1] = q2 * (m1_ * two * rr * cb * (egt - id2B))
        J[1][2] = four * rr * ca.sq() * (W1h * iCh - q3 * W1h
                                         + q2 * (one - iCXc) * W2)
        J[1][3] = q2 * (m1_ * rr * sb * (one - eight * cb3))
        # L23 (x rhoq^2)
        J[2][0] = q2 * (ra3 * ca * quarter - two * ca)
        J[2][2] = q2 * ra2 * gam * (one - eight * ra3 * ca3 * id2A)
        J[2][3] = ra2 * four * rr2 * cb.sq() * (
            q2 * ra3 * id2B * (K5v + K6) - K5h * iCh - q2 * iCXc * K6)
        # L25 (x rhoq^2)
        J[3][0] = q2 * (rr3 * ra3 * cb * quarter - two * cb)
        J[3][2] = rr2 * ra2 * (four * ca.sq() * (K5h * iCh - q2 * iCXc * K6)
                               + q2 * four * ra3 * ca.sq() * id2A * (K6 - K5v))
        J[3][3] = q2 * rr2 * ra2 * g2 * (one - eight * rr3 * ra3 * cb3 * id2B)
        # L35 (/ rhoq)
        J[4][0] = rq * R3h * W1h
        J[4][1] = ra2 * rr2 * (id2A - id2B) * K5h
        J[4][2] = ra2 * rr2 * Fch * (eight * ca3 * iCXc - one)
        J[4][3] = ra2 * rr2 * Fch * (one - eight * rr3 * cb3 * iCXc)
        # L36 (x rhoq^2)
        J[5][0] = q3 * R3h * W2
        J[5][1] = q2 * ra2 * rr2 * (id2A - id2B) * K6
        J[5][2] = ra2 * rr2 * (eight * ca3 * Fch * iCh - q3 * Fch)
        J[5][3] = ra2 * rr2 * (eight * rr3 * cb3 * Fch * iCh - q3 * Fch)
        return J
    return entries

def crosscheck():
    import random
    random.seed(113)
    ok = tried = 0
    while tried < 5:
        rav = F(random.randint(1, 25), 128)
        tbv = F(random.randint(-25, 25), 32)
        rqv = F(random.randint(1, 12), 64)
        tqv = F(random.randint(-30, 30), 32)
        oq = 1 + tqv * tqv
        al = -(1 - tqv * tqv) / oq
        be = 2 * tqv / oq
        rrv = 1 + rqv * al
        tav = tbv + rqv * be
        oa = 1 + tav * tav
        cav = (1 - tav * tav) / oa
        sav = 2 * tav / oa
        ob = 1 + tbv * tbv
        cbv = (1 - tbv * tbv) / ob
        sbv = 2 * tbv / ob
        if cav <= 0 or cbv <= 0 or rrv <= 0:
            continue
        tried += 1
        uv = rav * cav
        vv = 1 + rav * sav
        pv = rrv * rav * cbv
        qv = 1 + rrv * rav * sbv
        pt = [(x, x) for x in (rav, tbv, rqv, tqv)]
        Jc = entry_factory("iv")(pt)
        Jo = pl.r21.entry_matrix((uv, uv), (vv, vv), (pv, pv), (qv, qv))
        base = [F(1, 1) / rav, F(1, 1) / rav, rav**2, rrv**2 * rav**2,
                rav * rrv**2, rav * rrv**2]
        extra = [rqv**2, rqv**2, rqv**2, rqv**2, F(1, 1) / rqv, rqv**2]
        rowscale = [b * e for b, e in zip(base, extra)]
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
                    print(f"MISMATCH row {i} col {j}: {float(mid_c)} vs {float(mid_o)}")
                    good = False
        ok += good
    print(f"crosscheck: {ok}/5 points OK", flush=True)
    return ok == 5

def discard(box):
    rab, tbb, rqb, tqb = box
    rq, tq, tb = IV.raw(*rqb), IV.raw(*tqb), IV.raw(*tbb)
    Z = IV(0)
    Frac = lambda a, b: IV(F(a, b))
    CX2 = gen.CXn(rq, tq, Z, tb, Frac) * (gen.CXd(rq, tq, Z, tb, Frac)).inv()
    if CX2.hi < F(1, 1024):
        return True                      # M1-vert (pending)
    return False

def main():
    resume = "--resume" in sys.argv
    if not resume and not crosscheck():
        print("crosscheck FAILED, aborting")
        return
    seed = [((F(0), F(7, 32)), (F(-1), F(1)), (F(0), F(1, 4)), (F(-1), F(1)))]
    pl.run_covering(
        "m1", seed,
        entry_factory("iv"), entry_factory("dv"),
        HERE / "artifacts",
        "E:/_Datos/caos-research/central-configurations/EXP-022",
        discard=discard, depth=44, budget=21600, resume=resume)

if __name__ == "__main__":
    main()
