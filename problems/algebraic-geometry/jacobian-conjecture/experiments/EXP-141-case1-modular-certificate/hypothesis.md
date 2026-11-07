# EXP-141 preflight: a multi-modular cofactor certificate that Case 1 is empty (JCB-103, fallback of EXP-140)

Date: 2026-11-07. Status: frozen before the production computation. CPU only.

## Why

EXP-139 (degree-35 field) and EXP-140 (quintic subfield L) asked Singular for an exact standard basis over Q;
both stopped at their 6-hour caps. Over F_p the same ideals are easy, so the obstacle is coefficient size only.
Facts measured before this file (sizing probes, not results):

1. PARI `polredabs(h, 1)` on EXP-140's quintic h(v) gives P(y) = y^5 - y^4 + 3y^3 + 3y^2 + 26 and
   v = A(y) mod P(y), A(y) = -9725570295901/12623962 - (1170753213563/971074) y - (387111042229/12623962) y^2
   + (1578225240619/12623962) y^3 - (469713794365/6311981) y^4. Field discriminant 3065712 = 2^4 3 13 17^3.
2. Rewritten in the basis 1, y, ..., y^4 and made primitive over Z, the 13 equations E'_e have integer coordinates
   of 35 to 552 digits (10 to 591 digits for the numerators and denominators before).
3. At F_1021, with v replaced by a simple root of h, Singular `lift` writes 1 as a combination of the 13
   equations in 3 seconds: 11,714 cofactor terms in all, total degree at most 12, three cofactors zero. With v
   kept as a variable (ideal with h(v)) the same `lift` over F_32003 did not finish in 600 seconds.

## Method

1. **Field [D].** L = Q[y]/(P). Check exactly that P is irreducible over Q and that h(A(y)) = 0 mod P; then
   v -> A(y) is an isomorphism Q[v]/(h) -> L (both fields have degree 5). Let E''_e be E'_e with v -> A(y),
   reduced mod P and multiplied by a nonzero rational making its coordinates coprime integers. By EXP-140's
   reduction [D], Case 1 is empty iff (E''_1, ..., E''_13) is the unit ideal of L[q0, ..., q5].
2. **Modular cofactors.** For primes p in [2^30, 2^31) at which P has five distinct roots r_1..r_5 mod p: at each
   root, Singular (option redSB, ordering dp) computes `lift` of (E''_e(r_k) mod p) to 1. A prime is kept only if,
   at all five roots, the set of (cofactor, monomial) pairs with a nonzero coefficient is a subset of the
   reference support of the first kept prime, with the same per-cofactor term counts at the majority of roots;
   other primes are discarded as unlucky and counted. For each (cofactor, monomial) the five values are
   interpolated (Vandermonde in r_k) into the five coordinates in the basis 1, y, ..., y^4 mod p.
3. **Reconstruction.** Chinese remaindering over the kept primes and rational reconstruction (FLINT
   `fmpq_reconstruct_fmpz`) of every coordinate, at checkpoints. A checkpoint passes when every coordinate
   reconstructs and the reconstructed value agrees modulo three further kept primes not used in it.
4. **Exact verification [D].** With the reconstructed rational cofactors g_e, compute sum_e g_e E''_e in
   Q[q0..q5, y] exactly and reduce modulo P(y): the certificate holds iff the result is exactly 1. This identity is
   the proof; steps 2 and 3 only find a candidate, and no assumption about lucky primes enters the conclusion.
   A second exact check runs the same identity in Singular over the extension field (minpoly P).

## Gates (before production)

1. Field: P irreducible over Q; h(A(y)) = 0 mod P; at each of EXP-140's five gate primes the specialised E''
   (at a root of P) reproduce the unit result, and the first four equations alone stay non-unit of dimension 4.
2. Pipeline on a planted example: a small system with a known rational certificate (a random combination of
   three polynomials over L forced to equal 1) is recovered and verified exactly by the same code.
3. The interpolation and CRT code is checked on random vectors against direct computation.

## Prediction

The certificate is found and the exact identity holds (MODERATE: the heights of the cofactors are unknown and
could exceed the budget).

## Budget and stop condition

At most 12 hours of wall-clock time on up to 24 parallel processes and at most 6,000 kept primes. If no checkpoint
passes within that, record UNKNOWN with the measured heights; the next step would rescale q0..q5 (the
coefficients carry consistent powers of 2, 3, 13, 17 and 257 per monomial) before a new attempt. If a checkpoint
passes but the exact identity fails, record the failure, do not claim the result, and recheck the support rule.

## What a CONFIRMED verdict claims

Case 1 of GGHV Proposition 4.3 at (72,108), as encoded by our 13 compatibility equations (EXP-137), has no
solution over the algebraic closure, with an exact certificate checked twice. It claims nothing beyond Case 1 and
inherits EXP-137's encoding and EXP-140's reduction.
