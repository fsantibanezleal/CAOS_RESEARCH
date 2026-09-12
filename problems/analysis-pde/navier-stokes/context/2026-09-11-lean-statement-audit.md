# Audit: does the OpenAI Lean certificate state Fefferman's (C) and (D)?

Date: 2026-09-11. Auditor: this session. Subject: `openai/NavierStokesAndEuler` at last push
2026-09-10T15:14:13Z, cloned at depth 1 to `E:/_Temp/lean-ns`. Method: read the challenge and solution
modules directly and compare them clause by clause with the official Clay text.

This audit covers **the statement only**. It does not certify the proof. A Lean build was not run here
(see the cost note at the end), so nothing below asserts that the 641,332 lines compile.

## Why this audit is the right first move

A machine-checked proof answers "does this argument follow", never "is this the theorem". The standard
failure of a formalized claim is a faithful-looking definition that quietly weakens the hypothesis or
strengthens the conclusion, and it is invisible to the kernel. Our own record already carries two
instances of a green gate that measured the wrong subject. So the first question about a 641k-line
certificate is not whether it compiles; it is what it says.

## Repository shape, measured

| measurement | value |
|---|---|
| Lean files | 2,659 |
| Lean lines | 641,332 |
| `sorry` outside `ComparatorChallenges/` | 0 |
| `sorry` inside `ComparatorChallenges/` | 5 (the reference stubs, by design) |
| `axiom` declarations added by the project | 0 |
| declared permitted axioms | `propext`, `Quot.sound`, `Classical.choice` |
| license | Apache-2.0 |
| `formalization.yaml` review status | `self-assessed` |

The five `sorry`s are correct design rather than a gap: `ComparatorChallenges/NavierStokes.lean` and
`ComparatorChallenges/Euler.lean` hold the *reference statements* with `sorry` proofs, and Comparator
checks that the separately proved declarations in `NavierStokes/ComparatorSolution.lean` and
`Euler/Solution.lean` have the same type. The solution module is a one-liner per theorem:

```lean
theorem navier_stokes_breakdown_R3 (nu : ℝ) (hnu : nu > 0) :
    ∃ (u₀ : ℝ³ → ℝ³) (f : ℝ³ → ℝ → ℝ³),
    InitialVelocityConditionDecay u₀ ∧ ForceConditionDecay f ∧
    ¬ (∃ v p, NavierStokesExistenceAndSmoothnessRn nu u₀ f v p) := by
  exact ComparatorBridge.navier_stokes_breakdown_R3 nu hnu
```

**The strongest single fact in this repository is provenance of the statement.** The challenge file is
adapted from Google DeepMind's Formal Conjectures entry
`FormalConjectures/Millenium/NavierStokes.lean`, credited in both `formalization.yaml`
(`relationship: builds-on`) and `ComparatorChallenges/README.md`. The definitions that decide whether
the theorem is the right theorem were therefore written by a third party with no stake in the claim,
before the claim existed. That removes the most common way a formalized result can be hollow.

## Clause-by-clause comparison

Fefferman (C) requires: $\nu>0$, $n=3$; a smooth divergence-free $u^{\circ}$ satisfying (4); a smooth
$f$ on $\mathbb{R}^3\times[0,\infty)$ satisfying (5); and no $(p,u)$ satisfying (1), (2), (3), (6),
(7) on $\mathbb{R}^3\times[0,\infty)$.

| Clay clause | Lean encoding | verdict |
|---|---|---|
| $\nu>0$ | `(nu : ℝ) (hnu : nu > 0)` | faithful |
| $n=3$ | `ℝ³ → ℝ³` | faithful |
| $u^{\circ}$ smooth | `InitialVelocityCondition.smooth : ContDiff ℝ ∞ u₀` | faithful |
| $u^{\circ}$ divergence free | `div_free : ∀ x, ∇⬝ u₀ x = 0` | faithful |
| (4) rapid decay of $u^{\circ}$ | `decay : ∀ m K, ∃ C, ∀ x, ‖iteratedFDeriv ℝ m u₀ x‖ ≤ C / (1 + ‖x‖) ^ K` | faithful, see note 1 |
| $f$ smooth on the closed half-slab | `ForceCondition.smooth : ContDiffOn ℝ ∞ (↿f) (univ ×ˢ Ici 0)` | faithful |
| (5) rapid decay of $f$ in $(1+\lVert x\rVert+t)$ | `decay : ∀ m K, ∃ C, ∀ x, ∀ t ≥ 0, ‖iteratedFDerivWithin ℝ m (↿f) (univ ×ˢ Ici 0) (x,t)‖ ≤ C / (1 + ‖x‖ + t) ^ K` | faithful, note 1 |
| (1) the momentum equation | `derivWithin (v x ·) (Ici 0) t + fderiv ℝ (v · t) x (v x t) = nu • Δ (v · t) x - gradient (p · t) x + f x t` | faithful, note 2 |
| (2) incompressibility for all $t\ge0$ | `div_free : ∀ x, ∀ t ≥ 0, ∇⬝ (v · t) x = 0` | faithful |
| (3) initial condition | `initial_condition : ∀ x, v x 0 = u₀ x` | faithful |
| (6) $p,u\in C^{\infty}(\mathbb{R}^3\times[0,\infty))$ | `velocity_smooth`, `pressure_smooth : ContDiffOn ℝ ∞ … (univ ×ˢ Ici 0)` | faithful |
| (7) uniformly bounded energy | `integrable : ∀ t ≥ 0, MemLp (‖v · t‖) 2` and `globally_bounded_energy : ∃ E, ∀ t ≥ 0, (∫ x, ‖v x t‖ ^ 2) < E` | faithful |
| the conclusion: no such $(p,u)$ | `¬ (∃ v p, NavierStokesExistenceAndSmoothnessRn nu u₀ f v p)` | faithful |

