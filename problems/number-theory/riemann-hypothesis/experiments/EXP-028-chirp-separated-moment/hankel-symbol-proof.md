# Exact Hankel symbols: second analytic route to the separation estimate

This closes the differentiated-symbol assumption in the first candidate by
an exact integral, rather than by an unquantified asymptotic replacement.
It is classical Bessel analysis, not a new special-function identity.

For x>=1 and complex d in a fixed compact subset of |Re d|<1/2, define

    a_+(x,d)=1/Gamma(d+1/2) * integral_0^infinity
       e^(-t)*t^(d-1/2)*(1+i*t/(2*x))^(d-1/2) dt,
    a_-(x,d)=1/Gamma(d+1/2) * integral_0^infinity
       e^(-t)*t^(d-1/2)*(1-i*t/(2*x))^(d-1/2) dt.

Principal logarithms are unambiguous. DLMF 13.6.10 and 13.4.4 give, first
for positive real z and then for Re z>0 by analytic continuation,

    K_d(z)=sqrt(pi/(2z))*e^(-z)/Gamma(d+1/2)
       * integral_0^infinity e^(-t)*t^(d-1/2)
                     *(1+t/(2z))^(d-1/2)dt.

Dominated convergence allows z to approach -i*x or +i*x from Re z>0.
The factors 1+t/(2z) do not approach a branch cut or zero. Combining with
DLMF 10.27.8 yields the exact, remainder-free identities

    H_d^(1)(x)=sqrt(2/(pi*x))*e^(i*(x-pi*d/2-pi/4))*a_+(x,d),
    H_d^(2)(x)=sqrt(2/(pi*x))*e^(-i*(x-pi*d/2-pi/4))*a_-(x,d).

Every fixed symbol derivative is uniformly bounded:

    |x^k * partial_x^k a_+|+|x^k * partial_x^k a_-| <<_(k,compact) 1.

Indeed differentiation produces fixed combinations of
(t/x)^j*(1+/-i*t/(2*x))^(d-1/2-j). Its magnitude is bounded by a fixed
constant times |1+/-i*t/(2*x)|^(Re d-1/2), since
(t/x)/|1+/-i*t/(2*x)|<=2. The imaginary power is bounded on the compact
order set by exp(pi*|Im d|/2), and Re d-1/2<0. The remaining t integral
is dominated by e^(-t)*t^(Re d-1/2), integrable uniformly away from
Re d=-1/2. The gamma denominator is also uniformly bounded. This proves
all fixed differentiated bounds without summing an asymptotic series.

Writing J=(H^(1)+H^(2))/2 and Y=(H^(1)-H^(2))/(2i), the oscillatory
combination in EXP-027 is exactly

    sin(pi*d/2)*J_d(x)+cos(pi*d/2)*Y_d(x)
      =sqrt(2/(pi*x))*[-(i/2)*e^(i*(x-pi/4))*a_+(x,d)
                       +(i/2)*e^(-i*(x-pi/4))*a_-(x,d)].

There is no singular quotient at d=0. Both phases remain present.

## Normalized profile and absolute separation cost

Use the actual finite EXP-024 profiles and x=T/(2pi)+Hv/(2pi).
Their v profiles and every fixed derivative have uniformly bounded
Schwartz seminorms, as proved from the defining Gaussian Fourier integral
in mellin-proof.md. Factors from x/T and the central cutoff have bounded
v derivatives, because x~T and H/T<=1. The exact symbols above add only
bounded differentiated factors. The small-shift powers are assigned to
the three arithmetic sequences, with bounded remaining x powers.

For a dual block n~N,p~P,q~Q, put r=n/(pq),
lambda=sqrt(N*T/(PQ)), mu=H*sqrt(N/(T*PQ)). The oscillatory phase
4pi*sqrt(r*x) has v derivative comparable to mu on the full central
band. Each higher v derivative divided by its first derivative is
O_k((H/T)^(k-1)), hence bounded. Repeated nonstationary integration by
parts therefore gives an arbitrary fixed mu^(-A) gain. The amplitude
derivatives have uniform L1 bounds; the cutoff has vanishing endpoints.
Schwartz tails cover the entire central band, including v of order T/H.

One derivative in log r inserts a phase factor O(lambda) or differentiates
an exact symbol. Applying the same integrations by parts with this insertion
gives the same gain times 1+lambda. Smoothly cut off log r on an interval
of fixed length covering all ratios in the dyadic block. For the normalized
profile W, after removing H/[g*(PQ)^(3/4)*T^(1/4)]*n^(-1/4), this proves

    ||W||_2+(1+lambda)^(-1)||W'||_2 <<_A (1+mu)^(-A).

With Fourier convention What(t)=integral W(v)e^(-itv)dv, Cauchy-Schwarz
and Parseval give, for L=1+lambda,

    (1/(2pi))*integral |What(t)|dt
       <=sqrt(L/2)*(||W||_2^2+L^(-2)||W'||_2^2)^(1/2).

At each frequency r^(it)=n^(it)*p^(-it)*q^(-it), so all coefficients
are separated and unimodular twists do not alter their l2 norms.
For fixed g these norms are O(P^(1/2)), O(Q^(1/2)) and
O_epsilon(N^(1/4+epsilon)), including both mollifier cutoffs and weights.
The source parameter factor (1+N/(PQ))^(1/2) is retained.

The resulting ratio to H, before summing N, is bounded by

    (1/g)*[N^(17/20)*(PQ)^(-3/20)*(P+Q)^(1/4)
            +N*(PQ)^(-1/8)*(P+Q)^(1/8)]
       *(1+N/(PQ))^(1/2)*(1+sqrt(N/N0))^(-A)*T^epsilon,
    N0=T*P*Q/H^2.

Both N powers are positive below N0; above it a sufficiently large fixed
A absorbs both powers and the growing source factor. If N0<1 every
dyadic integer block lies in that tail and gives a stronger bound.
Evaluating the bound at N0 reproduces (7) in mellin-proof.md exactly.
Its absolute gamma route is coarser at smaller N but has the same dominant
scale. The main residues and compact-window conversion are reviewed
separately; this lemma alone does not establish a zero count.

Primary identities: https://dlmf.nist.gov/13.6.E10,
https://dlmf.nist.gov/13.4.E4, https://dlmf.nist.gov/10.27.E8.
