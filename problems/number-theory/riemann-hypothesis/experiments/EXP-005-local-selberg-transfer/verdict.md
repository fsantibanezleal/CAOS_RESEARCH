# EXP-005 verdict: confirmed explicit short-interval improvement

Date: 2026-09-19. Declaration
`6fd59fec51dda399de40e0327107dba42deb5b45` was committed and pushed before
implementation. The analytic proof, source-bound exact certificate, retained
failed/superseded attempts and adversarial record support the following result.

**Verdict: confirmed.** This confirms a new deduction from attributed analytic
inputs, with exact verification of its frozen numerical consequence. It does
not establish external peer acceptance, absolute novelty priority, an
end-to-end formal proof, or the Riemann hypothesis.

## Confirmed theorem

[D] Let $O(T,H)$ count distinct odd-multiplicity zeros of
$\zeta(1/2+it)$ in $(T,T+H]$, and let $N(T,H)$ count all nontrivial zero
copies there. Let

$$
C_3=C[q_3]\in
0.6567752140190419405677628751089899133\pm10^{-17}
$$

be the certified rank-three diagonal constant in Pearce-Crump's
arXiv:2609.15329v1. For every fixed $1/2<\theta<1$,

$$
\boxed{
\liminf_{T\to\infty}\frac{O(T,T^\theta)}{N(T,T^\theta)}
\ge\frac{\theta-1/2}{4eC_3}.}
\tag{1}
$$

[D] Let $S(T,H)$ count simple critical zeros and put

$$
c(\theta)=2-\frac\theta2-\frac1{\sqrt2}\cot(\theta/\sqrt2).
$$

Combining (1) with the confirmed EXP-004 parity identity gives

$$
\boxed{
\liminf_{T\to\infty}\frac{S(T,T^\theta)}{N(T,T^\theta)}
\ge\max\left\{0,c(\theta),
\frac{c(\theta)+(\theta-1/2)/(2eC_3)}3\right\}.}
\tag{2}
$$

The third numerator in (2) is strictly increasing. The exact certificate
proves it is negative at $\theta=0.5459$ and positive at $\theta=0.546$.
Therefore its unique positivity threshold lies in

$$
\boxed{0.5459<\theta_{\rm Sel}<0.546.}
\tag{3}
$$

This improves the explicit every-interval exponent over Wang's reported
cosine threshold $0.550193964744154\ldots$. At the concrete exponent
$\theta=0.546$, the fixed admissible choice $u=0.02299$ proves

$$
\liminf\frac{O(T,T^{0.546})}{N(T,T^{0.546})}
>0.0064386933093719401643291911693851080,
$$

$$
\boxed{
\liminf\frac{S(T,T^{0.546})}{N(T,T^{0.546})}
>0.0000976239413345396825264438351212564.}
\tag{4}
$$

The optimized limiting curve raises the last lower bound to
$0.0000994910410327771597380805441742896$. The fixed-$u$ value in (4) is
retained as the direct constructive certificate with strict localization
margin $\theta-1/2-2u=0.00002$.

## Mechanism

[D] Pearce-Crump's positive-semidefinite Selberg detector preserves the sign
of Hardy's function. Repeating its rectangle argument over $[T,T+H]$ is
legitimate because the source's rational-frequency Lemma 5.7 already holds on
arbitrary subintervals of $[T,2T]$. With $U\asymp T^u$, its normalized
off-diagonal becomes

$$
O(T^{1/2+2u-\theta}\log T),
$$

so it vanishes for $u<(\theta-1/2)/2$. The diagonal, approximate-functional-
equation and horizontal errors remain uniform at this scale. Keeping the
source normalization $\aleph Y=2\operatorname{Re}\beta$ yields

$$
O(T,H)\ge\frac{H\log U}{4\pi eC_3}(1+o(1)).
$$

Riemann--von Mangoldt normalization gives (1). EXP-004's pointwise inequality
$3S\ge2N-Q+2O+D$ with $D\ge0$, together with Wang's fixed-test pair limit,
then gives (2). The detector count is distinct odd critical support, exactly
the count used by the parity identity.

## Exact evidence

[MV] The canonical result is
[`artifacts/canonical/result.json`](artifacts/canonical/result.json), schema
`riemann-exp005-results-v1`, SHA-256
`3f0ca476c0e2fe688e4e4f43fc11861d9491b3066d067e46bf88d1a441c696a5`.
It was generated from clean commit
`864fe6b7bee69c6bdac72e72fbfb88b49ac0fef2`; its receipt records PASS in
0.313 seconds. All fourteen source, interval, exponent, positive, negative and
boundary checks passed.

The runner uses exact `Fraction` Taylor enclosures for $\sqrt2$, $e$, sine and
cosine, then requires containment of an independent 100-decimal `mpmath.iv`
calculation. It pins the Pearce-Crump PDF and TeX-source hashes and the Axiom
pull-request archive. Five focused tests and Ruff passed. Both Python and
PowerShell parse the portable artifact.

Attempt 1's serialization failure and attempt 2's passed but nonportable JSON
are preserved. The final schema correction changed integer representation to
decimal strings and did not change formulas, constants or frozen parameters.
The [adversarial record](adversarial-audit.md) checks every analytic error term,
the arbitrary-subinterval quantifier, normalization, count conventions and
limit order.

Replay from the repository root into a fresh directory:

```text
python problems/number-theory/riemann-hypothesis/experiments/EXP-005-local-selberg-transfer/run.py --output-dir tmp/riemann-exp005-replay --budget-seconds 60
pytest tests/test_riemann_local_selberg.py
```

## How could this be wrong?

The theorem imports recent preprint results of Pearce-Crump and Wang. The audit
checked the exact source interfaces and re-derived the changed length
bookkeeping, but it did not reprove every analytic lemma from first principles.
A later source correction could therefore affect the result. The source search
did not find this localization and combination, but it cannot establish
absolute priority.

The theorem is asymptotic and supplies no effective onset height. It neither
improves the global simple-zero record nor proves that every zero lies on the
critical line or is simple. The general Riemann hypothesis remains open.
