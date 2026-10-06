# EXP-005 adversarial validation record

Date: 2026-09-19. Declaration commit:
`6fd59fec51dda399de40e0327107dba42deb5b45`. This review separates the
analytic localization proof from the finite constant certificate. It is an
internal mathematical audit, not external peer review or formal verification.

## Primary-source re-derivation

The pinned TeX source of Pearce-Crump's *Optimising Selberg's method for
critical zeros*, arXiv:2609.15329v1, was read at Lemmas 4.1, 5.3, 5.4, 5.5 and
5.7, Propositions 4.3, 5.8 and 11.1, Theorem 11.3, Remark 11.4, Theorem 11.5,
and Proposition B.3. The audit then repeated the proof with the upper ordinate
changed from $2T$ to $T+H$, where $H=T^\theta$.

The decisive source statement is stronger than a dyadic mean-value estimate:
Lemma 5.7 explicitly permits arbitrary integration intervals
$I_{\xi,\eta}\subseteq[T,2T]$. For the moving truncation on $[T,T+H]$, each
pair interval is the intersection of $[T,T+H]$ with two threshold half-lines,
so it has exactly the required form. With $X_1\asymp T^{1/2}$, division by
$H$ gives

$$
O\!\left(T^{\delta-1/2}T^{1/2}U^2H^{-1}\log T\right)
=O\!\left(T^{1/2+2u-\theta}\log T\right).
$$

At the optimized displacement $x=1-2\delta\asymp1/\log T$,
$T^{\delta-1/2}=T^{-x/2}=O(1)$. Thus the off-diagonal is $o(1)$ for every
fixed $u< (\theta-1/2)/2$. This is the new localization inequality; no
global-to-local density inference is used.

## Mandatory attacks

| Possible failure | Attack and outcome |
|---|---|
| Lemma 5.7 only controls the full dyadic interval | The source says "arbitrary intervals" and its integration-by-parts proof depends only on containment in $[T,2T]$. The moving-truncation intersections for $[T,T+H]$ qualify. |
| The square-root cutoff was lost | Proposition 5.8 uses $X_1\asymp T^{1/2}$. Retaining it produces the threshold exponent $1/2+2u-\theta$, including the otherwise easy-to-miss $1/2$. |
| The diagonal error grows after shorter averaging | Lemma 5.5 is pointwise. Its error is $O(T^{-1/2}R_C(U))=O(T^{-1/2+2u}\log^2T)=o(1)$ for $u<1/4$, independently of $H$. The main diagonal constant is unchanged. |
| The approximate-functional-equation error accumulates over $H$ | Lemma 5.3 is pointwise: $E_U(t)=O(T^{-1/4}U\log^3T)=o(1)$. The normalized square and cross term are $o(1)$ because the main mean square stays bounded. |
| A horizontal term is merely $o(T)$ | Lemma 5.4 gives the explicit individual-edge bound $O(U\log T\{\log^2T+\eta_U+1\})$. For fixed regularization $\eta_U=O(1)$, and $u< (\theta-1/2)/2<\theta$, so this is $o(H)$. The auxiliary $\zeta$ and mollifier bounds are smaller. |
| The right-edge integrals scale like $H$ | At real part three the principal logarithms have absolutely convergent Dirichlet expansions with no constant term. Termwise integration divides each nonconstant frequency by its logarithm, giving a uniform $O(1)$ bound; this is $o(H)$. |
| The analytic half changes with the ordinate and is no longer analytic | The source fixes its phase at the dyadic block base $T$. The interval $[T,T+H]$ lies in $[T,2T]$, and Lemma 5.2 compares that fixed analytic half with the ordinate-dependent approximate-functional-equation half pointwise. |
| The PSD detector needs scalar coefficients | Proposition 11.1 explicitly extends the coefficient-uniform proof to the positive-semidefinite matrix detector. Gram Cauchy--Schwarz supplies the coefficient bound, and the regularized terminal coefficient supplies the Jensen center estimate. |
| Removing profile regularization needs uniformity in its parameter | It does not. Fix $\varepsilon>0$, take $T\to\infty$, then use Remark 11.4 to let $\varepsilon\downarrow0$. Only afterward is the supremum over fixed mollifier exponents taken. |
| The source's missing factor two reappears | The critical-line identity is $\aleph Y_C=2\operatorname{Re}\beta_C$. Thus $c=2$ and the optimized sign-change denominator is $4\pi eC_3$. The certificate and proof both retain this penalty. |
| The prime mollifier length cannot follow an arbitrary height | Bertrand's postulate supplies a prime $T^u\le U\le2T^u$, so $\log U=u\log T+O(1)$. The source uses the same selection. |
| Sign changes count copies or simple zeros | The nonnegative sum-of-squares weight has only even-order real zeros. A sign change therefore detects one distinct odd-multiplicity zero of Hardy's function. This is the distinct odd support $O$ in EXP-004, not multiplicity and not simplicity. |
| Endpoint conventions change the density | Limiting rectangle indentations handle boundary zeros. Switching among closed, open and half-open conventions changes at most two distinct support points, negligible versus $H\log T$. |
| The denominator normalization is global | Subtracting the Riemann--von Mangoldt formula at $T+H$ and $T$ gives $N(T,H)=H\log T/(2\pi)+O(H+\log T)$ for fixed $0<\theta<1$. |
| The parity combination illegitimately adds liminfs | The finite identity is pointwise: $3S\ge2N-Q+2O+D$. Divide by $N$, discard $D\ge0$, and use $\liminf(a_T+b_T)\ge\liminf a_T+\liminf b_T$. |
| The claimed threshold is decimal root finding | The certificate encloses the two function values by exact rational Taylor bounds. Strict monotonicity follows symbolically from $F'(\theta)=\{\csc^2(\theta/\sqrt2)-1\}/2+1/(2eC_3)>0$. |

