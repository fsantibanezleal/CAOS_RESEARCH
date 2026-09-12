# EXP-001: source and constant audit

Declared: 2026-09-12, before computation. Device: CPU. Deterministic reproduction.

## Question and prediction

Independent rational or certified arithmetic should reproduce the exact global and short-interval
constants stated by Lamzouri and Wang. The inspected original normalization
$d=\lfloor T\log(T/(2\pi))/(2\pi)\rfloor$ is asymptotic to $N(T,2T)$ but the asserted
$O(\log T)$ difference is inconsistent with Riemann-von Mangoldt; the main-term difference
should be $(2\log2-1)T/(2\pi)+O(\log T)$.

## Sources and premises

Lamzouri arXiv:2609.02882v2, Wang arXiv:2609.07918v1, and the supplied original/revised
Anthropic proof. The full relevant theorem, normalization, and final optimization sections
have been inspected. External analytic theorems are imported sources, not CAOS experiments.
Formal-source assumptions and upstream CI coverage are recorded separately from local replay.

## Method and invariant first

Use exact symbolic identities and rational Taylor intervals for trigonometric constants.
Compare independent arithmetic paths and certify decimal brackets. Expand the main term of
$N(2T)-N(T)$ algebraically; no zero sweep or GPU is needed.

## PASS, FAIL, and limitations

PASS establishes reproduction of these formulas and any exact normalization correction. It
does not independently prove the source analytic theorems, certify a finite-height zeta count,
or establish novelty. FAIL records the mismatch and blocks dependent numerical claims until
resolved. Source/license/hash checks must fail closed on missing or changed files.

## Budget and stop criterion

Expected arithmetic runtime below one minute; maximum five minutes. Stop on unresolved interval,
dependency error, or source mismatch and record an inconclusive outcome. No long formal build
is included; any such build needs its own logged budget and checkpoint plan.
