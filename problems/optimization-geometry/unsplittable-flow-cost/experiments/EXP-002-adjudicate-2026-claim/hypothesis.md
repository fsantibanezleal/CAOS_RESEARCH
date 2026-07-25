# EXP-002: adjudication of the 2026 claimed counterexample to Goemans' conjecture

Declared 2026-07-24, BEFORE the run and before any adjudication code was written
(methodology/02). Phase UF-P1. Backlog UFB-004.

## Question

Is the finite instance announced publicly on 2026-07-22/23 a valid counterexample to
Goemans' cost conjecture (Conjecture 1.2 of arXiv:2510.21287), decided by our own exact
enumeration and independently of the proposer's verifier; and exactly what does it force?

## Motivation

The claim is currently unadjudicated: no preprint, no peer review, no expert confirmation
found (literature dossier section 4). It is also finite, so its validity is a decidable
arithmetic fact that needs no external authority. Our checker was calibrated for exactly
this in EXP-001. Everything downstream in the programme (minimality, the alpha frontier,
the Conj 1.3 hunt) is conditioned on the answer.

## The object under test

Transcribed in `context/2026-07-24-claimed-counterexample-dossier.md` section 2 and
re-entered by hand into `run.py`, never parsed from the proposer's JSON, so that a
transcription error in either direction is visible rather than shared: vertices
$s, u, v, w, t_1, t_2, t_3$; demands $15, 10, 15$; nine arcs with the loads and costs of
that table; $d_{\max} = 15$.

## Falsifiable predictions

Every one is a machine assertion; the run exits nonzero on any failure. The core
prediction H4 is stated so that its failure would REFUTE the public claim, which is the
outcome this experiment must be equally prepared to report.

**The decision.**

- **H1 (feasibility, test C7).** $x$ is a feasible fractional flow: conservation holds at
  all seven vertices, and $x \ge 0$.
- **H2 (enumeration, test C8).** Our own depth-first search finds exactly 2 simple
  $s$-$t_i$ paths for each terminal, hence exactly 8 unsplittable routings. This is the
  prediction most likely to fail if the claim is wrong, because unnoticed extra paths are
  the documented way candidate counterexamples die.
- **H3.** $c^T x = 58$ exactly.
- **H4 (THE DECISION).** Exactly 4 of the 8 routings are congestion-good, the minimum cost
  among them is exactly 60, and 60 > 58. Therefore NO unsplittable routing is
  simultaneously congestion-good and cost-good, and the instance IS a counterexample to
  Conjecture 1.2.
- **H5 (the quantitative content, Q4).** $\alpha_{\mathrm{inst}} = 16/15$, where
  $\alpha_{\mathrm{inst}} = \min\{\max_a (y_a - x_a)^+ / d_{\max}\}$ over COST-GOOD
  routings. In words: the instance forces the violation constant above 1, but only by
  $1/15$, the smallest possible integer margin at $d_{\max} = 15$.

**The consistency battery (a valid counterexample must contradict no proved theorem).**

- **H6 (C6, the DGG floor).** At least one congestion-good routing exists. If this failed,
  the instance data would contradict the Dinitz-Garg-Goemans theorem and would therefore be
  wrong.
- **H7 (C1, Skutella 2002).** The demands $\{15, 10\}$ are NOT all multiples of one
  another, so the instance is outside the case where the conjecture is proved.
- **H8 (C2, MSW25).** The underlying undirected graph contains a $K_4$ subdivision, with
  branch vertices $\{s, u, v, w\}$. Series-parallel digraphs are built by series and
  parallel composition and their underlying graphs are $K_4$-minor-free, so exhibiting a
  $K_4$ subdivision places the instance outside the class where Majthoub Almoghrabi,
  Skutella and Warode prove the conjecture (their Theorem 2, with the STRICT bounds
  $x_e - d_{\max} < y_e < x_e + d_{\max}$; their footnote 2 restricts the class to
  directed series-parallel graphs). Only this implication direction is used.
- **H9 (planarity).** Fewer than 5 vertices have degree at least 4 and fewer than 6 have
  degree at least 3, so by Kuratowski the graph is planar with no embedding computation.
