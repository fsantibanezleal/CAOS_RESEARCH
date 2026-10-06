# Localizing the optimized Selberg detector

Date: 2026-09-19. Status: source preflight frozen before EXP-005; the later
[confirmed verdict](../experiments/EXP-005-local-selberg-transfer/verdict.md)
and [adversarial audit](../experiments/EXP-005-local-selberg-transfer/adversarial-audit.md)
are the authority for the completed result.

## 1. New source and why it changes the route

Andrew Pearce-Crump's 2026 preprint, *Optimising Selberg's method for critical
zeros* ([arXiv:2609.15329v1](https://arxiv.org/abs/2609.15329v1)), appeared after
the previous Riemann source cutoff. Its global theorem proves

$$
\liminf_{T\to\infty}\frac{N_0(T)}{N(T)}>0.0700162
$$

by a sign-preserving Selberg detector. The paper is CC BY 4.0. The PDF and TeX
source are pinned in the source manifest by exact bytes and SHA-256. The full
43-page paper, including Sections 3--5, Section 11, both appendices, the
declaration on AI use, and the bibliography, was inspected for this preflight.

The global percentage is weaker than the 2026 pair-correlation record and is
not itself the opportunity. The decisive new feature is the paper's explicit,
coefficient-uniform rational-frequency estimate. The estimate is already
formulated for arbitrary integration subintervals of $[T,2T]$. Keeping the
actual interval length in that estimate permits a short-interval version of the
sign-change theorem. This supplies the explicit odd-multiplicity density that
EXP-004 lacked.

## 2. What the source proves

The following facts are source statements, not CAOS results.

- **[V] Sign detector.** On the critical line, the detector is Hardy's real
  function multiplied by a positive-semidefinite sum of squared mollifiers.
  Every sign change detects a distinct critical zero of odd multiplicity.
- **[V] Rectangle inequality.** Lemma 4.1 converts the logarithmic mean of the
  analytic half into a lower bound for the number of sign changes. Proposition
  4.3 optimizes the displacement and gives the global proportion
  $2u/(ec^2\gamma)$ when $U=T^u$, $c=2$, and the diagonal constant is $\gamma$.
- **[V] Uniform analytic input.** Proposition 5.8 proves the mean-square and
  horizontal bounds uniformly for the declared coefficient class. Its proof
  uses a pointwise approximate-functional-equation remainder and the
  rational-frequency spacing lemma.
- **[V] Arbitrary subinterval kernel.** Lemma 5.7 bounds the off-diagonal
  integral for arbitrary intervals $I_{\xi,\eta}\subseteq[T,2T]$. Before
  division by the averaging length its decisive factor is
  $T^{\delta-1/2}XU^2\log(2XU)$, with $X\asymp T^{1/2}$.
- **[V] Certified profile.** Theorem 11.5 and Proposition B.3 give
  $C[q_3]=0.6567752140190419405677628751089899133\ldots$ with interval radius
  below $10^{-17}$. The source's main result uses this rank-three profile.
- **[V] Scope.** The paper states a dyadic/global theorem. It does not state the
  short-interval theorem derived below.

The source also corrects two errors in Zhuravlev's printed argument: a missing
factor-two normalization penalty and a polar denominator. Those corrections are
retained. The source's $7\%$ headline must not be combined with a formula that
uses the uncorrected normalization.

## 3. Candidate short-interval deduction

Let $H=T^\theta$ with fixed $1/2<\theta<1$, and let $A(T,H)$ count distinct
ordinates in $(T,T+H]$ at which $\zeta(1/2+it)$ has odd multiplicity. Fix

$$
0<u<\frac{\theta-1/2}{2},\qquad U\asymp T^u.
$$

Use the rank-three detector and repeat the source's rectangle argument over
$[T,T+H]$. The parts requiring a changed estimate are as follows.

1. Lemma 5.7 remains applicable because every moving-truncation interval is an
   arbitrary subinterval of $[T,2T]$ for large $T$.
2. Divide its off-diagonal bound by $H$, rather than by $T$. Since
   $T^{\delta-1/2}=O(1)$ at the optimized displacement and
   $X\asymp T^{1/2}$, the normalized off-diagonal is

   $$
   O\!\left(\frac{T^{1/2}U^2\log T}{H}\right)=o(1)
   $$

   precisely under $1/2+2u<\theta$.
3. The approximate-functional-equation remainder is pointwise
   $O(T^{-1/4}U\log^3T)=o(1)$ because $u<1/4$. The diagonal bound is pointwise
   before averaging, so replacing the interval length does not change its main
   constant.
4. Horizontal argument increments are $O(U\,\mathrm{polylog}(T))=o(H)$.
   The right-edge vertical integral errors are polylogarithmic and hence also
   $o(H)$. The rectangle and Jensen steps therefore have $H$ in place of $T$.

The same logarithmic optimization as Proposition 4.3 predicts

$$
A(T,H)\ge \frac{H\log U}{4\pi e C[q_3]}(1+o(1)).
\tag{1}
$$

The Riemann--von Mangoldt formula gives
$N(T,H)\sim H\log T/(2\pi)$. Thus, for every fixed admissible $u$,

$$
\liminf_{T\to\infty}\frac{A(T,T^\theta)}{N(T,T^\theta)}
\ge \frac{u}{2eC[q_3]}.
\tag{2}
$$

Letting the fixed parameter $u$ increase to $(\theta-1/2)/2$ after the height
limit gives the candidate explicit curve

$$
\boxed{\quad
\liminf_{T\to\infty}\frac{A(T,T^\theta)}{N(T,T^\theta)}
\ge \kappa_{\rm Sel}(\theta)
:=\frac{\theta-1/2}{4eC[q_3]}
\quad}\tag{3}
$$

for every fixed $1/2<\theta<1$.

This limiting step does not make $u$ depend on $T$: prove (2) for each fixed
$u$ and then take the supremum of the resulting lower bounds.

## 4. Candidate combination with EXP-004

EXP-004 proves, for any lower bound $\kappa$ on distinct odd-multiplicity
critical support in the same interval,

$$
\liminf\frac{S(T,T^\theta)}{N(T,T^\theta)}
\ge\max\left\{0,c(\theta),\frac{c(\theta)+2\kappa}{3}\right\},
\quad
c(\theta)=2-\frac\theta2-\frac1{\sqrt2}\cot\frac\theta{\sqrt2}.
\tag{4}
$$

Substitution of (3) predicts

$$
\liminf\frac{S(T,T^\theta)}{N(T,T^\theta)}
\ge\max\left\{0,c(\theta),
\frac{c(\theta)+(\theta-1/2)/(2eC[q_3])}{3}\right\}.
\tag{5}
$$

A provisional, noncanonical high-precision scratch calculation selected the
rational exponent $\theta=273/500=0.546$ as a candidate for an exact
certificate. It suggested that the third term in (5) is positive. This scratch
calculation was used only to select the declared test point; it is not retained
as evidence and cannot support the verdict. EXP-005 will run the first canonical
directed-rounding and rational-Taylor certificate after its hypothesis is
committed.

## 5. Novelty and priority search

Fresh searches covered the paper identifier and title combined with `short
intervals`, the numerical constant `0.0700162`, Wang's arXiv identifier, and
candidate thresholds around `0.545`--`0.548`. They returned the two source
papers and secondary indexing pages, but no matching localized theorem or
combined simple-critical bound. The Pearce-Crump paper discusses the pair
correlation breakthrough and calls its own detector local, yet states only the
dyadic/global proportion. Wang states the short-interval pair theorem and its
cosine consequence, without this later Selberg input.

This is a dated bounded search, not proof of absolute priority. The proposed
theorem must be described as a new deduction from attributed inputs until it
receives external mathematical review.

## 6. Formalization update

The open AxiomMath/ZetaZerosV2 pull request
[#1](https://github.com/AxiomMath/ZetaZerosV2/pull/1), head
`02dfc0b1c63d12e6d39649a0bbe08dfc7ef6cf75`, adds assumption-free Lean proofs
of the global Riemann--von Mangoldt and pair-correlation inputs and exposes all
four headline Lamzouri bounds. Its CI build passed. The pull request remains
open and has no review decision at this cutoff. The challenge statements still
contain `sorry` by design, while the new `ZetaZeros.Unconditional` audit reports
only `propext`, `Classical.choice`, and `Quot.sound` in the axiom closures of the
audited exports. The exact source snapshot is retained under Apache-2.0.

This formalization materially improves the verification status of the global
2026 theorem. It does not formalize Wang's short-interval input, the localized
Selberg deduction above, EXP-004, or EXP-005.

## 7. Preflight boundary

The candidate result is an unconditional short-interval zero-proportion theorem
if every localization step survives proof review. It is not a proof of RH, an
effective starting height, a claim that all critical zeros are simple, or a new
global record. The finite certificate will verify constants and inequalities;
it cannot substitute for the analytic localization proof.

## 8. Post-preflight adjudication

EXP-005 passed its exact certificate and term-by-term analytic review. For every
fixed $1/2<\theta<1$, the confirmed deduction is

$$
\liminf_{T\to\infty}\frac{A(T,T^\theta)}{N(T,T^\theta)}
\ge\frac{\theta-1/2}{4eC[q_3]}.
$$

Combining it with EXP-004 gives the simple-critical curve in (5). Exact rational
enclosures prove that its new term is negative at $0.5459$ and positive at
$0.546$; symbolic differentiation proves strict monotonicity. The unique new
positivity threshold is therefore in $(0.5459,0.546)$. At $0.546$, a fixed
strictly legal mollifier exponent proves a simple-critical lower proportion
above $9.7623941\times10^{-5}$. General RH remains open.
