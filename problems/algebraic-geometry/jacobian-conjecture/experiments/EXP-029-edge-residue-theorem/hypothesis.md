# EXP-029 - The edge residue in closed form: the weight-class theorem

- **Question.** JCB-032. Derive the single obstruction pairing in closed form and determine
  its true scope. Design derivation (to certify): with weights w = (v, 1 - u), the slice
  P = x + a x^u y^v (u >= 2, v >= 1) is w-HOMOGENEOUS, so J(P, .) preserves the w-grading up
  to a constant shift and the Keller equation J(P, Q) = 1 DECOUPLES by weight class. The
  constant sits in the image of exactly one class, spanned by the ray
  g_s = x^{ks} y^{(v/d)s + 1} (k = (u-1)/d, d = gcd(u-1, v)), and on that ray L = J(P, .) is
  BANDED (bidiagonal when d = 1): L(g_s) = A_s e_s + a B_s e_{s+d} with A_s, B_s > 0
  integers and e_t = x^{kt} y^{(v/d)t}. The first row forces the chain c_0 = 1/A_0,
  c_{s} = -a B_{s-d} c_{s-d} / A_s, all nonzero; the final row demands the last chain entry
  vanish: CONTRADICTION at every finite truncation. Since any polynomial partner truncates,
  P is NEVER a Keller component, at ANY degree: unconditional, no Abhyankar input.
- **Motivation.** EXP-028's anatomy (certificate support exactly on the P-edge ray) predicted
  a closed form; this is it. If verified, it (a) explains all seven measured pairings,
  (b) retires the entire pure-slice window program in one stroke, upgrading the [D]
  conditional to an unconditional theorem for monomial h, and (c) reaches beyond the ~108
  verified floor at negligible cost (e.g. deg P = 135), where nothing is verified in any
  form. Honesty note: the proof is elementary once seen (a specialist may call it folklore);
  we have not found it stated; the record claims exactly that.
- **Falsifiable predictions.**
  1. [MV] (Bidiagonal formula) For h = x^p y^q on a grid (p, q in 1..4, s in 0..5):
     L(g_s) = (2qs + 1) e_s + 2a (qs + p) e_{s+1} exactly (u = 2p, v = 2q, d may exceed 1:
     the banded generalization is verified in the same sweep for u in 2..7, v in 1..7).
  2. [MV] (The seven pairings) The closed-form chain product reproduces every measured
     pairing up to a rational unit: a-exponents (2,4,5,6 at (4, <= 6/10/14/18); 2 at
     (18, <= 27); 2 at (24, <= 36); 3 at (18, <= 36)) all match floor((N - 1)/raydeg) + 1.
  3. [MV] (Decoupling, end to end) For three (u, v) cases incl. one with d > 1: the FULL
     window system's inconsistency (small windows, direct linsolve) coincides with the ray
     subsystem's inconsistency: no other class ever obstructs (their systems are
     homogeneous, satisfied by zero).
  4. [MV] (Beyond the floor) For P = x + a x^{54} y^{81} (degree 135 > 108): the ray
     subsystem is inconsistent for ALL a != 0 at every truncation S <= 8 (covering partner
     degrees to ~1000), machine-certified; with the decoupling identity this certifies: no
     Keller partner of degree <= 1000. The induction for all S is stated in the verdict as
     the theorem's proof (each step machine-shadowed).
- **Method.** sympy over QQ and QQ(a): exact expansion of L on ray monomials; chain products;
  small-window cross-checks; the degree-135 class certificate. Caps 570 s.
- **Success criterion.** 1-4 verified; the theorem recorded with its elementary proof and the
  honest folklore caveat.
- **Failure criterion.** Any formula mismatch (the closed form is wrong: back to anatomy), or
  a full-window inconsistency NOT explained by the ray class (a second obstruction exists:
  bigger discovery, analyze immediately).

Declared 2026-07-21 before the run.
