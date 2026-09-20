# Hilbert dimension and parity compression preflight

Date: 2026-09-20. Status: frozen before EXP-006 computation. This is a
source and derivation preflight, not a verdict.

## Question

EXP-004 combined a linear Hilbert stability estimate with a lower bound for
distinct odd-multiplicity critical zeros. Its scalar relaxation retained only
the excess inequality `S + E >= O`. The relaxation was proved optimal for
those two scalar constraints, but it did not use the dimension of Lamzouri's
first Hilbert subspace.

The proposed refinement keeps that dimension. For a nonempty finite multiset
`Z` invariant under complex conjugation, let:

- `N` be its cardinality counted with multiplicity;
- `S` be the number of simple real elements;
- `O` be the number of distinct real elements of odd multiplicity; and
- `Q` be Lamzouri's squared-kernel pair sum.

The candidate finite inequality is

$$
Q(N-O)\ge 2(N-S)^2. \tag{P}
$$

When `N=O`, all elements must be simple and real, so the right interpretation
is `S=N`; the displayed product inequality remains valid.

## Proposed derivation and decisive invariant

Use the notation in the proof of Proposition 2.1 of Lamzouri's arXiv
2609.02882v2. The first nested subspace has dimension `d=r+k`, where `r`
counts nonsimple real support points and `k` counts nonreal conjugate support
pairs. If `alpha_j` are the real diagonal coefficients obtained after
Gram-Schmidt, Lamzouri proves Bessel's bound

$$
Q\ge\sum_j\alpha_j^2
$$

and his first-range calculation gives

$$
\sum_{j\le d}\alpha_j\ge N-S.
$$

Cauchy-Schwarz would therefore give

$$
Q\ge\frac{(N-S)^2}{d}.
$$

Every nonsimple real point consumes at least two copies, every nonreal pair
consumes at least two copies, and each odd nonsimple real point consumes at
least one additional copy. Hence

$$
N-S\ge 2d+(O-S),\qquad 2d\le N-O.
$$

These two estimates imply (P) when `d>0`. The `d=0` case must be handled
separately. This argument is short, but every count convention and the use of
real coefficients after Gram-Schmidt must be rechecked against the primary
proof before confirmation.

The decisive invariant is the dimension ratio

$$
\frac{N-S}{r+k},
$$

which was replaced by the coarser lower bound `2` in the published finite
inequalities. Parity makes the upper bound `2(r+k) <= N-O` strict whenever an
odd multiple real point is present.

## Proposed short-interval transfer

Wang's fixed-test short-interval theorem gives

$$
\frac QN\longrightarrow 2-c(\theta),
\qquad
c(\theta)=2-\frac\theta2-
\frac1{\sqrt2}\cot\!\left(\frac\theta{\sqrt2}\right).
$$

EXP-005 gives, for the reproducible rank-three Selberg profile,

$$
\liminf\frac ON\ge
k_3(\theta):=\frac{\theta-1/2}{4eC_3}.
$$

If (P) is valid, the proposed additional lower bound is

$$
\liminf\frac SN\ge
1-\sqrt{\frac{(2-c(\theta))(1-k_3(\theta))}{2}}. \tag{T}
$$

The positive range in (T) begins when

$$
c(\theta)+(2-c(\theta))k_3(\theta)>0. \tag{R}
$$

This differs structurally from EXP-004's condition
`c(theta)+2 k_3(theta)>0`. The new correction is
`-c(theta) k_3(theta)`, which is positive below Wang's root.

## Source scope and novelty boundary

The exact proof interfaces inspected for this preflight are:

1. Lamzouri, arXiv:2609.02882v2, Proposition 2.1 and its first-range
   Gram-Schmidt, Bessel, and multiplicity estimates;
2. Wang, arXiv:2609.07918v1, the short-interval pair formula and finite
   transfer;
3. the confirmed EXP-004 parity proof and its explicit statement that the
   scalar relaxation may be improved by additional mass or geometric
   constraints; and
4. the confirmed EXP-005 localization using Pearce-Crump's reproducible
   rank-three constant.

A dated exact-phrase and concept search on 2026-09-20 found the Lamzouri and
Wang sources and the known pair-correlation literature, but did not locate
(P), (T), or the dimension-parity compression above. This search was bounded
and cannot establish priority. The finite inequality may be an unstated
corollary of the same Hilbert-space proof. Novelty must be reported narrowly
as the explicit inequality and its short-interval consequence unless a wider
search or peer review finds prior art.

Pearce-Crump's Appendix B also states a stronger rank-six numerical benchmark
`C[q_6]`, but it does not print the rank-six profile. EXP-006 will record its
sensitivity effect separately. It is not needed for (P), and it cannot replace
the fully reproducible `C_3` premise in the canonical theorem.

## Required attacks

EXP-006 must try to refute the proposal by checking:

- the `d=0` and `N=O` cases;
- odd real multiplicities `1`, `3`, and at least `5`;
- even real multiplicities and simple or repeated nonreal pairs;
- whether the first-range coefficient sum is really at least `N-S` with the
  source's signs and conjugation convention;
- whether Cauchy-Schwarz can be applied to real coefficients without a lost
  absolute value;
- scaling of `Q`, `N`, `S`, and `O` under repeated copies;
- the direction of liminf and limsup in passing from (P) to (T);
- endpoint and smoothing limits in Wang's theorem;
- exact arithmetic at the frozen rational exponent; and
- comparison against the existing linear parity curve, including regimes in
  which either bound dominates.

No claim here solves the Riemann hypothesis, proves an effective height, or
constitutes external peer review.