- **H10 (C5, Conj 1.3 survives).** Some routing satisfies the cost-free two-sided bounds
  $x_a - d_{\max} \le y_a \le x_a + d_{\max}$. Predicted witness: the all-expensive
  routing. Hence this instance does NOT refute the Morell-Skutella cost-free conjecture.
- **H11 (C4, Conj 1.5 and TVZ24 survive).** Some routing is cost-good with violation at
  most $2 d_{\max}$. Predicted witness: the all-cheap routing, with
  $\alpha = 26/15 \le 2$. Since the instance is planar, a failure here would contradict
  Traub-Vargas Koch-Zenklusen, and the instance rather than the theorem would be wrong.
- **H12 (C3).** The digraph is not a source-plus-two-layers network: it has an $s$-$t$ path
  with at least 3 arcs.
- **H13 (C9, acyclicity, and the corollary cascade).** All costs are nonnegative, and the
  digraph is ACYCLIC. Acyclicity is what makes the refutation propagate to
  Conjecture 1.4 (Morell-Skutella with costs), since Conj 1.4 implies Conj 1.2 on acyclic
  instances, and to the convex-combination form.

**The independent second route (methodology/03 rung 1).**

- **H14 (structural derivation, no enumeration of costs).** Build the CONFLICT GRAPH $H$ on
  the three zero-cost path choices, joining two choices when EVERY completion of the third
  terminal violates some arc bound. Prediction: $H$ is a triangle. Then the maximum
  independent set of $H$ has size 1, so every congestion-good routing uses at least two
  expensive paths, so its cost is at least the sum of the two smallest expensive path costs
  $= 30 + 30 = 60$. This derivation reaches 60 WITHOUT costing the eight routings, and it
  must agree with the enumerated value of H4. Disagreement between the two routes would
  invalidate the experiment.
- **H15 (the invariant, RL1).** The fractional selection vector
  $\rho_i = x(\text{cheap choice } i)/d_i$ equals $(1/3, 2/5, 1/3)$ and violates the
  triangle stable-set inequality $\rho_1 + \rho_2 + \rho_3 \le 1$ with value exactly
  $16/15$. This is the invariant-first reading of the whole instance and is predicted to
  equal $\alpha_{\mathrm{inst}}$ numerically; whether that coincidence is structural or an
  artifact of this instance is NOT predicted here and is flagged as an open question for
  the verdict.

**The comparison (a report, not a method).**

- **H16.** Our independently computed numbers agree with the publicly reported ones (8
  routings, 4 congestion-good, fractional cost 58, minimum congestion-good cost 60). This
  is recorded as a comparison AFTER our own decision is made, never as an input to it. The
  proposer's verifier is not executed or imported at any point.

## Method

`run.py` re-enters the instance by hand, runs `ufclib` (adopted as ground truth by EXP-001)
for H1-H6 and H10-H13, runs the graph helpers for H7-H9, implements the independent
structural route for H14-H15 in fresh code, asserts every prediction, and tees the full
routing table to `artifacts/`. Exact rational arithmetic only; no floats; deterministic;
CPU only; no network.

## Success and failure criteria

- **Confirmed** if H1-H16 all hold: the claim is valid, and this repository holds an
  independent exact verification plus the quantitative content the announcement did not
  state.
- **Refuted** if the decision predictions fail in the direction that a congestion-good,
  cost-good routing DOES exist, or if the path enumeration finds paths the certificate did
  not consider. That outcome would mean the celebrated counterexample is wrong. It would be
  a much larger claim than confirming it, and per methodology/03 it would NOT leave this
  repository on the strength of one run: it would trigger a second independent
  implementation, a hand audit of every routing, and Felipe's decision on any external
  statement.
- **Inconclusive** if the instance is infeasible or malformed as transcribed, which would
  indicate a transcription problem on our side or in the bundle rather than a mathematical
  outcome; the transcription would be redone from the archived JSON hash and the experiment
  re-run.

## What this experiment cannot settle

Priority, attribution, and whether the mathematical community accepts the claim: those are
social facts and are outside the scope of any computation here. Also outside scope: whether
Goemans' conjecture holds with violation $O(d_{\max})$, which no single instance can
settle and which the literature calls the real breakthrough target.
