# RESUME: Jacobian conjecture program

Updated 2026-07-30 after EXP-126 reinterpreted the recursive atlas as a
divisor computation and reduced \(F_6\) to a finite residual. This is
the first-read navigation page. Primary artifacts and experiment verdicts
remain the evidence.

## 1. State in one screen

- The Jacobian conjecture is false in every dimension at least three. The program's exact
  validation, generalization, geometry, and consequence record remains intact.
- JC(2) remains open. The program has not excluded $(72,108)$ and has not raised the planar
  degree floor.
- The GGHV target is a reduced family with $[P,Q]=x^2$, three forced branches, and 51 free
  interior coefficients. Forced-edge samples and axis-symbolic families have certificates;
  simultaneous all-parameter coverage is missing.
- EXP-067 excludes a degree-one certificate in its declared full system. EXP-072 finds an
  infeasible degree-two restricted support. EXP-075's recovered and reproduced
  four-parameter hit excludes a global degree-three polynomial covector. Feasible supports in
  EXP-073 and before the EXP-075 hit remain one-sided nulls.
- EXP-078 withdrew the proposed finite ceiling. EXP-080 refuted the declared natural `sl2`
  grading at its invariant gate. Neither is a no-go theorem for all certificate constructions.
- EXP-093 is cancelled. Its proposed cubic target is proved empty by EXP-075.
- EXP-095 confirms that Newton resolution applies to the original degree-72
  Keller component, not directly to the final Laurent pair. The component
  exactly matches the first retained Makar-Limanov--Trakhtenberg \(D=72\)
  branch, so no exclusion follows.
- EXP-096 gives the first new quantitative source invariants for the open
  chain: seven possible nonzero inner vertices, exact intersection number
  \(21\), and an \(84+24\) major/minor root partition.
- EXP-097 proves that absolute resultant degree \(21\) is not a typed equation
  on the final Laurent coefficients without a missing boundary-divisor ledger.
  The direct transport route is closed; conditional exponent width survives.
- EXP-098 proves that principal-open localized certificate covers collapse to
  one global covector. The stronger object is a constructible rank
  stratification with new syzygies after closed specialization.
- EXP-101 gives the first exact chart transition on the actual GGHV matrix:
  \[
  \det A(s,t)/\det A_0=
  (st-8)^6\left(2^{15}s^9-(st-8)^7\right)/2^{39}.
  \]
  An alternative minor covers \(st=8\); the residual is the rational curve
  \(2^{15}s^9=(st-8)^7\).
- EXP-104/105 close the complete residual curve and hence the declared
  two-coefficient slice. With \(z=u^9\), two normalized maximal minors are
  \[
  F(z)=21-96z-1024z^2,\qquad G(z)=(8z+1)^{14},
  \]
  and an exact integer Bezout identity gives
  \(A(z)F(z)+B(z)G(z)=17^{14}\).
- EXP-106 proves the same connected \(\mathbb Z/9\) grading accepts all 23
  nonconstant remaining directions in the persisted lower family, with
  \(w_{p,q}=q-p+1\bmod9\). The promoted \((0,7)\) direction has ranks 53/41
  on the two charts.
- EXP-107 reconstructs the first three-parameter lift modulo \(998244353\).
  The endpoint-safe chart stays \(G(z)=(8z+1)^{14}\), independent of \(y\);
  the first chart leaves a squarefree degree-12 residual fiber at \(z=-1/8\).
  This is a finite third-chart target.
- EXP-108 closes that target exactly. A deterministic third chart restricts
  to a degree-13 polynomial \(H(y)\) coprime to the exact irreducible
  degree-12 \(Q(y)\), with a persisted integer Bezout identity. Three maximal
  minors therefore exclude the declared \((0,1)/(1,7)/(0,7)\) slice.
- EXP-111 supersedes EXP-110's interpretation. The constant \(Q\)-column is
  identically zero because \([P,1]=0\), so
  \(\operatorname{rank}M\leq124\) for every parameter value. EXP-059's exact
  nonzero pinned augmented minor then proves generic rank \(124/125\) for
  \(M/[M\mid b]\), hence generic-open inconsistency. This does not prove
  all-parameter inconsistency.
- EXP-110's forced-only row list has 289 rows. The complete union inside the
  same canonical EXP-071 pool has 302 rows: 13 omitted equations contributed
  by 14 lower directions. Four deterministic points over two primes retain
  the \(124/125\) profile in both row systems.
