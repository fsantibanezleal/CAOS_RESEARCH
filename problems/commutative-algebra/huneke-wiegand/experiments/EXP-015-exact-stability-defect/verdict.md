# EXP-015 verdict - square-tail prediction REFUTED at smoke gate

Run date: 2026-08-12. Exact integer and bitset arithmetic, CPU only.

## Result

The first `p=4` smoke run refuted the declared formula

```text
v(T_p^2)=(8s+C_p) union [9s,infinity)
```

at the value `13s-1=311`. This value is the Frobenius gap inherited from `R_p`; it does not lie in
`T_p^2`. No campaign artifact was written and no parameter beyond the first smoke instance was
used to alter the prediction.

Verdict: **REFUTED**.

## What survives

The proposed stability-defect set did not contain `13s-1`, so the smoke failure does not refute
the exact defect blocks or their predicted length `14p`. It refutes only the overbroad square tail.
The corrected square candidate is

```text
v(T_p^2)=(8s+C_p) union [9s,13s-2] union [13s,infinity).
```

Methodology requires a new experiment for that corrected statement. EXP-016 must be declared
before its smoke run and must retain the `13s-1` exclusion explicitly.

## Consequence

EXP-015 stops before a campaign. Its run code and smoke failure are retained as the exact
refutation record. No manuscript, wiki, or programme claim may cite EXP-015 as positive evidence.

## How could this be wrong?

The failure could only be an implementation error if the exact value-set multiplication omitted a
valid decomposition of `13s-1`. But both summands would be at least `4s`; direct inspection of the
EXP-013 blocks gives no such decomposition, and `13s-1` is absent from the prior EXP-014 square
artifact at `p=4`. EXP-016 will independently retain this exclusion as an adversarial gate.
