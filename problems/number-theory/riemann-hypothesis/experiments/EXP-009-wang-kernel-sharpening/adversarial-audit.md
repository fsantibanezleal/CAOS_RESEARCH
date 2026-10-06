# EXP-009 adversarial audit

Audit date: 2026-09-24.  Scope: theorem algebra, equality cases, dependence on
arXiv:2609.24167v1, exact numerical consequences, and the EXP-007/008 local
coupling.  This is an internal pre-publication audit, not peer review.

## Highest-risk questions

### Is the hyperbolic change of variables onto the whole domain?

Yes.  Every nonnegative `alpha` has a unique `u=arsinh(alpha)>=0`, and the
same holds for `beta`.  No finite or infinite region is omitted.

### Is `Y` really bounded above by `X`?

Yes.  Since `|u-v|<=u+v` and `cosh` is even and increasing on the
nonnegative axis, `1<=cosh(u-v)<=cosh(u+v)`.  Equality `Y=X` means
`|u-v|=u+v`, so at least one of `u,v` is zero.

### Can the derivative change sign?

For fixed `X>1`, the quotient derivative has positive denominator and the
sign of `1+sqrt(X^2-1)-X`.  The latter is positive because
`sqrt(X^2-1)>X-1`.  At `X=1` the only feasible point is handled directly.

### Did squaring introduce a false equality or reverse an inequality?

No.  In the one-variable reduction `X>=1` and `sqrt(X^2-1)>=0`, so every
quantity squared is nonnegative.  Equality forces `X^2=2`; combined with
`Y=X`, it gives exactly `(0,1)` and `(1,0)` in the original variables.

### Does Wang's preceding argument actually preserve the full ratio?

Yes.  The source first proves
`(1-d)^2 <= d(1+d)R(alpha,beta)` and only afterward bounds the numerator of
`R` to get `R<=2`.  The new theorem replaces precisely that last inequality.
The identity for `mathcal F`, the triangle estimates, and the assumption
`alpha,beta>=0` remain unchanged.

### Is the new root the correct branch?

Yes.  Rewriting equality as
`(sqrt(2)-1)d^2+(2+sqrt(2))d-1=0` gives one negative and one positive root.
The displayed `d_dagger` is the positive root.  Directed intervals prove it
lies above both the declared `3/2` fallback constant and Wang's constant.

### Could denominator signs invalidate the interval divisions?

No.  The runner proves `sqrt(2)>1`, `d_dagger>0`, every energy denominator is
positive, `1-a_H>0`, and `C0-2/H>0` at both global values of `H`.  Each
division routine asserts its lower denominator endpoint is positive.

### Is the new global decimal merely a floating optimizer output?

No.  Floating optimization selected the nearby scale, but the final value
`H*=372019/100000` is rational and frozen.  The certificate evaluates this
single value with exact fractions and directed elementary bounds.  It also
reproduces Wang's stated rational `H0` and brackets his printed correction.
No optimality claim for `H*` is made or needed.

### Is the global comparison interval-separated?

Yes.  The lower endpoint of the new gain exceeds the upper endpoint of the
reproduced Wang gain.  Both exact intervals overlap independent 120-digit
`mpmath.iv` evaluations.

### Does triple packing survive in a short interval?

Yes, subject to the already source-pinned pair statistic and rank-six local
inputs.  Each cell discards at most two simple points, so
`J>=(S-2M)/3`.  The scaled interval length is asymptotic to its zero count;
therefore `M/N<=1/H+o(1)`.  Wang's block lemma yields
`Delta/N >= (2e/3)s - 4e/(3H)`, which is exactly
`alpha_H*s-beta_H` with `beta_H=2alpha_H/H`.

### Is the tiny local gain a subtraction artifact?

No.  The headline lower bound does not subtract two independently rounded
roots.  At the old root, the strengthened quadratic equals
`(1-k_6)(alpha_H*h_6-beta_H)>0`.  On the interval to the new root its
derivative lies between `-4` and `-2`, giving the correlated bound
`F(h_6)/4 <= J_6-h_6 <= F(h_6)/2`.  The lower endpoint is more than 37
orders of magnitude above the upper endpoint of the prior EXP-008 spectral
gain.

## Dependency and novelty boundary

- The exact ratio theorem and its equality classification are the new
  elementary contribution of EXP-009.
- The global spectral inequality, smoothing construction, block lemma, and
  cell-packing framework are attributed to Wang arXiv:2609.24167v1.
- The local pair statistic, rank-six constant, and defect-parity product are
  source-pinned through EXP-007/008.
- The Wang paper is a recent v1 preprint.  Rechecking its full operator proof
  found no algebraic break relevant to the substitution, but this audit does
  not confer peer-review status.
- The rank-six local profile remains attribution-bounded because the source
  does not print its full coefficient vector.

## Rejected stronger claims

- The computation does not establish that `H*` is the exact optimizer.
- A larger positive proportion is not density one and does not prove RH.
- The short-interval gain does not move the onset exponent.
- Neither result supplies an effective height.
- No absolute priority claim is made until independent literature review and
  public timestamping are complete.

Audit disposition: proceed to canonical execution if the runner, proof, and
tests are committed and all source hashes match.  Publish only with the claim
boundaries above and an explicit dependency on Wang v1.

