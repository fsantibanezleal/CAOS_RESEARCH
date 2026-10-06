# petersen-coloring: RESUME (zero-loss handoff)

Updated 2026-10-06 (round 3: sync, methodology 13, publications, focus PCC-F6; EXP-013 and EXP-014 closed). First read for any
fresh session, per methodology 07. Derived view: on conflict, experiment verdicts win; the
strategic record is `research-governance.json` and `manuscript-map.md` in this folder.

## 1. State in one screen

The problem. `P` is the Petersen graph. A Petersen coloring of a cubic graph `G` is a map
$\sigma: E(G) \to E(P)$ sending every vertex star onto a vertex star. Jaeger's conjecture (1988)
that every bridgeless cubic graph has one is FALSE since August 2026 (Putman; Goedgebeur, Jooken,
Máčajová, Mattiolo, Mazzuoccolo, Ulyanov, arXiv:2608.10028, latest v4 of 2026-09-30; a 68-vertex
graph posted on X). CAOS does not claim the disproof (governance record, `prohibited_reframing`).

Published CAOS manuscripts (all Zenodo, CC BY 4.0, not peer reviewed):

| manuscript | version | DOI | result |
|---|---|---|---|
| consequence-audit | v0.06 (2026-10-06) | 10.5281/zenodo.23195171 | five graphs: covers, index 4, 5-CDC, flows, oddness, resistance, normal 6, parity theorem, defect 2 with all pairs critical, abnormal edges, statements (c), (d) false, Theorem 5.9 |
| unbounded-defect | v0.02 (2026-10-06) | 10.5281/zenodo.23196817 | statement (e) of the Mattiolo-Mazzuoccolo-Mkrtchyan conjecture false (rings on 102t vertices, defect at least t, `pd(R_3) = 3`); Section 6: transfer semigroups of 6-poles, every ring of claws and Petersen superedges colorable |
| colorable-only-by-itself | v0.01 (2026-10-06) | 10.5281/zenodo.22859075 | both 52-vertex counterexamples are colorable only by themselves (members of H_3), answering v4 Section 5.4 |

Focus record (strategic review 2026-10-06): F0, F1, F3, F4 closed; F2 dormant; F5 gated (G68 and
the unconditional H_3 form); **F6 active**: cut-space charges and cyclically 5-edge-connected cubic
graphs (Problem 11 of v4), first bounded action EXP-013.

The charge formulation (`context/2026-10-06-charges.md`): `q(v)` = class of the three labels at `v`
modulo the cut space; good iff `q(v) = 0`; the Gauss law says the charge in a region equals the flux
through its boundary; the 64 classes are the cosets of the [15,9,3] cut code, in six Aut(P)-orbits
`0, E (15), D3 (15), D2 (30), T1 (1), T2 (2)`; multipoles conduct classes; alternating rings of two
multipoles with disjoint conducted sets carry charges in at least half of their blocks.

Round-3 results (EXP-013, EXP-014): every 6-pole of `P`, `J5`, `J7` and the dodecahedron conducts the
core `{0, E, D2}`, so charges never separate them. The exact transfer relation of a 6-pole is block
diagonal over the 64 classes (six sector matrices of order at most 67), so every ring of a finite
block family is decided by closing a finite semigroup (certificate re-checkable by products). Every
ring of claws, of Petersen superedges `P - u - w`, or of both, is Petersen colorable; every Petersen
coloring of a flower snark puts an antipodal triple (class `T1`, the all-ones class) on each
junction; the odd identity rings of superedges are cyclically 5-edge-connected snarks of girth 5 on
`8t` vertices; `G52` split along a 6-edge cut has zero trace although the two sides conduct the same
classes. `pd(R_3) = 3`. Published in `unbounded-defect` v0.02 (Proposition 5.3, Section 6).

## 2. The objects table

| Object | Definition | Owner |
|---|---|---|
| `G112`, `H112`, `G52`, `G52b`, `G68` | `data/*.edgelist`; digests in wiki 03 | EXP-001, EXP-007 P0 |
| `R_t` | alternating ring of `A = G52 - {0,3} - {1,9}` and `B = G52 - {2,7}` | EXP-012, `pcclib/rings.py` |
| charges, orbits, signatures | `pcclib/charges.py` | `context/2026-10-06-charges.md` |
| conducted sets of 4-poles and 6-poles | `pcclib/poles.py`; EXP-012, EXP-013 runners | |
| H-colorings with unknown target | `pcclib/hcolor.py` | EXP-007 |

