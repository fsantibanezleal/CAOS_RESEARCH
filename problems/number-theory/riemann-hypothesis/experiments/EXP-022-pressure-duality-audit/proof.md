# Uniform pressure-family obstruction from valid gap witnesses

Keep the exact EXP-018 packet window and all its position-dependent
nonnegative pair weights fixed. Let S(g)=sum g_i and E(g) be the weighted
sum of squared normalized overlaps at the actual nine ordered points.
Every admissible universal certificate satisfies

    delta(p) <= E(g)+p*S(g) for every g_i>=0.

Thus delta_max is the infimum of affine functions of p and is concave.
Concavity here is classical convex duality, not a novel-method claim.
No search minimum is a lower bound for delta_max.

Fix q0=419/500. Every mixed-Gram transfer under study has

    q = (1+H0-8*p*t)/(2-delta*t), t=(m-8)/m in (0,1),

with positive denominator and H0 no greater than the actual window H.
The independent window audit encloses H below
H_upper=672457041415/10^12. Therefore q>=q0 would require

    t*(q0*delta-8*p) >= C=2*q0-1-H_upper > 0.

Since t<1 this forces q0*delta-8*p>C, and hence, for EVERY chosen valid
gap witness,

    q0*E(g)+p*(q0*S(g)-8)>C.

The audit uses certified upper energy enclosures E_i^+, so the relaxed
necessary inequalities replace E by E_i^+. This weakens the obstruction
and is the safe enclosure direction. Exact rational intersections then
give the maximum over p>=0 of the concave piecewise-affine envelope
min_i[q0*E_i^++p*(q0*S_i-8)]. A negative-slope witness controls infinity.

The primary all-vertex computation is independently checked by a much
smaller proof: one rising line and one falling line have equal values at
their nonnegative intersection p*. For p<=p*, the rising line is no
greater than its value there; for p>=p*, the falling line is no greater.
Their common intersection value therefore bounds the envelope for every
p>=0. Degenerate zero slopes and a decreasing active line at p=0 are
handled separately by their intercept bounds.

In the recorded exact run, witnesses 17 and 16 provide this pair bound.
The full rational intersection and energies are in pressure-duality.json;
its peak is approximately 0.00239144, below the required C approximately
0.00354296. An independent auditor must recompute the selected energy
enclosures before the barrier is closed. The finite exploration at nine
pressures is not part of the universal pressure argument.

The obstruction applies to this fixed packet window, weight schedule and
counting assembly. It leaves other weights, windows, local inequalities,
signed analytic estimates and RH entirely open. It does not assert a
sharp true ceiling, since it drops finite-block and spectral constraints
and uses only a finite upper-witness envelope.

The same experiment suggests a proposed local inequality at p=1/1250
and delta=52231/5000000, whose exact admissible block m=562, tau=1203/500
and c=1703/500 would imply 2340938143167/2795532013000 = 0.8373855610599...
under a complete new local certificate and the attributed analytic inputs.
No such universal certificate has been completed by EXP-022.