Note 1. Fefferman indexes decay by a multi-index $\alpha$; the Lean version indexes by derivative order
$m$ and bounds the norm of the full $m$-th Frechet derivative. These are equivalent up to constants,
because $\lVert\partial^{\alpha}g\rVert \le \lVert D^{m}g\rVert$ for $|\alpha| = m$ and conversely the
Frechet norm is controlled by finitely many partials of the same order. The quantifier order
$\forall m\,\forall K\,\exists C$ matches Fefferman's "for any $\alpha$ and $K$" with $C_{\alpha K}$
depending on both. No weakening.

Note 2. The momentum equation is stated pointwise and classically, with a one-sided time derivative on
$[0,\infty)$. Since the solution class already demands $C^{\infty}$ on the closed half-slab, this is
the strong formulation, which is the correct reading of Fefferman's (1) together with (6). It is not a
weak or distributional relaxation, so the non-existence conclusion is correspondingly *harder*, not
easier: it denies even the existence of a classical solution.

The periodic case (D) substitutes `InitialVelocityConditionPeriodic` (adds `IsOnePeriodic u₀`,
condition 8), `ForceConditionPeriodic` (adds spatial 1-periodicity and the time-only decay of
condition 9), and `NavierStokesExistenceAndSmoothnessPeriodic` (adds 1-periodicity of the velocity,
condition 10, and of the pressure). The pressure periodicity is documented in the source as following
"the errata appended to the Clay problem statement". The energy condition is correctly absent from the
periodic class, matching Fefferman, who imposes (10) and (11) rather than (7) there.

**Statement-level verdict: the formal theorems are a faithful rendering of Fefferman's alternatives
(C) and (D).** I found no weakened hypothesis, no strengthened conclusion, and no smuggled extra
assumption. The one direction of divergence is in OpenAI's favour: their paper delivers a compactly
supported force where (5) only asks for rapid decay.

## The Euler certificate

`Euler.exists_compact_smooth_euler_singularity` and `Euler.euler_breakdown_R3` are declared in
`Euler/Solution.lean` with the same zero-`sorry`, three-axiom profile and their own Comparator config.
Their subject is the **unforced** equation, which is the claim with the greater mathematical
consequence and which has no Clay reference statement to be checked against. That asymmetry matters:
the Navier-Stokes statement inherits a third-party reference, the Euler statement does not, so the
Euler formal statement deserves a separate line-by-line audit of its own definitions before we repeat
the claim anywhere. That audit is not done and is logged in the backlog.

## What this audit does not establish

1. That the Lean project compiles. Not attempted here.
2. That Comparator and the external kernel re-checkers (`lean4export`, `nanoda_bin`) accept the
   solution against the challenge. Not attempted here.
3. That the human-readable manuscripts contain the arguments the Lean files encode. The manuscript is
   165 pages plus three appendices and only the introduction and Section 2 were read.
4. Anything at all about the Alpoge-Buckmaster formalization at
   <https://github.com/tristanbuckmaster/fluid_lean>, which has not been examined.

Item 1 and item 2 are mechanically checkable and are the cheapest real verification available to us.
Preflight estimate before committing machine time: Lean 4.34.0-rc2 plus a Mathlib cache is several GB
of download, and a full build of 641k lines on this hardware is plausibly multi-hour and may be
memory-bound. Under `methodology/12-preflight-and-cost-discipline.md` this needs a declared budget, a
kill criterion, and a smoke test on a single module before the full build, and it must run on `E:`
with output redirected to files rather than through a pipe. It is written up as EXP-001 in
[`../../../program/navier-stokes/backlog.md`](../../../../program/navier-stokes/backlog.md).
