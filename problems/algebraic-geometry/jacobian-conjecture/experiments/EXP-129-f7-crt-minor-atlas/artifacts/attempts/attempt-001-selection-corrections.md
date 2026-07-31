# EXP-129 attempt 001 - selection implementation and single-basis redirect

The first two invocations stopped before mathematical selection because the
new driver passed a `Poly` object where an expression was required and then
looked up the modular coefficient helper on the wrong imported module. Both
interface errors were corrected without changing the declared experiment.

The next invocation completed all exact point-class checks and found two
full-rank modular probes on each retained (F_7) block. It then refuted the
single-basis prediction: none of the six row bases selected at those probes
was nonzero on all six probes.

Per the pre-run redirect rule, the accepted driver now computes a deterministic
greedy row-basis atlas and requires that the atlas cover every probe. A modular
atlas remains reconnaissance only; characteristic-zero closure still requires
exact reconstruction and blockwise norm-ideal tests.
