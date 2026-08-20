# EXP-022 part (c) verdict: the pair-collapse covering A_ulow

2026-08-20. DECLARED SUCCESS, zero residual failures: 880,947 boxes in
27,151 s (three coverings shared the machine); 377,798 plain + 29,483
mean-value rank >= 3 certificates; 26,090 trap certificates; 7,103
discarded (corner tubes and the A_tube sliver). The mA column rescale
(4u^2) held up: the u = 0 collapse face certified rank >= 3 cleanly,
matching the face-rank-4 closed-form analysis in the dossier.

The trapped set is NOT a degeneracy: it is the near-collision
CONDITIONING collar. The 26,090 trapped boxes hug v = +-1 at
u in [0.033, 0.25] (pair A within distance ~0.25 of an axis body, just
outside the discarded corner tubes), where entries scale like
d1A^-3 ~ 500-30,000 and interval dependency defeats 3 x 3 certificates at
that box size. Probe at a trapped midpoint: singular values
(157.96, 1.76, 0.60, 0.0004): sigma_3 is ORDER ONE (rank comfortably 3);
random descent does not shrink sigma_3 (no rank-2 structure nearby;
contrast the pentagon, exact rank 2, and the cross, sigma_3 ~ 1.7e-3).
The trap certificates still close the ladder there (R_1 empty, R_2 inside
2-manifolds), which is all the chain needs. Optional future hygiene: an
enlarged corner-tube chart (blow-up covering d1A <= 1/4) would convert
these traps into plain rank-3 certificates; NOT needed for the theorem.

By the swap identity (piece 9d), A_plow is the swap image of A_ulow:
covered with no run. Artifact: ulow-certificates.jsonl (sha256 in git).
