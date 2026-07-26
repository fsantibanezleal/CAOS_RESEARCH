# RESUME: Jacobian conjecture program

Updated 2026-07-26 after EXP-097's resultant-transport typing gate. This is the first-read
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
- EXP-102 proves a third minor is nonzero at \(u=1\) on that residual curve,
  but complete curve coverage remains open.
- Controlling strategy:
  [`strategy-audit-2026-07-25.md`](strategy-audit-2026-07-25.md).
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
| reduced linear system | $M(\varepsilon)q=b$ with 125 output rows and 165 gauge directions | EXP-052 onward |
| global covector | $c^TM=0$ and $c^Tb\ne0$, sufficient for inconsistency | EXP-053 onward |
| certificate module target | left syzygies of $M$, their pairing ideal with $b$, and localized chart certificates | strategy audit |
| constructible certificate recursion | generic pairing opens followed by kernel recomputation on residual closed strata | EXP-098 |
| first GGHV minor stratum | \((st-8)^6(2^{15}s^9-(st-8)^7)/2^{39}\) on directions \((0,1),(1,7)\) | EXP-101 |
| residual curve | \(s=8u^7,\ t=(8u^9+1)/u^7,\ u\ne0\) | EXP-101 |
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
- EXP-102: third chart exists at \(u=1\); complete pullback is inconclusive
  after the dense rank-121 determinant hit its five-minute budget.

## 4. In flight

- No Jacobian experiment process is active.
- EXP-098 through EXP-101 are complete and exact. EXP-102 is closed
  inconclusive for global curve coverage, with an exact third-chart checkpoint
  at \(u=1\).
- EXP-075 remains stopped after a conclusive reproduced hit. Its verdict and
  both artifacts are persisted.
- Current research branch: `work/jacobian-conjecture/next-round`.
- EXP-096 was merged into `develop` by PR `#81` at `7866b0f`.
- The planar manuscript reconciliation was merged by PR `#83` at `ffc6a3d`.
  Paper B v0.15 is published at `10.5281/zenodo.21584243`.
- EXP-097 and Paper B v0.16 were merged by PR `#85` at `d47937a`.
  Paper B v0.16 is published at `10.5281/zenodo.21589334`.
- Paper B v0.17, including EXP-098 through EXP-102, is published at
  `10.5281/zenodo.21593235` under concept DOI
  `10.5281/zenodo.21503367`. Its research PR is the current close-out action.
- No Jacobian PR or experiment process is active.
- The management mirror is updated directly on its canonical `develop`
  checkout. Do not create a management worktree or task branch.

## 5. Next actions, in order

1. Compute the residual-curve determinantal divisor:
   - clear Laurent powers after
     \(s=8u^7,\ t=(8u^9+1)/u^7\);
   - compute modular Smith/determinantal-divisor data for the full augmented
     polynomial matrix;
   - reconstruct over \(\mathbb{Q}[u]\);
   - a monomial divisor closes this exact two-parameter slice, while a
     nonmonomial divisor names every residual value.
2. Lift the constructible recursion to the next coefficient block only after
   the two-parameter slice is closed and independently checked.
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
7. Update wiki or manuscripts only when an adjudicated result changes a mathematical claim.

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
