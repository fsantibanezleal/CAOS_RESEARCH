# EXP-006 adversarial validation record

Date: 2026-09-20. Declaration commit:
`b1febcf8a6d5830218e1df386af1e8a92c3037be`. Strengthening and canonical
execution commit: `0d736fa22ce7e833200381a32e8cc89f77c660e8`. This is an
internal proof and artifact audit, not external peer review or formal
verification.

## Primary-source re-derivation

The finite proof was checked line by line against Proposition 2.1 of
Lamzouri, arXiv:2609.02882v2. The inspected interfaces were the kernel
factorization, second-moment identity, real Gram-Schmidt coefficients, exact
range dimensions, Bessel inequality, coefficient-sum bounds, and the
nonpositive last range.

The consistency audit also checked the repository's earlier multiplicity
route and Anthropic's archived `RankTraceMult.lean`. That route already
contains the arbitrary-parameter Hilbert inequality used in equation (5) of
the proof. Restoring its simple-real term strengthens the declared target from
`Q(N-O)>=2(N-S)^2` to
`(Q-S)(N-O)>=2(N-S)^2`. The earlier passed runs are retained under the two
superseded artifact directories; the strengthened runner and certificate were
then committed and executed from a clean revision.

The short-interval transfer was checked against Wang, arXiv:2609.07918v1,
including the scaled zero multiset, rational-weight removal, fixed-test error
`O_f(H+T^lambda log^2 T)`, Riemann-von Mangoldt normalization, cosine
optimization, smoothing, and the strict bandwidth order `lambda<theta`.
EXP-005 supplies the odd-support density independently of the pair test.

The archived AxiomMath pull-request snapshot was searched for the new parity
quantity and product inequality. It formalizes Lamzouri's four stated finite
conclusions, but the inspected snapshot does not state the strengthened
product. The four archived successor repositories and dated online results
were searched for the same formula; no match was found. This is useful
negative search evidence, not a proof of priority.

## Mandatory attacks

