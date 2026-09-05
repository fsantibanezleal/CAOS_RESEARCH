# EXP-056 verdict

Status: **P1/P2 PROVED UNIFORMLY; P3 PASSED**.

The exact original-map identity

$$M_ps_p=b_p^A+b_p^B+\gamma_p$$

holds for every `p>=8`. The source and residual both have exactly `p-1` terms, with coefficient
height at most two. The exhaustive symbolic A/B face calculation, endpoint cutoffs, and high
face signs in [proof.md](proof.md) are load-bearing; the parameter tests do not replace them.

The formula recovers half of the saved fixed-high source at `p=8,9,10`. All 93 stress parameters
`p=8,...,100` pass original-map multiplication, independently encoded gap-interval multiplication,
comparison with the frozen target formula, and deliberate sign mutation. The original `p=11`
source holdout remains unopened. The output is compact and deterministic.

The integral consequence is `[b_A+b_B]=-[gamma_p]` in the full cokernel. This turns the
quadratic-size displayed boundary into a linear-size explicit K-side target and eliminates the
need to extrapolate a 78-skeleton HNF pullback merely to represent that class.

## How could this be wrong?

Both arithmetic encodings use the persisted coefficient module, whose previous derivation is
a premise. The new proof explicitly covers all original faces and thresholds. It does not prove
that `gamma_p` is nonzero, that `2gamma_p` is a boundary for every parameter, or that the complete
relative quotient has no additional torsion. These are separate gates. The stated source identity
is not a generic source with boundary `2(b_A+b_B)` and must not be reported as one.

The next invariant-first step is EXP-057's endpoint reduction, followed by exact dual and
order-two certificates. The stronger manuscript-split gate remains unmet by this identity alone;
the published v0.23 claims and Zenodo files remain unchanged.
