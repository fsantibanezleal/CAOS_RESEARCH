# EXP-040 preflight - the degree-six relation inside the merged sector

Date: 2026-08-30. Status: source-complete for the declared finite test.

## Exact motivation

EXP-039 refutes bounded defect-one connected components but discovers exact defect partitions

```text
p=6: 4+2+2+1
p=7: 10+3+3+2
p=8: 20+4+4+3
p=9: 45+4, with 45=35+5+5.
```

Thus four latent sectors have finite dimensions

```text
binom(p-2,3), p-4, p-4, p-5,
```

and at `p=9` the first three merge in support while preserving their combined rank defect.  Their
free extension predicts 73 at `p=10`, but EXP-037 gives 72.  This locates the first possible
degree-six relation inside the merged sector, provided the fourth sector remains intact.

## Source boundary

Bruns--Herzog's squarefree-divisor-complex theorem
<https://doi.org/10.1016/S0022-4049(97)00051-0> justifies treating characteristic-dependent
multigraded Betti numbers as signed integral homology.  Autry et al.
<https://arxiv.org/abs/1804.06632> supports direct structural study of numerical-semigroup
divisor complexes.  The current sweep found no published decomposition or relation for this
conductor-family sequence.  FI/OI rationality results <https://arxiv.org/abs/2006.13083> remain a
possible all-parameter framework only after compatible translation maps are constructed; they do
not imply the sector predictions.

## Declared predictions

- At `p=10`, the defective connected-component partition is `67+5`.  Here
  `67=(56+6+6)-1`, so the unique deficit from the free-sector total lies in the merged component.
- Conditional on that pass, at `p=11` the partition is `96+6`, where
  `96=(84+7+7)-2`.  The correction multiplicity two is the first translate count of a degree-six
  relation.
- `GF(3)` and `GF(5)` agree component by component, not only in aggregate.

## Resource and kill gate

- CPU only, exact `GF(2)`, `GF(3)`, and `GF(5)` ranks.
- Reuse the frozen EXP-039 component decomposition without modifying it.
- `p=10` budget: 900 seconds and 30 GB.  Run `p=11` only if `p=10` passes; combined cap 2,400
  seconds and 36 GB, with a checkpoint after `p=10`.
- A partition mismatch refutes the sector-relation placement immediately.  A resource stop is
  **INCONCLUSIVE**.

## Structural follow-up gate

If both partitions pass, the next phase must label the four pre-merge sectors and exhibit signed
cross-sector columns whose removal restores the free partitions `68+5` and `98+6`.  Numerical
partition agreement alone remains finite evidence.  Manuscript v0.24 and Zenodo stay closed until
an all-parameter signed relation/translation theorem is proved.
