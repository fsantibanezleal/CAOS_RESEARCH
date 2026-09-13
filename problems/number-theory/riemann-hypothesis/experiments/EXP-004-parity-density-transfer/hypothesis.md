# EXP-004: parity density transfer across the cosine positivity threshold

Declared: 2026-09-12. Device: CPU. Baseline: `be5aac4` plus the source and
independent audit committed with this declaration. Status at declaration: paper
derivation reviewed; all new exact computational checks unexecuted. The hypothesis
must be committed and pushed before implementation or execution.

## Question and motivation

Can classical sign-change information improve the interval exponent for a positive
proportion of simple critical zeros, even when Wang's explicit simple-zero bound
is nonpositive? This changes the target from EXP-003's constant improvement to a
strict extension of the interval range. The mechanism combines arithmetic parity
with multiplicity information retained by the finite spectral inequality.

Primary-source statements, count conventions, packing, and candidate proof are in
[the critical-mass dossier](../../context/2026-09-12-critical-mass-and-multiplicity-route.md).
The independent review is recorded separately in the context directory. The
classical seed, finite stability mechanism, and Wang arithmetic theorem are prior
work. A new claim concerns their combined short-interval consequence, with the
dated novelty search and its limits preserved.

## Falsifiable finite predictions

Let a finite conjugation-invariant multiset have total multiplicity N, s simple
real support points, r multiple real support points, b nonreal conjugate pairs,
O distinct odd-multiplicity real support points, and Z distinct complex support
points. Define

$$E=N-s-2r-2b,\qquad Z=s+r+2b.$$

For the existing finite Hilbert operator let Q be its squared Hilbert--Schmidt
norm, and D the nonnegative simple-real Gram defect. Ordinary complex squares,
not squared moduli, occur in its full kernel pair sum. The imported inequality is

$$Q\ge4N-3s-4r-4b+D=2N-s+2E+D.$$

Set $\sigma=Q-(4N-3s-4r-4b+D)\ge0$. The predictions are the exact certificates

$$3s-(2N-Q+2O+D)=2(s+E-O)+\sigma\ge0,\tag{A}$$

$$6Z-(7N-2Q+O+2D)=(s+E-O)+6b+2\sigma\ge0.\tag{B}$$

Nonnegativity is atomwise: a simple real point contributes zero to s+E-O;
a multiple real point of even multiplicity m contributes m-2; one of odd
multiplicity m>=3 contributes m-3; a nonreal pair of multiplicity m on each
point contributes 2(m-1). These formulas include the boundary multiplicities.

The distinct bound (B) must be derived separately. The proposed shortcut
$2Z\ge N+s$ is false in the full multiset class, as shown by a single real
point of multiplicity three. Replacing its s by a new simple lower bound would
not fix that counting mistake.

For a relaxed scalar problem with real c, o>=0, s>=0, e>=0,
s-2e>=c and s+e>=o, predict the exact minimum

$$s_{\min}=\max\{0,c,(c+2o)/3\}.\tag{C}$$

The candidate primal witness is e=max(0,o-s_min). The three lower bounds give
dual certificates, with the parity bound obtained by adding one copy of
s-2e>=c and two copies of s+e>=o. This is optimality for the stated relaxation,
not for all geometric zero configurations or all arithmetic information.

## Predicted short-interval theorem

Write

$$c(\theta)=2-\theta/2-\cot(\theta/\sqrt2)/\sqrt2,$$

and let theta0 be its unique zero on (0,1). Fix the classical seed exponent
$\alpha=51/100<\theta_0$. Selberg's odd-zero theorem, restated and verified
in Karatsuba's original paper, supplies one constant a>0 such that every
sufficiently high seed interval contains at least a times its length times
logarithm of its starting height distinct odd critical zeros.

Packing consecutive seed intervals gives one fixed kappa>0 such that

$$\liminf_{T\to\infty}O(T,T^\theta)/N(T,T^\theta)\ge\kappa$$

for every fixed theta in (alpha,1). The same kappa is available throughout
this range; the starting height may depend on theta. Every denominator N
counts all nontrivial zero copies in (T,T+T^theta].

Apply (A) and (B) to Wang's fixed-test pair-sum limit. First take the height
limit with smooth density and support lambda<theta fixed. Then take the
smooth approximation limit, followed by lambda increasing to theta. Predict

$$\liminf S/N\ge\max\{0,c(\theta),(c(\theta)+2\kappa)/3\},\tag{D}$$

$$\liminf Z/N\ge\max\{\kappa,(1+c(\theta))/2,
(3+2c(\theta)+\kappa)/6\}.\tag{E}$$

Here S counts simple critical zeros and Z counts distinct zeros. In particular
at theta0 the simple lower bound is 2kappa/3>0. Since
$c'(\theta)=\tfrac12\cot^2(\theta/\sqrt2)<1/\theta^2<4$ for
theta>=alpha, define

$$\delta=\min\{(\theta_0-\alpha)/2,\kappa/4\}>0.$$

Then theta1=theta0-delta lies strictly between alpha and theta0, and (D)
predicts a simple-critical proportion at least kappa/3 for every fixed
theta>=theta1 with theta<1. This is a strictly smaller interval exponent
than the zero of Wang's displayed curve. It is an existential range extension,
not a certified decimal value of theta1. An optional distinct consequence can
use a smaller delta; it must be justified from (E), not from a half-sum shortcut.

## Source-complete gate and premise dependencies

