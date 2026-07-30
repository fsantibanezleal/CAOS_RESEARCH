# EXP-125 prime-admissibility redirect

Recorded 2026-07-30 after attempt 001 and before the accepted rerun.

## Refuted gate

The original hypothesis named 1009 and 1013 as the two reconnaissance
primes. Attempt 001 exhausted all \(1008^2\) pairs with \(A\ne0\) at
\(p=1009\) and found no \(F_3\) point. Therefore literal prediction 1 at
those named primes is refuted.

This is explained exactly by
\[
F_3=(5B+4)^3+16X=(5B+4)^3+16A^3.
\]
For \(A\ne0\), an \(F_3\) point exists over a field only if
\(-1/16\) is a cube. At \(p=1009\),
\[
\left(-1/16\right)^{(1009-1)/3}=634\not\equiv1\pmod{1009}.
\]
Thus the absence of samples is an arithmetic obstruction in the chosen
field, not a rank loss and not evidence against the characteristic-zero
factor stratum.

## Authorized redirect

Retain 1013 and replace only the inadmissible prime 1009 by 1019. Both primes
are \(2\bmod3\), so the cube map is bijective on their multiplicative groups.
They therefore admit nonzero \(F_3\) lifts for every \(B\ne-4/5\).

The sample count, rank predictions, basis requirements, exact method, and
compute gates are unchanged. The accepted verdict must report the original
prime prediction as refuted and the redirected admissible-prime result
separately.
