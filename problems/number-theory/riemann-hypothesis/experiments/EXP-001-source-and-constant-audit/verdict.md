# EXP-001 verdict: PASS for reproduction and algebraic audit

Executed 2026-09-12 on CPU after hypothesis commit `266486f`.
The runner completed in under one second using SymPy and python-flint from the
worktree virtual environment. The authoritative machine-readable record is
[artifacts/result.json](artifacts/result.json).

The primary arithmetic uses exact `Fraction` alternating-series brackets for
cosine and sinc, with rational $a^2=\theta^2/2$. It forms
$a\cot a=\cos a/(\sin a/a)$ without evaluating an irrational argument.
The remaining $\sqrt2$ in $C_2$ has an integer-square-root rational enclosure.
Every constant has an exact enclosure narrower than $10^{-95}$. The separate
256-bit Arb path contains each independently constructed exact enclosure.

| Quantity | Reproduced value, truncated |
|---|---:|
| $C_0$ | 0.672500703679411645734379790803 |
| $C_1$ | 0.836250351839705822867189895401 |
| $C_2$ | 0.887620008173354339866075859447 |
| $c(3/4)$ | 0.419075012975424333734553610698 |

The full rational endpoints and outward decimal bounds are in the artifact.
Four required source PDFs match hard-coded SHA-256 pins and their manifest
entries; source URLs, byte counts, and license metadata are checked before
arithmetic. Missing sources, changed bytes, absent metadata, or disagreement
between arithmetic paths produce an `INCONCLUSIVE` result and a nonzero exit.
A changed-source negative control was rejected before arithmetic. The canonical
Git artifact uses UTF-8 and LF newlines: 13,276 bytes, SHA-256
`a472e624ce0bf95e5a700fc663f6a37c57905e844b257f0a105a60f14da8cd62`.
The initial successful Windows replay used CRLF newlines (13,474 bytes,
SHA-256 `963313dc7cc1c5add51ddf4e6eb2d561a48156289861f27f946e857fca1df483`).
These files encode identical mathematics. The runner now writes explicit UTF-8
and LF on every platform; a fresh full replay matches the canonical Git blob
byte for byte. EXP-002 results and shared checkpoints use the same newline policy.
This full replay used the repository's `context/source-manifest.json` and each
row's relative `cache_path` under `context/source-cache`. Version and rendered
date notes are retained from the manifest; the Lamzouri v2 hash is unchanged.

SymPy verifies the triple numerator identity by direct polynomial expansion
and reduction under the two unit-circle constraints. The expanded identity
is already zero before imposing those constraints. It also verifies the
tangent-addition obstruction to three positive additive kernel roots.

The normalization audit gives

$$
N(2T)-N(T)-\left\lfloor\frac{T\log(T/(2\pi))}{2\pi}\right\rfloor
=\frac{(2\log2-1)T}{2\pi}+O(\log T).
$$

The original supplied PDF's equation (1.2) states the correct zero-count main
term. The revised August 11 PDF, Section 2.2, asserts
$d=N(T,2T)+O(L)$ with $L=\log(T/(2\pi))$; this sharper absolute-error assertion
is inconsistent with that main term. The correction is $O(T)=o(N)$, so this
finding alone does not refute the limiting zero-proportion theorem.

To reproduce after restoring the source cache from the persisted manifest,
run the following from the research worktree with its Python environment
active. The default source directory is resolved relative to the script, and
the output directory may be outside the experiment:

```bash
python problems/number-theory/riemann-hypothesis/experiments/EXP-001-source-and-constant-audit/run.py --output-dir tmp/riemann-baseline
```

For CI without cached PDFs, explicitly request math-only mode:

```bash
python problems/number-theory/riemann-hypothesis/experiments/EXP-001-source-and-constant-audit/run.py --math-only --output-dir tmp/riemann-baseline-math
python -m pytest tests/test_riemann_baseline.py
```

Math-only output has top-level status `PASS_MATH_ONLY`, `math_status: PASS`,
and `source_verification.status: NOT_PERFORMED`. It opens neither the manifest
nor its cached files. The committed result is the full source-verified replay.
The eleven cheap tests reproduce exact constants and symbolic identities,
compare the recorded mathematics, check deterministic UTF-8/LF bytes and precision
restoration, exercise the CLI with absent source files, and reject changed
source bytes and escaping cache paths using synthetic fixtures. These tests
require no redistributed PDFs. Scoped Ruff and all eleven tests passed.

PASS covers formula reproduction, source integrity, the normalization
correction, and exact algebraic identities. It establishes no novelty,
independent proof of the imported analytic theorems, finite-height zero
count, or local replay of upstream Lean developments.
