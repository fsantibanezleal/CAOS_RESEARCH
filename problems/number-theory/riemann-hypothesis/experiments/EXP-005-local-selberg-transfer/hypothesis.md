# EXP-005: local Selberg transfer and explicit sub-threshold simplicity

Declared: 2026-09-19. Device: CPU. Baseline: latest `origin/develop` at
`b2b29ee8fb1c25760d683fa1b88b6bcbdf52d766`, plus the source dossier and
manifest changes committed with this declaration. Status at declaration:
paper derivation complete; canonical implementation, exact certificate,
adversarial audit, and verdict unexecuted. The declaration commit must be
pushed before any canonical run.

## Question and motivation

Can Pearce-Crump's coefficient-uniform Selberg detector be localized to every
fixed interval $(T,T+T^\theta]$ with $\theta>1/2$, and can the resulting explicit
odd-multiplicity density make the EXP-004 simple-critical lower bound positive
at the concrete exponent $\theta=273/500=0.546$?

The [source preflight](../../context/2026-09-19-local-selberg-transfer.md)
records the complete proposed deduction, primary-source scope, formalization
update, and dated novelty search. This target replaces EXP-004's unspecified
classical constant by an explicit curve and would give a decimal interval
exponent below Wang's positivity root.

## Falsifiable prediction

Let $A(T,H)$ count distinct odd-multiplicity critical zeros in
$(T,T+H]$, and let $N(T,H)$ count all nontrivial zero copies. Let

$$
C_3=C[q_3]
$$

be Pearce-Crump's certified rank-three diagonal constant. Predict that for every
fixed $1/2<\theta<1$,

$$
\liminf_{T\to\infty}\frac{A(T,T^\theta)}{N(T,T^\theta)}
\ge \frac{\theta-1/2}{4eC_3}.
\tag{A}
$$

Combining (A) with the confirmed EXP-004 parity inequality predicts

$$
\liminf_{T\to\infty}\frac{S(T,T^\theta)}{N(T,T^\theta)}
\ge \max\left\{0,c(\theta),
\frac{c(\theta)+(\theta-1/2)/(2eC_3)}{3}\right\},
\tag{B}
$$

where

$$
c(\theta)=2-\frac\theta2-\frac1{\sqrt2}\cot(\theta/\sqrt2).
$$

At the frozen rational point $\theta=273/500$, predict that the final term
in (B) is strictly positive. The canonical run must certify a conservative
rational lower bound of at least $9\times10^{-5}$ for this simple-critical
proportion. It must also certify that $c(273/500)<0$, so the positive conclusion
really lies below the baseline cosine threshold.

A provisional scratch calculation selected this point before declaration. It is
not evidence, will not be copied into the artifacts, and cannot satisfy PASS.

## Source-complete gate and premise dependencies

| Premise | Evidence and status before the run |
|---|---|
| Pearce-Crump sign detector, rectangle argument, pointwise remainder, diagonal constant and interval certificate | Primary arXiv:2609.15329v1 PDF and TeX source; reviewed in the 2026-09-19 dossier; imported analytic input, not yet independently reproved end to end |
| Arbitrary-subinterval rational-frequency estimate | Lemma 5.7 and proof of Proposition 5.8 in the pinned source; decisive input for localization |
| Short-interval normalization $N(T,T^\theta)\sim T^\theta\log T/(2\pi)$ | Riemann--von Mangoldt input already used in confirmed EXP-002/004; error is negligible for fixed $\theta>0$ |
| Parity transfer from odd support to simple critical zeros | Confirmed EXP-004 identities, proof, exact artifacts, and verdict |
| Wang pair-sum transfer and cosine curve | Confirmed EXP-002/003/004 proofs and primary Wang audit |
| Numeric source enclosure for $C_3$ | Proposition B.3: printed center with radius below $10^{-17}$; exact rational profile and Bernstein data printed in Appendix B |
| Novelty | Dated primary-source and web search in the dossier; bounded, not exhaustive |

The AxiomMath open pull request is evidence about formal verification of the
global inputs only. It is not a premise for (A) or (B).

## Local analytic method to adjudicate

Fix $H=T^\theta$, $U\asymp T^u$, and
$0<u<(\theta-1/2)/2$. Repeat the source's rectangle proof on
$[T,T+H]$. The proof review must verify, term by term:

