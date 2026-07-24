# Direct-read dossier: Hampton-Moeckel 2006, the full certificate anatomy

Date: 2026-07-24. Source: the author-hosted revised PDF (December 17, 2004 revised
version) at www-users.cse.umn.edu/~rmoeckel/research/FinitenessRE4BP.rev.pdf, READ IN
FULL this session; archived at
`E:\_Datos\caos-research\central-configurations\papers\hampton-moeckel-2006-finiteness-re-4bp.pdf`
(SHA-256 b3ac523a1a4dbc214a1b0416c00cfd566365981dbc44b51d32ccff47eeff23f6). Published:
Invent. Math. 163 (2006) 289-312. This dossier upgrades every [HM-via-*] tag of the
method dossier to [V] and records the certificate at reproduction level. Backlog
CCB-002: DONE.

## Theorem and bounds (verbatim content)

Theorem 1: for positive masses, finitely many equivalence classes of relative
equilibria of the Newtonian 4-body problem; between 32 and 8472, INCLUDING the 12
collinear ones. Numerical experiments (Simo 1978) suggest the true count is always
between 32 and 50; 50 is attained at equal masses, and the equal-mass count 50 is
Albouy's THEOREM (Contemp. Math. 198 (1996)), not merely numerics. Earlier work:
generic finiteness without explicit genericity tests (Kuz'mina 1977; Moeckel 1985;
Moeckel 2001); much larger previous upper bounds (Kuz'mina; Llibre 1991). Whether a
4-body continuum can exist with a negative mass is stated as UNKNOWN (Roberts' 5-body
continuum cited).

## The equation system (their Section 2)

- Cartesian CC equations; multiply by m_j, sum, set lambda = m lambda'; the AC
  equations follow from the matrix form XA = 0 via translation-invariant Gram algebra
  (B_ij = -r_ij^2/2 on the mass-orthogonal plane P):
  $$\sum_{k=1}^n m_k [ S_{ik}(r_{jk}^2 - r_{ik}^2 - r_{ij}^2) + S_{jk}(r_{ik}^2 - r_{jk}^2 - r_{ij}^2) ] = 0,$$
  $S_{ij} = r_{ij}^{-3} + \lambda'$, $S_{ii} = 0$; normalization $\lambda' = -1$.
  VERBATIM MATCH with our cclib implementation (EXP-001/002 builders validated against
  the primary source).
- The equations are INDEPENDENT OF THE DIMENSION d ("they determine the central
  configurations in all dimensions at once"): the dimension-blindness our EXP-001
  refutation rediscovered by machine is stated in the primary source.
- Dziobek equations for planar noncollinear n = 4 (their (11)-(12)): from wedge
  products with signed areas Delta_l: $m_k S_{ik}\Delta_k = m_l S_{il}\Delta_l$, and
  the perpendicular-bisector theorem gives nonzero areas, yielding
  $$S_{12}S_{34} = S_{13}S_{24} = S_{14}S_{23}.$$
  Symmetrized to 3 product equations; total system: 9 equations in the 6 mutual
  distances. They could NOT run their method on the 6 AC equations alone ("We were not
  able to successfully apply our methods to the six Albouy-Chenciner equations"): the
  Dziobek enrichment is essential (mirrors our EXP-002 P1 finding that enrichment
  collapses the pathology).
- A typical AC equation (their (17)) has 14 distinct monomials; Newton polytope in R^6
  with 14 vertices (our EXP-001 P6 profile recorded exactly 14 monomials per f:
  cross-validated). Dziobek polytopes: 6 vertices.

## The finiteness criterion (their Section 3)

- Prop 1: an infinite variety V in the torus T forces a nonzero rational order vector
  alpha and convergent Puiseux solutions; dominant-axis refinement.
- Prop 2: if no Puiseux solutions of order alpha exist for all alpha in a half-space
  {c . alpha >= 0}, then V(I) is finite in T. (The tropical statement; HJ11 later
  recast it via Bieri-Groves/Speyer-Sturmfels.)
- Prop 3: if the reduced system (initial forms) f_{i,alpha} has no toric solutions,
  no Puiseux solution of order alpha exists. Reduced systems correspond to faces of
  the Minkowski sum of the Newton polytopes (normal fan refinement).

## The computation (their Sections 4-5): the reproduction targets

1. Minkowski sum polytope P of the 9 Newton polytopes in R^6, computed with Porta
   1.3.2 and lrs, exploiting S4 symmetry (factor ~24): raw vertex sums 134784 points;
   final: P has 12828 vertices and 2980 facets. f-vectors: P1 (AC sum)
   (2881, 12942, 22504, 18657, 7178, 964); P2 (Dziobek sum) (54, 210, 357, 312, 135, 24).
2. All but 53 of the 2980 facets are TRIVIAL (a reduced equation is a single monomial;
   no toric solution since masses and sums m_i, m_i + m_j, m are nonzero). Table 1
   lists the 53 nontrivial facet inequalities (transcribed in the archived PDF).
3. Half-space restriction c = (-1, ..., -1): only facets 22-53 need direct analysis;
   with S4 symmetry and the face-lattice induction (minimal representatives), the
   FULL list of faces to analyze is: {22} {25} {29} {33} {36} {48} {2,25} {2,36}
   {14,25} {14,36} {18,29} {22,48} {25,36} {33,48} {2,14,25} {2,14,36} {2,25,36}
   {14,25,36} {2,14,25,36} (19 face classes).
4. For each face: reduced system + the rescaling normalization
   r12 r13 r14 r23 r24 r34 = 1 (their (18)); Groebner elimination to MASS-ONLY
   polynomials (Mathematica, checked with Macaulay2). All faces yield mass eliminants
   in {m_i, m_i + m_j, m_i + m_j + m_k, m} EXCEPT:
   - facet 22 (alpha_22 = (0,0,-1,-1,0,0)): mass polynomial m1 m4 - m2 m3;
   - facet 33 (alpha_33 = (0,-1,-1,-1,-1,0)): (m_i+m_j)^2 (m_k+m_l)^2 (m_i^3+m_j^3)(m_k^3+m_l^3) Q,
     $$Q = (m_i^3 - m_j^3)^2 (m_k^3 - m_l^3)^2 + 4 m_i^3 m_j^3 (m_k^3 - m_l^3)^2 + 4 m_k^3 m_l^3 (m_i^3 - m_j^3)^2$$
     (their (19); the same shape as HJ11's troublesome-ray factorization, which forced
     m1 = m4, m2 = m3 there).
5. The two surviving faces are killed at SECOND ORDER (their Section 5): substitute
   r_14 = 1/t (facet 22; masses m1 m4 = m2 m3, m4 = 1) or r_13 = 1/t (facet 33;
   m1 = m2, m3 = m4 = 1); clear denominators: F(t,x) = F0(x) + F1(x) t + F2(x) t^2 + ...
   (F1 = 0 in case 22; F1(x(0)) = 0 in case 33); leading coefficients from the reduced
   equations (facet 22: x12^3(0) = m2/(1+m2), x34^3(0) = 1/(1+m2), x13^3(0) = m3/(1+m3),
   x24^3(0) = 1/(1+m3), x23(0) = +-i; facet 33 has complex leading data x14^3(0) = +-i,
   x23^3(0) = -+i, x24(0) = -1); rank DF0(x(0)) = 5; implicit function theorem: the
   second-order coefficient equations for u are consistent and unique, the THIRD-order
   equations for v are INCONSISTENT: no Puiseux solution. Theorem 1 follows.

## The bounds (their Section 6)

- LOWER 32: 12 collinear (Moulton) + 6 convex (MacMillan-Bartky, one per cyclic
  ordering) + 14 concave (their Prop 4, built on Hampton's thesis 2002: labeling
  m_C inside, triangle labels L > I > S; existence when m_I >= m_L, m_I >= m_S; 8
  permutations x reflections = 16 pairwise-inequivalent unless exactly three masses
  equal, where the count drops to 14). Unless exactly three masses are equal AND
  IU^2 degenerates, at least 34 (Xia's complementary proof).
- UPPER 8472: BKK cannot apply to the overdetermined 9-equation system; instead the
  10-equation, 10-unknown system in (r, z) (their (13): z_i = sqrt(mu) Delta_i,
  k = sqrt(mu) Delta_0, S_ij = z_i z_j, differences f_1 - f_4 etc.); a 2:1 map
  (r, z) -> r onto AC+Dziobek solutions; mixed volume of the 10 Newton polytopes
  computed with Emiris' Mixvol: 25380; the cube-root-of-unity action (omega r, z)
  divides by 3 for real r: at most 8460 noncollinear + 12 collinear = 8472.
- Their companion Mathematica notebook: reference [18] = www.math.umn.edu/~rick
  (fetch + archive: new backlog item CCB-021).

## Reference pins upgraded by this read

Smale [43] Math. Intelligencer 20 (1998) 7-15 (problem 6 attribution confirmed in a
primary paper); Chazy [8] Bull. Astron. 35 (1918) 321-389; Wintner [46] Princeton 1941;
Moulton [35] Ann. of Math. 12 (1910) 1-17; MacMillan-Bartky [28] Trans. AMS 34 (1932)
838-875; Albouy [2] Contemp. Math. 198 (1996) (the 50, as a theorem); Simo [41] Cel.
Mech. 18 (1978) 165-184; Xia [48] J. Diff. Eq. 91 (1991) 168-179; Kuz'mina [22] Sov.
Math. Dokl. 18 (1977) 818-821; Llibre [26] CMDA 50 (1991) 89-96; Moeckel [31] Ergod.
Th. Dynam. Sys. 5 (1985) 417-435; Moeckel [33] Trans. AMS 353 (2001) 4673-4686;
Emiris Mixvol [13]; Porta [9]; lrs [4]; Bernstein [6] Fun. Anal. Appl. 9 (1975);
Khovansky [20]; Kushnirenko [21].

## Consequences for our plan

- CC-P1's reproduction targets are now fully specified numerically: 12828 vertices /
  2980 facets / 53 nontrivial / 19 face classes / 2 exceptional facets with named mass
  eliminants / second-order kills / Mixvol 25380. Each is a machine-checkable rung.
- The z-variable system (13) is the RIGHT object for our mixed-volume rung (square
  10x10; BKK applies); implement it in cclib (new backlog CCB-022).
- HM06 could not handle the bare AC system; our EXP-002 P1 (enrichment collapses the
  pathology at n = 3) is the same phenomenon one level down: the method dossier's
  "enriched system as default" rule is now primary-source-grounded.
