# navier-stokes: an independent audit of the September 2026 blowup claims

First paper of the navier-stokes research series. Built from the experiment verdicts and context
dossiers of [`problems/analysis-pde/navier-stokes/`](../../../problems/analysis-pde/navier-stokes/),
never from memory, per methodology 09.

| | |
|---|---|
| version | 0.01 (2026-09-17) |
| pages | 9 |
| build | `pdflatex main.tex` twice, MiKTeX; zero errors, zero overfull or underfull boxes |
| labels | machine-verified `[MV]`, derived `[D]`, conjectural `[C]`, used in-text |
| Zenodo | not yet deposited |

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
