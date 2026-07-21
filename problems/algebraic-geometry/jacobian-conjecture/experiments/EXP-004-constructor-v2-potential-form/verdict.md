# EXP-004 - Verdict: CONFIRMED (2026-07-20)

Output: `artifacts/output-2026-07-20.txt`. All five predictions verified exactly.

## Established results (ours, exact)

1. **Skew-product determinant lemma (generic).** For ANY reduced data (a1, b1, c1) polynomial in
   (v, t) (verified with fully symbolic coefficients), the lifted map
   (a1/x^2, b1/x, x c1) satisfies det JF * c1^2 = -J2 with J2 = det d(V', T')/d(v, t),
   V' = b1 c1, T' = a1 c1^2.
2. **Constructor v2.** For a seed p with p(0) = 0, integral_0^1 p = 0, p(1) != 0,
   p'(1) != 2 p(1); scale k != 0; m = -k p(1); section q(v) with q(0) = k,
   q'(0) = k (p(1) - p'(1)) / (p'(1) - 2 p(1)) and ARBITRARY higher tail:
   the potential form V' = k^2 p(w) + m s, T' = w V' - k^2 Phi(w) (w = u s / k, s = c1 = q - t)
   lifts to a polynomial Keller map on C^3 with
   **det JF = -m^2/k = -k p(1)^2, constant**, and generic fiber degree deg(p) + 1.
3. **The announced F is the minimal instance** (p = 2w - 3w^2, k = 2, q affine): reproduced
   symbolically component by component.
4. **New explicit counterexamples (with rational collision certificates):**
   - P3: seed w - 2w^3, k = 3: det = -3, degrees (12, 11, 4), fiber degree 4; the points
     (-1/15, 18, 5130) and (1/24, -18, -10368) both map exactly to (-54, -54, 1).
   - P4: seed 8w - 12w^2 + 4w^3 - 5w^4, k = 14: det = -350, degrees (17, 16, 4), fiber degree 5;
     explicit rational collision verified.
   - P5: seed 2w - 3w^2 with q-tail v^2: det = -2, degrees (8, 7, 5), fiber degree 3; explicit
     rational collision verified. The free q-tail is a generalization axis BEYOND the announced
     family shape (it changes the component-degree pattern at fixed fiber degree).
5. **Exact reconstruction inverse.** From any root w of the fiber polynomial
   k^2 Phi(w) - (w Vt - Tt): s = (Vt - k^2 p(w))/m, u = k w / s, x = C/s, v = u - 1,
   t = q(v) - s, y = v/x, z = t/x^2; verified as an identity modulo the fiber polynomial.

## Adversarial validation record

- Route 1: determinants computed BOTH directly in (x, y, z) AND via the reduced identity
  J2 = m^2 c1^2 / k; both agree for every instance.
- Route 4: the collision certificates are exact rational substitutions into the full polynomial
  components (independent of the reconstruction machinery that produced them).
- The generic lemma (prediction 1) was verified with free symbolic coefficients, not instances.

## How could this be wrong?

- The constructor's admissibility conditions were derived at the origin (weights 0 and 1); we
  verified sufficiency on 4 instances plus the symbolic lemma, but a full symbolic proof of
  sufficiency for ARBITRARY degree d is written analytically in the wiki, with the instance runs
  as certification; the general-d statement beyond tested degrees rests on that derivation.
- Fiber degree = deg p + 1 is established at a random rational target per instance (squarefree
  check included); the "generic" quantifier rests on the discriminant being a nonzero polynomial
  in the target, which follows from nonvanishing at one point.

## Consequences

- The generalization question is answered affirmatively and constructively: counterexamples come
  in an infinite family indexed by (p, k, q-tail), all fiber degrees >= 3 realized, and the
  family is strictly larger than anything announced (q-tail axis).
- det JF = -k p(1)^2 shows every negative rational is realized as a determinant (scaling); with
  p(1) fixed, det tracks k linearly: no obstruction lives in the determinant value.
- EXP-005 uses this structure to formalize why N = 2 resists the mechanism.
