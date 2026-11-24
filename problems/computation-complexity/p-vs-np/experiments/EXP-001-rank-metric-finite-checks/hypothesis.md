# EXP-001: finite facts on the rank metric of Mat_mu(F_2) used by the note PNP-001

Date: 2026-11-24. CPU only, exact integer and rational arithmetic, no randomness.

Honest order of events. The script was run on 2026-11-24 before this file was written, so this is not a frozen
preregistration. What had been computed by hand before the run, in the coordinating session's working: for mu = 2,
the ratio 3/2 at the characters of rank one and 1/2 at rank two; the Fourier sums -3 and +1; four rank-one matrices
transversal to E11 and six rank-one summands of the identity, each set spanning; six maximal cliques of size four
through 0; eighteen transversal pairs. The run confirmed each of them. The values for mu = 3 and 4, and the closed
form 2 - 2^(1-mu), were first seen in the run.

## Question

Do the finite facts that the note uses hold, for mu = 2, 3, 4?

- H1. For characters B of Mat_mu(F_2), with p_r(B) the fraction of matrices W of rank r with <B, W> = 1, the largest
  value of p_mu(B)/p_1(B) over B != 0 is attained at rank one and equals 2 - 2^(1-mu).
- H2. The function rank is not of negative type: sum over W of rank(W) chi_B(W) is positive for some B.
- H3. The rank-one matrices transversal to a given rank-one matrix span Mat_mu(F_2); the rank-one summands of a
  full-rank matrix span; the invertible matrices span.
- H4. For mu = 2 the maximal cliques of the rank-distance-one graph through 0 are six cliques of four vertices.
- H5. The graph of transversal pairs on the rank-one matrices is connected and contains a triangle.

One representative B per rank is enough for H1 and H2, because the counts are invariant under multiplication by
invertible matrices on both sides.

## Kill criteria

Any of H1 to H5 false for mu = 2 withdraws the step of Proposition 5.2 that uses it. H1 false for mu = 3 or 4
withdraws the closed form of Proposition 5.4.
