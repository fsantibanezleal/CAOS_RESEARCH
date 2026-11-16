# manuscripts/tau-conjecture/census - the census paper

`main.tex` / `main.pdf`: "The Bottom of the Shub-Smale Tau Conjecture: an Exact Census of Integer Roots for Constant-Free
Straight-Line Programs of Length at Most Nine".

Current version: v0.07, published 2026-11-14 at [10.5281/zenodo.24231299](https://doi.org/10.5281/zenodo.24231299) (concept
[10.5281/zenodo.21753438](https://doi.org/10.5281/zenodo.21753438)); 35 pages, 600,037 bytes, SHA-256
`b85692fbe63bd9f6384bf6e32f09ccd3a2e767cec8d5c0087e0dde3add655e3d`. It is a revision from an independent audit and review
(corrected funnel table of the window-free additive scan, evidence marks on every literature claim, algorithm blocks,
figures generated from the records, related work, ablation and limitations); no result changes.

What the paper covers:

- The exact growth function z_max(tau) = 1, 2, 3, 3, 4, 5, 5, 6, 6 for tau = 1 to 9 (the maximum number of distinct
  integer roots of a nonzero polynomial computed by a constant-free straight-line program of at most tau gates), with the
  exact cost of 4, 5, 6 and 7 roots at 5, 6, 8 and 10 gates and the extremal witnesses.
- The search method: the last-gate lemma, the out-of-core construction of the depth-7 frontier (1,048,460,912 states), the
  union scan of the multiplicative ninth gate and the window-free 2-adic and 3-adic block filter for the additive ninth gate.
- The enumerator's anchors: Markstroem's published integer census (14 of 14 values) and computer-algebra root counts on 284
  and 228 polynomials.
- The stall theorems for iterated monic maps and the quadratic family x^2 - c, the digit-restricted ladders, and the exact
  ladders over F_p, R and Q.

The versions v0.01 to v0.07 are immutable Zenodo versions of one concept; the version notes are in `zenodo.json`.

Where the sources and the build live:

- Experiment records (hypothesis, run code, artifacts, verdict) of EXP-001 to EXP-015:
  `problems/computation-complexity/tau-conjecture/experiments/`; the enumerator library `tclib` in `.../code/tclib/`.
- Figures: `make_figures.py` rewrites `figures/*.dat` from the experiment artifacts (`python manuscripts/tau-conjecture/census/make_figures.py`);
  `main.tex` draws the axes from those files.
- Publication record: `zenodo.json` (metadata) and `publication-gate.json` (checks, hashes, review).
- Governance: `program/tau-conjecture/research-governance.json` and `manuscript-map.md`.
