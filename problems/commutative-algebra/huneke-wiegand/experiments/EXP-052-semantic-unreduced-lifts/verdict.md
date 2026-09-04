# EXP-052 verdict

Status: **CONFIRMED FINITELY** with an untouched semantic holdout.

Training on `p=8,9,10` yields explicit coefficient-labelled formulas for the exact divided
boundaries of the two-column EXP-051 witnesses. The `58->59` formula has six alternating edge
families and support `6p-30`; the `58->62` formula has four alternating triangular/interval
families and support `binom(p,2)-5`. Every coefficient is `+/-1` or `+/-2`.

The formulas were committed before semantic access to `p=11`. They then reproduced all 36 and 50
holdout rows exactly. Both cycles satisfy `Rz=2b`, and both parity classes are nonzero. A separate
full reconstruction passes 31 of 31 checks.

This is a relevant advance but not the all-parameter solution. The missing step is a labelled
source-domain formula proving `R_p y_p=2b_p` for arbitrary `p`; one class also does not establish
the completion's rank-two lower bound or its upper bound. EXP-049's bounded dual pair and a
relative-Morse/free-complement theorem remain separate required components.

No manuscript or Zenodo update is triggered.
