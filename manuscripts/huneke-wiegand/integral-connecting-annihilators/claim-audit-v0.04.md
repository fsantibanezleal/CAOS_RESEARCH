# Claim and scope audit, version 0.04

Date: 2026-09-20. Publication status: published and independently verified as
Zenodo record `22859408`, DOI `10.5281/zenodo.22859408`.

## Claim-to-evidence map

| manuscript claim | primary owner | audit boundary |
|---|---|---|
| Complete original integer presentation and quadratic direct summand | EXP-054--062 | The presentation has a direct summand `(Z/2)^q`; the full cokernel, free rank, odd torsion, and remaining primary factors are not classified |
| Literal triangle coordinates in persistent finite carriers | EXP-063 | Exact only for `p=8,9,10,11`; it is not an all-parameter comparison theorem |
| Exact elementary 2-primary carrier groups on the tested range | EXP-064 | Rational rank and first-Bockstein certificates close the exponent ambiguity only for the four declared parameters and masks |
| Support-one endpoint formula in the semantic projection | EXP-065--066 | EXP-065 extracts and freezes the pattern; EXP-066 proves it for every `p>=8` and `r=1,2` before contraction |
| Locked carrier holdout | EXP-066 | The untouched `p=11` carrier selects the predicted unique columns; this validates the comparison instance but does not make it uniform |

## Exact scope

For every `p>=8`, EXP-060--062 prove a direct summand
`(Z/2)^floor(((p-2)^2+3)/12)` in the specified full integer presentation. For
every `p>=8` and `r=1,2`, EXP-066 proves the displayed support-one source maps
to the negative endpoint row under the four-type semantic projection. The
finite carrier computations show how those rows behave for `p=8,9,10,11`.

The paper does not prove a canonical all-parameter identification between that
semantic projection and the persistent isolated carrier. It does not give the
complete projected kernel, a complete 2-primary quotient, a global retraction,
or a full Smith form. The endpoint formula cannot be used as an upper bound for
the remaining triangle classes.

## Validation and publication identity

- The EXP-066 producer checks 586 exact identities through `p=300` and 2,930
  perturbation controls; an independent reverse-order audit passes. The proof,
  not the finite sweep, establishes the all-parameter formula.
- The `p=11` comparison was locked before the endpoint formula was tested on
  that carrier.
- The 20-page PDF passed the scientific-voice guard, three stable build passes,
  zero-overfull-box inspection, and all-page rendered review.
- The public record contains the sole human author Felipe Santibáñez-Leal and
  ORCID `0000-0002-0150-3246`; no machine author or coauthor is present.
- A fresh unauthenticated download matches all 516,963 committed bytes at
  SHA-256
  `1570bf3c3f48d6949cda18a32b1ba6ebd63dc9a674ce074d88c42926f284e5bf`.

## Next-version and split decision

The manuscript remains coherent as one source/duality paper and should not be
split. A later version requires a canonical comparison, complete kernel or
quotient theorem, reusable integral matching theorem, correction, or material
reproducibility change. Another finite carrier table or endpoint identity does
not qualify. The route is governed as `HW-F5` and is currently gated.
