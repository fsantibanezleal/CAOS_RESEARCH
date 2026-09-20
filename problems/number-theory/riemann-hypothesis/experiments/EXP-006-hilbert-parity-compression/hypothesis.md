# EXP-006: Hilbert dimension and parity compression

Declared: 2026-09-20. Device: CPU. Baseline: latest `origin/develop` at
`4a7a08f37fcfc361285e2ceba123158cce573fdd`. Status at declaration:
primary source interfaces inspected and paper derivation proposed; canonical
implementation, exact certificate, proof review, adversarial audit, and verdict
unexecuted. The declaration commit must be pushed before any canonical run.

## Question and motivation

Can the dimension of Lamzouri's nonsimple/off-real Hilbert subspace be combined
with odd-multiplicity support to strengthen EXP-004's finite parity transfer,
and does that stronger inequality prove a positive proportion of simple
critical zeros at the previously excluded exponent
`theta=5459/10000=0.5459`?

The [source preflight](../../context/2026-09-20-hilbert-parity-compression.md)
records the proposed derivation, exact source interfaces, bounded novelty
search, and mandatory attacks. The target improves the transfer law itself. It
does not depend on a fresh mollifier optimization.

## Falsifiable finite prediction

Let `Z` be a nonempty finite multiset of complex numbers invariant under
complex conjugation. Let `N` count copies, `S` count simple real elements, and
`O` count distinct real elements of odd multiplicity. For Lamzouri's kernel
`K`, put

$$
Q=\sum_{z,w\in Z}K(z-w)^2.
$$

Predict the universal inequality

$$
\boxed{Q(N-O)\ge 2(N-S)^2.} \tag{A}
$$

The proof must cover `N=O` and an empty first Hilbert range explicitly. A
finite census can refute (A), but cannot prove universality.

## Falsifiable analytic prediction

For fixed `1/2<theta<1`, define

$$
c(\theta)=2-\frac\theta2-
\frac1{\sqrt2}\cot\!\left(\frac\theta{\sqrt2}\right),
\qquad
k_3(\theta)=\frac{\theta-1/2}{4eC_3},
$$

where `C_3` is Pearce-Crump's printed and reproducible rank-three constant.
Predict that (A), Wang's short-interval pair theorem, and EXP-005 imply

$$
\liminf_{T\to\infty}\frac{S(T,T^\theta)}{N(T,T^\theta)}
\ge
\max\left\{0,c(\theta),
\frac{c(\theta)+2k_3(\theta)}3,
1-\sqrt{\frac{(2-c(\theta))(1-k_3(\theta))}{2}}
\right\}. \tag{B}
$$

At the frozen point `theta=5459/10000`, predict that the last term is
strictly positive and has a conservative rational lower bound of at least
`1/100000`. The canonical run must also certify that the EXP-005 linear parity
term is negative there. This separates a genuine transfer improvement from a
recalculation of the earlier curve.

Predict further that the unique root of

$$
c(\theta)+(2-c(\theta))k_3(\theta)=0 \tag{C}
$$

lies in the frozen broad bracket

$$
0.5458<\theta_{\rm HP}<0.5459.
$$

A provisional estimate based only on the already committed EXP-005 endpoint
enclosures selected these targets before declaration. It is not canonical
evidence and cannot satisfy PASS.

## Paper proof to adjudicate

In Lamzouri's notation, let `d=r+k` be the dimension of the first nested
Hilbert subspace. The proof review must verify each implication:

1. Bessel's inequality gives `Q >= sum alpha_j^2`;
2. the first-range coefficients are real and satisfy
   `sum_{j<=d} alpha_j >= N-S`;
3. for `d>0`, Cauchy-Schwarz gives
   `sum_{j<=d} alpha_j^2 >= (N-S)^2/d`;
