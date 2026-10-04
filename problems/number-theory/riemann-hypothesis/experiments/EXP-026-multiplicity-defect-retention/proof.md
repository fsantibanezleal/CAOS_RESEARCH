# Retained multiplicity remainder and an isolation obstruction

The completion machinery is attributed to the mixed-Gram argument reviewed
in EXP-025. The retention below is elementary matrix algebra, without a
priority claim. It does not yet improve a zero proportion.

## Exact retained term

Use the notation and hypotheses of `hypothesis.md`. With A=2D+2M, the bound
C<=tau*I gives A<=2cI: its diagonal upper bound is
2(D+tau*D^(-1)), at most 2cI. For Hermitian A<=2cI, eigenvalue monotonicity
and completion of squares give

    tr(phi_c(P)) >= tr(A*P)-tr(A^2)/4.

Substitute A and P. Since U has diagonal one, tr(D^2*U)=tr(D^2),
and cyclicity gives tr(M*P)-tr(D*M)=tr(C*X). Hence

    tr(phi_c(P))-tr(D^2) >= 2tr(C*X)-tr(M^2)
      = tr(Psi_tau(U)) + Gamma_D(C),
    Gamma_D(C)=sum_(i,j) (1-1/(d_i*d_j))*|C_ij|^2.

No commutativity of D and C is assumed. Let E_22 sum |C_ij|^2 over
ordered doubled/doubled indices, and E_21 sum it over doubled/simple
indices (one orientation). Hermitian symmetry yields the exact identity

    Gamma_D(C)=(3/4)*E_22+E_21
              =(3/4)*tr(J*C^2)+(1/4)*E_21.

It strengthens the declared half-factor to three quarters. The coefficient
3/4 is sharp for this remainder inequality: D=2I gives M=C/2 and
Gamma_D(C)=(3/4)*tr(C^2). This does not assert sharpness of the complete
phi_c lower bound or a new zero-counting optimum.

## A count-only gain fails for actual point Grams

Let f be EXP-025's normalized positive window, K its Fourier transform,
and a=K(1/2). Positivity on the interior of [-1/2,1/2] implies 0<a<1:
cos(pi*t)>0 there, and is strictly below one off t=0. The integrable compact
window has K(x)->0 by the Riemann-Lebesgue lemma.

Take the three real points -R,0,1/2 and D=diag(2,1,1). Set
u_R=K(R)^2+K(R+1/2)^2. With tau=12043/5000, a three-point unit-diagonal
Gram has X<=2I<tau*I, so C=X and Psi_tau(U) has trace 2(a^2+u_R).
The weighted Gram converges to diag(2, [[1,a],[a,1]]), whose largest
eigenvalue is two. Therefore for all sufficiently large R it has
lambda_max<c=17043/5000 and no phi_c clipping. Direct expansion then gives

    tr(phi_c(P))-tr(D^2)=2*a^2+4*u_R,
    Gamma_D(C)=2*u_R,
    [tr(phi_c(P))-tr(D^2)]/tr(Psi_tau(U))
      =1+u_R/(a^2+u_R) -> 1.

Thus no factor 1+eta*(number_of_twos/m), eta>0, is valid for all such
point Grams. The doubled point can become spectrally isolated while the
simple pair retains positive energy. This is a genuine limiting point
Gram family, not a sampled zeta-zero configuration. It refutes a proposed
uniform transfer inequality; it does not assert that actual zeta zeros
realize that configuration or refute a pressure-constrained refinement.

## Isolation also occurs below the local pressure budget

The separately declared compact check supplies six disjoint rational
brackets of width at most 2^-40 inside (1/2,8). Each has opposite certified
kernel signs at its endpoints. Choose a root r_j in each bracket by the
intermediate value theorem. The kernel is continuous and is the Fourier
transform of the pinned positive window, so the seven-point matrix for
0,r_1,...,r_6 is a positive semidefinite unit-diagonal Gram.

Let D=diag(2,1,1,1,1,1,1). Since K(r_j)=0 exactly, U=1 direct-sum V:
the doubled point is isolated, rather than merely approximately isolated.
Interval bounds valid for every choice of roots in their brackets give
lambda_max(U)<1.261 and lambda_max(P)<=2, both below c=3.4086.
Thus C=X, both spectral clippings are inactive, and

    Gamma_D(C)=0,
    tr(phi_c(P))-tr(D^2)=tr(Psi_tau(U))=tr(V-I)^2>0.

The independent rational audit bounds this positive energy between
0.07308382802969 and 0.07308382803629. It also encloses the actual unequal
vector-pressure charge between 0.003950876179377 and
0.003950876179385, strictly below delta=0.0078738. All six gaps are positive.
The doubled count is one, so any strictly positive count-only remainder
bound, or the declared multiplicative factor 1+1/70, fails even on this
pressure-constrained family. This is a point-Gram counterexample; these
locations are not asserted to be actual zeta zeros.

The native check uses analytic sinc integrals at 256 bits. The separate
standard-library audit parses the source independently and uses the formula

    K(x) = [ (theta*sin(theta)*cos(pi*x)
               - pi*x*cos(theta)*sin(pi*x))/(theta^2-pi^2*x^2)
             + sum_(j=1)^12 c_j*(-1)^j*x*sin(pi*x)/(pi*(x^2-j^2)) ] / Z,
    theta=sqrt(2)/2, Z=sin(theta)/theta.

Its argument-reduced Taylor, Machin-pi and integer-square-root intervals
use outward rational arithmetic on a 65-decimal grid, without FLINT/Arb.
No denominator crosses zero on the audited inputs. Both implementations
prove all twelve endpoint signs, all fifteen simple-pair bounds, clipping,
energy and pressure. Reversed and overlapping brackets and changed source
bytes are rejected by the independent audit. Root uniqueness is unnecessary:
each disjoint bracket supplies a different point, and the bounds cover all
choices. Positivity of the window is checked independently as well.

## Next obligation

The remainder records weighted spectral mass at doubled rows, not merely
their count. Pressure alone cannot supply a strictly positive lower bound:
the compact witness meets that constraint with remainder zero. A viable
refinement must control the sum of the baseline local slack and the retained
term, rather than the term by itself. That joint estimate remains unproved.
No larger sweep, new proportion, manuscript or new version follows here.
