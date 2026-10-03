# Vector-pressure mixed-Gram transfer

This proof establishes an implication from an explicitly attributed universal
local theorem. Its concrete source binding and an independent numerical
window enclosure are in preflight.json. A complete independent review and
the final source-overlap assessment still determine the result disposition.

## Local input and block estimate

Let f be an even, nonnegative profile of integral one, supported on [-1/2,1/2].
Write K(x)=integral f(t) exp(2*pi*i*x*t)dt and w(x)=K(x)^2 for real x.
For a positive integer r, suppose a_ij>=0 and b_i>=0 satisfy

    sum_i a_(i,i+s) <= 2  for every index span s,
    sum_(i<j) a_ij*w(g_i+...+g_(j-1)) + sum_i b_i*g_i >= delta

for every nonnegative r-gap vector. Put B=sum_i b_i.

For an ordered m-point block, sum its m-r contained local inequalities.
Each unordered pair of a given index span has total coefficient at most
two. Thus its unit-diagonal Gram matrix U, with E=tr(U-I)^2, satisfies

    E + P_block >= D=delta*(m-r),

where P_block is the sum of the local vector pressure charges.
Every charge is nonnegative. For tau>0 define

    Psi_tau(x)=(x-1)^2-(x-1-tau)_+^2,  x>=0.

This is convex and nonnegative on [0,infinity), vanishing at one. If
all eigenvalues are <=1+tau, tr(Psi_tau(U))=E. Otherwise a single
eigenvalue contributes more than tau^2. Consequently D<=tau^2 implies

    tr(Psi_tau(U)) + P_block >= D.

This elementary dichotomy does not require a trace-zero sharp envelope.

## Global pressure charge and endpoints

Order l real points y_0<...<y_(l-1). For each of m offsets partition the
list into consecutive complete m-point blocks, omitting the two shorter
endpoint blocks. Pinching and convexity of Psi_tau give the full Gram
defect at least the sum of its complete-block defects; omitted singleton
diagonals contribute zero. Across all offsets, a fixed r-gap window is
contained in at most m-r complete blocks. Each gap participates in local
windows with total pressure at most B. Therefore the averaged total
pressure charge is at most B*(m-r)/m*(y_(l-1)-y_0).

There are exactly max(l-m+1,0) complete blocks across all m offsets, so
their average is at least l/m-1. The preceding estimates prove, also when
l<m or l=0,

    tr(Psi_tau(U_full)) >= a*l-beta*span-D,
    a=delta*(m-r)/m, beta=B*(m-r)/m.

Using the weaker endpoint term -2D is harmless. This derivation shows why
the total B, rather than r*min_i b_i, enters the zero-counting charge.
No assumption of equal pressures is needed.

## Complex-zero operator and multiplicity counts

Use the finite-rank Hermitian complex-zero operator from the integrated
BGSTB pair-correlation transfer reviewed in EXP-019/analytic-transfer-review.md.
Let N count all zeros with multiplicity, Nd count distinct strip points,
h count critical-line points of multiplicity >=3, and k count off-line
functional-equation pairs. The remaining l=Nd-h-2k critical-line points
have multiplicity one or two. Their contribution P is positive semidefinite;
the remainder Q has positive rank at most h+k. The threshold inequality is

    tr(P+Q)^2 >= 2c*N-2c*tr(P)+tr(phi_c(P))-c^2*(h+k),
    phi_c(x)=x^2-(x-c)_+^2.

For the low-multiplicity Gram matrix U and diagonal D0 with entries one
or two, set X=U-I, C=min(X,tau), M=D0^(-1/2)*C*D0^(-1/2),
and A=2D0+2M. If c>=max(1+tau,2+tau/2), then A<=2cI.
The dual completion of squares gives

    tr(phi_c(P))-tr(D0^2) >= 2tr(CX)-tr(M^2)
                             >= 2tr(CX)-tr(C^2)
                             = tr(Psi_tau(U)).

The second inequality holds entrywise since the factors d_i*d_j>=1.
It does not assume C or M is positive semidefinite. The threshold and
mixed-Gram inequalities, their multiplicity minima and operator construction
are attributed source machinery, independently reviewed in EXP-019.

