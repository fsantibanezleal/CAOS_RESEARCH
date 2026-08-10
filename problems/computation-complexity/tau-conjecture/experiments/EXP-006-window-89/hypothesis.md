# EXP-006: the [8,9] window, part 1: the multiplication case decided exactly, plus the construction hunt

Declared 2026-08-02, before the run. Actions TCB-021 (the standing
decision-bearing question after EXP-004): is the minimal $\tau$ with 6
distinct integer roots equal to 8 or to 9?

## The case-split reduction (method contribution, [D], proved here)

Let $f$ have $\tau(f) = 8$ and $z(f) \ge 6$. By the last-gate lemma
(EXP-003) applied at depth 8, $f = a \circ b$ over the operands of a
normalized depth-7 state $T = S \cup \{v\}$, where $S$ is a normalized
depth-6 state and $v$ its 7th-gate value.

CLAIM 1: the final gate must involve $v$. If $a, b \in S \cup \{\text{inputs}\}$
then $f$ is computable in 7 gates ($S$'s program plus one), so
$z(f) \le z_{\max}(7) = 5$ (EXP-004): contradiction.

CLAIM 2 (the multiplication case is combinatorial): if the final gate is
$\times$, then $f = v \cdot b$ with $b \in S \cup \{\text{inputs}\}$
($b = v$ gives $z(v^2) = z(v) \le 5$), and
$z(f) = |R_v \cup R_b|$ where $R_g$ is the set of distinct integer roots
of $g$ (roots of a product = union of root sets; multiplicity is
irrelevant to distinct counts). Both $R_v$ and $R_b$ are root sets of
polynomials of $\tau \le 7$, already characterized by the census. Hence
the existence of an 8-gate 6-rooter WITH FINAL GATE $\times$ is decided
by a pure co-occurrence query over the depth-6 frontier: does some
depth-6 state $S$ admit an extension $v$ and an operand $b$ with
$|R_v \cup R_b| \ge 6$? No polynomial arithmetic beyond the (memoized)
root sets is needed.

## Questions

1. (Exact) Does an 8-gate 6-rooter with final gate $\times$ exist?
2. (One-sided hunt) Does a grammar-restricted construction search: split
   quadratic products $(q - c_1)(q - c_2)(q - c_3)$ and their DOS/shift
   variants, with EXPLICIT generated programs and exact gate counts:
   find any 8-gate program with 6 distinct integer roots?
3. (Observational) The root sets of the depth-7 five-rooters: are all 63
   equal to $\{0, \pm 1, \pm 2\}$?

## Falsifiable predictions (committed before the run)

1. NO: the multiplication case is empty at 8 gates. Reasoning: five-rooter
   root sets appear to be exactly the stable core $\{0,\pm1,\pm2\}$, and
   producing a co-occurring value with a root outside the core requires
   built constants that the 7-gate budget does not leave room for; but
   after EXP-003 this is a judgment, not knowledge: the scan decides.
2. NO: the hunt finds no 8-gate 6-rooter (our best schemas cost 9).
3. YES: all 63 depth-7 five-rooter root sets equal $\{0, \pm 1, \pm 2\}$.

## One-sidedness (P4)

Question 1 is decision-complete for its case: a PASS (no hit) PROVES no
8-gate 6-rooter ends in a multiplication; a hit closes the window at 8.
Question 2 is one-sided: failure of the hunt proves NOTHING about the
$\pm$ case (the remaining sliver). If both come back negative, the
honest state becomes: min $\tau$(6 roots) $\in \{8, 9\}$ still, with
"8" possible ONLY via a final addition/subtraction gate: a crisp,
SAT-shaped residual question (declared follow-up EXP-007, RL-7).

## Premise dependencies (P3)

- Last-gate lemma (EXP-003 [D]); $z_{\max}(7) = 5$ (EXP-004 verdict);
  the interned engine's anchors (EXP-004 gates all green).
- Root sets memoized per polynomial id, computed by the same exact
  divisor argument used throughout (cross-checked vs sympy in round 3).

## Invariant-first note (P5)

Claim 2 IS the invariant-first move: it converts one of the two final-
gate cases from $10^{11}$ polynomial operations into root-set lookups.
No comparable reduction was found for $\pm$ (roots of a sum are not a
function of the summands' roots); hence the case split.

## Compute budget and kill criterion (P6)

- Smoke (P2): the same scan run one level down (depth-5 frontier
  deciding "7-gate 6-rooter with final $\times$") must return EMPTY
  (implied by $z_{\max}(7) = 5$) and must reproduce the depth-6 frontier
  gates; progress lines + checkpoint required.
- Part 2 (hunt): minutes; runs first.
- Part 1 (scan): budget 3.5 h wall single-core (the EXP-004 scan took
  69 min; this adds root-set lookups). Memory guard 30M states. Kill: at
  3 h inside the scan: checkpoint states-scanned and report the $\times$
  case PARTIAL (with the fraction covered); the window stands.

## Success and failure criteria

- Part 1 CONFIRMED if the scan completes (either outcome decides the
  $\times$ case); prediction 1 scored separately.
- Part 2 reported as found/not-found (one-sided).
- REFUTED (tooling) on any anchor-gate mismatch.
