# EXP-002: the census at tau = 5: does z_max reach 4, and what is its valuation spectrum?

Declared 2026-08-01, before the run. Continues the census spine (TC-P0/P1)
and adds the p-adic instrumentation adopted in
`program/tau-conjecture/approaches-evaluation-2026-08-01.md` (route A2/B2).

## Questions

1. Exact value of $z_{\max}(5)$ (max distinct integer roots over
   constant-free SLPs of length 5, inputs $\{-1,1,x\}$).
2. The minimal $\tau$ with $z_{\max}(\tau) = 4$ (EXP-001 left it $\ge 5$).
3. Observational (no committed prediction): the 2-adic valuation spectra of
   the record polynomials' roots: do records spread valuations (pressuring
   Rojas' $N_2$) or pile roots into one valuation class (pressuring the
   p-adic Digit Conjecture near 1)? Instrumented via
   `tclib.two_adic_valuations`.

## Motivation

EXP-001 decided $z_{\max}(1..4) = 1,2,3,3$ and minted question 2. The dual
view (approaches evaluation B1) reads $z_{\max}(5)$ as deciding the cost
$T(S)$ of 4-element root sets. Rojas (read in full, math/0304100) reduces
the tau-conjecture to its p-adic digit version and leaves the growth of the
valuation-spectrum bound $s \le N_p(s) \le s(s+1)/2$ open, which question 3
begins to measure.

## Candidate construction (committed before the run, [D])

The shifted-quadratic factory: with $u = x \cdot x$ (1 gate),
$v = u - x$ (2 gates; $x(x-1)$, roots $\{0,1\}$), $c = 1 + 1$ (3 gates),
$w = v - c$ (4 gates; $x^2 - x - 2 = (x-2)(x+1)$, roots $\{2,-1\}$),
$f = v \cdot w$ (5 gates) has the 4 distinct integer roots
$\{-1, 0, 1, 2\}$. Hence $z_{\max}(5) \ge 4$ unconditionally.
General mechanism: $q - c$ factors over $\mathbb{Z}$ for $q = x^2 - x$ iff
$1 + 4c$ is an odd perfect square iff $c = m(m+1)$; products
$\prod_{m}(q - m(m+1))$ are a root factory at asymptotic rate ~3 gates per
2 roots (linear), feeding the anatomy lens.

## Falsifiable predictions

1. $z_{\max}(5) = 4$ (the construction above is optimal; the census must
   show no 5-gate program reaches 5 distinct integer roots).
2. Hence the minimal $\tau$ with 4 roots is exactly 5.

## One-sidedness

The completed depth is decision-complete for questions 1-2 (exact theorem-
grade values either way); it proves nothing asymptotic about the
conjecture. Question 3 is observational: any outcome is recorded, none is a
test.

## Premise dependencies (P3)

- Enumerator correctness: anchored by EXP-001 (Stage A 14/14 vs Markstroem;
  verdict CONFIRMED). tclib refactor is re-anchored by its test suite
  (same anchors) before the run; a test failure aborts the experiment.
- Model lemmas (free-0 elimination, normalization, reached-set
  sufficiency): EXP-001 hypothesis lemmas 1-3 [D].

## Invariant-first note (P5)

Degree cap gives $z \le 2^5 = 32$: decides nothing. No known invariant
separates $z=4$ from $z=5$ at $\tau=5$ without search; the committed
construction settles the lower side for free, so the run only needs the
upper side (exhaustion). Justified.

## Compute budget and kill criterion (P6)

- Tooling gate first: `python -m pytest .../code/tclib -q` must pass.
- Smoke: depth-3 census re-run must match EXP-001 (states 9/98/1462).
- Budget: 45 minutes wall, CPU only. Expected: depth-5 frontier
  ~0.5-1.5M states, minutes-scale; memory guard at 5M states.
- Kill: if depth 5 incomplete at 40 min or the state cap trips, checkpoint,
  report depth 5 INCONCLUSIVE (with the standing lower bound
  $z_{\max}(5) \ge 4$ from the construction), and route the frontier to
  TCB-005 canonicalization.

## Success and failure criteria

- CONFIRMED: depth 5 exhausted; predictions 1-2 checked (whatever the
  values, the census decides them; the PREDICTIONS are confirmed only if
  $z_{\max}(5) = 4$).
- REFUTED (prediction): depth 5 exhausted and some 5-gate program attains
  $z \ge 5$ (this would be a striking mechanism find; record it fully).
- INCONCLUSIVE: kill criterion hit.
