# Nine-point conditional distinct-strip transfer

For an r-gap universal local inequality with nonnegative pair weights and
each span capacity at most 2, the mixed-Gram argument has
D=delta*(m-r), a<=F_m(D)/m and beta=r*p*(m-r)/m. The source threshold
and multiplicity residuals yield q=(1+H0-beta)/(2-a). This extension
is derived in [EXP-018](../experiments/EXP-018-nine-point-distinct-transfer/proof.md).

The pinned nine-point packet uses delta=15211/2500000 and p=1/2500.
At m=958,tau=2409/1000,c=3409/1000 all exact constraints pass and
q=3997934614153/4775549550000=0.83716744477146... . This is a conditional
distinct-strip result, pending the universal local certificate obligation.
The upstream [nine-point note](https://github.com/trmdy/zeta-simple-zeros-673137/blob/1610b97b7895ff34982260f8dcaf04a0f7b82cf7/docs/nine-point.md)
reports verification, but its candidate JSON retains a pending flag and
the log does not bind its target/weights by hash. The [verdict](../experiments/EXP-018-nine-point-distinct-transfer/verdict.md)
retains this discrepancy. Finite exact capacity tests do not close it.
Issue #356 tracks packet-bound independent replay and manuscript review.
No independent unconditional bound, new onset or RH proof is claimed.
