# EXP-132 - Transverse (2,8) Fitting-atlas lift

Declared 2026-08-01 before any verdict-bearing run.

## Question

After adding the smallest unused linear transverse direction `(2,8)` to the
closed normalized four-coefficient restriction, what is the joint exceptional
ideal of several accepted maximal-minor sections on the direct `A=0` boundary?
In particular, can an exact finite atlas close

\[
M_0(B,C,T)=M_{\rm forced}+B M_{(0,5)}+C M_{(2,9)}+T M_{(2,8)}
\]

over `QQ[B,C,T]`, or does the lift expose a smaller residual scheme that must
be recursed on?

## Motivation and alternative view

EXP-131 closes the `T=0` plane with two exact maximal minors whose squarefree
divisors satisfy a Bezout identity. EXP-122 identifies `(2,8)` as the smallest
unused linear candidate: its accepted anchor factor is `(3*T+68)/68`, its
selected direction matrix has rank 62, and its union with the `T_B` chart has
largest strongly connected component 35.

The matrix is also a presentation of a parameter-dependent cokernel module.
Its maximal-minor ideal is the zeroth Fitting ideal of that cokernel. Thus an
exact unit-ideal certificate is equivalently a zero-right-prime certificate
for the full-column-rank polynomial matrix, and implies a polynomial left
inverse/unimodular completion. This module/Fitting formulation is the primary
view; individual determinant charts are only generators sampled from that
ideal.

Lu--Ruan--Wang--Xiao, arXiv:2605.09286v1 (2026), gives recent Smith-form
criteria for structured multivariate polynomial matrices and extends them to
rectangular/rank-deficient cases. Its triangular highest-determinantal-divisor
hypothesis has not been proved for this family, so the paper motivates the
invariant-factor audit but is not used as a theorem about `M_0`.

## Premise dependencies

1. [MV] EXP-111 proves that the constant `Q` column is structurally zero and
   makes rank 125 of the reduced augmented matrix the inconsistency target.
2. [MV] EXP-112 reconstructs the complete 302-row, 125-column augmented
   system exactly.
3. [MV] EXP-118 and EXP-123/129/130/131 close the declared four-coefficient
   restriction on `d=0`, `A!=0,d=1`, and `A=0,d=1` respectively.
4. [MV] EXP-131 supplies two exact row bases and a unit Bezout identity at
   `T=0`; both are regression gates, not evidence away from `T=0`.
5. [MV] EXP-122 supplies the exact `(2,8)` anchor activity record quoted
   above.
6. [H] A small collection of inherited and residual-selected row bases is
   sufficient to expose the first transverse Fitting residual. This is the
   experimental premise being tested; failure does not imply matrix rank
   failure.

## Falsifiable predictions

1. Every accepted section reproduces its persisted `T=0` determinant or
   direct-rank control exactly.
2. The two EXP-131 sections have stable generic degree at most eight in `T`
   at both declared reconnaissance primes.
3. At least three distinct inherited sections are nonzero after the lift, and
   their squarefree modular gcd has degree zero at generic `(B,C)` fibres at
   both primes.
4. Exact reconstruction of the affordable sections either generates the
   unit ideal in `QQ[B,C,T]` or reduces the common locus to a proper residual
   scheme of dimension at most one. A positive-dimensional residual of
   dimension two or more refutes this prediction and redirects the campaign
   to a direct Fitting presentation/invariant-factor compression.

## Method

1. Hash-check the accepted EXP-112, EXP-122, EXP-123, EXP-124, and EXP-131
   inputs and rebuild the complete augmented matrix from the bracket
   equations. Specialize `A=0,d=1` before any normalization.
2. Load and deduplicate the EXP-131 primary and alternative bases, the
   EXP-123 shared basis, and the EXP-124 graph-alternative basis.
3. Reproduce the EXP-131 determinants at `T=0` and direct-rank controls for
   the other bases.
4. At two good primes, interpolate the degree in `T` on several generic
   `(B,C)` fibres, record squarefree gcds across the section suite, and search
   for residual-selected bases only where all inherited sections vanish.
5. Reconstruct every section that stays within the exact degree/support gate.
   Compute the joint ideal by staged resultants/Groebner bases, splitting all
   leading coefficients, denominators, and coordinate boundaries explicitly.
6. If direct multivariate reconstruction exceeds the gate, retain the modular
   atlas only as reconnaissance and launch no proof claim. The next experiment
   will use fraction-free polynomial-matrix reduction over one coefficient
   field with a complete denominator-fibre ledger.

## One-sidedness and interpretation gate

A **PASS** requires exact characteristic-zero generators and a verified
unit-ideal identity. It closes only the `A=0,d=1` boundary of the five-
coefficient restriction
`{(0,1),(0,5),(1,0),(2,9),(2,8)}`. Together with a future exact `A!=0`
lift and the already-closed `d=0` regression boundary, it could contribute to
closing that five-coefficient restriction. It does not settle the 24-parameter
core, the 51-parameter family, `(72,108)`, the planar degree floor, or JC(2).

A **FAIL** from an exact common residual proves only that the tested section
suite does not cover that residual. Even an exact augmented-rank defect would
not by itself construct a Keller pair or disprove JC(2); the upstream
necessity bridge would still control interpretation. A modular common zero,
degree-gate stop, or timeout is inconclusive.

## Invariant-first note

The first invariant is the EXP-131 Bezout identity after specialization
`T=0`; any mismatch invalidates the run before interpolation. The second is
the gcd/determinantal divisor of the inherited sections. A nonconstant common
divisor immediately identifies a codimension-one recursion target without a
Groebner computation. Smith/Popov invariant factors are deferred unless the
direct section gcd leaves a positive-dimensional locus, because their
fraction-field denominators would require a separate exceptional-fibre
ledger.

## Compute budget and kill criterion

- CPU only; exact rational and finite-field arithmetic; no randomness.
- Smoke stage: under 60 seconds, with flushed progress and a JSON checkpoint.
- Modular atlas: target under 5 minutes, hard gate 8 minutes.
- Any individual exact determinant worker: hard gate 5 minutes.
- Total accepted run: hard gate 20 minutes.
- Checkpoint after matrix construction, after each section/prime, and after
  each exact generator.
- On any gate, stop the worker, preserve completed records and hashes, and
  report `INCONCLUSIVE AT DECLARED GATE`; no mathematical closure follows.

## Adversarial controls

- Two independently chosen good primes and exact direct substitutions.
- Exact `T=0` reproduction of both EXP-131 determinant formulas and their
  Bezout identity.
- Deduplicate row bases before counting charts.
- Verify every claimed ideal identity by substitution/expansion over `QQ`.
- Treat modular ranks and modular unit ideals as target selection only.
- Recompute at least one accepted determinant from the original 302-row
  matrix rather than from a normalized or cached surrogate.
