# EXP-007 adversarial validation record

Date: 2026-09-20. Declaration commit:
`a2abdcc8360399b3fa42aaea9245e4b83352c30f`. Canonical execution commit:
`d63111ffa8a348c51eb4fd06f5a1e70a51211576`. This is an internal proof,
source, and artifact audit. It is not external peer review or an end-to-end
formal verification.

## Source re-derivation

The operator step was checked against Anthropic's pinned
`Zeta23/ZeroSide/RankTraceMult.lean`. Its theorem `rank_trace_mult` is
quantified over the parameter `c`, uses

$$
g_c(x)=x^2-cx-(x-c)_+^2,
$$

and bounds the positive index of the selfadjoint remainder. The inspected
teal-sea bridge independently identifies the `c=2` eigenbasis specialization
with Ainta's spectral profile `Psi=g_2+1`. EXP-007 attributes both facts. Its
finite contribution is the pointwise comparison `Psi_t>=Psi_2` followed by
the new simultaneous retention of the defect and the odd-support parity
factor.

The short-interval transfer reuses only previously reviewed interfaces:
Wang's fixed-test pair limit, the confirmed EXP-005 odd-support lower bound,
and the EXP-003 pressure-frame defect estimate. The new manipulation was
re-derived along a subsequence realizing the lower limit of `S/N`; it does
not split a liminf of a product.

A dated search covered the current Anthropic and AxiomMath repositories,
teal-sea's current head, Ainta and pressure successors, arXiv updates through
September 20, and exact formula searches. No identical defect-parity product
or strict full-curve consequence was found. This is bounded negative evidence,
not a guarantee of priority.

## Mandatory attacks

| Possible failure | Attack and outcome |
|---|---|
| The spectral term might be an unattributed new rank-trace theorem | It is not claimed as new. `RankTraceMult.lean` supplies the arbitrary parameter, and the teal-sea bridge supplies the eigenbasis interpretation at `t=2`. |
| The affine shift from `g_t` to `Psi_t` might have the wrong coefficient | Pointwise, `Psi_t(x)=g_t(x)+(t-2)x+1`. Summing over all `S` Gram eigenvalues uses `sum lambda_j=S`, producing `sum Psi_t=sum g_t+(t-1)S`. The focused test caught and rejects the incorrect pointwise coefficient `(t-1)x`. |
| Zero Gram eigenvalues might be omitted | `Psi_t(0)=1`, so zeros cannot be discarded after the affine shift. The proof and census sum all `S` eigenvalues, including zeros. |
| `Psi_t>=Psi_2` might fail across a branch boundary | The proof separates `0<=x<=2`, `2<=x<=t`, and `x>=t`. The exact census checks 652,260 rational spectra for five values of `t`, with both equality and strict eigenvalues. |
| The remainder positive index might exceed `d=r+k` | This is the same source interface audited for EXP-006. The simple-real operator is positive, while each nonsimple real point and each conjugate pair contributes at most one positive direction to the remainder. Removing that source fact invalidates the theorem and fails closed. |
| Optimizing at `t=(N-S)/d` might leave the allowed range | Multiplicity gives `N-S>=2d`, so `t>=2`. The empty case `d=0` is handled separately. |
| Subtracting `D(G)` could reverse a product inequality | Equation (7) proves `Q-S-D(G)>=(N-S)^2/d>=0`. Multiplication uses the nonnegative factor `N-O` and `2d<=N-O`. |
| The parity factor might count mass instead of support | `O` counts distinct odd-multiplicity real support points. Writing `o=O-S` yields `N-S>=2r+o+2k`, hence exactly `2d<=N-O`. |
| The claimed constant two might admit improvement after adding the defect | A single real double point and a single real triple point both have `S=D=0` and attain equality. The universal coefficient stays sharp. |
| The pressure estimate might concern another Gram matrix | EXP-003's defect is `tr Psi_2(G)` for the same simple-real Gram matrix. EXP-007 retains exactly that `D(G)` from the finite theorem. |
| A liminf product might have been split | Along a subsequence with `S/N->s`, eventual lower bounds for `O/N` and `D/N` give eventual upper bounds for both nonnegative factors. The finite inequality is applied first; only then is the limit taken. |
| The smaller quadratic root might be the wrong branch | The strengthened quadratic opens upward, is positive at the old root `h`, and is negative at `s=1`. Since `0<h<1`, the old root lies strictly below the new smaller root and the larger root exceeds one. |
| The strict comparison might be a cancellation artifact | For the chosen pressure certificate, `alpha*h-beta=beta=dh/5>0`. On `[h,H]`, `-4<=F'<0`, so the correlated exact bound `H-h>=(1-kappa)beta/4` avoids subtracting two nearly equal independently enclosed roots. |
| The analytic energy might vanish when `R=4/h` is large | EXP-002's explicit triangle estimate is positive for every finite `R`. The canonical target proves `d>1.6416710022140455631116821409474e-64`. |
| The near-threshold gain might justify another printed decimal | It does not. The certified relative gain is only greater than `1.3732525985593292701164661575e-70`, while the independent baseline enclosure is much wider. The verdict reports a strict symbolic and correlated interval improvement, not a new decimal value for the proportion. |
| The historical pressure control might be silently cherry-picked | At `theta=3/4`, the frozen EXP-003 pressure parameters lower the coupled-product root by about `1.6909e-5`; their direct pressure-only bound remains stronger. The canonical result records this negative control. |
| Independent interval disagreement might be hidden | The first run failed because three 100-digit replay intervals slightly exceeded narrower 110-digit rational intervals near their last digit. The audit preserved the failure and changed the comparison to nonempty overlap, the correct consistency relation for two valid enclosures. Every shared interval overlaps in the final run. |
| A later runner change might be mistaken for the canonical code | The execution receipt binds the run to clean commit `d63111ffa8a348c51eb4fd06f5a1e70a51211576`, the declaration commit, the runner hash, predecessor hashes, and the result hash. |
| The result might lower the positivity onset | It does not. At `h_3=0`, the construction `R=4/h_3` is unavailable and the Gram defect may vanish. The canonical claim boundary records `onset_exponent_improved=false`. |

No fatal defect remained after these attacks.

## Computational evidence

The canonical result `artifacts/canonical/result.json` has SHA-256
`ad635c5b60c4bcae63199fb54a7979a02206ce0ee572853b2df13933dafc320c`.
It ran from a clean worktree in 94.719 seconds under the 180-second CPU budget.

The exact checks covered 652,260 rational spectral profiles and 18,479
multiplicity profiles. The latter produced 270 equality trials, 55,155 strict
trials, and four empty-dimension profiles. Directed rational arithmetic proves
at `theta=0.5459`

$$
H-h_3>
1.3732525985593292701164661575215822615\mathbin{\cdot}10^{-70}.
$$

An independent `mpmath.iv` replay at 100 decimal digits overlaps every shared
directed enclosure. Four focused tests pass. The two failed attempts are
preserved with their stage logs and failure reasons.

## Residual risks and scope

The finite theorem is a written proof assembled from attributed operator
interfaces; the new product has not been formalized in Lean. The analytic
consequence imports recent preprints and internally reviewed EXP-003/005
results. External specialists have not reviewed the result.

The source search is bounded. The improvement is asymptotic, gives no
effective starting height, does not change the onset exponent, and does not
improve the best direct pressure bound at `theta=3/4`. It is structurally
stronger than EXP-006 across the complete positive curve, but deliberately
tiny near onset with the universal analytic energy chosen here. It neither
proves RH nor changes a global zero-density record.
