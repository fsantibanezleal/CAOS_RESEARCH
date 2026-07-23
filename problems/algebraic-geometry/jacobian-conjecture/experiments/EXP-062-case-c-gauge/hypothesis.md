# EXP-062 - Case c under the torus gauge (route N2, the closure of the last branch)

- **Question.** Close Prop 4.3's case c) on its forced family, replacing the stalled
  two-symbol run (EXP-060) with the gauge-reduced one-symbol certificates.
- **Motivation (the declared derivation).** The scaling sigma: x -> lambda x,
  y -> mu y acts on the reduced systems: the forced edge y^8 (xy - t)^8 has t scale
  by (lambda mu)^{-1}, so lambda mu = t normalizes t to 1; the Jacobian scales by
  lambda mu and the target x^2 by lambda^2, both absorbed by a linear rescaling of Q
  (the bracket is linear in Q); consistency of [P, Q] = x^2 is therefore INVARIANT
  along the gauge orbit. Hence: emptiness at t = 1 for all remaining parameters
  implies emptiness for all t != 0. The remaining parameters: the right-edge
  coefficient beta (free-parameter form subsumes the forced R^2 relation) and the
  interior coefficients (symbolic one at a time = the free-interior upgrade).
- **Falsifiable predictions.**
  1. [MV] The gauge identity: for a sample (t0, beta0), the transformed system at
     t = 1 has the same consistency verdict (explicit transformed P, rescaled target),
     verifying the invariance concretely.
  2. [MV] At t = 1: the beta-symbolic H-certificate exists with nonzero polynomial
     pairing (bare + two interior-sampled variants).
  3. [MV] The free-interior upgrade begins: for at least four interior lattice
     points, the certificate with THAT coefficient symbolic (t = 1, beta sampled)
     has a nonzero polynomial pairing whose vanishing locus misses the stratum or
     falls back to certified subfamilies.
  4. [D] Assembly: with EXP-061 (cases a/b) and this closure of case c's forced
     family (interior at mixed sampled/symbolic generality), all three Prop 4.3
     branches are covered; remaining: completing the interior upgrade across all
     points (mechanical, seconds each) and the orientation swap; then the assembled
     floor-raise statement goes to Felipe.
- **Method.** sympy over QQ(beta) / QQ(eps_i); H-restricted reduced systems; caps
  per part; background only if needed.
- **Success criterion.** 1-3 verified; 4 stated.
- **Failure criterion.** A vanishing-pairing locus inside the stratum or a
  consistent point: adjudicate directly; escalate genuine consistency immediately.

Declared 2026-07-22 before the run.
