# Scope check for a simple-critical counting assembly

The EXP-023 target is distinct points in the whole strip. This supplementary
check considers a different counting assembly and is conditional on the
same, still unfinished, local inequality. It does not convert the proposed
distinct proportion into a simple-critical proportion or assert a new zero
theorem. All threshold and rank arguments used here are classical.

Let S count simple zeros on the critical line and N count all zeros with
multiplicity. Retain only these S unit-weight real Gram atoms in P. The
remaining Hermitian operator Q has positive rank at most (N-S)/2: each
remaining on-line point has multiplicity at least two, and each off-line
pair has total multiplicity at least two and at most one positive direction.
The threshold inequality, followed by the unit-diagonal clipped Gram bound,
therefore gives

    (2-H)*N >= (2c-c^2/2)*N+(1-2c+c^2/2)*S+defect-o(N).

Suppose consecutive-block averaging supplies defect>=a*S-beta*N-o(N),
with u=(m-r)/m in [0,1], a<=delta*u and beta=r*p*u. The elementary block
dichotomy has a=delta*u when admitted; the sharp retained-energy envelope
cannot exceed the raw local charge delta*(m-r). These are hypotheses of
this particular assembly, rather than restrictions on every possible
simple-zero method. Whenever its denominator is positive, its numerical
lower-bound output is

    q_simple = (H-x-r*p*u)/(1-x-a),  x=(c-2)^2/2 >= 0.

For a nonnegative numerator, increasing a to delta*u can only increase
that output. Its replacement denominator stays positive: x<=H-r*p*u
implies 1-x-delta*u>=1-H+(r*p-delta)*u>0 for these constants.
A negative numerator already supplies no positive bound.
At a=delta*u the derivative with respect to x has the sign of
H-1+(delta-r*p)*u, which is negative for the pinned constants throughout
[0,1]. Hence x=0 gives an upper bound for the useful output. The derivative
of (H-r*p*u)/(1-delta*u) has sign H*delta-r*p, which is positive. Thus

    q_simple <= (H-r*p)/(1-delta)
              = 3330285207/4947769000.

Here H=3362285207/5000000000, r=8, p=1/1250 and
delta=52231/5000000. This is a relaxed uniform ceiling for the output of
the specified simple-atom threshold assembly. It does not upper-bound the
actual proportion of simple zeros, exclude other transfer arguments or
upgrade the incomplete local certificate. It explains why a pressure
optimized for the distinct-strip objective need not improve a
simple-critical objective. The original EXP-023 transfer and its complete
coverage requirement are unchanged.
