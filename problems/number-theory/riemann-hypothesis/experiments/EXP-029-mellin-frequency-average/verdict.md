# EXP-029 status: inconclusive, finite and conditional controls pass

Hypothesis pushed as 06bfe46e before code and control computation.
Issue #374 tracks the experiment. The first exact run passes 432 dyadic
blocks, 524,400 triples and 180 exponent configurations in 2.421875 CPU
seconds. Fraction grouping agrees with independently reduced integer pairs;
the proper spacing and full collision costs hold on that grid. Omitting
the collision N factor fails on an actual ratio-one group.

The initial named spacing mutation removed both 16 and N; its N=1 witness
does not isolate the N cost. Its comparison alone is a failed sufficient
spacing test, rather than a direct logarithmic refutation. The separate
declared rational audit resolves this: for P=Q=1,N=32, actual ratios 1/64
and 1/63 have log-gap at most 1/63, strictly below the wrong delta 1/16,
while the proper delta 1/512 is retained. The first runner/receipt stay
unchanged and are not used as a standalone N-factor refutation.

Native Arb and independent stdlib rational outward intervals agree for
the frozen detector at theta=527/1000, nu=499/10000, eta=1/100000.
Charged exponents are -51/12500 and -6711/40000. Conditional parity density
exceeds 0.0005947542001; the zero-detector alternative is negative. Both
receipts explicitly keep analytic_moment_theorem_proved=false.

The full analytic assembly and its adversarial review remain required.
The proposed larger range and theta=0.527 consequence are not admitted;
the current established onset is 0.5339. No finite pass proves the moment.

How could this be wrong? The common Mellin multiplier may retain an
unaccounted coefficient dependence; a repeated-frequency, tail, gcd,
small-shift, residue, derivative or compact-conversion cost may invalidate
the estimate. Passing finite frequency examples cannot eliminate these
uniform analytic failure modes or establish worldwide novelty.

Published v0.02 and app 0.76.000 are immutable premises, not changed outputs.
No manuscript or publication follows from this initial status.
