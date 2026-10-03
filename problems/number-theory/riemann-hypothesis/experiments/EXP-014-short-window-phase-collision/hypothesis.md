# EXP-014: an exact off-diagonal phase-resolution obstruction

Declared 2026-10-03. Device: CPU. Exact integers and rational log bounds.
This declaration is committed before the runner or its outputs exist.

## Question and motivation

Can the uniform large-phase step used in EXP-010 Lemma 2.1 still work
beyond `nu<theta-1/2` by increasing the number of integrations by parts?
See [preflight](../../context/2026-10-03-update-and-dual-family-preflight.md),
sections 2 and 4. This concerns that proof mechanism, not the truth of the
mollified moment asymptotic.

## Frozen family and predictions

For integers `B>=2`, `a>b>=1`, put
`T=16 B^(2a)`, `M=B^b`, `r=B^(a-b)`, `h=M`, `k=M-1`,
`m=kr+1`, `n=hr+1`, and `H=B^d`. Then `H` has exponent
`theta=d/(2a)` and `M` has exponent `nu=b/(2a)` relative to `T`;
fixed factors do not change these exponents.

A. `hm-kn=1`, `h,k<=M`, and `mn<T/8` for the frozen cases.
Thus these terms are off diagonal and within the approximate-functional-
equation product scale, rather than in a rapidly decaying large-product tail.

B. The phase excursion `H log(hm/kn)` is enclosed exactly between
`H/(kn+1)` and `H/(kn)`. Its scale is `B^(d-a-b)` with multiplicative
factor tending to one as `B` tends to infinity.

C. With `(a,b,d)=(50,5,54)` the phase tends to zero
(`theta=0.54`, `nu=0.05>theta-1/2`). With `(50,4,54)` it tends to one;
with `(50,3,54)` it tends to infinity. Verify at `B=2,10,100` and
prove these limits symbolically for the entire family.

## PASS and FAIL

PASS is an explicit obstruction to a uniform pointwise large-phase
argument at or beyond the exponent threshold. It does not prove a
nonzero summed contribution, failure of a Mobius mollifier, failure of
a shorter or differently structured detector, or a barrier to RH.
`h` is a power and may have zero Mobius weight; this is deliberately a
control of the generic twisted lemma, not an assertion about the actual
signed mollifier sum. FAIL would refute the specified arithmetic family
or give inconclusive evidence on this mechanism.

## Premises and source-complete check

EXP-010's proof identifies its large-phase step; EXP-012's verdict supplies
the reciprocal-family size correction. Young's twist lemma and Tang's
Theorem 1 were read with their range conditions and final remarks.
Only exact arithmetic and `x/(1+x)<=log(1+x)<=x` for `x>=0` are needed
for the new certificate. Imported analytic theorems are not conclusions
of this experiment.

## Invariant, validation and budget

The invariant is the integer difference `hm-kn`, followed by the exponent
`d-a-b`. Use independent Bezout expansion and polynomial identity checks,
test diagonal controls and swapped twists, and stress `B=2` as well as
the scaling limit. CPU budget 30 seconds per entry point; exact integers
stay small enough, no GPU or checkpoint needed. If stopped, inconclusive.
Disposition: research-record; no new zero-proportion theorem or manuscript.
