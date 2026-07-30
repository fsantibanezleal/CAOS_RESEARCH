# RESUME: Jacobian conjecture program

Updated 2026-07-29 after EXP-111's full-family rank audit. This is the first-read
navigation page. Primary artifacts and experiment verdicts remain the evidence.

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
- Controlling strategy:
  [`strategy-audit-2026-07-29.md`](strategy-audit-2026-07-29.md).
- Source audit:
  [`2026-07-25-strategy-source-audit.md`](../../problems/algebraic-geometry/jacobian-conjecture/context/2026-07-25-strategy-source-audit.md).

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
- EXP-102: third chart exists at \(u=1\); complete pullback is inconclusive
  after the dense rank-121 determinant hit its five-minute budget.

## 4. In flight

- No Jacobian experiment process is active.
- EXP-098 through EXP-101 are complete and exact. EXP-102 is closed
  inconclusive for global curve coverage, with an exact third-chart checkpoint
  at \(u=1\).
- EXP-075 remains stopped after a conclusive reproduced hit. Its verdict and
  both artifacts are persisted.
- EXP-111 through EXP-114 are complete. EXP-115 is the next round, but its
  hypothesis has not yet been written.
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
- No Jacobian PR or experiment process is active.
- The management mirror is updated directly on its canonical `develop`
  checkout. Do not create a management worktree or task branch.

## 5. Next actions, in order

1. Declare and run EXP-115 on the weighted \(T_B\) residual:
   - set \(a=\varepsilon_{(0,1)}\),
     \(b=\varepsilon_{(0,5)}\), and
     \(d=1+\varepsilon_{(1,0)}\);
   - split \(d\ne0\) from \(d=0\);
   - use weights \((7,3,9)\) to normalize the open chart;
   - select alternative minors using all 302 rows and compute exact gcd or
     residual ideals against \(G_{54}\) and \(H_{63}\).
2. Continue constructible determinant charts only from exact factor loci.
   Use EXP-101 through EXP-108 as regression controls.
3. Reopen intersection-\(21\) transport only with a complete
   boundary-divisor ledger through the swap, Laurent cuts, and final inversion;
   do not impose absolute degree directly on the 51 coefficients.
4. Pursue further Newton resolution only if a new condition is derived beyond
   the already-retained first \(D=72\) branch; do not repeat direct comparisons
   with \(P_T\).
5. Continue the independent [125,150] frontier:
   - keep C10/C11/C19/C20 unresolved by GGV2 Remark 2.32;
   - derive the 16 missing \(A'_0\) values through the declared chain algorithm;
   - preserve C01/C04 as open absent an exact exclusion.
6. Re-rank after steps 1 through 5. The admissible next choices are a source-derived
   restriction, a module/chart-cover computation, or a newly justified higher-degree
   structural probe. Do not build EXP-093.
7. Keep EXP-109 as a bounded regression control, not as the main route.
8. Update wiki or manuscripts only when an adjudicated result changes a mathematical claim.

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
