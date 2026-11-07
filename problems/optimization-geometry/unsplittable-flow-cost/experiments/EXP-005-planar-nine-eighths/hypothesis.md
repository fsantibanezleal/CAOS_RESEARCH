# EXP-005 preflight: independent check of the planar 9/8 family, and its frontier values

Date: 2026-11-07. Status: frozen before any computation. CPU only, exact rationals.

Numbering note: earlier plans used "EXP-005" for the next conflict-structure experiment (UFB-037, re-scoped by
UFB-065); that experiment takes the next free number. This one answers UFB-063.

## Question

Muffatti (GitHub `terrorproforma/maths`, `planar-cost-lower-bound`, commit dbf9d23 of 2026-08-31; Proposition 1 and
Theorem 2 of `paper/planar_cost_lower_bound.tex`, read in full 2026-11-07) claims that Rybin's topology with
demands (1, b, 1), cheap-path fractions (r, q, r) and expensive paths of unit integral cost forces, for
b = 3/4, r = 1/4, q = 1/2 + eps, a violation of at least 9/8 - (3/4) eps on every cost-preserving routing, so the
planar cost-preserving constant is at least 9/8 (supremum, not attained). Our record has alpha* >= 16/15 (EXP-002,
EXP-004), and EXP-004's verdict reads its null sweep as "pushing alpha* meaningfully above 1 will not come from
tuning this family's parameters" [D]. Does our own exact instrument confirm the claim, and what does the optimal
pricing (the frontier value) give on the same family?

## Instance M(b, r1, q, r3, d3)

Vertices s, u, v, w, t1, t2, t3; arcs and the two paths per terminal exactly as in Rybin's instance (AFP entry
Dinitz_Garg_Goemans_Counterexample; our `ufclib` arc order): t1: paid s-t1, free s-u-v-t1; t2: paid s-t2, free
s-u-v-w-t2; t3: paid s-u-t3, free s-u-v-w-t3. Demands d1 = 1, d2 = b, d3. The fractional flow sends the fraction
r1, q, r3 of each demand on its free path and the rest on its paid path; the arc flows are the sums. Muffatti's
costs per unit flow: s-t1 = 1/d1, s-t2 = 1/b, u-t3 = 1/d3, all others 0 (each paid path has integral cost 1).

## Predictions

- P1 (claim check, fixed costs). For eps in {1/10, 1/100, 1/1000} and M(3/4, 1/4, 1/2 + eps, 1/4, 1) with
  Muffatti's costs: the fractional cost is 2 - eps, and the least alpha(y) over routings y with
  c^T y <= c^T x equals 9/8 - (3/4) eps exactly.
- P2 (structure). Each M(3/4, 1/4, 1/2 + eps, 1/4, 1) is acyclic, has a K4 subdivision, and is planar by our
  degree-based Kuratowski check (as Rybin's instance).
- P3 (frontier value). For the same three instances, alpha_max (our `frontier_value`, the optimal pricing) is at
  least 9/8 - (3/4) eps; its exact value is reported (it may be larger).
- P4 (exploration, no value predicted). Over the grid d1 = 1, b in {1/8, ..., 8/8}, d3 in {1/4, 2/4, 3/4, 1},
  r1, q, r3 in {1/16, ..., 15/16}, the largest alpha_max is reported with its parameters. A value above 9/8 at
  some grid point would be a lower bound alpha* >= that value on a planar acyclic instance, to be re-checked by an
  independent route before any claim.

## Consequences fixed in advance

If P1 to P3 hold, our records move to alpha* >= 9/8 and alpha*_planar in [9/8, 2], credited to Muffatti; EXP-004's
[D] reading is withdrawn in writing (its [MV] sweep stands, its box did not contain these parameters). If P1
fails, the claim is not confirmed and the discrepancy is reported.

## Budget

At most 2 hours of one process for P4; P1 to P3 take seconds.
