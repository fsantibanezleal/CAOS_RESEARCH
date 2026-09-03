# petersen-coloring: RESUME (zero-loss handoff)

Updated 2026-09-03 (round 1, six experiments). First read for any fresh session, per methodology
07. Derived view: on conflict, experiment verdicts win.

## 1. State in one screen

The problem. `P` is the Petersen graph. A Petersen coloring of a cubic graph `G` is a map
$\sigma: E(G) \to E(P)$ such that for every vertex $v$ of $G$ there is a vertex $w$ of $P$ with
$\sigma(\partial_G(v)) = \partial_P(w)$. Jaeger 1988 conjectured every bridgeless cubic graph has
one; Jaeger 1985: equivalent to a normal 5-edge-coloring [V via the 2026 papers]. It implied
Berge-Fulkerson and the 5-cycle double cover conjecture [V].

Status. FALSE since August 2026: Putman's `G112`, `H112` (arXiv:2608.10012, Zenodo 21845291),
Jooken's human-checkable proof (arXiv:2608.10028), GJMMM's `G52` and infinite families (Zenodo
21933786); smallest counterexample in $[38, 52]$; a 68-vertex graph on X is not retrievable [U].

CAOS results (all exact; every negative a drat-trim-verified DRAT proof, every positive a witness
re-verified from the graph alone):

- EXP-001 CONFIRMED: independent encodings refute all three graphs (Petersen and normal-5);
  controls pass; Putman's proofs verify; cyclic edge connectivity exactly 4.
- EXP-002 CONFIRMED: Berge-Fulkerson, Berge-5, Fan-Raspaud hold on all three; perfect matching
  index exactly 4 (Petersen graph: 5).
- EXP-003 CONFIRMED: 5-cycle double covers and nowhere-zero 5-flows on all three; no 4-flows;
  oddness 4, 4, 2; resistance 3, 3, 2 (our oddness-2 prediction refuted on the 112s).
- EXP-004: normal 6 and strong normal 6 on all three, so $\chi'_N = 6$ exactly; cardinality-
  encoded defect ladders stalled at bound 1 (30-minute cap): INCONCLUSIVE on defects.
- EXP-005: classes of `k` copies of `F` plus `m` free vertices; `(5,0)`, `(6,0)` exhausted by a
  universal coloring (Proposition: pure compositions of `F` are always colorable, [D]); `(3,2)`
  control and `(5,2)` did not converge in budget (CEGAR with one clause per coloring).
- EXP-006: Petersen defect. Parity THEOREM [D]: for any cubic graph and any edge map into `P`
  the number of bad vertices is never exactly 1 (bad-set label vectors sum into the cut space of
  `P`; odd cuts of size 1 or 3 in `P` are stars). `G52`: all 52 singles UNSAT, all 1,326 pairs
  critical: defect exactly 2. `G112`, `H112`: all 6,216 pairs critical each: defect exactly 2 and
  universal 2-criticality on all three graphs (13,758 pair witnesses, bad set always the relaxed
  pair). The 78 edge relaxations of `G52` (normal-5 defect) were RUNNING at this update.

Key formula (oddness encoding): $\mathrm{oddness}(G) = \min_{M,\mathrm{col}} \#\{e \in E
\setminus M : \mathrm{col}(u_e) = \mathrm{col}(v_e)\}$ over perfect matchings $M$ and vertex
2-colorings.

## 2. The objects table

| Object | Definition | Owner |
|---|---|---|
| `G112`, `H112` | Putman's graphs, digests `dc16cc18...`, `0f2d8858...`; 12 disjoint copies of `F` plus 16 free vertices each | EXP-001, EXP-005 |
| `G52` | GJMMM appendix graph, 0-based digest `27db5d3b...`; 6 copies of `F` plus 4 free vertices | EXP-001, EXP-005 |
| `F` | Petersen minus two adjacent vertices; owners `[2,5,6,7]`; 8 semi-edge automorphisms; `PCOL_F` has 315 boundary tuples | `pcclib.compose` |
| `C(k,m)` | cubic graphs from `k` copies of `F` and `m` free vertices | EXP-005 |
| Petersen defect | least number of bad vertices over all edge maps | EXP-006 |
| critical pair | pair of vertices at which a map may fail while valid elsewhere | EXP-006 |

## 3. Experiment index

