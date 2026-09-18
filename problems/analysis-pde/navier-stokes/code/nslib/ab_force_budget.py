"""The exponent content of the Alpoge-Buckmaster force estimates, and the dissipation it allows.

Transcribed from their Boussinesq paper, Sections 5 to 8, read in the primary source on
2026-09-17. It replaces the single inequality `J[(1 - delta) - 5/Q] >= k + 6` that
`ab_ceiling` used, which misread two things: the seed rule `lambda^(-k-6)` controls the
ACTIVATION contribution, not the remainder, and the per-level parameter is
`Pi^5 lambda^(-7/8) <= lambda^(-7/8 + 25/Q)` (their p. 69), not `lambda^(-7/8 + 5/Q)`. It also
omitted the nonoscillatory phase means, which are quadratic in the amplitude and cost only
`Pi^2` per physical derivative.

NOTATION. Everything is an exponent of `lambda = lambda_q`. Write `m` for the amplitude
margin (the layer stops at `Y = lambda^(-(1-m))`; theirs is `m = 1/8`), `d` for the number
of force derivatives controlled (their `k_q`), `Q` for the frequency ratio
(`lambda_q = lambda_{q-1}^Q`), and `pi = c_Pi / Q` for the exponent of their coefficient
scale, `Pi <= lambda^(5/Q)` by (7.4). The per-level small parameter is
`delta = Pi^e Y` with `e = 5` (Subsection 7.1.1), so each correction level gains
`g = (1 - m) - e pi`.

THE EIGHT FORCE CONTRIBUTIONS of Theorem 7.3 at derivative order `k <= d`, with the
physical-evaluation cost (7.19): `(lambda Pi^2)^k` for oscillatory profiles and `Pi^(2k)`
for phase-independent ones.

    activation            Pi lambda^(-d-6) (lambda Pi^2)^k      set by the seed, free
    leading means (7.17)  Pi^(2k+3) Y^2                         quadratic in Y
    higher means          lambda Y Pi^(2k-2) delta^4 (vorticity), Y Pi^(2k-2) delta^3
    remainders            (lambda Pi^2)^k lambda Y delta^(2d+9)  first grade J+1 = 2d+9

Each must be at most `lambda^(-tau)`. Their proof uses `tau = 3/2` (7.26), which absorbs the
common majorant `K(d) <= log lambda`; summability of the force series needs only `tau > 0`.
Worst case `k = d` throughout, since every exponent is increasing in `k`.

THE RATIO FLOOR. The correction recursion needs coefficient derivatives through order
`r_* = 9d + 41` (7.15), and Theorem 5.5 supplies them uniformly only through `Q_q - 1`,
because the future-stage sums of Lemma 5.4 converge only for orders `n <= Q_q`. So
`Q >= 9d + 42` is forced by the architecture. Their `120 d <= Q` and `Q >= 201` are
sufficient simplifications on top of it.

DISSIPATION, ours: a layer grows only while `nu lambda^(2 alpha) < sqrt(A) sin s`, which
with `A_q = lambda_{q-1}^m` and an insertion angle of order one is `alpha < m / (4Q)`
(Theorem 3.1 with `p = Q/m`, `gamma = 1/2`).
"""

from __future__ import annotations

from dataclasses import dataclass

PI_COEFF = 5            # (7.4): Pi <= lambda^(5/Q)
LEVEL_PI_POWER = 5      # 7.1.1: delta = Pi^5 lambda^(-7/8), i.e. Pi^5 Y
PUBLISHED_TAU = 1.5     # (7.26): each contribution below lambda^(-3/2)
PUBLISHED_MARGIN = 1 / 8
RANGE_SLOPE, RANGE_OFFSET = 9, 42     # (7.15) and Theorem 5.5: 9d + 41 <= Q - 1


