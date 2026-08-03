# tau-conjecture: approaches re-evaluation addendum (round 8, 2026-08-02)

Third route re-ranking, after the window closed (EXP-006). Extends the
r4/r5 addenda.

## What EXP-006 changed about the ranking

1. **Co-occurrence is now a first-class primitive.** The times-case
   reduction (product roots = union of root sets) converted a threshold
   decision from ~$10^{11}$ polynomial operations into root-set lookups
   over the frontier. Lesson generalized: for any final-gate question,
   look first for a gate whose OUTPUT invariant is a function of operand
   invariants (multiplication: root sets; NOT addition). The census
   should permanently carry per-state root-set profiles.
2. **Third refutation of a structural emptiness judgment.** EXP-003
   (multiply-by-$x$), EXP-005 (2-cycles), EXP-006 (chained subtraction
   sharing): each time the exhaustive method found a sharing trick our
   models missed. Policy consequence (standing): treat OUR OWN cost
   models as upper-bound generators only; never let them argue
   emptiness; predictions may lean on them but stay explicitly moderate.
3. **The hunt's corrected cost model** (chained constants) upgrades the
   RL-8 moves calculus: subtraction chains make arithmetic progressions
   of constants nearly free after the first (one gate per additional
   term with shared differences).

## New view V9 (this round's exploration deliverable): the digit census

Rojas Theorem 1 [V, read in full]: bounding only the roots
$\equiv 1 \pmod p$, for ONE fixed prime, polynomially in $\tau$ already
implies the whole tau conjecture. Nobody (both sweeps) has measured
that restricted growth function. V9 instruments the census catalog with
per-digit-class root counts: the ladders
$z^{(p,1)}_{\max}(\tau)$ for $p = 2, 3$ (EXP-007). This is strictly
finer data than $z_{\max}$: the conjecture would follow from a
polynomial bound on ONE of these ladders, so their measured growth is
the closest census-shaped object to the actual open statement. Smoke
data already shows the odd-root ladder reaching 3 by $\tau = 6$ (one
step behind the full ladder's 5): the digit restriction is measurably
harder to grow, consistent with Rojas' intuition that the digit form
concentrates the difficulty.

## Standing ranking (updated)

1. RL-1 census spine: EXP-007 (running); then exact $z_{\max}(8)$ via
   the $\pm$ case (SAT lane, design note ready) or TCB-005 backend.
2. V9 digit census: ships with EXP-007; extend per-depth and per-prime
   as standard instrumentation of every future census level.
3. RL-8 moves calculus with the corrected cost model: now credible as a
   certified upper-bound generator for the $T(S)$ table and the 7-root
   threshold hunt.
4. RL-5 integer frontier (Markstroem extension): unchanged, ready when
   a long-run slot is free.
5. Reads: KPT15 still TO FETCH (two sweeps returned only the arXiv
   listing; fetch the PDF next round); Narkiewicz attribution status
   upgraded: the cycle fact is stated as common knowledge in the
   current literature (e.g. Best-Dynes-Miller-Powell-Weiss 2015 state
   it without attribution), standard treatment Narkiewicz LNM 1600:
   our citation practice (classical + self-contained proof) is correct.

## Postscript (round 8, second sweep): view V10, the three worlds

Context note `2026-08-02-three-worlds-view.md`: the same SLP read over
F_p / R / Z gives maximal-violation / violation / conjectured-polynomial
root growth; both failures come from a cheap coincidence-rich
endomorphism (Frobenius; the doubling semiconjugacy), and Z has none:
the stall theorems are the quantitative form of that absence, so the
conjecture reduces (as a mechanism statement) to pricing
constant-building: exactly what the census and the digit ladders
measure. Adjacent literature (finite-field SPARSE root bounds:
Bi-Cheng-Rojas Descartes; arXiv:1411.6346) attacks term count, not SLP
length; the trichotomy framing appears unclaimed. New cheap
instrumentation queued: mod-p root counts of census records vs the
Frobenius ceiling (backlog row TCB-027).
