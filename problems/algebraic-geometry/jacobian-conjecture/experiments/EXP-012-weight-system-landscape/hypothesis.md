# EXP-012 - The weighted mechanism landscape in C^3: a parity law, a JC(2) bridge, and a new family at m = 4

- **Question.** The counterexample mechanism lives on the weight system (1, -1, -2). What
  happens on the other two-invariant systems (1, -1, -m)? Which admit counterexample families,
  which are rigid, and does any yield total degree < 7?
- **Motivation.** JC-P3 (global minimality) and the generalization mandate. Design analysis
  (to be certified here) predicts a structural trichotomy governed by the order of vanishing of
  the reduced Jacobian along the section s = 0.
- **The framework (to certify).** Source weights (1, -1, -m), invariants v = xy, t = x^m z;
  components F_i = x^{o_i} f_i(v, t) with output weights o = (o_1, o_2, o_3), o_3 = 1.
  1. (Determinant lemma) det JF = x^{sigma + m} (o_1 f_1 J_23 - o_2 f_2 J_13 + o_3 f_3 J_12),
     sigma = o_1 + o_2 + o_3, J_ab = f_a,v f_b,t - f_a,t f_b,v. Keller forces sigma = -m and
     the bracket D = const != 0.
  2. (Pairing reduction) With s = c_1 = f_3 and weight-0 output invariants
     V' = F_a F_3^{r_a}, T' = F_b F_3^{r_b}, one gets J_2 := det d(V', T')/d(v, t) =
     (+/-) c_1^{r_a + r_b - 1} D, so Keller makes the reduced Jacobian in the chart (w, s),
     w = u s / k, vanish to order r_a + r_b - 2 = m - 1 along s = 0.
  3. (Parity law, the core hypothesis) A potential form V' = k^2 p(w) + mu g(s),
     T' = w V' - k^2 Phi(w) has reduced Jacobian -mu^2 g'(s) g(s)-shaped, reaching exactly the
     ODD vanishing orders (g = s^a gives order 2a - 1). Hence: m EVEN admits collision
     families (m = 2 is the known one, a = 1; m = 4 is NEW, a = 2, with a two-preimages-per-w
     mechanism via s -> -s); m ODD is rigid at the potential level, and m = 1 is special: there
     the reduced pair is itself a 2D KELLER map, so a counterexample of that shape would
     refute JC(2) directly (a bridge, not a route).
- **Falsifiable predictions.**
  1. [MV] The determinant lemma holds for m in {1, 2, 3, 4}, several o-triples, generic
     symbolic f_i.
  2. [MV] The pairing reduction identities hold generically for the four pairings
     (m, r_a, r_b) = (1, 1, 1), (2, 1, 2), (3, 2, 2), (4, 2, 3).
  3. [MV] m = 1, o = (-1, -1, 1): small-degree exhaustive Keller solves produce only maps with
     in-image fiber size <= 1 (injective); and on any such solution the reduced (w, s)-map has
     CONSTANT Jacobian (the JC(2) bridge identity).
  4. [MV] m = 3, o = (-2, -2, 1): the (w, s)-ansatz solves for det = gamma s^2 (s-degree <= 2,
     w-degree <= 3) admit only branches whose reduced maps have fiber size <= 1 (rigidity at
     the scanned sizes; consistent with the even-order/no-swap analysis).
  5. [MV] m = 4, o = (-3, -2, 1): the constructor V' = k^2 p(w) + mu s^2, T' = w V' - k^2
     Phi(w) with a valuation-2 seed (p(0) = p'(0) = 0) yields, for admissible parameters, a
     POLYNOMIAL Keller map of C^3 with constant nonzero determinant, fiber polynomial of
     degree deg p + 1 in w with TWO preimages per root (s and -s): a counterexample family on
     a NEW weight system, with an explicit rational collision of the form (w_0, s_0) vs
     (w_0, -s_0).
  6. (Minimality synthesis) None of the scanned systems yields total degree < 7 (m = 4
     degrees will be computed and are expected to exceed 7), so within the scanned
     two-invariant weighted landscape the announced map remains minimal.
- **Method.** sympy over QQ throughout: generic symbolic identity checks; exhaustive
  undetermined-coefficient solves with nondegeneracy imposed Rabinowitsch-style; explicit
  construction, lift, and exact verification for m = 4 (polynomiality residues, direct 3x3
  determinant, fiber, collision).
- **Success criterion.** Predictions 1-5 verified; 6 recorded with the computed degrees.
- **Failure criterion.** Any [MV] fails. A collision found at m = 1 would refute JC(2)
  (escalate immediately); a collision at m = 3 scanned sizes would refute the parity law.

Declared 2026-07-21 before the run.
