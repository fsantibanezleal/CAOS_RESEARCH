"""EXP-022 mini-chart M1-vert: the vertical collision corner at body 1.

Sphere blow-up (M3 pattern) of bicorner-same's mutual center
{rr = 1, taua = taub = +1}: (rr - 1, taua - 1, taub - 1) = rhoy (n1, n2,
n3), rational 2-sphere in (t1, t2); antipodal hemisphere = chart sign -1
with the odd-hat convention; the taua = taub = -1 center is the mirror
image (piece 9e). Chart variables (rhoa, t1, t2, rhoy) in [0, 7/32] x
[-1, 1]^2 x [0, 1/4].

Covers M1's vertical discard {CXc < 1/32} and bicorner-same's
{CXc < 1/16} near the center. Entry orders mirror M3: the ca^2/cb^2
column factors cancel every pole in rows L13-L25; rows L35, L36 divide by
rhoy. Discards: unphysical boxes (ca.hi < 0 or cb.hi < 0) and the
SQS-cone {SQS < 1/16} (pairs also merging: the last leaf M1v2, declared);
the SQX-cone needs no discard on the physical region... it does: also
{SQX < 1/16} deferred to M1v2 (both cones are lower-dimensional in the
sphere and map to collision structures).
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
gv = _load("m1vert_gen", "m1vert_gen.py")
IV, DV = pl.IV, pl.DV

def dv_inv(x):
    iv = x.v.inv()
    isq = (x.v * x.v).inv()
    return DV(iv, [IV(-1) * isq * g for g in x.g])

def K_inv(x):
    return x.inv() if isinstance(x, IV) else dv_inv(x)

def entry_factory(hemi, mode):
    def entries(args):
        if mode == "iv":
            ra, t1, t2, ry = (IV.raw(*b) for b in args)
            one, two, m1_, Z = IV(1), IV(2), IV(-1), IV(0)
            four, eight = IV(4), IV(8)
            quarter, egt = IV(F(1, 4)), IV(F(1, 8))
            Frac = lambda a, b: IV(F(a, b))
        else:
            ra, t1, t2, ry = args
            one, two, m1_, Z = DV(1), DV(2), DV(-1), DV(0)
            four, eight = DV(4), DV(8)
            quarter, egt = DV(F(1, 4)), DV(F(1, 8))
            Frac = lambda a, b: DV(F(a, b))
        rys = ry * hemi
        dnm = one + t1.sq() + t2.sq()
        idn = K_inv(dnm)
        n1 = two * t1 * idn
        rr = one + rys * n1
        n2 = two * t2 * idn
        n3 = (one - t1.sq() - t2.sq()) * idn
        ta = one + rys * n2
        tb = one + rys * n3
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
        A = (rys, t1, t2, Frac)
        # Per-entry guards: on boxes touching a cone ({CSc = 0} or
        # {CXc = 0}) the corresponding icube is UNDEFINED; entries using it
        # become None and the None-tolerant pipeline skips minors touching
        # them. No cone discard, no deeper chart.
        try:
            iSQS = icube((gv.CSc2n(*A) * K_inv(gv.CSc2d(*A))).sqrt())
        except AssertionError:
            iSQS = None
        try:
            iSQX = icube((gv.CXc2n(*A) * K_inv(gv.CXc2d(*A))).sqrt())
        except AssertionError:
            iSQX = None
        W1h = gv.W1n(*A) * K_inv(gv.W1d(*A)) * hemi
        W2h = gv.W2n(*A) * K_inv(gv.W2d(*A)) * hemi
        G5h = gv.G5n(*A) * K_inv(gv.G5d(*A)) * hemi
        Kbh = gv.Kbn(*A) * K_inv(gv.Kbd(*A)) * hemi
        Fch = gv.Fcn(*A) * K_inv(gv.Fcd(*A)) * hemi
        Cah = gv.Can(*A) * K_inv(gv.Cad(*A)) * hemi
        Cbh = gv.Cbn(*A) * K_inv(gv.Cbd(*A)) * hemi
        K5h = two * G5h + rr * ra * W1h
        K6h = two * Kbh + rr * ra * W2h
        R3h = (IV(3) if mode == "iv" else DV(3)) * n1 \
            + (IV(3) if mode == "iv" else DV(3)) * rys * n1.sq() \
            + rys.sq() * n1 * n1.sq()
        R3h = R3h * hemi                 # (rr^3 - 1) = ry * hemi-adjusted R3h
        ra2 = ra.sq(); ra3 = ra2 * ra
        rr2 = rr.sq(); rr3 = rr2 * rr
        y3 = ry * ry * ry
        Ca2 = Cah.sq(); Cb2 = Cbh.sq()
        Ca3 = Ca2 * Cah; Cb3 = Cb2 * Cbh
        bothSX = iSQS is not None and iSQX is not None
        J = [[None] * 4 for _ in range(6)]
        # L13 (bicorner scaling; regular entries direct)
        J[0][0] = Z
        J[0][1] = m1_ * two * ca * (egt - id2A)
        J[0][2] = m1_ * sa * (one - eight * ca * ca * ca)
        if bothSX:
            J[0][3] = four * (y3 * Cb2 * W1h - rr3 * Cb2 * W1h * iSQS
                              + y3 * Cb2 * W2h - rr3 * Cb2 * W2h * iSQX)
        # L15
        J[1][0] = Z
        J[1][1] = m1_ * two * rr * cb * (egt - id2B)
        if bothSX:
            J[1][2] = four * rr * (Ca2 * W1h * iSQS - y3 * Ca2 * W1h
                                   + y3 * Ca2 * W2h - Ca2 * W2h * iSQX)
        J[1][3] = m1_ * rr * sb * (one - eight * cb * cb * cb)
        # L23
        J[2][0] = ra3 * ca * quarter - two * ca
        J[2][1] = Z
        J[2][2] = ra2 * gam * (one - eight * ra3 * (ca * ca * ca) * id2A)
        if bothSX:
            J[2][3] = ra2 * four * rr2 * (y3 * Cb2 * ra3 * id2B * (K5h + K6h)
                                          - Cb2 * (K5h * iSQS + K6h * iSQX))
        # L25
        J[3][0] = rr3 * ra3 * cb * quarter - two * cb
        J[3][1] = Z
        if bothSX:
            J[3][2] = rr2 * ra2 * four * (Ca2 * (K5h * iSQS - K6h * iSQX)
                                          + y3 * Ca2 * ra3 * id2A * (K6h - K5h))
        J[3][3] = rr2 * ra2 * g2 * (one - eight * rr3 * ra3 * (cb * cb * cb) * id2B)
        # L35 (/ rhoy on top of bicorner's)
        J[4][0] = ry * R3h * W1h
        J[4][1] = ra2 * rr2 * (id2A - id2B) * K5h
        if iSQX is not None:
            J[4][2] = ra2 * rr2 * Fch * (eight * Ca3 * iSQX - one)
            J[4][3] = ra2 * rr2 * Fch * (one - eight * rr3 * Cb3 * iSQX)
        # L36 (/ rhoy)
        J[5][0] = ry * R3h * W2h
        J[5][1] = ra2 * rr2 * (id2A - id2B) * K6h
        if iSQS is not None:
            J[5][2] = ra2 * rr2 * Fch * (eight * Ca3 * iSQS - one)
            J[5][3] = ra2 * rr2 * Fch * (eight * rr3 * Cb3 * iSQS - one)
        return J
    return entries

def crosscheck(hemi):
    import random
    random.seed(131 + hemi)
    ok = tried = 0
    while tried < 5:
        rav = F(random.randint(2, 25), 128)
        t1v = F(random.randint(-30, 30), 32)
        t2v = F(random.randint(-30, 30), 32)
        ryv = F(random.randint(1, 10), 64) * hemi
        dn = 1 + t1v * t1v + t2v * t2v
        n1v = 2 * t1v / dn
        n2v = 2 * t2v / dn
        n3v = (1 - t1v * t1v - t2v * t2v) / dn
        rrv = 1 + ryv * n1v
        tav = 1 + ryv * n2v
        tbv = 1 + ryv * n3v
        oa = 1 + tav * tav
        cav = (1 - tav * tav) / oa
        sav = 2 * tav / oa
        ob = 1 + tbv * tbv
        cbv = (1 - tbv * tbv) / ob
        sbv = 2 * tbv / ob
        if cav < F(1, 64) or cbv < F(1, 64) or rrv <= 0:
            continue
        csc2 = (cav - rrv * cbv)**2 + (sav - rrv * sbv)**2
        cxc2 = (cav + rrv * cbv)**2 + (sav - rrv * sbv)**2
        if csc2 < F(1, 4096) or cxc2 < F(1, 4096):
            continue
        tried += 1
        uv = rav * cav
        vv = 1 + rav * sav
        pv = rrv * rav * cbv
        qv = 1 + rrv * rav * sbv
        pt = [(rav, rav), (t1v, t1v), (t2v, t2v), (abs(ryv), abs(ryv))]
        Jc = entry_factory(hemi, "iv")(pt)
        Jo = pl.r21.entry_matrix((uv, uv), (vv, vv), (pv, pv), (qv, qv))
        base = [F(1, 1) / rav, F(1, 1) / rav, rav**2, rrv**2 * rav**2,
                rav * rrv**2, rav * rrv**2]
        extra = [1, 1, 1, 1, F(1, 1) / abs(ryv), F(1, 1) / abs(ryv)]
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
                wid = max(aiv.hi - aiv.lo, hi - lo, F(1, 1 << 18))
                if abs(mid_c - mid_o) > 8 * wid:
                    print(f"MISMATCH hemi={hemi} row {i} col {j}: "
                          f"{float(mid_c)} vs {float(mid_o)}")
                    good = False
        ok += good
    print(f"crosscheck hemi={hemi}: {ok}/5 points OK", flush=True)
    return ok == 5

SIXT = F(1, 16)

def make_discard(hemi):
    def discard(box):
        rab, t1b, t2b, ryb = box
        ry = IV.raw(*ryb) * hemi
        t1, t2 = IV.raw(*t1b), IV.raw(*t2b)
        one, two = IV(1), IV(2)
        idn = (one + t1.sq() + t2.sq()).inv()
        n2 = two * t2 * idn
        n3 = (one - t1.sq() - t2.sq()) * idn
        ta = one + ry * n2
        tb = one + ry * n3
        ioa = (one + ta.sq()).inv()
        ca = (one - ta.sq()) * ioa
        iob = (one + tb.sq()).inv()
        cb = (one - tb.sq()) * iob
        if ca.hi < 0 or cb.hi < 0:
            return True                  # unphysical
        # NO cone discards: the None-tolerant pipeline handles the cones
        # via per-entry guards (undefined entries skip their minors).
        return False
    return discard

def main():
    resume = "--resume" in sys.argv
    seed = [((F(0), F(7, 32)), (F(-1), F(1)), (F(-1), F(1)), (F(0), F(1, 4)))]
    for hemi in (1, -1):
        if not resume and not crosscheck(hemi):
            print("crosscheck FAILED, aborting")
            return
        nm = f"m1vert-{'N' if hemi == 1 else 'S'}"
        pl.run_covering(
            nm, seed,
            entry_factory(hemi, "iv"), entry_factory(hemi, "dv"),
            HERE / "artifacts",
            "E:/_Datos/caos-research/central-configurations/EXP-022",
            discard=make_discard(hemi), depth=44, budget=21600, resume=resume)

if __name__ == "__main__":
    main()