- PLAN REDIRECT (EXP-111): all \(125\)-minors of \(M\) vanish trivially because
  of the zero constant column, so that target is retired. Remove the constant
  column, append \(b\), and attack the common zero locus of augmented
  \(125\)-minors. EXP-112 first searches the complete 302-row system for an
  acyclic row basis or a small strongly connected parameter core.
- EXP-112 gives an exact pinned-chart compression. The selected
  125-by-125 determinant factors through one 36-by-36 cyclic block depending
  on 24 parameters, three one-dimensional
  \(1+\varepsilon_{(1,0)}\) factors, and acyclic singleton blocks. The other
  27 parameters do not affect this selected determinant.
- EXP-113 proves the 36-core remains strongly connected without the forced
  direction. Full connectivity is already generated by
  \(T_A=\{(0,1),(0,7),(2,9)\}\) and independently by
  \(T_B=\{(0,1),(0,5),(1,0)\}\).
- EXP-114 corrects the graph reading algebraically. The \(T_A\) determinant is
  independent of \((2,9)\) and factors in degrees \(3,12,6\). On \(T_B\),
  with \(d=1+\varepsilon_{(1,0)}\), the determinant factors into weighted
  homogeneous polynomials of weights \((7,3,9)\) and weighted degrees 54 and
  63. Weighted residual charts are now the P0 route.
- EXP-115 splits the weighted-open residual into three irreducible components
  \(G,L,Q\). Exact good-prime alternative minors prove that none is contained
  in the rank-deficient locus; \(L\) also has a rational characteristic-zero
  witness. On \(d=0\), however, rank 125 is structurally impossible:
  \(P=a y+b y^5+y^8(1-xy)^8\) enters the \(Q\)-space and gives the polynomial
  kernel \([P,P]=0\). Exact representatives of all three boundary components
  have rank profile \(123/124\). The P0 route is now the quotient by this
  explicit \(P\)-kernel.
- EXP-116 removes the fixed \(y^8\) kernel coordinate and obtains a
  302-by-124 quotient system. The origin is a deeper \(112/113\) stratum;
  \((0,1)\) and all three nonzero boundary controls have exact gap
  \(123/124\). The quotient graph has a 51-column largest SCC, above the
  declared determinant gate. EXP-117 is the next exact factorization gate.
- EXP-117 factors that quotient determinant exactly. In original coordinates
  it is a nonzero scalar times \(b^{32}F_{28}\) and five binomials
  \(c a^3+5^7b^7\). On \(b\ne0\), \(z=a^3/b^7\) reduces the selected residual
  to nine distinct geometric points: five rational and four on a squarefree
  quartic. The remaining quotient targets are those nine points and \(b=0\).
- EXP-118 closes the complete \(d=0\) quotient boundary. An alternative
  124-row minor is exactly \(C a^{107}\), so it covers \(a\ne0\); the
  EXP-117 chart restricts to \(b^{95}\) on \(a=0\); and the origin retains
  the exact quotient rank gap \(112/113\). The nine invariant points,
  including the quartic fibre, are covered by the alternative chart.
- EXP-119 computes a first characteristic-zero alternative chart on
  \(d\ne0\). With \(X=A^3\), its exact determinant has 114 monomials and
  meets each irreducible selected component \(G,L,Q\) properly. Exact
  resultants reduce all three intersections to finite schemes.
- EXP-120 adds an independent third chart. Its determinant is, up to a
  nonzero scalar, \(X^{30}LQR\). Factorwise exact Groebner certificates close
  the complete \(G\) component. The \(L\) and \(Q\) common residuals remain
  zero-dimensional; the \(L\) eliminant has degree 108 and squarefree degree
  73.
- EXP-121 selects row bases on those finite residuals. The \(L\) and \(Q\)
  selections return the same 125-row basis, with 68 replacements and largest
  cyclic block 26. Its 23-term determinant is
  \(A^{87}R(A^3,B)\). A direct exact Groebner basis closes \(L\); an exact
  \(B^{36}\) zero-set split, quadratic reduction, and two unit univariate
  gcds close \(Q\). Combined with EXP-118 and EXP-120, the complete
  three-parameter \(T_B\) restriction is closed. The 24-parameter core,
  51-parameter family, \((72,108)\), degree floor, and \(JC(2)\) remain open.
