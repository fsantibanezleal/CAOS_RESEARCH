"""EXP-022 mini-chart M3: the vertical far-corner.

Blow-up of fa2b's vertical center {r = 1, tauA = tauB = +1} (both pairs
vertical at infinity, same side and rate; A+ approaches B- across the
axis). The tauA = tauB = -1 center is the mirror image (piece 9e): no
separate run. Chart variables (rhox, t1, t2, epsB): (r - 1, tauA - 1,
tauB - 1) = rhox (n1, n2, n3), rational 2-sphere (n1, n2, n3) =
(2 t1, 2 t2, 1 - t1^2 - t2^2)/(1 + t1^2 + t2^2); the antipodal hemisphere
runs as chart sign -1 (same formulas, direction negated). rhox in
[0, 3/8] covers fa2b's CX^-discard: there |1-r|, |tauA-1|, |tauB-1| are
each <= ... CX^ <= 1/16 forces |aA| <= 1/16 and r|aB| <= 1/8-ish, hence
|tauA - 1|, |tauB - 1| <= 1/4 and |r - 1| <= 1/8 by |bA - r bB| <= CX^:
rhox <= sqrt(1/64 + 2/16) < 3/8. All factorizations machine-generated
(m3_gen): CX^2 = rhox^2 QXn/QXd, CS^2 = rhox^2 QSn/QSd (BOTH cross
distances vanish quadratically here), T-brackets and Fh and aA, aB each
to first order. Entry orders: the aA^2/aB^2 column factors cancel every
blow-up pole in rows L13-L25 (no row rescale); rows L35, L36 divide by
rhox. Fartube's own CX-discard region is exactly this chart's territory.
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
g3 = _load("m3_gen", "m3_gen.py")
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
            rx, t1, t2, eB = (IV.raw(*b) for b in args)
            one, two, m1_, Z = IV(1), IV(2), IV(-1), IV(0)
            four, eight = IV(4), IV(8)
            quarter = IV(F(1, 4))
            Frac = lambda a, b: IV(F(a, b))
        else:
            rx, t1, t2, eB = args
            one, two, m1_, Z = DV(1), DV(2), DV(-1), DV(0)
            four, eight = DV(4), DV(8)
            quarter = DV(F(1, 4))
            Frac = lambda a, b: DV(F(a, b))
        rxs = rx * hemi   # signed radius: hemi = -1 runs the antipode
        # reconstructed physical parameters
        dnm = one + t1.sq() + t2.sq()
        idn = K_inv(dnm)
        n1 = two * t1 * idn
        n2 = two * t2 * idn
        n3 = (one - t1.sq() - t2.sq()) * idn
        r = one + rxs * n1
        tA = one + rxs * n2
        tB = one + rxs * n3
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
        # generated hats (evaluated at the SIGNED radius)
        A = (rxs, t1, t2, eB, Frac)
        SQS = (g3.CS2n(*A) * K_inv(g3.CS2d(*A))).sqrt()
        SQX = (g3.CX2n(*A) * K_inv(g3.CX2d(*A))).sqrt()
        iSQS = icube(SQS)
        iSQX = icube(SQX)
        # Odd-order hats absorb the hemisphere sign so the radius rx stays
        # POSITIVE in every composition: X = rx * (hemi * Xhat(rxs)).
        Th135 = g3.T135n(*A) * K_inv(g3.T135d(*A)) * hemi
        Th154 = g3.T154n(*A) * K_inv(g3.T154d(*A)) * hemi
        Th235 = g3.T235n(*A) * K_inv(g3.T235d(*A)) * hemi
        Th236 = g3.T236n(*A) * K_inv(g3.T236d(*A)) * hemi
        Fhh = g3.Fhn(*A) * K_inv(g3.Fhd(*A)) * hemi
        Ah = g3.Ahn(*A) * K_inv(g3.Ahd(*A)) * hemi
        Bh = g3.Bhn(*A) * K_inv(g3.Bhd(*A)) * hemi
        r3 = r * r * r
        eB3 = eB * eB * eB
        eB2 = eB.sq()
        x3 = rx * rx * rx
        Ah2 = Ah.sq()
        Bh2 = Bh.sq()
        Ah3 = Ah2 * Ah
        Bh3 = Bh2 * Bh
        J = [[Z] * 4 for _ in range(6)]
        # L13 (fa2b scaling, regular)
        J[0][1] = m1_ * aA * quarter + two * aA * r3 * eB3 * iD2A
        J[0][2] = emA * (one - eight * (aA * aA * aA) * iD1A)
        J[0][3] = four * (x3 * Bh2 * iD1B * (Th135 - Th154)
                          - r3 * Bh2 * (iSQS * Th135 - iSQX * Th154))
        # L15
        J[1][1] = m1_ * aB * quarter + two * aB * eB3 * iD2B
        J[1][2] = m1_ * four * (x3 * Ah2 * iD1A * (Th135 + Th154)
                                - Ah2 * (iSQS * Th135 + iSQX * Th154))
        J[1][3] = emB * (one - eight * (aB * aB * aB) * iD1B)
        # L23
        J[2][0] = aA * quarter - two * aA * r3 * eB3 * iD1A
        J[2][2] = m1_ * epA * (one - eight * (aA * aA * aA) * iD2A)
        J[2][3] = four * (x3 * Bh2 * iD2B * (Th235 + Th236)
                          - r3 * Bh2 * (iSQS * Th235 + iSQX * Th236))
        # L25
        J[3][0] = aB * quarter - two * aB * eB3 * iD1B
        J[3][2] = four * (m1_ * (x3 * Ah2 * iD2A * Th235 - Ah2 * iSQS * Th235)
                          + (x3 * Ah2 * iD2A * Th236 - Ah2 * iSQX * Th236))
        J[3][3] = m1_ * epB * (one - eight * (aB * aB * aB) * iD2B)
        # L35 (/ rhox on top of fa2b's scaling)
        J[4][0] = eB2 * (r3 * iD1A - iD1B) * Th135
        J[4][1] = eB2 * (r3 * iD2A - iD2B) * Th235
        J[4][2] = Fhh * (eight * Ah3 * iSQX - one)
        J[4][3] = Fhh * (one - eight * Bh3 * r3 * iSQX)
        # L36 (/ rhox)
        J[5][0] = m1_ * eB2 * (r3 * iD1A - iD1B) * Th154
        J[5][1] = eB2 * (r3 * iD2A - iD2B) * Th236
        J[5][2] = Fhh * (eight * Ah3 * iSQS - one)
        J[5][3] = Fhh * (eight * Bh3 * r3 * iSQS - one)
        return J
    return entries

def crosscheck(hemi):
    import random
    random.seed(127 + hemi)
    ok = tried = 0
    while tried < 5:
        rxv = F(random.randint(1, 10), 64) * hemi
        t1v = F(random.randint(-30, 30), 32)
        t2v = F(random.randint(-30, 30), 32)
        eBv = F(random.randint(1, 20), 32)
        dn = 1 + t1v * t1v + t2v * t2v
        n1v = 2 * t1v / dn
        n2v = 2 * t2v / dn
        n3v = (1 - t1v * t1v - t2v * t2v) / dn
        rv = 1 + rxv * n1v
        tAv = 1 + rxv * n2v
        tBv = 1 + rxv * n3v
        oA = 1 + tAv * tAv
        aAv = (1 - tAv * tAv) / oA
        bAv = 2 * tAv / oA
        oB = 1 + tBv * tBv
        aBv = (1 - tBv * tBv) / oB
        bBv = 2 * tBv / oB
        if aAv <= 0 or aBv <= 0 or rv <= 0 or eBv <= 0:
            continue
        if abs(aAv) < F(1, 64) or abs(aBv) < F(1, 64):
            continue
        tried += 1
        eAv = rv * eBv
        uv, vv = aAv / eAv, bAv / eAv
        pv, qv = aBv / eBv, bBv / eBv
        pt = [(abs(rxv), abs(rxv)), (t1v, t1v), (t2v, t2v), (eBv, eBv)]
        Jc = entry_factory(hemi, "iv")(pt)
        Jo = pl.r21.entry_matrix((uv, uv), (vv, vv), (pv, pv), (qv, qv))
        base = [rv * eBv, eBv, rv * eBv, eBv, rv * eBv, rv * eBv]
        extra = [1, 1, 1, 1, F(1, 1) / abs(rxv), F(1, 1) / abs(rxv)]
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

def make_discard(hemi):
    def discard(box):
        rxb, t1b, t2b, eBb = box
        rx = IV.raw(*rxb) * hemi
        t1, t2 = IV.raw(*t1b), IV.raw(*t2b)
        one, two = IV(1), IV(2)
        idn = (one + t1.sq() + t2.sq()).inv()
        n2 = two * t2 * idn
        n3 = (one - t1.sq() - t2.sq()) * idn
        tA = one + rx * n2
        tB = one + rx * n3
        iopA = (one + tA.sq()).inv()
        aA = (one - tA.sq()) * iopA
        iopB = (one + tB.sq()).inv()
        aB = (one - tB.sq()) * iopB
        if aA.hi < 0 or aB.hi < 0:
            return True                  # unphysical: u < 0 or p < 0
        return False
    return discard

def main():
    resume = "--resume" in sys.argv
    seed = [((F(0), F(3, 8)), (F(-1), F(1)), (F(-1), F(1)), (F(0), F(2, 3)))]
    for hemi in (1, -1):
        if not resume and not crosscheck(hemi):
            print("crosscheck FAILED, aborting")
            return
        nm = f"m3-{'N' if hemi == 1 else 'S'}"
        pl.run_covering(
            nm, seed,
            entry_factory(hemi, "iv"), entry_factory(hemi, "dv"),
            HERE / "artifacts",
            "E:/_Datos/caos-research/central-configurations/EXP-022",
            discard=make_discard(hemi), depth=44, budget=21600, resume=resume)

if __name__ == "__main__":
    main()
