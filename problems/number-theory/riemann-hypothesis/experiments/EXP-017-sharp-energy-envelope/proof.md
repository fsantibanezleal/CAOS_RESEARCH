# Sharp retained energy for zero-sum spectra

Let m>=2, tau>0, sum x_i=0 and E=sum x_i^2. Put A=(m-1)/m,
s=sqrt(A*E), and psi(x)=x^2-(x-tau)_+^2. Cauchy applied to the
other m-1 entries gives x_i<=s. If s<=tau no entry is clipped.

Otherwise write P=sum_{x_i>0}x_i^2 and S=sum_{x_i>0}x_i. There is
at least one negative entry and at most m-1 negative entries. Thus
E-P>=S^2/(m-1)>=P/(m-1), so P<=A*E. For 0<x_i<=s,
(x_i-tau)_+^2<=x_i^2*(1-tau/s)^2. Summing gives clipping loss
at most A*E*(1-tau/s)^2=(s-tau)^2. Therefore

    sum psi(x_i)>=E-(s-tau)^2=E/m+2*tau*s-tau^2.

The sharp envelope F_m(E) is E below E0=tau^2/A and the displayed
expression above E0. Equality at every E occurs at
x_1=s, x_2=...=x_m=-s/(m-1). For E<=m*(m-1), s<=m-1 and this
is the displacement spectrum of the PSD unit-diagonal matrix
U=(1-s/(m-1))*I+(s/(m-1))*J. No realizability by a zeta window
Gram matrix is asserted; sharpness concerns the larger stated class.

## Independent scalar minorant

For s>tau set r=-s/(m-1), b=(s-tau)^2/(s-r)^2, lambda=1-b,
mu=2*b*r and kappa=-b*r^2. Since 0<b<1, lambda>0. For x<=tau,

    psi(x)-lambda*x^2-mu*x-kappa=b*(x-r)^2>=0.

For tau<=x<=s the same difference is a concave quadratic, nonnegative
at tau and zero at s. Thus it is nonnegative throughout. All entries
lie below s, so summing the minorant and using sum x_i=0 gives
lambda*E-m*b*r^2=E-(s-tau)^2. This derivation does not sum positive
energies and independently confirms the sharp formula.

## Pressure transfer without a hard block cutoff

For E>E0, F'(E)=1/m+tau*sqrt(A/E), F''(E)<0. At E0 the derivative
is 1, matching the linear lower branch. Consequently F is increasing,
concave, F(0)=0, and 1-Lipschitz. If p,W,D>=0 and E+p*W>=D, then
F(E)+p*W>=F(D): monotonicity handles E>=D, and the Lipschitz bound
F(D)-F(E)<=D-E<=p*W handles E<D. Hence clipped_energy+p*W>=F(D).
The p,W>=0 assumptions are essential.

For the source's block, D=delta*(m-6). Replace the old lower energy
coefficient by any a<=F_m(D)/m. Summing over blocks and phase-averaging
keeps beta=6*p*(1-6/m). The unchanged mixed-multiplicity threshold
and counting proof applies if c>=max(1+tau,2+tau/2),
6*c-7-c^2>=a and 4*c-2-c^2>=2*a. It yields the attributed
distinct-strip lower proportion (1+H0-beta)/(2-a).

The new lower energy coefficient is usually smaller than delta*(m-6)/m
above the old clipping cutoff, but allows larger blocks. EXP-013/016's
restricted-assembly caps remain valid. The present candidate uses exact
rational square-root brackets and does not claim a global optimum.

## Prior art and limitations

The tau=1 formula and pressure transfer already appear in
trmdy/zeta-simple-zeros-673137/docs/refined-deduction.md at pinned commit
1610b97, with attribution to tawanerguo-cn/zeta-simple-zeros. Its original
trace_energy_envelope.md explicitly proves the pressure implication at
A=1.02129. Scaling x and E shows F_tau(E)=tau^2*Phi_m(E/tau^2):
this formula is prior art, not an independent novelty claim. The uniform
all-energy proof and scalar minorant here avoid that source's restricted
multi-clipped case analysis. Classical trace/variance bounds are also
acknowledged (Wolkowicz--Styan, 1980). The independent
algebraic check supports the uniform proof, whereas finite controls only
test implementation. The consequence retains Knausgard's analytic/local
inputs, does not independently replay them, and changes neither a
simple-critical proportion nor the 0.534 short-window onset nor RH.
