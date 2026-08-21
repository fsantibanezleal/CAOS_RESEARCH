# EXP-012: does a 9-gate SEVEN-rooter exist (final gate $\times$)? The $\{9,10\}$ window

Declared 2026-08-20, before any run. Actions TCB-032. Decides the
multiplication case of the seven-root threshold, exactly, using the
depth-7 frontier asset built by EXP-011.

## The reduction (same shape as EXP-006, one level up) [D]

Let $\tau(f) = 9$ with $z(f) \ge 7$. Its first 8 gates form a depth-8
state; by the last-gate lemma the final gate must involve the 8th gate
value $v_8$, because otherwise $f$ is computable in 8 gates and
$z(f) \le z_{\max}(8) = 6$ (EXP-011). If that final gate is a
MULTIPLICATION then $f = v_8 \cdot b$ with $b$ an operand, and
$$z(f) = |R_{v_8} \cup R_b|,$$
a union of two known root sets. Every depth-8 state is one gate over a
depth-7 state, so the question becomes: is there a depth-7 state $S_7$,
a one-gate extension $v_8$, and an operand $b \in S_7 \cup \{-1,1,x\}$
with $|R_{v_8} \cup R_b| \ge 7$? The stored frontier
($1{,}048{,}460{,}912$ states) makes this decidable exactly.

Cost note from EXP-011's histogram: among $2.08 \times 10^{11}$
depth-8 op-results only $929{,}780$ have $z = 5$ and $328$ have $z = 6$;
with $|R_b| \le z_{\max}(7) = 5$, the union test needs
$z(v_8) \ge 7 - \max_b z(b)$, so the extra work over EXP-011's scan is
negligible.

## Phases

- **A (hunt, seconds)**: the $(6,1)$ sub-case on stored data: for each
  recorded 8-gate 6-rooter witness, is ANY operand of its depth-8 state
  (inputs, the six state values, $v_7$, and $f_8$ itself) a polynomial
  with a root OUTSIDE $R_{f_8}$? If yes, a 9-gate 7-rooter exists
  immediately.
- **B (scan, ~7 h detached, 20 workers)**: the exact decision over the
  whole depth-7 frontier, with the pruning above; per-partition
  checkpoints, resumable, known-answer gated (below).

## Known-answer gate (runs first inside B)

The identical scan with threshold 6 instead of 7 must find hits (the
EXP-006 8-gate six-rooters are exactly the threshold-6 hits one level
down); we run the threshold-6 variant on ONE partition and require a
nonzero hit count before the threshold-7 sweep is trusted.

## Falsifiable predictions (committed)

1. Phase A finds nothing (the 8-gate 6-rooter states spend all gates on
   the 6-rooter; in the $q$-family every operand's roots lie inside
   $R_{f_8}$).
2. Phase B finds NO 9-gate 7-rooter via $\times$. Hence (with the $\pm$
   case still open) the threshold is 10 unless a final-$\pm$ 9-gate
   7-rooter exists. Emptiness commitment number SEVEN; our record is
   2-for-6, so confidence is explicitly MODERATE and the machine
   decides.
3. If B is empty, the strongest honest statement becomes: the
   seven-root threshold is 10 for multiplicative last gates, and lies
   in $\{9, 10\}$ in general.

## One-sidedness

B is decision-complete for the $\times$ case. A hit RESOLVES the window
at 9 (with an explicit witness to replay). Emptiness leaves only the
final-$\pm$ case at 9 gates, which needs either a ~$4\times10^{10}$-state
depth-8 frontier (~1.1 TB) or a different idea; that residual is stated,
not hidden.

## Premises (P3)

EXP-011 ($z_{\max}(8) = 6$ and the stored frontier, cross-anchored);
the last-gate lemma; tclib arithmetic (sympy cross-checked).

## Budget and kill (P6)

Phase A: 5 min. Phase B: 12 h cap, 20 workers, disk-resident frontier
(read-only), per-partition JSON checkpoints; on budget kill report
coverage and the partial (lower-bound) reading.
