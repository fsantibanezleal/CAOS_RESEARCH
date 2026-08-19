# EXP-008 verdict - proposed interval family refuted

Run date: 2026-08-10. Verdict: REFUTED.

## Result

The declared interval formula is not an infinite family. It produces exact rigid Route K
instances at precisely the three tested parameters

```text
q = 6, 7, 8,
s = 26, 30, 34,
```

but fails at `q=9`, `s=38`. The first missing rigidity value is

```text
D = 349 = 9s+7.
```

The exact finite run stopped at the first predicted-range failure, as declared. The `q=7` and
`q=8` membership hashes reproduce the corresponding EXP-006 models exactly. At `q=6`, the formula
supplies a different valid model at the already SAT parameter `s=26`.

The `q=5` boundary control is also rejected as predicted because residue 14 belongs to both `A`
and `B`. This makes `4s+14` a member of `D` below the minimum possible value `8s` of `E+E`.

## All-parameter obstruction for q>=9

The finite failure extends to a symbolic refutation of the declared formula for every `q>=9`.
Set `s=4q+2`.

The formula contains the entire high block `[9s,13s-2]`. Therefore

```text
9s+7, 10s+7, 11s+7 are all in Gamma,
```

so `9s+7` belongs to `D`.

Below block 9, the only possible decompositions of an `E+E` value in block 9 are:

1. two level-4 elements, with a carry by `s`; or
2. one level-4 and one level-5 element, without a carry.

For the proposed

```text
A = [0,q-2] union [2q+1,2q+4],
B = [q-1,q+1] union [q+3,2q] union {3q-1} union [3q+3,4q+1],
```

the only sum in `A+A` that reaches `s` comes from the second interval with itself. Its carried
residues are exactly `[0,6]`. Meanwhile the smallest value in `A+B` is `q-1`, which is at least 8
when `q>=9`. Hence residue 7 belongs to neither carried `A+A` nor `A+B`. Thus

```text
9s+7 is in D but not in E+E
```

for every `q>=9`. This proves non-rigidity uniformly and explains the first exact witness at
`q=9`.

## Predictions

- P1 REFUTED: the formula does not pass through `q=100`; its first predicted-range failure is
  `q=9`.
- P2 REFUTED as a universal statement: exact rigidity holds at `q=6,7,8` and fails for all
  `q>=9`.
- P3 PASS for the valid instances and, deductively, for the proposed parameter pattern: membership
  of `m+1` forces generalized-arithmetic parameters `h=1,d=1`, while membership of `m+2q+1`
  would force the actual gap `m+q-1`.
- P4 PASS: `q=5` is rejected by the declared overlap.
- P5 resolves by refutation: the interval-layer proof above proves failure for all `q>=9`, so no
  finite extrapolation is used.
- P6 PASS: `q=7,8` reproduce their source models, and malformed reflected blocks are rejected by
  the semantic checker and unit tests.

## Consequence and redirection

Visual recurrence of a few density-optimal SAT models is not a reliable family extractor. The
load-bearing object is the four-layer additive cover:

```text
D_8  is covered by low A+A,
D_9  is covered by carried A+A and low A+B,
D_10 is covered by carried A+B and low B+B,
D_11 is covered by carried B+B,
D_12 is covered by low A+C.
```

The failed formula leaves a widening hole between the fixed carried interval `[0,6]` and the
moving start `q-1` in layer 9. Any next construction must make these cover endpoints meet for all
parameters while preserving the closure identity between `A+A` and the symmetry complement `C`.
This cover system, rather than a fixed list of offsets, is the strongest next search space.

## Adversarial record

- Independent generation from the lower blocks agrees with the explicit formula through the
  conductor in every executed case, so the failure is not caused by an inconsistent high-block
  transcription.
- Symmetry and closure pass at `q=9`; rigidity alone fails at the predicted value.
- The standard full-window/tail checker reports no reverse-containment failure.
- The residual risk is in the broader family search, not this refutation: other choices of `A`
  and `B` can and do yield valid `s=38` models, as EXP-006 proves.

## Reproduction

From the repository root:

```powershell
.\.venv\Scripts\python.exe `
  problems\commutative-algebra\huneke-wiegand\experiments\EXP-008-parametric-block-family\run.py `
  --min-q 5 --max-q 100 `
  --artifact-dir problems\commutative-algebra\huneke-wiegand\experiments\EXP-008-parametric-block-family\artifacts
```

The expected process exit code is 2 because the declared family is refuted. Compact artifact
aggregate SHA-256: `055b027dc2b04206ce9ecd502dd2eeb27519b051bf0159f8cddc90019af86faa`.
