# EXP-027: shifted composite Voronoi dual for the actual signed moment

Declared 2026-10-04 before code and computation. RH-F4 / issue #360 remains
primary. EXP-026 closes its own bounded route; this returns to EXP-024's
unevaluated shifted additive-divisor average. No new focus is introduced.

For sigma_(a,b)(n)=sum_(uv=n)u^(-a)v^(-b), define
D_(a,b)(s,A/q)=sum sigma_(a,b)(n)e(An/q)n^(-s), gcd(A,q)=1.
Test and prove the full shifted functional equation

    D_(a,b)(s,A/q)=2 q^(1-2s-a-b) (2pi)^(2s+a+b-2)
      Gamma(1-s-a) Gamma(1-s-b)
      [cos(pi(a-b)/2) D_(-a,-b)(1-s,+Ainv/q)
       -cos(pi(s+(a+b)/2)) D_(-a,-b)(1-s,-Ainv/q)].

Apply it by Mellin inversion to a smooth compact profile, retaining the
two poles 1-a and 1-b, their coalescent limit and both transformed phases.
In EXP-024 the shifts are a=alpha, b=-beta. Keep the squarefree gcd class,
both mollifier polynomials and their coupled cutoff in the outer sum.

P1: the exact inputs are DLMF 25.11.1, 25.11.9 and the established
meromorphic continuation. The finite Hurwitz representation and the full
modular double Fourier sum derive this classical equation directly.
Bettin 1607.05595v1 and Tang 2608.14852v1 are already archived and reviewed
in the source dossiers; their pointwise reciprocity is not a short-window
signed asymptotic. No new method priority is claimed.
P3: EXP-021 supplies the actual gcd/mollifier bookkeeping; EXP-024 supplies
the smooth-window signed representation with absolute o(H) errors.
P5: modular orthogonality decides both inverse signs before numerical work.

Controls: standard-library integer cyclotomic reduction for the complete
double Fourier sum at q=1,...,12, A=1 and q-1 (deduplicated), all n,m mod q;
32 interval functional-equation controls at q in {1,3,6,8}, unshifted,
unequal real, unequal complex and equal shifts, two non-pole s values.
Reject phase reversal, lost composite nonunit classes and shift reversal
on specified nondegenerate cases. Native controls share FLINT/Arb between
Hurwitz paths; exact finite arithmetic and the analytic proof are separate.

PASS resolves the normalization and exact transformed signed sum, not its
asymptotic size. FAIL records a phase, pole, shift or contour mismatch before
repair. Sixty seconds CPU, one worker, immutable receipt; a budget hit is
inconclusive. No parameter sweep, GPU, new zero bound or publication follows
from this supporting transformation. A new manuscript requires the remaining
uniform signed estimate and a certified onset below 0.534.
