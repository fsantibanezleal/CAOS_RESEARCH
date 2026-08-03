# EXP-007: 8-gate seven-rooters (full-retention re-scan) and the digit census

Declared 2026-08-02 (round 8), before the run. Actions TCB-025 and the
new view V9 (digit census; this round's exploration deliverable).

## Questions

1. (Exact, TCB-025) Among ALL final-multiplication 8-gate polynomials
   (the EXP-006 scan space), what is the maximum root count: does an
   8-gate SEVEN-rooter with final gate $\times$ exist? EXP-006 retained
   only 50 of its 408 hits and no union sizes beyond the $\ge 6$ flag;
   this re-scan retains every hit with its union size.
2. (New instrumentation, V9) The DIGIT CENSUS: Rojas proved that
   bounding only the roots $\equiv 1 \pmod p$ (any fixed prime)
   polynomially in $\tau$ already implies the full tau conjecture. We
   measure the exact bottom of that SUFFICIENT statement: for
   $p \in \{2, 3\}$, the ladder
   $z^{(p,1)}_{\max}(\tau) = \max\{\#\{r \in R_f : r \equiv 1 \bmod p\} :
   \tau(f) \le \tau\}$ for $\tau \le 7$, from the census catalog's root
   sets (cheap: no new enumeration).
3. (Observational, TCB-026 feed) Save the 67 five-rooter POLYNOMIALS
   (EXP-006 kept only their root-set summary) for the punctured-set
   anatomy pass.

## Falsifiable predictions (committed before the run)

1. Max union size = 6: NO 8-gate seven-rooter with final $\times$.
   Reasoning: a union of 7 needs (5,2)-or-(4,3)-type disjointness, and
   the observed five/four-rooter root sets crowd the same small
   integers; but three prior emptiness-style judgments of ours were
   refuted (EXP-003/005/006), so confidence is explicitly moderate:
   the scan decides.
2. $z^{(2,1)}_{\max}(7) = 3$ (odd-root count at most 3 through depth 7),
   with the value 3 first attained at or before $\tau = 7$ (the shifted
   five-blocks $\{-1,0,1,2,3\}$ carry odd roots $\{-1, 1, 3\}$).
3. No commitment on question 3 (anatomy is post-hoc).

## One-sidedness

Question 1 is decision-complete for the final-$\times$ case at 8 gates
(both outcomes exact); it does NOT decide $z_{\max}(8)$ (the final-$\pm$
case remains; SAT lane). Question 2 is decision-complete for the digit
ladders at $\tau \le 7$ given the catalog (the catalog itself is
decision-complete by EXP-001..004).

## Premise dependencies (P3)

EXP-004 catalog and gates; EXP-006 machinery (this is the same scan with
full retention); Rojas Thm 1 [V, read in full] motivates question 2 but
is not a premise of any computation.

## Invariant-first note (P5)

Question 2 IS an invariant measurement (a digit-restricted count);
question 1 has no cheaper decider than the scan (the co-occurrence
reduction is already the invariant-first form of the $\times$ case).

## Compute budget and kill criterion (P6)

- Smoke (P2): depth-5-based scan must reproduce EXP-006's smoke (zero
  hits) and the digit pass must run on the $\tau \le 5$ catalog with a
  progress line and checkpoint.
- Budget: 3.5 h wall. Kill at 3 h inside the scan: checkpoint coverage
  fraction; report question 1 PARTIAL.
- Expected: scan ~2.5 h (EXP-006 measured 2h23m); digit pass minutes.

## Success and failure criteria

- CONFIRMED: scan complete (question 1 decided either way) + digit
  ladders computed; predictions scored separately.
- INCONCLUSIVE: kill hit (partial coverage reported).
- REFUTED (tooling): any frontier-gate mismatch, or hit count at
  union $\ge 6$ differing from EXP-006's 408.