4. multiplicity and parity give `2d <= N-O`;
5. these estimates yield (A), with a separate valid argument when `d=0`;
6. normalization by `N^2`, not by `N`, produces the correct finite ratio;
7. Wang's fixed-test limit is taken before smoothing and bandwidth limits;
8. the EXP-005 odd-support lower bound can be inserted with the correct
   liminf direction; and
9. the square-root lower bound is used only in the regime in which its right
   side is nonnegative.

Any missing implication makes the analytic prediction inconclusive even if
the numeric target passes.

## Audit strengthening after the declared prediction

The post-run consistency audit recovered the nonnegative simple-real term
already present in Lamzouri's arbitrary-parameter inequality. It strengthens
the declared finite target (A) to

$$
\boxed{(Q-S)(N-O)\ge 2(N-S)^2.} \tag{A+}
$$

This was not used to select the frozen exponent or root bracket. It leaves the
positivity condition (C) unchanged, but replaces the square-root term in (B)
by the smaller root of

$$
2(1-s)^2=(1-k_3(\theta))(2-c(\theta)-s).
$$

The earlier passed artifact must be retained as superseded evidence. A new
clean-commit canonical run, universal proof revision, and independent interval
replay are required before (A+) or its stronger numerical bound can pass.

## Exact computational scope

After this declaration is committed and pushed, implement deterministic
`run.py` with no network access. It will:

1. verify pinned source and predecessor artifact hashes;
2. enumerate conjugation-invariant atom profiles through a declared small
   multiplicity/support cap and check the algebraic dimension and parity
   inequalities, preserving equality and near-equality cases;
3. use exact rational arithmetic to verify the aggregate implications behind
   (A), including all zero-denominator branches;
4. parse the frozen interval for `C_3` and independently enclose `e`, `sqrt(2)`,
   `sin`, and `cos` by directed rational series;
5. certify the signs of the new and old transfer expressions at
   `theta=5459/10000`;
6. certify the bracket in (C) and monotonicity on that bracket;
7. cross-check all transcendental intervals with an independent high-precision
   implementation; and
8. emit canonical JSON, raw stdout, checkpoints, hashes, and an execution
   receipt without overwriting prior experiments.

The computation must also evaluate Pearce-Crump's printed rank-six constant as
a sensitivity control. Because its profile is not printed, that control is
source-attributed and cannot become the canonical premise of (B).

## Complementary lens and barrier check

As a separate exact linear-program check, include all four finite conclusions
stated in Lamzouri's Proposition 2.1 together with the EXP-004 scalar
constraints. Determine whether any of those published scalar inequalities
alone improves the minimum `S` near the new threshold. If they do not, retain
a dual certificate showing that the new gain comes from the uncompressed
first-subspace dimension, not from recombining already stated headline bounds.

## PASS, FAIL, and one-sidedness

PASS requires the universal paper proof of (A), a complete analytic transfer
to (B), the frozen exact numeric target, a valid monotonic root bracket, and an
adversarial review. A finite census or floating optimizer alone cannot confirm
the result.

A counterexample to (A), an invalid source interface, a failed limit passage,
or a nonpositive exact bound at `theta=0.5459` refutes the corresponding
prediction. Failure of the rank-six sensitivity control does not affect the
rank-three theorem. Finding prior art changes the novelty assessment without
changing a valid deduction.

## Budget and stop rule

The exact census and interval certificate have a hard CPU budget of 120
seconds. The scalar linear program has a further 60-second budget. Progress and
checkpoint output must be flushed after source validation and after each
stage. A timeout is inconclusive and retains the completed prefix. There is no
GPU allocation, stochastic search, profile optimization, or automatic budget
extension in this experiment.

## Consequences and boundaries

If confirmed, EXP-006 supplies a new parity-sensitive finite Hilbert inequality
and lowers the explicit power-interval threshold below `0.5459` using the same
reproducible analytic inputs as EXP-005. It does not solve RH, improve the
global 67.25 percent record, give an effective onset height, establish
uniformity as `theta` varies with `T`, or constitute external peer review.
