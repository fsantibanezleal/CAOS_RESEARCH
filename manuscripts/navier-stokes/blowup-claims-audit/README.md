# navier-stokes: how much dissipation can a multiscale layer cascade carry?

First paper of the navier-stokes research series. Theorem 3.1: a layer cascade growing at sqrt(A)
cannot carry more than alpha = 1/2, and one growing at A no more than alpha = 1 (|grad|^alpha
convention, classical viscosity 2), under the hypothesis that the background gradients are unbounded;
a remark covers a stage-dependent frequency exponent. Theorems 4.1 and 4.2: both smooth-forcing
designs, Boussinesq and axisymmetric Euler, are pendulum-class, and their force estimates certify at
most 5.3e-04 and 6e-08 as published, 9.0e-03 and 7.5e-03 under any retuning (|grad|^alpha), at least
ten times below the proved rough-force threshold. Built from the experiment verdicts and context
dossiers of [`problems/analysis-pde/navier-stokes/`](../../../problems/analysis-pde/navier-stokes/),
never from memory, per methodology 09.

| | |
|---|---|
| source version | 0.10 (2026-11-14), built and not yet released; content-bar pass applied (10,653 words, 8 figures, 28 references, 5 algorithms by `tools/zenodo/check_manuscript_depth.py`) |
| published version | 0.09 (2026-11-02), version DOI [10.5281/zenodo.23890775](https://doi.org/10.5281/zenodo.23890775), concept DOI [10.5281/zenodo.22820520](https://doi.org/10.5281/zenodo.22820520) (always latest) |
| pages | 35 |
| build | `pdflatex main.tex` twice, MiKTeX; zero errors, zero warnings, zero overfull or underfull boxes |
| labels | `[V]` read on a primary source (equation or page cited), `[D]` derived, `[MV]` machine-verified (kernel replay, exact symbolic computation, or a recorded run pinned by a test), `[U]` unverified, `[C]` conjecture; used in the text after each statement |

## What it contains, and where each part comes from

| section | source in the repository |
|---|---|
| the layer mechanism, the single-mode identity and the dissipative extension | `context/2026-09-11-simplified-model-and-beyond.md`, Alpoge-Buckmaster Lemma 3.1 |
| the class ceiling, its hypotheses and the stage-dependent remark | `nslib/class_ceiling.py`, EXP-003 and EXP-008 verdicts |
| the design bound, from the full force budget, with equation and page of every estimate | `context/2026-09-17-force-estimates-exponent-content.md`, `nslib/ab_force_budget.py`, `references/ab-boussinesq.pdf` |
| the Euler design: its growth class, the thirteen quotients and the force estimates | `context/2026-09-18-euler-force-budget.md`, `nslib/ab_euler_budget.py`, `references/ab-euler.pdf` |
| the published threshold recovered from its budget; admissible frequency ratios | `context/2026-09-14-threshold-reconstruction.md`, `nslib/cmz_budget.py`, exact checks in CI |
| numerical methods and reproducibility | `nslib/boussinesq.py`, `corotating.py`, `steering.py`, the `args` blocks of the result files, `code/reproduce_all.py` |
| verification of the dissipative extension, every criterion met or not met | EXP-002, EXP-003, EXP-004, EXP-005, EXP-007 and EXP-008 verdicts and result files |
| machine verification, build and kernel replay | EXP-001 and EXP-006 verdicts |
| related work: the hypotheses and conclusion of each construction and announced result examined (Section 1.1) | the abstracts, main theorems and pages of the archived PDFs in `references/`, read depth in `context/references.md`; Crossref for the journal items |
| experimental design: the question, the committed prediction and the pass criterion of every run (Section 7.1) | the `hypothesis.md` files and the runner docstrings of EXP-001 to EXP-008 |
| algorithms: the integrating-factor step, the local-rate estimator, the localization test, the bisection and the design search (Section 6) | `nslib/boussinesq.py`, `code/run_exp004.py`, `code/run_exp007.py`, `code/run_exp008.py`, `nslib/cascade.py`, `nslib/ab_force_budget.py` |
| figures (eight) | `figures/make_figures.py`, which reads the result files and `nslib` |

Every number quoted in the paper is also gated in continuous integration against the result files it
came from (`tests/test_navier_stokes_quoted_numbers.py`), and every experiment reproduces from its own
recorded arguments (`code/reproduce_all.py`, experiments 2, 3, 4, 7 and 8; the experiment 5 commands
are reconstructed from its `args` blocks).

## What the paper reports that did not pass

The verification section lists every criterion. Three were not met and are reported with their
numbers: the slope of the local growth rate in the two-scale background (1.36 times the prediction,
criterion 1 plus or minus 0.15), the correlation of the steered two-layer handoff (0.808 at best,
0.509 at the largest separation, criterion 0.9), and the steered cycle at its first chosen
parameters (refuted, 726-fold growth). One run, the handoff without steering, is inconclusive.

## What the paper does not claim

It does not prove blowup for any equation, does not verify the mathematics of either announced proof
beyond what a kernel replay of a formalization establishes, does not improve any published threshold,
and does not claim the layer mechanism, which belongs to Cordoba and Martinez-Zoroa. The relation
p = 11/4 + sqrt 7 at the published threshold is stated in the text to carry no information about it.

## Rebuilding

```
cd manuscripts/navier-stokes/blowup-claims-audit
python figures/make_figures.py
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```
