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

## Next obligation

The remainder records weighted spectral mass at doubled rows, not merely
their count. A useful counting improvement must lower-bound that mass using
gap geometry and charge the isolation cost to the available total pressure.
The local source theorem by itself does not supply this lower bound. No
larger sweep, new proportion, manuscript or new version follows here.
