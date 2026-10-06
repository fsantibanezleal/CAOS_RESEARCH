# Verified numerical linear algebra: overlap and next obligation

Primary source: S. M. Rump, [Verification of positive definiteness](https://www.tuhh.de/ti3/paper/rump/Ru06c.pdf),
BIT Numerical Mathematics 46 (2006), 433-452. The paper derives verified
Cholesky tests with rounding/underflow bounds, an interval-matrix extension,
scaling and eigenvalue enclosures. Source URL, cache hash and review scope are
in `source-manifest-rump-20261004.json`. No numerical criterion is imported
into the frozen EXP-023 run.

## An apparent new route is already implemented

Inspection of the pinned `code/rh019_vendor/quadratic_partitioned.py`,
`convex_tangent_lower`, disproves the premise that the present checker uses
only a Gershgorin curvature bound. It already builds a lower Hessian from
pair-span second-derivative bounds, runs a floating LDL prefilter, verifies
positive pivots with Arb, and applies both a tangent and a quadratic lower
bound. Merely adding verified LDL or unconstrained quadratic minimization
would duplicate existing work, not constitute a new method or discovery.
The earlier completed EXP-020 uses the corresponding quadratic machinery.

## A materially different candidate

Independent minima for each pair span can discard correlations among sums
of the same eight gaps. On a box, write

`H(x) = sum a_ij w''(v_ij . x) v_ij v_ij^T`.

Nonnegative weights make `H(x) >= M = sum a_ij ell_ij v_ij v_ij^T` when every
`ell_ij` bounds that pair term throughout the box. The frozen verifier already
uses this implication. If M is indefinite, more accurate LDL arithmetic alone
cannot turn it into a positive matrix. A prospective improvement must retain
the shared gap dependence: for example, a matrix Taylor/Bernstein enclosure
with rigorous remainders, or a certified rational polynomial matrix witness
on a declared subbox. This is an inference and an untested path, not a theorem
upgrade. Polynomial approximations without uniform remainder control fail.

Before implementation, a bounded preflight must identify an actual box where
the current bound fails, distinguish real curvature from enclosure loss,
establish a uniform stronger minorant and measure verification cost. Any new
checker needs source binding, adverse rounding/singularity controls and a
complete cover audit. No change to the present frozen worker, no new bound,
no new manuscript and no additional large traversal are admitted by this note.
RH-F4's signed analytic estimate remains the principal alternative research
target; the completed EXP-020/025 release remains the delivery priority.
