# EXP-063 verdict

Status: **CONFIRMED FINITELY** for `p=8,9,10,11`; P1--P3 pass in their declared
operational mod-two scope.

All 19 exact EXP-062 triangle rows survive the certified unit contraction,
occur uniquely in the persistent component, and are semantic `R5` rows. The
contraction carries each one to the literal same target coordinate. In both
full carrier masks 59 and 62, their mod-two quotient rank is the full sequence
`3,4,5,7`; no triangle relation occurs.

Mask 58 has ranks `1,2,3,5`. Its complete triangle relation space is uniformly
spanned, throughout the tested range, by the two endpoint triangles

```text
(0,1,p-3),  (0,2,p-4).
```

Mask 56 has ranks `0,0,0,1`, with `(2,3,4)` the sole surviving direction at
`p=11`. These ranks exactly reproduce the independent carrier Bockstein
certificates. A separate audit rebuilds all four labelled components, checks
all 19 persisted `+/-2x_T` boundaries, exhausts every triangle combination in
all 16 mask cases, and passes 12 mutation controls.

This closes the missing **finite labelled comparison**, not HWB-081's uniform
integral map. A mod-two-zero order-two class can still be twice a class of
order four, so the two endpoint vectors have not yet been proved integrally
zero in mask 58. The next strongest path is an all-parameter integral relative
identity and transformed dual calculation for precisely those two classes,
followed by the complementary quotient. Repeating generic HNF extraction or
expanding the parameter sweep is lower priority.

The result is relevant but finite. It does not alter the theorem or claims of
the current companion manuscript, so no manuscript revision or Zenodo version
is triggered.
