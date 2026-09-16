"""Exponent budget of the Cordoba-Martinez-Zoroa-Zheng hypodissipative construction.

Source, read in the primary: D. Cordoba, L. Martinez-Zoroa, F. Zheng, "Finite time
blow-up for the hypodissipative Navier Stokes equations with a force in
L1_t C^{1,eps}_x and L^inf_t L^2_x", Arch. Ration. Mech. Anal. 250 (2026) article 38,
arXiv:2407.06776v2. Section 1.2.4 (heuristic) and Section 4 (construction and force
estimates 4.3.2 to 4.3.5). The construction and the constants are theirs; this module
only makes their exponent bookkeeping explicit and checks which constraint sets the
published threshold.

Convention: THEIR dissipation |grad|^alpha, so classical viscosity is their alpha = 2.

Parameters, all exponents of a large base N, per power R^n:

    M_n = N^(R^n)          frequency of vortex layer n
    A_n = N^(a R^n)        amplitude of layer n; the stretching felt by layer n is
                           A_{n-1} = N^((a/R) R^n)
    L_n = N^(b R^n)        localization scale of layer n
    s                      Holder margin of the force, which must be positive

Constraints at the level of exponents (delta -> 0, logarithmic factors dropped):

    D    dissipation absorbed with equality:   a = alpha R          (Section 4.3.5)
    S    self-interaction error summable:      2a - a/R + b + s - 1 <= 0   (4.3.2)
    L    localization inside the outer layer:  b >= a + 1/R + s             (4.3.3)
    O    outer velocity on the inner layer:    a + 2/R + s + 1 - 3b <= 0    (4.3.4)

Result, derived rather than fitted (every coefficient below follows from D, S, O):

    with D and S saturated, O reads    s < (2 + 3 alpha - 7 alpha R - 2/R) / 4
    optimum over R:                    alpha R^2 = 2/7, i.e. R = sqrt(2/(7 alpha)),
                                       which is exactly the paper's choice
    optimal margin:                    s(alpha) = (2 + 3 alpha - 2 sqrt(14 alpha)) / 4
    s(alpha) = 0 at                    alpha_0 = (22 - 8 sqrt 7) / 9   (the theorem)
    L at that point is SLACK by        (sqrt(2 alpha / 7) - alpha) / 2 > 0

The paper's heuristic (Section 1.2.4) binds on L instead and does not contain O:

    with D and S saturated, L reads    s <= (1 + alpha - 3 alpha R - 1/R) / 2
    optimum:                           alpha R^2 = 1/3,  s(alpha) = (1+alpha)/2 - sqrt(3 alpha)
    threshold:                         5 - 2 sqrt 6 = 0.10102...

So the gap between the heuristic threshold and the proved one is exactly a swap of the
binding constraint: the heuristic's binder (localization) is slack in the proof, and the
proof's binder (outer velocity on the inner layer) is absent from the heuristic.

What this corrects in our own record. Under D the frequency and the stretching obey
ln M_n = (1/alpha) ln A_{n-1} at EVERY alpha. Our cascade model's relation
alpha_c = 1/(4p) is that same saturated constraint, so p = 1/(2 alpha) holds identically
along the whole family and does not select alpha_0. The published threshold is set by O,
which our reduced cascade model does not contain. See `implied_p_is_tautological`.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

ALPHA0 = (22.0 - 8.0 * math.sqrt(7.0)) / 9.0
ALPHA_HEURISTIC = 5.0 - 2.0 * math.sqrt(6.0)


# ---------------------------------------------------------------- the binding budget


def s_bound_outer(alpha: float, R: float) -> float:
    """Largest Holder margin allowed by constraint O with D and S saturated."""
    return (2.0 + 3.0 * alpha - 7.0 * alpha * R - 2.0 / R) / 4.0


def s_bound_localization(alpha: float, R: float) -> float:
    """Largest margin allowed by constraint L with D and S saturated (the heuristic)."""
    return (1.0 + alpha - 3.0 * alpha * R - 1.0 / R) / 2.0


def optimal_R_outer(alpha: float) -> float:
    """argmax_R of `s_bound_outer`: alpha R^2 = 2/7."""
    return math.sqrt(2.0 / (7.0 * alpha))


def optimal_R_localization(alpha: float) -> float:
    """argmax_R of `s_bound_localization`: alpha R^2 = 1/3."""
    return 1.0 / math.sqrt(3.0 * alpha)


def s_max_outer(alpha: float) -> float:
    """The paper's s(alpha) = (2 + 3 alpha - 2 sqrt(14 alpha)) / 4."""
    return (2.0 + 3.0 * alpha - 2.0 * math.sqrt(14.0 * alpha)) / 4.0


def s_max_localization(alpha: float) -> float:
    """The paper's heuristic s(alpha) = (1 + alpha)/2 - sqrt(3 alpha)."""
    return (1.0 + alpha) / 2.0 - math.sqrt(3.0 * alpha)


# ------------------------------------------------------------ parameter point checks


