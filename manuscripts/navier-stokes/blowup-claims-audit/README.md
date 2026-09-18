# navier-stokes: how much dissipation can a multiscale layer cascade carry?

First paper of the navier-stokes research series. Theorem 3.1: a layer cascade growing at sqrt(A)
cannot carry more than alpha = 1/2, and one growing at A no more than alpha = 1 (|grad|^alpha
convention, classical viscosity 2). Theorem 4.1: the force estimates of the smooth-forcing design
certify at most 5.29e-04 at the published choices and 8.96e-03 under any retuning, at least ten
times below the proved rough-force threshold. v0.05 replaces the v0.04 design bound (1.08e-03),
which rested on a misread inequality; earlier versions are superseded. Built from the experiment verdicts and context
dossiers of [`problems/analysis-pde/navier-stokes/`](../../../problems/analysis-pde/navier-stokes/),
never from memory, per methodology 09.

| | |
|---|---|
| version | 0.05 (2026-09-17) |
| pages | 8 |
| build | `pdflatex main.tex` twice, MiKTeX; zero errors, zero overfull or underfull boxes |
| labels | machine-verified `[MV]`, derived `[D]`, conjectural `[C]`, used in-text |
| Zenodo | v0.05, version DOI [10.5281/zenodo.22822133](https://doi.org/10.5281/zenodo.22822133), concept DOI [10.5281/zenodo.22820520](https://doi.org/10.5281/zenodo.22820520) (always latest) |

## What it contains, and where each part comes from

| section | source in the repository |
|---|---|
| machine verification, build and kernel replay | EXP-001 and EXP-006 verdicts |
| reduced model and its validation | EXP-002 and EXP-004 verdicts |
| the steering cycle on a torus, and its refuted first run | EXP-005 verdict |
| what localization costs the damping law | EXP-007 verdict |
| the published threshold recovered from its budget | `context/2026-09-14-threshold-reconstruction.md` |
| admissible frequency ratios, and the exclusion of geometric cascades | `nslib/cmz_budget.py`, exact checks in CI |
| our cascade cap, and why it is unreachable | `context/2026-09-16-model-side-force-budget.md` |
| the regularity-against-dissipation trade-off and the dated prediction | `context/2026-09-16-smoothness-versus-dissipation.md` |
| the design bound, from the full force budget | `context/2026-09-17-force-estimates-exponent-content.md`, `nslib/ab_force_budget.py` |
| the class ceiling and its numerical confirmation | `nslib/class_ceiling.py`, EXP-008 verdict |

Every number quoted in the paper is also gated in continuous integration against the result files it
came from (`tests/test_navier_stokes_quoted_numbers.py`), and every experiment reproduces from its own
recorded arguments (`code/reproduce_all.py`).

## What the paper does not claim

It does not prove blowup for any equation, does not verify the mathematics of either announced proof
beyond what a kernel replay of a formalization establishes, does not improve any published threshold,
and does not claim the layer mechanism, which belongs to Cordoba and Martinez-Zoroa. Two claims from
an earlier round are retracted in the text and the retractions are kept there.

## Rebuilding

```
cd manuscripts/navier-stokes/blowup-claims-audit
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```
