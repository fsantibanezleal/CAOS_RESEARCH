# The growth rhythm of z_max, and what it predicts at tau = 9

Note dated 2026-08-23, written while the two nine-gate scans run (their
outcome is NOT known here). Pre-registration of a reading that CONTRADICTS
our own committed predictions, so that the record shows both.

## The measured sequence

    tau :  1  2  3  4  5  6  7  8
    zmax:  1  2  3  3  4  5  5  6

Increments: +1, +1, 0, +1, +1, 0, +1. The rhythm is (+1, +1, 0) repeating,
and it fits a clean closed form on the residues mod 3:

    tau = 3k+1 : zmax = 2k+1      (tau = 1, 4, 7 -> 1, 3, 5)
    tau = 3k+2 : zmax = 2k+2      (tau = 2, 5, 8 -> 2, 4, 6)
    tau = 3k   : zmax = 2k+1      (tau = 3, 6    -> 3, 5)

i.e. zmax grows by 2 roots per 3 gates, with the plateau falling on
tau = 3k+1. Mechanically this is exactly the q-ladder accounting: each
new factor q - m(m+1) costs 3 gates and buys 2 roots (build the constant,
subtract, multiply), while the odd values come from multiplying by x,
which buys the root 0 for one gate whenever the current record does not
already contain it.

## The prediction it makes

The closed form gives zmax(9) = 7 (tau = 3k with k = 3), i.e. a 9-gate
SEVEN-rooter should exist. This is the OPPOSITE of the emptiness we
committed to in EXP-012 and EXP-013, and it is recorded here before those
scans report.

Two-sided reading, fixed in advance:
- If a scan finds a witness, the rhythm continues, zmax(9) = 7, and the
  seven-root threshold is 9.
- If both scans come back empty, the rhythm BREAKS at 9: it would be the
  first place where the 2-roots-per-3-gates accounting fails, giving a
  third plateau (zmax(9) = 6) and a threshold of 10. That is a result in
  its own right: it would say the q-ladder step, which has been optimal
  at every measured point, stops being purchasable at nine gates, and the
  reason would be exactly the constant-building friction the plateaus
  already expose (the next ladder constant is 12, which needs two gates
  to build, not one).

## Why the second outcome is plausible despite the rhythm

The ladder's next step needs q - 12 alongside q, q - 2, q - 6. The
constants 2 and 4 suffice for the first three factors (6 = 2 + 4 comes
free as a chained subtraction), but 12 requires a further build. Counting
gates for the 8-root product gives 12 gates, not 11, so the rhythm's
arithmetic already shows strain past tau = 8; whether the strain lands at
9 or later is exactly what the scans decide.
