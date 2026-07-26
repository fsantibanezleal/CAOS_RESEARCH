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

- Authors: Leonid Makar-Limanov and Leonid Trakhtenberg.
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
3. The paper gives several explicit degree-72 resolution shapes and leading forms. Its first
   \(D=72\) row has
   \(v_0=(16,56)\), \(v'_1=(2,0)\), \(v_1=(11/2,14)\), and
   \(\phi_0=cx(xy^4-r_1)^7\).
4. The hypotheses concern an actual Jacobian pair with constant bracket and a reduced component.

Applicability boundary:

The CAOS forced polynomial $P_T=y^8(xy-1)^8+x$ is part of the GGHV reduced system
$[P,Q]=x^2$ in \(K[x,x^{-1},y]\), so the source hypotheses do not apply directly
to that final pair. EXP-095 instead returns to the original polynomial Keller
pair. Its degree-72 component has
\(2A_0=(16,56)\), \(2A'_0=(2,0)\), and
\(2A_1=(11/2,14)\), exactly matching the first printed \(D=72\) row. Thus the
published Newton-resolution list independently retains, rather than excludes,
the open GGHV branch. Any further use requires new conditions beyond that
published candidate classification.

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

- Authors: Kyungyong Lee and Li Li.
- arXiv: https://arxiv.org/abs/2408.01279
- Accessed: 2026-07-25.
- Reviewed PDF SHA-256:
  `4A9E77064137C46F4F202206645D00DC0569A8985DECC28D66A93847CC9140D6`.

EXP-096 completed the source reading and instantiated Theorem 5.8 and
Corollary 5.10 on the original degree-72 component. With
\((a,b,m,n)=(2,3,16,56)\), every nonzero inner or innermost vertex lies in

\[
\{(1,3),(2,7),(3,10),(4,14),(5,17),(6,21),(7,24)\}.
\]

The zero inner-polynomial alternative remains. Corollary 5.11 does not force
the diagonal because \(3/2\not>19\). These facts apply after polynomial
rectangularization of the original pair, not directly to the final Laurent
pair.

## Guccione, Guccione, Horruitiner, and Valqui: the $(72,108)$ reduction

- arXiv: https://arxiv.org/abs/2204.14178
- Accessed: previously verified against the TeX source; rechecked for this strategy audit.

Load-bearing boundary: the reduced systems used in the CAOS experiments have bracket $x^2$ and
free interior coefficients. This prevents direct import of theorems whose hypotheses require
bracket one unless the source reduction itself transports the relevant invariant.

## Approximate roots and intersection numbers

- Primary source: Guccione, Guccione, Horruitiner, and Valqui.
- arXiv: https://arxiv.org/abs/1708.09367
- Accessed: 2026-07-25.
- Reviewed v2 PDF SHA-256:
  `331FE6361ED98EC31795CC5F42FFC0A7AF6AE70510FCDF78CCE9672CAD08C3F1`.

EXP-096 instantiated Proposition 3.21 and Theorem 3.15 on the open chain.
Four major classes each have \(3\cdot7=21\) roots and
\(\lambda_\tau^Q=1/4\), so

\[
I(P,Q)=\deg_x\operatorname{Res}_y(P,Q)=4\cdot21/4=21.
\]

The degree-108 component partitions into 84 major and 24 minor roots. This is
an exact original-pair rejection gate. The paper's hoped-for minor-root
exclusion does not follow: it proves an inequality where the earlier argument
required equality.

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
