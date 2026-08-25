# The real record mechanism: two gates per doubling, and where it stalls

Round 11b, 2026-08-25, following the exhaustive real ladder.

## The ladder, now to tau = 6

    tau                1    2    3    4    5    6
    zmax over Z        1    2    3    3    4    5
    zRmax over R       1    2    3    4    6    8
    zpmax over F_p     1    2    4    8   16   32
    degree ceiling     1    2    4    8   16   32

Depth 6 was reached without a depth-6 census: the last-gate lemma applied to the
778,087-state depth-5 frontier enumerated all 134,494 new tau = 6 polynomials in
180 s. The run carried a known-answer gate on the same set, requiring the
INTEGER maximum to come out at 5 (the exhaustively established zmax(6)); it did,
and only then was the real number reported.

CORRECTION (2026-08-25, adversarial validation pass): this note and the paper
first reported 134,497 new polynomials, three more than EXP-003's recorded
134,494. The three are exactly (-1), (1) and x, the FREE INPUTS, which
last_gate_scan reports as new unless the known-set is seeded with them. EXP-003
had already hit and fixed this same artifact one depth down (11,380 against
11,377) and wrote it into its verdict; the seeded call reproduces 134,494
exactly. The three have degrees 0, 1, 0 and 0, 1, 0 integer roots, so no
maximum is affected: zRmax(6) = 8, zQmax(6) = 5 and zmax(6) = 5 all stand. Only
the population count was wrong.

## The mechanism

The tau = 6 real record is

    (1, 0, -7, 0, 14, 0, -7, 0, 1)  =  x^8 - 7x^6 + 14x^4 - 7x^2 + 1
                                    =  (x^4 - 3x^2 + 1)(x^4 - 4x^2 + 1)

and the left factor is precisely the tau = 4 record, g1 = (x^2-1)^2 - x^2. So the
step from 4 gates to 6 gates is

    g  ->  g * (g - x^2)

which costs TWO gates (x^2 is already in the state) and DOUBLED the real root
count, 4 to 8. Written out from scratch:

    1 a = x*x     2 b = a-1     3 c = b*b     4 g = c-a      (4 real roots)
    5 h = g-a     6 g = g*h                                  (8 real roots)

This matters because it beats the obvious construction. A Chebyshev tower costs
three gates per doubling (T_2 = 2x^2 - 1 is three gates, and composition repeats
it), reaching about 2^(tau/3). This step reaches 2^(tau/2) while it lasts, and it
matches the EXHAUSTIVE census at both tau = 4 and tau = 6, so in that range it is
not merely a good construction, it is the record.

## Where it stalls

Iterating the step, with distinct real roots against degree:

    gates    4     6     8    10    12
    degree   4     8    16    32    64
    real     4     8    16    28    48
                             ^^^^  ^^^^ no longer totally real

Three clean doublings, through 16 distinct real roots at 8 gates, and then the
polynomial stops being totally real: 28 of 32, then 48 of 64. The successive
ratios fall from 2 to 1.75 to 1.71. The family keeps growing exponentially but
at a rate below 2^(tau/2), and we do not claim its limit.

This is the same shape as the integer-side results: a natural doubling
construction runs for a few steps and then stalls, exactly as the monic stall
theorem describes for iterated towers over Z. The real side stalls later and
from a much higher base, which is consistent with the real analogue of the
conjecture being false while the integer one is not known to be.

## An observation worth keeping

The tau = 6 real record has ZERO integer roots, while the tau = 6 integer record
has five. At the same cost the two worlds are optimized by completely disjoint
polynomials. The real ladder is not the integer ladder with extra roots
attached; it is a different extremal problem that happens to share the
difference-of-squares mechanism at the bottom.

## Scope

zRmax is exhaustive through tau = 6 only. The lower bound zRmax(8) >= 16 comes
from the family above, not from a census; extending the exhaustive real ladder
to tau = 7 needs the 25.8M-state depth-6 frontier resident, which the additive
nine-gate scan currently rules out. No asymptotic rate is claimed for zRmax.
