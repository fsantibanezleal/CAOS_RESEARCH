# EXP-014 verdict: the windowed gap is 0.002%, and the prediction was refuted

2026-08-25. Question: what fraction of the additive nine-gate search space does
the [-32, 32] evaluation window actually DECIDE, and what fraction remains
window-limited?

## Pre-registered prediction, REFUTED

Declared before the run (`../../context/2026-08-25-confinement-lemma.md`): "the
fraction will be LOW (most nine-gate values carry large constants), so the
honest headline stays windowed and the value of EXP-014 is that it prices the
gap instead of leaving it open."

Measured: the decided fraction is **99.998%**. The prediction was wrong, and
wrong in the favourable direction. This is the fifth pre-registered prediction
this problem has refuted.

## Method

For each candidate f = t +- b, construct f EXACTLY and read its true trailing
(first nonzero) coefficient c, then apply the confinement lemma: |c| <= 1187
confines when 0 is not a root, |c| <= 395 when it is. No proxy, no coefficient
horizon. Sampled over 400 states from each of four partitions (000, 073, 150,
231); the frontier is hash-partitioned, so a sample is representative by
construction. 6,400,000 candidates constructed. Code: `../EXP-013-additive-residual/exp014.py`.

## Result

    candidates constructed exactly : 6,400,000
    identically zero (excluded)    :    93,898   1.467%
    nonzero candidates             : 6,306,102

    CONFINED by the lemma          : 6,301,361   99.9248% of nonzero
    excluded by degree < 7         :     4,619    0.0732% of nonzero
    WINDOW-LIMITED (degree >= 7)   :       122    0.0019% of nonzero

The degree row is not a lemma but arithmetic: a polynomial with 7 DISTINCT roots
has degree at least 7, so a degree-2 or degree-6 candidate is excluded outright
with no reference to the window. Together, 99.998% of nonzero candidates are
decided independently of the evaluation window.

The residual class is small and well characterized: degrees 8 (100 of 122), 9
(2) and 12 (20); 64 distinct |c| values from 512 to 38,220. A divisor refinement
(a seven-rooter's roots all divide c, and the least |product| of 7 distinct
nonzero integers is 144, rising to 1188 when one root escapes) eliminates only
2 of the 64 values, so it does not by itself close the class.

## Two instrument errors, both caught by cross-checking

1. A vectorized version carrying the low K coefficients reported ~1.5%
   "undetermined" at K = 6 and stayed at ~1.47% for K = 12 and K = 20, which
   looked like a class of deeply x-divisible polynomials. Exact construction
   found ZERO nonzero candidates divisible by x^20: every one of that 1.47% is
   the IDENTICALLY ZERO polynomial. Low coefficients alone cannot tell "deeply
   divisible" from "zero". This is the FIFTH appearance of the zero-object
   degeneracy in this problem.
2. A valuation-pair instrument (v, L) was written to remove the coefficient
   horizon; it resolves ties worse (17% unresolved against 1.5%) because
   cancelling leads are common among these operands. It was kept as a
   cross-check, and it agrees with the coefficient instrument on the number that
   matters: window-limited 9,124 against 9,156 on the same sample, both 0.076%
   before the degree filter.

## What this does and does not establish

It does NOT make the additive scan unconditional. Scaled to the full space of
roughly 4.2e12 candidates, 0.0019% is on the order of 1e8 candidates the window
alone does not decide.

It does replace an unbounded caveat with a measured, structurally characterized
one. The honest form of the pending nine-gate statement is therefore: emptiness
holds outright for 99.998% of the additive search space, and is windowed only on
a residual of about 0.002% whose degrees and trailing coefficients are known.

These are SAMPLE estimates from 4 of 256 partitions, not exhaustive counts, and
are reported as such. Making the residual exhaustive is the natural follow-up:
the class is rare enough that a full pass retaining only degree >= 7 candidates
with |c| above the bound is affordable, and each survivor can then be
root-counted exactly over the divisors of its trailing coefficient.
