# General r-gap mixed-multiplicity transfer

Assume the pinned window has source energy coefficient C<=2-H0 and,
for every ordered y_0,...,y_r, nonnegative weights w_ij satisfy
sum_i w_(i,i+d)<=2 at each d=1,...,r and

    p*(y_r-y_0)+sum w_ij*K(y_j-y_i)^2>=delta.

This universal local inequality is an explicit premise, not established
by a finite packet-capacity calculation or the imported replay summary.

For m>r consecutive points, sum over all m-r contained windows. Each
fixed pair at index distance d receives a subset of the nonnegative
weights at span d, hence total weight at most 2. Thus raw Gram energy
E=2*sum_{i<j}K(y_j-y_i)^2 and total window spread W obey
E+pW>=D=delta*(m-r). EXP-017 gives clipped_energy+pW>=F_m(D).

Pinch into consecutive m-point blocks and average over m partition
offsets. The number of full blocks across offsets is at least l-2m,
where l counts distinct on-line points of multiplicity one or two.
Each r+1-point window survives in at most m-r partitions; each gap
is included in at most r windows. Nonnegativity of p and the gaps
therefore yields the defect lower bound

    defect>=a*l-beta*spread-O_m(1)-smoothing errors,
    a<=F_m(D)/m, beta=r*p*(m-r)/m.

All dimensions are fixed before T tends to infinity. Source smoothing
and pinching estimates continue to apply with unchanged hypotheses.
The complete source argument for the analytic energy and smoothing is
attributed to Knausgard arXiv:2609.33043v1.

The mixed threshold inequality gives
E_total>=3N-2Nd+defect+rh*h+rk*k, where
rh=6c-7-c^2, rk=4c-2-c^2, and l=Nd-h-2k.
The spread is at most N+o(N). Substitution and rearrangement yield

    (2-a)*Nd >= (1+H0-beta)*N+(rh-a)*h+(rk-2a)*k-o(N).

With c>=max(1+tau,2+tau/2), rh>=a, rk>=2a and 2-a>0,
liminf Nd/N >= (1+H0-beta)/(2-a). This counts distinct zeros in
the whole strip. It neither counts simple-critical zeros nor improves
the short-window positivity onset.

At the fixed nine-point candidate m=958,tau=2409/1000,c=3409/1000,
F_m(D)=D, so the final certificate uses rational arithmetic only. The
conditional consequence exceeds 837/1000. Exact weights, capacities,
thresholds and the full fraction are independently checked by audit.py.
The source's pending flag and absent candidate-hash binding are retained.
No universal local inequality is inferred from those finite checks.
