# EXP-012: a longer short-window mollifier through Tang-Khan reciprocity

Declared: 2026-09-28. Device: analysis first, CPU certification afterwards.
Baseline: branch `task/riemann-strategy-review` after the EXP-011 records.

Status at declaration: analytic experiment in flight. The route preflights
(section RH-027 of [`context/2026-09-27-route-preflights.md`](../../context/2026-09-27-route-preflights.md))
reduced RH-027 to the statements below and priced them with scratch values
(onset about `0.5307` for target A'). No proof, runner or canonical artifact
exists. This declaration fixes the statements and the proof plan before any
proof is written, so that a partial or failed attempt is recorded against a
fixed target.

## Question

EXP-010 proves the localized Levinson-Conrey moment for `nu<theta-1/2` because
Young's off-diagonal condition `hk<=Delta^2 T^(-1-eps)` is a product condition.
Tang (arXiv:2608.14852v1, Theorem 1) evaluates the short-window twisted second
moment for prime twists `p,q` under `H^2/max{p,q}>T^(1+eps)`, a condition on the
larger twist, at the price of a dual moment of Dirichlet `L`-functions on a
range of length about `T/H`. Can this give the EXP-010 moment (A) for
`nu<(2/3)(2theta-1)`, and hence a lower simple-critical onset?

## Predictions

A (general twists and shifts). For fixed `1/2<theta<1`, `H=T^theta`, coprime
`h,k<=T^nu`, and shifts `|alpha|,|beta|<<1/L`,

$$
\int\Bigl(\frac hk\Bigr)^{it}\zeta(\tfrac12+\alpha+it)\zeta(\tfrac12+\beta-it)
e^{-(t-T)^2/H^2}\,dt=\mathcal M_{h,k}(\alpha,\beta)+\mathcal D_{h,k}(\alpha,\beta)
+O\Bigl(T^{\epsilon}\frac TH\Bigl(\sqrt{\tfrac hk}+\sqrt{\tfrac kh}\Bigr)\Bigr),
$$

where `M` is the diagonal main term of Conrey type and `D` is a dual sum of
`|L(1/2+it,chi)|^2`-type moments over characters modulo `h` and `k` on a range of
length about `T/H`, uniformly in the shifts.

B (summed dual moments, trivial bound). With `a_h=mu(h)h^(-1/2)P[h]`,
`sum_{h,k<=T^nu} a_h a_k D_{h,k}<<T^eps (T/H) T^(3nu/2)`.

C (the moment and the onset). A and B give the EXP-010 moment (A) for every
`nu<(2/3)(2theta-1)`. With certified detector constants at new frozen `nu`,
EXP-010's Prediction B and the EXP-006 product then give a positive proportion
of simple critical zeros for every fixed `theta` above a certified onset below
`0.534`; the scratch value is about `0.5307`.

## Proof plan (fixed before writing)

1. Rederive Tang's Theorem 1 for general coprime `h,k`, replacing the character
   decomposition modulo a prime by the full decomposition modulo `h` (and `k`),
   following Tang's Section 3 (Fourier expansion (fourier1)-(F2), the
   restriction lemmas `bound`, `bound2`, the Taylor step `a1`, the Mellin lemmas
   `mellininversion`, `mellin2`, `weight`, and the residue and epsilon lemmas).
   Khan's global relation (Proc. Amer. Math. Soc. 153 (2025), DOI
   10.1090/proc/17003) and the Bettin-Conrey cotangent-sum reciprocity are the
   global templates.
2. Insert shifts `alpha,beta` and check that every error term is uniform in
   `|alpha|,|beta|<<1/L`; the main term must match the Conrey-Young form used by
   EXP-010.
3. Bound `D` trivially by orthogonality of characters on a range of length
   `T/H`, and sum over `h,k` with the mollifier weights (Prediction B).
4. Assemble the moment (A) and run the EXP-010 counting argument unchanged.
5. Certify detector constants at frozen `nu` values in `(theta-1/2,(2/3)(2theta-1))`
   with the EXP-010 exact routine, and the onset by directed arithmetic.

## What PASS and FAIL prove

PASS requires complete written proofs of A and B surviving an adversarial
review, and certified C. It proves a lower every-interval simple-critical
onset. A failure of step 1 or 2 is recorded with its obstruction (for example a
non-negligible dual main term); certified numbers without the proofs are
supporting evidence only.

## Stop rules

A time-boxed attempt: if step 1 or 2 exposes a dual main term of size
comparable to `H`, or a loss of uniformity in the shifts that the trivial bound
cannot absorb, the attempt stops and the obstruction is recorded as the result.
