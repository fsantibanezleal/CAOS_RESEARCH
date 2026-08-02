# EXP-006 Route G verdict - fixed-offset family REFUTED

Run date: 2026-08-02. EXP-006 remains open for Route K.

## Result

The exact fixed-offset lift of the public `s=14` generator blocks is not a family. Among all even
`s=14,16,...,100`, only the seed `s=14` passes the predicted Frobenius, symmetry, exact minimal
generator and rigidity checks.

The first failure is `s=16`:

```text
actual F = 205
predicted F = 13s-1 = 207
```

For `s=16,18,...,26`, the observed Frobenius is `12s+13`, not `13s-1`. At `s=28` the predicted
Frobenius value returns (`F=363`) but symmetry fails first at 14. For every tested even `s>=30`,
symmetry already fails at 1.

## Predictions

- P1 PASS: `s=14` reconstructs exactly the 26 public minimal generators, `F=181`, symmetry and
  rigidity.
- P2 PASS by the falsification branch: the naïve template fails before 28 with an explicit first
  invariant witness.
- P6 PASS for Route G: deterministic order, checkpoint, membership hashes and first-failure
  witnesses are committed.
- P3-P5 remain open and belong to the constrained-block and algebraic routes.

## Redirection

Do not extrapolate fixed residue offsets from the public seed. Route K must allow the level-4 and
level-6 residue sets to vary with `s` while retaining `m=4s` and testing whether `F=13s-1` is itself
structural. Any recurrent SAT instances still require the three-non-seed and symbolic-proof gate
before an infinite-family claim.
