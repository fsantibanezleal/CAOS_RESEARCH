# EXP-013 - Verdict: CONFIRMED 1-2, PARTIAL 3 (2026-07-21)

Artifacts: `artifacts/output-12-2026-07-21.txt`, `artifacts/output-3-*-2026-07-21.txt`.

## Established results

1. **Dependence at the top ray [MV].** On a deterministic library of 8 real Keller maps
   (compositions of elementary and unimodular affine maps, degrees up to (4, 4) and mixed):
   whenever deg P + deg Q > 2, the ordinary leading forms satisfy J(P_+, Q_+) = 0 and share a
   common radical form (exact factorization; radical ratio a nonzero constant in every case).
2. **Ray sweep: the local model everywhere [MV].** 56 (map, ray) pairs over the fan sample
   {(1,1), (2,1), (1,2), (3,1), (1,3), (3,2), (2,3)}: at every ray with positive top degree,
   the omega-leading pair is Jacobian-dependent with a common radical form. Every real planar
   Keller map is, at every sampled ray, the DEGENERATE boundary of the EXP-010 equivariant
   classification: the bridge between our rigidity theorem and the classical Newton-polygon
   program is now certified on data, ray by ray.
3. **Exhaustive JC(2) at (2, 2) [MV].** In the affine gauge (linear parts normalized to the
   identity, WLOG since the linear part of a Keller map is invertible): the full Keller system
   for generic degree-(2, 2) maps has exactly 2 solution branches; all 6 clean instances have
   in-image fiber size <= 1. JC(2) holds mechanically at (2, 2) by our own certificate.

## Partial / honest limitations

- **(2, 3) and (3, 3) are NOT settled by this run.** sympy's solve returned an empty set for
  the (2, 3) system, which is a SOLVER ARTIFACT, not mathematics: the triangular map
  (x, y + a x^2 + b x^3) is an explicit Keller witness inside that ansatz, so branches exist
  and the solver failed to parametrize the underdetermined nonlinear system. The first
  monolithic run also timed out and was split. A proper approach (triangular decomposition /
  Groebner-cover of the solution variety) is queued as the EXP-013 continuation (JCB-021).
- The design note in the hypothesis stands: a naive "two-floor coprime kill" was discarded
  BEFORE running (floor 2 admits solutions); the full descent is the queued deeper cascade.

## Adversarial validation record

- The library maps are verified Keller exactly before use (det computed, constant, nonzero);
  the dependence checks are exact factorizations, not numerics.
- The (2, 3) empty-solve was refuted by an explicit witness rather than accepted: the failure
  mode (solver, not theorem) is itself demonstrated.

## Consequences

- Route 1 toward JC(2) (the tropical sweep) now has its foundation certified: at every ray the
  local model is the degenerate equivariant datum, exactly the object our rigidity theorem
  classifies. The next floor is the descent bookkeeping (Newton-polygon similarity and the
  divisibility constraints), queued with proper solver tooling.
- The affine-gauge trick (normalize linear parts, c = 1) is the right harness for exhaustive
  small-degree JC(2) certificates; (2, 2) is done, (2, 3)/(3, 3) need the better decomposition.
