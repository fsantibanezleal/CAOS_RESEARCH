# Approaches evaluation, 2026-08-19 (round 32)

Requested: continue everything, re-evaluate the most effective approaches
with measurements, and probe for genuinely different views. This document
updates approaches-evaluation-2026-08-02.md with the round 25-32 data,
which is the strongest measurement set the campaign has produced.

## 1. Measured instrument ranking (what actually produced theorems)

Ranked by verdict-grade output per unit cost, all figures from this
campaign's own runs:

1. **Certified interval coverings (menu + mean-value + trap).** Four
   regions certified in one day: core (854,317 boxes, 85 min, ZERO
   failures), band (1.58M boxes, 92 min, 44 stubborn all trapped), tube
   chart R (68,567 boxes, 76 min, ZERO failures, 4,544 traps on the
   predicted face curve), tube chart L + pair-collapse running. Beyond
   certification the instrument DISCOVERS: the centered pentagon (exact
   rank-2 point, golden field) and the cross near-miss (singular values
   1.7e-3 / 8.2e-5 without an exact degeneracy) both came out of stubborn
   boxes. Nothing else in the campaign has this discovery-plus-proof
   density.
2. **Closed-form minor analysis + exact witnesses (the pieces
   technique).** Nine lemma pieces; closed k = 0, 1, 2, 4, R_0 globally,
   the swap identity (24/24 syntactic), the tube factorizations. Seconds
   of machine time each once derived; the derivation cost is chat-time,
   not compute.
3. **Exact identification of machine-found points.** Pentagon confirmed
   in Q(sqrt5, sqrt(10 +- 2 sqrt5)) with exact rank 2 and kernel; the
   cross cluster REFUTED as a degeneracy by exact root separation. This
   pairing (interval discovery, then algebraic identification) is the
   campaign's signature move now.
4. **Blow-up rescalings that make singular limits analytic.** The tube
   polar blow-up (every 1/rho^3 cancelled algebraically before
   evaluation) and the 4u^2 column rescale. They convert limit arguments
   (unsound per the closure-hole correction) into coverings (sound).
5. **Singular on small complete systems** (shape dimensions in seconds);
   still the right tool at that scale. All five Groebner routes to the
   LOCI bounds remain measured-closed (EXP-011/017/017b/017c/019).
6. **gfan prevariety at n = 6** (EXP-005): the counting gate for the full
   problem; alive but infrastructure-fragile (three WSL kills to date;
   pow2 checkpoint-protected, pow3 has never reached its first
   checkpoint).
7. Refuted/closed: free-atom chambers (EXP-020, 125M residuals), mod-p as
   anything but a screen, slice-limit collar arguments (closure hole,
   round 31, abandoned before use).

## 2. The remaining chain work, re-planned by the measurements

The atlas still owes: corner tubes (part d), the double corner, and the
outer region (part e). Thinking part (e) through produced a structural
simplification, adopted now:

- **(e1) A closed-form dominance lemma instead of 6-8 inverted charts.**
  For R_A = sqrt(u^2 + v^2) >= R* with the collision tubes excluded, the
  far s-factors are pinned: d1A, d2A >= R* - 1 give s(r12, d1A),
  s(r12, d2A) in (1/8 - 1/(R*-1)^3, 1/8), so the anti-diagonal corner
  {L13, L23} x {m1, m2} has an explicit positive lower bound of order
  u^2/16, and bordered 3 x 3 minors inherit dominance with explicit
  constants; the B-side factors are bounded on the complement of the
  corner tubes. One pieces-style lemma with machine-verified constants
  replaces the whole chart zoo; the swap identity halves the case count.
  R* is fixed by whatever the constants demand (target 8).
- **(e2) Extend the existing box and tube coverings from 3 to R*.** The
  coverings scale linearly and certified [1/4,3]^4-scale regions in ~90
  minutes; the extension is compute, not mathematics.
- **(d) Corner tubes stay blow-up coverings** (the tube.py machinery with
  a different center), bounded part only; their far composition is
  handled by (e1).

## 3. Another view of the problem? Three genuinely different ones, evaluated

- **V11, the Albouy-Kaloshin singular-sequence view (the upgrade path).**
  A-K proved n = 4 finiteness for ALL masses and n = 5 off an explicit
  codimension-2 mass set by classifying singular sequences of CCs
  (clusters and escapes) and deriving per-type mass obstructions. Our
  chain gives GENERIC-mass finiteness for the stratum; the A-K view
  targets the stronger all-masses statement, and on this stratum the
  taxonomy collapses (sequences inherit the reflection symmetry, so the
  cluster/escape types live on the 4-position quotient, a handful of
  cases; our outer charts and corner tubes are literally the escape and
  cluster regimes, with the rescaled matrices already derived). Verdict:
  the highest-value SECOND theorem, to start only after the covering
  chain closes; do not mix routes mid-proof.
- **V12, the certified census view.** The IV/DV machinery can be pointed
  at the CC SYSTEM itself (fixed sample masses, interval Newton /
  Krawczyk on 4-variable subsystems, residual verification of the
  remaining equations) to produce certified solution COUNTS per mass
  sample: Dias-Pan-style tables, but with certificates. Verdict: the
  natural post-theorem deliverable; it also stress-tests the theorem
  (counts must be finite and locally constant off the discriminant).
- **V9, the explicit-discriminant view.** The chain's proof shows failure
  of finiteness requires masses in the image of the low-rank loci under
  the kernel map; the pentagon already names one component candidate (the
  centered-pentagon family m1 = mA = mB with m2 free, from kernel
  (0,1,0,0) + (1,0,1,1)). Making the exceptional mass set EXPLICIT as
  polynomial conditions would sharpen "generic" into a named discriminant.
  Verdict: medium cost, high statement value, after the chain.
- Also weighed: equivariant Morse counting on the symmetric shape sphere
  (lower bounds for the census, analytical side note, no program); the
  BKK/tropical view is already running as EXP-005 for n = 6.

## 4. The queue (in force)

1. Finish tube-L + ulow (running); post-process any stubborn boxes.
2. (e1) dominance lemma: derive, machine-verify constants, fix R*.
3. (d) corner-tube blow-up charts (bounded part), verified then run.
4. (e2) covering extensions to R*.
5. Chain assembly: IF everything certifies, STOP and take the statement
   wording to Felipe FIRST (standing rule).
6. EXP-005 heartbeats; pow3 parked if it dies once more without a
   checkpoint (record, keep pow2).
7. After the chain: V12 census, then V9 discriminant, then V11 as the
   all-masses upgrade campaign.