| EXP | Question | Verdict | Load-bearing output |
|---|---|---|---|
| 001 | independent certification | CONFIRMED | 9 verified refutations; controls; public proofs verified |
| 002 | perfect matching covers | CONFIRMED | BF, Berge-5, FR hold; index 4 |
| 003 | double covers, flows, oddness, resistance | CONFIRMED (oddness prediction refuted) | 5-CDC, 5-flow; oddness 4/4/2; resistance 3/3/2 |
| 004 | normal 6, defects | normal 6 CONFIRMED; defects INCONCLUSIVE | $\chi'_N = 6$ on all three |
| 005 | compositions of `F` below 52 | partial: `(5,0)`, `(6,0)` exhausted; `(5,2)`, `(6,2)` budget | pure-F proposition; CEGAR non-convergence measured |
| 006 | critical vertices and pairs | CONFIRMED as redirected (P1, P2 refuted by theorem) | parity theorem; defect 2 on all three; all three universally 2-critical |

## 4. In flight

- EXP-006 edge relaxations of `G52` (`run.py --skip-vertices`, log `artifacts/run-edges-G52.log`,
  13 of 78 UNSAT at this update); pair sweeps complete.
- EXP-005 classes `(5,2)`, `(6,2)` under their 2-hour budgets (`run.py --skip-controls --classes`).
- EXP-004 last instance (`G52_pdef_1`, cardinality bound 1, expected UNSAT or timeout).

## 5. Next actions, ordered

1. Close EXP-004, EXP-005, EXP-006 verdicts from their manifests; wiki 04/05 already carry the
   decided rows.
2. Manuscript v0.01 (`manuscripts/petersen-coloring/consequence-audit/main.tex`): fill the
   remaining sentence on EXP-005 (`PENDING005`), rebuild twice, visual QA, then the vault
   prereserve flow: `python tools/zenodo/reserve_doi.py petersen-coloring consequence-audit`,
   print the DOIs in the header, rebuild, `attach_pdf.py`, `publish_manuscripts.py`.
3. Open the PR `work/petersen-coloring/open -> develop`; do not bump the version or bake.
4. Next round: PCR-4b (symmetry-broken composition search), PCR-1/2 (families), PCR-3
   (critical-pair structure: distance profile of pairs; which pairs are critical in the 112s).

## 6. Where everything lives

| what | path |
|---|---|
| problem tree | `problems/combinatorics/petersen-coloring/` (data/, code/pcclib, experiments/EXP-001..006, wiki/01-05, context/) |
| programme record | `program/petersen-coloring/` (plan, state, backlog, research lines, this file) |
| scouting record | `problems/combinatorics/petersen-coloring/context/scouting-2026-09/` |
| external evidence and heavy artifacts | `E:/_Datos/caos-research/petersen-coloring/` (sources, EXP-001..006 CNFs and proofs, web-gate screenshots) |
| manuscript | `manuscripts/petersen-coloring/consequence-audit/` |
| web page | `frontend/src/pages/PetersenColoring.tsx` (gate `_CAOS_MANAGE/tools/visual-verify/_pcc-gate.mjs`: 24 shots, pass) |
| management mirror | `_CAOS_MANAGE/plans/caos-research/petersen-coloring/` |
| vault manuscript metadata | `_CAOS_MANAGE/manuscripts/petersen-coloring/` |

## 7. Gotchas

- Work in the worktree `E:/_Temp/caos-research-newproblem` on `work/petersen-coloring/open`;
  the main checkout is another session's.
- Putman's Zenodo DOI in GJMMM's reference list is v1.0.0 (`21819153`); the graphs are unchanged
  in v1.1.0 (`21845291`). GJMMM's concept record `21933785` has no API entry; the version record
  is `21933786`.
- Two poles are both called `C` in the two papers (claw six-pole vs trimmed-K4 4-pole).
- Normal-5 instances of the 112-vertex graphs take 15 to 25 minutes with proofs near 0.8 GB;
  the Petersen encoding with symmetry breaking is 20 to 40 times cheaper.
- Cardinality-encoded defect bounds are hard for the solver; designated relaxation (one unit at
  a time) is fast. Single-vertex relaxation is pointless: the parity theorem decides it.
- CEGAR composition search does not converge at 26 semi-edges; do not rerun it unchanged.
- Shell heredocs mangle backslashes and split literals; write LaTeX and Python through the file
  tools, never through inline shell strings.
- Solver UNSAT without a checked DRAT is not a theorem here.
