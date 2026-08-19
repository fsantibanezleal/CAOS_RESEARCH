# EXP-022 part (a) verdict: the band covering

2026-08-19. Region A_band = {u, p in [1/4,3], v, q in [-3,3], |f| <= 1/4,
max(|u-p|, |f|) >= 1/16}.

## Outcome against the declared criterion

The run's zero-failure criterion FAILED: 1,583,629 boxes processed in
5,548 s, 640,536 certified rank >= 3 by plain intervals, 3,601 by
mean-value forms, 8,154 discarded to A_core, 139,480 discarded to A_tube,
and 44 boxes failed at depth cap 44. Recorded as declared.

## The declared fallback closes the ladder

Per the hypothesis ("any stubborn cluster is investigated... and gets ball
certificates"), band-postprocess.py ran the trap certificate on each
failed box: ALL 44 TRAPPED (rank-2 witness: a 2x2 minor interval-nonzero
over the box, so R_1 meets none of them; gradient pair: two 3x3 minors
with interval-independent gradients over the box, so R_2 meet box lies in
a smooth 2-manifold). Together with the certified remainder:

    dim(R_2 meet A_band) <= 2,   R_1 meet A_band = EMPTY.

## The cluster is a near-miss, not a degeneracy (cross-degeneracy3.py)

The 44 boxes sit at v = q (equal heights, ON the excluded f = 0 slice to
box precision) around (u, p) ~ (1.4507, 0.6306) and the pair-swap image:
the cross configurations (bodies 1, 2 at (0, +-1), both mirror pairs on
the horizontal axis). Exact-precision analysis at u = 1.4507: three
independent 3x3 minors have DISTINCT roots in p (0.6307533..., 0.6305156...,
0.63; separations 2.4e-4 and 7.5e-4 at 25 digits); the joint zero of two
minors lands at (p, t) = (0.63063..., -0.000235...) where a third minor is
1.85e-5, NONZERO; the singular values there are (2.279, 1.477, 1.66e-3,
8.2e-5). The matrix approaches rank 2 without attaining it: a conditioning
near-miss, unlike the centered pentagon (which is exact rank 2). No new
degeneracy; the near-miss sits off-stratum (f = 0) in any case. Deeper
bisection would eventually certify rank >= 3 here, but the trap closure is
equally strong for the chain and the declared budget is honored.

## Artifacts

- E:/_Datos/caos-research/central-configurations/EXP-022/
  band-certificates.jsonl (644,181 certificate lines + 44 FAILED lines).
- artifacts/band-summary.json (the run as declared: ok = false, 44 failed).
- artifacts/band-failed-postprocess.json (44/44 trapped).
- cross-degeneracy3.py output quoted above (mpmath, 50 dps).