1. the right-edge logarithmic integrals and all horizontal increments are
   $o(H)$;
2. the diagonal estimate remains uniform over the shorter interval;
3. the pointwise approximate-functional-equation remainder is $o(1)$;
4. Lemma 5.7 gives normalized off-diagonal
   $O(T^{1/2+2u-\theta}\operatorname{polylog}T)=o(1)$;
5. Jensen's inequality and the optimized displacement retain the factor
   $1/(4\pi e C_3)$ in the sign-change count;
6. the count is distinct odd critical support, matching EXP-004's $O$;
7. $u$ is fixed during $T\to\infty$, and the supremum
   $u\uparrow(\theta-1/2)/2$ is taken afterward.

Any one missing uniformity or count-convention match makes the asymptotic
prediction inconclusive even if the finite constant certificate passes.

## Exact computational scope

After this declaration is committed and pushed, implement a deterministic
`run.py` with no stochastic search and no network access. It will:

1. parse frozen rational upper and lower enclosures for $C_3$ and for $e$;
2. certify $\sin$ and $\cos$ at the rational argument
   $273/(500\sqrt2)$ using directed rational Taylor remainders, independently
   recomputing $c(273/500)$ without a floating library;
3. derive a rational lower bound for
   $\kappa_{\rm Sel}=(\theta-1/2)/(4eC_3)$ and for
   $(c(\theta)+2\kappa_{\rm Sel})/3$;
4. prove the strict exponent inequalities for a frozen rational mollifier
   exponent, including $1/2+2u<273/500$ and $u<1/4$;
5. run an independent high-precision interval implementation and require its
   enclosure to contain the rational certificate;
6. preserve negative controls with $θ$ below the predicted root and with the
   forbidden boundary $1/2+2u=\theta$, neither of which may pass the strict
   theorem gate;
7. emit canonical JSON, raw stdout, source hashes, and an execution receipt
   without overwriting an existing result.

The canonical result must keep the analytic theorem status separate from the
finite constant status.

## Invariant-first decision

The distinguishing invariant is the exponent of the normalized off-diagonal:

$$
T^{1/2+2u-\theta}.
$$

Its sign decides whether the source's coefficient-uniform mean square localizes.
No GPU search, zero list, kernel optimization, or higher-point certificate is
needed. The second cheap invariant is the EXP-004 atom charge $s+E-O\ge0$,
already confirmed and reused without modification.

## PASS, FAIL, and one-sidedness

A finite PASS proves only the frozen transcendental inequalities, constants,
strict exponent margins, source identities, and cross-implementation agreement.
It does not by itself prove (A). A confirmed verdict additionally requires a
complete paper proof of every localization step and an adversarial review that
tries to break the uniformity, normalization, and count conventions.

A finite FAIL refutes the frozen decimal consequence or reveals an implementation
error; the raw failure is retained. A proof-review FAIL or unsupported imported
estimate refutes or suspends (A) and therefore (B), regardless of numerical
output. Discovery of prior art changes the novelty conclusion without changing a
valid mathematical deduction.

Mandatory attacks are: replacing interval length $T$ by $H$ in every error term;
the arbitrary-subinterval quantifier in Lemma 5.7; the square-root truncation
$X\asymp T^{1/2}$; the factor $c=2$; counted-with-multiplicity denominators versus
distinct sign changes; endpoint zeros; fixed versus moving $u$; the printed
$C_3$ radius; and the possibility that a right-edge or horizontal term is only
$o(T)$ rather than $o(H)$.

## Budget and kill criterion

Expected canonical runtime is below five CPU seconds. The hard budget is sixty
seconds, with flushed stage output and a checkpoint after source validation and
after each interval calculation. A timeout records the completed prefix and an
inconclusive computation. It cannot confirm the finite certificate or theorem.
There is no escalation of precision beyond 512 bits, no parameter search, and no
GPU allocation.

## Consequences and boundaries

If confirmed, EXP-005 supplies an explicit odd-multiplicity density in every
fixed power interval above exponent $1/2$ and a positive proportion of simple
critical zeros at exponent $0.546$, improving the explicit interval range over
Wang's reported cosine threshold. It does not solve RH, prove all zeros simple,
give an effective onset height, improve the global 67.25% record, or constitute
external peer review.
