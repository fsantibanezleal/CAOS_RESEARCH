# Changed-pressure distinct-strip implication, pending the complete cover

This is a review of the logical implication and its complete-cover gate.
It does not assert that the unfinished local certificate has passed.

The exact window and 36 rational weights are unchanged from the pinned
packet. Each of eight index-span capacities equals two, including zero
weights. For m=562, r=8, p=1/1250 and delta=52231/5000000, summing the
m-r contained windows gives E+pW>=D=delta*(m-r). All pressure and gap
terms are nonnegative. Here tau=1203/500 and c=1703/500.

The attributed elementary block dichotomy suffices because D<=tau^2:
if every eigenvalue is at most 1+tau, clipped and raw energy coincide;
otherwise a single clipped contribution already exceeds tau^2, and the
remaining contributions and pressure are nonnegative. This avoids an
unnecessary appeal to the sharper EXP-017 envelope. It is classical
source machinery, not a new matrix theorem.

Average the consecutive m-point blocks over all m offsets. Each contained
r-gap window occurs in at most m-r partitions; each gap occurs in at most
r windows. Span capacities control the pair charge. The missing endpoint
blocks cost O_m(1). With a=D/m and beta=r*p*(m-r)/m, the defect is at least
a*l-beta*spread-O_m(1), where l=Nd-h-2k. The entire counting and smoothing
review is in EXP-019/analytic-transfer-review.md; its BGSTB integrated
pair-correlation theorem and correction are explicit analytic dependencies.
The fixed block dimensions precede T tending to infinity and subsequent
removal of the smooth cutoff. No gap-dependent approximation is used.

The mixed threshold bound and span<=N+o(N) then give

    (2-a)*Nd >= (1+H-beta)*N+(6c-7-c^2-a)*h
                          +(4c-2-c^2-2a)*k-o(N).

The exact threshold, clipping, high-multiplicity, off-line and denominator
residuals must all pass. The independent stdlib transfer_audit.py first
executes the independently reconstructed full-cover audit, then checks
packet capacities, the source-bound native window audit and every rational
residual. It refuses to issue a transfer receipt for an incomplete cover.
After those gates the fraction would be 2340938143167/2795532013000.
This counts distinct points across the whole critical strip, with all zeros
counted with multiplicity in the denominator. It is not a critical-line
simple-zero fraction, an effective-height theorem or a proof of RH.

The executed Python/FLINT/Arb interval code remains a stated trust base.
Accounting hashes detect corruption and bind execution; they are not a
formal proof against fabricated recomputed receipts. No external referee
or worldwide priority assessment has been completed.
