# EXP-064 carrier-exponent preflight

Date: 2026-09-20. Written before EXP-064 computation.

## Exact obstruction left by EXP-063

EXP-063 proves that the two endpoint triangle classes are zero in the mod-two
cokernel of mask 58 throughout `p=8,...,11`. Their integral images have order
dividing two, but this does not imply integral zero if the carrier cokernel has
order-four torsion: the element `2` in `Z/4` is order two and maps to zero
modulo two.

The smallest exact discriminator is already present in the repository. For an
integer matrix with rational rank `r`, the gap between `r` and its rank modulo
two counts even nonzero Smith factors. The first integral Bockstein detects
exactly those factors with 2-adic valuation one. Equality of the two counts
therefore proves that the complete 2-primary torsion has exponent two. A
synthetic diagonal `[4]` is the necessary control: its rank gap is one but its
first Bockstein rank is zero.

## Route choice

Adapt EXP-043's exact modular-Hadamard rank certificate to each frozen carrier
projection in masks `56,58,59,62`. Do not compute a transformed Smith form and
do not extract another generic HNF basis. The frozen EXP-045 ranks over 3 are
candidate lower bounds only; enough distinct verified primes plus the exact
Hadamard bound must force the rational upper bound.

If the carrier 2-primary groups are elementary and their ranks equal the
EXP-063 triangle-span ranks, elementary abelian group theory upgrades the
finite comparison:

- a nonzero order-two element injects into `G/2G` when the 2-primary torsion of
  `G` has exponent two;
- therefore EXP-063's mod-two-zero endpoint images are integrally zero;
- the mod-two-independent remaining triangle images form the complete
  2-primary subgroup.

This remains a finite theorem. It does not provide the all-parameter
Hadamard-rank formula, uniform integral sources, a complementary full-cokernel
bound, or a recurrence.
