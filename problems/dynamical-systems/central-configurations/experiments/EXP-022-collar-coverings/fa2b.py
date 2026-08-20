"""EXP-022 part (e), chart F_A2b: both pairs far, RATIO parametrization.

Supersedes fa2.py, whose absolute-scale far-tube criterion was a design
error: on the double-infinity face epsA = epsB = 0 the unscaled
CS = |epsB dirA - epsA dirB| vanishes IDENTICALLY, so every box touching
that 2-dim face had undefined 1/CS^3 entries and bisected to the depth cap
(272k structural failures). The geometry is scale-relative: the far-tube
is where cs is small relative to R_A, i.e. |dirA - r dirB| small with
r = R_B/R_A ... = epsA/epsB.

Chart variables (r, tauA, epsB, tauB): epsA = r epsB, r in [0, 1] (the
radius ordering is built in; r > 1 is the swap image), epsB in [0, 2/3],
u = aA/(r epsB), v = bA/(r epsB), p = aB/epsB, q = bB/epsB. The rescaled
cross-separations
  CS^ = sqrt((aA - r aB)^2 + (bA - r bB)^2),
  CX^ = sqrt((aA + r aB)^2 + (bA - r bB)^2)
are ANALYTIC on the closed chart and vanish only on the true far-tube
(r ~ 1, dirA ~ dirB) and the vertical far-corner (CX^): both discarded
here (blow-up chart next). Scalings: rows (L13, L23, L35, L36) x (r epsB),
rows (L15, L25) x epsB; columns mA x 4u^2, mB x 4p^2. Every entry is
polynomial in (r, epsB, aA, bA, aB, bB) over the certified-positive
radicals D1A, D2A, D1B, D2B, CS^, CX^ (entry table in the dossier).
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
            r, tA, eB, tB = (IV.raw(*b) for b in args)
            one, two, m1_, Z = IV(1), IV(2), IV(-1), IV(0)
            four, eight = IV(4), IV(8)
            quarter = IV(F(1, 4))
        else:
            r, tA, eB, tB = args
            one, two, m1_, Z = DV(1), DV(2), DV(-1), DV(0)
            four, eight = DV(4), DV(8)
            quarter = DV(F(1, 4))
        iopA = K_inv(one + tA.sq())
        aA = (one - tA.sq()) * iopA
        bA = two * tA * iopA
        iopB = K_inv(one + tB.sq())
        aB = (one - tB.sq()) * iopB
        bB = two * tB * iopB
        reB = r * eB
        emA = reB - bA
        epA = reB + bA
        emB = eB - bB
        epB = eB + bB
        D1A = (aA.sq() + emA.sq()).sqrt()
        D2A = (aA.sq() + epA.sq()).sqrt()
        D1B = (aB.sq() + emB.sq()).sqrt()
        D2B = (aB.sq() + epB.sq()).sqrt()
        CSh = ((aA - r * aB).sq() + (bA - r * bB).sq()).sqrt()
        CXh = ((aA + r * aB).sq() + (bA - r * bB).sq()).sqrt()
        def icube(x):
            return K_inv(x * x * x)
        iD1A = icube(D1A); iD2A = icube(D2A)
        iD1B = icube(D1B); iD2B = icube(D2B)
        iCS = icube(CSh); iCX = icube(CXh)
        r3 = r * r * r
        eB3 = eB * eB * eB
        eB2 = eB.sq()
        aA3 = aA * aA * aA
        aB3 = aB * aB * aB
        aA2_4 = four * aA.sq()
        aB2_4 = four * aB.sq()
        T135 = aB * emA - aA * emB
        T154 = aB * emA + aA * emB
        T136 = m1_ * T154
        T235 = m1_ * aB * epA + aA * epB
        T236 = aA * epB + aB * epA
        Fh = bA - r * bB
        J = [[Z] * 4 for _ in range(6)]
        # L13 (x r epsB)
        J[0][1] = m1_ * aA * quarter + two * aA * r3 * eB3 * iD2A
        J[0][2] = emA * (one - eight * aA3 * iD1A)
        J[0][3] = aB2_4 * ((iD1B - r3 * iCS) * T135 + (iD1B - r3 * iCX) * T136)
        # L15 (x epsB)
        J[1][1] = m1_ * aB * quarter + two * aB * eB3 * iD2B
        J[1][2] = m1_ * aA2_4 * ((iD1A - iCS) * T135 + (iD1A - iCX) * T154)
        J[1][3] = emB * (one - eight * aB3 * iD1B)
        # L23 (x r epsB)
        J[2][0] = aA * quarter - two * aA * r3 * eB3 * iD1A
        J[2][2] = m1_ * epA * (one - eight * aA3 * iD2A)
        J[2][3] = aB2_4 * ((iD2B - r3 * iCS) * T235 + (iD2B - r3 * iCX) * T236)
        # L25 (x epsB)
        J[3][0] = aB * quarter - two * aB * eB3 * iD1B
        J[3][2] = m1_ * aA2_4 * (iD2A - iCS) * T235 + aA2_4 * (iD2A - iCX) * T236
        J[3][3] = m1_ * epB * (one - eight * aB3 * iD2B)
        # L35 (x r epsB)
        J[4][0] = eB2 * (r3 * iD1A - iD1B) * T135
        J[4][1] = eB2 * (r3 * iD2A - iD2B) * T235
        J[4][2] = Fh * (eight * aA3 * iCX - one)
        J[4][3] = Fh * (one - eight * aB3 * r3 * iCX)
        # L36 (x r epsB)
        J[5][0] = m1_ * eB2 * (r3 * iD1A - iD1B) * T154
        J[5][1] = eB2 * (r3 * iD2A - iD2B) * T236
        J[5][2] = Fh * (eight * aA3 * iCS - one)
        J[5][3] = Fh * (eight * aB3 * r3 * iCS - one)
        return J
    return entries

def crosscheck():
    import random
    random.seed(41)
    ok = 0
    for _ in range(5):
        rv = F(random.randint(1, 31), 32)
        eBv = F(random.randint(1, 20), 32)
        tAv = F(random.randint(-30, 30), 32)
        tBv = F(random.randint(-30, 30), 32)
        aAv = (1 - tAv * tAv) / (1 + tAv * tAv)
        bAv = 2 * tAv / (1 + tAv * tAv)
        aBv = (1 - tBv * tBv) / (1 + tBv * tBv)
        bBv = 2 * tBv / (1 + tBv * tBv)
        if aAv == 0 or aBv == 0:
            continue
        eAv = rv * eBv
        uv, vv = aAv / eAv, bAv / eAv
        pv, qv = aBv / eBv, bBv / eBv
        pt = [(x, x) for x in (rv, tAv, eBv, tBv)]
        Jc = entry_factory("iv")(pt)
        Jo = pl.r21.entry_matrix((uv, uv), (vv, vv), (pv, pv), (qv, qv))
        rowscale = [rv * eBv, eBv, rv * eBv, eBv, rv * eBv, rv * eBv]
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
                wid = max(aiv.hi - aiv.lo, hi - lo, F(1, 1 << 28))
                if abs(mid_c - mid_o) > 8 * wid:
                    print(f"MISMATCH row {i} col {j}: {float(mid_c)} vs {float(mid_o)}")
                    good = False
        ok += good
    print(f"crosscheck: {ok}/5 points OK", flush=True)
    return ok == 5

SIXT = F(1, 16)

def discard(box):
    rb, tAb, eBb, tBb = box
    r, tA, tB = IV.raw(*rb), IV.raw(*tAb), IV.raw(*tBb)
    one, two = IV(1), IV(2)
    iopA = (one + tA.sq()).inv()
    aA = (one - tA.sq()) * iopA
    bA = two * tA * iopA
    iopB = (one + tB.sq()).inv()
    aB = (one - tB.sq()) * iopB
    bB = two * tB * iopB
    CSh = ((aA - r * aB).sq() + (bA - r * bB).sq()).sqrt()
    if CSh.hi < SIXT:
        return True                      # the true far-tube (blow-up chart)
    CXh = ((aA + r * aB).sq() + (bA - r * bB).sq()).sqrt()
    if CXh.hi < SIXT:
        return True                      # the vertical far-corner (ditto)
    return False

def main():
    resume = "--resume" in sys.argv
    if not resume and not crosscheck():
        print("crosscheck FAILED, aborting")
        return
    seed = [((F(0), F(1)), (F(-1), F(1)), (F(0), F(2, 3)), (F(-1), F(1)))]
    pl.run_covering(
        "fa2b", seed,
        entry_factory("iv"), entry_factory("dv"),
        HERE / "artifacts",
        "E:/_Datos/caos-research/central-configurations/EXP-022",
        discard=discard, depth=44, budget=10800 if resume else 43200, resume=resume)

if __name__ == "__main__":
    main()
