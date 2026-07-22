# EXP-046 - The Tower Lemma: proof attempt (route N1, the last step to Theorem 5)

- **Question.** JCB-038. EXP-044 reduced Theorem 5 all-degree to the TOWER LEMMA. Prove it.
- **Motivation (the declared derivation, in full).** Let P = x + R (R without constant or
  linear part), M_N the window matrix (columns = coefficient vectors of L(m) = J(P, m),
  m of degree 2..N), rhs from J(P, y) - 1. Three structural facts give the induction
  N -> N + 1:
  (i) DEGREE BOOKKEEPING: outputs of old columns (deg m <= N) have degree
  <= N + deg P - 2, so the new rows (degree N + deg P - 1) meet only new columns: the
  old-column block over new rows is ZERO.
  (ii) THE TOP BLOCK: the new-rows x new-columns block D is the action m -> J(T, m) of
  the TOTAL-DEGREE TOP FORM T of P on degree-(N + 1) forms; its kernel consists of the
  forms kappa with J(T, kappa) = 0, i.e. powers of the primitive root g of T = c g^e.
  (iii) THE RESONANCE REDUCTION: given a certificate Lambda_N (left-null, pairing != 0),
  an extension Lambda_{N+1} = (Lambda_N, Lambda_new) exists iff Lambda_N annihilates
  L(kappa) for every kernel form kappa (solvability of Lambda_new^T D = -Lambda_N^T C
  requires exactly orthogonality to ker D; L(kappa) is supported on old rows since
  D kappa = 0). If it exists, the pairing is PRESERVED (rhs lives on old rows), so
  inconsistency propagates forever from any certified base window.
  THE KEY IDENTITY killing the resonances when kappa = (scalar) T^k: T = P - x - (lower
  P-terms), so T^k = lambda P^k + (terms of degree <= N), and P^k is in ker L; hence
  L(T^k) = L(in-window polynomial), which EVERY left-null certificate annihilates. For
  the Theorem 5 family this covers: d < u + v (T = a x^u y^v, kernel = B-powers,
  B^k = a^{-k}(P - x - b x^d)^k reduces in-window); d = u + v (T = P - x directly);
  d > u + v (T = b x^d, x^{(N+1)} resonances reduce via P^{(N+1)/d}). The delicate case
  is T a PROPER POWER (e.g. u = v = 2: T = a (xy)^2): kernel contains g^s with e not
  dividing s (odd (xy)-powers), which do NOT reduce mod C[P]; for those the annihilation
  must come from class-support disjointness (to be measured; if it fails, the tower
  needs the odd resonances handled separately and the lemma's scope narrows to
  primitive-top families, stated honestly).
- **Falsifiable predictions.**
  1. [MV] (Bookkeeping) The old-column/new-row block is zero on samples; D equals the
     top-form action; ker(D) at tested degrees is exactly the predicted span.
  2. [MV] (The key identity) T^k - lambda P^k is supported in degree <= N, and the rank
     test confirms L(kappa) lies in the old-column space, for the family's three regimes
     at several (N, k).
  3. [MV] (End-to-end extension) At (2,1,2), the explicit extension Lambda_8 -> Lambda_9
     (an active resonance step, 3 | 9) and Lambda_11 -> Lambda_12 exist, are left-null,
     and preserve the pairing up to the measured tower ratio.
  4. [MV] (The proper-power case) At (2,2,2), the odd resonances (xy)^s: measure
     Lambda_N(L((xy)^s)); prediction (from the measured tower's persistence): they
     vanish by class-support disjointness; if not, record the break honestly.
  5. [D] (The lemma and the theorem) With 1-3: THE TOWER LEMMA holds for primitive-top
     and T = P - x families, and THEOREM 5 becomes UNCONDITIONAL there; the
     proper-power scope is settled by 4's outcome.
- **Method.** sympy over QQ and QQ(a, b); rank tests (EXP-036 style); explicit extension
  solves; caps 570 s per part.
- **Success criterion.** 1-3 verified and 4 measured: Theorem 5 unconditional on the
  covered scope, with the scope stated exactly.
- **Failure criterion.** The rank test failing on a claimed in-window reduction (the key
  identity is wrong); an extension failing where the derivation says it exists.

Declared 2026-07-22 before the run.
