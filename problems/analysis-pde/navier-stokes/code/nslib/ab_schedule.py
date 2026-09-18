"""The Alpoge-Buckmaster frequency schedule, and what dissipation would do to it.

Transcribed from L. Alpoge and T. Buckmaster, "Blowup for the Boussinesq equations with
smooth forcing" (2026-09-07), Subsection 3.3, equations (3.7), (3.8), (3.10). Their
construction is inviscid; nothing here is a claim about what they proved. What is computed
is what OUR dissipative extension of their own modulation system (derived in
`modulation.py`, confirmed against the PDE by EXP-002) would require of that schedule if
fractional dissipation were switched on and the schedule left as published.

THE SCHEDULE, AS PUBLISHED.

    beta = 1/8,  Q* >= 200 an integer,  Q_q = Q* + q
    lambda_q = lambda_{q-1}^(Q_q)                                     (3.7)
    k_q = max{k : 120 k <= Q_q, ...},  Theta_seed = -lambda_q^(-k_q - 6),
    L_q = (k_q + 5 + beta) log lambda_q                               (3.8)

`k_q` is the number of derivatives controlled uniformly, and the rule `120 k_q <= Q_q` is
what ties the frequency ratio to the smoothness of the force: **more derivatives require a
larger ratio**. The paper states the consequence of (3.8) exactly:

    |Theta_seed| e^(L_q) = lambda_q^(-7/8)

so a layer stops at temperature amplitude `lambda_q^(-7/8)` and, by the amplification
identity `grad vartheta(0) = lambda Theta zeta`, deposits a gradient

    A_{q+1} = lambda_q |Theta_q| = lambda_q^(1/8).

WHAT THAT MEANS FOR DISSIPATION. Writing the deposited gradient as `A_q = lambda_{q-1}^delta`
with the published margin `delta = 1/8`, the frequency and the background it grows on are
related by

    lambda_q = A_q^(Q_q / delta),      that is    p_q = Q_q / delta = 8 Q_q

in the notation of `cascade.py`. Our growth-positivity constraint `alpha p < 1/4` then reads

    alpha < delta / (4 Q_q) = 1 / (32 Q_q)        (most favourable insertion angle)

and, with their own insertion angle `s_q = L_q sigma_{q-2}/sigma_{q-1}` of (3.10), which is
itself a negative power of the frequency, a factor `Q_{q-1}` tighter:

    alpha < delta / (4 Q_q Q_{q-1}) = 1 / (32 Q_q Q_{q-1}).

**`Q_q = Q* + q` grows without bound, so no positive `alpha` satisfies either at every
stage.** The cascade stalls at a finite stage, and a finite cascade produces a finite
gradient, not blowup. With the published `Q* >= 200` the first stage already fails for any
`alpha` above about `1.6e-04`, and above `7.8e-07` once their own insertion angle is used.

THE STRUCTURAL READING, which is the point of this module: in this construction smooth
forcing and fractional dissipation pull in opposite directions. Smoothness is bought with a
frequency ratio that must grow (to control ever more derivatives), and any positive
dissipation caps that ratio. A hypodissipative version of this mechanism therefore has to
bound `Q`, which bounds the derivatives controlled, or raise the amplitude margin `delta`
toward 1, or change the mechanism. That is a prediction about work not yet released, and it
is recorded as one, with its falsification criterion, in
`../context/2026-09-16-smoothness-versus-dissipation.md`.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

BETA = 0.125                 # their beta
DELTA_PUBLISHED = 0.125      # the amplitude margin: |Theta_q| = lambda_q^(-1 + delta)
Q_STAR_MIN = 200             # their Q* >= 200
DERIVATIVES_PER_RATIO = 120  # their rule 120 k_q <= Q_q


@dataclass(frozen=True)
class ABSchedule:
    """The published schedule, with `Q_q = Q_star + q` and amplitude margin `delta`."""

    Q_star: int = Q_STAR_MIN
    delta: float = DELTA_PUBLISHED

    def Q(self, q: int) -> int:
        """Frequency ratio exponent at stage q: lambda_q = lambda_{q-1}^(Q_q)."""
        if q < 1:
            raise ValueError("stages are indexed from 1")
        return self.Q_star + q

    def derivatives_controlled(self, q: int) -> int:
        """`k_q`, the number of derivatives controlled uniformly at stage q."""
        return self.Q(q) // DERIVATIVES_PER_RATIO

    def p(self, q: int) -> float:
        """Our cascade exponent at stage q: lambda_q = A_q^p with p = Q_q / delta."""
        return self.Q(q) / self.delta

    def alpha_max(self, q: int, favourable_angle: bool = True) -> float:
        """Largest dissipation exponent stage q can carry, in our (-Laplacian)^alpha.

        `favourable_angle=True` gives the optimistic bound `delta / (4 Q_q)`, which assumes
        an insertion angle of order one. Their own angle (3.10) is a negative power of the
        frequency and costs a further factor `Q_{q-1}`.
        """
        bound = self.delta / (4.0 * self.Q(q))
        if favourable_angle:
            return bound
        return bound / self.Q(q - 1) if q > 1 else bound

    def stall_stage(self, alpha: float, favourable_angle: bool = True) -> int | None:
        """First stage whose growth is beaten by dissipation, or None if none is.

        With the favourable angle the condition `alpha < delta/(4 Q_q)` fails as soon as
        `Q_q > delta/(4 alpha)`, that is at `q > delta/(4 alpha) - Q_star`. Returns 1 when
        even the first stage cannot grow.
        """
        if alpha <= 0.0:
            return None
        # Closed form rather than a search: the stall stage is astronomically large for a
        # small alpha (about 3e10 at 1e-12), so a bounded loop would report "never stalls"
        # for exactly the exponents where the point is that it does.
        target = self.delta / (4.0 * alpha)          # Q_q must stay BELOW this
        if favourable_angle:
            return max(1, int(math.ceil(target) - self.Q_star))
        # Their own angle costs a factor Q_{q-1}, which stage 1 does not have: it is
        # governed by the favourable bound, and the product rule starts at stage 2.
        if alpha >= self.alpha_max(1, favourable_angle=False):
            return 1
        # smallest q >= 2 with Q_q Q_{q-1} >= target, solving the quadratic in Q_q
        q_ratio = 0.5 * (1.0 + math.sqrt(1.0 + 4.0 * target))
        return max(2, int(math.ceil(q_ratio) - self.Q_star))


def alpha_max_general(delta: float, Q: float) -> float:
    """The trade-off in one line: `alpha < delta / (4 Q)`.

    `delta` is the amplitude margin (a layer stops at `lambda^(-1 + delta)`, so `delta`
    measures how much gradient a layer deposits per unit frequency) and `Q` the frequency
    ratio exponent. Our cap of `1/4` from `cascade.py` is the limit `delta -> 1`, `Q -> 1`;
    the published smooth-forcing design sits at `delta = 1/8`, `Q >= 200`.
    """
    if delta <= 0.0 or Q <= 0.0:
        raise ValueError("delta and Q must be positive")
    return delta / (4.0 * Q)


def ratio_needed_for(alpha: float, delta: float = DELTA_PUBLISHED) -> float:
    """Largest frequency ratio compatible with a target dissipation exponent."""
    return delta / (4.0 * alpha)


def derivatives_affordable(alpha: float, delta: float = DELTA_PUBLISHED) -> float:
    """How many derivatives of the force their `120 k <= Q` rule can then buy.

    This is the trade-off stated as the thing the construction is actually buying:
    `k <= Q / 120 <= delta / (480 alpha)`. At the published threshold of
    Cordoba-Martinez-Zoroa-Zheng in our convention, `alpha = 0.0463`, it is below one, so
    this schedule cannot control even a single derivative there; at `alpha = 1e-04` it is
    about 2.6.
    """
    return ratio_needed_for(alpha, delta) / DERIVATIVES_PER_RATIO


def smooth_forcing_is_incompatible_with_dissipation(
    schedule: ABSchedule | None = None, epsilon: float = 1e-12
) -> bool:
    """No positive alpha survives every stage: for any `epsilon` some stage falls below it.

    `Q_q = Q* + q` is unbounded while the admissible exponent is `delta/(4 Q_q)`, so the
    admissible set shrinks to zero: stage `q > delta/(4 epsilon) - Q*` cannot carry even
    `epsilon`. Written as a function, and driven by the caller's `epsilon`, so a test
    exercises the reasoning instead of a comment asserting it.
    """
    s = schedule or ABSchedule()
    if epsilon <= 0.0:
        raise ValueError("epsilon must be positive")
    q = int(math.ceil(s.delta / (4.0 * epsilon))) + 1
    return s.alpha_max(q) < epsilon and s.stall_stage(epsilon) is not None


def alpha_max_for_derivatives(k: int, delta: float = 1.0) -> float:
    """Largest dissipation exponent compatible with controlling `k` derivatives.

    Their rule `120 k <= Q` fixes the frequency ratio a given force regularity costs, and
    the dissipation constraint is `alpha < delta / (4 Q)`. Together:

        alpha < delta / (480 k).

    The default `delta = 1` is the most generous amplitude margin the amplification
    identity allows, so this is an upper bound for the mechanism, not for their design.
    Even then **one derivative caps the exponent at 1/480 = 0.00208**, which is 22 times
    below the threshold already proved for a `C^{1,eps}` force by
    Cordoba-Martinez-Zoroa-Zheng (0.0463 in our convention).

    The reading: it is not the constants of the published design that keep this scheme out
    of the hypodissipative regime, it is the correction hierarchy's exchange rate of 120
    ratio per derivative. A hypodissipative version has to change that rate, not retune
    around it.
    """
    if k < 1:
        raise ValueError("k must be at least 1; a force with no derivatives controlled is not the case of interest")
    if not 0.0 < delta <= 1.0:
        raise ValueError("delta must lie in (0, 1]")
    return delta / (float(DERIVATIVES_PER_RATIO) * 4.0 * k)


def gap_to_published_threshold(k: int = 1, delta: float = 1.0) -> float:
    """How far short of the published hypodissipative threshold this scheme falls.

    Ratio of the published threshold (in our convention) to `alpha_max_for_derivatives`.
    Greater than one means the scheme cannot reach the regime that is already proved.
    """
    from . import cascade

    return (cascade.ALPHA0_CMZ / 2.0) / alpha_max_for_derivatives(k, delta)
