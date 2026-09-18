"""EXP-022 part (e2): the far-tube blow-up chart.

Blows up fa2b's center {r = 1, tauA = tauB} (the two pairs merging at
infinity): r = 1 + rhof alpha, tauA = tauB + rhof beta, with
(alpha, beta) = (-(1 - tauf^2), 2 tauf)/(1 + tauf^2) (alpha <= 0 is the
r <= 1 half; the other half is the swap image, piece 9d). Chart variables
(rhof, tauf, epsB, tauB) in [0, 1/2] x [-1, 1] x [0, 2/3] x [-1, 1].

SEAM (exact): a point of fa2b's region (tauA, tauB in [-1, 1], r <= 1)
with CS^ <= 1/16 has |1 - r| <= CS^-triangle <= 1/4 ... more precisely
|1-r| = ||dirA| - r|dirB|| <= |dirA - r dirB| = CS^ <= 1/16 gives
|1-r| <= 1/16; then |dirA - dirB| <= CS^ + |1-r| <= 1/8, and the chord
formula |dir(s) - dir(t)| = 2|s-t|/sqrt((1+s^2)(1+t^2)) with s, t in
[-1, 1] gives |tauA - tauB| <= |dirA - dirB| * 2/2 <= ... <= 1/8 * 2 = 1/4.
So rhof = |(r-1, tauA-tauB)| <= sqrt(1/256 + 1/16) < 0.26 < 1/2: the chart
covers every discarded box. (The CX^-discards satisfy the same bound via
CX^ >= ... they are re-discarded here into the vertical sub-corner.)

All 1/rhof^3 cancellations are ALGEBRAIC via the generated factorizations
(fartube_gen.py, emitted and spot-checked by verify-fartube.py):
CS^2 = rhof^2 Qn/Qd, T135 = rhof T135n/T135d, T235 = rhof T235n/T235d,
Fh = rhof Fhn/Fhd. Row scalings on top of fa2b's: (L13, L15, L23, L25,
L36) x rhof^2 and L35 / rhof. Discards: {CX^ < 1/16} (the vertical
far-corner where pairs meet ACROSS the axis at infinity: declared pending,
its own mini-chart) and {aA wholly < 0} (unphysical: u < 0 after tauA
leaves [-1, 1] under the blow-up; the physical region has aA >= 0).
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
            rf, tf, eB, tB = (IV.raw(*b) for b in args)
            one, two, m1_, Z = IV(1), IV(2), IV(-1), IV(0)
            four, eight = IV(4), IV(8)
            quarter = IV(F(1, 4))
            Frac = lambda a, b: IV(F(a, b))
        else:
            rf, tf, eB, tB = args
            one, two, m1_, Z = DV(1), DV(2), DV(-1), DV(0)
            four, eight = DV(4), DV(8)
            quarter = DV(F(1, 4))
            Frac = lambda a, b: DV(F(a, b))
        iopf = K_inv(one + tf.sq())
        alpha = m1_ * (one - tf.sq()) * iopf
        beta = two * tf * iopf
        r = one + rf * alpha
        tA = tB + rf * beta
        iopA = K_inv(one + tA.sq())
        aA = (one - tA.sq()) * iopA
        bA = two * tA * iopA
        iopB = K_inv(one + tB.sq())
        aB = (one - tB.sq()) * iopB
        bB = two * tB * iopB
        emA = r * eB - bA
        epA = r * eB + bA
        emB = eB - bB
        epB = eB + bB
        D1A = (aA.sq() + emA.sq()).sqrt()
        D2A = (aA.sq() + epA.sq()).sqrt()
        D1B = (aB.sq() + emB.sq()).sqrt()
        D2B = (aB.sq() + epB.sq()).sqrt()
        def icube(x):
            return K_inv(x * x * x)
        iD1A = icube(D1A); iD2A = icube(D2A)
        iD1B = icube(D1B); iD2B = icube(D2B)
        # generated factorizations
        Th135 = gen.T135n(rf, tf, eB, tB, Frac) * K_inv(gen.T135d(rf, tf, eB, tB, Frac))
        Th235 = gen.T235n(rf, tf, eB, tB, Frac) * K_inv(gen.T235d(rf, tf, eB, tB, Frac))
        Fhh = gen.Fhn(rf, tf, eB, tB, Frac) * K_inv(gen.Fhd(rf, tf, eB, tB, Frac))
        CSh2 = gen.Qn(rf, tf, eB, tB, Frac) * K_inv(gen.Qd(rf, tf, eB, tB, Frac))
        CSh = CSh2.sqrt()
        iCSh = icube(CSh)
        CX2 = gen.CXn(rf, tf, eB, tB, Frac) * K_inv(gen.CXd(rf, tf, eB, tB, Frac))
        CX = CX2.sqrt()
        iCX = icube(CX)
        T154 = aB * emA + aA * emB
        T136 = m1_ * T154
        T236 = aA * epB + aB * epA
        r3 = r * r * r
        eB3 = eB * eB * eB
        eB2 = eB.sq()
        aA3 = aA * aA * aA
        aB3 = aB * aB * aB
        aA2_4 = four * aA.sq()
        aB2_4 = four * aB.sq()
        f2 = rf.sq()
        f3 = f2 * rf
        J = [[Z] * 4 for _ in range(6)]
        # L13 (fa2b x rhof^2)
        J[0][1] = f2 * (m1_ * aA * quarter + two * aA * r3 * eB3 * iD2A)
        J[0][2] = f2 * emA * (one - eight * aA3 * iD1A)
        J[0][3] = aB2_4 * (f3 * iD1B * Th135 - r3 * Th135 * iCSh
                           + f2 * (iD1B - r3 * iCX) * T136)
        # L15 (x rhof^2)
        J[1][1] = f2 * (m1_ * aB * quarter + two * aB * eB3 * iD2B)
        J[1][2] = m1_ * aA2_4 * (f3 * iD1A * Th135 - Th135 * iCSh
                                 + f2 * (iD1A - iCX) * T154)
        J[1][3] = f2 * emB * (one - eight * aB3 * iD1B)
        # L23 (x rhof^2)
        J[2][0] = f2 * (aA * quarter - two * aA * r3 * eB3 * iD1A)
        J[2][2] = f2 * m1_ * epA * (one - eight * aA3 * iD2A)
        J[2][3] = aB2_4 * (f3 * iD2B * Th235 - r3 * Th235 * iCSh
                           + f2 * (iD2B - r3 * iCX) * T236)
        # L25 (x rhof^2)
        J[3][0] = f2 * (aB * quarter - two * aB * eB3 * iD1B)
        J[3][2] = m1_ * aA2_4 * (f3 * iD2A * Th235 - Th235 * iCSh) \
            + aA2_4 * f2 * (iD2A - iCX) * T236
        J[3][3] = f2 * m1_ * epB * (one - eight * aB3 * iD2B)
        # L35 (/ rhof)
        J[4][0] = eB2 * (r3 * iD1A - iD1B) * Th135
        J[4][1] = eB2 * (r3 * iD2A - iD2B) * Th235
        J[4][2] = Fhh * (eight * aA3 * iCX - one)
        J[4][3] = Fhh * (one - eight * aB3 * r3 * iCX)
        # L36 (x rhof^2)
        J[5][0] = m1_ * f2 * eB2 * (r3 * iD1A - iD1B) * T154
        J[5][1] = f2 * eB2 * (r3 * iD2A - iD2B) * T236
        J[5][2] = eight * aA3 * Fhh * iCSh - f3 * Fhh
        J[5][3] = eight * aB3 * r3 * Fhh * iCSh - f3 * Fhh
        return J
    return entries

def crosscheck():
    import random
    random.seed(83)
    ok = tried = 0
    while tried < 5:
        rfv = F(random.randint(1, 12), 32)
        tfv = F(random.randint(-30, 30), 32)
        eBv = F(random.randint(1, 20), 32)
        tBv = F(random.randint(-25, 25), 32)
        opf = 1 + tfv * tfv
        al = -(1 - tfv * tfv) / opf
        be = 2 * tfv / opf
        rv = 1 + rfv * al
        tAv = tBv + rfv * be
        opA = 1 + tAv * tAv
        aAv = (1 - tAv * tAv) / opA
        bAv = 2 * tAv / opA
        opB = 1 + tBv * tBv
        aBv = (1 - tBv * tBv) / opB
        bBv = 2 * tBv / opB
        if aAv <= 0 or aBv <= 0 or rv <= 0:
            continue
        tried += 1
        eAv = rv * eBv
        uv, vv = aAv / eAv, bAv / eAv
        pv, qv = aBv / eBv, bBv / eBv
        pt = [(x, x) for x in (rfv, tfv, eBv, tBv)]
        Jc = entry_factory("iv")(pt)
        Jo = pl.r21.entry_matrix((uv, uv), (vv, vv), (pv, pv), (qv, qv))
        base = [rv * eBv, eBv, rv * eBv, eBv, rv * eBv, rv * eBv]
        extra = [rfv**2, rfv**2, rfv**2, rfv**2, F(1, 1) / rfv, rfv**2]
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
                wid = max(aiv.hi - aiv.lo, hi - lo, F(1, 1 << 22))
                if abs(mid_c - mid_o) > 8 * wid:
                    print(f"MISMATCH row {i} col {j}: {float(mid_c)} vs {float(mid_o)}")
                    good = False
        ok += good
    print(f"crosscheck: {ok}/5 points OK", flush=True)
    return ok == 5

SIXT = F(1, 16)

def discard(box):
    rfb, tfb, eBb, tBb = box
    rf, tf, tB = IV.raw(*rfb), IV.raw(*tfb), IV.raw(*tBb)
    one, two, m1_ = IV(1), IV(2), IV(-1)
    iopf = (one + tf.sq()).inv()
    alpha = m1_ * (one - tf.sq()) * iopf
    beta = two * tf * iopf
    tA = tB + rf * beta
    iopA = (one + tA.sq()).inv()
    aA = (one - tA.sq()) * iopA
    if aA.hi < 0:
        return True                      # unphysical: u < 0
    Frac = lambda a, b: IV(F(a, b))
    eB = IV.raw(*eBb)
    CX2 = gen.CXn(rf, tf, eB, tB, Frac) * (gen.CXd(rf, tf, eB, tB, Frac)).inv()
    if CX2.hi < F(1, 256):
        return True                      # vertical far-corner (pending chart)
    return False

def main():
    resume = "--resume" in sys.argv
    if not resume and not crosscheck():
        print("crosscheck FAILED, aborting")
        return
    seed = [((F(0), F(1, 2)), (F(-1), F(1)), (F(0), F(2, 3)), (F(-1), F(1)))]
    pl.run_covering(
        "fartube", seed,
        entry_factory("iv"), entry_factory("dv"),
        HERE / "artifacts",
        "E:/_Datos/caos-research/central-configurations/EXP-022",
        discard=discard, depth=44, budget=43200, resume=resume)

if __name__ == "__main__":
    main()
