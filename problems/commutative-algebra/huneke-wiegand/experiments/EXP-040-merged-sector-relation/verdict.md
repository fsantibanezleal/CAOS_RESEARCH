# EXP-040 verdict

Status: **REFUTED** overall. P1 passes; P2 fails; P3 was not attempted.

The exact `p=10` characteristic-defect partition is `67+5`, exactly as declared.  This localizes
the first correction from the free-sector value 73 to the merged component: its predicted free
count 68 becomes 67, while the other component contributes five.  Every component agrees over
`GF(3)` and `GF(5)`.

The conditional `p=11` prediction fails.  The observed partition is `95+7`, not `96+6`, although
both sum to the already audited total 102.  Therefore the simple rule that translated relations
remain wholly in the merged sector while a fourth sector follows `p-5` is false.  Sign erasure and
one-sign-flip controls confirm that both observed components depend essentially on orientation.

The strongest next route is semantic component profiling: identify which row/column interval
types form the small components at `p=10` and `p=11`, transport tags from the four pre-merge
sectors, and only then test signed bridge removal.  The finite P1 localization is relevant but is
not an explicit relation or an all-parameter theorem.  Manuscript and Zenodo gates remain closed.
