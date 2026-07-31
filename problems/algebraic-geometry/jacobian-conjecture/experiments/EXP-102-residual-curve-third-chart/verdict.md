# EXP-102: Third chart exists at one curve point; pullback is inconclusive

## Verdict

**INCONCLUSIVE** for complete residual-curve coverage.

The declared five-minute exact symbolic run reached its kill criterion before
factoring the third minor on the normalized curve. The process was terminated
at the budget. No nonvanishing or finite-residual claim is inferred from the
timeout.

The refactored preflight did produce an exact, decision-bearing partial result.

## Confirmed partial result

At the residual-curve point

\[
u=1,\qquad (s,t)=(8,9),
\]

the two EXP-101 minors both vanish exactly.

Modular rank over the prime \(2147483629\) gives lower bounds

\[
\operatorname{rank}M\ge124,\qquad
\operatorname{rank}[M\mid b]\ge125.
\]

The constant-\(Q\) column gives
\(\operatorname{rank}M\le124\), and adjoining one right-hand-side column gives
\(\operatorname{rank}[M\mid b]\le125\). Therefore the rational ranks are
exactly

\[
\operatorname{rank}_{\mathbb Q}M=124,\qquad
\operatorname{rank}_{\mathbb Q}[M\mid b]=125.
\]

The fiber remains inconsistent. Modular pivoting selected a third 125 by 125
augmented minor containing the right-hand-side column. Its exact rational
determinant at \((8,9)\) is nonzero.

The persisted checkpoint records the rows, columns, determinant, and rank
probes. The two parameter-direction matrices of this third minor have combined
rank \(121\) modulo \(2147483629\). This explains why the generic dense
bivariate determinant reduction is a poor next backend.

## Failed and repaired execution

1. The first run was stopped at 304 seconds by the declared five-minute limit.
2. A diagnostic preflight initially repeated expensive exact zero determinants
   and rational ranks. That staging was retired.
3. The repaired preflight evaluates the already-proved EXP-101 polynomials,
   uses modular lower bounds plus structural upper bounds for exact ranks, and
   selects the third minor by modular pivots.
4. The repaired preflight completes in about two seconds and writes
   `artifacts/checkpoint.json`.

## Route decision

Do not retry a dense 121-rank bivariate determinant.

On the normalized curve, clear the Laurent denominator:

\[
s=8u^7,\qquad t=8u^2+u^{-7}.
\]

For the full augmented polynomial matrix \(A(u)\), multiply rows by a sufficient
power of \(u\) and compute the determinantal divisor of the 125-minors over the
PID \(\mathbb Q[u]\), or first over several finite fields with exact rational
reconstruction. A monomial determinantal divisor would prove rank 125 for every
\(u\ne0\). A nonmonomial divisor gives the exact finite residual values.

This Smith/determinantal-divisor formulation uses all minors simultaneously and
is better typed than expanding one dense third minor.

## Scope

- EXP-102 proves a third chart exists at \(u=1\).
- It does not prove that the third chart covers the whole residual curve.
- EXP-101's first transition and exact residual curve remain fully valid.
- The two-parameter slice, the full \((72,108)\) case, and \(JC(2)\) remain
  open.

## How could this be wrong?

- Modular rank can drop relative to characteristic zero, not rise. Here the
  modular lower bounds meet independent structural upper bounds, so the
  rational ranks are forced exactly.
- The selected third minor is point-local. It may vanish elsewhere on the
  curve.
- A polynomial-matrix Smith calculation must control primes and rational
  reconstruction before yielding a characteristic-zero conclusion.
