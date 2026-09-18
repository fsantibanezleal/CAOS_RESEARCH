"""Ceilings for the multiscale layer program, independent of any design constants.

`ab_force_budget` bounds one published DESIGN. This module bounds the MECHANISM CLASSES, which
is the statement that does not move when constants are retuned, and it answers the question
the whole program is aimed at: can a layer cascade reach classical viscosity?

THE ASSUMPTIONS, and where each comes from.

A1  Each layer stops at temperature (or vorticity) amplitude `lambda_q^(-1 + delta)` with
    `delta < 1`. Forced by the blowup statement itself: the field stays bounded while its
    gradient diverges, so the amplitudes must be summable, and at `delta = 1` they are
    order one.
A2  The layer deposits a gradient `A_{q+1} = lambda_q^delta`, by the amplification identity
    `grad vartheta(0) = lambda Theta zeta` of the construction.
A3  Frequencies and gradients are related by `lambda_q = A_q^p` for a fixed `p`. Then
    `p > 1` is not an assumption: by A2, `A_{q+1} = A_q^(p delta)`, the gradients must grow for
    blowup, so `p delta > 1`, and with `delta < 1` from A1 this gives `p > 1/delta > 1`.
A4  The growth rate is set by the background gradient the layer sits on, either
    `sqrt(A)` for the Boussinesq pendulum mechanism, transcribed from the amplitude system
    and confirmed against the nonlinear equations by EXP-002, or `A` for vortex stretching,
    which is the law the hypodissipative Navier-Stokes construction uses and the reason its
    dissipation constraint reads `a = alpha R` rather than ours.
A5  Dissipation damps a layer at `nu lambda^(2 alpha)`. Derived in this problem, confirmed
    against the equations by EXP-002, and shown by EXP-007 to survive localization with a
    relative error `3.6 alpha/(ell lambda)`.

THE ARGUMENT. Growth needs `nu lambda_q^(2 alpha) < c rate(A_q)`. Taking logarithms with
`lambda_q = A_q^p`, for all large `q`:

    rate = sqrt(A):   2 alpha p <= 1/2   =>   alpha <= 1/(4p) < delta/4 < 1/4
    rate = A:         2 alpha p <= 1     =>   alpha <= 1/(2p) < delta/2 < 1/2

The inequality in `alpha` is not strict at this step (at equality the condition reduces to
`nu < c`, which a small viscosity satisfies); strictness comes from `p > 1/delta`.

**Neither class reaches classical viscosity, `alpha = 1` in this convention.** The pendulum
mechanism falls short by a factor four and the stretching mechanism by a factor two, for
reasons that involve no constant of any particular design: only the growth law, the
amplification identity and the requirement that the frequencies grow at all.

That is consistent with the published record and explains a choice made in it: every
hypodissipative result in this program sits below these ceilings, and the group that reached
for the viscous case abandoned the cascade for a self-similar core with a Reynolds number of
order one instead.
"""

from __future__ import annotations

from dataclasses import dataclass

CLASSICAL_ALPHA = 1.0     # classical viscosity in the (-Laplacian)^alpha convention


@dataclass(frozen=True)
class MechanismClass:
    """A class of layer mechanism, identified by the exponent of its growth law."""

    name: str
    rate_exponent: float      # rate ~ A^(rate_exponent): 1/2 for pendula, 1 for stretching

    @property
    def budget_factor(self) -> float:
        """`c` in `alpha < delta/(c Q)`, equal to `2 / rate_exponent`."""
        return 2.0 / self.rate_exponent

    def alpha_max(self, p: float) -> float:
        """Ceiling at a given frequency exponent `p` (`lambda = A^p`): `1/(c p)`."""
        if p <= 1.0:
            raise ValueError("the frequency exponent must exceed 1 for a cascade")
        return 1.0 / (self.budget_factor * p)

    @property
    def class_ceiling(self) -> float:
        """Supremum over admissible designs, approached as `p` tends to 1 from above."""
        return 1.0 / self.budget_factor

    @property
    def shortfall_from_classical(self) -> float:
        """How many times below classical viscosity the whole class sits."""
        return CLASSICAL_ALPHA / self.class_ceiling


PENDULUM = MechanismClass("Boussinesq pendulum", rate_exponent=0.5)
STRETCHING = MechanismClass("vortex stretching", rate_exponent=1.0)
CLASSES = (PENDULUM, STRETCHING)


def in_their_convention(alpha_ours: float) -> float:
    """Convert to the `|grad|^alpha` convention, in which classical viscosity is 2."""
    return 2.0 * alpha_ours


def summary() -> list[dict]:
    """The table the conclusion rests on."""
    from . import ab_force_budget, cascade

    published = {
        "Boussinesq pendulum": ab_force_budget.PUBLISHED.ceiling()["best"]["alpha"],
        "vortex stretching": cascade.ALPHA0_CMZ / 2.0,
    }
    rows = []
    for m in CLASSES:
        best = published[m.name]
        rows.append({
            "mechanism": m.name,
            "rate_law": f"A^{m.rate_exponent}",
            "class_ceiling_ours": m.class_ceiling,
            "class_ceiling_theirs": in_their_convention(m.class_ceiling),
            "times_below_classical": m.shortfall_from_classical,
            "best_published": best,
            "published_below_own_ceiling": m.class_ceiling / best,
        })
    return rows


def reaches_classical(m: MechanismClass) -> bool:
    """Can this class reach classical viscosity at any admissible design? It cannot."""
    return m.class_ceiling >= CLASSICAL_ALPHA


def frequency_exponent_needed_for(alpha: float, m: MechanismClass) -> float:
    """The frequency exponent a target would require. Below 1, hence inadmissible.

    Solving `alpha = 1/(c p)` for `p`. A value at or below 1 means no cascade can be built,
    because the frequencies would have to stop growing.
    """
    if alpha <= 0.0:
        raise ValueError("alpha must be positive")
    return 1.0 / (m.budget_factor * alpha)