- EXP-122 restores all 24 cyclic-core directions on the EXP-121 shared basis.
  None of the 21 directions outside \(T_B\) is free on its anchor line.
  Thirteen act inside the size-26 block, 16 enlarge the fixed-\(d\) SCC, and
  all 21 participate at first or pairwise mixed order. The eight directions
  \((2,j)\), \(2\leq j\leq9\), have linear anchor-line factors.
- EXP-123 lifts the sparsest direction \((2,9)\) exactly. With
  \(X=A^3\), \(Y=A^2C\), and \(C=\varepsilon_{(2,9)}\),
  \[
  \Delta=A^{87}\bigl(R(X,B)+Y S(X,B)\bigr),
  \qquad \gcd_{\mathbb Q[X,B]}(R,S)=1.
  \]
  The polynomials \(R,S\) have 23 and 18 monomials. On \(A\ne0\), the
  selected exceptional locus is the rational graph \(Y=-R/S\) over
  \(S\ne0\), plus finite \(V(R,S)\). No four-parameter cover is proved.
- EXP-124 selects an alternative basis on that graph and reconstructs
  \(\Delta_{\rm alt}=A^{90}N(A^3,B)\). The exact 21-term degree-16
  polynomial \(N\) factors into three plane curves \(F_3F_6F_7=0\).
- EXP-125 finds new cross-prime bases on all three curves. On
  \(F_3=(5B+4)^3+16X\), exact restriction gives
  \((5B+4)Q_6^2Q_9Q_{15}\). After removing \(A=0\) and the \(R=S=0\)
  base locus, only \(Q_9Q_{15}=0\) remains: 24 normalized values and 72
  lifted algebraic points.
- EXP-126 finds that the persisted \(F_6\) basis is the same exact section
  already reconstructed in EXP-125. Its nonzero quotient class
  \(U(B)X+V(B)\) has degree-74 norm
  \(D_2D_3^4D_6^2Q_{18}Q_{30}\). Exact same-point checks remove the first
  three boundary factors, leaving \(Q_{18}Q_{30}=0\) on \(AS\ne0\):
  48 normalized values and 144 lifted algebraic points. Only \(F_7\)
  remains positive-dimensional on the graph.
- Controlling strategy:
  [`strategy-audit-2026-07-30.md`](strategy-audit-2026-07-30.md).
- Source audit:
  [`2026-07-30-strategy-refresh.md`](../../problems/algebraic-geometry/jacobian-conjecture/context/2026-07-30-strategy-refresh.md).

## 2. The objects table

