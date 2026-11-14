# EXP-022 atlas verdict (CCB-042), 2026-11-14

Source: independent review with a CPU rerun of m2w, CAOS_MANAGE `wip/caos-research/cc-m2w-verdict-2026-11-14.md`
(reviewer agent, opus). Summary of its findings, which this record adopts:

- [MV] m2w is sound: a rerun of both sign charts reproduces the stored counters exactly (P: 1,201 processed, 492
  certified, 109 discarded, 0 failed; N: 1,213, 494, 113, 0); every certificate is a plain interval minor, the leaves
  tile the seed exactly, and the column rescaling agrees with the assembly record's argument at 408 sampled points.
- The quadruple corner is NOT closed:
  - B1: below the chart's lower bound (tt < 1/2) no certificate exists; m2w delegates it to m2, and every stored m2
    checkpoint leaves that half unprocessed (witness u = p = 1/50, v = 0, q = -1/50);
  - B2: the 7/32 axis-body band that m2w discards contains a thin sliver that no chart covers (an exact witness point
    and its symmetry images are all discarded);
  - B3: the rest of that band is delegated to bicorner-same and m1, which left 98.0% and 99.96% of their regions
    unprocessed.
- The "failed" counters of collapse (20), bicorner-same (19), fartube (20), m1 (21) and uplow (10) are unprocessed stack
  boxes of runs stopped at their time budget, not boxes that failed at the depth cap; their unprocessed shares of the
  seed are 39.6% (0% after the mirror, conditional on its last 412 boxes), 98.0%, 98.4%, 99.96% and 89.3% (69.5% after
  the full symmetry group). deep-L and deep-R stopped at their budget with 6,086 and 134,008 genuine failures and 37.3%
  and 46.7% of the seed unprocessed after the mirror; fa2b and m2 are incomplete likewise. m1vert-S never ran.
- Corrected status: complete with 0 failures: bicorner-opp, fa1, tube-L, tube-R, tubeext-L, tubeext-R, ulow, m2w-P and
  m2w-N (own domain); complete modulo the mirror: collapse (conditional); finished with dispositioned failures: band
  (44 trapped); finished with failures not dispositioned in stored artifacts: cb1 (26), cb1f (2); incomplete: deep-L,
  deep-R, fa2b, m2-L, m2-R (tt < 1/2), bicorner-same, fartube, m1, uplow.
- The stratum assembly record treats the stopped runs as complete; the (2,2) atlas is not established. Per-box failure
  widths and locations could not be checked (the certificate files under the data root are not on the review device).

Consequence: the manuscript's atlas description (v0.12) is corrected in v0.13 (backlog CCB-044).
