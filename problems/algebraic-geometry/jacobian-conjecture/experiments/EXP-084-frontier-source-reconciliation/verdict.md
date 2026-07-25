# EXP-084 - Verdict: the remark settles four more A0 cases; two of our configs are candidates, gated on one unsourced list

**Status: DECIDED at the level the sources support. Honest DERIVATION NEEDED on
the remaining link.**

## What the GGV2 closing remark states, in full [VERIFIED, arXiv:1605.09430 source]

Every item below forces an IMPOSSIBLE A0' (a corner in the excluded family
wp(n', n'-1)), and so discards its case:
1. A0 = (10,25) forces A0' = (2,1).
2. A0 = (14,35) forces A0' in {(6,3),(3,2)}.
3. The corner (8,32) as an A0 gives, after an automorphism, A0' = (8,4).
4. Heitmann's infinite families (5k+3, 3k+2) and (4k+3, k+1), corresponding to
   A0 = (7,21), come from A0' = (2,1). (Stated by the authors as the first time
   one of Heitmann's infinite families is discarded.)
5. B0 = (6,15) with B1 = (6, 18+6k), where 18+6k is NOT a multiple of 30, leads
   to A0' = (6,3).
6. B0 = (8,28) with B1 = (8,40) leads to A0' = (8,4). [our C13, EXP-082]
7. B0 = (9,21) with B1 = (9,27) leads to A0' = (9,6).

## Mapping to our 24 configurations

- **C13** (A0 = (8,40) on the (8,28) chain): EXCLUDED by item 6. Already recorded
  (EXP-082).
- **C10, C11** (both A0 = (7,21)): CANDIDATES for item 4. Our table records them
  as family rows F9 j=1 and F11 j=0. The remark discards the families
  (5k+3, 3k+2) and (4k+3, k+1). Whether C10 and C11 are members of THOSE families
  is not decidable from the remark alone: it requires Heitmann Thm 2.25's family
  parameterisation, which we have NOT sourced. DERIVATION NEEDED. A direct
  numeric check of our degree pairs against the printed parameterisations does
  not match cleanly ((84,140) and (56,140) are not of the form (5k+3,3k+2) or
  (4k+3,k+1) for integer k), which is itself evidence that those parameterisations
  index CORNERS or family members, not degree pairs. Do not guess.
- **C19, C20** (both A0 = (6,15)): CANDIDATES for item 5, which additionally
  requires knowing B1 and the divisibility condition (18+6k not a multiple of 30).
  Our table does not carry B1 for these rows. DERIVATION NEEDED (GGV Remark 7.9).
- Items 1, 2, 3, 7 concern A0 values ((10,25), (14,35), (8,32), (9,21)) that do
  NOT appear among our 24 configurations, so they settle nothing further for us.

## Net effect on the frontier map
Confirmed excluded so far: C13 only. Four configs (C10, C11, C19, C20) are
STRONG CANDIDATES for exclusion by this remark, each blocked by exactly one
unsourced list (Heitmann Thm 2.25 for C10/C11; GGV Remark 7.9's B1 data for
C19/C20). The next step is a source fetch, NOT a computation: obtain Heitmann
"On the Jacobian conjecture" (J. Pure Appl. Algebra 64, 1990) Thm 2.24/2.25 and
the GGV Remark 7.9 list. Per P1 this precedes any further frontier machine work.

## Preflight value note
Reading the remark in full took minutes and moved four configurations from
"unknown, attack later" to "one source fetch from settled". The same rule, applied
one session earlier, would have prevented the entire C13 derivation effort.