| Object | Definition or role | Evidence |
|---|---|---|
| $F$ | validated dimension-three counterexample | EXP-001/002 |
| constructor v2 | exact seed-family constructor | EXP-004 and `code/jclib/` |
| planar theorem ladder | weight classes, anchored edges, vertex dichotomy, staircase towers | EXP-029 through EXP-051 |
| GGHV forced polynomial | $P_T=y^8(xy-1)^8+x$ | EXP-052/053 and the GGHV dossier |
| reduced equation | $[P,Q]=x^2$ | GGHV Proposition 4.3 transcription |
| parameter ring | $R=\mathbb{Q}[\varepsilon_1,\ldots,\varepsilon_{51}]$ | EXP-054 onward |
| reduced linear system | \(M(\varepsilon)q=b\), with 125 \(Q\)-columns, 302 complete pool rows, and one structural constant column | EXP-111 |
| effective augmented system | \(A=[M_{\mathrm{nonconstant}}\mid b]\), a 302-by-125 affine-linear matrix | EXP-111 |
| global covector | $c^TM=0$ and $c^Tb\ne0$, sufficient for inconsistency | EXP-053 onward |
| certificate module target | left syzygies of $M$, their pairing ideal with $b$, and localized chart certificates | strategy audit |
| constructible certificate recursion | generic pairing opens followed by kernel recomputation on residual closed strata | EXP-098 |
| first GGHV minor stratum | \((st-8)^6(2^{15}s^9-(st-8)^7)/2^{39}\) on directions \((0,1),(1,7)\) | EXP-101 |
| residual curve | \(s=8u^7,\ t=(8u^9+1)/u^7,\ u\ne0\) | EXP-101 |
| exact residual-curve cover | \(F(z)=21-96z-1024z^2,\ G(z)=(8z+1)^{14},\ AF+BG=17^{14}\) | EXP-104/105 |
| pinned augmented cyclic core | 36 columns and 24 active parameters; 27 directions acyclic on the chart | EXP-112 |
| connectivity triples | \(T_A=\{(0,1),(0,7),(2,9)\}\), \(T_B=\{(0,1),(0,5),(1,0)\}\) | EXP-113 |
| weighted residual factors | \(D_B=2^{-42}G_{54}H_{63}\), weights \((7,3,9)\) in \((a,b,d)\) | EXP-114 |
| weighted-open components | irreducible \(G,L,Q\), each generically removed by an alternative complete-row minor | EXP-115 |
| \(d=0\) kernel | \(P=a y+b y^5+y^8(1-xy)^8\) lies in the \(Q\)-space and \([P,P]=0\); sample rank gap \(123/124\) | EXP-115 |
| \(d=0\) quotient graph | remove \(y^8\); origin rank \(112/113\), generic controls \(123/124\), largest SCC 51 | EXP-116 |
| quotient residual invariant | \(b=0\) or nine squarefree values of \(z=a^3/b^7\) from one quartic and five linear factors | EXP-117 |
| complete \(d=0\) quotient cover | \(C a^{107}\), \(b^{95}\), and the origin rank gap cover the boundary plane | EXP-118 |
| first weighted-open alternative chart | exact \(X=A^3\) factorization; proper finite intersections with \(G,L,Q\) | EXP-119 |
| third weighted-open chart | \(\Delta_G\doteq X^{30}LQR\); unit ideal on \(G\), finite nonunit ideals on \(L,Q\) | EXP-120 |
| finite-residual shared chart | one 125-row basis on both \(L,Q\); \(\Delta_{\mathrm{fin}}=A^{87}R(A^3,B)\); exact unit certificates on both | EXP-121 |
| shared-basis core activity tensor | exact traces, pair traces, anchor-line factors, and SCC changes for all 24 core directions | EXP-122 |
| first four-parameter lift | \(\Delta=A^{87}(R(A^3,B)+A^2CS(A^3,B))\), with primitive coefficient gcd one | EXP-123 |
| rational exceptional graph | \(Y=-R(X,B)/S(X,B)\) on \(A S\ne0\), with finite base locus \(V(R,S)\) | EXP-123 |
| dense-open graph chart | \(\Delta_{\rm alt}=A^{90}N(A^3,B)\), with \(N=F_3F_6F_7\) up to scalar | EXP-124 |
| \(F_3\) finite reduction | principal-open residual \(Q_9(B)Q_{15}(B)=0\): 24 normalized values, 72 lifted algebraic points | EXP-125 |
| \(F_6\) divisor reduction | quotient section \(U(B)X+V(B)\); principal-open residual \(Q_{18}(B)Q_{30}(B)=0\): 48 normalized values, 144 lifted algebraic points | EXP-126 |
| complete \(T_B\) restriction cover | \(d=0\) quotient cover plus exact \(G,L,Q\) weighted-open covers | EXP-118/120/121 |
| lower-family grading | \(w_{p,q}=q-p+1\pmod9\) for all 23 nonconstant remaining directions | EXP-106 |
| properness instrument | exact resultant-leading-coefficient test | EXP-014 |
| equivariant classification | EXP-010 on opposite-sign/one-zero scope; Shaska covers all signatures with triangular same-sign controls | 2026-07-25 reconciliation |

Cancelled EXP-093 size facts:

$$
(\binom{51}{1}+\binom{52}{2})165=227{,}205
$$

unknowns through degree two, and

$$
(\binom{51}{1}+\binom{52}{2}+\binom{53}{3})165=4{,}092{,}495
$$

through degree three. The order-four target block alone contains

$$
\binom{54}{4}\cdot125=39{,}531{,}375
$$

scalar conditions before exploiting sparsity.

## 3. Experiment index

- EXP-001 through EXP-066: see
  [`wiki/05-experiments.md`](../../problems/algebraic-geometry/jacobian-conjecture/wiki/05-experiments.md)
  and the individual verdicts.
- EXP-067: degree-one full certificate system infeasible under its exact modular gate.
- EXP-068/069: obstruction calculus and degree-two vector decisions.
- EXP-070: retracted because of fractional modular conversion and overflow defects.
- EXP-071: repaired arithmetic; pair supports feasible.
- EXP-072: an infeasible degree-two triple support, conclusive only for that declared
  degree/support completeness claim.
