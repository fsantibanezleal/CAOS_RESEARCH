# EXP-022 part (b) verdict: the collision-tube blow-up covering

2026-08-19. Both angle charts DECLARED SUCCESS, zero residual failures:
chart R 68,567 boxes (28,304 plain + 1,436 mean-value certificates, 4,544
trapped) in 4,556 s; chart L 68,357 boxes (28,093 + 1,536, 4,550 trapped)
in 5,207 s. The trapped boxes line the predicted rank-2 face degeneracy
curve w^2 + v^2 = 1 (the coincident double-pair on the circle through the
axis bodies, found during the blow-up derivation and machine-verified);
each carries the rank-2 witness (R_1 empty there) plus the gradient pair
(R_2 inside a smooth 2-manifold). With rows rescaled by rho^2 exactly as
verified in verify-tube-blowup.py, certificates on boxes touching rho = 0
certify the punctured tube, so

  dim(R_2 meet A_tube) <= 2,  R_1 meet A_tube = EMPTY (both charts).

The two charts' counts differ only mirror-symmetrically (4,544 vs 4,550
traps), the expected signature of the swap identity (piece 9d).
Artifacts: tube-R/L-certificates.jsonl in the heavy store, hashes in git.