For completeness the threshold completion is elementary. Write Q=Q_+-Q_-,
with Q_+*Q_-=0. Then tr(P-Q_-)*Q_+=tr(P*Q_+)>=0. Completing squares on
Q_+ gives tr(Q_+^2)>=2c*tr(Q_+)-c^2*rank(Q_+). Minimizing the remaining
quadratic in Q_- over positive semidefinite matrices gives
-tr((P-cI)_+^2), proving the stated threshold. For any Hermitian A<=2cI,
Loewner eigenvalue monotonicity implies
tr((P-A/2)^2)>=tr((P-cI)_+^2), so
tr(phi_c(P))>=tr(A*P)-tr(A^2)/4. Substitution of A=2D0+2M,
tr(D0^2*U)=tr(D0^2) and tr(M*P)-tr(D0*M)=tr(C*(U-I)) proves
the mixed completion without a commutativity assumption.

The low-multiplicity identity is tr(D0^2)=3*tr(D0)-2*l. The high-point
and off-line multiplicity mass is at least 3h+2k. Since 2c-3>=0, the
threshold becomes

    tr(P+Q)^2 >= 3N-2Nd+(6c-7-c^2)*h+(4c-2-c^2)*k
                              + tr(Psi_tau(U)).

This independently reconstructs both residual coefficients rather than
assuming a simple-zero proportion can be converted to this stronger count.

## Analytic energy and limit order

For fixed smooth compact approximations f_epsilon to f, supported strictly
inside (-1/2,1/2), apply integrated BGSTB Lemma 5 separately to
R=f_epsilon*f_epsilon and R''. Its published correction preserves that
integrated lemma. Multiplication of the entire Fourier transform by
1+pi^2*z^2/log(T)^2 cancels the complex pair weight, as derived in the
EXP-019 review. The energy coefficient tends to

    C_f=(integral f^2 + double integral |s-t|f(s)f(t)dsdt),
    H_f=2-C_f.

The normalized low-multiplicity real-point span is <=N+o(N) by
Riemann-von Mangoldt. The scalar function Psi_tau is Lipschitz on the
nonnegative spectrum with constant 2*max(1,tau). Entrywise perturbation
of K by ||f_epsilon-f||_1 changes an m-point clipped trace by at most
2*max(1,tau)*m^2*||f_epsilon-f||_1. Thus summing fixed-size blocks costs
O_(m,tau)(||f_epsilon-f||_1)*N. Choose the window, m, tau and c first;
let T tend to infinity next, and only then remove the smooth cutoff.
No gap-dependent approximation, growing block size or effective onset
is used. The integrated analytic theorem is an attributed input, not a
consequence of a finite scalar calculation.

Combining these estimates with the threshold/multiplicity counting gives

    (2-a)*Nd >= (1+H_f-beta)*N+(6c-7-c^2-a)*h
                                  +(4c-2-c^2-2a)*k-o(N).

Hence, if 2-a>0 and both final residuals are nonnegative,

    liminf_(T->infinity) Nd(T)/N(T) >= (1+H_f-beta)/(2-a).

This counts distinct points across the whole critical strip. It is neither
a simple critical-line proportion nor a proof of RH. It carries no effective
height and does not establish external peer acceptance or worldwide novelty.

## Concrete attributed input

Lavery's attempt-013 cert_AM proves the local inequality for every
nonnegative six-gap vector, with the normalized thirteen-term kernel
wfunAM. Its kernel definition is exactly the Fourier normalization above;
the scaling MAM cancels. The named source arrays equal its certified
functional G, including every individual pressure and weight. Its reported
external Lean/nanoda check is retained as an attributed check; no local
rebuild is asserted. The independent window evaluation proves
H_f>=33608554629/50000000000.

With the predeclared r=6, m=742, delta=39369/5000000,
B=199193/50000000, tau=12043/5000 and c=17043/5000, every exact
condition above passes, and the fraction is

    30945470743359/36955122080000 = 0.8373797460706156... .

An independent final audit, actual vector-charge accounting controls and
source-overlap review remain necessary before a final consequence verdict.
