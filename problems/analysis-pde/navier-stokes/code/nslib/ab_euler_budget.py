"""The exponent content of the Alpoge-Buckmaster Euler force estimates, and the dissipation it allows.

Transcribed from *Blowup for the Euler equations with smooth forcing*, Sections 3, 6 and 12,
read in the archived PDF (`references/ab-euler.pdf`) on 2026-09-18. Companion of
`ab_force_budget`, which does the same for the Boussinesq paper.

THE GROWTH LAW (their (3.4)). The principal amplitude pair obeys
`d/dt (T, Omega^) = B (T, Omega^)` with off-diagonal entries `-d/(sigma kappa)` and
`sigma c zeta_1`, where `d = (J zeta) . grad Gamma_<` is the background circulation gradient
and `c = 2 W Gamma_<` is of order one by (2.12). The growing rate is the square root of the
product, so it scales like `sqrt(|grad Gamma|)`: the PENDULUM law, `gamma = 1/2`, in the
blowup variable `grad Gamma` of (1.3). Section 12 confirms it on the chosen sequence:
`sigma_i ~ N_i^(beta/2)` against a deposited circulation gradient `N_i Y_i = N_i^beta`.
Theorem 3.1 of the navier-stokes paper therefore caps this class at `alpha <= 1/4` (ours).

THE EXPONENTS (Section 12, all powers of the layer frequency `N = N_m`).
`beta` is the amplitude margin (amplitude `N^(-(1-beta))`, theirs 1/8), `h = 1 - beta`,
`Pi <= N^v` with `v = p/Q` (their `Pi_i = N_{i-1}^p`, `p = 8`, gauge `q = 10`),
`delta = Pi^d N^(-h)` the per-level parameter (theirs `d = 16`), `h* = h - d v`,
`J = 2k + 8` levels, `k` derivatives controlled, `u >= k v`. Their (12.15):

    activation   1 - e + 2u + v                       set by the seed exponent e, free
    terminal     -(2 h* - 1) k + beta - 9 h* + 2u + v
    means        -2 h + 3u + 6v

must each be below `-tau` (theirs: -6, -6 and -3/2, then (12.14) and (12.16) reach
`N^(-1/2)`; summability needs only `tau > 0`). Side conditions, all theirs:

    (12.13) coefficient quotients, each (A - B d) v - n beta <= 0 (rows below)
    (12.7)  decay exponents positive: a - 5 beta/2 > 0 (localization ell = N_{i-1}^(-a)),
            2 h* - beta/2 > 0, 2 h* - v > 0; and Pi dominates ell^-1, so p >= a
    p. 101  derivative range B + 3 = 9k + 51 <= Q

DISSIPATION, ours: growth needs `nu N_i^(2 alpha) < sigma_{i-1} sin s_i` with
`sigma_{i-1} ~ N_{i-1}^(beta/2)` and `N_i = N_{i-1}^Q`, so `alpha < beta / (4Q)` at a
favourable angle, the same form as the Boussinesq design (pendulum class, `p = Q/beta`).
For a Navier-Stokes version the damping of a localized swirl layer is taken to be
`nu (N |zeta|)^(2 alpha)`, the leading symbol; EXP-002 verified that law for Boussinesq, not
for axisymmetric swirl, which is stated as a caveat wherever the number is used.
"""

from __future__ import annotations

from dataclasses import dataclass

# (A, B, n): the (12.13) quotient Pi^(A - B d) N^(-n beta) must be at most one.
QUOTIENT_ROWS = (
    (3, 1, 1), (4, 2, 2),        # Z-flat first; second
    (4, 1, 1),                   # {U, q}
    (5, 1, 1), (6, 2, 2),        # d_t Z-flat first; second
    (4, 1, 1), (5, 2, 2),        # b gradient fast; slow
    (4, 1, 1),                   # c h . grad V
    (5, 1, 1),                   # 2 varpi V h . grad q
    (2, 1, 0), (3, 2, 1),        # fast; slow transport
    (2, 1, 0), (4, 2, 1),        # fast; slow circulation square
)
PUBLISHED = dict(beta=1 / 8, d=16, p=8, q=10, a=4, e=8, c_Q=2 ** 18, q0=2 ** 20)