@dataclass(frozen=True)
class Architecture:
    """The structural constants of the estimate architecture, and the force target."""

    tau: float = PUBLISHED_TAU
    pi_coeff: float = PI_COEFF
    level_pi_power: float = LEVEL_PI_POWER
    published_ratio_rule: bool = True     # Q >= max(201, 120 d), their choice

    def ratio_floor(self, d: int) -> int:
        floor = RANGE_SLOPE * d + RANGE_OFFSET
        if self.published_ratio_rule:
            floor = max(floor, 201, 120 * d)
        return floor

    def margin_bounds(self, d: int, Q: float) -> dict[str, float]:
        """Largest margin `m` each constraint allows, solved exactly (all are linear in m)."""
        pi = self.pi_coeff / Q
        ep = self.level_pi_power * pi
        t = self.tau
        return {
            # d(1 + 2 pi) + m - (2d + 9)(1 - m - ep) <= -tau
            "remainder": (d + 9 - 2 * d * pi - (2 * d + 9) * ep - t) / (2 * d + 10),
            # pi(2d + 3) - 2(1 - m) <= -tau
            "leading_means": 1 - (pi * (2 * d + 3) + t) / 2,
            # (2d - 2) pi + m - 4(1 - m - ep) <= -tau
            "higher_means_vorticity": (4 - t - (2 * d - 2) * pi - 4 * ep) / 5,
            # (2d - 2) pi - (1 - m) - 3(1 - m - ep) <= -tau
            "higher_means_scalar": (4 - t - (2 * d - 2) * pi - 3 * ep) / 4,
            # each level must gain: 1 - m - ep > 0
            "level_gain": 1 - ep,
        }

    def margin_max(self, d: int, Q: float) -> tuple[float, str]:
        b = self.margin_bounds(d, Q)
        name = min(b, key=b.get)
        return b[name], name

    def alpha_max(self, d: int, Q: float) -> float:
        m, _ = self.margin_max(d, Q)
        return max(0.0, m) / (4.0 * Q)

    def best_ratio(self, d: int, Q_span: int = 4000) -> tuple[int, float]:
        """Integer ratio maximizing `alpha` at derivative order `d` (their Q_q are integers)."""
        lo = self.ratio_floor(d)
        best = max(range(lo, lo + Q_span), key=lambda Q: self.alpha_max(d, Q))
        return best, self.alpha_max(d, best)

    def ceiling(self, d_max: int = 60) -> dict:
        rows = []
        for d in range(0, d_max + 1):
            Q, a = self.best_ratio(d)
            m, binding = self.margin_max(d, Q)
            rows.append({"d": d, "Q": Q, "margin": m, "binding": binding, "alpha": a})
        best = max(rows, key=lambda r: r["alpha"])
        return {"best": best, "rows": rows}


PUBLISHED = Architecture()                                    # their tau, their ratio rule
RELAXED = Architecture(tau=0.0, published_ratio_rule=False)   # every free choice released
# The most favourable reading of the structural constants: localization at the previous
# wavelength (Pi ~ lambda_{q-1}), and the per-level parameter at the smallest power of Pi the
# scale table (7.14) permits (b1 needs delta >= Pi^5/lambda, b2 needs delta >= Y Pi^3).
OPTIMISTIC = Architecture(tau=0.0, published_ratio_rule=False, pi_coeff=1.0,
                          level_pi_power=3.0)


def published_design_is_feasible(d: int) -> bool:
    """Their own margin 1/8 must pass their own constraints at their own ratio: a sanity check."""
    Q = PUBLISHED.ratio_floor(d)
    m, _ = PUBLISHED.margin_max(d, Q)
    return m >= PUBLISHED_MARGIN


def in_their_convention(alpha_ours: float) -> float:
    return 2.0 * alpha_ours


def shortfall_against_proved(alpha_ours: float) -> float:
    from . import cascade

    return (cascade.ALPHA0_CMZ / 2.0) / alpha_ours


def summary() -> list[dict]:
    """The three readings, each with its best design and the design at one derivative."""
    out = []
    for name, arch in (("published", PUBLISHED), ("relaxed", RELAXED),
                       ("optimistic", OPTIMISTIC)):
        c = arch.ceiling()
        d1 = next(r for r in c["rows"] if r["d"] == 1)
        out.append({
            "reading": name,
            "best": c["best"],
            "best_alpha_theirs": in_their_convention(c["best"]["alpha"]),
            "best_times_below_proved": shortfall_against_proved(c["best"]["alpha"]),
            "one_derivative": d1,
            "one_derivative_times_below_proved": shortfall_against_proved(d1["alpha"]),
        })
    return out
