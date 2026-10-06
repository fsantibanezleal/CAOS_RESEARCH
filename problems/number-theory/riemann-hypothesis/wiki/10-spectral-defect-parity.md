# Spectral-defect parity coupling

EXP-007 asks whether the convex Gram defect can survive the dimension-parity
compression that produced EXP-006. It can. The result gives a strict
improvement at every point where the EXP-006 curve is positive, although its
universal near-threshold gain is deliberately tiny and the onset is unchanged.

## Finite theorem

Use the finite Hilbert notation from Chapters 3 and 9. Let `N` count copies,
`S` count simple real support points, `O` count distinct odd-multiplicity real
support points, and `Q` be the squared-kernel pair sum. Let `G` be the Gram
matrix of the `S` simple real vectors and define

$$
\Psi(x)=
\begin{cases}
(x-1)^2,&0\le x\le2,\\
2x-3,&x\ge2,
\end{cases}
\qquad D(G)=\operatorname{tr}\Psi(G).
$$

Then

$$
\boxed{(Q-S-D(G))(N-O)\ge2(N-S)^2.}\tag{1}
$$

The proof begins with Anthropic's attributed arbitrary-parameter rank-trace
theorem. For `t>=2`, its spectral normal form is

$$
Q\ge2tN-(2t-1)S-t^2d+D_t(G),
$$

where `d=r+k` is the first remainder dimension and

$$
\Psi_t(x)=
\begin{cases}
(x-1)^2,&0\le x\le t,\\
(t-1)(2x-t-1),&x\ge t.
\end{cases}
$$

Direct branch comparison gives `Psi_t>=Psi_2`. Substituting
`t=(N-S)/d` gives

$$
Q\ge S+\frac{(N-S)^2}{d}+D(G).
$$

Multiplicity parity gives `2d<=N-O`, which proves (1). A real double point
and a real triple point show that the coefficient two remains sharp.

The general rank-trace theorem, its abstract tightness, and the eigenbasis
interpretation of the `t=2` defect are prior art. Equation (1) is the scoped
finite deduction tested here.

## Short-interval transfer

Let `h3(theta)` be the EXP-006 lower-proportion term, let
`q(theta)=2-c(theta)`, and let `kappa(theta)=k3(theta)`. If an EXP-003 pressure
certificate gives

$$
\liminf\frac{D(G)}N\ge\alpha s-\beta,
\qquad s=\liminf\frac SN,
$$

then (1) implies

$$
2(1-s)^2\le(1-\kappa)
\{q+\beta-(1+\alpha)s\}.\tag{2}
$$

For any fixed `theta` with `h=h3(theta)>0`, choose

$$
R=\frac4h,
\qquad \epsilon=d(\theta,R),
\qquad p=\frac dR,
\qquad \ell=2.
$$

Here `d(theta,R)>0` is the analytic triangle energy from EXP-002. The
pressure-frame theorem gives

$$
\alpha=\frac{2d}{5},
\qquad \beta=\frac{dh}{5},
\qquad \alpha h-\beta=\beta>0.
$$

If `H(theta)` is the smaller root of equality in (2), the quadratic sign and
derivative arguments prove

$$
H-h\ge\frac{(1-\kappa)\beta}{4}>0.
$$

Therefore

$$
\boxed{
\liminf_{T\to\infty}
\frac{S(T,T^\theta)}{N(T,T^\theta)}
\ge H(\theta)>h_3(\theta).}
$$

At `theta=0.5459`, the exact correlated lower bound for the gain exceeds
`1.3732525985593292701164661575215e-70`. The gain proves strictness but is
smaller than the independent uncertainty width of the printed baseline root,
so it does not support another decimal digit in the headline.

## What the result changes

The finite theorem now retains three pieces at once: simple support, odd
support, and the continuous Gram spectral defect. This closes a structural
gap between the Ainta stability route and the EXP-006 parity route. It also
shows that any positive lower bound on the same defect can be inserted into a
single coupled quadratic rather than compared as a separate headline.

The theorem does not move the onset. When `h3=0`, the selected radius `4/h3`
is unavailable, and configurations with no simple point have zero simple-real
Gram defect. A lower exponent requires information that survives at `S=0`,
such as a new off-line horizontal statistic, a stronger odd-support input, or
a realizability constraint beyond the first Hilbert dimension.

## Alternative disciplines and next interfaces

The interdisciplinary search separated useful analogies from missing proof
interfaces:

- Convex spectral theory is productive because it yields the exact defect in
  (1), with no probabilistic modeling assumption.
- Semidefinite programming may optimize admissible pair kernels inside proven
  Fourier support. Beyond that range it needs new arithmetic input, so an SDP
  optimum alone cannot improve the theorem.
- Signed Krein or Pontryagin geometry could affect the onset only if arithmetic
  controls the magnitude of horizontal displacement. Counting negative
  directions is insufficient because near-line pairs have arbitrarily small
  negative eigenvalues.
- Optimal transport and finite moment duality recover the current scalar
  relaxation sharply. They need a new realizability statistic, such as the
  retained `D(G)`, to become stronger.
- Bohr-Jessen concentration for finite Dirichlet polynomials concerns zeros of
  truncations and does not transfer automatically to zeros of zeta.
- The Cauchy law for projected zero ordinates becomes stronger only with a
  separate bound on total horizontal displacement. That missing input is close
  to the core RH difficulty.

The complete [EXP-007 proof](../experiments/EXP-007-spectral-defect-parity/mathematical-proof.md),
[audit](../experiments/EXP-007-spectral-defect-parity/adversarial-audit.md), and
[verdict](../experiments/EXP-007-spectral-defect-parity/verdict.md) are the
authorities. General RH remains open.

[Previous: Hilbert-parity compression](09-hilbert-parity-compression.md) |
[Return to overview](README.md)
