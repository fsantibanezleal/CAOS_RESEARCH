# EXP-019 - Single-minor incremental cuts with the Cohen-Macaulay argument: the chain's endgame

Declared: 2026-08-02, BEFORE any run.

## The mathematical shortcut (stated fully, since the verdict will lean on it)

The gauged shape ideal in the height ring has 13 variables and 9 generators
(seven quadrics, the gauge r12 - 1, the saturation), and its dimension is 4
= 13 - 9 (EXP-017 P0a, two-way agreement). An ideal whose dimension equals
variables minus generators is a COMPLETE INTERSECTION; complete
intersections are Cohen-Macaulay, hence UNMIXED: every irreducible
component has dimension exactly 4 and there are no embedded components. By
Krull's principal ideal theorem, for ANY polynomial g, each component C of
the shape variety satisfies: either g vanishes identically on C, or
dim(C meet {g = 0}) = 3. Therefore

    dim(shape + g) <= 3   IMPLIES   g vanishes on NO component,
    hence {g = 0} meets EVERY component properly.

Moreover if g is such a nonzerodivisor, shape + g is again Cohen-Macaulay
(a regular element on a CM ring) and unmixed of dimension 3, so the
argument ITERATES for a second polynomial g'. This removes the
component-identification problem (the twice-failed minAss) from the chain
entirely: single-minor incremental dimension checks suffice.

## What closes what

- k = 4 needs dim(shape meet R_3) <= 3 where R_3 = all 4x4 minors vanish.
  Since R_3 is contained in {g4 = 0} for ANY single 4x4 minor g4:
  P1: dim(shape + g4) <= 3 CLOSES k = 4.
- k = 3 needs dim(shape meet R_2) <= 2 with R_2 = all 3x3 minors vanish,
  contained in {g3 = 0} meet {g3' = 0} for any two 3x3 minors:
  P2: dim(shape + g3) <= 3, then P3: dim(shape + g3 + g3') <= 2
  (the iteration step uses P2's Cohen-Macaulay conclusion) CLOSE k = 3.

With k = 0, 1, 2 already proven (lemma pieces 1-5), P1 + P2 + P3 COMPLETE
THE CHAIN: dim(Omega_stratum) <= 4 and generic finiteness for the two-pair
stratum off equal heights follows. Per the standing rule, on completion
everything STOPS and the statement wording goes to Felipe FIRST.

## Choices and predictions

Minors are built in the height ring with row-LCM clearing (the EXP-017
construction, cross-validated at W1) and CHOSEN BY SIZE: g4 = the 4x4 on
rows {L13, L15, L23, L25} (four structural zeros, the smallest cleared
form); g3, g3' = the two smallest-term-count 3x3 minors with distinct row
sets. Predictions:

- P1: Singular std(SH + g4) completes within 1800 s with dimension <= 3,
  two-way agreement. (EXP-017's fallback tried single minors at 60 s only;
  this is a new declared budget on the SMALLEST minor, not an extension.)
- P2: std(SH + g3) completes within 1800 s with dimension exactly 3.
- P3: std(SH + g3 + g3') completes within 1800 s with dimension <= 2.
- Sanity in-run: the EXP-016 witnesses have rank 4, so every chosen minor
  is NONZERO at them; each minor is evaluated exactly at W1 before its run
  and must be nonzero (a zero would mean a construction bug, stop).

## Preflight (methodology/12)

- Source-complete: the CM/Krull facts are classical (Matsumura-level
  commutative algebra, no citation risk); everything else is our verified
  construction. No [U] premise.
- Smoke: the W1 nonvanishing evaluations, plus the shape dimension re-check
  (must be 4) in the same Singular session before each cut.
- One-sidedness: a completed run with dimension 4 would mean the minor
  vanishes on some component: a REAL structural finding (that component
  would be a rank-degenerate 4-dim family, publishable in itself) and the
  k = 4 route would then genuinely need the CC witness. Caps are honest
  outcomes; the budget is per-run 1800 s, no extensions.
- Invariant-first: per-run dimension and wall time.

## Consequence ladder

- P1 + P2 + P3 land: THE CHAIN IS COMPLETE. STOP. Statement wording
  (generic finiteness, two-pair symmetric stratum, off the equal-heights
  sub-stratum, pair-equal masses forced by the lemma, generic mass
  4-tuples off a proper closed set) to Felipe FIRST before any further
  record.
- Any run returns dimension 4: structural finding, component audit, the
  affected case reverts to its witness route.
- Caps: recorded; the affected case stays open; the witness route (k = 4)
  and deeper border analysis (k = 3) continue next round.