- EXP-073: all degree-three triple supports feasible, a one-sided null superseded at the next
  tier by EXP-075's decisive obstruction.
- EXP-074: rational-denominator enlargement vacuous after clearing.
- EXP-075: decided. The original blocker-first artifact and a targeted 2026-07-25 rerun agree:
  index 2662, support $\{(0,3),(1,0),(3,4),(4,7)\}$, is infeasible over both primes.
  Therefore no global degree-three polynomial covector exists. Stop at the hit.
- EXP-076/077/082: C13 forcing corrected and then located as already excluded in GGV.
- EXP-078: no justified finite certificate ceiling.
- EXP-079: unrun; flat-connection formulation retired as undefined.
- EXP-080: natural `sl2` premise refuted at the invariant gate; no commutators run.
- EXP-081: unrun; collision projection retired without a typed map.
- EXP-083/084/085: source frontier transcribed; EXP-085 has no pre-run
  `hypothesis.md`, so its candidate inference is not a complete experiment
  record.
- EXP-086 through EXP-090: incidence/recognition mechanism excluded in dimension two for its
  declared family.
- EXP-091: LND and line-fibre route mapped for genuine Keller pairs.
- EXP-092: unrun and on hold because $D_P(Q)=x^2$ in the reduced family.
- EXP-093: cancelled because EXP-075 proves that its degree-three target is empty.
- EXP-094: exact source-identity audit confirmed that GGV2 Remark 2.32 excludes
  none of C10, C11, C19, or C20. C10/C11 have \(A'_0=(1,0)\), not \((2,1)\);
  C19/C20 have \(B_1=A_0=(6,15)\), not \((6,18+6k)\). The four cases remain
  unresolved, not validated.
- EXP-095: applicability confirmed at the original polynomial-pair stage and
  rejected at the final Laurent bracket-\(x^2\) stage. The exact open-component
  signature \((72,(16,56),(2,0),(11/2,14))\) is the first retained Newton
  \(D=72\) branch. This is source consistency, not an exclusion.
- EXP-096: the original degree-72 component has seven possible nonzero
  Lee--Li inner vertices. The original pair satisfies
  \(\deg_x\operatorname{Res}_y(P,Q)=21\), with 84 major and 24 minor roots.
  These are necessary rejection gates; the open chain remains unresolved.
- EXP-097: exact resultant identities show that Laurent localization forgets
  the absolute \(x=0\) order and final inversion reflects exponent intervals
  by \(s\mapsto1536-s\). Degree \(21\) remains an original-pair
  reconstruction gate, not a direct condition on the 51 reduced coefficients.
- EXP-098: a pure principal-open certificate cover is equivalent to a global
  covector; specialization-only syzygies make constructible strata strictly
  stronger.
- EXP-099/100: common-strict-flag shortcuts are refuted; the first genuine
  interior interaction is \((0,1),(1,7)\).
- EXP-101: first two-parameter minor factored exactly, alternative chart
  constructed, and residual rational curve derived.
- EXP-102/103: third point-chart constructed; dense pullback retired; NTT
  determinantal-divisor engine isolates the exact endpoint issue.
- EXP-104: exact 100-point interpolation proves determinant support
  \([1628,1646]\), and two endpoint-controlled minors have gcd one.
- EXP-105: the compact exact cover is
  \(F(z)=21-96z-1024z^2\), \(G(z)=(8z+1)^{14}\), with integer Bezout
  constant \(17^{14}\).
- EXP-106: all nonconstant remaining lower directions preserve the connected
  mod-9 grading; \((0,7)\) is promoted to EXP-107.
- EXP-107: the first two bivariate charts have a zero-dimensional common
  locus modulo \(998244353\). It consists of the squarefree degree-12 fiber
  cut out by the first chart over \(z=-1/8\).
- EXP-108: the first deterministic point chart closes the modular fiber, and
  29 exact determinant evaluations plus independent controls lift the result.
  The exact \(Q,H\) have gcd one and an integer Bezout identity, proving the
  three-chart cover over characteristic zero.
- EXP-109: declared lift through \((0,6)\), using
  \(x=\varepsilon_{(0,6)}/u^2\) and the new term \(zxA_{(0,6)}\).
- EXP-110: generic \(124/125\) profile observed, but the persisted script and
  interpretation are superseded by EXP-111.
- EXP-111: the constant \(Q\)-column makes rank \(M\leq124\) structural; the
  complete row union has 302 rather than 289 rows. Generic-open inconsistency
  is exact from EXP-059's pinned augmented minor. The exceptional augmented
  determinantal locus remains open.
- EXP-112: exact SCC decomposition compresses the selected determinant to a
  36-column, 24-parameter cyclic block and three forced singleton factors.
- EXP-113: forced removal does not split the core; two explicit triples each
  generate full 36-vertex connectivity.
- EXP-114: exact triple determinants factor compactly. \(T_A\) cancels
  \((2,9)\) identically; \(T_B\) exposes the shifted weighted geometry
  \((7,3,9)\).
- EXP-115 through EXP-117: the open residual components and boundary kernel
  are isolated; the quotient boundary residual is reduced to nine invariant
  points plus \(b=0\).
- EXP-118: an exact \(C a^{107}\) alternative minor, the selected
  \(b^{95}\) axis chart, and the origin rank gap close the complete \(d=0\)
  quotient plane.
- EXP-119: a first exact weighted-open alternative determinant intersects
  each of \(G,L,Q\) in a finite proper scheme.
- EXP-120: a third exact chart closes the \(G\) component. The \(L\) and
  \(Q\) common residuals remain zero-dimensional.
- EXP-121: one shared residual-selected basis closes both \(L\) and \(Q\)
  exactly. The accepted run completes in 44.57 seconds; two quantitative
  predictions (first-four-prime coverage and at most ten replacements) are
  explicitly refuted.
- EXP-122: the free-lift prediction is refuted for all 21 restored
  directions. The exact activity audit isolates the linear \((2,j)\) ladder
  and promotes \((2,9)\).
- EXP-123: \((2,9)\) is affine over the complete symbolic \(A,B\) chart.
  The accepted exact run completes in 131.86 seconds and reduces the selected
  exceptional set to a rational graph plus finite base locus.
- EXP-124: an exact alternative chart covers a dense open of the graph and
  leaves the three factors \(F_3,F_6,F_7\).
- EXP-125: all three factor curves retain sampled rank \(124/125\) and expose
  cross-prime new bases. Exact recursion reduces \(F_3\) to the finite
  \(Q_9Q_{15}\) residual on \(AS\ne0\).
- EXP-126: the exact \(F_6\) quotient section is nonzero. Its independently
  checked degree-74 norm leaves only the degree-18 and degree-30 factors on
  \(AS\ne0\), a finite set of 48 normalized values / 144 lifts.
- EXP-102: third chart exists at \(u=1\); complete pullback is inconclusive
  after the dense rank-121 determinant hit its five-minute budget.

## 4. In flight

- No Jacobian experiment process is active.
- EXP-098 through EXP-101 are complete and exact. EXP-102 is closed
  inconclusive for global curve coverage, with an exact third-chart checkpoint
  at \(u=1\).
- EXP-075 remains stopped after a conclusive reproduced hit. Its verdict and
  both artifacts are persisted.
- EXP-111 through EXP-126 are complete. No Jacobian process is active.
- Current research branch: `work/jacobian-conjecture/next-round`.
- EXP-096 was merged into `develop` by PR `#81` at `7866b0f`.
- The planar manuscript reconciliation was merged by PR `#83` at `ffc6a3d`.
  Paper B v0.15 is published at `10.5281/zenodo.21584243`.
- EXP-097 and Paper B v0.16 were merged by PR `#85` at `d47937a`.
  Paper B v0.16 is published at `10.5281/zenodo.21589334`.
- Paper B v0.17, including EXP-098 through EXP-102, is published at
  `10.5281/zenodo.21593235` under concept DOI
  `10.5281/zenodo.21503367`.
- EXP-107/108 and Paper B v0.19 were merged by PR `#90` at `2481d3a`.
  Paper B v0.19 is published at `10.5281/zenodo.21610744`.
- Paper B v0.20, including EXP-111 through EXP-114, is published at
  `10.5281/zenodo.21694807` under concept DOI
  `10.5281/zenodo.21503367`.
- Paper B v0.21, including EXP-115 through EXP-117, is published at
  `10.5281/zenodo.21695367` under the same concept DOI.
- EXP-110 through EXP-114 and Paper B v0.20 were merged into `develop` by
  PR `#92` at `9e039e1`.
- EXP-115 through EXP-117 and Paper B v0.21 were merged into `develop` by
  PR `#93` at `b57a9b7`.
- EXP-121 is committed and pushed on the active research branch at
  `cada7fb`.
- EXP-118 through EXP-120 and Paper B v0.22 were merged into `develop` by
  PR `#95` at `68ec8d3`. Paper B v0.22 is published at
  `10.5281/zenodo.21696190` under concept DOI
  `10.5281/zenodo.21503367`.
- EXP-121 and Paper B v0.23 were merged into `develop` by PR `#97` at
  `d55798f`. Paper B v0.23 is published at
  `10.5281/zenodo.21697928` under the same concept DOI.
- EXP-122/123 and Paper B v0.24 were merged by PR `#99` at `646911b`.
  Paper B v0.24 is published at `10.5281/zenodo.21698923` under concept DOI
  `10.5281/zenodo.21503367`.
- EXP-124/125 and Paper B v0.25 were merged by PR `#101` at `f28c5a2`;
  DOI PR `#102` merged at `d51c1ae`. Paper B v0.25 is published at
  `10.5281/zenodo.21711580`.
- Promotion PR `#103` synchronized the validated tree to `main`. Exact
  current pointers must be verified live rather than copied from this file.
- The management mirror is updated directly on its canonical `develop`
  checkout. Do not create a management worktree or task branch.

## 5. Next actions, in order

1. Preserve EXP-125/126 as complete. The graph residual is the curve \(F_7\),
   the finite \(Q_9Q_{15}\) set on \(F_3\), the finite \(Q_{18}Q_{30}\) set
   on \(F_6\), the finite base locus, and the separate divisor \(A=0\).
2. Declare EXP-127 on \(F_7\). Reuse its distinct persisted cross-prime
   basis, reconstruct its exact determinant, reduce first on \(Y=-R/S\) and
   then modulo \(F_7(X,B)\), and compute the exact norm in \(B\). Stop at a
   finite residual; do not launch a generic Groebner basis.
3. If the \(F_7\) basis exceeds the exact block budget, select another
   persisted divisor section or combine modular norm gcds before redirecting.
4. Cover the finite \(F_3/F_6\) and \(V(R,S)\) points by algebraic charts;
   keep \(A=0\) as a separate boundary experiment.
5. Keep the complete EXP-118--121 \(T_B\) cover as a regression gate. Do not
   add redundant charts to the closed three-parameter restriction.
6. Reopen intersection-\(21\) transport only with a complete
   boundary-divisor ledger through the swap, Laurent cuts, and final inversion;
   do not impose absolute degree directly on the 51 coefficients.
7. Pursue further Newton resolution only if a new condition is derived beyond
   the already-retained first \(D=72\) branch; do not repeat direct comparisons
   with \(P_T\).
8. Continue the independent [125,150] frontier:
   - keep C10/C11/C19/C20 unresolved by GGV2 Remark 2.32;
   - derive the 16 missing \(A'_0\) values through the declared chain algorithm;
   - preserve C01/C04 as open absent an exact exclusion.
9. Keep the recursive graph-cover computation as P0 while it reduces
   dimension exactly. Do not build EXP-093.
10. Keep EXP-109 as a bounded regression control, not as the main route.
11. Paper B v0.26 is triggered by EXP-126. Publish it as a Zenodo new version;
   preserve immutable DOI `10.5281/zenodo.21711580` for v0.25.

Suggested source-round commands:

```powershell
git status --short
rg -n "C10|C11|C19|C20|A'_0|B_1" problems/algebraic-geometry/jacobian-conjecture program/jacobian-conjecture
rg -n "Makar|Lee-Li|approximate root|intersection" problems/algebraic-geometry/jacobian-conjecture/context
```

Before any new run:

```powershell
python scripts/check_research_structure.py
python -m pytest -q
```

Use the exact commands exposed by current scripts if these guard names have changed.

## 6. Where everything lives

- Program control:
  `program/jacobian-conjecture/`
- Primary problem record:
  `problems/algebraic-geometry/jacobian-conjecture/`
- Experiments:
  `problems/algebraic-geometry/jacobian-conjecture/experiments/EXP-*/`
- Source dossiers:
  `problems/algebraic-geometry/jacobian-conjecture/context/`
- Wiki:
  `problems/algebraic-geometry/jacobian-conjecture/wiki/`
- Append-only history:
  `problems/algebraic-geometry/jacobian-conjecture/history/log.md`
- Shared code:
  `problems/algebraic-geometry/jacobian-conjecture/code/jclib/`
- Manuscripts:
  `manuscripts/jacobian-conjecture/{foundational,planar,cascade}/`
- Management mirror:
  `plans/caos-research/jacobian-conjecture/` in `CAOS_MANAGE`

Latest correction publications:

- Paper A v0.11: `10.5281/zenodo.21579022`
- Paper B v0.16: `10.5281/zenodo.21589334`
- Paper B v0.17: `10.5281/zenodo.21593235`
- Paper B v0.19: `10.5281/zenodo.21610744`
- Paper B v0.20: `10.5281/zenodo.21694807`
- Paper B v0.21: `10.5281/zenodo.21695367`

EXP-097 changed the admissible use of intersection number \(21\), so the planar
manuscript was expanded, built, visually verified, merged through PR `#85`,
and published as Zenodo v0.16.

## 7. Gotchas, gates, and lenses

Gotchas:

- Never convert a rational coefficient with `int(Fraction)` before modular reduction. EXP-070
  was retracted for this defect.
- Fraction-field row reduction is generic-only unless denominators and exceptional strata are
  handled.
- A finite polynomial covector is sufficient, not known necessary.
- Feasible support ansatzes do not prove full-system feasibility.
- A theorem for $[f,g]=1$ does not automatically apply to $[P,Q]=x^2$.
- Syzygy modules and kernels can jump after parameter specialization.
- Principal-open localized global syzygies do not by themselves enlarge the
  global-covector class; closed specialization strata are essential.
- Dense determinant expansion is retired for EXP-102's rank-121 curve
  pullback. Use the polynomial determinantal divisor instead.
- Do not use the 289-row forced-only list as the complete family system.
- Rank \(124\) is structurally forced by the constant \(Q\)-column; it is not
  evidence of a new nontrivial covector.
- Do not compute all \(125\)-minors of \(M\). They vanish trivially.
- Dependency-graph edges can cancel from a determinant. EXP-114's
  \((2,9)\) direction is the exact control; use determinant support after SCC
  support.
- Do not implement EXP-093. Its target is empty.
- No floor raise until every GGHV branch and every free coefficient is covered.

Lenses ledger for this round:

- systematic exclusion: retained as the spine;
- invariant-first: the EXP-093 size count first forced a feasibility gate, then recovery of the
  existing EXP-075 hit cancelled the route entirely;
- Newton/valuation: recent integrality and polynomiality restrictions promoted;
- commutative algebra: certificate modules and finite chart covers replace the undefined
  connection analogy;
- global geometry: LND, fibres, and Jelonek held behind applicability bridges;
- parameter spaces: Jelonek's 2026 component theorem added as medium-term framing;
- adversarial validation: false two-sided, finite-ceiling, and support-completeness inferences
  explicitly withdrawn;
- external source sweep: Makar-Limanov, Trakhtenberg, Lee-Li, GGHV, and Jelonek recorded in the
  dated source audit.
- source-identity invariant: EXP-094 separated \(A_0\), \(A'_0\), \(B_0\), and
  \(B_1\), correcting four false exclusion candidates without heavy compute;
- self-questioning: the cheap frontier lookup did not shrink the four named
  cases, so further Heitmann matching is retired for them and the immediate
  \((72,108)\) campaign returns to the applicability bridge;
- exploration moment: endpoint identity is treated as a reusable source-audit
  invariant before any future corner-family comparison.
- 2026-07-29 invariant-first correction: the constant \(Q\)-column retires the
  EXP-110 maximal-minor target before heavy compute.
- 2026-07-29 graph-compression lens: use common acyclicity or strongly
  connected components of normalized augmented operators to reduce the
  51-parameter exceptional locus before exact elimination.
- 2026-07-29 cancellation audit: graph participation is necessary but not
  sufficient for determinant dependence.
- 2026-07-29 symmetry lens: the shifted \(T_B\) factors are weighted
  homogeneous with weights \((7,3,9)\), giving a weighted-projective
  open/boundary split for EXP-115.
