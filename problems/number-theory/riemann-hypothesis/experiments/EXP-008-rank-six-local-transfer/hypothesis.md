# EXP-008: rank-six local Selberg transfer

Declared: 2026-09-20. Device: CPU. Declaration baseline:
`0c1a66039c219ea482a23deca918db8fac9507d8`.

Status at declaration: the primary-source theorem and its local interface have
been inspected, and exploratory non-authoritative decimal calculations selected
the frozen brackets below. No EXP-008 runner or authoritative exact result has
been created. This declaration is committed before implementation and canonical
computation.

## Question

Does Pearce-Crump's source-certified six-square Selberg detector localize by the
same coefficient-uniform short-rectangle argument as EXP-005, and does its
smaller diagonal constant produce a certified earlier short-interval positivity
onset after EXP-006's sharp Hilbert-parity transfer?

## Imported source claim

Pearce-Crump states that a fixed ten-direction, six-square profile has

$$
C_6\in 0.6566338678379319741683641732\ \pm\ 5.63\times10^{-18}.
$$

The same paper proves the vector-profile transfer for every fixed finite rank.
The public arXiv source prints the certified enclosure but not the rank-six
coefficient matrix. EXP-008 therefore treats the existence and enclosure of the
profile as an attributed analytic input. It independently certifies the local
length bookkeeping and every scalar consequence, but it cannot independently
rebuild the source's rank-six contraction.

## Prediction A: rank-independent localization

For every fixed finite-rank admissible vector profile with diagonal constant
`C`, the EXP-005 proof should give, for every fixed `1/2 < theta < 1`,

$$
\liminf_{T\to\infty}\frac{A(T,T^\theta)}{N(T,T^\theta)}
\ge \frac{\theta-1/2}{4eC}.
\tag{A}
$$

Here `A` counts distinct odd-multiplicity critical-line support and `N` counts
all zero copies. Specializing (A) to the source-certified `C_6` defines

$$
k_6(\theta)=\frac{\theta-1/2}{4eC_6}.
$$

No coefficient, mollifier length, or profile is allowed to vary with `T`.

## Prediction B: earlier Hilbert-parity onset

With Wang's pair term

$$
c(\theta)=2-\frac\theta2-\frac1{\sqrt2}\cot(\theta/\sqrt2),
$$

put

$$
h_6(\theta)=\frac{3+k_6(\theta)-
\sqrt{(1-k_6(\theta))(9-k_6(\theta)-8c(\theta))}}4.
\tag{B}
$$

The EXP-006 finite product is independent of the detector rank, so the predicted
lower bound is

$$
\liminf_{T\to\infty}\frac{N_0^s(T,T^\theta)}{N(T,T^\theta)}
\ge\max\left\{0,c(\theta),\frac{c(\theta)+2k_6(\theta)}3,h_6(\theta)\right\}.
\tag{C}
$$

The unique zero `theta_6` of `h_6` is predicted to satisfy

$$
0.545883<\theta_6<0.545884,
$$

which is strictly below the EXP-006 rank-three onset. At `theta=0.545884`,
`h_6` is predicted to exceed `2.5e-7` while `h_3` is negative. At
`theta=0.5459`, `h_6` is predicted to exceed `1.776e-5` and improve `h_3` by
more than `9.26e-7`.

## Prediction C: radius-optimized spectral companion

EXP-007 chose `R=4/h` only for a transparent positivity proof. For any fixed
`rho>2`, the same proof permits `R=rho/h`. Freeze `rho=11/5`, which was selected
by a non-authoritative one-dimensional scan motivated by the large-radius
asymptotic optimum. With `h=h_6`, analytic energy `d=(b/B)^2`, frame size five,

$$
\alpha=\frac{2d}{5},\qquad
\beta=\frac{4d}{5R},\qquad
\alpha h-\beta=\frac{2dh}{55}>0.
$$

The resulting coupled root `H_6` is predicted to satisfy `H_6>h_6` at every
point of the positive curve. At `theta=0.5459`, the exact correlated gain floor
is predicted to exceed `9e-69`, at least fifty times the EXP-007 `R=4/h_3`
gain floor. This spectral correction is secondary; Prediction B is the new
onset result.

## Required exact checks

1. Prove the EXP-005 short-rectangle and local mean-square estimates are
   componentwise and uniform for every fixed finite rank, so the source's fixed
   six-square profile satisfies (A).
2. Encode the printed `C_6` interval as outward exact decimals and verify it is
   strictly below the certified `C_3` interval.
3. Recompute `c`, `k_3`, `k_6`, `h_3`, and `h_6` with directed rational Taylor
   bounds; prove the frozen onset signs and pointwise lower bounds.
4. Prove uniqueness of the new onset from the same positive derivative used in
   EXP-006.
5. Recompute the `rho=11/5` analytic spectral correction, including the exact
   reserve and gain floor, with directed rational intervals.
6. Independently replay all shared transcendental quantities at 100 decimal
   digits with `mpmath.iv` and require interval overlap.
7. Bind source, declaration, runner, imported EXP-005/006/007 artifacts, and
   canonical output hashes.

## Budget and stop rules

The run is CPU-only and capped at 120 seconds. No GPU workload is justified by
one-dimensional interval arithmetic. A failed source hash, unresolved directed
interval, nonpositive endpoint sign, missed frozen pointwise target, or failed
independent overlap gives an inconclusive or refuted verdict. It does not
permit changing `C_6`, `rho`, brackets, or target exponents without a new
committed declaration.

## Novelty and claim boundary

The six-square profile and its constant are Pearce-Crump's result. The proposed
contribution is its rank-independent localization to every fixed short-interval
exponent, its combination with the EXP-006 Hilbert-parity product, the resulting
earlier onset and exact certificate, and the radius optimization of EXP-007's
secondary spectral correction. The result remains asymptotic, relies on recent
preprints, supplies no effective starting height, and does not prove RH.