| Possible failure | Attack and outcome |
|---|---|
| The pair sum might be complex or signed | Conjugation invariance changes the complete sum to Lamzouri's tensor norm `integral |F|^2`. Thus `Q` is real and nonnegative before any scalar inequality is used. |
| The coefficients might be complex | Lamzouri proves the structured spanning functions have real inner products, so ordinary Gram-Schmidt uses real coefficients and every `alpha_j` is real. |
| The first subspace might have dimension below `r+k` | Linear independence of distinct exponentials on the positive-measure support of `eta` gives `D_U=r+k` exactly. The argument fails closed if that source step is removed. |
| The arbitrary-parameter inequality might have the wrong middle coefficient | Summing `x^2>=2tx-t^2` on the first range, `x^2>=2x-1` on the middle range, and `x^2>=2tx` on the nonpositive last range gives `Q>=2tN-(2t-2)A_M-S-t^2d`. Since `A_M<=S` and `t>=1`, this is `Q>=2tN-(2t-1)S-t^2d`. |
| The optimizing value of `t` might be inadmissible | Multiplicity gives `N-S>=2d`, so `t=(N-S)/d>=2`. This lies inside the attributed range `t>=1`. |
| The empty first range causes division by zero | When `d=0`, there are no nonsimple real or nonreal support points. Then `N=S=O`, and (1) reads `0>=0`. The code tests this branch separately. |
| `O` was confused with odd multiplicity mass | `O` counts support points. Writing `o=O-S`, each odd nonsimple point costs one copy beyond the two-copy floor, which gives `N-S>=2d+o` and exactly `2d<=N-O`. |
| A higher odd multiplicity breaks the count | Multiplicity `2j+1>=5` adds residual mass and makes the dimension inequality strict. The exact census includes real multiplicities through seven. |
| The factor two might be reversed | From `2d<=N-O`, one has `1/d>=2/(N-O)`. Multiplying the nonnegative quantity `Q-S` by `N-O` gives the displayed direction. |
| The retained `S` might be subtracted without support | Equation (6) proves `Q-S>=(N-S)^2/d`. The original weaker run omitted this nonnegative term; the amended proof and runner preserve it. |
| The finite normalization might use `N` instead of `N^2` | Dividing `(Q-S)(N-O)>=2(N-S)^2` by `N^2` gives `(Q/N-S/N)(1-O/N)>=2(1-S/N)^2`. The runner and proof use this form. |
| A liminf product was split illegally | No product liminf identity is used. For each epsilon, Wang gives an eventual upper bound for `q_T`, while EXP-005 gives an eventual lower bound for `o_T`; these are inserted pointwise before epsilon tends to zero. |
| Replacing `q_T-s_T` by an upper bound could reverse sign | The finite inequality makes `q_T-s_T` nonnegative unless every point is simple, which is already a success case. The eventual upper bound `C(f)+epsilon-s_T` is therefore nonnegative too. |
| The wrong quadratic root might be used | The quadratic is positive at values below its smaller root and has leading coefficient two. Since `0<=s_T<=1`, the pointwise inequality forces `s_T` above the smaller root in the near-threshold regime. Exact substitution and the independent interval replay use the same branch. |
| The odd-support theorem might use another interval convention | EXP-005 and Wang both use the same fixed power interval after negligible endpoint adjustment. Both denominators count zero copies. |
| Smoothing might depend on height | The order is fixed smooth test, height limit, smooth approximation to the cosine density, then `lambda` increasing to `theta`. No test function or bandwidth moves with `T`. |
| The new positive value could come from the rank-six constant | The canonical theorem uses only the fully printed rank-three `C_3`. Rank six is labeled source-only sensitivity and excluded from the premise. |
| The result might be a recombination of published scalar headlines | The exact triple/double witness satisfies every applicable published scalar inequality with `S=0` at `theta=0.5459`. The product inequality rejects it at Wang's actual pair level because it retains `d=r+k`. |
| The root might be a floating-point artifact | Directed rational Taylor bounds prove opposite signs at `0.545884` and `0.545885`. Symbolic differentiation proves strict monotonicity. An independent 100-digit interval calculation is contained in the rational enclosures. |
| The finite inequality might have a larger universal coefficient | Real points of multiplicity two and three give exact equality, so the coefficient two is globally sharp. |

No fatal defect remained after these attacks.

## Computational evidence

The canonical result
`artifacts/canonical/result.json` has SHA-256
`82c4761b5c97011ff86cdd379d647ad0f94643a7eb8324a4a09aa37f58848bbf`.
It started from clean commit
`0d736fa22ce7e833200381a32e8cc89f77c660e8`, completed in 0.953 seconds,
and passed every declared control.

The exact census checked 18,479 atom profiles: 135 equality cases, 18,340
strict positive-dimension cases, and four empty-dimension cases. The census is
diagnostic and does not prove universality. The paper proof does.

The numeric certificate uses exact fractions, directed Taylor enclosures for
`e`, `sqrt(2)`, sine, and cosine, an exact rational square-root enclosure, and
an independent `mpmath.iv` calculation at 100 decimal digits. It proves at
`theta=0.5459` that the strengthened lower bound exceeds
`0.0000168381638551244569880374399`; the earlier valid but weaker bound exceeds
`0.0000126556179972388281537305037`. It also retains the broad-bracket and
weaker-transfer runs as superseded evidence.

Seven focused EXP-006 tests and the combined 48-test EXP-004/005/006 suite
pass. Ruff reports no violations in the runner or focused test.

## Residual risks and scope

The theorem imports recent preprint inputs from Lamzouri, Wang, and
Pearce-Crump, plus the internally reviewed EXP-005 localization. Their exact
interfaces were re-derived, but the entire analytic literature was not
formalized end to end. The AxiomMath snapshot does not formalize the new
finite product. A later correction to an imported theorem can affect the
short-interval consequence without invalidating the elementary finite proof.

The prior-art search is bounded. The result is asymptotic, supplies no
effective starting height, and proves only a positive proportion in fixed
power intervals. It does not establish the Riemann hypothesis or external
peer acceptance.
