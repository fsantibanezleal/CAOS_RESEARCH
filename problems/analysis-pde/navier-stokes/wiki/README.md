# navier-stokes wiki

The September 2026 finite-time blowup claims for fluid equations, what they actually say, and the one
piece of analysis this problem contributed. Written per unit as the units landed, per ADR-0056 and
methodology 05.

The blowup mechanism described here is due to **Diego Cordoba and Luis Martinez-Zoroa**, pushed to
smooth forcing by **Levent Alpoge and Tristan Buckmaster**, with a different mechanism for the viscous
case produced by **OpenAI**. Nothing in this problem is our mechanism.

## Pages

1. [The problem as Fefferman states it](01-the-problem-as-fefferman-states-it.md).
   The system, the admissibility conditions (4) to (11), the four alternatives, and the asymmetry that
   everything turns on: (A) and (B) are unforced, (C) and (D) are not, and all four count for the
   prize.
2. [The two September 2026 constructions](02-the-two-september-2026-constructions.md).
   The shared low-frequency plus high-frequency scheme; the Alpoge-Buckmaster layer cascade on a
   Rayleigh-Taylor background; the OpenAI self-similar vortex core with its anisotropic Reynolds
   split; a side-by-side comparison.
3. [The modulation system](03-the-modulation-system.md).
   The exact wave, why it does not advect itself, the three amplitude equations, the growth rate
   $\sqrt{A}\sin\varphi$, the amplification identity $\nabla\vartheta(0)=\lambda\Theta\zeta$, and the
   growth-steering-holding cycle.
4. [Dissipation and the frequency cap](04-dissipation-and-the-frequency-cap.md).
   The derived dissipative extension, the frequency cap, the threshold $\alpha_c=1/(4p)$, the
   landscape diagram, and the exact calibration $p=11/4+\sqrt7$ against the published threshold.
5. [What machine verification does and does not establish](05-what-machine-verification-establishes.md).
   The Lean certificates, why third-party provenance of the statement is the strongest fact in them,
   what we audited by hand, and what a faithful statement still does not give you.
6. [Where the published threshold comes from](06-where-the-published-threshold-comes-from.md).
   The Cordoba-Martinez-Zoroa-Zheng exponent budget, the four constraints, the one that binds, and why
   their own heuristic overshoots by exactly one constraint swap.

## The one-paragraph version

Two groups posted finite-time blowup constructions one day apart. OpenAI's Navier-Stokes result is
**forced**, which is Fefferman's alternative (C), a legitimate resolution of one of the four
statements but not the sentence a non-specialist hears. Their companion Euler result is **unforced**
and is the larger mathematical claim. Both certificates state their theorems faithfully, checked
clause by clause against statements written by a third party before the claims existed. Neither proof
has been verified by the community.

Underneath the constructions is an exact four-dimensional reduction whose growth rate carries no
dependence on the wave frequency: frequency buys gradient, not growth, while dissipation charges for
frequency. That gives a cap on how far the layer cascade can be pushed into the viscous regime, it
explains why every published result in the program is inviscid or Darcy, and it sends the published
hypodissipative threshold $(22-8\sqrt7)/9$ to the frequency exponent $11/4+\sqrt7$ exactly.

## What is verified, and how

| claim | where | evidence |
|---|---|---|
| the reduction predicts the PDE | [EXP-002](../experiments/EXP-002-reduction-control/verdict.md) | GPU pseudo-spectral run; peak rate to 4e-05 relative; three corrupted models fail |
| frequency independence | EXP-002 | rate spread 2.7e-04 across $\lambda$ from 20 to 160 |
| the derived dissipative term | EXP-002 | tracks the measured rate to 2.6e-04 absolute across $\alpha$ and $\nu$ |
| $\alpha_c=1/(4p)$, and both repaired omissions are non-binding | [EXP-003](../experiments/EXP-003-threshold-sweep/verdict.md) | 1,000,000 schedules, zero violations; C4 never binds alone |
| $p=11/4+\sqrt7$ at the published threshold | EXP-003 | exact to 6.2e-15 |
| the Lean statements are faithful | [audits](../context/) | clause-by-clause against Fefferman and against the manuscripts |

Not verified: that the Lean projects compile (EXP-001), that the manuscripts support the formalized
statements, and anything at all about a multi-layer PDE simulation.

## Conventions used throughout

Dissipation is $-\nu(-\Delta)^{\alpha}$, so classical viscosity is $\alpha=1$. Cordoba,
Martinez-Zoroa and Zheng write $|\nabla|^{\alpha}=(-\Delta)^{\alpha/2}$, so their exponent is twice
ours. Every number quoted states which convention it is in.

## Assets

- [`assets/dissipation-landscape.svg`](assets/dissipation-landscape.svg), theme-aware through an
  internal `prefers-color-scheme` block rather than page tokens, since a standalone SVG loaded as an
  image cannot read the host page's CSS variables.
