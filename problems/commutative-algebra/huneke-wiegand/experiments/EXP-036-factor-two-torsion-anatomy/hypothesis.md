# EXP-036 hypothesis - factor-two torsion localization and propagation

Status at declaration: **ACTIVE, NO RESULT CLAIMED**.

## Question

Is the `Z/2Z` factor found by EXP-035 an isolated `(p,t)=(4,2)` accident, or does it come from a
compact integral incidence mechanism that persists in larger family cells?

## Declared targets

For `p>=4` and `2<=t<=p-2`, retain

```text
b_(p,t)=10p+t,
F_(p,t)=[3p,4p-2] union {t} union [t+2,p],
i_(p,t)=2p-t-1,
tau_(p,t)=4p^2+6p-t(t-1)/2.
```

Let `Delta_(p,t)` be the complete integral kernel incidence matrix in homological degree `i_(p,t)`
and offset `tau_(p,t)`. Let `M_(p,t)` be the complete EXP-035 block matrix incorporating the
degree-one source boundary of `D_p`, the connecting chain map, and `Delta_(p,t)`.

## Falsifiable predictions

### P1. Finite propagation gate

At least one declared cell with `p=5` has an even Smith factor in `coker(Delta_(p,t))`. Equivalently,

```text
rank_(GF(2))(Delta_(p,t)) < rank_(GF(1000003))(Delta_(p,t))
```

for `t=2` or `t=3`. Exact equality of the ranks in both `p=5` cells refutes P1. The complete screen
also records every allowed cell for `p=4,5,6` reached within budget, but a finite PASS alone does
not prove infinitely many torsion cells.

### P2. Compact torsion core at `p=4`

Unimodular unit cancellation of `Delta_(4,2)` leaves one factor-two block plus the four known free
cokernel generators. The stronger recognition prediction is that the factor-two block can be
supported on six essential low variables and has the integral homology profile of the minimal
triangulation of the real projective plane. A residual factor two on a different essential support
confirms compact algebraic localization but refutes the projective-plane recognition clause.

### P3. Structural propagation

If P1 and the compact-core part of P2 pass, the same signed core is predicted to embed after unit
cancellation in a parameterized subfamily of `Delta_(p,t)`. A valid all-parameter PASS requires an
explicit index map, sign comparison, and proof that every added row and column cancels by integral
units without touching the core. Finite rank agreement cannot establish P3.

For every finite cell, EXP-036 also computes

```text
dim A = rows(Delta) + rank(d_D) - rank(M)
```

over `GF(2)`, `GF(3)`, and `GF(1000003)`. Characteristic dependence in `K_p` need not survive the
connecting quotient, so the `A_p` and `C_p` conclusions are separate recorded outputs.

## Premise dependencies

- EXP-032: complete Betti polynomial of `D_p`.
- EXP-033: exact sequence `0 -> K_p -> A_p -> D_p -> 0`, regular reduction, and minimal cubic cone.
- EXP-034: two-layer integral incidence differential for `K_p`.
- EXP-035: zero-row family, complete `(4,2)` target, block-rank identity, and
  `coker(Delta_(4,2))=Z^4 direct-sum Z/2Z`.

Every run must recheck the frozen hashes listed in the EXP-036 preflight. No literature result is a
premise for the family-specific computation.

## Validation routes

### Canonical route

- enumerate only fixed-cardinality subsets at the exact permitted sums;
- reproduce the EXP-035 `(4,2)` basis hashes and all four field ranks;
- compute every feasible `p=5,6` family cell with exact sparse modular elimination;
- apply exact unimodular unit cancellation and Smith form to every positive even-rank defect.

### Independent route

- reconstruct the two Artinian layers from numerical-semigroup ideal powers, as in EXP-035;
- use a separately written subset-sum enumerator and reversed pivot order;
- compare basis hashes, field ranks, and residual determinant divisors;
- reject wrong-block, removed-zero-row, sign-erased, filled-gap, and odd-prime controls.

### Recognition and symbolic route

- compare the compact residual with the six-vertex real-projective-plane chain profile;
- if a repeated core appears, give its explicit parameter map and prove the interval/sign
  obligations symbolically;
- otherwise preserve the failed recognition and state the actual residual support.

## What PASS and FAIL prove

- **P1 PASS** proves a second exact parameter with even torsion. It refutes isolation at `p=4`, but
  not finite-only behavior.
- **P1 FAIL** proves that the declared `p=5` family cells have no even torsion. It refutes the
  simplest propagation guess, not every larger or off-family cell.
- **P2 compact-core PASS** gives a reproducible small integral torsion certificate.
- **P2 recognition PASS** identifies that certificate with the declared projective-plane model;
  recognition FAIL redirects the topology lens without weakening the Smith result.
- **P3 PASS** proves an infinite torsion subfamily only after the written all-parameter cancellation
  proof and independent reconstruction pass.
- A budget stop is inconclusive and cannot be reported as a mathematical result.

## Invariant-first note

The mod-two versus odd-prime rank defect detects even torsion before Smith computation. Unit
cancellation then localizes it. Ordinary Hilbert numerators, total Betti counts, zero-row counts,
and the selected-coordinate connecting test cannot distinguish a free class from a torsion class.

## Compute budget and kill criterion

- `(4,2)` regression and localization: 120 seconds;
- complete `p=5` screen: 300 seconds;
- `p=6` screen only after the `p=5` checkpoint: 600 seconds;
- integral localization: 300 seconds per positive cell;
- checkpoint after each cell and stop at the first elapsed-budget breach.

No GPU is used. All decisive arithmetic is integral or over explicitly declared prime fields.

## Publication gate

A second exact parameter plus a compact transferable certificate is enough to expand the existing
manuscript. A separate manuscript requires P3 or a comparable all-parameter torsion theorem. A
finite null screen is persisted in the experiment and programme record but does not trigger a
Zenodo version by itself.
