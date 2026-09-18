"""EXP-022 chart M2W: the quadruple corner, reparametrised and rescaled.

This replaces m2chart.py on the corner tt in [1/2, 1], where m2's residue
lives. m2 fails there for two reasons, both diagnosed in assembly section
10 and both fixed here.

FIX 1 -- the physical boundary becomes axis aligned. m2 uses tau, and the
physical region uh, ph >= 0 is then the CURVE ct = st |alpha| in
(tt, tau). Axis-aligned bisection can approach that curve but never
resolve it, so a straddling box contains unphysical points at every depth
and no certificate can hold on it; about half of m2's residual boxes
straddle it. Substituting

    alpha = ct W / st,      W in [-1, 1]

gives uh = ct(1 + W)/2 and ph = ct(1 - W)/2, so the physical region is
exactly the box W in [-1, 1]. Nothing unphysical is ever evaluated.

This needs st >= ct, i.e. tt >= tan(pi/8) = 0.4142, which is why the chart
starts at tt = 1/2 (there st/ct >= 4/3, so |alpha| <= 3/4 and
beta = sqrt(1 - alpha^2) is comfortably real). m2 covers tt in [0, 1/2],
where it is clean: every one of its residual boxes has tt above 0.98.

One chart replaces BOTH of m2's sign charts on the alpha side, since W
ranges over both signs. The two charts here are the two signs of beta,
which m2 got from the sign of tau.

FIX 2 -- the starved columns are rescaled. As the pairs collapse the m1
and m2 columns are O(s) while mA and mB are O(s^-2), a ratio of exactly
s^3, and both small singular directions live entirely on (m1, m2). m2
inherits deep's rescales mA x 4u^2 and mB x 4p^2 and rescales nothing
else, so on a failing box its column magnitudes run 5e-6, 7e-7, 1, 1.
Here columns m1 and m2 are divided by Rc*ct, which is legitimate because
rank is invariant under an invertible column scaling, and which cancels
ALGEBRAICALLY because every entry of those columns carries the factor
explicitly once alpha is written in W:

    2u/(Rc ct) = 1 + W,          2p/(Rc ct) = 1 - W
    D135 = ct * D135h,           D135h = W h1/st + beta Rc (1+W)/2
    D235 = ct * D235h,           D235h = W gam/st + beta Rc (1+W)/2
    D136 = Rc ct * D136h,        D136h = -[(1+W) g1 + (1-W) h1]/2
    D236 = Rc ct * D236h,        D236h = -[(1+W) g2 + (1-W) gam]/2

so no division by a vanishing quantity is ever performed, and the chart
stays analytic on the CLOSED region including the face ct = 0 where both
pairs sit on the axis.

Row scalings are m2's: L13, L15, L23, L25, L36 times rho^2 and L35
divided by rho^2 then times Rc. Column scalings are
(1/(Rc ct), 1/(Rc ct), 4u^2, 4p^2), and the crosscheck below verifies the
whole thing against the original matrix at five rational points.
"""
import sys
from fractions import Fraction as F
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
_s = importlib.util.spec_from_file_location("pipeline", HERE / "pipeline.py")
pl = importlib.util.module_from_spec(_s)
_s.loader.exec_module(pl)
IV, DV = pl.IV, pl.DV


def dv_inv(x):
    iv = x.v.inv()
    isq = (x.v * x.v).inv()
    return DV(iv, [IV(-1) * isq * g for g in x.g])


def K_inv(x):
    return x.inv() if isinstance(x, IV) else dv_inv(x)


