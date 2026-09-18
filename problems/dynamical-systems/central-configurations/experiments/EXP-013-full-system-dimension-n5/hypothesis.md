# EXP-013 - The full-system shot: exact staircase dimension of the n = 5 spatial Dziobek cut

Declared: 2026-08-01, BEFORE any run. Backlog: CCB-033/CCB-037 follow-up per
EXP-012's declared menu-growth consequence, upgraded to a full-system attempt
by EXP-012's cost measurements (28 of 31 subideals at sub-second cost).

## Question

Does Singular over QQ complete the grevlex Groebner basis of the ENTIRE cut
(all fifteen stripped Dziobek products + the spatial Cayley-Menger equation +
the Rabinowitsch saturation, eleven variables), and if so, what is the EXACT
staircase dimension? If the full system caps, does the enlarged subideal menu
push the union bound from EXP-012's 7 down to the 5-or-4 range?

Unlike every previous rung, a completed P1 yields not a bound but the true
Krull dimension of the cut in the torus. The expected value from the
generic-finiteness picture is 4 (projectivized mass-space dimension). A
completed value ABOVE 4 would mean the overvariety's degenerate strata
dominate the genuine Dziobek stratum, itself a structural finding that would
redirect the lane to enriched cuts; a value BELOW 4 would contradict the
witness structure and force an exact audit.

## Predictions

- P1 (the full-system shot): Singular std() on the full ideal completes
  within a 600 s cap, and the staircase dimension of its leading ideal is 4.
  The dimension value is read two ways and must AGREE: (a) our independent-set
  staircase computation on the parsed leading monomials; (b) Singular's own
  dim(std(I)) report. Disagreement stops everything.
- P2 (fallback bound, runs only if P1 caps): the growth menu (ten
  double-local subideals = all six products of two adjacent quadruples; five
  local+CM subideals; ten adjacent-pair+CM subideals; one all-fifteen-products
  no-CM subideal), each at 120 s, pushes the union bound to d_pgb <= 5.
- P3 (cost cartography, always recorded): per-subideal times, extending
  EXP-012's observation that the hard combinations were _bc pairings sharing
  the body pair {1, 2}.

## Preflight (methodology/12)

- Source-complete: everything used is our own EXP-011/012-validated tooling;
  no new literature premise; no [U] dependency.
- Smoke: none needed beyond EXP-012's controls, which validated the exact
  pipeline (parser, orders, engines) this run reuses unchanged; the toy and
  job-3 controls remain green from two hours ago on the same binaries.
- One-sidedness: P1 can cap (fallback declared); its completed value can land
  anywhere and each outcome branch is specified above, including the
  uncomfortable ones.
- Invariant-first: the invariant is the exact dimension (or the bound path's
  d_pgb) plus the cost map.
- Budget and kill: P1 600 s; P2 (if triggered) 26 x 120 s = 52 min worst; no
  extensions. If P1 caps AND fewer than 10 of the 26 menu subideals complete,
  the verdict records the menu ceiling honestly and the lane's next move is
  the witness-set spike, not more menus.

## Consequence ladder

- P1 completes at 4: the n = 5 spatial Dziobek cut has certified dimension 4
  in the torus; the incidence-dimension lane's central quantity is DECIDED at
  n = 5 by a deterministic computation, the strata campaign proceeds with the
  same instrument, and the manuscript gains its first non-replication
  dimension theorem-by-machine (statement-level wording goes to Felipe first,
  as always).
- P1 completes at != 4: structural finding; stop, audit exactly, redirect
  (enriched cuts if above, witness audit if below).
- P1 caps, P2 lands <= 5: the bound path continues (triples next), the
  strata campaign proceeds on Dias-Pan precedent.
- P1 caps, P2 weak: menu ceiling recorded; witness sets carry the lane.
