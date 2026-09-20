# EXP-007: spectral-defect parity coupling

Declared: 2026-09-20. Device: CPU. Baseline: release `v0.71.000` and public
develop commit `824efb1c837b16882f5d534b4a1858341cc4fc1c`.

Status at declaration: source preflight and paper derivation completed;
experiment code and numerical target have not been run. This declaration must
be committed before implementation or computation.

## Question

Can the parameterized spectral defect already present in the attributed
multiplicity-aware rank-trace theorem be retained through EXP-006's
dimension-parity compression, and can the existing pressure machinery then
give a strict improvement of the complete positive EXP-006 curve?

## Prediction A: finite theorem

Use the notation of EXP-006. Let `G` be the Gram matrix of the `S` simple real
support points and

$$
D(G)=\operatorname{tr}\Psi(G),\qquad
\Psi(x)=\begin{cases}(x-1)^2,&0\le x\le2,\\2x-3,&x\ge2.
\end{cases}
$$

The prediction is

$$
\boxed{(Q-S-D(G))(N-O)\ge2(N-S)^2.}
\tag{A}
$$

The coefficient two is predicted to remain sharp through the one-point
multiplicity-two and multiplicity-three examples. The new content is the
simultaneous retention of `D(G)` and `O`, not the rank-trace theorem, the
spectral profile, or either ingredient separately.

The proof target is to define for every `t>=2`

$$
\Psi_t(x)=\begin{cases}(x-1)^2,&0\le x\le t,\\
(t-1)(2x-t-1),&x\ge t,
\end{cases}
$$

derive

$$
Q\ge2tN-(2t-1)S-t^2d+\operatorname{tr}\Psi_t(G),
\tag{B}
$$

from the attributed general `g_t` rank-trace inequality, prove
`Psi_t>=Psi_2`, substitute `t=(N-S)/d`, and use `2d<=N-O`.

## Prediction B: strict short-interval improvement

For every fixed `theta` with `h_3(theta)>0`, take

$$
R=\frac4{h_3(\theta)}
$$

and the positive analytic triangle energy `d(theta,R)` from equation (18) of
the EXP-003 proof. Set

$$
\epsilon=d,\qquad p=d/R,\qquad k=2,\qquad
\alpha=\frac{2d}{5},\qquad\beta=\frac{4d}{5R}.
$$

Let `H(theta)` be the smaller root in `s` of

$$
2(1-s)^2=(1-k_3(\theta))
\{2-c(\theta)+\beta-(1+\alpha)s\}.
\tag{C}
$$

The prediction is

$$
\liminf_{T\to\infty}
\frac{S(T,T^\theta)}{N(T,T^\theta)}
\ge H(\theta)>h_3(\theta).
\tag{D}
$$

The strict comparison should follow before decimal evaluation from
`alpha*h_3-beta=d*h_3/5>0`.

## Frozen numerical target

At

$$
\theta=5459/10000,
$$

the experiment will certify all inputs in (C), prove `H>h_3` with outward
rational intervals, and report a lower enclosure for `H-h_3`. No minimum gain
size is required: the target is strict positivity under the declared analytic
energy formula. The result is refuted if the exact interval for the gain is not
strictly positive.

As a sensitivity control, the existing EXP-003 pressure certificate at
`theta=3/4` will be inserted into (C). It may improve the product term while
remaining below the already stronger pressure-only headline. Such an outcome is
diagnostic and must not be advertised as a new best bound at that exponent.

## Required exact checks

1. Verify the two piecewise formulas for `Psi_t`, continuity at `x=t`,
   nonnegativity for `t>=2`, and `Psi_t>=Psi_2` on both branches.
2. Enumerate rational spectral profiles with nonnegative entries summing to
   `S` and confirm the aggregate affine-shift identity connecting `g_t` and
   `Psi_t`.
3. Enumerate finite multiplicity profiles through at least multiplicity seven,
   including empty dimension, equality, and strict cases, and check every
   scalar step in (A).
4. Recompute `c(theta)`, `k_3(theta)`, `h_3(theta)`, `R`, the analytic energy,
   `alpha`, `beta`, `H`, and the strict gain with directed rational Taylor
   bounds.
5. Replay the final transcendental interval independently with at least
   100-digit `mpmath.iv` arithmetic.
6. Bind the declaration, runner, imported EXP-002/003/005/006 artifacts, and
   output hashes in the canonical result.

## Budget and stop rules

The run is CPU-only and capped at 180 seconds. No GPU workload is justified by
one-dimensional interval arithmetic and finite exact censuses. Floating-point
values may guide display precision but cannot discharge a sign or theorem gate.
Any unresolved interval, nonpositive gain enclosure, source-hash mismatch, or
failed independent replay gives an inconclusive or refuted computational
verdict. It does not authorize changing `R`, `k`, the target exponent, or the
energy formula without a new committed declaration.

## Source and novelty boundary

The general `g_t` rank-trace inequality and its tightness are attributed to the
Anthropic formal source. The eigenbasis spectral interpretation and the
`t=2` Ainta profile identification are attributed to the inspected teal-sea
bridge. The pressure assembly is EXP-003 and prior pressure-frame work. Wang
supplies the short-interval pair limit; Pearce-Crump and EXP-005 supply the
odd-support curve.

The dated source search is recorded in
`context/2026-09-20-interdisciplinary-update-and-defect-parity.md`. The scoped
candidate contribution is (A), its proof as a defect-parity coupling, and (D).
No absolute priority, external acceptance, lower onset exponent, effective
height, global record, or proof of RH is predicted.
