# EXP-012 - Verdict: CONFIRMED 1-4, REFUTED 5 (2026-07-21). The m = 2 mechanism is unique in the scanned landscape

Artifacts: `artifacts/output-{AB,C,D,E}-2026-07-21.txt` (the first monolithic attempt timed out
and is kept as `output-monolithic-timeout-2026-07-21.txt`; the run was split into parts).

## Established results (ours, exact)

1. **Determinant lemma [MV].** For weights (1, -1, -m) and components F_i = x^{o_i} f_i(v, t):
   det JF = x^{sigma+m} (o_1 f_1 J_23 - o_2 f_2 J_13 + o_3 f_3 J_12). Certified for
   m in {1, 2, 3, 4} x five o-triples (20 cases, generic sparse symbolic f_i). Keller forces
   sigma = -m and the bracket D constant.
2. **Pairing reductions [MV].** J_2 = (+/-) c_1^{r_a + r_b - 1} D for the four natural pairings
   ((1,1) at m=1 sign +; (1,2) at m=2 sign -; (2,2) at m=3 sign +; (2,3) at m=4 sign -):
   the reduced Jacobian vanishes to order m - 1 along the section, as designed.
3. **m = 1 is the JC(2) bridge, rigid in scans [MV].** 93 polynomial Keller instances across
   24 sparse patterns (including t-free sections, which the first pass wrongly excluded: the
   permutation-type maps live there); every in-image fiber has one point. On this class the
   reduced pair is itself a 2D Keller map, so a collision here would refute JC(2).
4. **m = 3 is empty or rigid [MV].**
   - o = (-2, -2, 1): the class is EMPTY: the lattice forbids v-linear monomials in both
     negative components, so d f1/dv and d f2/dv vanish at the origin and D(0,0) = 0 identically
     (one-line valuation proof, machine-certified on a generic ansatz).
   - o = (-3, -1, 1): 60 polynomial Keller instances, every fiber single-point.
5. **The m = 4 potential family does NOT exist (prediction 5 REFUTED, with a certificate)
   [MV].** For the pairing (-3, -2, 1) and the potential form V' = k^2 p(w) + mu s^2,
   T' = w V' - k^2 Phi(w): the five low-weight polynomiality conditions, with seed degree up to
   5 and gauge Q0 = 1, have Groebner basis [1] under mu != 0 (Rabinowitsch): the admissibility
   system is EMPTY. Hand analysis of the degree-4 subcase shows the mechanism: the conditions
   successively pin p(1)-type combinations until mu = 0 is forced.

## The landscape synthesis

The design hypothesis (a parity law: families at every even m) is REFUTED. What the landscape
actually looks like, within everything scanned: **the weight system (1, -1, -2) with output
weights (-2, -1, 1), i.e. exactly the announced counterexample's system, is the UNIQUE
collision-capable weighted mechanism.** m = 1 cannot collide without refuting JC(2); m = 3 is
empty or rigid; the m = 4 potential form is empty. The announced map is not the smallest rung of
a ladder of weighted families: within the scanned weighted world, its mechanism is essentially
THE mechanism. This sharpens the minimality picture beyond EXP-008.

## Adversarial validation record

- The emptiness statements are Groebner/valuation certificates, not failed searches.
- The scans fixed two instantiation bug classes mid-experiment (missing t-free sections; loose
  auxiliary-symbol filters) and their intermediate outputs are retained in artifacts; the final
  counts (93, 60) are clean-instance counts with in-image targets.

## How could this be wrong?

- All scans are bounded (sparse patterns, low degrees, specific o-triples and pairings); the
  uniqueness statement is a statement about the SCANNED landscape, clearly quantified, not a
  theorem for all weighted mechanisms. Wider weight systems ((1, -2, -m), three-invariant
  degenerations) and higher-degree seeds are the queued widening (JCB-019).
- The m = 4 emptiness is for the potential-form ansatz with g = mu s^2 and seed degree <= 5;
  a non-potential m = 4 Keller map is not excluded (the D(ii)-style lattice scan for m = 4 is
  part of JCB-019).

## Consequences

- The generalization story consolidates: one mechanism, an infinite family INSIDE it (seed,
  scale, section tail; EXP-004/008), and no sibling mechanisms at neighboring weights (this
  run). The uniqueness angle enters the manuscript and the diffusion material.
- The JC(2) bridge (m = 1) is now the sharpest structural link between the 3D landscape and the
  open planar case: any collision in that class IS a planar counterexample.
