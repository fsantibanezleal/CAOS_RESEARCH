# EXP-009: Wang kernel sharpening and parity transfer

Declared: 2026-09-24. Device: CPU. Baseline: public `develop` commit
`07373317d188bc4f8536afe1d5a2c6a91018751c` and release `v0.72.000`.

Status at declaration: Wang arXiv:2609.24167v1 has been archived and read;
no optimization runner, interval certificate, or result has been implemented or
executed. This declaration must be committed before computation.

## New source and question

Wang's September 21 preprint proves the first stated global improvement over
the Montgomery--Taylor/Alpoge--Furman constant. Its finite defect
`Delta_K=tr Psi(G_K)` overlaps the spectral term retained independently in
EXP-007, while its explicit three-point kernel lemma is new to the CAOS source
baseline.

The source bounds an auxiliary ratio

$$
R(alpha,beta)=\frac{\sqrt{(1+alpha^2)(1+beta^2)}
+alpha\sqrt{1+alpha^2}+beta\sqrt{1+beta^2}}
{1+alpha^2+alpha beta+beta^2}
$$

by `2`. This gives `d >= sqrt(5)-2` and the kernel energy

$$
e(H)=\frac{(\sqrt5-2)^2}{(1+2\pi^2H^2)^2}.
$$

EXP-009 asks whether the ratio bound can be sharpened rigorously and whether
the resulting three-point energy improves both Wang's global proportion and
the EXP-007/008 short-interval parity product.

## Prediction A: sharpen the auxiliary ratio

Prove for all `alpha,beta >= 0` that

$$
\boxed{R(alpha,beta)\le\frac32.}
\tag{A}
$$

The proof may be symbolic or a finite exact/Arb interval certificate after a
compactification with separately proved boundary estimates. A grid or floating
optimizer is discovery evidence only.

If (A) holds, Wang's derivation gives

$$
(1-d)^2\le\frac32d(1+d),
\qquad
\boxed{d\ge d_*:=\frac{\sqrt{57}-7}{2}>\sqrt5-2.}
\tag{B}
$$

Hence every three-point block of span at most `H` has energy at least

$$
\boxed{e_*(H)=\frac{d_*^2}{(1+2\pi^2H^2)^2}.}
\tag{C}
$$

## Prediction B: new global proportion

Let

$$
a_*(H)=\frac{2e_*(H)}3,
\qquad
u_*(H)=\frac{C_0-2a_*(H)/H}{1-a_*(H)}.
$$

Use a directed global search followed by an exact rational interval proof on a
frozen interval for `H` to certify some explicit `H_*` with

$$
\boxed{\nu_*(H_*)>C_0+\delta_0,}
\tag{D}
$$

where `delta_0` is Wang's printed improvement. The final claim will use a
rationally rounded value of `H_*` and a downward-rounded proportion. A merely
better floating value does not pass.

The distinct-zero companion is `(1+nu_*(H_*))/2` by the same finite argument.

## Prediction C: stronger short-interval spectral-parity curve

For each fixed `theta` where the EXP-008 rank-six Hilbert-parity term
`h_6(theta)` is positive, take any fixed `H>2/h_6(theta)`, put

$$
alpha_H=\frac{2e_*(H)}3,
\qquad beta_H=\frac{2alpha_H}{H},
$$

and let `J_6(theta,H)` be the smaller root of

$$
2(1-s)^2=(1-k_6(theta))
\{q(theta)+beta_H-(1+alpha_H)s\}.
\tag{E}
$$

Then EXP-007's finite defect-parity product predicts

$$
\boxed{J_6(theta,H)>h_6(theta).}
\tag{F}
$$

At the frozen point `theta=0.5459`, optimize only over a declared compact
interval derived from the scale `H=x/h_6`, certify the selected rational `H`,
and prove that the resulting gain is strictly larger than the v0.07 spectral
gain `1.7766622541125682978e-68`.

This branch is expected to improve the positive curve but not its onset,
because the cell condition requires an already positive simple-zero term.

## Required checks

1. Reproduce Wang's `C0`, `H0`, `a0`, and `delta0` with directed arithmetic.
2. Check every inequality in the proof of (A), including axes, infinity, and
   all compactified cells; record unresolved boxes and subdivision depth.
3. Derive (B) without decimal substitution and verify `d_*>sqrt(5)-2` exactly.
4. Optimize the global `H` only for discovery, freeze a rational candidate,
   then certify (D) with outward intervals.
5. Re-derive the triple packing count in a short interval and combine it with
   EXP-007 before taking limits.
6. Certify the pointwise short-interval gain and replay all transcendental
   signs independently at at least 100 decimal digits.
7. Bind source, declaration, runner, proof, audit, and output hashes in the
   canonical result.

## Budget and stop rules

The declared run is CPU-only and capped at 600 seconds per canonical attempt.
A GPU is unjustified unless tensor or interval batches exceed that budget and a
separate exact validation path exists. The result is refuted if (A) has a
counterexample. It is inconclusive if any compactification boundary, interval
box, or downstream sign remains unresolved. In either case, preserve the
attempt and do not weaken `3/2` without a new committed amendment.

## Attribution and claim boundary

Wang owns the published global spectral-defect/triple-packing framework and
the `R<=2` proof. EXP-007 predates this source in the CAOS history but absolute
priority for the defect term is not claimed. The scoped candidate contribution
is the sharper ratio theorem (A), its global quantitative consequence (D), and
its coupling to the EXP-007 parity product in (E)--(F).

No effective height, density-one theorem, universal simplicity, peer-review
status, or proof of the Riemann hypothesis is predicted.
