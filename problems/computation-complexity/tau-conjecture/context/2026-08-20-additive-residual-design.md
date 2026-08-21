# Design note: deciding the ADDITIVE residual at depth 9 (EXP-013 groundwork)

Dated 2026-08-20, written while EXP-012 (the multiplicative case) runs, so
the route is ready either way. Method design only; no claims.

## The residual

If EXP-012 returns empty, a 9-gate 7-rooter can only have a final gate
$+$ or $-$: $f = v_8 \pm b$, with $v_8$ the 8th gate value and $b$ an
operand of the depth-7 state. Root sets do NOT compose across addition,
so the co-occurrence trick that decided both the depth-8 threshold and
the multiplicative case here does not apply. The naive cost is the full
product: about $10^9$ states $\times$ 130 extensions $\times$ 10
operands $\times$ 2 signs $= 2.6 \times 10^{12}$ polynomial
constructions plus root counts, roughly 90 hours at our measured
throughput. Too expensive as stated.

## The evaluation-window reduction (V11 in operational form)

Work with VALUES, not polynomials. Fix the window
$W = \{-32, \dots, 32\}$ (every census record ever observed has all
roots in $[-4, 4]$, so this is generous). For a state:

1. Evaluate each of the 10 operands (3 inputs + 7 state values) on all
   65 points of $W$: a $10 \times 65$ integer matrix, built once per
   state by table lookup (the value vectors of catalogued polynomials
   can be precomputed ONCE globally for the whole 2.16M-polynomial
   catalog: a $2.16\text{M} \times 65$ int64 table is 1.1 GB, or
   computed per worker for the ids actually used).
2. Every extension $v_8 = a \circ c$ has its value vector obtained by
   one vectorized operation on two rows.
3. $f = v_8 \pm b$ vanishes at $r \in W$ iff the corresponding entries
   satisfy $v_8(r) = \mp b(r)$. So the root count within the window is
   a vectorized comparison: `(vv == -bv).sum()` or `(vv == bv).sum()`,
   with no polynomial arithmetic and no root finding at all.
4. Only candidates reaching 7 window-hits get promoted to exact
   polynomial construction and exact root counting (rare by
   construction: at depth 8 only $1.6 \times 10^8$ of
   $2.1 \times 10^{11}$ results even had 4 roots).

Expected cost: the inner loop becomes ~1300 vectorized 65-wide compares
per state instead of 2600 polynomial multiplications; a 20-40x speedup
over the naive route puts the full additive sweep in the 3-6 hour range,
the same class as the scans already run.

## Soundness scope (stated in advance)

- A hit is EXACT after promotion (the witness is rebuilt and its roots
  counted exactly): a positive result is unconditional.
- Emptiness is a WINDOWED statement: no 9-gate 7-rooter with final
  $\pm$ whose seven roots all lie in $[-32, 32]$. Combined with a
  multiplicative-case emptiness, the honest summary would be: the
  seven-root threshold is 10 unless a nine-gate witness has a root of
  absolute value $> 32$. That caveat must appear in any paper text; it
  is weaker than the depth-8 result, which was unconditional.
- Removing the window would need a height bound on roots of low-tau
  polynomials: none is known to us (the geometric-progression family
  shows roots can be huge in general), which is exactly why the
  statement stays windowed.

## Cheap precursor worth running first

The same machinery restricted to $v_8$ ranging over the 67 catalogued
five-rooters and the 6-rooters (rarity: 328 occurrences at depth 8)
decides the $(5,2)$ and $(6,1)$ additive sub-cases in minutes rather
than hours, and those are where a 7-rooter would most plausibly live.
