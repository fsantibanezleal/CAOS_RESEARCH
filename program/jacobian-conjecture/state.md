# Jacobian conjecture - state (heartbeat)

- **State:** exploring (opened 2026-07-20).
- **Done (2026-07-20, sessions 1-2):** EXP-001 confirmed (exact validation; 3-point fiber).
  EXP-002 confirmed (structure owned). EXP-003 partially refuted (v1 lift; d = 2 rigidity).
  EXP-004 confirmed (constructor v2; new counterexamples P3/P4/P5 with rational collisions).
  EXP-005 confirmed with caveats (2D reduction; caveats honest). EXP-006 confirmed (2D scan
  non-vacuous: 216 instances, all LINEAR, all injective). EXP-007 confirmed (asymptotic variety
  explicit: A(F) = {C=0} union discriminant surface; escape = multiple fiber root). EXP-008
  confirmed (degree law (5d-3, 5d-4, 4); fiber floor 3; NEW fiber-degree-6 instance; F minimal
  within family). EXP-009 confirmed (char-p certificates: degree 12 < ell for ell = 13, 101).
  Wiki 01-05 current; manuscript v0.02 (LaTeX + PDF) built.
- **Also done (2026-07-21, session 4):** EXP-012 confirmed 1-4 / refuted 5: landscape mapped;
  the m = 2 mechanism is UNIQUE among scanned weighted systems (m = 1 = JC(2) bridge; m = 3
  empty/rigid; m = 4 potential form empty by Groebner certificate).
- **Now:** M3 web app (GitHub Pages per ADR-0016/0017/0056/0057/0058: shared shell,
  header/footer, references, page structure; baked census/wall artifacts ready from
  EXP-007/011; portfolio board from program/portfolio.yaml).
- **Also done (2026-07-21, session 3):** EXP-010 confirmed (2D equivariant rigidity THEOREM
  for opposite-sign/one-zero weights: every map in that scope is linear; the all-signature
  wording was corrected 2026-07-25). EXP-011 confirmed (real census:
  1 or 3 real preimages split by the discriminant wall; real surjectivity; real Keller
  corollary). Manuscript v0.03.
- **Next experiments:** JC-P3 continuation (global-minimality search, degrees 3..6, GPU); JC-P4
  cascade verification from primary sources; optional Lean hardening of the rigidity theorem.

- **Session 5 (2026-07-21):** EXP-013 (ray-sweep bridge certified; (2,2) exhaustive JC(2));
  EXP-016 (cascade verified from primary sources, flags lifted). Queued: JCB-021..024.
