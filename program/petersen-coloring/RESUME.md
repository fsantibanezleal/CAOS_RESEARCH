# petersen-coloring: RESUME (zero-loss handoff)

Updated 2026-09-18 evening (round 2: EXP-007 to EXP-010; round 1 closed 2026-09-03). First read for
any fresh session, per methodology 07. Derived view: on conflict, experiment verdicts win.

## 1. State in one screen

The problem. `P` is the Petersen graph. A Petersen coloring of a cubic graph `G` is a map
$\sigma: E(G) \to E(P)$ such that for every vertex $v$ of $G$ there is a vertex $w$ of $P$ with
$\sigma(\partial_G(v)) = \partial_P(w)$. Jaeger 1988 conjectured every bridgeless cubic graph has
one; equivalent to a normal 5-edge-coloring (Jaeger 1985). It implied Berge-Fulkerson and the
5-cycle double cover conjecture.

Status. FALSE since August 2026. Five retrievable counterexamples: `G112`, `H112` (Putman),
`G52`, `G52b` (Goedgebeur et al.; House of Graphs 57244, 57278), `G68` (House of Graphs 57280).
arXiv:2608.10028v3 (2026-09-11): smallest counterexample has order in $[40, 52]$; it reports for
the five graphs Berge-Fulkerson covers, perfect matching index at most 4, 5-cycle double covers,
strong normal 6-edge-colorings, colorings with two abnormal edges (overlap with round 1, obtained
independently; round 1 is dated 2026-09-03), and asks whether the 52-vertex graphs are colorable
only by themselves.

CAOS results (every negative a drat-trim-verified DRAT proof, every positive a witness re-verified
from the graph alone; `[D]` = proved here):

- Round 1 (EXP-001 to EXP-006) on `G112`, `H112`, `G52`: independent certification; perfect
  matching index 4; 5-CDC; 5-flow, no 4-flow; oddness 4, 4, 2; resistance 3, 3, 2; normal chromatic
  index 6; parity theorem `[D]` (the number of bad vertices of an edge map into `P` is never 1);
  Petersen defect exactly 2 with EVERY vertex pair critical; pure-`F` proposition `[D]`.
- EXP-008 CONFIRMED: `G52b` and `G68` have exactly the invariants of `G52` (index 4, oddness 2,
  resistance 2, normal chromatic index 6, defect 2, all 1,326 and 2,278 pairs critical). Universal
  2-criticality now holds on all five graphs (17,362 pair witnesses).
- `pd <= ab` `[D]` (Petersen defect at most the least number of abnormal edges of a proper
  5-edge-coloring); with the parity theorem it reproves Proposition 3 of Mattiolo, Mazzuoccolo,
  Mkrtchyan 2021 (`ab` is never 1). `pd = ab = 2` on all five graphs.
- Rings and frames `[D]` (`context/2026-09-18-defect-unbounded.md`): `t` counterexamples opened at
  an edge and joined cyclically, or a cubic frame with vertices replaced by counterexamples minus
  a vertex, have a bad vertex in every block, so `ab >= pd >= t`. Same constructions as in
  Mattiolo et al., stronger conclusion. Consequence: no sublinear bound on `ab` for 2-connected
  or 3-connected cubic graphs; statements (a) to (d) of their Conjecture 3 are false; the
  conjecture now equals the falsity of (e) (cyclically 4-edge-connected class). Threshold
  proposition `[D]`: ONE cyclically 4-edge-connected cubic graph with `pd >= 3` refutes (e).
- EXP-009 CONFIRMED: `pd(R_2) = 2`, `pd(R_3) = 3`, `pd(R_4) = 4`, `pd(K_4[G52]) = 4`, one bad
  vertex per block; 20 same-block relaxations of `R_2` refuted; `2 <= ab(R_2) <= 4`, other `ab`
  values undecided.
- EXP-010 (see section 4 for its state): every 4-pole `G - e1 - e2` of `G52`, `G52b`, `G68` is
  Petersen colorable (482, 482, 4,947 orbit representatives), boundary patterns only "crossed" or
  "four edges around an edge"; ten dot products `G52 . G52` (102 vertices) are NEW counterexamples
  with checked proofs, all with `pd = 2`; distance sets at a deleted edge always contain 1.
