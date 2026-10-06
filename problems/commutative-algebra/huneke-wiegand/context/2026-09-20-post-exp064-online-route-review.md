# Post-EXP-064 online route review

Date: 2026-09-20. Scope: primary-source update and route selection after the
exact finite carrier theorem.

## Current external state

Son Pham's preprint, *A Counterexample to the Huneke-Wiegand Conjecture*,
arXiv:2609.07615, gives a characteristic-independent numerical-semigroup
counterexample and reduces its finite core to a sumset identity. It also records
the trace ideal, endomorphism ring, completion and a direct graded tensor
verification. This settles the original general conjecture negatively, but it
does not compute the integral carrier maps studied in EXP-042--064.

Lars Winther Christensen, Alex Gerko and Srikanth B. Iyengar,
*Some non-principal rigid ideals in Gorenstein domains of dimension one*,
arXiv:2608.21666, give an independent field-extension construction. Their
criterion is expressed through subspace multiplication in a degree-24 field
extension. It is structurally different from the numerical-semigroup family and
does not identify the CAOS Koszul carrier quotient.

The March 2026 revision of Landeros, O'Neill, Pelayo, Pena, Ren and Wissman,
*Families of numerical semigroups and a special case of the Huneke-Wiegand
conjecture*, arXiv:2404.12519, proves the positive two-generated-monomial-ideal
case for generalized arithmetic-sequence semigroups. Its visualization and
arithmetic-sequence method is useful for semigroup-family classification, not
for the current integer presentation after the counterexample has been fixed.

## Adjacent methods checked

1. **Algebraic Morse theory.** Skoldberg, *Algebraic Morse theory and
   homological perturbation theory*, arXiv:1311.5803, and Chen-Liu-Zhou,
   arXiv:2404.10165, justify unit cancellation and perturbative reconstruction.
   They do not provide the problem-specific matching. The actionable target is
   therefore an explicit parametric matching or rewrite system, not another
   citation-level appeal to Morse theory.
2. **Modules and matroids over the integers.** Fink and Moci, *Matroids over a
   ring*, arXiv:1209.6571, packages deletion, contraction and torsion data over
   Dedekind domains. The six carrier atoms naturally suggest this language, but
   the CAOS row projections have not been proved to form the required matroid
   minors. It is a theorem framework only after explicit maps are built.
3. **Representation stability.** Church and Ellenberg, *Homology of
   FI-modules*, arXiv:1506.01022, supplies integral stable-range machinery for
   finitely generated FI-modules. The present labels depend on affine intervals
   and distinguished endpoints, so ordinary FI-functoriality is not established.
   An ordered-injection or finite-state rewrite model would have to be proved
   first.
4. **Topological critical groups.** Alfaro et al., *The Smith normal form of
   Laplacian matrices of simplicial annuli and high dimensional trees*,
   arXiv:2607.23506, shows that structured simplicial families can admit exact
   Smith forms through graph/sandpile models. The carrier matrix is not known to
   be a Laplacian, so this is an analogy and a recognition target, not evidence.
5. **Polynomial Smith equivalence.** Lu, Ruan, Wang and Xiao,
   arXiv:2605.09286, study equivalence to Smith form for multivariate polynomial
   matrices through determinantal ideals. Our matrix size changes with `p`, so a
   polynomial matrix model would first require a finite-state block encoding.

## Reprioritized paths

### Path A: dual-guided exact decoding, selected now

EXP-064 proves that the two mask-58 endpoint rows are in the integral image for
`p=8,...,11`, but gives no source coefficients. Treat source columns as moves
and a target row as a syndrome. On a partial column set, exact elimination either
finds a witness or produces an annihilating dual. Any full witness must use an
omitted column with nonzero dual pairing, so add exactly those escaping columns.
This is the column-generation/cutting-plane reading of EXP-058's escaping-column
lemma. It can produce original-coordinate witnesses while avoiding a global HNF.

### Path B: relative divisor-complex filtration

Interpret the six row atoms as strata in a pair of divisor complexes and seek a
long exact sequence whose connecting map is the carrier inclusion. This would
explain the constant two-class completion and may yield an all-parameter upper
bound. It remains secondary until the exact chain map is written down.

### Path C: finite-state algebraic Morse matching

Normalize every row and column by interval endpoint distances. If the decoder's
witnesses use finitely many normalized transition types, orient them as rewrite
rules and prove termination with a lexicographic height. This is the strongest
candidate for a uniform theorem because it can construct both the source and a
free complement.

### Path D: representation stability or polynomial Smith form

Attempt only after Path C produces a finite transition alphabet. Without that
finite generation input, FI/OI and polynomial-matrix language merely rename the
unproved uniformity.

## Manuscript assessment

No split is justified now. EXP-063/064 are exact but finite and belong as future
computational evidence in the existing integral-connecting manuscript only after
an all-parameter comparison theorem is obtained. A separate manuscript becomes
appropriate if either:

- a uniform carrier exact sequence classifies the complete 2-primary quotient;
- a finite-state integral Morse theorem applies beyond this semigroup family; or
- the full complementary cokernel receives a normal form or recurrence.

The two external counterexample constructions should not be combined into a new
CAOS manuscript unless CAOS proves a comparison or classification theorem that
is not already in those sources.

## Primary sources

- https://arxiv.org/abs/2609.07615
- https://arxiv.org/abs/2608.21666
- https://arxiv.org/abs/2404.12519
- https://arxiv.org/abs/1311.5803
- https://arxiv.org/abs/2404.10165
- https://arxiv.org/abs/1209.6571
- https://arxiv.org/abs/1506.01022
- https://arxiv.org/abs/2607.23506
- https://arxiv.org/abs/2605.09286

