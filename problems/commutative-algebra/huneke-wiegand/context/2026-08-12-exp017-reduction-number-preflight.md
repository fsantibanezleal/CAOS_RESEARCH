# EXP-017 preflight - conductor reduction sequence

Date: 2026-08-12.

## Why this path is next

EXP-016 proves that the conductor `T_p` is not stable and computes the first Sally quotient
`length(T_p^2/t^(4s)T_p)=14p`. The next structural question is not another nearby-family search:
it is whether the full reduction sequence of this already explicit ideal terminates uniformly.
This converts a negative property into an exact Rees/Hilbert invariant.

Reduction ideals and reduction numbers are standard for an `m`-primary ideal `I`: a reduction
`Q` satisfies `I^(r+1)=Q I^r`, and the least such `r` is its reduction number. Mafi--Naderi,
`https://arxiv.org/abs/1707.09843`, provides a current primary-source orientation to this
framework. No theorem from that paper supplies the formulas predicted below; they must be proved
from the EXP-013/016 value blocks.

## Scouting boundary

A disposable exact-value calculation at parameters `p=4,5,17,73` suggested successive quotient
lengths `14p,2p,1,0` after `T_p/Q_p`. This calculation is discovery scouting only: it is neither a
committed artifact nor evidence for the experiment. EXP-017 is declared before its formal
implementation, campaign, audit, or proof.

## Hypothesis selected

Put `Q_p=t^(4s)R_p`, where `4s=24p` is the least value of `T_p`. Predict that `Q_p` is a minimal
reduction, that its reduction number is exactly four, and that the complete quotient-length
profile is affine in `p`. The exact set differences, not just cardinalities, are required.

The competing paths are lower priority:

- a nearby-Kunz-face SAT sweep has no comparably sharp finite target;
- formalization is valuable but does not presently expose new mathematics;
- testing more positive Huneke--Wiegand hypotheses is broader and less directly connected to the
  newly proved conductor formula.

