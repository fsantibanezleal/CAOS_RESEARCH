# Independent mathematical review of the distinct-strip transfer

The numerical window audit is complete. The local inequality remains in
flight. This document reviews the logical implication, not a completed
stronger zeta proportion.

## Analytic dependency, including its correction

The published unconditional complex-zero pair-correlation input is
Baluyot, Goldston, Suriajaya and Turnage-Butterbaugh,
[arXiv:2306.04799v1](https://arxiv.org/abs/2306.04799v1), Lemma 5.
Its complete statement and proof were reread from the newly archived TeX.
The authors' correction in
[arXiv:2501.14545v3](https://arxiv.org/abs/2501.14545v3), Section 3,
corrects the uniform pointwise error but explicitly preserves the earlier
integrated Lemmas 5 and 7. The corrected proof for (0,T] and its closing
estimate were also inspected. All four PDF/source bytes are pinned in
`context/source-manifest-exp019-analytic.json`; originals stay in the local
research archive under their original distribution terms.

For fixed smooth even f_epsilon=eta_epsilon^2 supported inside (-1/2,1/2),
let R=f_epsilon*f_epsilon and L=log(T). Both R and R'' are real, even,
integrable and Lipschitz at zero, with support strictly inside [-1,1].
Their entire Fourier transforms satisfy

    Fourier(R-R''/(4*L^2))(z)=(1+pi^2*z^2/L^2)*K_epsilon(z)^2.

At z=i*(rho-rho')*L/(2*pi), the first factor equals
1-(rho-rho')^2/4, the reciprocal of the pair weight. Apply Lemma 5
separately to the two fixed functions R and R'', then combine with the
T-dependent scalar 1/(4*L^2). This avoids applying its error bound to a
varying test function. The R'' contribution is O_epsilon(N/L^2), and the
remaining energy coefficient is

    C(f_epsilon)=integral f_epsilon^2
                +double integral |s-t| f_epsilon(s)f_epsilon(t) ds dt.

Smooth cutoffs and normalization give L1 and L2 convergence to f=v/I1.
Thus C(f_epsilon) tends to (I2+J)/I1^2, whose enclosure is independently
certified in `artifacts/window-audit.json`. This step uses the published
analytic theorem; the scalar computation is not a substitute for it.

## Operator and threshold checks

The functional equation pairs off-line zeros at the same height and
multiplicity. At z=i*(rho-1/2)*L/(2*pi), the finite-rank operator
sum nu_z F_z outer F_conjugate(z) is Hermitian with trace N and square
trace equal to the entire-kernel pair sum. An off-line pair has the form
nu*(v outer w+w outer v), a difference of two positive rank-one matrices,
so it has at most one positive eigenvalue. No termwise nonnegativity of
the complex pair sum is assumed.

Split the low-multiplicity on-line contribution P>=0 from the remainder
Q, whose positive rank is at most h+k. Set phi_c(x)=x^2-(x-c)_+^2.
Writing Q=Q_+-Q_- and using Q_+Q_-=0, the cross term of P-Q_-
with Q_+ is nonnegative. Scalar completion of squares on Q_+ and
the positive/negative decomposition of P-cI give

    tr(P+Q)^2 >=2c*N-2c*tr(P)+tr(phi_c(P))-c^2*(h+k).

The mixed Gram bound of
[Knausgard, arXiv:2609.33043v1](https://arxiv.org/abs/2609.33043v1),
Theorem 2, was independently reread with its proof and the entire counting
assembly. For U with unit diagonal and D with diagonal entries 1 or 2,
put X=U-I, C=min(X,tau), M=D^-1/2*C*D^-1/2 and B=2D+2M.
Since c>=max(1+tau,2+tau/2), B<=2cI. The dual completion of squares gives

    tr(phi_c(D^1/2*U*D^1/2))-tr(D^2)
      >=2tr(CX)-tr(M^2)
      >=2tr(CX)-tr(C^2)=tr(Psi_tau(U)).

Here tr(M^2)<=tr(C^2) follows entrywise from d_i*d_j>=1. Combining
the two inequalities yields exactly the high-point residual
rh=6c-7-c^2 and off-line-pair residual rk=4c-2-c^2. The multiplicity
minima are valid because c>=2: the residuals increase with multiplicity.

## Window summation and endpoint controls

For an r-gap certificate with nonnegative weights and each span capacity
at most 2, summing the m-r contained windows counts any pair with total
weight at most 2, so E+pW>=delta*(m-r). The sharp zero-sum envelope from
EXP-017 is nondecreasing and 1-Lipschitz, giving
clipped_energy+pW>=F_m(delta*(m-r)).

Pinching is valid for the convex scalar Psi_tau, which is nonnegative on
the nonnegative spectrum. Across all m partition offsets, each complete
r-gap window occurs in m-r partitions and each gap belongs to at most r
windows. Therefore the averaged pressure charge is at most
r*p*(m-r)/m times the total span. Fewer than 2m omitted endpoint points
cost only O_m(1). If there are no complete blocks, nonnegativity and this
same endpoint allowance still prove the inequality.

Replacing K by K_epsilon perturbs every Gram entry by at most
d_epsilon=||f_epsilon-f||_1, uniformly at every real argument. For fixed
m, the operator norm changes by at most m*d_epsilon and the clipped
trace by at most max(2,2tau)*m^2*d_epsilon. Its summed error is
O_(m,tau)(d_epsilon)*N. No gap-dependent compact-uniform assumption or
exchange of m with T is required. Choose m,tau,c first, let T tend to
infinity next, and only then let epsilon tend to zero.

With l=Nd-h-2k and span<=N+o(N), the final implication is

    (2-a)*Nd >= (1+H-beta)*N+(rh-a)*h+(rk-2a)*k-o(N),
    a<=F_m(delta*(m-r))/m, beta=r*p*(m-r)/m.

All residual and denominator conditions in EXP-018 are exact. This review
found no logical change needed in that conditional transfer. It does not
close incomplete interval coverage, establish external peer acceptance,
or prove the Riemann hypothesis.
