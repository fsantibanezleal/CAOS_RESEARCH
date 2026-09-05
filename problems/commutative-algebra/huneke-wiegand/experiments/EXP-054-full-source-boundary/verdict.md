# EXP-054 verdict

Status: **P1 REFUTED; P2/P3 CONFIRMED FINITELY**.

The complete original differential has one extra row in each training case:

| p | residual coefficient | residual row |
|---:|---:|---|
| 8 | 2 | `[K,L_p minus {2,3p};13p]` |
| 9 | -2 | `[K,L_p minus {2,3p};13p]` |
| 10 | 2 | `[K,L_p minus {2,3p};13p]` |

The two saved source multisets agree, every projected component identity passes, and the full
source remains a mod-two cycle because the residual is even. The independent audit passes all
213 checks, including all 15,405 projected rows and a sign-corruption control. Both outputs are
deterministic, with no full-basis enumeration or HNF.

## Consequences

EXP-053's positive result is an identity in the reduced component, not a literal zero-extended
full-source identity. The original source needs a pivot-lift correction. EXP-055 constructs it.
The finite Smith/Bockstein results remain valid under integral unit cancellation. The proposed
all-parameter source chain, second class, and upper bound are still open.

The published v0.23 and companion v0.02 do not depend on EXP-053. This finding does not create an
erratum to either frozen PDF or a new Zenodo trigger. Derived research narratives must nevertheless
be corrected. The new path is provenance-preserving contraction plus bounded low-complement
coordinates, not another generic transformed-HNF extraction.

## How could this be wrong?

The full differential is independently encoded from the same persisted coefficient-module
definition; this is not an independent derivation of that algebra itself. Saved source labels
come from EXP-053, but exact grading, full multiplication, and the original frozen matrix
regression are checked here. Only `p=8,9,10` residuals are claimed. A correction lemma for all `p`
does not supply an all-parameter source family.
