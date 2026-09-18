# EXP-017 - The determinantal-loci dimension bounds: the stage that carries the stratum theorem

Declared: 2026-08-01, BEFORE any run. After EXP-018, this stage carries the
WHOLE remaining chain: no CC witness is needed if these bounds land.

## The construction (enlarged ghost-free ring)

Ring: the nine quotient distances + height auxiliaries (h1, e12, f) + t.
Shape ideal SH (all quadric, no chain-squaring, no ghosts):
4h1^2 = 4d1A^2 - wA^2; e12^2 = r12^2; 4f^2 = 4cs^2 - (wA - wB)^2;
4(h1 - e12)^2 = 4d2A^2 - wA^2; 4(h1 + f)^2 = 4d1B^2 - wB^2;
4(h1 - e12 + f)^2 = 4d2B^2 - wB^2; cx^2 - cs^2 = wA wB; gauge r12 = 1;
saturation t * (product of the nine distances) * f - 1. Note f in the
saturation product: the variety EXCLUDES the equal-heights sub-stratum by
construction, which is exactly the campaign's declared scope.

The mass matrix J: rows indexed by the reduced block, columns by
(m1, m2, mA, mB); the signed areas are polynomials in (wA/2, wB/2, h1, e12,
f) (every Delta involves only y-DIFFERENCES, all height-expressible); the
s-factors are inverse-cube differences of quotient distances; each row is
cleared by its denominator LCM so all minors are polynomial. Determinantal
loci Delta_k = vanishing of all (k+1) x (k+1) minors (rank <= k).

## The case-chain arithmetic (stated in full)

For any component Omega_i of the stratum incidence variety with
k-dimensional shape projection (k in {0..4}), Lemma 7.3 of Dias-Pan gives
dim Omega_i <= k + (4 - rank) <= 4 provided the projection is NOT contained
in Delta_{k-1}... precisely: provided rank >= k somewhere over the
projection, which holds when dim(SH + Delta_k-minors) < k, i.e. the rank-<k
locus meets the shape variety in dimension below k. The k = 0 case needs
nothing (0 + 4 = 4). So FOUR bounds close everything:

    P1: dim(SH + all 4x4 minors) <= 3     (k = 4 case)
    P2: dim(SH + all 3x3 minors) <= 2     (k = 3 case)
    P3: dim(SH + all 2x2 minors) <= 1     (k = 2 case)
    P4: dim(SH + all entries)    <= 0     (k = 1 case)

If P1-P4 all land: dim(Omega_stratum) <= 4 = the mass count, and the fiber
dimension theorem gives GENERIC FINITENESS for the k = 2, p = 2 stratum off
the equal-heights sub-stratum. Then STOP: the statement wording goes to
Felipe FIRST, before any record beyond the verdict.

## Predictions

- P0a (smoke, enlarged shape dimension): the gauged SH ideal has dimension
  4 in Singular (two-way agreement), re-verifying EXP-015 in the new ring.
- P0b (smoke, matrix cross-validation): the enlarged-ring J, evaluated at
  the EXP-016 witness geometry W1 (exact distance and height values), equals
  the coordinate-built matrix from EXP-016 entrywise after the row-LCM
  clearing is divided back out (equivalently: cleared-row proportionality
  checks exactly). Any mismatch stops everything as a mapping bug.
- P1..P4 as above, each via Singular std at 300 s; where a full basis walls,
  the partial-GB union fallback (per-minor subideals {SH, one minor}, 60 s
  each: 15, 80, 90, 24 subideals respectively) gives the bound if the union
  staircase lands below the threshold; two-way agreement wherever a full
  basis completes. Declared honest outcome classes per rung: BOUND MET /
  BOUND NOT MET (a real structural finding: some rank locus is fat, the
  theorem needs the sign-analysis lemma instead) / INCONCLUSIVE-CAP.

## Preflight (methodology/12)

- Source-complete: every ingredient is our own verified construction
  (dossier identities; EXP-016's matrix; Dias-Pan's lemma logic read in
  full). No [U] premise.
- Smoke: P0a + P0b before any minor is trusted.
- One-sidedness: BOUND NOT MET is a declared, meaningful outcome per rung;
  caps are honest.
- Invariant-first: per-rung dimension values, entry-size cost data, wall
  times: the cost map for the k = 0, p = 3 sibling stratum later.
- Budget and kill: worst case about 4 x 300 s full attempts + (15 + 80 +
  90 + 24) x 60 s fallbacks, around 4 h; no extensions; any rung may end
  inconclusive-cap without poisoning the others.

## Consequence ladder

- All four land: the stratum theorem chain is COMPLETE (statement to Felipe
  first). Manuscript v0.08 consolidates the arc after his review of the
  wording.
- Some rung lands BOUND NOT MET: the chain needs the Dias-Pan 7.2-style
  sign-analysis lemma for that k (physical fibers avoid the fat locus);
  declared as its own follow-up.
- Caps dominate: the pgb menu deepens (pairs of minors) in a follow-up; the
  bounds route stays open, nothing is lost.