No fatal defect remained after these attacks. The deduction is unconditional in
the ordinary mathematical sense relative to the cited published preprint
lemmas. Those imported analytic lemmas were source-checked but were not
reproved from first principles or formalized.

## Computational validation and retained failures

The canonical certificate started from clean commit
`864fe6b7bee69c6bdac72e72fbfb88b49ac0fef2`, passed all fourteen declared
checks, and has SHA-256
`3f0ca476c0e2fe688e4e4f43fc11861d9491b3066d067e46bf88d1a441c696a5`.
Exact rational Taylor enclosures and an independent 100-decimal `mpmath.iv`
implementation agree by interval containment. PowerShell and Python both parse
the final artifact. Five focused tests and Ruff passed before the run.

The evidence retains two earlier attempts. Attempt 1 completed every
mathematical control but failed while serializing an integer longer than
Python's default digit limit. Attempt 2 passed but encoded those exact integers
as JSON number tokens; Python parsed it, while PowerShell rejected it. That
artifact is preserved under `superseded-attempt-2`. The portable schema stores
the exact numerator and denominator as decimal strings. The fix was committed
and pushed before the canonical run; none of the mathematical formulas or
frozen parameters changed.

At $\theta=0.546$ and the strictly legal $u=0.02299$, the exponent margin is
$0.00002$. The exact lower bounds are

$$
\frac{O}{N}>0.0064386933093719401643291911693851080,
$$

and, after the EXP-004 transfer,

$$
\frac{S}{N}>0.0000976239413345396825264438351212564.
$$

The optimized curve lower bound is
$0.0000994910410327771597380805441742896$. The cosine-only upper bound at
$0.546$ is negative. The negative control proves the combined curve is still
negative at $0.5459$, and the boundary control rejects $u=0.023$ because its
off-diagonal exponent margin is zero.

## Residual risks and scope

The recent Pearce-Crump and Wang inputs have not undergone the long community
scrutiny of classical zeta theorems. A later correction to either input can
change the conclusion. The dated novelty search is bounded and cannot prove
absolute priority. The result gives no effective starting height, no global
record, no claim that all critical zeros are simple, and no proof of the
Riemann hypothesis. The rank-six constant printed in the source is marginally
stronger, but its full profile data are not printed; EXP-005 deliberately uses
the fully reproducible rank-three profile.
