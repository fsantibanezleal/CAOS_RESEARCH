# EXP-008 adversarial validation record

Date: 2026-09-20. Declaration commit: `2297d2fc`. Canonical execution
commit: `5f4885c70188a7126f0b47ea954e589a7583b358`. This is an internal
source-interface, proof, and interval audit. It is not external peer review or
an independent reconstruction of Pearce-Crump's rank-six contraction.

## Source audit

The pinned arXiv source proves its vector-profile diagonal theorem for an
arbitrary fixed finite dimension `J`. The rank-three profile is printed in full.
The subsequent subsection states that a ten-direction, six-square profile gives

`C_6 in 0.6566338678379319741683641732 +/- 5.63e-18`.

The public TeX archive does not print the rank-six coefficient matrix. Exact web
searches through the cutoff found no separate coefficient or code release.
Accordingly, EXP-008 imports the existence, admissibility, and interval for the
six-square profile as one attributed source claim. The local theorem and all
scalar consequences are independently derived here. The verdict must fail if it
is read as an independent validation of `C_6` itself.

## Localization re-derivation

The source's vector detector is a fixed finite sum of squares. Its horizontal
argument estimate and approximate-functional-equation error apply to each
component. The diagonal theorem already packages all fixed cross terms into
`C[q]`. The arbitrary-subinterval rational-frequency estimate applies to every
fixed mixed term. After division by `H=T^theta`, each off-diagonal term is

`O_q(T^(1/2+2u-theta) log T)`.

For fixed rank there are finitely many terms, so the same exponent controls the
sum. Choosing a fixed `u<(theta-1/2)/2` makes it `o(1)`. All profile and
regularization constants are fixed before the height limit. The height limit is
taken before the endpoint regularization limit. This confirms that the EXP-005
proof is rank-independent for every fixed admissible source profile.

## Mandatory attacks

| Possible failure | Attack and outcome |
|---|---|
| The six-square constant might be a locally certified result | Rejected. The source prints an interval but not the matrix. Every EXP-008 claim labels it an attributed source-certified input. |
| A finite-rank sum might destroy the short-interval exponent | For a fixed six-component detector, summing finitely many component and cross-term bounds changes only fixed constants. The power `T^(1/2+2u-theta)` is unchanged. |
| The regularization might vary with height | The proof fixes the profile and its regularization, takes `T` to infinity, then removes regularization. No uniform-in-regularization estimate is asserted. |
| The rank-six profile might require a different mollifier length | The vector-profile theorem uses the same power-basis mollifier length. The local constraint depends on `U`, `H`, and the frequency estimate, not on the fixed vector dimension. |
| Replacing `C_3` by `C_6` might reverse a bound | The canonical exact decimals prove `C_6^+<C_3^-`. Since the odd-support lower bound is proportional to `1/C`, `k_6>k_3`. |
| The EXP-006 product might depend on detector rank | It does not. `(Q-S)(N-O)>=2(N-S)^2` is a finite multiset theorem. The detector enters only through the lower bound for `O/N`. |
| The smaller quadratic root might use the wrong branch | The normalized product gives an upward-opening quadratic. Its admissible lower endpoint is the smaller root; direct substitution reproduces formula (12) in the proof. |
| The onset might not be unique | The sign function is `F_6=c(1-k_6)+2k_6`. On `(1/2,1)`, `c'>0`, `k_6'>0`, `k_6<1`, and `c<2`, so `F_6'>0`. |
| Decimal subtraction might fake an earlier onset | No root subtraction is needed. At `theta=0.545884`, directed intervals prove the rank-three root term is negative while the rank-six term exceeds `2.5541123454645702e-7`. |
| The coarse bracket might hide a sign ambiguity | Directed exact intervals give a negative upper bound at `0.545883` and a positive lower bound at `0.545884`. A finer independent bracket gives `0.5458837<theta_6<0.5458838`. |
| The claimed shift might overlap the old onset | The same arithmetic gives `0.5458846<theta_3<0.5458847`; hence the two fine brackets are disjoint in the claimed direction. |
| The pointwise improvement might be below the declared gate | At `theta=0.5459`, directed intervals give `h_6-h_3>9.2635430617773560e-7`, exceeding the frozen `9.26e-7` gate. |
| The radius `11/5` might not yield positive spectral reserve | With `R=(11/5)/h_6`, exact algebra gives `alpha h_6-beta=2d h_6/55>0`. The canonical lower interval is `7.1526323908964106e-68`. |
| Direct subtraction of spectral roots might lose the sign | The certificate uses the correlated mean-value bound `(1-k_6)(alpha h_6-beta)/4`, whose exact lower endpoint is `1.7766622541125682e-68`. |
| The near-asymptotic radius choice might be advertised as globally optimal | It is not. `rho=11/5` is a frozen rational selected from an exploratory one-dimensional scan. The theorem needs only `rho>2`. |
| Independent arithmetic might share the directed implementation | The replay separately uses 100-decimal `mpmath.iv` transcendental functions. Every shared interval has nonempty overlap with the rational Taylor implementation. |
| A dirty worktree might contaminate the canonical result | The receipt records `tracked_clean_at_start=true` at commit `5f4885c70188a7126f0b47ea954e589a7583b358`. |
| The result might imply RH or an effective threshold | It does neither. It is an asymptotic lower-density statement conditional on the correctness of cited recent analytic preprints. |

No fatal defect remained within this scope.

## Canonical evidence

The canonical result has SHA-256
`56db06037e0b36ed519919c352fb0a5419e2b6ba29629d65948f399c1d3bf4ba`.
It passed in 64.406 seconds under a 120-second CPU budget. No GPU was justified.

The exact certificate proves

$$
0.5458837<\theta_6<0.5458838,
\qquad
0.5458846<\theta_3<0.5458847.
$$

At `theta=0.545884`,

$$
h_3<0,
\qquad
h_6>2.5541123454645702\mathbin{\cdot}10^{-7}.
$$

At `theta=0.5459`,

$$
h_6>0.0000177645181613023236390595079,
$$

and

$$
h_6-h_3>9.2635430617773560\mathbin{\cdot}10^{-7}.
$$

The optimized spectral companion further proves

$$
H_6-h_6>
1.7766622541125682\mathbin{\cdot}10^{-68}.
$$

## Residual risks

The main residual risk is the unprinted rank-six profile. The primary source's
stated existence and interval have not been independently reconstructed, so a
future coefficient release or source correction could change the numerical
onset. The localization proof itself is rank-independent and can be replayed
with any future independently reproducible constant.

The analytic inputs are recent preprints and have not received external peer
review. The source search is bounded. The result is asymptotic, has no effective
starting height, and does not address off-line zeros individually.
