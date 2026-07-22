# EXP-014 - Puiseux escape obstructions: the properness instrument (first contact)

- **Question.** JCB-022 (queued since session 5, slot reserved). Build the exact
  instrument that decides non-properness (escape at infinity) for planar polynomial
  pairs, certify the library, and state the reduction that makes it a JC(2) route.
- **Motivation (derivation, declared).** A planar Keller map that is PROPER is a covering
  of the simply connected C^2, hence invertible (classical). So JC(2) is EXACTLY the
  statement that no planar Keller map has a nonempty asymptotic (Jelonek) set: escape
  branches (Puiseux curves to infinity with bounded image) are the only way a
  counterexample can exist, mirroring the 3D mechanism we own exactly (EXP-007: escape
  iff multiple fiber root). The computable handle: for F = (P, Q), the x-leading (resp.
  y-leading) coefficient of Res_y(P - u, Q - v) (resp. Res_x) is a polynomial in (u, v)
  whose non-vanishing certifies properness over that chart; for automorphisms it must be
  a nonzero constant.
- **Falsifiable predictions.**
  1. [MV] (Properness certificates) For every library pair, the leading coefficients of
     both resultants are nonzero CONSTANTS: exact properness certificates for all 8
     automorphisms.
  2. [MV] (Non-proper control) F = (xy, y): the instrument returns leading coefficient v
     (up to sign/scalar), i.e. the asymptotic set lies in {v = 0}, matching the exact
     fiber analysis (fiber over (u, 0) empty for u != 0: escape along y -> 0, x -> inf).
  3. [MV] (Proper non-injective control) F = (x^2, y) passes the properness certificate
     while being non-injective: properness and injectivity separate without the Keller
     hypothesis (the Keller condition is what upgrades proper to invertible).
  4. [C] (The route statement) JC(2) <=> every planar Keller map has empty Jelonek set.
     For the excluded shapes (Theorems 1-4), escape structure is the dual picture of the
     staircase: on the controls, the asymptotic locus direction aligns with a Newton
     edge direction of the components (observation recorded, not a theorem).
- **Method.** sympy resultants over QQ[u, v]; Poly leading coefficients; exact fiber
  checks on the controls. Caps 570 s.
- **Success criterion.** 1-3 verified; 4 recorded; the certificate function becomes a
  library instrument for any future candidate completion.
- **Failure criterion.** A library pair failing the certificate (instrument wrong: an
  automorphism is proper); a control giving a constant leading coefficient (instrument
  blind).

Declared 2026-07-22 before the run. (Slot note: EXP-014 was reserved for this topic in
session 5 and is filled now; experiments 015..040 predate it chronologically.)
