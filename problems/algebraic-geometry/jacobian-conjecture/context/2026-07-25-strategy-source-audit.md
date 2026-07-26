# Strategy source audit: 2026-07-25

Purpose: record the primary sources used to reassess the next $(72,108)$ experiments. This
dossier verifies source statements and their applicability boundary. It does not claim a new
Jacobian-conjecture result.

## EXP-094 source-identity correction

The four configurations previously described as strong candidates under the
GGV2 closing remark do not satisfy its exact source predicates. C10/C11 have
\(A'_0=(1,0)\), not the required \((2,1)\). C19/C20 have
\(B_1=A_0=(6,15)\), not the required \((6,18+6k)\). The remark therefore
excludes none of C10, C11, C19, or C20. This correction is limited to that
remark; it does not certify the configurations against other restrictions.

## Makar-Limanov and Trakhtenberg: Newton resolution

- Authors: Leonid Makar-Limanov and Eugene Trakhtenberg.
- Title: *Properties of a Jacobian mate*.
- MPIM preprint: 2024 (33).
- Official PDF:
  https://archive.mpim-bonn.mpg.de/5148/1/mpim-preprint_2024-33.pdf
- Publication record and DOI:
  https://doi.org/10.1007/s40863-025-00520-4
- Accessed: 2026-07-25.
- Local review copy:
  `E:\_Datos\caos-research\jacobian-conjecture\sources\2026-07-25-strategy-audit\makar-limanov-trakhtenberg-2024-33.pdf`
- SHA-256:
  `492B13AF6D8FBB56481BF89415E67875389B6FCC0F95AE4F6F85D8A2E7AF623B`

Verified statements:

1. The paper develops a finite Newton-resolution algorithm using divisibility, integrality, and
   polynomiality conditions on the edge expansions of a hypothetical planar counterexample.
2. For total degree $D\le100$, its computer search lists
   $D\in\{42,48,50,56,60,63,64,66,70,72,75,80,84,88,90,96,98,99,100\}$.
3. The paper gives several explicit degree-72 resolution shapes and leading forms.
4. The hypotheses concern an actual Jacobian pair with constant bracket and a reduced component.

Applicability boundary:

The CAOS forced polynomial $P_T=y^8(xy-1)^8+x$ is part of the GGHV reduced system
$[P,Q]=x^2$. Its total degree and edge power data look incompatible with the source list if
$P_T$ were itself the reduced component of a Keller counterexample. It is not. No exclusion
follows until the GGHV reduction is shown to preserve the exact hypotheses and invariants used by
the Newton-resolution algorithm.

## Makar-Limanov: shape restrictions

- Author: Leonid Makar-Limanov.
- Title: *On the shape of a counterexample to the two-dimensional Jacobian conjecture*.
- Journal: Serdica Mathematical Journal 51 (2025).
- Official article page:
  https://serdica.math.bas.bg/index.php/serdica/article/view/300
- Accessed: 2026-07-25.
- Local review copy:
  `E:\_Datos\caos-research\jacobian-conjecture\sources\2026-07-25-strategy-audit\makar-limanov-shape-2025.pdf`
- SHA-256:
  `455B57CDB9C4E45E04517F78E1B13D6645CCAED3353EAF0DAF10F9F3FF092C65`

Verified statements:

1. Leading forms of a hypothetical planar counterexample are constrained by dependence and
   Newton-polygon similarity.
2. The paper proves no reduced counterexample has
   $\deg_y(f)=2\deg_x(f)$ with the specified vertical-edge hypothesis.
3. These statements again assume a genuine Keller pair.

Applicability boundary: use only after translating the original Keller component and its Newton
polygon through the complete GGHV normalization.

## Lee and Li: inner polynomials

- Authors: Nguyen Van Chau Lee and Jie-Tai Yu Li.
- arXiv: https://arxiv.org/abs/2408.01279
- Accessed: 2026-07-25.

Verified at abstract/source-discovery scope: the work supplies inner-polynomial and inner-vertex
restrictions intended to constrain polynomial pairs with constant Jacobian. The current program
has cited the route but has not instantiated all hypotheses on the $(72,108)$ normalization.
Status: SOURCE-COMPLETE READING REQUIRED before use.

## Guccione, Guccione, Horruitiner, and Valqui: the $(72,108)$ reduction

- arXiv: https://arxiv.org/abs/2204.14178
- Accessed: previously verified against the TeX source; rechecked for this strategy audit.

Load-bearing boundary: the reduced systems used in the CAOS experiments have bracket $x^2$ and
free interior coefficients. This prevents direct import of theorems whose hypotheses require
bracket one unless the source reduction itself transports the relevant invariant.

## Approximate roots and intersection numbers

- Primary source: Guccione, Guccione, and Valqui.
- arXiv: https://arxiv.org/abs/1708.09367
- Accessed: 2026-07-25.

Status: identified as a high-value source route. The formulas may constrain the same degree and
polygon data independently of the certificate ladder. They have not yet been instantiated on the
51-parameter reduced family, so no conclusion is recorded.

## Jelonek: bounded-degree parameter spaces

- Author: Zbigniew Jelonek.
- Title: *On mappings with Jacobian one*.
- arXiv: https://arxiv.org/abs/2607.20597
- Accessed: 2026-07-25.

Verified statements:

1. For fixed source dimension and degree bound, the automorphism locus inside the
   Jacobian-one mapping space is Zariski closed.
2. Each irreducible component either consists of automorphisms or has a generic
   counterexample locus.

Applicability boundary: this organizes genuine bounded-degree Jacobian-one maps. The CAOS
reduced $[P,Q]=x^2$ family is not directly a subfamily of that space. Use this as a medium-term
component strategy only after defining the relevant original Keller parameter space.

## Decision supported by this dossier

The source record supports a source-first applicability round before more large linear algebra.
It does not support excluding $(72,108)$, raising the degree floor, or inferring the existence of
a counterexample from failure to find a certificate.
