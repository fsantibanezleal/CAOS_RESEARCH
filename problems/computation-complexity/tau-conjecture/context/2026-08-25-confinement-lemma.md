# The confinement lemma: turning "windowed" into a decidable criterion

Round 11b, 2026-08-25. The weakest point in the pending nine-gate result is
that the additive instrument is WINDOWED: it tests residue agreement on
[-32, 32], so emptiness there excludes only a nine-gate seven-rooter whose
roots all lie in that range. A nine-gate program can build constants as
large as 2^256 by repeated squaring, so large-root witnesses are not
excluded by the scan alone. This note removes most of that gap.

## Lemma

Let f in Z[x], f nonzero, with distinct integer roots r_1, ..., r_k. Then

    prod_i (n - r_i)  divides  f(n)    for every integer n.

Proof. The r_i are distinct integers, so prod (x - r_i) is monic in Z[x] and
divides f in Q[x]; the cofactor is in Z[x] by Gauss. Evaluate at n. QED

## Corollary (the criterion)

Let c be the trailing (first nonzero) coefficient of f, and suppose f has 7
distinct integer roots, at least one with |r| >= 33.

- If 0 is not a root, c = f(0) and |c| >= prod |r_i|. The six non-escaping
  roots are distinct and nonzero, so their |product| is at least
  |(-1)(1)(-2)(2)(-3)(3)| = 36, giving |c| >= 33 * 36 = 1188.
- If 0 is a root, write f = x^m g, so c = g(0) and the six other roots are
  distinct nonzero; the five non-escaping ones give |product| at least 12,
  so |c| >= 33 * 12 = 396.

Hence

    |c| <= 395   ==>   every integer root of f lies in [-32, 32],

and for such f the windowed scan is CONCLUSIVE, not merely suggestive.

## Both checked numerically

`scripts/confinement_lemma.py` verifies the divisibility on the two
ten-gate witnesses across n in [-40, 40], and searches for a counterexample
to the 396 floor over seven-root sets containing an escaping root. The
minimum trailing coefficient found is exactly 396, at the root set
{-3,-2,-1,0,1,2,33}: **the bound is tight, not merely valid.**

Worth noting: the two verified ten-gate seven-rooters have trailing
coefficients 48 and -64, an order of magnitude inside the criterion. The
shapes that actually achieve seven roots cheaply are exactly the ones the
window sees.

## What this does and does not settle

It does NOT make the additive scan unconditional. It converts the caveat
from an unknown into a measured quantity: the scan is conclusive on every
candidate with |c| <= 395, and window-limited only on candidates with a
large trailing coefficient.

Crucially the criterion is CHEAP in our setting. For an additive last gate
f = v +- b, the trailing coefficient comes from the constant terms of v and
b, which the stored state already holds; no exact polynomial construction is
needed. So the window-limited fraction of the search space can be measured
exactly rather than estimated.

## EXP-014 (declared, to run after the current scan)

Question: what fraction of the nine-gate additive search space has
|trailing coefficient| <= 395, and is therefore rigorously decided by the
completed windowed scan?

Method: a second pass over the same partitions computing c = c_0(v) +- c_0(b)
exactly per candidate; report the distribution of |c| and the decided
fraction. If the decided fraction is high, the nine-gate emptiness is
unconditional on all but an explicitly characterized and small remainder,
and that remainder can be attacked directly by exact root-finding on the
divisors of its trailing coefficients.

Pre-registered expectation, stated before running: the fraction will be LOW
(most nine-gate values carry large constants), so the honest headline stays
"windowed" and the value of EXP-014 is that it prices the gap instead of
leaving it open. Recording the prediction so it can be refuted, as with the
four previous ones.
