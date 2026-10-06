# Petersen coloring: result and manuscript map

Updated 2026-10-06. This map separates mathematical evidence, strategic value, manuscript
coverage and external novelty (methodology 13). Experiment verdicts remain the authority for
proofs and refutations.

## Status boundary

Jaeger's Petersen coloring conjecture is already false. Priority belongs to Putman, to Goedgebeur,
Jooken, Máčajová, Mattiolo, Mazzuoccolo and Ulyanov, to the July 2026 68-vertex announcement, and to
Jooken for the first human-checkable proof. The CAOS program certifies those counterexamples, audits
what they imply, and proves theorems about the structure the disproof opened. It does not claim the
disproof.

Internal exact validation and Zenodo persistence do not establish peer review or worldwide novelty.
The searches recorded in `problems/combinatorics/petersen-coloring/context/2026-10-06-literature-refresh.md`
did not find the results below elsewhere; specialist confirmation is still required.

## Result blocks

| block | experiments | result status | value | manuscript home |
|---|---|---|---|---|
| Independent certification of the five retrievable counterexamples | EXP-001, EXP-007 P0 | reproduced, not novel | trusted baseline | `consequence-audit`, Section 2 |
| Consequence audit (covers, index 4, 5-CDC, flows, oddness, resistance, normal 6) | EXP-002, EXP-003, EXP-004, EXP-008 | decided from both sides on five graphs; partly overlapping with arXiv:2608.10028v3/v4 (stated) | direct | `consequence-audit` |
| Petersen defect: parity theorem, defect 2, universal 2-criticality | EXP-006, EXP-008, EXP-011 | theorem plus exhaustive pair sweeps on five graphs and adjacent pairs of ten more | structural | `consequence-audit` |
| Compositions of the Petersen 4-pole | EXP-005 | pure-F proposition proved; search non-convergent | minor | `consequence-audit`, Section 6 (research record for the search) |
| H_3 membership of the 52-vertex counterexamples | EXP-007 | both colorable only by themselves (conditional on Observation 10 of v4); fiber-parity and unused-vertex lemmas | answers v4 Section 5.4 | `colorable-only-by-itself` |
| Abnormal edges, rings and frames, statements (c), (d) | EXP-009 | proved, attained on four instances | settles part of MMM Conjecture 3 | `consequence-audit`, Section 5.3 |
| Statement (e) is a two-defect statement | EXP-010, EXP-011 | proved (Theorem 5.9, given MMM Proposition 2) | reduction | `consequence-audit`, Section 5.3 |
| Statement (e) false: cyclically 4-edge-connected graphs of unbounded defect | EXP-012 | proved (conduction lemma, alternating rings, certificates) | settles MMM Conjecture 3 | `unbounded-defect` |

## Manuscripts

| slug | version | version DOI | concept DOI | central question |
|---|---|---|---|---|
| `consequence-audit` | v0.06 | [10.5281/zenodo.23195171](https://doi.org/10.5281/zenodo.23195171) | [10.5281/zenodo.22285164](https://doi.org/10.5281/zenodo.22285164) | what survives on the counterexamples, and how far they are from colorable |
| `unbounded-defect` | v0.01 | [10.5281/zenodo.22847193](https://doi.org/10.5281/zenodo.22847193) | [10.5281/zenodo.22847192](https://doi.org/10.5281/zenodo.22847192) | is the defect bounded on cyclically 4-edge-connected cubic graphs (statement (e)) |
| `colorable-only-by-itself` | v0.01 | [10.5281/zenodo.22859075](https://doi.org/10.5281/zenodo.22859075) | [10.5281/zenodo.22859074](https://doi.org/10.5281/zenodo.22859074) | are the 52-vertex counterexamples colorable only by themselves |

Split decision (2026-10-06 review): the three papers have different central questions and proof
toolkits (certified invariants; cut-space conduction; H-coloring fibers and target search), so they
stay separate. The audit carries a short statement and citation of the other two and no longer
repeats their proofs beyond Section 5.3.

## Focus record

- Closed: PCC-F0, PCC-F1, PCC-F3, PCC-F4 (success gates met).
- Dormant: PCC-F2 (composition search non-convergent).
- Gated: PCC-F5 (G68 and the unconditional H_3 form; only portfolio runs at the most informative
  orders, starting with target order 52).
- Active: **PCC-F6**, cut-space charges and cyclically 5-edge-connected cubic graphs (Problem 11 of
  arXiv:2608.10028v4). Its first bounded action is EXP-013; a manuscript is created only on its
  success gate.

## Open obligations

- `unbounded-defect`: the exact defect of `R_3` (only `pd >= 3` is established).
- `colorable-only-by-itself`: the unconditional form needs orders 6 to 22 (`G52`) and 2 to 38
  (`G52b`); the 68-vertex graph needs orders 40 to 60.
- `consequence-audit`: none beyond corrections.
