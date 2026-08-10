# EXP-009 - growing interval counterexample family

Declared 2026-08-10 before implementation, the formal parameter sweep, or the symbolic proof.
Phase HW-P4, Route A. EXP-008 is refuted because its carried level-4 sum interval has fixed width;
this experiment makes that width grow.

Pre-run erratum, 2026-08-10: P3 originally said embedding dimension `11p-1`. Before implementation
or any EXP-009 run, direct cardinality bookkeeping gave `|A|=2p`, `|B|=3p`, and a level-5 block
of size `6p`, hence the correct predicted embedding dimension is `11p`. The construction and every
other prediction are unchanged.

## Question and construction

For every integer `p>=4`, set

```text
s = 6p,
F = 13s-1,
m = 4s,
A = [0,p] union [3p,4p-2],
B = ([p+1,3p-1] minus {2p-1}) union {4p} union [5p-1,6p-1],
C = [0,s-1] minus (s-1-A).
```

Define `Gamma_p` by the membership blocks

```text
{0}, 4s+A, [5s,6s-1], 6s+B, 8s+C, [9s,13s-2], [13s,infinity),
```

with every unlisted nonnegative value below `13s` a gap. Let

```text
R_p = k[t^Gamma_p] localized at its positive-degree maximal ideal,
I_p = (t^(4s),t^(5s))R_p,
```

whose normalized shift is `s`.

## Pre-compute derivation

The symmetry complement is predicted to be

```text
C = [0,2p] union [3p,5p-2].
```

Writing `low(X+Y)` and `carry(X+Y)` for residues of sums below and above `s`, the proposed interval
sets should satisfy

```text
low(A+A)   = C,
carry(A+A) = [0,2p-4],
low(A+B)   = [p+1,6p-1],
carry(A+B) = [0,4p-3],
low(B+B)   = [2p+2,6p-2],
carry(B+B) = [0,6p-2],
low(A+C)   = [0,6p-2].
```

The only threshold-sensitive join is the level-9 coverage

```text
[0,2p-4] union [p+1,6p-1] = [0,6p-1],
```

which holds exactly when `p>=4`. This is the invariant-first reason for the declared threshold.

## Predictions

- P1: `p=2,3` fail rigidity, while every `p=4,...,300` passes exact closure, symmetry and
  full-window/tail rigidity checks.
- P2: the seven displayed residue-sum identities hold exactly throughout the sweep and reduce to
  affine endpoint inequalities valid for every integer `p>=4`.
- P3: the displayed lower membership blocks generate exactly `Gamma_p`, with multiplicity `4s`,
  Frobenius `13s-1`, conductor `13s`, and embedding dimension `11p`.
- P4: `I_p` is nonprincipal because `s` is a gap and rigid because `D=E+E`; hence the construction
  gives infinitely many counterexamples in the two-generated monomial-ideal class.
- P5: every `Gamma_p` is outside the generalized-arithmetic-sequence positive family: membership
  of `4s+1` forces unit step, while the later member `4s+3p` would force the actual gap `4s+p+1`.
- P6: the exact `p=4` and `p=5` masks reproduce Route K instances at `s=24` and `s=30`; clearing
  a forced endpoint and changing the omitted selector residue are both rejected.

## One-sidedness and proof gate

- A failed instance refutes the formula and stops the experiment.
- A finite sweep alone proves only its evaluated instances.
- The infinite-family theorem requires a readable interval proof that the block set is a numerical
  semigroup, is symmetric, and has `D=E+E` at every low layer and throughout the conductor tail.
- The conclusion stays inside numerical semigroup rings and two-generated monomial ideals. It does
  not classify arbitrary modules or rings. Son Pham retains priority for the first public
  counterexample; this proposed family is a CAOS extension.

## Premises and adversarial validation

- EXP-001 through EXP-003 support the semigroup/colon dictionary and exact finite checker.
- EXP-006 supplies eleven non-seed models and the independently audited Route K machinery.
- EXP-008 supplies the exact level-9 obstruction that motivates the growing width.
- Independently compare direct block membership with generation from the proposed minimal
  generators through the conductor.
- Verify the seven sumset identities both by explicit finite sets and by affine interval endpoints.
- Retain the `p=2,3` negative witnesses and two corrupted positive controls.

## Budget and stop rules

- Exact sweep `p=2,...,300`: under two minutes, CPU only.
- Symbolic endpoint verification: under thirty minutes, exact integers only.
- Stop at the first failure for `p>=4`; do not alter the formula inside EXP-009.
- A theorem result triggers the manuscript and Zenodo new-version gate only after an independent
  reconstruction audit and a narrative claim audit.

## Exploration moment

The failed EXP-008 family revealed that level-9 coverage, not symmetry or closure, controls the
width. Reading that obstruction backwards constructs the growing interval: `carry(A+A)` must reach
the first residue supplied by `low(A+B)`. This turns a failed extrapolation into an explicit affine
design rule.