@dataclass(frozen=True)
class Point:
    """One parameter choice (alpha, R, a, b, s) in exponent form."""

    alpha: float
    R: float
    a: float
    b: float
    s: float

    @classmethod
    def published(cls, alpha: float) -> "Point":
        """The parameters chosen in Section 4 of the paper, at a given alpha."""
        R = math.sqrt(2.0 / (7.0 * alpha))
        a = math.sqrt(2.0 * alpha / 7.0)
        s = s_max_outer(alpha)
        b = 1.0 + alpha - s - 2.0 * a
        return cls(alpha=alpha, R=R, a=a, b=b, s=s)

    # Each residual is <= 0 when the constraint holds; 0 means it binds.
    def residual_D(self) -> float:
        return self.alpha * self.R - self.a

    def residual_S(self) -> float:
        return 2.0 * self.a - self.a / self.R + self.b + self.s - 1.0

    def residual_L(self) -> float:
        return (self.a + 1.0 / self.R + self.s) - self.b

    def residual_O(self) -> float:
        return self.a + 2.0 / self.R + self.s + 1.0 - 3.0 * self.b

    def residual_dissipation_summable(self) -> float:
        """Section 4.3.5 needs M^(alpha - sqrt(2 alpha/7)) summable, i.e. alpha < a."""
        return self.alpha - self.a

    def binding(self, tol: float = 1e-12) -> dict[str, str]:
        out = {}
        for name, r in (("D", self.residual_D()), ("S", self.residual_S()),
                        ("L", self.residual_L()), ("O", self.residual_O()),
                        ("dissipation_summable", self.residual_dissipation_summable())):
            out[name] = "binds" if abs(r) <= tol else ("holds" if r < 0 else "VIOLATED")
        return out


def localization_slack_at_published(alpha: float) -> float:
    """How far constraint L is from binding at the published point: (sqrt(2a/7) - a)/2."""
    return -Point.published(alpha).residual_L()


# ------------------------------------------------------------------ the correction


def implied_p_is_tautological(alpha: float) -> float:
    """Return ln M_n / (2 ln sigma_n) - 1/(2 alpha) at the published point; it is zero.

    Our cascade model wrote lambda ~ sigma^(2p) and read the published threshold as
    p = 1/(2 alpha_0). At the published parameters the frequency and the stretching
    satisfy ln M_n = (1/alpha) ln A_{n-1} at every alpha, so 2p = 1/alpha holds along
    the entire family, not just at alpha_0. The identity therefore carries no
    information about where alpha_0 sits. Returned as a residual so tests can assert 0.
    """
    p = Point.published(alpha)
    ln_M_over_ln_rate = 1.0 / (p.a / p.R)   # per R^n: ln M_n = R^n, ln A_{n-1} = (a/R) R^n
    return ln_M_over_ln_rate / 2.0 - 1.0 / (2.0 * alpha)


# ------------------------------------------------- the admissible frequency ratios


def feasible_R_interval(alpha: float) -> tuple[float, float] | None:
    """Range of frequency ratios `R` that admit a positive force margin, or None.

    With dissipation and self-interaction saturated, the outer-velocity constraint reads
    `4 s < 2 + 3 alpha - 7 alpha R - 2/R`, so a positive margin needs

        7 alpha R^2 - (2 + 3 alpha) R + 2 < 0,

    a quadratic in `R` whose roots bound the admissible interval:

        R_pm = [ (2 + 3 alpha) +/- sqrt((2 + 3 alpha)^2 - 56 alpha) ] / (14 alpha).

    The discriminant is exactly `9 alpha^2 - 44 alpha + 4`, so it vanishes at
    `alpha_0 = (22 - 8 sqrt 7)/9`: **the interval of admissible frequency ratios closes to
    a single point precisely at the published threshold**, and that point is the paper's
    own `R = sqrt(2/(7 alpha))`. Above the threshold there is no admissible ratio at all.

    The lower end is what matters structurally: `R_- > 1` for every `alpha > 0`, tending
    to 1 only as `alpha -> 0`. A cascade whose frequencies grow geometrically, so that
    `ln M_n` is linear in `n` rather than geometric, is the case `R = 1`, and it is
    inadmissible at every positive dissipation: with `R = 1` the localization constraint
    needs `b >= a + 1 + s` while self-interaction allows only `b <= 1 - a - s`, which
    forces `alpha + s <= 0`. **The construction does not merely prefer super-geometric
    frequency growth, it requires it**, and requires more of it as `alpha` rises.
    """
    if alpha <= 0.0:
        raise ValueError("alpha must be positive")
    disc = (2.0 + 3.0 * alpha) ** 2 - 56.0 * alpha
    if disc < 0.0:
        return None
    root = math.sqrt(disc)
    return ((2.0 + 3.0 * alpha - root) / (14.0 * alpha),
            (2.0 + 3.0 * alpha + root) / (14.0 * alpha))


def geometric_cascade_margin(alpha: float) -> float:
    """Force margin available at `R = 1`, the geometric cascade. Always negative.

    Evaluates `(2 + 3 alpha - 7 alpha - 2)/4 = -alpha` at `R = 1`: the outer-velocity
    budget allows only `s < -alpha`, so a geometric cascade has no admissible force
    margin at any positive dissipation, and the deficit is exactly `alpha`.
    """
    return s_bound_outer(alpha, 1.0)
