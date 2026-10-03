# Riemann hypothesis result and manuscript map

Updated 2026-09-27 (after the route preflights). This map separates mathematical evidence, strategic value,
manuscript coverage and external novelty. Experiment verdicts remain the
authority for proofs and refutations; the machine-readable record is
[`research-governance.json`](research-governance.json).

## Status boundary

The Riemann hypothesis is open. The 2026 unconditional simple-critical
proportion is due to Alpoge and Furman (argument found by Claude,
arXiv:2608.13637), with Lamzouri's direct proof and Wang's short-interval and
global extensions. The CAOS program proves improvements and localizations of
those proportion theorems. It claims no progress on RH itself.

Internal exact or certified validation and Zenodo persistence do not establish
peer review or worldwide novelty. The recorded source searches, most recently
the [2026-09-27 sweep](../../problems/number-theory/riemann-hypothesis/context/2026-09-27-literature-and-representation-sweep.md),
did not locate exact matches for the results below. That sweep could not read
arXiv full text, so specialist confirmation is still required.

## Result blocks

| block | experiments | result status | attributed inputs | manuscript home |
|---|---|---|---|---|
| Baseline reproduction and audit | EXP-001 | reproduced, not novel | all | research record; provenance in `short-interval-stability` |
| Short-interval stability, parity, localization, Hilbert compression, spectral defect | EXP-002--008 | internally proved, certified | Wang's pair theorem; Pearce-Crump's rank-six constant (EXP-008) | `short-interval-stability` v0.07 |
| Sharp three-point kernel ratio | EXP-009 | ratio theorem internal; global proportion through Wang's framework | Wang arXiv:2609.24167 | `sharp-three-point-kernel` v0.01 |
| Localized Levinson-Conrey detector, onset 0.534 | EXP-010 | internally proved, certified, two referee passes | Wang's pair theorem | `short-interval-levinson` v0.01 |
| Linear-refinement barrier (certified counterexamples) | EXP-011 | confirmed, research record | none | no manuscript; recorded in the wiki and verdict |
| Tang-type short-window moment (stopped) | EXP-012 | inconclusive, obstruction recorded | Tang arXiv:2608.14852 | no manuscript; research record |

## Published manuscripts

| slug | version | version DOI | concept DOI |
|---|---|---|---|
| `short-interval-stability` | v0.07 | `10.5281/zenodo.22860012` | `10.5281/zenodo.22727388` |
| `sharp-three-point-kernel` | v0.01 | `10.5281/zenodo.22940291` | `10.5281/zenodo.22940290` |
| `short-interval-levinson` | v0.01 | `10.5281/zenodo.22984155` | `10.5281/zenodo.22984154` |

## Active focus and routing of future results

Current focus: **RH-F4**, the short-interval onset toward `theta>1/2`.

- A lower onset that uses the Levinson detector goes to the next version of
  `short-interval-levinson`.
- A proved general-`Q`, uniform-shift short-window moment (RH-027) is a
  standalone theorem and would trigger a new coherent paper.
- Focus RH-F5 (unconditional Cohn-Elkies kernels) was closed on 2026-09-27
  with its obstruction in the research record.
- RH-034 was closed by EXP-011 (research record).
- A longer short-window mollifier (RH-038), if proved, goes to the next version
  of `short-interval-levinson`.
- Closed route preflights (RH-028, RH-032, RH-033, RH-035, RH-036) are
  research records.

## October update and disposition

The 2026-10-03 full-text review supersedes the historical external-standing
paragraph above. A distinct-zero paper and higher upstream global candidate
exist; no located source improves the 0.534 short-window onset.

| block | experiments | result status | attributed inputs | manuscript home |
|---|---|---|---|---|
| Fixed mixed-Gram parameter optimum | EXP-013 | exact improvement and cap, research record | Knausgard energy and seven-point certificate | no standalone manuscript |
| Generic phase resolution | EXP-014 | uniform mechanism obstruction | elementary; EXP-010 mechanism | short-interval-Levinson supporting research record |
| Squarefree supported collisions | EXP-015 | elementary support-aware obstruction | none for arithmetic proof | short-interval-Levinson supporting research record |

These do not justify splitting or publishing another paper. The positive
analytic target remains a complete signed reduction and cancellation theorem
(RH-038), which would justify a coherent manuscript if proved.
