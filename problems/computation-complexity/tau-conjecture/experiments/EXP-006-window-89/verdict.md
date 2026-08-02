# EXP-006 verdict: WINDOW CLOSED: the minimal $\tau$ for 6 distinct integer roots is exactly 8

Run 2026-08-02, `run.py` (hunt first, then the times-case scan; smoke over
the depth-5 frontier returned the required empty answer), repo venv, exact
arithmetic; scan 2 h 23 min over all 25,844,905 depth-6 states (budget
3.5 h). Raw output: `artifacts/window.json`; witness verification:
`verify_witness.py` (run, all checks pass).

## The theorem this decides [MV, both directions]

**The minimum number of gates of a constant-free SLP computing a
polynomial with 6 distinct integer roots is exactly 8.**
Lower bound: $z_{\max}(7) = 5$ (EXP-004, decision-complete). Upper bound:
explicit verified witnesses, e.g. the 8-gate program
$$x{-}1;\ 2;\ q = x(x{-}1);\ 4;\ q{-}2;\ q{-}6;\ q(q{-}2);\ f = q(q{-}2)(q{-}6)$$
with $f$ having root set $\{-2,-1,0,1,2,3\}$ (three witnesses replayed
end-to-end by `verify_witness.py`, programs printed gate by gate).

## Prediction scorecard (committed before the run)

1. "The multiplication case is empty at 8 gates": **REFUTED**: the scan
   found 408 hits (states admitting an extension $v$ and operand $b$ with
   $|R_v \cup R_b| \ge 6$). This is the third time the exhaustive method
   has beaten our structural judgment (after EXP-003 and EXP-005), and
   the mechanism it found is instructive: the witness is exactly our
   9-gate schema $q(q-2)(q-6)$ computed one gate cheaper by CHAINED
   subtraction sharing: build constants $\{2, 4\}$ (2 gates), then
   $q-2$ and $(q-2)-4 = q-6$: the hunt's cost model built $\{2, 6\}$
   independently and missed the saving.
2. "The schema hunt finds no 8-gate 6-rooter": CONFIRMED (it found the
   6-rooter family but proved only 9 gates for it): the blind spot above
   is now a recorded cost-model lesson for the RL-8 moves calculus:
   subtraction CHAINS make constants cheaper than independent builds.
3. "All depth-7 five-rooter root sets equal $\{0,\pm1,\pm2\}$":
   **REFUTED**: the 67 five-rooters of $\tau \le 7$ realize SEVEN root-set
   patterns: $\{-2..2\}$ (39), the shifted blocks $\{-1..3\}$ (8),
   $\{-3..1\}$ (8), $\{0..4\}$ (4), $\{-4..0\}$ (4), and the
   NON-CONSECUTIVE $\{-1,0,1,2,4\}$ (2) and $\{-4,-2,-1,0,1\}$ (2).
   The non-consecutive patterns are new mechanism data (a five-rooter
   with a "hole" leaves room for a co-occurring factor to fill it).

## Census consequences

- Threshold table update: 3 roots at 3 gates, 4 at 5, 5 at 6, **6 at 8**.
- $z_{\max}(8) \ge 6$; the exact value of $z_{\max}(8)$ remains open
  (the full depth-8 census is TCB-005's goal). All 50 stored hits have
  union size exactly 6; whether any of the 408 hits reaches 7 was not
  retained (truncation) and is queued for a cheap re-scan (backlog).
- The sequence so far: $z_{\max} = 1, 2, 3, 3, 4, 5, 5, \ge 6$.

## Method note

The case-split reduction did its job: the multiplication case collapsed
to root-set co-occurrence (no polynomial arithmetic in the inner loop)
and was decided EXACTLY in one scan; the $\pm$ case, which the SAT design
note (2026-08-02) was written for, turned out not to be needed for the
threshold: the window closed on the $\times$ side. The SAT lane is
rescoped to future targets ($z_{\max}(8)$ exact; deeper thresholds).

## Adversarial validation record

- Smoke: the identical scan one depth down returned EMPTY, as implied by
  $z_{\max}(7) = 5$: a known-answer test of the whole pipeline.
- Frontier gates: depth 1-6 state counts reproduced exactly (including
  the 25,844,905).
- Witnesses: three hits reconstructed as EXPLICIT 8-gate programs by
  restricted DFS and replayed in exact arithmetic; root sets confirmed.
- The hit list (first 50) and the five-rooter root-set summary are in
  the committed artifact.

## How could this be wrong?

The scan's soundness rests on the last-gate lemma at depth 8 plus claim
1 (final gate must involve the 7th value, else $z \le z_{\max}(7)$),
both proved in the hypothesis; completeness of the $\times$ case rests
on roots-of-product = union-of-roots (exact for distinct counts). The
witness verification is independent of the scan machinery (restricted
DFS + direct evaluation), so the POSITIVE claim (threshold = 8) does
not depend on the scan's correctness at all: only the (now moot for the
threshold) emptiness questions did.

## Consequences for the strategy

- TCB-021 RESOLVED: min $\tau$(6 roots) = 8. Ships as a Zenodo NEW
  VERSION of the census paper (v0.02) together with the corrected
  five-rooter taxonomy.
- New questions minted: does an 8-gate SEVEN-rooter exist (union-7
  re-scan, cheap with hit retention); the 7-roots threshold (in
  $[9, ?]$: upper witness needed); non-consecutive record root sets as
  a mechanism class (anatomy lens).
- RL-8 cost model upgraded: chained-subtraction constant sharing.
