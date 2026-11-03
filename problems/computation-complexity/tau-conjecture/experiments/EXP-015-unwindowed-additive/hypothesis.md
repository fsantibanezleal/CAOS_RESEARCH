# EXP-015: the additive nine-gate case without a window (TCB-039)

Declared 2026-11-02, before the production run. The instrument (engine, filter
library, residue tables, probe) was built and gated on samples first; no
production partition has been scanned when this file is committed.

## Question

EXP-013 decided the additive ninth gate only for seven-rooters whose seven roots
all lie in [-32, 32]. EXP-014 priced the rest: a seven-rooter outside the window
needs a trailing coefficient |c| >= 396, about 0.002% of the nonzero candidates
in a four-partition sample, and that class was never scanned (TCB-039).

Is there a depth-7 state, an eighth gate t on its 10 operands (inputs -1, 1, x
and the 7 state values), an operand b and a sign such that f = t + b or
f = t - b has 7 distinct integer roots ANYWHERE in Z?

A "no" closes the additive case without a window. With EXP-012 (multiplicative
ninth gate, unconditional) and EXP-011 (z_max(8) = 6, so a nine-gate
seven-rooter's last gate involves the eighth value), it gives z_max(9) = 6 and a
seven-root threshold of exactly 10 (the two ten-gate seven-rooters of TCB-032
give the upper side).

## Method

The lemma (code/tclib/padic.py). If a nonzero f in Z[x] has distinct integer
roots r_1..r_k and f = x^m g with g(0) != 0, then prod (x - r_i) divides f, so
for every prime p, every integer n with f(n) != 0 and every 0 <= m' <= m,

    v_p(f(n)) - max(m' - 1, 0) v_p(n) >= sum_i v_p(n - r_i).

Summed over a block of p^a consecutive points, the right-hand side has a least
value over all placements of k distinct integer roots that depends only on which
block points have f(n) == 0 mod p^e (the zero mask). That least value is the
table LB_k[mask]; a candidate whose left-hand sum is smaller has fewer than k
distinct integer roots. No window is involved: the roots may lie anywhere.

The engine (engine.py) applies, in order, to every candidate of every state:

1. degree: deg f <= max(deg t, deg b) (deg t exact for products, at most the
   max for sums and differences); below 7 the candidate is dropped;
2. the 2-adic layer: 16 points -8..7, residues mod 2^64 (uint64 arithmetic,
   exact), with m' the proven lower bound on the power of x (minimum of trailing
   indices, sum for a product);
3. the 3-adic layer: 9 points -4..4, residues mod 3^20, on the survivors;
4. a survivor whose residues vanish at all 25 points is tested for f == 0
   exactly, from the exact operands (cached by operand ids);
5. every other survivor is built exactly and its distinct integer roots are
   counted by the rational root theorem (tclib.enum.integer_roots).

Residues, degrees and trailing indices of the 2,161,049 interned polynomials are
precomputed by residues.py (0 mismatches against exact Python evaluation on
20,000 random polynomials).

## Gates, run before production (outputs in artifacts/)

- Unit tests (code/tclib/test_padic.py): planted k-rooters (k = 4..7, roots up to
  5000 in absolute value, x-powers, 2- and 3-power content) are never rejected,
  for every m' <= m; random dense polynomials are rejected; modular arithmetic
  is exact.
- Known-answer gate: on sampled states, the engine at threshold K must report
  exactly the number of candidates with >= K distinct integer roots found by
  building EVERY candidate exactly (no filter). Already passed on design
  samples: K = 4, 150 states of partition 0, 325 = 325; K = 5, 300 states of
  partition 73, 2 = 2. Before production it is re-run on further partitions
  and recorded.
- Integrity: each frontier file's SHA-256 must equal the EXP-011 manifest before
  it is scanned (the copy comes from the data drive marked read-only).

## Completeness audit (after production)

All 256 partitions present, each with its manifest SHA-256 and its manifest state
count; the states total 1,048,460,912; per-partition stage counters sum
consistently (candidates = 4000 x states).

## Falsifiable prediction

Production at threshold 7 finds NO additive nine-gate seven-rooter. Basis:
EXP-013 found none in the window and EXP-014 measured the out-of-window class as
small (122 window-limited candidates in 6.4 million). Confidence MODERATE: the problem's record of refuted predictions is long.

If a hit is found: it is verified by exact construction, the seven roots are
substituted, and the result is z_max(9) = 7 (threshold 9), the opposite outcome.

## Scope

The candidate space is EXP-013's (same frontier, same 200 eighth gates, same 10
operands, both signs). The reduction to this space rests on EXP-011 (complete
depth-7 frontier, z_max(8) = 6) and EXP-012, which are earlier verdicts and are
not re-derived here.
