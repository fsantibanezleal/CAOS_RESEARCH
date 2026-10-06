# 11. Rank-six local transfer and the earlier onset

[D+MV] EXP-008 is confirmed relative to an attributed source-certified
rank-six input. The [complete proof](../experiments/EXP-008-rank-six-local-transfer/mathematical-proof.md),
[adversarial audit](../experiments/EXP-008-rank-six-local-transfer/adversarial-audit.md),
[verdict](../experiments/EXP-008-rank-six-local-transfer/verdict.md), and
[proof-review binding](../experiments/EXP-008-rank-six-local-transfer/proof-review.json)
state the theorem and its source boundary. General RH remains open.

## Rank-independent localization

Let a fixed finite vector profile of rank $q$ have source constant $C_q$.
The local short-rectangle bookkeeping in EXP-005 depends on the common
mollifier length, rational-frequency estimate, and fixed dimension. It does
not depend on the value $q=3$. The same proof therefore gives, for every fixed
$1/2<\theta<1$,

$$
\liminf_{T\to\infty}\frac{O(T,T^\theta)}{N(T,T^\theta)}
\ge k_q(\theta):=\frac{\theta-1/2}{4eC_q}.
$$

Here $N$ counts nontrivial zero copies with multiplicity and $O$ counts
distinct odd-multiplicity critical zeros. The dimension is fixed before the
height limit. The result does not allow $q$ to grow with $T$.

Combining this odd-support curve with the sharp EXP-006 product

$$
(Q-S)(N-O)\ge2(N-S)^2
$$

gives the lower term

$$
h_q(\theta)=\frac{3+k_q(\theta)-
\sqrt{(1-k_q(\theta))(9-k_q(\theta)-8c(\theta))}}4.
$$

The complete lower bound also retains zero, Wang's cosine term, and the earlier
linear parity term.

## Source-certified rank-six input

Pearce-Crump states the interval

$$
C_6\in 0.6566338678379319741683641732\ \mathbin{+/-}\ 5.63\times10^{-18},
$$

which lies strictly below the printed rank-three constant. The public source
does not print the rank-six coefficient matrix. EXP-008 therefore treats the
existence, admissibility, and interval for $C_6$ as an attributed theorem input.
It independently proves the rank-independent localization and the subsequent
interval arithmetic, but it does not claim to reconstruct the source's
rank-six contraction.

## Certified onset and pointwise comparison

Directed rational bounds and an independent 100-digit interval replay prove

$$
0.5458837<\theta_6<0.5458838,
$$

while the same arithmetic sharpens the rank-three onset to

$$
0.5458846<\theta_3<0.5458847.
$$

The brackets are disjoint. At $\theta=0.545884$, the rank-three term remains
negative, while

$$
h_6(0.545884)>2.554112345464570216\times10^{-7}.
$$

At $\theta=0.5459$,

$$
h_6(0.5459)>0.000017764518161302323639059507973,
$$

and

$$
h_6(0.5459)-h_3(0.5459)>
9.2635430617773560329\times10^{-7}.
$$

This is about a 5.5 percent increase in the lower-bound value at that fixed
point. It is not a 5.5 percent statement about all zeta zeros.

## Spectral companion

The EXP-007 defect-parity theorem can be combined with the rank-six curve. At
$\theta=0.5459$, the optimized fixed radius $\rho=11/5$ gives a positive
certified reserve and

$$
H_6-h_6>1.7766622541125682\times10^{-68}.
$$

The gain is structurally strict and numerically tiny. It does not move the
rank-six onset because the pressure construction starts from a positive scalar
term.

## Evidence and limits

The portable canonical result has SHA-256
`1ccfa56face643fb96148856c4608577b3afa75947383cf738423ce13eeb5781`.
The runner uses exact fractions, directed Taylor bounds, and an independent
`mpmath.iv` replay. Focused tests reject changed source hashes, overlapping
onset brackets, nonpositive pointwise gains, and a false RH flag.

The result is asymptotic for each fixed exponent. It supplies no effective
starting height, no independent reconstruction of the rank-six matrix, no
global record claim, and no proof of RH. External mathematical review remains
separate from the repository's proof review and the Zenodo publication.

[Previous: spectral defect](10-spectral-defect-parity.md) | [Open questions](05-open-questions.md) | [Return to overview](README.md)
