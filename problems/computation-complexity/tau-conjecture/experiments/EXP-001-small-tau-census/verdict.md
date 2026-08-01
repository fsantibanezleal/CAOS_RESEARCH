# EXP-001 verdict: CONFIRMED (census decision-complete for tau <= 4)

Run 2026-08-01, `run.py` (smoke first, then full), repo venv Python 3.13.0,
CPU only, deterministic, 4.2 s wall (budget was 30 min; kill criterion never
approached). Raw output in `artifacts/census.json` (checkpointed per depth).

## Stage A: Markstroem regression gate: PASS, all seven anchors

Integer restriction (inputs {1}, positive normalized values) reproduces
arXiv:1306.3091v4 Figure 1 EXACTLY at every compared depth:

| k | reached (ours / Markstroem) | initial interval (ours / Markstroem) |
|---|---|---|
| 1 | 2 / 2 | 2 / 2 |
| 2 | 4 / 4 | 4 / 4 |
| 3 | 9 / 9 | 6 / 6 |
| 4 | 26 / 26 | 12 / 12 |
| 5 | 102 / 102 | 40 / 40 |
| 6 | 562 / 562 | 112 / 112 |
| 7 | 4363 / 4363 | 310 / 310 |

The enumerator core is therefore anchored to an independent published exact
computation before its polynomial output is used.

## Stage B: the census (exact, all depths complete)

Model: inputs $\{-1, 1, x\}$; gates $+,-,\times$; length = gate count
(equivalent to the survey's free-$\{-1,0,1\}$ model by hypothesis lemma 1).

| $\tau$ | reached-set states | new polynomials first seen | $z_{\max}(\tau)$ |
|---|---|---|---|
| 1 | 9 | 9 | 1 |
| 2 | 98 | 34 | 2 |
| 3 | 1462 | 177 | 3 |
| 4 | 29506 | 1249 | **3** |

**Main fact established: $z_{\max}(4) = 3$.** No constant-free program of
length 4 computes a polynomial with 4 distinct integer roots; the record 3
is attained already at $\tau = 3$ ($x^3 - x$, roots $\{-1,0,1\}$) and at
$\tau = 4$ by 37 distinct new polynomials.

Prediction scorecard (hypothesis committed before the run):
1. Stage A reproduces the seven anchors: PASS.
2. $z_{\max}(1)=1$, $z_{\max}(2)=2$ (witness $x^2-1$), $z_{\max}(3)=3$
   (witness $x^3-x$): PASS.
3. $z_{\max}(4) \in \{3,4\}$: DECIDED, value 3.

Growth data so far: $1, 2, 3, 3$: consistent with (and far below) the
conjecture's polynomial bound at these depths; decision value is structural.

## Mechanism notes (feeds the anatomy lens, TCB-007)

- Depth-3 records are exactly the four sign/scale variants of $x^3 - x =
  x(x-1)(x+1)$: consecutive-triple roots centered at 0.
- Depth-4 records include SHIFTED consecutive triples, e.g.
  $-x(x+1)(x+2)$ via the 4-step program
  $(-1)-x \to -x-1$; $1-(-x-1) \to x+2$; $x \cdot (-x-1) \to -x^2-x$;
  $(-x^2-x)(x+2)$: translation of the root block costs exactly one extra
  gate. Also degree-4 records with a squared factor, e.g.
  $-x(x+1)^2(x+2)$ (roots $\{-2,-1,0\}$): multiplicity is free in $z$.
- No length-4 mechanism separates 4 distinct integer points; the cheapest
  4-root witness is now the target of the next census depth.

## Adversarial validation record

- Every record polynomial was replayed from its reconstructed SLP (exact
  tuple equality asserted) and every claimed root re-verified by exact
  evaluation; the root COUNT is certified by the rational-root argument
  (integer roots of the $x^m$-stripped part divide its nonzero trailing
  coefficient; all divisors tested both signs). All assertions passed.
- Stage A interpretation risk (what Figure 1 counts) was fixed in the
  hypothesis BEFORE the run and matched on all seven values
  simultaneously; a wrong interpretation matching seven exact values and
  seven interval lengths is not plausible.

## Exact-arithmetic status

All arithmetic is native Python integers on dense coefficient tuples; no
floats anywhere; no randomness; no declared nondeterminism.

## How could this be wrong?

1. The reached-set sufficiency lemma (state = set of computed values) could
   be unsound if program order mattered: it does not, since every gate
   draws only from the set of available values; this is the same reduction
   Markstroem states and our Stage A anchoring exercises it on a published
   ground truth.
2. The free-0 elimination lemma could hide programs that need the constant
   0: lemma 1 of the hypothesis shows any 0-use is replaceable at equal
   cost; a missed case would UNDERCOUNT $\tau$ by at most nothing (it can
   only make our model more generous, never less: we allow $-1$ directly).
   Verified reasoning, not tested; flagged as the weakest link and
   revisited in the TCB-005 canonicalization pass.
3. A silent bug in padd/psub/pmul would corrupt everything: mitigated by
   the witness replays and the Stage A anchor (which shares the state
   machinery though not the polynomial arithmetic); TCB-005 adds a sympy
   cross-check of the polynomial layer as a due diligence row.

## Consequences for the strategy

- The tooling is trusted to the anchor; the frontier work (tau = 5 and
  beyond) needs the canonicalization lemmas (TCB-005) since the naive
  state count grows ~30x per depth (29506 at depth 4, ~1M-scale at 5 in
  Python; feasible but the lemma-backed pruning is the right move first).
- New decision-bearing question minted for the next round: the minimal
  $\tau$ with $z_{\max}(\tau) = 4$ (candidate constructions at
  $\tau \in \{5, 6\}$; the census will decide).
