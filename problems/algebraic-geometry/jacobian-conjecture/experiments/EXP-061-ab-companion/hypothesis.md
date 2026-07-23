# EXP-061 - The a/b companion: the sub-polygon cases of Prop 4.3 (route N2)

- **Question.** GGHV Prop 4.3's cases a) and b) have the smaller reduced polygons
  N(P) = {(0,0),(1,0),(8,14),(8,16)}, N(Q) = {(0,0),(2,1),(12,21),(12,24)} (no
  (0,8)/(0,12) corners). The Q-side is already covered by the case-c certificates
  (bigger Q-polygon emptiness implies smaller); the P-side needs its own family run.
  Close it.
- **Motivation.** The forced right edge is l_{1,0}(P) = R^2 with
  R = x^4 y^7 (a0 + a1 y) (the dossier's derived structural note): coefficients
  (a0^2, 2 a0 a1, a1^2) at (8,14), (8,15), (8,16). R is defined up to scalar: two
  normalization charts (a1 = 1 with a0 symbolic; a0 = 1 with a1 symbolic) cover the
  family with ONE symbol each. Lower interior coefficients enter as samples (their
  full generality follows the same free-coefficient pattern as before; recorded).
- **Falsifiable predictions.**
  1. [MV] Chart a1 = 1: the H-certificate over QQ(a0) exists with nonzero polynomial
     pairing, for the bare family and two interior-sampled variants.
  2. [MV] Chart a0 = 1: same with a1 symbolic (covers the a1 = 0 gauge boundary via
     the other chart).
  3. [MV] The pairings' vanishing loci miss the stratum (nonzero R constraints),
     chart by chart.
  4. [D] With EXP-060 (case c) and this companion, ALL THREE branches of Prop 4.3's
     reduced systems are certificate-covered on their forced families (interior
     coefficients at sampled generality, with the free-coefficient upgrade queued):
     the assembly toward the floor-raise is complete modulo that upgrade and the
     orientation swap.
- **Method.** sympy over QQ(a0) / QQ(a1); the H-restricted reduced system on the
  smaller polygons; caps per part; background if needed.
- **Success criterion.** 1-3 verified; 4 stated.
- **Failure criterion.** A consistent point or vanishing-pairing locus inside the
  stratum: adjudicate directly; escalate a genuine consistency immediately.

Declared 2026-07-22 before the run.
