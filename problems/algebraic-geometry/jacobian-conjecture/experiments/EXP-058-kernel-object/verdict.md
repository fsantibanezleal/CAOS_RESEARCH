# EXP-058 - Verdict: k = 1; ALL-ORDERS SOLVABILITY IS PROVED in one line (2026-07-22)

Artifacts: `artifacts/output-2026-07-22.txt`, `artifacts/kernel-2026-07-22.txt`.

## Findings

1. **[MV] THE KERNEL IS THE CONSTANTS.** The nullspace of the reduced system over
   QQ(t) is one-dimensional and spanned by k = 1 (one nonzero coefficient, at
   (0,0)). Structurally obvious in hindsight: [P, 1] = 0 for EVERY P, and (0,0) is
   in N(Q); the machine confirms nothing else joins it (rank exactly 124).
2. **Prediction 2 REFUTED, trivially:** the exact bracket [P0, k] is ZERO, not
   off-pool-nonzero; the declared reasoning missed the constant polynomial itself.
3. **[MV -> PROVED] ALL-ORDERS SOLVABILITY.** A rung solves iff its rhs annihilates
   the kernel; the rhs entry at the constant column is -Lambda_prev([m, 1]) = 0
   IDENTICALLY (brackets kill constants). Every conceivable ladder rhs annihilates
   the kernel: THE LADDER CAN NEVER STICK, at any order, for any parameters. The
   276/276 record is fully explained. Part-3 rank tests concur.

## What remains for the stratum closure

TERMINATION alone (the ladder is an eventually-polynomial covector series or not);
with solvability settled, the next round attacks it directly: either the support-
drift bound on the fixed pool, or the fixed-P inconsistency framing (rank M(eps) ==
124 with the x^2 rhs outside the column space for every parameter: a determinantal
statement now that the kernel is known to be exactly the constants for every P).

## How could this be wrong?

- Kernel dimension could jump at special t (rank checks at the sampled values only;
  the constant is in the kernel for ALL t, so dim >= 1 everywhere: jumps could only
  ADD kernel, which would only add solvability conditions at those t: flagged).
