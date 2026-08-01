# EXP-014 - The incremental cut: adjoining Cayley-Menger to the completed products basis

Declared: 2026-08-01, BEFORE any run. Follow-up to EXP-013 per its declared
consequence 1. The question EXP-013 localized: the products ideal has EXACT
dimension 5 in the torus (complete basis, nine seconds); does adjoining the
single Cayley-Menger polynomial drop the dimension to the expected 4?

## Method

Work entirely in Singular over QQ, grevlex, short=0 (the EXP-012-validated
pipeline). One script:

1. Recompute S = std(products + saturation) in-session (nine seconds by
   EXP-013's measurement; the archived basis is the cross-check).
2. SANITY RUNG FIRST: the normal form NF(cm, S). It MUST be nonzero: if CM
   reduced to zero, the cut would equal the products variety, which the
   EXP-011 smoke gate already refutes (the all-ones 4-simplex lies on the
   products variety and CM = -5 there). A zero normal form would therefore
   mean a pipeline bug, and everything stops.
3. THE CUT: T = std(S, cm), Singular's incremental basis extension, under a
   1800 s cap declared here (a NEW budget for a NEW computation; the
   from-scratch 600 s cap of EXP-013 P1 is not being extended, it stays
   spent). If it terminates: dimension read TWICE (Singular's dim(T) and our
   independent-set staircase on the parsed leading ideal) with agreement
   REQUIRED.

## Predictions

- P1: NF(cm, S) != 0 (sanity; a zero stops everything as a bug, not a
  finding).
- P2: std(S, cm) terminates within 1800 s. (The incremental extension
  typically does far less work than the from-scratch run that capped;
  measured basis: 2436 elements, one new generator of degree 8.)
- P3: the exact staircase dimension of the cut is 4, read with two-way
  agreement. Branches, all declared: 4 = the lane's central quantity at
  n = 5 is DECIDED deterministically (statement-level wording goes to Felipe
  before any publication step, per the standing rule); 5 = Cayley-Menger
  vanishes identically on some top component of the products variety, a
  structural finding demanding component-level audit (enriched cuts next);
  below 4 = witness audit (the bipyramid slice must be re-examined exactly);
  cap = the bound dim <= 5 stands and the menu path (triples) or witness
  sets carry on.

## Preflight (methodology/12)

- Source-complete: everything is our own validated tooling from EXP-012/013,
  same binaries, same parser, controls green this morning. No [U] premise.
- Smoke: P1 IS the in-run sanity gate; additionally the recomputed S must
  have 2436 leading monomials (EXP-013's archived count) before anything
  proceeds.
- One-sidedness: P2 can cap (branch declared); P3 has all four outcome
  branches declared including the uncomfortable ones.
- Invariant-first: the invariant is the exact dimension (or the surviving
  bound) and the incremental-vs-from-scratch cost ratio, which calibrates
  the "adjoin realizability equations incrementally" cost law for the
  strata campaign.
- Budget and kill: one script, worst case about 9 s + NF + 1800 s. No
  extensions; a cap is a recorded outcome.

## Consequence ladder

- P3 = 4: record as the deterministic dimension of the n = 5 spatial
  Dziobek cut; wiki/log/mirror; manuscript v0.07 consolidates EXP-012/013/014
  with ONE Zenodo new version; the k = 2, p = 2 stratum campaign is declared
  next with the established cost law.
- P3 = 5: component audit experiment next (which top components carry CM
  identically; Singular primary decomposition on the products basis or
  witness sets).
- P2 caps: the incremental route joins the from-scratch route as measured-
  out-of-reach; the lane's dimension work at n = 5 stands at dim <= 5
  deterministic and moves to witness sets; the strata campaign proceeds
  regardless (its systems are smaller).
