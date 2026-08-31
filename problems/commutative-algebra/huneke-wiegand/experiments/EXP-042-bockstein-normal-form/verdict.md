# EXP-042 verdict

Status: **CONFIRMED** finitely for `p=8,...,11`. P1, P2, and P3 pass.

The exact isolated signed matrices reproduce every frozen hash, size, nonzero count, and rank.
Their first-Bockstein ranks are exactly `3,4,5,7`, under forward/reverse order and an independent
opposite-pivot audit. Therefore the four matrices have exactly `3,4,5,7` nonzero Smith factors
whose 2-adic valuation is one. The entire observed odd-minus-two rank gap is detected by genuine
factor-two arithmetic inside the persistent twelve-atom sector.

The audit also rejects an overstrong localization: high-pivot representatives lie in the `D:B`
row atom, while low-pivot representatives lie in `K:C0`. The rank is intrinsic; either chosen
representative is reduction dependent. A signed bridge between those families is a research clue,
not yet a proved subcomplex.

The next strongest gate is a rigorous rational-rank upper certificate using modular ranks and a
Hadamard bound. If it passes, it will rule out additional 4-divisible factors and completely
identify the isolated block's 2-primary torsion at the tested parameters. EXP-042 does not prove a
recurrence, all-parameter theorem, or full lower strand, and it does not trigger a manuscript or
Zenodo update.