## 3. Experiment index

| EXP | verdict | output |
|---|---|---|
| 001 to 006, 008 | CONFIRMED (see verdicts) | consequence audit |
| 005 | INCONCLUSIVE | pure-F proposition |
| 007 | CONFIRMED | both 52-vertex graphs in H_3; G68 orders 62 to 66 refuted |
| 009 | CONFIRMED | rings and frames of defect t |
| 010 | expectations refuted | all 4-poles of the 52s and G68 colorable; dot products |
| 011 | CONFIRMED | adjacent pairs of ten 102-vertex counterexamples critical |
| 012 | CONFIRMED | statement (e) false |
| 013 | P1, P2 PASS; P3 REFUTED | core `{0, E, D2}` on every 6-pole of the four cyclically 5-edge-connected sources |
| 014 | CONFIRMED (F4, F5 at their caps) | transfer semigroups; ring theorems for claws and Petersen superedges; G52 zero-trace control |

## 4. In flight (2026-10-06)

- EXP-007 addendum 7: portfolio for `G68` at target order 52 (formula
  `E:/_Datos/caos-research/petersen-coloring/EXP-007/G68_k52-portfolio.cnf`, 82,107 variables,
  2,683,782 clauses; result `artifacts/result-G68-k52-portfolio.json`; on SAT run
  `write_formula.py --graph G68 --k 52 --decode <model file>`).
- Nothing of EXP-013 or EXP-014 is in flight (the `F4`, `F5` antichain closures ended at their
  one-hour limits, undecided).

## 5. Next actions, ordered

1. PCC-F6: declare EXP-015 (6-poles cut from the cyclically 5-edge-connected snarks of order at
   most 28, House of Graphs lists; sector matrices; closures of each block alone and of pairs; a
   zero-trace element is a candidate for Problem 11 of v4) before it runs; close the focus if it
   finds none.
2. PCC-F5: act on the `G68` order-52 answer (SAT: decode, check, refute the target; UNSAT: record).
3. Release step (version bump, bake, tag) belongs to the serialized release owner, not to this
   branch.

## 6. Where everything lives

| what | path |
|---|---|
| problem tree | `problems/combinatorics/petersen-coloring/` (data, code/pcclib, code/probes, experiments EXP-001..013, wiki 01-07, context) |
| programme record | `program/petersen-coloring/` (governance, manuscript map, plan, state, backlog, research lines, this file) |
| heavy artifacts | `E:/_Datos/caos-research/petersen-coloring/` |
| manuscripts | `manuscripts/petersen-coloring/{consequence-audit,unbounded-defect,colorable-only-by-itself}/` |
| research worktree | `E:/_worktrees/CAOS_RESEARCH-petersen-coloring` on `work/petersen-coloring/open` (moved from `E:/_Temp` on 2026-10-06) |
| vault worktree | `E:/_worktrees/CAOS_MANAGE-petersen-coloring` (detached at `origin/develop`, push with `git push origin HEAD:develop`) |
| management mirror | `_CAOS_MANAGE/plans/caos-research/petersen-coloring/` |
| vault manuscript metadata | `_CAOS_MANAGE/manuscripts/petersen-coloring/` |

## 7. Gotchas

- Worktrees live in `E:/_worktrees/<Repo>-<topic>`; remove one only after
  `git merge-base --is-ancestor HEAD origin/<branch>` succeeds. CAOS_MANAGE is written from an
  isolated worktree, never from the shared checkout; fast-forward the shared checkout after pushes.
- Methodology 13 (2026-10): governance record and manuscript map are guarded by
  `scripts/check_research_governance.py`; every manuscript folder needs a README with version and
  DOI; strategic review at each boundary; show the user a changed target before treating it as the
  continuation.
- Methodology 09 (2026-10-04): a manuscript record holds only the manuscript PDF; supporting files
  go to a separate evidence record.
- The runner watchdog cannot interrupt an in-process PySAT solve; external solver calls honour it.
  WSL solvers orphaned by a killed runner keep writing proofs: check them post hoc with
  `certify_existing.py`.
- The WSL virtual machine stopped once (2026-09-18 21:18) and killed every proof check; complete
  proofs on disk end with the empty clause and can be rechecked.
- Stopping a background `xargs` job does not kill its driver on Windows; list `xargs.exe` first.
- Shell heredocs mangle backslashes; write LaTeX and Python with file tools.
- Another session may publish versions of these records (author-name release made audit v0.03);
  check the vault ledger before choosing a version number.