def exponents(beta: float, k: int, v: float, u: float, d: float, e: float = 8.0) -> dict:
    """The three force exponents of (12.15) for a general margin."""
    h = 1.0 - beta
    hs = h - d * v
    return {
        "activation": 1 - e + 2 * u + v,
        "terminal": -(2 * hs - 1) * k + beta - 9 * hs + 2 * u + v,
        "means": -2 * h + 3 * u + 6 * v,
        "h_star": hs,
    }


def quotient_rows_hold(beta: float, v: float, d: float) -> bool:
    return all((A - B * d) * v - n * beta <= 1e-15 for A, B, n in QUOTIENT_ROWS)


def min_level_power(beta: float, v: float) -> float:
    """Smallest per-level power d of Pi for which every (12.13) quotient is at most one."""
    return max(max((A - n * beta / v) / B for A, B, n in QUOTIENT_ROWS), 0.0)


def published_check() -> dict:
    """Their constants must pass their own (12.15) targets: the transcription check."""
    P = PUBLISHED
    Q = P["q0"] + 1                      # the smallest Q_i
    v = P["q"] / Q
    u = P["q"] / P["c_Q"]
    k = Q // P["c_Q"]
    ex = exponents(P["beta"], k, v, u, P["d"], P["e"])
    return {
        "Q": Q, "k": k, "v": v, "u": u, **ex,
        "passes": (ex["activation"] < -6 and ex["terminal"] < -6 and ex["means"] < -1.5
                   and quotient_rows_hold(P["beta"], v, P["d"])
                   and 9 * k + 51 <= Q
                   and P["d"] * v < 1 / 16 and 8 * u + 100 * v < 1 / 16),
        "alpha_first_stage": P["beta"] / (4 * Q),
    }


@dataclass(frozen=True)
class Reading:
    """How much of the architecture is held fixed when retuning."""

    tau: float = 0.0             # force target exponent (summability needs only > 0)
    a_over_beta: float = 2.5     # (12.7): a > 5 beta / 2, the localization exponent
    a_floor: float = 1.0         # a layer sits inside its parent's phase cell: a >= 1
    p_over_a: float = 1.0        # Pi dominates ell^-1 = N_{i-1}^a, so p >= a
    free_d: bool = True          # d at the least value (12.13) permits, else 16

    def margin_ok(self, beta: float, k: int, Q: int) -> tuple[bool, dict]:
        a = max(self.a_over_beta * beta, self.a_floor)
        p = self.p_over_a * a
        v = p / Q
        u = k * v
        d = min_level_power(beta, v) if self.free_d else 16.0
        ex = exponents(beta, k, v, u, d)
        hs = ex["h_star"]
        ok = (ex["terminal"] < -self.tau and ex["means"] < -self.tau
              and hs > 0 and 2 * hs - beta / 2 > 0 and 2 * hs - v > 0
              and quotient_rows_hold(beta, v, d) and 9 * k + 51 <= Q and beta < 1)
        return ok, {"a": a, "p": p, "v": v, "d": d, **ex}

    def margin_max(self, k: int, Q: int, steps: int = 4000) -> float:
        best = 0.0
        for i in range(1, steps):
            beta = i / steps
            if self.margin_ok(beta, k, Q)[0]:
                best = beta
        return best

    def ceiling(self, k_max: int = 10, Q_span: int = 150) -> dict:
        rows = []
        for k in range(0, k_max + 1):
            lo = 9 * k + 51
            cands = []
            for Q in range(lo, lo + Q_span):
                m = self.margin_max(k, Q, steps=800)
                cands.append((m / (4 * Q), Q, m))
            a, Q, m = max(cands)
            # refine the margin at the chosen ratio
            m = self.margin_max(k, Q)
            rows.append({"k": k, "Q": Q, "margin": m, "alpha": m / (4 * Q)})
        return {"best": max(rows, key=lambda r: r["alpha"]), "rows": rows}


RELAXED = Reading()
# the most favourable reading: localization at the previous wavelength (a = 1), ignoring the
# a > 5 beta/2 that the (12.7) decay rows require
OPTIMISTIC = Reading(a_over_beta=0.0)