| Premise | Evidence and status before computation |
|---|---|
| Finite operator, complex-square convention and multiplicity excess | Confirmed EXP-002/003 proofs and verdicts; retained exact inequality, not a new spectral assumption |
| Wang fixed smooth-test limit and legal support/approximation order | Context arithmetic-transfer audit and pinned 2609.07918v1; EXP-002/003 confirmed transfer |
| Distinct odd-zero seed for every sufficiently high interval | Karatsuba 1985 main theorem and Theorem B, plus p.536 sign-change counting; primary PDF visually inspected; new critical-mass source dossier |
| theta0>51/100 and derivative formula | Exact paper comparison below and analytic differentiation; no existing root enclosure is presumed |
| Packing, parity deduction and corrected distinct companion | New paper predictions (A)--(E), with independent refutation attempt required for confirmation |
| Novelty | Bounded primary-source/repository search; no matching combination located, no exhaustive priority guarantee |

The 2025 Conrey--Farmer--Kwan--Lin--Turnage-Butterbaugh short-mollifier theorem
is explicitly excluded from the premises. Its high-degree derivative construction
does not automatically give simple zeros, and its localization would require a
separate analytic audit. Weighted Gram, full negative spectrum, approximation/tail
and heat-flow proposals are also excluded from this experiment's theorem.

## Method and exact computational scope

1. Use formal symbols for N,s,r,b,O,D and sigma to verify both residual identities.
   Prove atom nonnegativity for symbolic even m=2j, odd m=2j+1, and conjugate
   pairs, with the correct integer ranges; separately regress multiplicities 1--12.
2. Check a complete finite census with real-support atom counts a_1,...,a_6
   and pair counts b_1,...,b_3 independently in {0,1,2}: exactly 3^9=19,683
   count vectors, including the empty boundary case. Evaluate exact residuals
   for sigma=0,1,2. These checks diagnose transcription errors; the universal
   atom proof, not this finite bound, establishes the theorem.
3. Verify (C) with rational primal and dual witnesses for the frozen Cartesian
   grid c in {-2,-1,-1/2,0,1/2,1,2}, o in {0,1/10,1/3,1/2,1,2}. This is a
   42-case regression of a separately proved general relaxation result.
4. Preserve sharpness controls using orthogonal real feature vectors of
   multiplicity one or two, realized by the sinc kernel on distinct integers.
   Check s,r independently from 0 through 5, including the empty boundary.
   Preserve the multiplicity-three negative control to the false distinct rule.
5. Check the rational derivative comparison 1/alpha^2<4 and
   $2-1/\alpha-\alpha/4=-1801/20400<0$. The inequalities
   $\cos x\ge1-x^2/2$ and $\sin x\le x$ imply
   $c(\alpha)\le2-1/\alpha-\alpha/4<0$; $\tan x>x$ gives
   $c(1)>1/2$. Together with c'>0 these prove alpha<theta0<1
   without a numerical root computation. Verify source hashes and persist
   proof/audit status as explicit
   fields. Classical a, kappa and the new decimal exponent must remain null
   numerical fields; no numerical lower bound is fabricated from existence.

Implementation is a deterministic headless run.py using Fraction and SymPy,
with an explicit output directory, flushed stage progress, source identities,
canonical JSON and a raw stdout log. A failed check exits nonzero and writes
a failure record. Canonical artifact files are never overwritten by a rerun;
replays use fresh ignored output directories. There is no optimization or
parameter search, stochastic component, or GPU task.

## Invariant-first decision

The single distinguishing invariant is s+E-O>=0, certified per multiplicity
atom. It directly links a classical sign-change count to the already proved
spectral inequality. Finite zero lists, matrix-spectrum sampling, and large
kernel searches add no proof of this implication and are unnecessary here.

## PASS, FAIL, one-sidedness and adversarial review

A PASS of the exact computational checks establishes the recorded algebraic
identities, witness feasibility and finite controls. It alone does not prove
the all-height theorem. A confirmed verdict also requires the complete universal
paper proof, precise imported sources, correct packing and limit order, and an
independent adversarial review addressing all of them.

A genuine counterexample to an identity or claimed implication refutes that
prediction. An implementation error is diagnosed and corrected transparently;
the declaration and failed artifact are retained. A source mismatch or unsupported
analytic premise makes the affected asymptotic conclusion inconclusive even if
all finite checks pass. Known prior art changes attribution and novelty status,
not the truth value of a correct deduction.

Mandatory attacks include odd-versus-simple conflation, multiplicity versus
distinct count, a nonreal pair, the false half-sum distinct rule, endpoint
duplication, uniformity in a moving exponent, illegal support=lambda=theta,
and extraction of a numeric density/exponent from an unspecified constant.

## Budget and kill criterion

Expected exact runtime is below ten CPU seconds; the hard run budget is sixty
seconds, with per-stage and census-loop deadline checks. There is no escalation
of counts, degrees, cases, precision or time. The census emits progress at least
every 2,000 vectors and saves its next index and source identity. A budget stop
records the completed prefix and an inconclusive computation; it cannot confirm
the full census or the theorem. No run is expected to reach five minutes, so a
long-run smoke campaign is not warranted. A fresh rerun after a software fix
retains the failed output and is separately identified.

## Consequences and explicit boundaries

If confirmed, this supplies a qualitative improvement of the simple-critical
positivity range and a precise transfer inequality. It is more consequential
than another small change in the theta=3/4 example, but it does not solve RH,
give an effective starting height, prove all zeros simple, improve the global
record, or certify a decimal new exponent. Automated mathematical audits and
exact arithmetic are not peer review or an end-to-end formal proof. Publication
and replay claims must trace to the final verdict, with the classical ingredients
and dated novelty limitation visible.