- **Session 22 (2026-07-22):** seven experiments (EXP-037/038/039/040/014/041 + the two
  context dossiers): the staircase transport instrumented (block-triangular, obstruction at
  the constant's class, generic -2a = 0); pair theory = tool; (3, n) column closed; JCB-028
  closed by subsumption; the frontier RECALIBRATED to B = 16 + (72, 108) (gcd 9/12
  certificates are replications); the properness instrument shipped; THE DIM-48 WITNESS
  (first explicit symmetric/gradient/HN falsification, HC(48) false explicitly). Routes
  evaluation in routes-2026-07-22.md. v0.25.000.
- **Session 23 (2026-07-22):** EXP-042 (THEOREM 5 window form: cleared all-parameter
  certificates, monomial pairings, window law -c_N a^N; annihilation transfers) + EXP-043
  (x^m-anchored edge operator NEW; B = 16 core = staircase transport; scoping: largest
  blocks 13/22: the frontier attack is block-cheap). THE MANUSCRIPT SPLIT: three papers
  (A foundational v0.07; B planar program v0.01 NEW; C cascade v0.02 with the explicit
  witness); all compile. Routes addendum (current view + N/M/L map + decision rule).
  v0.26.000.
- **Session 24 (2026-07-22):** EXP-044 (the certificate tower: Theorem 5 all-degree [D];
  gap = the TOWER LEMMA) + EXP-045 (degree-32 frontier certificates; similarity filter
  x18.8: the (48,64) sweep is now small). Wiki 04 rewritten; bake verified automatic.
  v0.27.000.
- **Session 25 (2026-07-22):** THE TOWER LEMMA PROVED (EXP-046): THEOREM 5 UNCONDITIONAL
  for primitive tops / d >= u+v (proper-power odd-resonance kill queued); EXP-047: the
  filtered (48, <= 64) certificates run in 2.4-3.6 s each (three samples, all empty).
  manuscript-planar v0.02. v0.28.000.
- **Session 26 (2026-07-22):** THEOREM 6 (the universal tower: one certified window =
  all-degree exclusion, non-proper-power tops) + the half-plane mechanism (EXP-048) +
  FIRST certificates at the (72,108) degrees (EXP-050, ~1 s each). manuscript-planar
  v0.03. v0.29.000. Residual structural gap: the general half-plane construction.
- **Session 27 (2026-07-22):** THE HALF-PLANE TOWER LEMMA (EXP-051): one H-certificate
  = all-degree exclusion on the whole y-most-corner staircase stratum (proper-power tops
  included); FRONTIER PAYOFF: P32 and P72 excluded at ALL partner degrees. v0.30.000.
- **Historical queue, superseded 2026-07-25:** the N1/N2 sweep ordering was replaced by the
  full strategy audit. Current work is source/applicability first, then a certificate-module
  analog. EXP-093 is cancelled.
- **Blocked on:** Felipe: novelty phrasing validation (blocks submission, not work);
  outreach call on the Thompson index correction (17 -> 18); diffusion go/no-go.

- **2026-07-25 source reconciliation:** the fresh primary-source sweep found T. Shaska,
  arXiv:2607.20210v1 (submitted 2026-07-22), independently proving the full planar
  $\mathbb{G}_m$-equivariant Keller classification. EXP-010 remains valid on its declared
  opposite-sign/one-zero scope. Derived phrases saying all signatures are linear were
  corrected: same-sign actions may give nonlinear triangular automorphisms; all signatures
  are automorphisms. The old "NOT FOUND" novelty status is superseded, with no priority
  claim. Papers A v0.11 and B v0.14 are published as immutable correction versions
  (10.5281/zenodo.21579022 and 10.5281/zenodo.21579025).
- **2026-07-25 EXP-080:** the exact invariant gate refuted the declared natural
  `sl2` triple before commutator assembly: \(P_T\) has no nonzero monomial grading,
  the edge gives nine distinct \((v,1-u)\) candidates, and sign grouping mixes
  raw shift degrees. Scoped null only; other chosen gradings/gauges remain open.
  The next action is not a full cubic solve.
- **2026-07-25 strategy audit:** the campaign is redirected. Absence of a finite
  covector and feasible support ansatzes are not evidence of consistency. EXP-075
  is retired from full execution; EXP-079 and EXP-081 are retired as stated;
  EXP-092 is held because the reduced Hamiltonian equation has \(D_P(Q)=x^2\),
  not a unit slice. During close-out, EXP-075's dormant index-2662 hit was recovered
  and reproduced in 12 seconds over both primes. The support
  \(\{(0,3),(1,0),(3,4),(4,7)\}\) is infeasible, so no global degree-three
  polynomial covector exists. EXP-093 is cancelled: its proposed 4,092,495-unknown
  target is empty. Immediate priorities:
  finish EXP-084/085 source mappings; test Makar-Limanov/Trakhtenberg, Lee-Li,
  and approximate-root constraints through an explicit GGHV applicability bridge;
  then test the exact certificate-module/chart-cover formulation on small controls.
  No experiment process is active.
- **2026-07-25 EXP-094:** the exact source-identity audit corrected the
  EXP-084/085 strong-candidate classification. C10/C11 have \(A'_0=(1,0)\),
  not the \((2,1)\) required by the discarded Heitmann families. C19/C20 have
  \(B_1=A_0=(6,15)\), not the \((6,18+6k)\) required by the separate GGV
  exclusion. GGV2 Remark 2.32 therefore excludes none of the four. This is not
   evidence that they are realizable. The immediate \((72,108)\) route advances
   to the Newton-resolution applicability bridge, followed by the
   certificate-module control if the bridge yields no restriction.
- **2026-07-25 EXP-095:** the Newton-resolution applicability bridge is
  decided. The source hypotheses do not apply directly to the final Laurent
  pair with bracket \(x^2\), but they do apply to the hypothetical original
  polynomial Keller pair. Its degree-72 component has
  \(v_0=(16,56)\), \(v'_1=(2,0)\), and \(v_1=(11/2,14)\), exactly the first
  retained \(D=72\) branch in Makar-Limanov--Trakhtenberg. No exclusion or
  floor raise follows. Next: Lee--Li plus GGHV approximate-root/intersection
  applicability, then the small certificate-module/chart-cover control.
- **2026-07-25 EXP-096:** the next source gate yields two exact necessary
  invariants. A nonzero Lee--Li inner or innermost vertex of the original
  degree-72 component is one of seven points from \((1,3)\) through
  \((7,24)\). The original pair also satisfies
  \(\deg_x\operatorname{Res}_y(P,Q)=21\), with 84 major and 24 minor roots.
  The minor-root source formula is only an inequality and cannot perform the
  hoped-for family exclusions. Next: attempt low-cost transport of these gates
  to the reduced coefficients; otherwise begin the certificate-module control.
- **2026-07-25 manuscript reconciliation:** Paper B v0.15 transcribes the
  EXP-095 applicability boundary and EXP-096 quantitative gates, corrects the
  forward program, and preserves the non-exclusion scope. The two-pass PDF and
  visual QA gates passed; PR #83 merged at `ffc6a3d`; Zenodo version DOI
  `10.5281/zenodo.21584243` is published under concept DOI
  `10.5281/zenodo.21503367`.
- **2026-07-26 EXP-097:** direct transport of intersection number \(21\)
  fails its invariant-typing gate. The GGHV pipeline swaps the selected
  eliminant, localizes \(x\), and inverts a boundary divisor. With final
  \((p,q,c)=(16,24,4)\), an input resultant interval \([\nu,21]\) becomes
  \([1515,1536-\nu]\), of width \(21-\nu\). The missing order \(\nu\) is not
  encoded by the 51 reduced coefficients alone. Do not build a direct
  degree-21 equation; proceed to the certificate-module/chart-cover analog
  unless a full boundary-divisor reconstruction is first supplied.
  Paper B v0.16 records the audit; PR #85 merged at `d47937a`, and Zenodo
  version DOI `10.5281/zenodo.21589334` is published under concept DOI
  `10.5281/zenodo.21503367`.
- **2026-07-26 EXP-098 through EXP-102:** the certificate route is now typed
  correctly and has reached the actual GGHV matrix. EXP-098 proves that a
  principal-open cover of localized global syzygies collapses to one global
  covector; the strict generalization requires closed specialization strata
  where kernels jump. EXP-099/100 refute common-flag shortcuts. EXP-101 gives
  the exact first two-parameter augmented-minor factorization
  \[
  (st-8)^6\left(2^{15}s^9-(st-8)^7\right)/2^{39},
  \]
  finds an explicit alternative minor on \(st=8\), and leaves the rational
  residual curve \(2^{15}s^9=(st-8)^7\). EXP-102 proves a third chart exists at
  \(u=1\), but its dense rank-121 curve pullback hit the five-minute budget.
  Next use the polynomial-matrix determinantal divisor over
  \(\mathbb{Q}[u,u^{-1}]\). The two-parameter slice and the full case remain
  open.
- **2026-07-26 publication:** Paper B v0.17 transcribes the constructible
  specialization correction and first exact GGHV chart transition. The
  two-pass 12-page PDF and visual QA passed. Zenodo version DOI:
  `10.5281/zenodo.21593235`, concept DOI: `10.5281/zenodo.21503367`.
- **2026-07-26 EXP-103 through EXP-105:** the complete residual curve is now
  closed exactly. EXP-103's NTT engine found a modular gcd-one pair but caught
  an 81-degree endpoint cancellation before overclaiming. EXP-104 evaluated
  100 exact 125-by-125 determinants and proved support \([1628,1646]\).
  EXP-105 exposed the connected \(\mu_9\) grading and compressed the cover to
  \[
  F(z)=21-96z-1024z^2,\qquad G(z)=(8z+1)^{14},
  \]
  with an exact integer identity \(AF+BG=17^{14}\). This excludes the complete
  declared \(\{(0,1),(1,7)\}\) slice, not the full family.
- **2026-07-26 EXP-106:** all 23 nonconstant remaining directions in the
  persisted lower family preserve both chart gradings, following
  \(w_{p,q}=q-p+1\bmod9\). The constant \((0,0)\) direction is bracket-zero.
  Promote \((0,7)\), the smallest selected support, to EXP-107. In invariant
  variables \(z=u^9,\ y=v/u\), both existing minors have \(z\)-width 14 and
  new-direction ranks 53/41. No process is active.
- **2026-07-26 publication:** Paper B v0.18 records the complete exact slice
  cover and global lower-family grading. The two-pass 13-page PDF and visual
  QA passed. Zenodo version DOI: `10.5281/zenodo.21598065`, concept DOI:
  `10.5281/zenodo.21503367`.
- **2026-07-26 EXP-107:** the first three-parameter graded lift was
  reconstructed over \(\mathbb F_{998244353}[z,y]\). The endpoint-safe minor
  remains exactly \(G(z)=(8z+1)^{14}\), independent of \(y\). The other minor
  leaves a squarefree degree-12 fiber over \(z=-1/8\); the common ideal is
  zero-dimensional, not the unit ideal. EXP-108 now targets those twelve
  geometric points with a third maximal minor. No JC(2) conclusion follows.
- **2026-07-26 EXP-108:** the first deterministic third chart eliminates all
  twelve residual geometric points. The characteristic-zero lift used 29
  exact determinant values plus independent controls. Its primitive
  degree-12 and degree-13 fiber polynomials are coprime and satisfy a
  persisted integer Bezout identity. This exactly excludes the declared
  \((0,1)/(1,7)/(0,7)\) slice, not the other coefficients or JC(2). EXP-109
  is declared for the next direction \((0,6)\).
- **2026-07-26 publication:** Paper B v0.19 records the exact
  three-coefficient slice cover. Its two-pass 14-page PDF and full visual QA
  passed; PR #90 merged at `2481d3a`. Zenodo version DOI:
  `10.5281/zenodo.21610744`, concept DOI: `10.5281/zenodo.21503367`.
- **2026-07-29 EXP-111:** the full-family rank plan is corrected. The constant
  \(Q\)-column is identically zero, so rank \(M\leq124\) is structural and the
  proposed all-\(125\)-minors target is vacuous. EXP-059's exact pinned
  augmented minor proves generic-open inconsistency, not all-parameter
  closure. The complete canonical row union has 302 rows, 13 more than
  EXP-110's forced-only list. The next route is an acyclic or small-core
  augmented basis search on the complete system. JC(2) and \((72,108)\)
  remain open.
- **2026-07-29 EXP-112:** the selected complete-family augmented minor
  compresses exactly from 125 columns and 51 parameters to one 36-column
  block depending on 24 parameters, plus three forced singleton factors. The
  other 27 directions are acyclic and determinant-inert on this chart.
- **2026-07-29 EXP-113:** removing the forced direction does not split the
  36-core. Two different three-parameter supports already generate its full
  strong connectivity, so graph complexity is intrinsically small-support.
- **2026-07-29 EXP-114:** exact triple determinants are compact. The
  \(T_A\) determinant has 24 monomials, factors in degrees \(3,12,6\), and
  cancels the graph-active \((2,9)\) direction identically. The \(T_B\)
  determinant factors into weighted degrees 54 and 63 after
  \(d=1+\varepsilon_{(1,0)}\), with weights \((7,3,9)\). Next: weighted
  alternative-minor charts on the two factor loci. No floor claim follows.
- **2026-07-29 publication:** Paper B v0.20 records the corrected full-family
  rank target and the exact 36-core/weighted-factor reduction. Its two-pass
  15-page PDF and visual QA passed; PR #92 merged at `9e039e1`. Zenodo version DOI:
  `10.5281/zenodo.21694807`, concept DOI: `10.5281/zenodo.21503367`.
- **2026-07-29 EXP-115:** weighted normalization splits the \(d\ne0\)
  selected residual into three irreducible components \(G,L,Q\). Persisted
  good-prime alternative minors prove that none is wholly rank-deficient;
  \(L\) also has an exact rational transition. The \(d=0\) prediction is
  refuted structurally: \(P=a y+b y^5+y^8(1-xy)^8\) lies in the retained
  \(Q\)-space and supplies the exact kernel \([P,P]=0\). Exact representatives
  of all three boundary components retain rank gap \(123/124\). Next:
  quotient by \(P\) and prove a 124-minor cover. No floor claim follows.
- **2026-07-29 EXP-116:** removing the fixed \(y^8\) kernel coordinate gives
  a 302-by-124 quotient system. The origin is a deeper exact \(112/113\)
  stratum; the anchor \((0,1)\) and all three nonzero boundary controls have
  exact gap \(123/124\). The normalized quotient graph has largest SCC 51,
  refuting the predicted bound 24. The corrected run enforces its 36-column
  determinant gate; EXP-117 will factor the 51-block under a new budget.
- **2026-07-29 EXP-117:** the exact quotient determinant factors as a nonzero
  scalar times \(b^{32}\), one five-term weighted factor \(F_{28}\), and five
  binomials \(c a^3+5^7b^7\). On \(b\ne0\), the invariant
  \(z=a^3/b^7\) reduces the residual to nine distinct points: five rational
  values and four roots of a squarefree quartic. EXP-118 will cover those
  points and \(b=0\) with alternative quotient charts. No floor claim follows.
- **2026-07-29 publication:** Paper B v0.21 records EXP-115 through EXP-117,
  including the structural \(P\)-kernel, 124-column quotient, and finite
  nine-point invariant reduction. Its two-pass 16-page PDF and visual QA
  passed; PR #93 merged at `b57a9b7`. Zenodo version DOI:
  `10.5281/zenodo.21695367`, concept DOI:
  `10.5281/zenodo.21503367`.
- **2026-07-29 EXP-118:** the complete \(d=0\) quotient plane is covered.
  A deterministic alternative 124-row minor is exactly \(C a^{107}\) with
  \(C\ne0\); EXP-117's selected chart is \(b^{95}\) on \(a=0\); and the
  origin retains exact rank profile \(112/113\). The alternative chart is
  nonzero at all nine invariant residual points, including the squarefree
  quartic fibre. This closes only the quotient boundary stratum.
- **2026-07-29 EXP-119:** the full 302-by-125 system has exact
  \((7,3,9)\) covariance. A characteristic-zero alternative determinant on
  \(d=1\), expressed through \(X=A^3\), has 114 monomials and unit gcd with
  each selected component \(G,L,Q\). Nonconstant exact resultants prove that
  all three pairwise intersections are finite, not empty.
- **2026-07-29 EXP-120:** the independent \(G\)-basis determinant is, up to
  a nonzero rational scalar, \(X^{30}LQR\). Factorwise exact Groebner bases
  prove the full three-chart ideal is the unit ideal on \(G\). On \(L\) and
  \(Q\) it is nonunit and zero-dimensional; the \(L\) eliminant has degree
  108 and squarefree degree 73, while the \(Q\) FGLM conversion stopped at
  its declared cost gate. Next select new bases directly on these finite
  residuals. The full \(T_B\) restriction, \((72,108)\), the degree floor,
  and JC(2) remain open.
- **2026-07-29 publication:** Paper B v0.22 records EXP-118 through EXP-120,
  including the complete quotient-boundary cover, exact \(G\)-component
  closure, and finite \(L/Q\) remainder. Its two-pass 16-page PDF and
  page-by-page visual QA passed; PR #95 merged at `68ec8d3`. Zenodo version
  DOI: `10.5281/zenodo.21696190`, concept DOI:
  `10.5281/zenodo.21503367`.
- **2026-07-30 EXP-121:** modular selection on the finite \(L\) and \(Q\)
  residual schemes returns one shared 125-row basis. It has 68 row
  replacements, largest cyclic block 26, and an exact 23-term determinant
  \(A^{87}R(A^3,B)\). The direct exact \(L\) ideal is the unit ideal. For
  \(Q\), splitting the first chart's \(B^{36}\) factor leaves a unit gcd on
  \(B=0\); quadratic reduction on the quotient branch produces degree-144
  and degree-176 compatibility polynomials with unit gcd. Thus \(L\) and
  \(Q\) are both closed. Together with EXP-118 and EXP-120, the complete
  three-parameter \(T_B\) restriction is closed. The 24-parameter core, full
  51-parameter family, \((72,108)\), degree floor, and \(JC(2)\) remain open.
- **2026-07-30 publication:** Paper B v0.23 records EXP-121 and
  the complete \(T_B\) cover. Its two-pass 17-page PDF build and complete
  visual QA pass. PR #97 merged at `d55798f`; the immutable Zenodo version
  DOI is `10.5281/zenodo.21697928`, under concept DOI
  `10.5281/zenodo.21503367`.
- **2026-07-30 EXP-122:** all 24 pinned cyclic-core directions are restored on
  the EXP-121 shared basis. None of the 21 directions outside \(T_B\) is
  determinant-inert on its anchor line; 13 act inside the size-26 block, 16
  enlarge the cyclic SCC, and all 21 participate at first or pairwise mixed
  order. The eight \((2,j)\) directions have linear anchor-line factors.
- **2026-07-30 EXP-123:** the sparsest direction \((2,9)\) lifts symbolically:
  \[
  \Delta=A^{87}\bigl(R(A^3,B)+A^2CS(A^3,B)\bigr).
  \]
  The polynomials \(R(X,B)\) and \(S(X,B)\) have 23 and 18 monomials and
  gcd one. On \(A\ne0\), the selected exceptional locus is the rational graph
  \(Y=-R/S\), plus the finite base locus \(V(R,S)\). No four-parameter cover
  is claimed.
- **2026-07-30 publication:** Paper B v0.24 records EXP-122/123 and the first
  higher-dimensional constructible reduction. PR #99 merged at `646911b`.
  Zenodo version DOI: `10.5281/zenodo.21698923`; concept DOI:
  `10.5281/zenodo.21503367`.
- **2026-07-30 EXP-124:** a cross-prime one-row basis replacement gives the
  exact alternative determinant \(A^{90}N(A^3,B)\), independent of \(C\).
  The 21-term degree-16 \(N\) factors into three plane factors
  \(F_3F_6F_7\), each coprime to \(R,S\). This covers a dense open of the
  EXP-123 graph.
- **2026-07-30 EXP-125:** corrected cube-locus primes 739 and 811 give
  \(124/125\) samples and new cross-prime bases on all three factor curves.
  Exact recursion on \(F_3=(5B+4)^3+16X\) leaves only
  \(Q_9(B)Q_{15}(B)=0\) on \(AS\ne0\): 24 normalized values and 72 lifted
  algebraic points. \(F_6,F_7\), the base locus, and \(A=0\) remain.
- **2026-07-30 publication and promotion:** Paper B v0.25 records
  EXP-124/125. PR #101 merged at `f28c5a2`, DOI PR #102 at `d51c1ae`, and
  promotion PR #103 synchronized `main`. The immutable Zenodo DOI is
  `10.5281/zenodo.21711580`.
- **2026-07-30 EXP-126:** the persisted \(F_6\) basis is exactly the
  characteristic-zero basis already reconstructed in EXP-125. Its graph
  numerator has a nonzero class \(U(B)X+V(B)\) modulo the irreducible
  quadratic \(F_6\). The exact degree-74 norm factors as
  \(D_2D_3^4D_6^2Q_{18}Q_{30}\). Direct quotient-field checks place
  \(D_2\) on \(X=S=0\) and \(D_3,D_6\) on \(R=S=0\). On \(AS\ne0\), the
  residual is \(Q_{18}Q_{30}=0\): 48 normalized values and 144 lifted
  algebraic points. \(F_7\), all finite graph strata, \(A=0\), the full
  four-parameter restriction, \((72,108)\), the floor, and \(JC(2)\)
  remain open.
- **2026-07-30 publication:** PR #106 merged EXP-126 and Paper B v0.26 into
  `develop` at `37a1341`. The immutable Zenodo version DOI is
  `10.5281/zenodo.21712096` under concept DOI
  `10.5281/zenodo.21503367`. The public 391364-byte PDF checksum
  `md5:900c591a9fdf1c02542d889e0fb0b710` matches the local file; local
  SHA-256 is
  `97444d2801f053a43fd0f868880d03a5df9f9084c0ef4be08ea690ef2f26f43a`.
- **2026-07-30 EXP-127:** the distinct persisted \(F_7\) basis reconstructs
  at anchor \((1,1,0)\) with largest cyclic block 31. Its invariant section
  is independent of \(Y\), has a nonzero linear class modulo \(F_7\), and
  gives a degree-58 norm
  \(B^{16}E_3E_9E_{12}E_{18}\). Same-point arithmetic places \(B=0\) on
  \(A=0\) and \(E_{12}\) on \(R=S=0\). On \(AS\ne0\), only
  \(E_3E_9E_{18}=0\) remains: 30 normalized values and 90 lifted points.
  No positive-dimensional factor curve remains on the graph chart. The
  finite 102-value ledger, base locus, \(A=0\), full four-parameter
  restriction, \((72,108)\), the floor, and \(JC(2)\) remain open.
- **2026-07-30 publication:** PR #109 merged EXP-127 and Paper B v0.27 into
  `develop` at `d32b7f0`. The immutable Zenodo version DOI is
  `10.5281/zenodo.21712314` under concept DOI
  `10.5281/zenodo.21503367`. The public 393753-byte PDF checksum
  `md5:954061a333009dbbe737f353b288ff5f` matches the local file; local
  SHA-256 is
  `41b869b2ef65e155c54e0257be437fb19d22d303b76c5c8df399ceb755ffcb9c`.
- **2026-07-31 EXP-128:** the seven retained graph-ledger factor
  appearances collapse to five squarefree projected blocks of degrees
  \(9,15,18,30,3\), total degree 75. Degree 9 is shared by \(F_3/F_7\) and
  degree 18 by \(F_6/F_7\). The \(h_7\) section covers the unique degree-15
  and degree-30 blocks; \(h_{36}\) vanishes on \(F_7\).
- **2026-07-31 EXP-129:** exact quotient arithmetic proves the shared
  projections have the same \(X\)-classes. Six modular controls retain full
  augmented rank 125. The single-basis prediction is refuted, but two exact
  SCC-reconstructed maximal minors have blockwise unit norms: atlas 2 covers
  degree 3 and atlas 1 covers degrees 9 and 18. Combined with EXP-124--128,
  the complete \(AS\ne0\) rational graph is closed. The finite base locus,
  \(A=0\), full four-parameter restriction, \((72,108)\), degree floor, and
  \(JC(2)\) remain open.
- **2026-07-31 publication:** PR #112 merged EXP-128/129 and Paper B v0.28
  into `develop` at `6adc5dc`. The immutable Zenodo version DOI is
  `10.5281/zenodo.21727663` under concept DOI
  `10.5281/zenodo.21503367`. The public 395770-byte PDF checksum
  `md5:db52e8d453936a3e28222fbadeb809ce` matches the local artifact; local
  SHA-256 is
  `ee97e7519b94083e1b7977f68967e73f26db0ebe268ccd37d9a5b222a6160896`.
- **2026-07-31 EXP-130:** exact projection resultants and factorwise
  subresultants decompose (V(R,S)\cap D(X)) into four reduced field blocks
  of degrees (3,6,12,69), total dimension 90. Existing sections cover the
  degree-12 and degree-69 blocks. A structurally selected new section, with
  largest SCC 33, breaks the common quadratic fibres on degrees 3 and 6.
  Exact (K[Y]) Bezout identities, independent (Y)-resultants, direct
  125-by-125 determinant control, and multiplication-matrix norms certify a
  complete finite atlas uniform in (C). Together EXP-123/129/130 close the
  complete (A\ne0) sector of the declared four-parameter restriction. The
  direct (A=0) boundary, 24-parameter core, 51-parameter family,
  ((72,108)), degree floor, and (JC(2)) remain open.
- **2026-07-31 publication:** PR #115 merged EXP-130 and Paper B v0.29
  into `develop` at `2388374`. Zenodo record `21730506` is public at
  immutable DOI `10.5281/zenodo.21730506`; its 400234-byte PDF MD5
  `80fe44419f7ed570456b91300adebeed` matches the local artifact. JCB-086
  is complete. The direct `A=0` specialization remains the sole P0 boundary
  inside the declared four-parameter restriction.
- **2026-07-31 EXP-131:** the direct \(A=0,d=1\) 302-by-125 augmented matrix
  has two exact determinants independent of \(C\). Their squarefree
  \(B\)-divisors have an explicit Bezout identity equal to one, so the
  complete boundary plane is covered. Combined with EXP-118 and
  EXP-123/129/130, the complete declared four-coefficient restriction is
  closed. The 24-parameter core, full 51-parameter family, \((72,108)\),
  degree floor, and JC(2) remain open. EXP-132 next tests direction \((2,8)\).
- **2026-07-31 publication:** PR #118 merged EXP-131 and Paper B v0.30 into
  `develop` at `51aadae`. Zenodo record `21730785` is public at immutable DOI
  `10.5281/zenodo.21730785`; its 403128-byte PDF MD5
  `e3884477cbec6392959580176c221210` matches the local artifact. JCB-087 is
  complete.
- **2026-08-01 EXP-132:** direction \((2,8)\) was added to the original
  direct \(A=0,d=1\) system. The EXP-131 primary section stays exactly
  \(T\)-independent; the second becomes affine through one
  \(B^{106}CT\) term. A residual-selected exact acyclic section is
  \(B^{105}C\). Eliminating the mixed term leaves a univariate polynomial
  coprime to the primary section, and an exact three-minor Bezout identity
  proves the maximal-minor/Fitting ideal is the unit ideal. This closes the
  complete direct boundary of the five-coefficient lift. Its \(A\ne0,d=1\)
  and transverse \(d=0\) sectors, the 24-parameter core, full 51-parameter
  family, \((72,108)\), degree floor, and JC(2) remain open. Accepted artifact
  SHA-256:
  `9465FD7E112733C0D21EB011A432898578D5ECB39FDDBE87E141C2ACE71AB0F4`.
