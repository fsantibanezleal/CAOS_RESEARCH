# EXP-008: the final-$\pm$ residual at depth 8, by SMT (resolves $z_{\max}(8)$)

Declared 2026-08-03 (round 9), before the run. Actions TCB-029 per the
SAT-lane design note (2026-08-02), encoding (1)/(2).

## Question

Does an 8-gate constant-free SLP whose FINAL gate is $+$ or $-$ (and
involves the 7th value; the $\times$ case is excluded by EXP-007) compute
a polynomial with 7 distinct integer roots? If NO: $z_{\max}(8) = 6$
(EXP-006 lower + EXP-007 exclusion + this), the third exact census value
beyond the last stored frontier.

## Encoding (evaluation form; soundness class stated)

Structure variables per gate ($op_j \in \{+,-,\times\}$, operand
selectors over inputs $\{-1, 1, x\}$ and earlier gates, commutative
symmetry-break $L \le R$); SEVEN integer root variables
$r_1 < \dots < r_7$; evaluation variables $E[i][t]$ = value of item $t$
at $x = r_i$, with gate semantics as guarded equalities; final gate
constrained to $\pm$ involving gate 7; $E[i][\text{out}] = 0$ for all
$i$. No polynomial coefficients are represented: evaluations only.

- The structure space is a SUPERSET of normalized programs, so UNSAT
  proves the theorem over ALL programs. [D]
- The one unsound-for-SAT hole: $f \equiv 0$ vanishes everywhere.
  Handled by CEGAR: every SAT witness is replayed EXACTLY through tclib;
  a zero polynomial (or any mismatch) adds a blocking clause on the
  structure assignment and re-solves. A surviving witness is verified
  independently of the solver. [D]
- Variant (2): $|r_i| \le 32$ (bounded-root, partial); variant (1):
  unbounded (full theorem strength). UNSAT in (1) is a complete proof;
  UNSAT in (2) only a window statement; `unknown` is a recorded outcome.

## Known-answer validation (committed; runs FIRST)

The same encoding with SIX roots and the final gate UNRESTRICTED must
return SAT, and its CEGAR-replayed witness must be a genuine 8-gate
6-rooter (EXP-006 guarantees existence). If this fails, the encoding is
broken and nothing downstream is trusted.

## Falsifiable predictions

1. The known-answer test passes (SAT + valid replay).
2. The 7-root final-$\pm$ instance is UNSAT in the bounded variant.
3. It is UNSAT (or, acceptably, `unknown`) in the unbounded variant;
   we PREDICT UNSAT, i.e. $z_{\max}(8) = 6$. Confidence moderate (the
   record: one surviving emptiness prediction out of four; but here the
   $\pm$ gate destroys root-set structure rather than composing it, and
   no census signal points the other way).

## One-sidedness

Bounded UNSAT alone leaves $z_{\max}(8) \in \{6\} \cup \{7+\ \text{via
roots outside } [-32,32]\}$: reported as partial. Unbounded UNSAT closes
$z_{\max}(8) = 6$ and (with EXP-006/007) makes the seven-root threshold
$\ge 9$. A SAT witness (after replay) would give $z_{\max}(8) \ge 7$:
a discovery either way.

## Premise dependencies (P3)

EXP-006/007 verdicts (the $\times$ exclusion and the 408 anchor); the
last-gate lemma; tclib (replay only). z3-solver 4.16.0 in the repo venv.

## Budget and kill (P6)

Known-answer: 30 min cap. Bounded 7-root: 2 h cap. Unbounded: 3 h cap;
solver `unknown` or timeout recorded as such (not a failure). Total
budget 6 h; each phase checkpoints its result immediately.

## Success criteria

CONFIRMED if the known-answer passes and at least the bounded variant
resolves; the verdict reports each variant's exact status. REFUTED
(tooling) if the known-answer fails.

## Amendment (2026-08-19, before the re-run; the first launch died with the session)

The first launch's known-answer phase did not complete within its cap
(plain NIA struggles even at 6 gates / 5 roots / bound 8), and the
process died with the session teardown before any checkpoint. Redesign,
recorded before the re-run:

1. Known-answer gains an intermediate-VALUE bound ($|E| \le 10^9$):
   harmless for a SAT-side validation (it only shrinks the witness
   space, and known witnesses have tiny values).
2. Phase ladder for the 7-root final-$\pm$ question:
   (a) root-bounded ($|r| \le 32$), values unbounded, QF_NIA, 2 h cap;
   (b) if (a) is unknown: doubly-bounded ($|r| \le 32$, $|E| \le
   10^{12}$), 1 h cap: its UNSAT is a windowed partial, stated as such;
   (c) unbounded attempt, 2 h cap, `unknown` acceptable and recorded.
3. Solvers created via SolverFor("QF_NIA").
Soundness classes are unchanged from the original declaration; only
tractability engineering moved. If even (b) returns unknown, the
residual routes to the depth-8 census backend (TCB-005) and this
experiment reports INCONCLUSIVE with the solver record.

## Amendment 2 (2026-08-19, before the second re-run)

The re-run's known-answer phase entered a DEGENERATE CEGAR loop: 179,649
consecutive zero-polynomial models in 6.7 h (the blocking clause removes
one structure per iteration from a sea of trivial zero-producers), and
the loop had no iteration budget (the phase cap was implemented only as
the per-check solver timeout). Two fixes, recorded before the re-run:

1. STRUCTURAL nonzero constraint: one additional evaluation column at a
   fresh integer variable $y$ with $E_y[\mathrm{out}] 
e 0$. This
   excludes exactly the zero polynomial (any nonzero $f$ has an integer
   non-root) and nothing else, so soundness classes are unchanged; CEGAR
   remains only as a verification backstop.
2. Loop budgets: at most 50 blocked models per phase AND a wall-clock
   cap per phase enforced in the loop; hitting either records the phase
   as INCONCLUSIVE(budget) rather than looping.
Lesson recorded for the audit trail: a per-check solver timeout is not a
phase budget; CEGAR needs its own kill criterion (methodology 12 P6
applies to LOOPS, not just runs).