- EXP-007 (H-colorings by an unknown target): Lemma A `[D]` (all fibers of the vertex map have
  the same parity), Lemma B `[D]` (unused target vertices reduce to at most one, splitting
  lemma); reduced encoding agrees with the unreduced one on 21 controls. Decided orders: section 4.

Key formulas. Fiber parity: $f^{-1}(xy)$ is a perfect matching of
$G[\varphi^{-1}(x) \cup \varphi^{-1}(y)]$, so $n_x \equiv n_y \pmod 2$. Transfer principle: a block
with only good vertices pushes a cut of $P$ onto its boundary labels,
$\sum_{v \in B} \chi_v = \sum_{e \in \partial B} \mathbf{1}_{\sigma(e)} \in \mathrm{Cut}(P)$.

## 2. The objects table

| Object | Definition | Owner |
|---|---|---|
| `G112`, `H112`, `G52`, `G52b`, `G68` | `data/*.edgelist`; digests in wiki 03 | EXP-001, EXP-007 P0 |
| `F` (= `W` in v3) | Petersen minus two adjacent vertices | `pcclib.compose` |
| `H`-coloring, fibers, kinds (O), (E0), (E1) | `context/2026-09-18-hcoloring-reduction-lemmas.md` | EXP-007, `pcclib/hcolor.py` |
| `pd`, `ab`, rings `R_t`, frames `K[G]` | `context/2026-09-18-defect-unbounded.md` | EXP-009, `pcclib/graphs.py` (`ring_join`, `frame_substitution`) |
| 4-poles `M(G; e1, e2)`, boundary patterns, `Dist(e0, e)` | EXP-010 hypothesis and addenda | EXP-010 `run.py`, `run_dist.py`, `run_dot.py` |
| classes modulo the cut space | 64 classes, six orbits | `code/probes/classes_mod_cut_space.py` |

## 3. Experiment index

| EXP | Question | Verdict | Load-bearing output |
|---|---|---|---|
| 001 to 006 | round 1 | see round-1 rows in `wiki/README.md` | certification, audit, parity theorem, defect 2 |
| 006 add. 4 | normal-5 defect of `G52` | PASS | 42 refuted edges meet all 14 edge orbits; two-abnormal-edge witnesses; lower bound is also MMM Prop. 3 |
| 007 | is a 52-vertex counterexample colored by a smaller bridgeless cubic graph? | see section 4 | Lemmas A, B; certified refuted orders; `G52` in `H_3` given v3 Observation 9 |
| 008 | battery on `G52b`, `G68` | CONFIRMED | same invariants as `G52`; all pairs critical |
| 009 | defect of rings and frames | CONFIRMED (`ab` undecided) | `pd` = number of blocks on four instances |
| 010 | non-colorable 4-poles, statement (e) | see section 4 | all 4-poles of three graphs colorable; threshold proposition; dot products |

## 4. In flight (2026-09-18 evening)

EXP-007, all with `experiments/EXP-007-colorable-only-by-itself/run_inc.py` (worktree `.venv`,
python-sat), results `artifacts/result-<graph>-k<k>.json`, formulas and proofs under
`E:/_Datos/caos-research/petersen-coloring/EXP-007/`:

- `G52`: refuted with verified proofs: 2, 4, 30 to 50. Orders 26 and 28 hit the 6-hour limit
  during the proof check; their complete proofs are on disk and are being checked post hoc by
  `certify_existing.py --graph G52 --k 26` (and 28); logs `artifacts/certify-G52-k*.log`. Orders 6
  to 24 run until their own limits; when a runner dies during certification its WSL solver keeps
  writing the proof, which `certify_existing.py` can check afterwards.
- `G52b`: refuted: 44 to 50. Order 42: external solve with proof in progress (in-process UNSAT
  after 14,448 s); order 40: `--suffix=-long --cap 86400` run in progress
  (`artifacts/run-G52b-k40-long.log`, result `result-G52b-k40-long.json`). Orders below 40 were
  stopped undecided (not needed for the conditional form).
- `G68`: refuted: 64, 66; orders 62 down to 40 running, five at a time
  (`artifacts/run-G68-k*.log`).
- Verdict forms fixed in addendum 5: (U) the list of refuted orders; (C) membership in `H_3`
  given Observation 9 of v3 (no counterexample below 40 vertices), which needs orders 40 to `n - 2`.
  `G52` is complete under (C). `G52b` needs 40 and 42.
