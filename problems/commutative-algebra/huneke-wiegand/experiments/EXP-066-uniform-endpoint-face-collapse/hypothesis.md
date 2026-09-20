# EXP-066 hypothesis: uniform endpoint face collapse

Date: 2026-09-20. Frozen before opening the `p=11` holdout or running any
symbolic parameter sweep.

## Question

Does the support-one formula discovered on the EXP-065 training range give a
direct all-parameter boundary identity, before any unit contraction, and does
that identity agree with the untouched `p=11` frozen carrier?

For `p>=8` and `r in {1,2}`, put

```text
L_p     = [1,p] union [3p,4p-2],
E_{p,r} = (L_p minus {p-r,3p,3p+r}) union {6p,10p},
s_{p,r} = [S,E_{p,r};p-2],
x_{p,r} = x_(0,r,p-2-r).
```

Let `Pi_58` be the semantic row projection of the full original target module
that retains precisely atoms `R1,R3,R4,R5`, using the six atom definitions
frozen by EXP-048.  This definition makes sense before selecting or contracting
a persistent component.

## Falsifiable predictions

### P1: untouched holdout

For `p=11`, independently reconstruct `s_{p,1}` and `s_{p,2}` in the original
presentation and in the frozen labelled component.  In both cases mask 58 must
leave exactly one entry, coefficient `-1` at `x_{p,r}`.  No decoder, HNF, SNF,
or training result artifact may be used.

### P2: uniform original-presentation identity

For every integer `p>=8` and `r in {1,2}`,

```text
Pi_58 d(s_{p,r}) = -x_{p,r}.
```

More strongly, every nonzero face in the complete original boundary has one of
the following types:

1. deleting a surviving first-interval exterior generator produces atom `R0`;
2. deleting a surviving second-interval exterior generator produces atom `R2`;
3. deleting `10p` produces atom `R5`, the row `x_{p,r}`, with sign `-1`;
4. deleting `6p` produces no target basis element.

Thus `Pi_58` kills cases 1 and 2 and retains only case 3.  The proof must derive
all interval inequalities and normalized counts symbolically; a finite sweep is
only a regression check.

### P3: exact controls and scope boundary

An independent implementation must reject each of:

- replacing either omitted point `p-r` or `3p+r` by a neighbouring point;
- replacing `10p` by `10p-1` where admissible;
- changing the source coefficient or requested endpoint row; and
- retaining `R0` or `R2` in the projection.

The producer must test both endpoints for every `p=8,...,300`, with separate
boundary construction and closed-form classification agreeing exactly.  These
finite checks do not replace the all-parameter proof.

## Method

1. Hash and verify the EXP-042, EXP-048 and EXP-065 dependencies.
2. Open the locked `p=11` carrier only after this file is committed and pushed.
3. Construct each original source boundary directly from the defining exterior
   differential and coefficient multiplication.
4. Classify every surviving row semantically, apply `Pi_58`, and compare to the
   formula without importing EXP-065's decoder or output.
5. Independently reconstruct the `p=11` labelled component and compare the
   corresponding frozen column.
6. Emit a deterministic certificate for the holdout, regression sweep, symbolic
   case conditions, and negative controls.

No floating arithmetic, random search, normal-form solver, or post-hoc change to
the formula is permitted.

## Proof obligations

The written proof must explicitly establish:

- `|E_{p,r}|=2p-2`, so deletion of the last exterior entry `10p` has sign
  `(-1)^(2p-3)=-1`;
- the exact low-product thresholds for both low intervals;
- the normalized exterior-count vectors defining `R0`, `R2`, and `R5`;
- why the `6p` face has no degree-two target row; and
- why the `10p` face label is exactly `(0,r,p-2-r)` rather than merely an
  atom of the same type.

Agreement with the finite contracted carrier must be stated separately from the
uniform identity in the full semantic row projection.  The experiment must not
claim a uniform persistent-component reconstruction or a complete cokernel.

## Compute budget and kill criteria

- CPU only, one producer and one independent auditor.
- `p=11` holdout first; at most 120 seconds and 2 GiB per program.
- Regression sweep `p=8,...,300`; at most 120 seconds and 1 GiB per program.
- Checkpoint after the holdout and every 25 sweep parameters.
- Stop on the first mismatch and preserve the counterexample.

## Publication gate

If P1--P3 and the symbolic proof pass, the result is a new uniform constructive
theorem for two endpoint classes in the full mask-58 semantic projection.  It
should be incorporated into the existing integral connecting-map manuscript,
not split into a separate paper.  Zenodo requires a further judgement: update
only if the theorem materially advances the manuscript's stated connecting-map
objective, preferably together with a uniform independence/upper-bound result
for the remaining triangle classes.  A finite pass alone does not qualify.
