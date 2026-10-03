# Certified second-order box lower bound

Let F be C^2 on a convex box B and x0 in B. Suppose a symmetric positive
definite matrix H satisfies Hessian(F)(x)-H positive semidefinite for
every x in B. For h=x-x0, two integrations along the segment give

    F(x)-F(x0)-grad(F)(x0)^T h
      =integral_0^1 (1-t) h^T Hessian(F)(x0+t*h) h dt
      >=1/2*h^T H h.

Complete the square:

    g^T h+1/2*h^T H h
      =1/2*(h+H^-1*g)^T H*(h+H^-1*g)-1/2*g^T H^-1*g
      >=-1/2*g^T H^-1*g.

This is a universal lower bound on B, even when the minimizer of the
quadratic lies outside B. It need not dominate the first-order box bound;
use either bound when it proves the target.

If H=L D L^T is a certified positive-pivot LDL decomposition, solve
L z=g by forward substitution. Then g^T H^-1*g=sum z_i^2/D_i.
All coefficients of H are exact dyadic lower coefficients from the
source's signed interval Hessian minima. Positive pivots are proved by
Arb, and the substitution/loss use Arb intervals. Taking the enclosure of
F(x0)-loss/2 therefore encloses the exact lower expression. Interval
dependency can weaken a bound but cannot justify an unsafe pruning.

Independent exact SymPy inversion and direct completion-of-squares
controls check dense rational positive matrices at 128 and 256 bits.
Indefinite, singular and uncertain pivots are rejected. These controls
test the implementation; the preceding uniform argument supplies the
mathematical justification. General quadratic lower bounds are classical;
the proposed new numerical input still requires the entire interval cover.
