# EXP-041 - The explicit symmetric/gradient witness in dimension 48

- **Question.** JCB-024. Nobody has published an explicit symmetric / gradient /
  Hessian-nilpotent witness from the July 2026 counterexample (verified sweep,
  context/2026-07-22-symmetrization-dossier.md, Task 5). Construct it: an explicit
  non-invertible SYMMETRIC Keller map Ftil = id + grad f on C^48 with a 2-point collision
  certificate, and the failing Hessian-nilpotent homogeneous quartic P_star = -f.
- **Inputs (with credit).** W. Thompson's explicit Bass-Connell-Wright cubic-homogeneous
  form of the Alpoge/Fable counterexample: G = U + H on Q^24, H cubic homogeneous,
  54 cubic monomials, published 2026-07-21 (github.com/wtho704/
  explicit-cubic-homogeneous-jacobian-counterexample, Zenodo 21466221), with a rational
  collision pair; copies in `data/` here. The de Bondt-van den Essen construction
  (PAMS 133 (2005) 2201-2205): f_H = -i sum_j H_j(x + iy) y_j, with the triangular
  conjugation S^{-1} o (id + grad f_H) o S = (x + H, y + (JH)^t y - i H) and the explicit
  collision transfer w = i (I + JH(v)^t)^{-1} (u - v), p1 = (u, 0), p2 = (v - iw, w).
  Zhao's convention (TAMS 359 (2007)): P_star = -f_H is the HN quartic.
- **Falsifiable predictions.**
  1. [MV] (Input verification) H parses to a cubic homogeneous map on Q^24; the published
     collision pair satisfies G(P) = G(Q) exactly with P != Q.
  2. [MV] (Nilpotency, in-house) JH is nilpotent: target the full sparse certificate
     (JH)^17 = 0 by exact dict arithmetic; at minimum, symbolic traces Tr(JH^k) = 0 for
     small k plus exact point-nilpotency (JH(pt))^17 = 0 at random rational points; any
     shortfall from the full identity is recorded and Thompson's dual-verified
     certificate is cited as external.
  3. [MV] (The conjugation identity) S^{-1} o (id + grad f_H) o S = (x + H(x),
     y + (JH(x))^t y - i H(x)) holds IDENTICALLY in the 48 variables: with nilpotency
     this makes Ftil = id + grad f_H a symmetric Keller map (det = 1).
  4. [MV] (The collision) p1 = (u, 0) != p2 = (v - iw, w) and Ftil(p1) = Ftil(p2)
     exactly over Q(i): Ftil is NOT invertible: the Hessian Conjecture HC(48) is false
     with an explicit witness; the symmetric/gradient JC falls explicitly.
  5. [MV] (The failing quartic) P_star = -f_H is homogeneous of degree 4 with nilpotent
     Hessian (equivalent to 2 by the dBvdE char-poly identity); it explicitly falsifies
     Zhao's Vanishing Conjecture; sanity: Delta P_star^2 != 0 (forced by Zhao Cor 3.9).
- **Method.** sympy over Q(i) for construction and evaluations; pure-Python exact
  Fraction dict arithmetic for the sparse nilpotency chain; all point arithmetic exact.
  Caps 570 s per part; long nilpotency chain run as its own part.
- **Success criterion.** 1, 3, 4, 5 verified in-house; 2 fully in-house or honestly
  partial + external. The witness objects are persisted as artifacts (f_H, P_star,
  collision points) for the record and the manuscript.
- **Failure criterion.** Conjugation identity fails (construction misread); collision
  fails to transfer (formula misread); input verification fails (fall back to redoing
  the BCW ladder ourselves, out of scope today).

Declared 2026-07-22 before the run.
