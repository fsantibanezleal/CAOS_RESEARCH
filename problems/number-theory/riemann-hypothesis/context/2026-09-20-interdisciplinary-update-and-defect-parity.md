# Interdisciplinary update and the spectral-defect parity seam

Date: 2026-09-20. Search cutoff: 2026-09-20 12:00 UTC.

This dossier records the source preflight for EXP-007. It separates recent
primary-source updates, methods imported from other areas, and the exact seam
that remains after EXP-006. The general Riemann hypothesis remains open.

## 1. Source changes after the previous cutoff

The arXiv API was queried for recent work containing `Riemann zeta`, ordered by
submission date, and the directly relevant GitHub repositories were checked at
their live heads.

| Source | Inspected state | Consequence for this program |
|---|---|---|
| Dubon, [arXiv:2609.17875v1](https://arxiv.org/abs/2609.17875v1) | 28 pages, submitted September 15 | Proves vertical zero-density concentration for finite Dirichlet polynomials through Jessen potentials, a finite Bohr lift, and isolated-prime anti-concentration. Its zeros are zeros of truncations, not zeros of the zeta function, so it supplies a design analogy rather than an RH input. |
| Najnudel and Nikeghbali, [arXiv:2609.15862v1](https://arxiv.org/abs/2609.15862v1) | 36 pages, submitted September 14 | Gives an unconditional Cauchy limit for a Stieltjes transform of projected zeta ordinates. The comparison with the logarithmic derivative assumes the total right-side distance from the critical line is `o(T)`. That horizontal-collapse premise is not supplied by the current pair theorem. |
| Pearce-Crump, [arXiv:2609.15329v1](https://arxiv.org/abs/2609.15329v1) | unchanged v1 | Its rank-three Selberg profile remains the reproducible odd-support input used by EXP-005 and EXP-006. The printed rank-six value still lacks the full profile needed for independent certification. |
| AxiomMath, [ZetaZerosV2 PR 1](https://github.com/AxiomMath/ZetaZerosV2/pull/1) | open, clean merge state, head `02dfc0b1c63d12e6d39649a0bbe08dfc7ef6cf75`, updated September 16 | The PR exposes assumption-free Lean versions of the global Riemann-von Mangoldt and pair-correlation inputs. Its stated build has 9,042 jobs and standard axioms only. It does not formalize Wang's short-interval theorem or the EXP-005/006 transfers. |
| teal-sea, [zeta-lab](https://github.com/teal-sea/zeta-lab/tree/f402358c6c3f3c838605e71dd97cb6401a6963f0) | head `f402358c6c3f3c838605e71dd97cb6401a6963f0`, September 18 | Post-September-12 changes concern prime-pair-error and Davenport-Heilbronn campaigns, not an identical short-interval parity product. The older stable rank-trace bridge is decisive prior art for the parameterized spectral defect used below. |

The two new arXiv PDFs are retained in the local `source-cache` with byte sizes
and SHA-256 hashes in `source-manifest.json`. Their arXiv license is the
perpetual non-exclusive distribution license, so the public repository records
provenance and hashes without relicensing or tracking the PDFs.

## 2. What the existing formal source already proves

The Anthropic/Axiom multiplicity-aware rank-trace theorem uses

$$
g_t(x)=x^2-tx-(x-t)_+^2.
$$

At an eigenbasis presentation of the simple-real positive block, that theorem
retains the complete spectral sum of `g_t`. The teal-sea bridge identified the
usual Ainta profile at `t=2` as this same function plus an affine term. Thus the
parameterized defect is prior work and is not an EXP-007 novelty claim.

For `t>=2`, define

$$
\Psi_t(x)=g_t(x)+(t-2)x+1
=\begin{cases}
(x-1)^2,&0\le x\le t,\\
(t-1)(2x-t-1),&x\ge t.
\end{cases}
$$

If `G` is the Gram matrix of the `S` simple real support points, then
`tr G=S`, so adding the affine term changes no aggregate bookkeeping. The
attributed rank-trace theorem therefore gives

$$
Q\ge2tN-(2t-1)S-t^2d+D_t(G),
\qquad D_t(G)=\operatorname{tr}\Psi_t(G),
\tag{1}
$$

where `d=r+k` is the first Hilbert-subspace dimension. At `t=2`, `D_t` is the
spectral defect used by EXP-002 and EXP-003. Pointwise comparison gives
`Psi_t>=Psi_2` for every `t>=2`.

## 3. The candidate new seam

EXP-006 substituted `t=(N-S)/d` into the defect-free form of (1) and then used
`2d<=N-O`. Retaining the attributed defect through exactly those two steps
predicts

$$
\boxed{(Q-S-D(G))(N-O)\ge2(N-S)^2,}
\qquad D(G)=D_2(G).
\tag{2}
$$

The finite coefficient two stays sharp because a single real point of
multiplicity two or three has no simple Gram block and gives equality. Equation
(2) is nevertheless strict relative to EXP-006 whenever `D(G)>0` and
`N>O`.

No inspected primary paper, formal source, or live repository states (2) or its
short-interval consequence. This is bounded negative evidence only. The
parameterized rank-trace theorem, the spectral profile, pressure packing, Wang's
pair theorem, and the Selberg odd-support seed are all attributed inputs.

## 4. Transfer predicted from pressure packing

Suppose a fixed cosine kernel has a certified pressure inequality with parameters
`p,epsilon,k`, and put

$$
M=2k+1,
\qquad \alpha=\frac{k\epsilon}{M},
\qquad \beta=\frac{2kp}{M}.
$$

EXP-003 proves, after the lawful fixed-test and smoothing limits,

$$
\liminf\frac{D(G)}N\ge\alpha s-\beta,
\qquad s=\liminf\frac SN.
\tag{3}
$$

Write `q(theta)=2-c(theta)` and let `kappa(theta)=k_3(theta)` be the
EXP-005 odd-support curve. Equations (2)-(3) predict the necessary quadratic

$$
2(1-s)^2\le
(1-\kappa(\theta))
\{q(\theta)+\beta-(1+\alpha)s\}.
\tag{4}
$$

Its smaller root is

$$
H(\theta;\alpha,\beta)=
\frac{4-(1+\alpha)(1-\kappa)-
\sqrt{[4-(1+\alpha)(1-\kappa)]^2
-8[2-(1-\kappa)(q+\beta)]}}4.
\tag{5}
$$

At `alpha=beta=0`, this is the EXP-006 curve `h_3(theta)`. If a pressure
choice makes `alpha*h_3-beta>0`, substituting `s=h_3` makes (4) fail strictly,
so `H>h_3`.

The universal analytic triangle bound already proved in EXP-002 supplies such a
choice for every fixed `theta` with `h_3(theta)>0`: take
`R=4/h_3(theta)`, its positive analytic energy `d(theta,R)`, set
`epsilon=d`, `p=d/R`, and take `k=2`. Then

$$
\alpha h_3-\beta=\frac{d h_3}{5}>0.
$$

If certified, this gives an explicit strict improvement of the full positive
EXP-006 curve. It does not lower the onset exponent because the simple Gram
defect vanishes at `S=0`.

## 5. Cross-disciplinary evaluation

| Viewpoint | Useful translation | Missing interface or decision |
|---|---|---|
| Convex spectral analysis and frame theory | `D_t(G)` is a convex spectral distance from the equality spectrum. Schur-Horn and pinching turn local Gram geometry into an additive certificate. | This is the productive seam for EXP-007. Its parameterized form is prior art; coupling it to parity is the candidate contribution. |
| Semidefinite programming | Chirre, Goncalves, and de Laat optimize pair-correlation test functions by SDP. An SDP can search pressure profiles or weighted block covers. | Their published bounds use RH-conditional positivity outside the unit Fourier support. Any new profile must remain inside Wang's unconditional short-interval support and end in exact interval or SOS certificates. |
| Coding theory and Delsarte linear programming | Odd multiplicity is a parity syndrome, while Gram entries act like pairwise code correlations. Dual polynomials suggest finite cover inequalities. | The analogy becomes a proof only after producing a positive-type kernel inequality with the correct multiplicity and conjugation symmetries. No current MacWilliams identity controls the zeta pair sum. |
| Statistical mechanics and pressure | EXP-003 already turns local energy plus span pressure into a thermodynamic-looking density bound. | Larger frames can improve constants but do not alone cross the `S=0` threshold. They remain useful inside (2). |
| Probability and stationary point processes | The new Cauchy-law paper gives a robust transform limit for projected ordinates without RH. | Its logarithmic-derivative comparison needs horizontal collapse. Pair data and parity do not currently prove that premise. |
| Bohr-Jessen convex potentials | The new Dirichlet-polynomial paper shows how isolated prime coordinates force a one-corner limiting potential. | The objects are finite truncations and their vertical mean zeros. Passing that concentration to zeta zeros would require a uniform truncation approximation that is absent and is unsafe to assume. |
| Krein and Pontryagin space geometry | Off-line conjugate pairs form signed rank-two blocks. A quantitative negative-direction defect could improve the threshold even when `S=0`. | Near-line pairs have arbitrarily small negative eigenvalues. A useful theorem needs new arithmetic control of horizontal displacement, not only an inertia count. |
| Optimal transport and moment duality | The scalar relaxation can be written as a finite moment problem over multiplicity types, with exact dual witnesses. | EXP-006 already solves the first-dimension relaxation sharply. A better scalar dual must import a realizability statistic such as `D(G)` or a new analytic moment. |

## 6. Manuscript decision rule

If EXP-007 confirms (2) and (5), it is a direct strengthening of the existing
short-interval stability manuscript and belongs in version 0.07. A separate
paper is justified only if the parameterized defect-parity theorem is developed
as an independent operator-theoretic result with applications beyond the zeta
transfer. Splitting now would duplicate the same analytic dependencies and
obscure the short proof chain.

## 7. Explicit boundaries

This preflight does not prove (2), (4), a lower onset exponent, an effective
height, density one, or RH. It does not promote an open GitHub PR to a published
formal result. The computation declared in EXP-007 may test identities and
certify constants, but the universal theorem requires a separate written proof,
adversarial audit, and proof-review binding.
