# Supported collision theorem and boundary

## Uniform existence of the supported twists

For primes after 7, enlarge their set to every odd integer at least 11.
Since 1/x^2 decreases, the step-two integral bounds their reciprocal-square
sum by 1/121+(1/2) integral_11^infinity x^(-2) dx = 1/121+1/22.
Adding the four earlier primes gives the declared rational S<12/25.

Let I=[ceil(M/2),floor(3M/4)], with L integer points. For a prime p,
at most L/p^2+1 points satisfy p^2|h, and at most that many satisfy
p^2|(h-1). All relevant primes satisfy p<=sqrt(M). The union bound
therefore leaves at least L(1-2S)-2 floor(sqrt(M)) supported pairs.
Since L>=M/4-1 and 1-2S>1/25, this is strictly larger than
M/100-1/25-2 sqrt(M). With x=sqrt(M)>=1000, x^2/100-2x
is increasing and at least 8000. The count is positive for every
M>=1000000, with no assumed distribution of primes or prime pairs.

These h,k=h-1 are coprime and squarefree; hence mu(h),mu(k) are in
{-1,1}. For the basic mollifier coefficient
mu(h) P(log(M/h)/log M)/sqrt(h), with P(x)=x, neither factor is zero.
The same holds at k. This is a support statement, not a quantitative
lower bound uniform over all mollifier polynomials.

## Phase and scale

For any r>=2, m=kr+1,n=hr+1 give hm-kn=1. Since h<=M,
m<=Mr and n<=Mr+1, mn<T/8 for T=16(Mr)^2 exactly as in EXP-014.
For M>=1000000 and M/2<=h<=3M/4, we have

    M^2 r/5 <= kn < M^2 r.

The lower bound follows from (M/2-1)(M/2)>=M^2/5 for M>=10.
For the upper bound, (3M/4)(3Mr/4+1)<M^2 r when M r>=2.

The logarithm inequalities give H/(kn+1)<=H log(hm/kn)<=H/kn.
Since kn+1<=M^2 r+1<=2M^2 r, the phase lies between
H/(2M^2 r) and 5H/(M^2 r). For M=B^b,r=B^(a-b),H=B^d,
these are fixed positive constants times B^(d-a-b). The three
threshold regimes in the declaration follow for every sufficiently
large integer B and every supported pair, without a limiting h/M.

The derivative scale H/log T is still smaller. Nonzero Mobius weights
therefore do not restore uniform pointwise rapid oscillation. The
signed sum can nevertheless cancel. This theorem does not contradict
a mollified moment asymptotic or lower the simple-critical onset.
