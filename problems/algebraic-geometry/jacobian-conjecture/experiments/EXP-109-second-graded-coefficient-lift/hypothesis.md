# EXP-109: Second graded coefficient lift

## Question

Can the exact three-chart cover from EXP-108 be lifted through the next
lowest-support lower-family direction without returning to a dense
all-parameter determinant expansion?

## Coordinate

After \((0,7)\), EXP-106 ranks \((0,6)\) next by total selected support. Its
shared grading residue is \(7\). Write

\[
w=\varepsilon_{(0,6)},\qquad x=w/u^2.
\]

In the cleared residual-curve matrix the new direction is therefore
\(u^9xA_w=zxA_w\), while the existing invariant coordinates remain
\(z=u^9\) and \(y=v/u\).

## Pilot

1. Reconstruct the exact support and direction-rank bounds of all three
   EXP-108 charts after adding \(zxA_w\).
2. Use the existing exact unit cover at \(x=0\) to organize a recursive
   constructible-stratum computation; do not begin with a dense
   16-by-64-by-64 transform unless the support audit proves it necessary.
3. Compute resultants or Gröbner eliminants only on residual closed strata,
   selecting point-local charts after each specialization.
4. Stop after four charts or at the first positive-dimensional residual and
   persist the exact redirect.
5. Repeat modular closures and lift exact certificates before a
   characteristic-zero four-coefficient claim.

## Decision boundary

Closing this lift would exclude the declared four-coefficient slice only.
Failure names the next residual stratum; neither outcome decides the complete
GGHV family or JC(2).

Declared 2026-07-26 after the exact EXP-108 lift and before implementation.
