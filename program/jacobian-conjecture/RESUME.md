# RESUME: Jacobian conjecture program

Updated 2026-07-25 after the complete strategy and source audit. This is the first-read
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
- EXP-083/084/085: source frontier reduced; C10/C11/C19/C20 and 16 unprinted forcings
  remain exact source tasks.
- EXP-086 through EXP-090: incidence/recognition mechanism excluded in dimension two for its
  declared family.
- EXP-091: LND and line-fibre route mapped for genuine Keller pairs.
- EXP-092: unrun and on hold because $D_P(Q)=x^2$ in the reduced family.
- EXP-093: cancelled because EXP-075 proves that its degree-three target is empty.

## 4. In flight

- No Jacobian experiment process is active.
- EXP-075 is stopped after a conclusive reproduced hit. Its verdict and both artifacts are
  persisted.
- Current research branch: `work/jacobian-conjecture/next-round`.
- Research PR: `#74`, branch into `develop`.
- Current management branch: `docs/jacobian-scope-reconciliation`.
- Management PR: `#482`, branch into `develop`.
- Do not merge either PR until this audit round passes the repository guards and both diffs are
  reviewed.
- The unrelated diffusion checkpoint is preserved separately on
  `fix/diffusion-two-counterexamples`; do not mix it into the Jacobian PR.

## 5. Next actions, in order

1. Complete the cheap source frontier:
   - C10/C11 against Heitmann Theorem 2.25;
   - C19/C20 against the published $B_1$ table;
   - derive the 16 missing $A'_0$ values;
   - preserve C01/C04 as open absent an exact exclusion.
2. Declare the Newton-resolution applicability experiment. Translate the original Keller
   component through the GGHV reductions and decide which Makar-Limanov/Trakhtenberg hypotheses
   survive. Do not compare polygons visually and infer a contradiction.
3. Declare a Lee-Li plus approximate-root applicability experiment on the same transformation.
4. Declare a small certificate-module/chart-cover experiment:
   - left syzygy module;
   - pairing ideal;
   - localized certificates;
   - radical cover;
   - specialization controls.
5. Re-rank after steps 1 through 4. The admissible next choices are a source-derived
   restriction, a module/chart-cover computation, or a newly justified higher-degree
   structural probe. Do not build EXP-093.
6. Update wiki or manuscripts only when an adjudicated result changes a mathematical claim.

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
- Paper B v0.14: `10.5281/zenodo.21579025`

No publication action is triggered by this strategy audit because it changes the work plan, not
an adjudicated manuscript theorem.

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