- Incident (hypothesis, incident note): an orphaned attempt-1 driver ran old code for four hours
  into shared log files; no result file affected. Always list `xargs.exe` after stopping a fan-out.

EXP-010: H112 4-pole sweep (2,324 representatives, six workers, about 35 s each) was started at
15:16; the experiment's 6-hour budget ends at 17:43, when it is stopped and the verdict written;
`G112` (about 14,000 representatives) was not run.

Second manuscript (`manuscripts/petersen-coloring/colorable-only-by-itself/`, parts +
`assemble.py` + `make_tables.py`): draft complete, waits for `G52b` orders 40 and 42; then
`make_tables.py`, fill `%%EXTRA_ORDERS%%` in `results-theorem.tex`, `assemble.py`, reserve a DOI
(`_CAOS_MANAGE/tools/zenodo/reserve_doi.py petersen-coloring colorable-only-by-itself`), build,
attach, publish, vault metadata.

## 5. Next actions, ordered

1. Collect EXP-007 results; run `certify_existing.py` for every order whose proof is complete on
   disk; write `EXP-007/verdict.md` with both forms; update wiki 06 results table, the web page
   constants `h3En`, `h3Es`, this file.
2. Publish the second manuscript when `G52b` orders 40 and 42 are certified (or with `G52` alone
   if they fail).
3. PCR-7: a cyclically 4-edge-connected cubic graph with `pd >= 3` (threshold proposition). Ideas
   on file: superposition with connector label triples (class-only argument is insufficient, see
   the probe); boundary-pattern calculus PCR-9.
4. PCR-8: `G68`, then the probe `k = 52` for `G112`, `H112`.
5. Release step (version bump, bake, tag) belongs to the serialized release owner, not to this
   branch.

## 6. Where everything lives

| what | path |
|---|---|
| problem tree | `problems/combinatorics/petersen-coloring/` (data/, code/pcclib, code/probes, experiments/EXP-001..010, wiki/01-07, context/) |
| programme record | `program/petersen-coloring/` (plan, state, backlog, research lines with the round-2 exploration moment, this file) |
| heavy artifacts | `E:/_Datos/caos-research/petersen-coloring/` (sources incl. arxiv v3, mmsw, mmm-2104.09241, hog/, misc/; EXP-001..010 formulas and proofs) |
| manuscripts | `manuscripts/petersen-coloring/consequence-audit/` (v0.04 published, 10.5281/zenodo.22836612, concept 10.5281/zenodo.22285164); `colorable-only-by-itself/` (draft) |
| web page | `frontend/src/pages/PetersenColoring.tsx` (eight tabs; gate `_CAOS_MANAGE/tools/visual-verify/_pcc-gate.mjs`) |
| management mirror | `_CAOS_MANAGE/plans/caos-research/petersen-coloring/` |
| vault manuscript metadata | `_CAOS_MANAGE/manuscripts/petersen-coloring/` |

## 7. Gotchas

- Work in the worktree `E:/_Temp/caos-research-newproblem` on `work/petersen-coloring/open`;
  the main checkout is another session's.
- A lazy-constraint search over an unknown structure needs a proof that the structure has no part
  unconstrained by the data (EXP-007 attempt 1: 2,000 cuts per order, no decision).
- G52b is 10 to 25 times harder than G52 for the same target order; G68 harder still.
- The proof check (drat-trim) dominates: a 0.9 GB proof takes more than three hours. The runner's
  watchdog kills Python at the limit but NOT the WSL solver or checker; use `certify_existing.py`.
- Stopping a background `xargs` job does not kill the driver on Windows: list `xargs.exe`, kill it
  first, check instance start times (`Get-CimInstance Win32_Process`).
- Five experiments on one machine turned many instances into timeouts; schedule heavy runs alone.
- Search the literature for the CONSTRUCTION, not only the statement: the ring and frame
  constructions and `ab != 1` were already in Mattiolo-Mazzuoccolo-Mkrtchyan 2021.
- Shell heredocs mangle backslashes; write LaTeX, TSX and Python containing backslashes with the
  file tools, and assemble LaTeX from part files (`assemble.py`), never through shell strings.
- Another session publishes manuscript versions of this problem too (author-name release made
  v0.03); always `git fetch` and check the vault ledger before choosing a version number.
- Solver UNSAT without a checked DRAT is not a theorem here.
