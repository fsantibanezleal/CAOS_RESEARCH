# Stronger local overlap certificates and global distinct-zero counts

Let N(T) count all nontrivial zeros with multiplicity and Nd(T) count distinct
points in the whole critical strip. The completed local certificate EXP-020
gives Nd/N asymptotic lower bound 3997934614153/4775507750000, approximately
0.8371747724947154. The source-attributed vector-pressure consequence EXP-025
gives 30945470743359/36955122080000, approximately 0.8373797460706156.

The manuscript PDF is published as
[v0.01](https://doi.org/10.5281/zenodo.23128663). The full certificate ZIP
and scoped mathematical source are in the
[separate evidence record](https://doi.org/10.5281/zenodo.23135359).
[The concept DOI](https://doi.org/10.5281/zenodo.23128662)
resolves to later versions. The three earlier papers remain immutable.

## General implication and the reusable pressure rule

For an even bounded nonnegative probability profile f on [-1/2,1/2], write
K(x)=integral f(t)exp(2*pi*i*x*t)dt and w(x)=K(x)^2 on real x.
Suppose nonnegative weights have every index-span mass at most two, and

    sum_(i<j) a_ij*w(g_i+...+g_(j-1)) + sum_i b_i*g_i >= delta

for every nonnegative r-gap vector. Put B=sum_i b_i. With fixed m>r,
D=delta*(m-r), a=D/m and beta=B*(m-r)/m, require

    D<=tau^2, c>=max(1+tau,2+tau/2), a<2,
    6c-7-c^2-a>=0, 4c-2-c^2-2a>=0.

Then the corrected integrated BGSTB pair-correlation input and Knausgard's
mixed-Gram argument give

    liminf Nd(T)/N(T) >= (1+H_f-beta)/(2-a),
    H_f=2-integral f^2-double integral |s-t|f(s)f(t)dsdt.

The block argument has an elementary dichotomy: without a large eigenvalue
clipped defect equals raw energy; a large one alone pays at least tau^2.
Across all offsets each gap is charged at most (m-r)*B. It is incorrect to
use r*min(b_i) for an unequal vector. The complete-block count is exactly
max(l-m+1,0), so endpoint loss is bounded by D. The general proof supplements
288 exact list/block examples and 183 pair-count controls, rather than being
inferred from them.

## Completed independent local input

EXP-020 retains the upstream nine-point window and weights, pressure 1/2500,
and proves the stronger delta=3051/500000 on the full eight-dimensional
nonnegative orthant. All 96 shards complete with 107,752,902 nodes. The
independent standard-library checker verifies full domain/source/table/tree
bindings, all 12 actual-output corruption controls are rejected, and native
hypergeometric/Taylor formulas enclose both input tables over every one of
61,029 closed cells. The 233-member runtime archive passes exact-byte and
extracted-auditor reproduction checks.

Its transfer uses m=958, tau=2409/1000, c=3409/1000 and
H>=3362285207/5000000000. It implies EXP-018's older same-pressure premise;
it does not complete EXP-019's suspended source-identical traversal.

## Stronger attributed local input

Samuel Lavery's newly published attempt-013 proves a seven-point theorem
using typh's thirteen-term cosine window and Ainta's weighted refinement.
The six pressures have numerators (41468,70344,87381,87381,70344,41468)
over 10^8. EXP-025 binds the exact certified functional, independently encloses
H>=33608554629/50000000000, and uses delta=39369/5000000, m=742,
tau=12043/5000, c=17043/5000. All exact residuals pass.

The complete Apache-2.0 source, metadata, external Lean/nanoda log and
attestation are preserved. Those formal checks were not locally rebuilt.
The scalar identity is independently proved with rational Taylor/Machin
enclosures and separately checked with native Arb integrals.

## Evidence and scientific limits

The interval computation trusts the frozen Python/FLINT/Arb verifier and
directed enclosures. Native table checks share FLINT/Arb; archive and cover
checks do not rerun every interval operation. The source-attributed result
also depends on Lavery's external local theorem. Neither theorem is an
end-to-end local Lean proof. The corrected BGSTB analytic input is applied to
fixed R and R'' separately; fixed block parameters precede T->infinity,
followed by removal of the smooth cutoff.

The located prior distinct-strip source, Knausgard arXiv:2609.33043v1, gives
0.83699288145242... . These improvements have limited primary-source overlap
review, with worldwide priority and peer acceptance unconfirmed. They give
no effective height, simple-critical-line proportion, shorter onset or RH
proof. EXP-023's larger candidate remains incomplete and is not used.
