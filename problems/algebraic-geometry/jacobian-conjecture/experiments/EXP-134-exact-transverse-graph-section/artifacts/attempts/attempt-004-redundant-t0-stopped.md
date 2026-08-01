# Attempt 004 - redundant `T=0` recomputation stopped

The rank/root worker passed every structural gate and began recomputing the
33-vertex determinant at `T=0`. It was stopped before its gate because
EXP-124 already persists that exact characteristic-zero determinant.

The accepted continuation derives the `T=0` core factor exactly by dividing
the persisted EXP-124 determinant ratio by the unchanged singleton factors,
verifies the product identity, and spends computation only on the seven new
values `T=1,...,7`. This is an exact reuse of an accepted theorem-bearing
artifact, not a sampled baseline.