def entry_factory(bsgn, mode):
    def entries(args):
        if mode == "iv":
            Rc, tt, v, W = (IV.raw(*b) for b in args)
            one, two, m1_, Z = IV(1), IV(2), IV(-1), IV(0)
            four, eight = IV(4), IV(8)
            egt = IV(F(1, 8))
            half = IV(F(1, 2))
        else:
            Rc, tt, v, W = args
            one, two, m1_, Z = DV(1), DV(2), DV(-1), DV(0)
            four, eight = DV(4), DV(8)
            egt = DV(F(1, 8))
            half = DV(F(1, 2))
        iot = K_inv(one + tt.sq())
        ct = (one - tt.sq()) * iot
        st = two * tt * iot
        ist = K_inv(st)
        alpha = ct * W * ist
        beta = (one - alpha.sq()).sqrt()
        if bsgn < 0:
            beta = Z - beta
        opW = one + W
        omW = one - W
        uh = ct * opW * half
        ph = ct * omW * half
        u = Rc * uh
        p = Rc * ph
        wc = Rc * ct * half
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

        i_d1A, i_d2A = icube(d1A), icube(d2A)
        i_d1B, i_d2B = icube(d1B), icube(d2B)
        # The inverse cube of Rc*CXd DIVERGES as Rc goes to zero, and every
        # place it appears is multiplied by enough powers of Rc to cancel
        # it. The cancellation has to be ALGEBRAIC, or the interval is
        # unbounded on any box touching Rc = 0, which is the total-collapse
        # face where both pairs sit on the axis AND merge. Each such term
        # reduces to
        #     r2 * fourXs * (that inverse cube) * D_36
        #         = 4 st^2 Xh^2 ct D_36h Rc^2 / CXd^3
        # so only icube(CXd), with no Rc in it, is ever formed.
        icx3 = icube(CXd)
        u3 = u * u * u
        p3_ = p * p * p

        # the factored forms: D135 = ct * D135h, D136 = Rc*ct * D136h
        D135h = W * h1 * ist + beta * Rc * opW * half
        D235h = W * gam * ist + beta * Rc * opW * half
        D135 = ct * D135h
        D235 = ct * D235h
        D136h = Z - (opW * g1 + omW * h1) * half
        D236h = Z - (opW * g2 + omW * gam) * half
        D136 = Rc * ct * D136h
        D236 = Rc * ct * D236h

        E1 = two * beta * h1 - two * alpha * wc + rho * beta.sq()
        E2 = two * beta * gam - two * alpha * wc + rho * beta.sq()
        F1h = m1_ * two * ct * alpha + st * (beta.sq() - alpha.sq())
        G1h = two * ct * alpha + st * (beta.sq() - alpha.sq())
        SD1 = (d1B.sq() + d1A * d1B + d1A.sq()) * K_inv(d1A + d1B) \
            * i_d1A * i_d1B
        SD2 = (d2B.sq() + d2A * d2B + d2A.sq()) * K_inv(d2A + d2B) \
            * i_d2A * i_d2B
        XAh = (CXd.sq() + two * uh * CXd + four * uh.sq()) \
            * K_inv(CXd + two * uh) * icube(CXd)
        XBh = (CXd.sq() + two * ph * CXd + four * ph.sq()) \
            * K_inv(CXd + two * ph) * icube(CXd)
        # FIX 3. m2's row scaling multiplies L13, L15, L23, L25, L36 by
        # rho^2 = Rc^2 st^2. That clears the collision singularities, but at
        # the total-collapse face Rc = 0 it over-clears: every one of those
        # rows then vanishes identically and only L35 survives, so the chart
        # has rank 1 there and no box touching Rc = 0 can ever certify. The
        # cure is to scale those rows by st^2 instead, i.e. to divide the
        # rho^2 scaling by Rc^2. Every term in them carries at least Rc^2
        # explicitly, so the division is ALGEBRAIC: below, u3 = Rc^3 uh3,
        # p3_ = Rc^3 ph3, fourps = 4 Rc^2 ph2, r2 = Rc^2 st2, r3 = Rc^3 st3,
        # and D136 = Rc ct D136h, so exactly Rc^2 comes out of each.
        st2 = st.sq()
        st3 = st2 * st
        uh2 = uh.sq()
        ph2 = ph.sq()
        uh3 = uh2 * uh
        ph3 = ph2 * ph
        Rc2 = Rc.sq()
        Rc3 = Rc2 * Rc
        st2ct = four * st2 * ct * icx3

        def cxterm(Dh, sq):
            return st2ct * Dh * sq

        J = [[Z] * 4 for _ in range(6)]
        # L13 x st^2                        (m1 column is zero here)
        J[0][1] = m1_ * st2 * opW * (egt - i_d2A)
        J[0][2] = st2 * h1 * (one - eight * Rc3 * uh3 * i_d1A)
        J[0][3] = m1_ * Rc3 * st3 * i_d1B * D135 * four * ph2 \
            + four * ph2 * D135 \
            + Rc3 * st2 * ct * D136h * four * ph2 * i_d1B \
            - cxterm(D136h, ph2)
        # L15 x st^2
        J[1][1] = m1_ * st2 * omW * (egt - i_d2B)
        J[1][2] = four * uh2 * (Rc3 * st3 * i_d1A * D135 - D135) \
            + Rc3 * st2 * four * uh2 * i_d1A * ct * D136h \
            - cxterm(D136h, uh2)
        J[1][3] = st2 * g1 * (one - eight * Rc3 * ph3 * i_d1B)
        # L23 x st^2                        (m2 column is zero here)
        J[2][0] = st2 * opW * (egt - i_d1A)
        J[2][2] = st2 * gam * (one - eight * Rc3 * uh3 * i_d2A)
        J[2][3] = m1_ * Rc3 * st3 * i_d2B * D235 * four * ph2 \
            + four * ph2 * D235 \
            + Rc3 * st2 * ct * D236h * four * ph2 * i_d2B \
            - cxterm(D236h, ph2)
        # L25 x st^2
        J[3][0] = st2 * omW * (egt - i_d1B)
        J[3][2] = four * uh2 * (Rc3 * st3 * i_d2A * D235 - D235) \
            + Rc3 * st2 * four * uh2 * i_d2A * ct * D236h \
            - cxterm(D236h, uh2)
        J[3][3] = st2 * g2 * (one - eight * Rc3 * ph3 * i_d2B)
        # L35 / rho^2, x Rc   (already O(1); no Rc^2 to remove)
        J[4][0] = m1_ * E1 * D135h * SD1
        J[4][1] = m1_ * E2 * D235h * SD2
        J[4][2] = m1_ * beta * F1h * XAh
        J[4][3] = beta * G1h * XBh
        # L36 x st^2
        J[5][0] = Rc * st3 * E1 * SD1 * D136h
        J[5][1] = Rc * st3 * E2 * SD2 * D236h
        J[5][2] = Rc * beta * (eight * uh3 - st3)
        J[5][3] = Rc * beta * (eight * ph3 - st3)
        return J
    return entries


