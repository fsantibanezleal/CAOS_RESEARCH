# EXP-001 verdict: the exact SSUF instance checker

Run 2026-07-24 with the repo `.venv` (Python 3.13.0), CPU only, no randomness, no network.
Artifacts: `artifacts/run-log.txt` (the full tee'd run).
Reproduce from the repository root:

```
.venv/Scripts/python.exe problems/optimization-geometry/unsplittable-flow-cost/experiments/EXP-001-exact-instance-checker/run.py
.venv/Scripts/python.exe -m pytest problems/optimization-geometry/unsplittable-flow-cost/code/ufclib/tests/ -q
```

## Verdict: CONFIRMED

All eight declared predictions hold, after one specification error in P8 that is recorded
in full below rather than quietly patched. The checker is adopted as the programme's
ground truth (plan.md, UF-P0). The pytest suite (14 tests) is the permanent regression
gate.

## Exact-arithmetic status

Exact throughout. Every demand, arc load, cost, bound and reported quantity is a
`fractions.Fraction`; the constructor REFUSES `float` inputs with a `TypeError` rather than
coercing them, and a token-level scan of `ufclib/*.py` plus `run.py` confirms there are no
float literals outside a single, explicitly marked negative control. There is no
floating-point path anywhere in this problem's machinery, so no verdict here rests on
rounding.

## What the machine reported

| id | paths | routings | congestion-good | min cost among them | alpha_instance | good routing exists |
|---|---|---|---|---|---|---|
| V1 direct expensive vs free detour | {t: 2} | 2 | 2 | 0 | 1/2 | yes |
| V2 parallel arcs | {t: 2} | 2 | 2 | 0 | 1/2 | yes |
| V3 congestion never binds, rational loads | {t: 2} | 2 | 2 | 1 | 1/2 | yes |
| V4 tight boundary | {t1: 2, t2: 1} | 2 | 2 | 0 | 0 | yes |
| V5 with a directed cycle | {t: 3} | 3 | 3 | 0 | 1/2 | yes |

Prediction by prediction:

- **P1 enumeration completeness: PASS.** Every path count matched the hand count fixed in
  `hypothesis.md`, including V5's three paths (the count that was corrected in the
  hypothesis table before the run, and recorded as corrected there).
- **P2 routing count: PASS.** Products of per-terminal path counts throughout.
- **P3 feasibility is actually checked: PASS.** The corrupted V1 was rejected with
  "conservation fails at s: divergence 3, expected 2", and all five valid instances were
  accepted. A checker that accepted the corrupted instance would have been useless, so
  this negative control matters more than the positive ones.
- **P4 the DGG floor: PASS.** At least one congestion-good routing exists on every
  instance, as the Dinitz-Garg-Goemans theorem forces. This is the cheapest available
  self-check on instance data and stays wired into the pytest suite.
- **P5 the known answers: PASS.** Both the existence of a simultaneously congestion-good
  and cost-good routing and the exact minimum congestion-good cost matched the values
  fixed by inspection (0, 0, 1, 0, 0).
- **P6 boundary inclusivity: PASS.** On V4 the routing through `m` loads arc `u->m` to
  exactly `x + d_max = 0 + 1 = 1` and is classified congestion-good, with
  `alpha = 1` exactly. An exclusive reading of the inequality would have misclassified it,
  and would have silently manufactured counterexamples later.
- **P7 cycles: PASS.** The enumerator terminated on the cyclic V5, returned exactly the
  three simple paths, and `is_acyclic` returned False on V5 and True on V1-V4.
- **P8 exactness: PASS after a corrected scan** (see below).

## The P8 specification error (recorded, not patched away)

As written in `hypothesis.md`, P8 asserted that a scan of the experiment code finds no
float literals. The first run FAILED that assertion, and the failure was correct: the
scan found `1.0` at `run.py:255`, inside the negative control whose entire purpose is to
feed a float to the constructor and observe that it is refused. The prediction as phrased
was therefore unsatisfiable together with the test it was meant to protect.

What was changed, and what was not: the SCAN was narrowed to allow float literals on lines
explicitly annotated `float-literal-ok` in the source, of which there is exactly one, and
the hypothesis file was left untouched. The substantive content of P8 (no float arithmetic
anywhere in the library or the experiment) was never weakened, and the two stronger clauses
of P8 (the constructor refuses floats; every reported quantity is a `Fraction`) passed on
the first run without modification. This is logged here because a session that adjusts a
check after seeing it fail owes the record an explicit account of what moved.

## Adversarial validation

Rung 4 of methodology/03 (stress families engineered to break the finding) is what this
whole experiment is:

- **Parallel arcs (V2).** A checker keyed on `(tail, head)` pairs, which is the obvious
  implementation and is what the proposer's archived verifier uses, finds ONE path here
  and would report one routing instead of two. Our arc-indexed model finds two. This is a
  real divergence in the models, and it is the reason ours is arc-indexed.
- **Directed cycles (V5).** A naive path enumerator that guards on arcs rather than
  vertices does not terminate. Ours guards on vertices and terminates, returning the
  genuinely new third path that the cycle creates.
- **The tight boundary (V4).** An off-by-one in the inequality direction changes the answer
  on an instance engineered to sit exactly on the bound.
- **A corrupted flow (P3).** Feasibility checking is verified to reject, not merely to
  exist.
- **The DGG floor (P4).** An independent theorem is used as an oracle on every instance: if
  our enumeration ever reports zero congestion-good routings, the data or the code is
  wrong, since the theorem is not.

## How could this be wrong?

Residual failure modes this experiment does NOT exclude, stated plainly:

1. **Correct on small instances, wrong on large ones.** Every validation instance has at
   most three paths per terminal. Nothing here tests behaviour at the scale the minimality
   exhaustion (UF-P2) will need, where the routing count is a product over many terminals.
   Performance and memory are untested, and a future experiment that needs scale must
   re-validate at that scale.
2. **The simple-path restriction is argued, not machine-proved.** The hypothesis records
   the derivation (appending a cycle adds load and, since costs are nonnegative, adds cost,
   so a non-simple routing is never better). The argument is elementary and was re-checked
   by hand, but the code does not verify it; it assumes it by only enumerating simple
   paths. If a future statement in this programme ever concerns walks rather than paths,
   this assumption must be revisited explicitly.
3. **Agreement with the conjecture's exact wording rests on our transcription.** The
   inequalities implemented are inclusive and measured against `x`, per the literature
   dossier's verbatim transcription of Conjecture 1.2. If that transcription were wrong,
   every downstream verdict would be wrong in the same way. It was taken verbatim from
   arXiv:2510.21287 and cross-read against arXiv:2308.02651 and arXiv:2412.05182, which is
   the strongest control available short of the Combinatorica original (UFB-002).
4. **The graph-class helpers are only lightly exercised here.** `has_k4_subdivision` and
   the Kuratowski-by-degrees planarity test have unit tests but have not yet been run on a
   graph where the answer is contested. They carry no weight until EXP-002 uses them, and
   the planarity helper deliberately returns `None` rather than guessing when the degree
   argument does not settle the question.

## Consequences for the strategy

The checker exists and is trusted at small scale, so UF-P1 may proceed: EXP-002 adjudicates
the 2026 claimed counterexample using this machinery and nothing else. The two instruments
EXP-002 additionally needs (the K4-subdivision detector and the demand-multiplicity
predicate) are implemented and unit-tested here. The instruments the later rungs need (the
exact rational separation LP, UFB-010; the canonical form, UFB-011) are NOT built and are
not implied by this verdict.
