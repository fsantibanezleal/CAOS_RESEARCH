# Audit: does the OpenAI Lean certificate state unforced Euler blowup?

Date: 2026-09-12. Closes NS-004. Subject: `ComparatorChallenges/Euler.lean` and
`Euler/Solution.lean` in `openai/NavierStokesAndEuler`, clone at `E:/_Temp/lean-ns`. Method: read the
challenge module and compare it with Theorem 1.1 of the OpenAI Euler manuscript.

Statement level only. No build was run for this audit.

## Correction to the previous audit

[`2026-09-11-lean-statement-audit.md`](2026-09-11-lean-statement-audit.md) said the Euler certificate
"has no external reference statement and therefore needs one more". **That is wrong, and this
supersedes it.** The Euler challenge file carries the same provenance header as the Navier-Stokes one:

> Adapted from `FormalConjectures/Millenium/NavierStokes.lean` at
> <https://github.com/google-deepmind/formal-conjectures/> ... This is the whole-space breakdown
> alternative specialized to zero viscosity and zero external force.

So both certificates inherit their solution class and admissibility conditions from the same
third-party formalization, written by Google DeepMind before the claim existed. The earlier statement
was an inference from the absence of a Clay reference for Euler, and it was not checked against the
file. The provenance argument applies to both certificates equally.

## Why this one matters more than the Navier-Stokes one

The Navier-Stokes result is forced, which is the weaker of Fefferman's alternatives. The Euler result
is **unforced**, and finite-time blowup for unforced 3D Euler from smooth compactly supported
finite-energy data is the question that Elgindi, Elgindi-Ghoul-Masmoudi,
Cordoba-Martinez-Zoroa-Zheng, Elgindi-Pasqualotto, Chen-Shkoller and Chen-Hou have each reached only
in a restricted regularity class or a restricted geometry. If correct, this is the larger
mathematical event, and it is not a Millennium problem so it has attracted less scrutiny.

## The two declarations

### `euler_breakdown_R3`

```lean
theorem euler_breakdown_R3 :
    ∃ u₀ : ℝ³ → ℝ³, InitialVelocityConditionDecay u₀ ∧
      ¬ (∃ v p, EulerExistenceAndSmoothnessR3 u₀ v p)
```

with the solution class requiring, at every `t ≥ 0`:

| clause | encoding | note |
|---|---|---|
| the equation | `derivWithin (v x ·) (Ici 0) t + fderiv ℝ (v · t) x (v x t) = -gradient (p · t) x` | **unforced and inviscid**: the right-hand side is exactly `-grad p`, with no `f` and no `nu Δv` |
| incompressibility | `∀ x, ∀ t ≥ 0, ∇⬝ (v · t) x = 0` | faithful |
| initial datum | `∀ x, v x 0 = u₀ x` | faithful |
| smoothness | `ContDiffOn ℝ ∞ (uncurry v)` and same for `p`, on `univ ×ˢ Ici 0` | classical, not weak |
| finite energy | `MemLp (‖v · t‖) 2` | faithful |
| uniformly bounded energy | `∃ E, ∀ t ≥ 0, (∫ x, ‖v x t‖ ^ 2) < E` | faithful |
| admissible data | smooth, divergence free, all derivatives decaying faster than any polynomial | Fefferman's condition (4) |

The absence of a force is the whole point and it is visible in one line: the momentum equation has
`-gradient (p · t) x` on the right and nothing else.

### `exists_compact_smooth_euler_singularity`

This is the quantitative version and it is the one worth reading closely, because it is where a
blowup claim usually gets soft. It asserts the existence of `u₀`, `Tstar`, `v`, `p` with all of:

1. `InitialVelocityConditionDecay u₀ ∧ HasCompactSupport u₀ ∧ u₀ ≠ 0`. The nonzero clause blocks the
   trivial solution; compact support matches the manuscript and is stronger than the decay the
   breakdown statement needs.
2. `0 < Tstar ∧ Tstar ≤ 1`.
3. A solution on `Ico 0 Tstar` in an all-order Sobolev class: spatially `C^∞` at each time, with every
   derivative tensor in `L²` and continuous in time in `L²`, and the Euler equation holding at
   interior times against a strong `L²`-valued time derivative.
4. Uniformly bounded energy on `[0, Tstar)`.
5. **Maximality**: `∀ T > 0, ((∃ w q, solution on Icc 0 T) ↔ T < Tstar)`. This is the clause that
   makes the theorem a blowup theorem rather than a statement about some arbitrary time. `Tstar` is
   pinned as the exact lifespan in both directions.
6. **No earlier singularity**: on every `Icc 0 T` with `T < Tstar`, the `C¹` norm is finite and the
   vorticity time-integral is finite. So the breakdown is located at the endpoint and not smuggled in
   from a solution that was already singular.
7. `limsup` of the `C¹` norm as `t → Tstar⁻` is `⊤`, and `∫ vorticityNorm` over `Ico 0 Tstar` is `⊤`.
   Both of the standard criteria, including the Beale-Kato-Majda integral.
8. The global breakdown conclusion of the first theorem, for the same datum.

Definition checks done by hand: `vorticity` uses cyclic indices,
`(curl v)_i = ∂_{i+1} v_{i+2} - ∂_{i+2} v_{i+1}`, which for `i = 0` is `∂_1 v_2 - ∂_2 v_1`, the correct
first component. `velocityC1Norm` is `sup ‖v‖ + sup ‖Dv‖` valued in `ℝ≥0∞`, so an unbounded field has
norm `⊤` rather than silently failing to be defined. Suprema in `ℝ≥0∞` are the right choice here: they
make "unbounded" a value rather than an error.

## Verdict

**The Euler certificate states unforced finite-time blowup for 3D incompressible Euler from nonzero,
smooth, compactly supported, rapidly decaying, divergence-free initial data, with maximal lifespan
pinned in both directions, no earlier singularity, and both standard blowup criteria diverging at the
endpoint.** I found no weakened hypothesis, no strengthened conclusion, and no gap through which a
trivial witness could pass. Together with the Navier-Stokes audit, both certificates are faithful at
the statement level and both inherit their admissibility conditions from a third party.

Solution-class note, stated rather than hidden: the equation is imposed at interior times with an
`L²`-valued strong time derivative, which is the standard formulation for this class and not a
relaxation that would make non-existence easier. The all-order Sobolev continuity requirement is if
anything more demanding than a classical statement.

## What remains unchecked

The same three items as before, none of them touched by this audit: that the project compiles, that
Comparator and the external kernel re-checkers accept the solution modules against these challenge
modules, and that the 56-page manuscript contains the arguments the Lean files encode. The build is
EXP-001 and is the only one of the three that is mechanically available to us.