def crosscheck(bsgn):
    import random
    random.seed(917 + bsgn)
    ok = tried = 0
    guard = 0
    while tried < 5 and guard < 4000:
        guard += 1
        Rcv = F(random.randint(1, 6), 128)
        ttv = F(random.randint(16, 31), 32)
        vv = F(random.randint(-90, 90), 32)
        if abs(vv - 1) < F(3, 32) or abs(vv + 1) < F(3, 32):
            vv = F(1, 3)
        Wv = F(random.randint(-28, 28), 32)
        ot = 1 + ttv * ttv
        ctv = (1 - ttv * ttv) / ot
        stv = 2 * ttv / ot
        if ctv == 0:
            continue
        alv = ctv * Wv / stv
        b2 = 1 - alv * alv
        if b2 <= 0:
            continue
        uhv = ctv * (1 + Wv) / 2
        phv = ctv * (1 - Wv) / 2
        # keep clear of the reference evaluation's grid floor
        if uhv < F(1, 64) or phv < F(1, 64):
            continue
        # beta is irrational in general; evaluate the reference on the
        # SAME interval the chart uses, so the comparison stays exact in
        # every other variable
        pt = [(x, x) for x in (Rcv, ttv, vv, Wv)]
        Jc = entry_factory(bsgn, "iv")(pt)
        bev = IV.raw(b2, b2).sqrt()
        if bsgn < 0:
            bev = IV(0) - bev
        uv = Rcv * uhv
        pv = Rcv * phv
        rhov = Rcv * stv
        fiv = IV(rhov) * bev
        qlo, qhi = vv - fiv.hi, vv - fiv.lo
        Jo = pl.r21.entry_matrix((uv, uv), (vv, vv), (pv, pv), (qlo, qhi))
        tried += 1
        rowscale = [stv ** 2] * 4 + [Rcv / rhov ** 2, stv ** 2]
        colscale = [F(1) / (Rcv * ctv), F(1) / (Rcv * ctv),
                    4 * uv ** 2, 4 * pv ** 2]
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
                    print(f"MISMATCH bsgn={bsgn} row {i} col {j}: "
                          f"{float(mid_c)} vs {float(mid_o)}  "
                          f"(width {float(wid):.3e})")
                    good = False
        ok += good
    print(f"crosscheck bsgn={bsgn}: {ok}/5 points OK "
          f"({guard} draws)", flush=True)
    return ok == 5


# The axis-body slab is widened from 1/16 to 7/32, matching deep.py, which
# already delegates that radius to the bi-corner charts. bicorner-same
# covers d1A <= 7/32 and runs at zero failures, and every one of this
# chart's residual boxes at the narrower radius was verified to map inside
# it: 69996 of 69996, largest d1A 0.093875 against the 0.21875 limit, none
# in the bi-corner's own quadruple-cluster discard. That verification was
# done through the real coordinate map and per box, because the same claim
# taken from a docstring turned out to be one third true for m2.
CORNER = F(7, 32)


def discard(box):
    """The axis-body slabs, at the bi-corner radius. The physical region IS
    the box now, so there is no unphysical discard to make, which is the
    whole point of the reparametrisation."""
    Rcb, ttb, vb, Wb = box
    if vb[0] >= 1 - CORNER and vb[1] <= 1 + CORNER:
        return True
    if vb[0] >= -1 - CORNER and vb[1] <= -1 + CORNER:
        return True
    return False


def main():
    resume = "--resume" in sys.argv
    seed = [((F(0), F(3, 32)), (F(1, 2), F(1)), (F(-3), F(3)), (F(-1), F(1)))]
    for bsgn in (1, -1):
        if not resume and not crosscheck(bsgn):
            print("crosscheck FAILED, aborting")
            return
        nm = f"m2w-{'P' if bsgn == 1 else 'N'}"
        pl.run_covering(
            nm, seed,
            entry_factory(bsgn, "iv"), entry_factory(bsgn, "dv"),
            HERE / "artifacts",
            "E:/_Datos/caos-research/central-configurations/EXP-022",
            discard=discard, depth=48, budget=21600, resume=resume)


if __name__ == "__main__":
    main()
