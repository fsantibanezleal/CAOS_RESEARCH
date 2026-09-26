# EXP-009 verdict: confirmed sharp kernel ratio and proportion improvement

Date: 2026-09-24.  The original target was declared at
`123eee0d49969226201e68d6c32746087a91e6fc`, strengthened before downstream
calculation at `edd689fef41ee5986353f6b62e8c34f81d55ae0f`, and executed from
clean commit `6b8e009c73f87047a2bc2c237991d241bd3b08c0`.

**Verdict: confirmed relative to Wang's source-pinned analytic framework.**
The sharp auxiliary ratio theorem is an exact elementary result.  Its global
and short-interval consequences pass directed arithmetic, independent
120-digit interval replay, and internal adversarial review.  Wang's
arXiv:2609.24167v1 is a recent unreviewed preprint, so the external theorem
status remains attribution-bounded.

## Confirmed sharp theorem

For every `alpha,beta>=0`,

$$
 \frac{\sqrt{(1+\alpha^2)(1+\beta^2)}
 +\alpha\sqrt{1+\alpha^2}+\beta\sqrt{1+\beta^2}}
 {1+\alpha^2+\alpha\beta+\beta^2}
 \le\sqrt2,
$$

with equality exactly at `(0,1)` and `(1,0)`.  The hyperbolic substitution in
`mathematical-proof.md` reduces the statement to `(X^2-2)^2>=0`; it covers the
full unbounded quadrant and needs no numerical boxes.

The corresponding three-point kernel constant is

$$
 d_\dagger=
 \frac{\sqrt{2+8\sqrt2}-(2+\sqrt2)}{2(\sqrt2-1)}
 =0.2831654308085373270052981480781329\ldots,
$$

which is strictly larger than both the declared `3/2` fallback root and
Wang's `sqrt(5)-2`.

## Confirmed global consequence

Substitution into Wang's spectral-defect and triple-packing proof, at the
frozen rational cell length `H=372019/100000`, gives

$$
 \boxed{
 \liminf_{T\to\infty}\frac{N_0^s(T)}{N(T)}
 \ge0.6725007995946757558283550562963947\ldots .}
$$

The companion distinct-zero proportion is

$$
 \boxed{
 \liminf_{T\to\infty}\frac{N_d(T)}{N(T)}
 \ge0.8362503997973378779141775281481973\ldots .}
$$

The new correction above
`C0=0.6725007036794116457343797908032951...` is

$$
 9.5915264110093975265493099597924\times10^{-8}.
$$

The runner independently reproduces Wang's correction as
`6.6662458333412524952...e-8`; the new lower interval endpoint exceeds its
upper endpoint.  The correction is about 43.88 percent larger.

## Confirmed short-interval consequence

At `theta=0.5459` and the frozen integer cell length `H=140730`, the
EXP-007/008 defect-parity interface gives a strict addition to the rank-six
curve:

$$
 J_6-h_6>
 3.08678099833341875132438420197419\times10^{-31}.
$$

This exceeds the EXP-008 spectral lower gain by more than 37 orders of
magnitude.  It remains numerically tiny and does not move the rank-six onset.

## Evidence and replay

The canonical result is `artifacts/canonical/result.json`, schema
`riemann-exp009-results-v1`, SHA-256
`0cea78e847d1bcec62eb8cd809b704ceaebd58f78f1c405f13ec40838fbb5a66`.
It records PASS from a clean commit in 37.157 seconds on CPU.  Its execution
receipt binds the result and runner hashes.

Replay from the repository root:

```text
python problems/number-theory/riemann-hypothesis/experiments/EXP-009-wang-kernel-sharpening/run.py --output-dir tmp/riemann-exp009-replay --budget-seconds 600
python -m pytest -q tests/test_riemann_wang_kernel_sharpening.py
```

## Manuscript decision and scope

Prepare a separate concise manuscript.  The main global theorem, proof method,
and source dependency differ from the existing short-interval manuscript;
folding it into that 30-page work would obscure both results.  The local
corollary should be stated briefly and cross-referenced to the existing
defect-parity paper.

This result does not prove the Riemann hypothesis, density one, universal
simplicity, or an effective starting height.  No peer-review status or
absolute novelty priority is claimed.

