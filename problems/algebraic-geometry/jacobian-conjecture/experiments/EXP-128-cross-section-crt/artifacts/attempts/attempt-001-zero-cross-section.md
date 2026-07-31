# EXP-128 attempt 001 - a predicted cross-section is identically zero

Date: 2026-07-31.

The first run verified all source hashes, reconstructed the three curve
ledgers, found two exact projection overlaps, and completed the \(h_7\)
quotient computations on \(F_3\) and \(F_6\). It then found that the
graph-restricted \(h_{36}\) section has zero remainder modulo \(F_7\).

The initial implementation treated every cross-section as necessarily
nonzero and stopped at that falsified prediction before persisting a final
artifact. The zero remainder is mathematical evidence, not a software
failure: \(h_{36}\) vanishes identically on the complete \(F_7\) curve and
cannot cover any part of its retained divisor.

Correction: persist a zero quotient as an exact nonunit result whose gcd is
the full target ledger. Continue the other cross-unit tests and CRT checks;
do not redirect or infer failure of the multi-minor atlas.
