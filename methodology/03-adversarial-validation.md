# 03 - Adversarial validation

No positive finding is believed, written into the wiki, shown on the web, or claimed in the
manuscript until it survives a refutation attempt. The attempt and its output are persisted with
the finding (normally inside the experiment's `verdict.md`, or as a dedicated follow-up EXP).

## The ladder (stronger routes first; use the strongest applicable)

1. **Exact re-derivation by an independent route.** A second symbolic derivation using a different
   algorithm, ordering, parametrization or library than the one that produced the finding
   (e.g. verify a determinant both by cofactor expansion and by Bareiss/LU over the rationals;
   verify a fiber both by Groebner elimination and by resultants).
2. **Certified numerics.** Interval arithmetic, rational certificates, alpha-theory certificates
   for root counts; the certificate object is persisted, not just its conclusion.
3. **Cross-implementation agreement.** Two independent codes (ideally one CPU-symbolic, one
   GPU-numeric) agreeing within proven bounds.
4. **Stress families / null models.** The finding is run against cases engineered to break it
   (degenerate parameters, boundary weights, adversarial seeds). Surviving the designed attack is
   the evidence.

## Always, additionally

- `verdict.md` carries a **"how could this be wrong?"** section: the residual failure modes the
  validation does NOT exclude (e.g. "identity verified for degrees up to 12; the general-degree
  statement remains a conjecture of ours").
- Claims imported from literature are re-verified from the primary source (or re-derived) before
  they carry weight in an argument; otherwise they stay flagged UNVERIFIED and no conclusion may
  depend on them.
- Null and negative results are recorded with the same care as positives; they gate future
  strategy and are citable inside the repo.
