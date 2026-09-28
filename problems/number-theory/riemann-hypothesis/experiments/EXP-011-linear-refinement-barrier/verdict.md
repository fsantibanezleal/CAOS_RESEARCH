# EXP-011 verdict: confirmed barrier for linear refinements

Date: 2026-09-28. Declaration `9886f07` (amended before implementation in
`136b40f`) was pushed before the runner existed. The canonical run used the
committed runner on a clean tree.

**Verdict: confirmed.** All four predictions pass with Arb ball arithmetic at
128 bits. This is a certified counterexample result for one fixed window. It
changes no zero-counting theorem and does not prove RH.

## Certified results

A. For C1 (six real triples at `+-0.949374`, `+-1.9925`, `+-3.03254` and one
simple conjugate pair at `+-0.24556 i`; `N=20`, `O=6`, `S=0`),

$$
Q=57.941781999783195766\ldots,\qquad Q-(2N+3O-4S)=-0.0582180002168042\ldots<-0.05 .
$$

So `Q>=2N+3O-4S` is false for the Montgomery-Taylor window.

B. For C2 (a lattice of 10001 cells, one triple and five simple conjugate pairs
per cell; `O=10001`, `N=130013`, `S=0`),

$$
\frac{Q-2N}{O}=2.35886369542621\ldots<2.365 .
$$

So no inequality `Q>=2N+beta O-gamma S` with `beta>=2.365` holds for this window.

C. With the EXP-010 frozen detectors admissible at `theta=0.532`
(`nu=0.0199`, `0.0299`) and `beta=2.365`,
`h_beta(0.532)=-0.00560725...` and `-0.00136485...`, both negative. With these
detectors no linear refinement with `beta<2.365` reaches `theta=0.532`.

D (controls). The EXP-006 product holds with positive certified slack on C1
(`11.18494800`) and C2 (`2.306825641e8`), and the translation-invariant
lattice formula overlaps the direct double sum at `M=50`.

## Independent audit

[`audit.py`](audit.py) evaluates C1 with the kernel computed by numerical
quadrature of its definition (not the closed form) at 30 digits
(`Q-58=-0.05821800021680423353`), C2 with a float64 closed form summed
separately (`2.3588636954262485`, relative difference below `1e-14`), and a
quadrature-kernel lattice at `M=5` against the float sum (14 digits). Audit
run 1 used `M=30` with an unsubdivided quadrature, which is inaccurate for
`|xi|` near 360; it failed that check and is kept as
[`artifacts/audit/audit-run1-failed.json`](artifacts/audit/audit-run1-failed.json).
Run 2 subdivides the quadrature and passes.

## Erratum in the declaration

The declaration states `N=110011` for C2. The correct count is
`N=13 x 10001=130013` (three copies per triple and two per pair, five pairs per
cell). The predicted inequality concerns `(Q-2N)/O` and is evaluated with the
correct `N`; the threshold and the conclusion are unaffected.

## Interpretation and disposition

The EXP-006 product is the envelope of Lamzouri's one-parameter family of
linear inequalities and is tight only for single points. A linear refinement
could improve it near the onset only with `beta>2`. For the window that
Lamzouri's argument uses, `beta` is at most `2.3589`, and the infinite-lattice
preflight suggests about `2.32`. With the single-piece detector ceiling
`kappa=0.7173 nu` (uncertified context) such a refinement could move the onset
at most from 0.53396 to about 0.5324. RH-034 is closed as a theorem target;
the result is a `research-record`. Multi-point inputs and nonlinear
refinements are not covered.

## Evidence

| Artifact | SHA-256 |
|---|---|
| Canonical result | `d53992d7b2bc7e8fade30315a5e3b69a0ef0929265f5d451a1f1d4c567822c01` |
| Audit report (run 2) | `29de599a055cc0892b771b74fc054c9db5ad16620f9cd32cf2f54321f707de15` |
