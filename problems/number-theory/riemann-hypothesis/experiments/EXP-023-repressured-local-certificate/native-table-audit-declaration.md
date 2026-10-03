# Independent native hypergeometric table audit

This is an additional input audit of the already declared EXP-023 certificate,
not a new pressure target, interval pruner or scientific search. Frozen runtime
files and live output will not be edited. A passed audit must enclose every
closed cell in both bound prefix tables; finite samples are insufficient.

Use the entire identities, with u=-z^2/4,

    sinc(z)=0F1(3/2;u),
    sinc'(z)=-(z/3)*0F1(5/2;u),
    sinc''(z)=-(1/3)*0F1(5/2;u)+(z^2/15)*0F1(7/2;u).

They follow by differentiating 0F1's power series and use FLINT/Arb's native
hypergeometric enclosure. This differs from the archived kernel's small-z
explicit derivative series and large-z divided sine/cosine formulas. Assemble
the Fourier window and squared-kernel derivatives from the exact packet.
For each rational closed cell, prove the stored binary64 dyadic values are
no greater than the new interval lower bounds. When a new enclosure is too
wide, bisect the cell, at most eight levels, preserving its closed cover.
Failure to prove a comparison is inconclusive for this extra audit and is
not by itself evidence that the existing table or local inequality is false.

First check normalization identities and benchmark at most 512 consecutive
cells with a thirty-second cooperative budget, on one additional CPU.
Proceed to the 52,240-cell audit only if the pilot's complete-cell throughput
projects at most ten minutes. The full audit has a ten-minute cooperative
budget, prints progress and retains its exact audited range. A partial range
cannot issue an all-cells success flag. Full success remains a Python/FLINT/Arb
computation; it is not a separate arithmetic library or formal proof checker.

This audit supports the distinct-strip certificate and its stated execution
trust base. It is not a manuscript or research stopping condition by itself.
