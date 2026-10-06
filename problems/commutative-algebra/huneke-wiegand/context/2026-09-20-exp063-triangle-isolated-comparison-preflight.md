# EXP-063 triangle-to-isolated comparison preflight

Date: 2026-09-20. This note was written before EXP-063 computation.

## Question inherited from the proved results

EXP-062 proves in the full original integral presentation that the selected
triangle rows `x_T` generate a split subgroup `(Z/2)^q`, where
`q=floor(((p-2)^2+3)/12)`. EXP-042--048 independently isolate a persistent
signed component whose complete finite two-primary ranks are `3,4,5,7` for
`p=8,9,10,11`. Equality of these four ranks is not a comparison map.

The missing low-cost test is whether every exact labelled `x_T` survives the
already certified unit cancellations, lands as the semantic `R5` row in the
isolated component, and spans its mod-two Bockstein image. If so, the literal
surviving target coordinates give a finite integral target comparison and
locate the relative losses under masks `59/62 -> 58 -> 56`.

## Sources and proof-language boundary

- Emil Skoldberg, *Algebraic Morse theory and homological perturbation theory*,
  arXiv:1311.5803, gives the contraction discipline behind algebraic Morse
  cancellation. The CAOS use remains elementary: every cancelled entry is a
  unit, and the target image of a vector supported only on surviving rows is
  tracked explicitly through the block elimination. No theorem from that paper
  identifies the problem-specific triangle rows.
- Alex Fink and Luca Moci, *Matroids over a ring*, JEMS 18 (2016), 681--731,
  DOI 10.4171/JEMS/600, supplies a useful deletion/contraction viewpoint for
  modules over rings. It does not supply the required CAOS comparison or an
  upper bound, so EXP-063 will not import a matroid-over-a-ring claim.
- Bruns and Herzog, *Semigroup rings and simplicial complexes*, JPAA 122
  (1997), 185--208, remains a possible relative-divisor-complex language. The
  required semigroup quotient and signed chain identification have not been
  established, so they are not premises of this experiment.

The exact finite computation can establish a labelled comparison for the four
tested parameters and expose candidate relations. It cannot by itself prove a
uniform comparison, a complementary quotient, or a recurrence.

## Reconciled route decision

Do not reopen the failed bounded-canonical-lift or leaf-core searches. Use the
frozen signed isolated matrices, independently reconstruct the omitted exact
row labels, and compute the quotient ranks of the literal triangle-coordinate
vectors modulo the projected relation images. Preserve the relation kernels as
named triangle combinations; those kernels, rather than elimination indices,
are the input to any later symbolic experiment.

The publication threshold is unchanged. A finite comparison is a relevant
research result and plan update, but not by itself a manuscript or Zenodo
revision. A uniform labelled chain comparison, integral normal form, or full
upper bound would trigger a manuscript revision assessment.
