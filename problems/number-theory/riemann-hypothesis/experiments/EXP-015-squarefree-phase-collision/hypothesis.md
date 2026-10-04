# EXP-015: phase collisions with nonzero Mobius weights

Declared 2026-10-03, before the runner and outputs. CPU, exact integers.

## Question and frozen predictions

EXP-014 controls a generic twisted lemma, but its power twists can have
zero Mobius coefficients. Can the same threshold obstruction be proved
for twists actually present in a standard Mobius mollifier?

A. For every integer M>=1000000 there exists h in
ceil(M/2)<=h<=floor(3M/4) with both h and k=h-1 squarefree.
Prove this uniformly by excluding square divisors. Use the rational bound
S=1/4+1/9+1/25+1/49+1/121+1/22 < 12/25
for the sum over primes of 1/p^2. Primes after 7 are odd and at least 11;
their tail is bounded by the first term plus the step-two integral.
The union bound loses at most 2 floor(sqrt(M)) endpoint terms.

B. Put T=16(Mr)^2, m=kr+1, n=hr+1 for any integer r>=2.
Then hm-kn=1 and mn<T/8. Both Mobius coefficients are nonzero.
For the basic polynomial P(x)=x, the two mollifier coefficients are
nonzero since 1<h,k<M. No nonzero total off-diagonal sum is asserted.

C. Let M=B^b, r=B^(a-b), H=B^d, a>b>=1 and a<d<2a.
The phase H log(hm/kn) is comparable, with uniform positive constants,
to B^(d-a-b), for any such squarefree pair h,k. Thus the same
threshold nu=theta-1/2 survives on the supported twists: phase tends
to zero above it, stays bounded away from zero and infinity at it,
and tends to infinity below it. This is an exponent statement, not a
specific limiting constant because h/M can vary.

## Controls, budget and disposition

Find the first admissible pair at M=1000000 using an exact squarefree
sieve; freeze r=1000000 and H=10^16,10^18,10^20. Audit independently
by trial division, integer expansion, rational logarithm inequalities
and the uniform count proof. Reject squareful twists, diagonal changes,
zero coefficient assertions, and altered tail bounds. Budget 30 seconds
per entry point; no GPU or stochastic computation.

PASS strengthens only the obstruction to uniform pointwise integration
by parts. It does not disprove the signed moment formula, eliminate
cancellation, lower the onset, or prove RH. FAIL is refuted/inconclusive
as appropriate. Research-record, no standalone manuscript trigger.
The proof uses elementary divisibility and EXP-014's log inequalities;
no imported analytic theorem supplies the new support assertion.
