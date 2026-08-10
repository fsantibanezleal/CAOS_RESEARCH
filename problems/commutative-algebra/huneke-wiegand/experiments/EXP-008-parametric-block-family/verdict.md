# EXP-008 verdict - fixed-width interval family REFUTED

Run date: 2026-08-10. Exact arithmetic, CPU only.

## Result

The proposed formula is not an infinite family. The declared `q=5` boundary control is rejected,
the three parameters `q=6,7,8` are exact rigid instances, and the first out-of-sample value `q=9`
fails rigidity:

```text
q = 9
s = 38
first element of D absent from E+E = 349 = 9s+7.
```

The run stopped at this first predicted-parameter failure, as required. The deterministic artifact
aggregate is recorded in `artifacts/results.json`.

## Symbolic obstruction

Write the proposal's level-4 set as

```text
A = [0,q-2] union [2q+1,2q+4].
```

At level 9, `E+E` can only come from a carried sum of two level-4 residues or a non-carried sum of
a level-4 and a level-5 residue. Direct interval addition gives

```text
carry(A+A) = [0,6],
low(A+B)   = [q-1,s-1].
```

The target `D` contains the entire level-9 block. These two intervals meet exactly when `q<=8`.
For every `q>=9`, residue 7 is absent, so `9s+7` lies in `D` but not in `E+E`. Thus the proposed
formula fails for every `q>=9`, not only at the computed witness.

## Predictions

- P1 FAIL at `q=9`; the sweep stopped there.
- P2 FAIL at `q=9` with the exact witness `9s+7`.
- P3 is immaterial to a failed counterexample family; no positive-family claim is made.
- P4 PASS: `q=5` is rejected and has `A intersect B = {14}`.
- P5 FAIL for the proposed formula; the symbolic interval analysis instead proves its obstruction.
- P6 PASS: source values `q=7,8` regenerate exactly and the boundary corruption is rejected.

Verdict: **REFUTED**.

## Consequence

The second interval in `A` cannot keep constant width four. A valid family must let the carried
`A+A` interval grow with the first level-4 interval so that it meets the `A+B` coverage. Any
replacement formula belongs to a newly declared experiment.

## How could this be wrong?

The refutation concerns exactly the EXP-008 formula. It does not negate the eleven Route K models
or the existence of another interval family. The dictionary from block sums to `D=E+E` is also
checked by the full exact rigidity routine at every evaluated parameter; an error would therefore
have to affect both the elementary interval calculation and the independently reused finite
checker.
