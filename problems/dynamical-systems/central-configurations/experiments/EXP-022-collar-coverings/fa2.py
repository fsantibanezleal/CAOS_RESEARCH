"""EXP-022 part (e), chart F_A2: both pairs far.

Chart variables (epsA, tauA, epsB, tauB): epsX = 1/R_X, dirX = (aX, bX) =
((1 - tauX^2), 2 tauX)/(1 + tauX^2); u = aA/epsA, v = bA/epsA,
p = aB/epsB, q = bB/epsB. Region: epsA in [0, 1/3], epsB in [0, 2/3]
(R_B >= 3/2; below that F_A1 covers), tauA, tauB in [-1, 1]. Discards:
boxes wholly with epsB < epsA (R_B > R_A: the swap image, piece 9d) and
boxes wholly inside the far-tube {CS < 1/16 and CX < 1/16}
(CS = |epsB dirA - epsA dirB|, CX with dirB mirrored): the pairs-merge-at-
infinity structure, covered by its own blow-up chart next.

Scalings: rows (L13, L15, L23, L25) x (epsA, epsB, epsA, epsB), rows
(L35, L36) x epsA epsB; columns mA x 4u^2, mB x 4p^2. Exact T-brackets
absorb every 1/eps:
  T135 = aB(epsA - bA) - aA(epsB - bB),   T154 = aB(epsA-bA) + aA(epsB-bB),
  T235 = -aB(epsA + bA) + aA(epsB + bB),  T236 = aA(epsB+bB) + aB(epsA+bA),
  T136 = -T154,  F~ = bA epsB - bB epsA (= epsA epsB f).
All entries are then polynomial in these over the certified-positive
radicals D1A, D2A, D1B, D2B, CS, CX: analytic on the CLOSED chart
including both infinity faces and both vertical-escape faces.
Crosschecked against the original matrix before running.
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
            eA, tA, eB, tB = (IV.raw(*b) for b in args)
            one, two, m1_, Z = IV(1), IV(2), IV(-1), IV(0)
            four, eight = IV(4), IV(8)
            quarter = IV(F(1, 4))
        else:
            eA, tA, eB, tB = args
            one, two, m1_, Z = DV(1), DV(2), DV(-1), DV(0)
            four, eight = DV(4), DV(8)
            quarter = DV(F(1, 4))
        iopA = K_inv(one + tA.sq())
        aA = (one - tA.sq()) * iopA
        bA = two * tA * iopA
        iopB = K_inv(one + tB.sq())
        aB = (one - tB.sq()) * iopB
        bB = two * tB * iopB
        emA = eA - bA          # epsA - bA
        epA = eA + bA
        emB = eB - bB
        epB = eB + bB
        D1A = (aA.sq() + emA.sq()).sqrt()
        D2A = (aA.sq() + epA.sq()).sqrt()
        D1B = (aB.sq() + emB.sq()).sqrt()
        D2B = (aB.sq() + epB.sq()).sqrt()
        CS = ((aA * eB - aB * eA).sq() + (bA * eB - bB * eA).sq()).sqrt()
        CX = ((aA * eB + aB * eA).sq() + (bA * eB - bB * eA).sq()).sqrt()
        def icube(x):
            return K_inv(x * x * x)
        iD1A = icube(D1A); iD2A = icube(D2A)
        iD1B = icube(D1B); iD2B = icube(D2B)
        iCS = icube(CS); iCX = icube(CX)
        eA3 = eA * eA * eA
        eB3 = eB * eB * eB
        aA3 = aA * aA * aA
        aB3 = aB * aB * aB
        aA2_4 = four * aA.sq()
        aB2_4 = four * aB.sq()
        T135 = aB * emA - aA * emB
        T154 = aB * emA + aA * emB
        T136 = m1_ * T154
        T235 = m1_ * aB * epA + aA * epB
        T236 = aA * epB + aB * epA
        Ft = bA * eB - bB * eA
        J = [[Z] * 4 for _ in range(6)]
        # L13 (x epsA)
        J[0][1] = m1_ * aA * quarter + two * aA * eA3 * iD2A
        J[0][2] = emA * (one - eight * aA3 * iD1A)
        J[0][3] = aB2_4 * ((iD1B - eA3 * iCS) * T135 + (iD1B - eA3 * iCX) * T136)
        # L15 (x epsB)
        J[1][1] = m1_ * aB * quarter + two * aB * eB3 * iD2B
        J[1][2] = m1_ * aA2_4 * ((iD1A - eB3 * iCS) * T135 + (iD1A - eB3 * iCX) * T154)
        J[1][3] = emB * (one - eight * aB3 * iD1B)
        # L23 (x epsA)
        J[2][0] = aA * quarter - two * aA * eA3 * iD1A
        J[2][2] = m1_ * epA * (one - eight * aA3 * iD2A)
        J[2][3] = aB2_4 * ((iD2B - eA3 * iCS) * T235 + (iD2B - eA3 * iCX) * T236)
        # L25 (x epsB)
        J[3][0] = aB * quarter - two * aB * eB3 * iD1B
        J[3][2] = m1_ * aA2_4 * (iD2A - eB3 * iCS) * T235 + aA2_4 * (iD2A - eB3 * iCX) * T236
        J[3][3] = m1_ * epB * (one - eight * aB3 * iD2B)
        # L35 (x epsA epsB)
        J[4][0] = (eA3 * iD1A - eB3 * iD1B) * T135
        J[4][1] = (eA3 * iD2A - eB3 * iD2B) * T235
        J[4][2] = Ft * (eight * aA3 * eB3 * iCX - one)
        J[4][3] = Ft * (one - eight * aB3 * eA3 * iCX)
        # L36 (x epsA epsB)
        J[5][0] = m1_ * (eA3 * iD1A - eB3 * iD1B) * T154
        J[5][1] = (eA3 * iD2A - eB3 * iD2B) * T236
        J[5][2] = Ft * (eight * aA3 * eB3 * iCS - one)
        J[5][3] = Ft * (eight * aB3 * eA3 * iCS - one)
        return J
    return entries

def crosscheck():
    import random
    random.seed(31)
    ok = 0
    for _ in range(5):
        eAv = F(random.randint(1, 10), 32)
        eBv = F(random.randint(1, 20), 32)
        if eBv < eAv:
            eAv, eBv = eBv, eAv
        tAv = F(random.randint(-30, 30), 32)
        tBv = F(random.randint(-30, 30), 32)
        aAv = (1 - tAv * tAv) / (1 + tAv * tAv)
        bAv = 2 * tAv / (1 + tAv * tAv)
        aBv = (1 - tBv * tBv) / (1 + tBv * tBv)
        bBv = 2 * tBv / (1 + tBv * tBv)
        if aAv == 0 or aBv == 0:
            continue
        uv, vv = aAv / eAv, bAv / eAv
        pv, qv = aBv / eBv, bBv / eBv
        pt = [(x, x) for x in (eAv, tAv, eBv, tBv)]
        Jc = entry_factory("iv")(pt)
        Jo = pl.r21.entry_matrix((uv, uv), (vv, vv), (pv, pv), (qv, qv))
        rowscale = [eAv, eBv, eAv, eBv, eAv * eBv, eAv * eBv]
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
    eAb, tAb, eBb, tBb = box
    # the swap image: R_B > R_A wholly (epsB < epsA)
    if eBb[1] < eAb[0]:
        return True
    # the far-tube: CS and CX both wholly below 1/16
    args = [tuple(x) for x in box]
    eA, tA, eB, tB = (IV.raw(*b) for b in args)
    one, two = IV(1), IV(2)
    iopA = (one + tA.sq()).inv()
    aA = (one - tA.sq()) * iopA
    bA = two * tA * iopA
    iopB = (one + tB.sq()).inv()
    aB = (one - tB.sq()) * iopB
    bB = two * tB * iopB
    CS = ((aA * eB - aB * eA).sq() + (bA * eB - bB * eA).sq()).sqrt()
    CX = ((aA * eB + aB * eA).sq() + (bA * eB - bB * eA).sq()).sqrt()
    if CS.hi < SIXT and CX.hi < SIXT:
        return True
    return False

def main():
    resume = "--resume" in sys.argv
    if not resume and not crosscheck():
        print("crosscheck FAILED, aborting")
        return
    seed = [((F(0), F(1, 3)), (F(-1), F(1)), (F(0), F(2, 3)), (F(-1), F(1)))]
    pl.run_covering(
        "fa2", seed,
        entry_factory("iv"), entry_factory("dv"),
        HERE / "artifacts",
        "E:/_Datos/caos-research/central-configurations/EXP-022",
        discard=discard, depth=44, budget=43200, resume=resume)

if __name__ == "__main__":
    main()
