
## Integrated rerun verdict (2026-08-19)

DECLARED SUCCESS. One pipeline, one artifact, zero residual failures:
854,317 boxes processed in 5,096 s; 412,975 certified rank >= 3 by plain
interval menu; 4,857 by mean-value forms; 9,317 discarded as the |f| < 1/4
band (EXP-022's region, covered there); 10 boxes inside the four pentagon
exclusion balls. Each ball (radius 2^-8, dyadic centers of the four
symmetric pentagon copies) carries BOTH certificates: a 2x2 minor
interval-nonzero over the whole ball (rank >= 2 everywhere, so R_1 meets
no ball) and a gradient pair (two 3x3 minors with a 2x2 interval
subdeterminant of their gradient matrix excluding zero over the whole
ball, so R_2 meet ball lies inside a smooth codimension-2 manifold).
Together with piece 9-prep (R_0 empty on the stratum):

    dim(R_2 meet core) <= 2,  R_1 meet core = EMPTY,  R_0 = EMPTY,

the FULL ladder on the core, with explicit radii everywhere (the implicit
function theorem step of lemma piece 8 is retired). Artifact:
E:/_Datos/caos-research/central-configurations/EXP-021/
integrated-certificates.jsonl, 417,842 lines, 51 MB, sha256
11ea7b324400ab3d927044585a17e39647dd2421f1de860f4d8dee6b32b726e8.
The certificate spread across phases 1-3 (the old artifact-hygiene gap,
including the 3,000-of-4,414 phase-3 sample) is superseded.
