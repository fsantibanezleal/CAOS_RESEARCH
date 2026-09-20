# EXP-007 verdict: confirmed spectral-defect parity coupling

Date: 2026-09-20. The declaration was committed at
`a2abdcc8360399b3fa42aaea9245e4b83352c30f` before implementation or
computation. The canonical certificate ran from clean commit
`d63111ffa8a348c51eb4fd06f5a1e70a51211576`.

**Verdict: confirmed.** This is an internally reviewed finite deduction and
short-interval consequence from attributed inputs. It does not establish
absolute priority, external peer acceptance, a lower onset exponent, a global
record, or the Riemann hypothesis.

## Confirmed finite theorem

[D] In the EXP-006 finite Hilbert setting, let `N` count copies, `S` count
simple real support points, `O` count distinct odd-multiplicity real support
points, `Q` be the squared-kernel pair sum, and `G` be the Gram matrix of the
simple real vectors. Define

$$
D(G)=\operatorname{tr}\Psi(G),\qquad
\Psi(x)=
\begin{cases}
(x-1)^2,&0\le x\le2,\\
2x-3,&x\ge2.
\end{cases}
$$

Then

$$
\boxed{(Q-S-D(G))(N-O)\ge2(N-S)^2.}\tag{1}
$$

The coefficient two is sharp. The arbitrary-parameter rank-trace theorem and
the spectral profile are attributed prior work. The new candidate contribution
is their coupling to the EXP-006 parity factor in (1).

## Confirmed strict curve improvement

[D] Let `h_3(theta)` be the EXP-006 simple-critical lower-proportion term,
`q(theta)=2-c(theta)`, and `kappa(theta)=k_3(theta)`. For every fixed
`theta` with `h_3(theta)>0`, take

$$
R=\frac4{h_3(\theta)},\qquad
\epsilon=d(\theta,R),\qquad p=\frac dR,
$$

where `d(theta,R)>0` is the analytic triangle energy from EXP-002, and put

$$
\alpha=\frac{2d}{5},\qquad
\beta=\frac{4d}{5R}=\frac{d h_3}{5}.
$$

Let `H(theta)` be the smaller root of

$$
2(1-s)^2=(1-\kappa)
\{q+\beta-(1+\alpha)s\}.
$$

Then

$$
\boxed{
\liminf_{T\to\infty}
\frac{S(T,T^\theta)}{N(T,T^\theta)}
\ge H(\theta)>h_3(\theta).}\tag{2}
$$

The strict comparison is symbolic:

$$
\alpha h_3-\beta=\beta>0,
\qquad
H-h_3\ge\frac{(1-\kappa)\beta}{4}>0.
\tag{3}
$$

Thus EXP-007 improves every positive point of the EXP-006 curve. It leaves the
onset bracket `0.545884<theta_HP<0.545885` unchanged.

## Frozen exact target

[MV] At `theta=0.5459`, the certificate proves

$$
d>1.6416710022140455631116821409474\mathbin{\cdot}10^{-64}
$$

and

$$
\boxed{
H-h_3>
1.3732525985593292701164661575215\mathbin{\cdot}10^{-70}.}
\tag{4}
$$

This is a rigorous strict improvement, but it is far too small to justify a
new printed decimal for the near-threshold proportion. The useful result is
the strengthened finite inequality and the full-curve theorem (2).

The `theta=3/4` sensitivity control also sets a boundary. Substituting the
historical EXP-003 pressure parameters into the product root makes that root
smaller than `h_3` by about `1.6909e-5`; the direct pressure-only lower bound
remains much stronger. Pressure parameters must be optimized for the coupled
objective rather than imported from a different headline.

## Exact evidence

[MV] The canonical result is
[`artifacts/canonical/result.json`](artifacts/canonical/result.json), schema
`riemann-exp007-results-v1`, SHA-256
`ad635c5b60c4bcae63199fb54a7979a02206ce0ee572853b2df13933dafc320c`.
It records PASS from a clean commit in 94.719 seconds.

The runner checked 652,260 rational spectral profiles, 18,479 multiplicity
profiles, exact source hashes, a correlated directed-rational gain, and overlap
with an independent 100-digit interval implementation. Four focused tests
pass. Two failed canonical attempts remain archived because they sharpened the
replay comparison and exposed the negative sensitivity control.

Replay into a fresh directory from the repository root:

```text
python problems/number-theory/riemann-hypothesis/experiments/EXP-007-spectral-defect-parity/run.py --output-dir tmp/riemann-exp007-replay --budget-seconds 180
python -m pytest -q tests/test_riemann_spectral_defect_parity.py
```

The [complete proof](mathematical-proof.md),
[adversarial audit](adversarial-audit.md), and `proof-review.json` state the
claim boundary.

## Manuscript decision

The result belongs in the existing short-interval manuscript as v0.07 because
its analytic consequence depends on EXP-002, EXP-003, EXP-005, and EXP-006 and
does not replace their setup. Splitting it now would duplicate most of that
dependency chain. A separate operator paper becomes justified only if (1) is
generalized beyond this zeta-zero kernel setting or independently formalized
as a reusable theorem.

## Scope

The result is asymptotic and supplies no effective height. It does not improve
the positivity onset or a global proportion, and its absolute novelty has not
been externally established. The general Riemann hypothesis remains open.
