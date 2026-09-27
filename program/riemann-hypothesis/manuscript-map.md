# Riemann hypothesis result and manuscript map

Updated 2026-09-27. This map separates mathematical evidence, strategic value,
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
- A global gain from unconditional Cohn-Elkies kernels (gated focus RH-F5)
  goes to the next version of `sharp-three-point-kernel`; a negative answer
  stays in the research record.
- Closure notes and certificate replays (RH-034 to RH-036) are research
  records unless they prove a theorem-sized barrier.
