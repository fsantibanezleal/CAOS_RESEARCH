# Riemann research code

Deterministic exact/certified routines for declared experiments live here. Exploratory floating
calculations cannot certify a theorem. Tests write only to temporary paths, never to canonical
experiment artifacts. CPU is the default for the present finite calculations.

`restore_sources.py` restores the local full-text archive from the portable manifest and
checks exact size and SHA-256. `--verify-only` performs no network requests. Publicly
redistributable code archives retain upstream licenses in `context/source-snapshots/`.

`riemann_certificates.py` evaluates the entire cosine kernel, generates an exact binary
subdivision certificate, and replays that certificate with either Arb's sinc or a separate
96-term Taylor evaluator with a rigorous remainder. The evaluators share Arb, geometry and
the analytic Lipschitz estimate. Checkpoint termination cannot produce a passing certificate.

```text
python -m pip install -r problems/number-theory/riemann-hypothesis/requirements.txt
python problems/number-theory/riemann-hypothesis/experiments/EXP-001-source-and-constant-audit/run.py --math-only --output-dir tmp/riemann-baseline
python problems/number-theory/riemann-hypothesis/experiments/EXP-002-short-interval-stability/run.py --output-dir tmp/riemann-replay --radius 21/4 --threshold 1/7000
pytest tests/test_riemann_baseline.py tests/test_riemann_certificates.py
```

The math-only baseline mode does not read or verify PDFs. Omit `--math-only` after restoring
the archive for full source-integrity checks. The general theorem and the limits of numerical
verification are documented in EXP-002's proof, verdict and adversarial audit.
