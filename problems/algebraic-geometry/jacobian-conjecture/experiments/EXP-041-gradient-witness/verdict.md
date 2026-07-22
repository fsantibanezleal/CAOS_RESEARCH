# EXP-041 - Verdict: CONFIRMED; the first explicit symmetric/gradient witness, dimension 48 (2026-07-22)

Artifacts: `artifacts/output-{A,B,C,D,E}-2026-07-22.txt`;
`artifacts/witness-Pstar-2026-07-22.txt` (the failing quartic, 382 monomials);
`artifacts/witness-collision-2026-07-22.txt` (the exact Q(i) collision pair).
Inputs: `data/` (Thompson's dim-24 BCW form, sha256-matched; credit in data/README.md).
Construction sources: `context/2026-07-22-symmetrization-dossier.md` (de Bondt-van den
Essen PAMS 133 (2005); Zhao TAMS 359 (2007); BCW 1982; all read from primary texts).

## The result

**HC(48) is false with an explicit witness, and with it the symmetric/gradient Jacobian
conjecture and Zhao's Vanishing Conjecture fall EXPLICITLY (not just existentially):**

1. **Input verified in-house [MV].** Thompson's H (Q^24, 54 cubic monomials, homogeneous)
   parses exactly; the published rational collision G(P) = G(Q), P != Q, holds exactly.
2. **Nilpotency, in-house, with a CORRECTION [MV].** Exact sparse Fraction arithmetic:
   (JH)^18 = 0 identically while (JH)^17 has 6 surviving terms: JH is nilpotent of index
   18, NOT 17 as the upstream repo claims; nilpotency itself (the load-bearing fact)
   holds, so det(I + JH) = 1 (BCW grading lemma) and G is Keller. Traces Tr(JH^k) = 0
   for k = 1, 2, 4, 8 concur. An instrument bug of ours was caught en route (the first
   "trace" check tested per-entry vanishing instead of the diagonal SUM) and fixed;
   recorded per methodology.
3. **The construction is exact [MV].** f_H = -i sum_j H_j(x + iy) y_j is a homogeneous
   quartic in 48 variables (382 Q(i) monomials), and the de Bondt-van den Essen
   triangular conjugation S^-1 o (id + grad f_H) o S = (x + H(x), y + JH(x)^t y - iH(x))
   holds IDENTICALLY in all 48 components: Ftil = id + grad f_H is a symmetric Keller
   map of exactly the Corollary 1.3 form (gradient of a Hessian-nilpotent quartic).
4. **The collision [MV].** w = i (I + JH(v)^t)^{-1} (u - v); p1 = (u, 0),
   p2 = (v - iw, w): p1 != p2 and Ftil(p1) = Ftil(p2) EXACTLY over Q(i) (all 48
   components): Ftil is not injective, hence not invertible.
5. **The failing quartic [MV].** P_star = -f_H is an explicit homogeneous
   Hessian-nilpotent quartic in 48 variables whose deformed inversion pair is not
   polynomial: Zhao's Vanishing Conjecture (and the homogeneous d = 4 form, hence the
   full equivalence chain) fails AT AN EXPLICIT POLYNOMIAL. The finite certificate of
   failure is the collision (as the dossier explains, direct Delta^m P^{m+1}
   non-vanishing at the guaranteed range is astronomically out of reach); the forced
   sanity Delta P_star^2 != 0 holds (9028 terms).

## Priority and framing

Per the verified sweep (dossier Task 5), as of 2026-07-22 nobody had published an
explicit symmetric / gradient / Hessian-nilpotent witness; Zhang's consequences note is
explicitly non-constructive, and Thompson's artifact (which we credit and verified,
correcting its index claim 17 -> 18) is the cubic-homogeneous input, not the symmetric
witness. Manuscript addition queued; upstream index correction worth reporting to the
Thompson repo (Felipe's call on outreach).

## How could this be wrong?

- The witness inherits Thompson's BCW derivation from the Alpoge/Fable map; we verified
  his artifact's homogeneity, collision and nilpotency in-house, but did NOT re-derive
  the BCW ladder from the original 3-dimensional map (fallback documented in the
  dossier if ever needed).
- Symmetric JC is known TRUE for n <= 4 (nonhomogeneous) and n = 5 homogeneous; 48 is
  far above; whether a smaller symmetric witness exists is open (recorded, dossier 1.5).
