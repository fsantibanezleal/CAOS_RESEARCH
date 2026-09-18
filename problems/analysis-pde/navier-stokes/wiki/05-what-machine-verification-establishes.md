# 5. What machine verification does and does not establish

Both September 2026 claims shipped with Lean 4 formalizations. This page records what that buys, what
it does not, and what we checked ourselves. Full audits:
[Navier-Stokes (C) and (D)](../context/2026-09-11-lean-statement-audit.md) and
[unforced Euler](../context/2026-09-12-euler-statement-audit.md).

## The distinction that does the work

A machine-checked proof answers **"does this argument follow"**. It never answers **"is this the
theorem"**. The standard way a formalized claim is hollow is a faithful-looking definition that
quietly weakens a hypothesis or strengthens a conclusion, and the kernel cannot see it: the proof of a
weaker statement is just as valid as the proof of a stronger one.

So the first question about a 641,332-line certificate is not whether it compiles. It is what it says,
and **who wrote what it says**.

## What the OpenAI repository actually contains

Measured on the clone at last push 2026-09-10:

| measurement | value |
|---|---|
| Lean files | 2,659 |
| Lean lines | 641,332 |
| `sorry` outside `ComparatorChallenges/` | 0 |
| `sorry` inside `ComparatorChallenges/` | 5, the reference stubs, by design |
| `axiom` declarations added by the project | 0 |
| permitted axioms | `propext`, `Quot.sound`, `Classical.choice` |
| `formalization.yaml` review status | `self-assessed` |

The five `sorry`s are correct design, not a gap. `ComparatorChallenges/` holds the *reference
statements* with `sorry` proofs; Comparator checks that the separately proved declarations have the
same type, with `lean4export` and `nanoda_bin` re-checking outside the Lean kernel.

## The strongest single fact: provenance of the statement

Both challenge files are **adapted from Google DeepMind's Formal Conjectures**, specifically
`FormalConjectures/Millenium/NavierStokes.lean`, credited in `formalization.yaml`
(`relationship: builds-on`) and in `ComparatorChallenges/README.md`. The Euler file carries the same
header, specialized to zero viscosity and zero force.

So the definitions that decide whether the theorem is the right theorem were written **by a third
party with no stake in the claim, before the claim existed**. That removes the most common way a
formalized result can be hollow, and it is a practice worth copying in our own work.

> Our first audit asserted that the Euler certificate had no such third-party reference. That was
> inferred from the absence of a Clay statement for Euler and was not checked against the file. It is
> corrected in place in the 2026-09-11 dossier.

## What we verified by hand

**Navier-Stokes (C) and (D).** Every clause of Fefferman's statement compared with its Lean encoding:
viscosity positivity, dimension, smoothness and divergence-freeness of the datum, the rapid-decay
conditions (4) and (5), the momentum equation, incompressibility, the initial condition, joint
smoothness (6), square integrability and uniformly bounded energy (7), and the non-existence
conclusion. All faithful. The decay conditions are indexed by derivative order rather than multi-index,
which is equivalent up to constants. The momentum equation is pointwise and classical, so the
non-existence conclusion is *harder* than a distributional one, not easier.

**Unforced Euler.** The momentum equation has only $-\nabla p$ on the right: no force, no viscosity.
The quantitative theorem is carefully guarded in four ways that a soft blowup claim would not be:

1. **Maximality in both directions**: a closed-interval solution exists **if and only if** $T<T_*$, so
   $T_*$ is pinned as the exact lifespan.
2. **No earlier singularity**: on every earlier closed interval the $C^1$ norm is finite and the
   vorticity time-integral is finite, locating the breakdown at the endpoint.
3. **Nonzero, compactly supported data**, which blocks the trivial witness.
4. **Both standard criteria diverge**: the $C^1$ limsup and the Beale-Kato-Majda vorticity integral.

Definitions hand-checked: the cyclic vorticity indices give the correct first component
$\partial_1v_2-\partial_2v_1$, and the $C^1$ norm is valued in the extended reals so that "unbounded"
is a value rather than an undefined expression.

**Statement-level verdict on both: faithful.** No weakened hypothesis, no strengthened conclusion, no
smuggled assumption. Where the claims differ from the minimum required, they differ in the authors'
favour: a compactly supported force where (5) asks only for rapid decay.

## What a faithful statement still does not give you

1. **That the project compiles.** This is [EXP-001](../experiments/EXP-001-lean-replay/verdict.md), and
   it is the one mechanically available check. **It is now done for the whole certificate.** The
   Navier-Stokes development built cleanly three times, and on 2026-09-13 the full project built too:
   **11,424 jobs, zero `sorryAx`, zero errors**, with all four headline theorems, Fefferman (C) and
   (D) and both unforced-Euler theorems, depending on exactly `propext`, `Classical.choice`,
   `Quot.sound`. The Euler half took a two-part local cache repair (overwriting oleans an external
   disk event had corrupted, then an incremental build loop to ride out Windows read-contention); the
   artifact was never at fault, every failure being a file-read error, never a mathematical one.
2. **That Comparator and the external re-checkers accept the solution modules.** `lake build`
   type-checks the proofs; running `Comparator` with `lean4export` and `nanoda_bin` to re-check the
   solution against the challenge outside the Lean kernel is a further step, not yet attempted.
3. **That the human-readable manuscripts contain the arguments the Lean encodes.** The Navier-Stokes
   paper is 165 pages plus three appendices; only the introduction and the physical description were
   read here.
4. **That the community accepts the result.** At the time of writing nobody had, and the Clay
   Mathematics Institute had not commented. OpenAI stated it does not intend to claim the prize.

A compiling certificate settles item 1: the proof has no gaps under the kernel. Items 3 and 4 are the
ones that decide whether this is accepted mathematics, and neither is settled by a certificate.

## The honest summary, for any surface we publish

The statements are faithful and the certificates are well engineered, with third-party reference
statements and external kernel re-checking. We independently rebuilt the entire certificate from a
clean checkout, Navier-Stokes and Euler both, and it type-checks with no gaps and only the standard
axioms. Nobody has yet confirmed that the human-readable arguments
support the statements, and the community has not weighed in. A compiling certificate is real evidence
that the proof has no logical gaps; it is not the same as the result being accepted.

## Lessons we are taking into our own work

- **Inherit your statement.** Where a third-party formalization of a problem exists, formalize against
  it rather than writing your own admissibility conditions.
- **Publish the axiom set and the `sorry` count** as machine-readable metadata, the way
  `formalization.yaml` does.
- **A green gate is not evidence of what it claims.** This problem produced three instances inside
  three days: a negative control evaluated where it could not discriminate, a log-slope fit in a region
  where the amplitude crosses zero, and a horizon too short to see the effect it was testing for. Each
  passed silently until it was checked against something independent.
