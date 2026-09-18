# 01 - Statement and history

## The conjecture

Let $k$ be a field of characteristic 0 and $F = (F_1, \dots, F_N) : k^N \to k^N$ polynomial. A
**Keller map** is one with $\det JF \in k^\times$ (a nonzero constant). The Jacobian conjecture
JC(N) asserted:

$$\det JF \in k^{\times} \implies F \text{ has a polynomial inverse.}$$

Over $\mathbb{C}$, invertibility is equivalent to injectivity (an injective polynomial self-map
of $\mathbb{C}^N$ is automatically surjective with polynomial inverse), so a refutation needs one
thing only: a Keller map with a repeated value.

## Timeline

- **1884.** The two-variable statement appears in a paper of L. Kraus, with a flawed proof; the
  flaw (controlling ramification at infinity) is the durable obstacle of the subject
  (L. O. Rodriguez Diaz, C. R. Math. 364 (2026) 363-370, arXiv:2512.23614).
- **1939.** O.-H. Keller, "Ganze Cremona-Transformationen", Monatsh. Math. Phys. 47, 299-306,
  doi:10.1007/BF01695502. Keller proves the birational case.
- **Classical ladder** (details and sources in `../context/`): Wang (1980): degree 2 holds, any
  N. Moh (1983): JC(2) holds to degree 100. Bass-Connell-Wright (1982), Bull. AMS 7(2) 287-330:
  reduction to cubic homogeneous $F = X + H$. Druzkowski (1983), Math. Ann. 264, 303-313: cubic
  linear form. de Bondt-van den Essen (2005): symmetric cubic reduction. Pinchuk (1994), Math. Z.
  217, 1-4: the strong REAL variant is false (non-constant positive Jacobian, non-injective).
- **1998.** Problem 16 in Smale's "Mathematical problems for the next century".
- **2026-07-19/20.** Levent Alpöge (with the LLM Claude Fable 5; question posed by Akhil)
  announces $F = (P, Q, R)$ on $\mathbb{C}^3$, $u = 1 + xy$:
  $$P = u^3 z + y^2 u (4 + 3xy), \quad Q = y + 3x u^2 z + 3x y^2(4 + 3xy), \quad R = 2x - 3x^2 y - x^3 z,$$
  with $\det JF = -2$ and $F(0, 0, -\tfrac14) = F(1, -\tfrac32, \tfrac{13}{2}) =
  F(-1, \tfrac32, \tfrac{13}{2}) = (-\tfrac14, 0, 0)$. **JC(N) is false for all $N \ge 3$**
  (append dummy coordinates). No arXiv paper exists as of 2026-07-20; the certificate is fully
  machine-checkable and this program validated it independently in exact arithmetic (EXP-001),
  adding that the fiber over $(-\tfrac14, 0, 0)$ is EXACTLY those three points (lex Groebner:
  eliminant $\tfrac18 (2z - 13)(4z + 1)$, with $3x + 2y = 0$ and $12y^2 = 4z + 1$ on the fiber).
- **Open.** JC(2). The evidential status of the 2-variable case has always been distinguished
  from the general one; see [04-two-dimensional-frontier.md](04-two-dimensional-frontier.md).

## Consequence cascade (primary sources: EXP-016, EXP-018; dimension indices: EXP-136)

The refutation propagates through implications checked against their primary records, each
taken with the dimension index its source states (EXP-136):

- **Mathieu conjecture: false for SU(2) and for SU(N), N >= 24.** Mathieu's argument
  (Mathieu 1997, expounded in arXiv:2511.16561, Theorems 4.16 and 4.23) shows that the
  conjecture for SU(N) makes every Keller map x - h of C^N with h homogeneous invertible; the
  24-variable cubic-homogeneous form verified in EXP-041 is such a map and is not injective.
  SU(2) fails by an explicit example (Long, arXiv:2607.19012). For 3 <= N <= 23 the located
  proofs do not decide it: F is not affinely of homogeneous type (EXP-136), and the reduction to
  that type adds variables. Abelian case: Duistermaat-van der Kallen 1998.
- **Gaussian moments conjecture: false for every n >= 3**, with an explicit three-variable
  counterexample (Long, arXiv:2607.18186); GMC implies JC (Derksen-van den Essen-Zhao, Israel J.
  Math. 2017, arXiv:1506.05192), and GMC(1) holds (their Proposition 4.2); a proof of GMC(2)
  is claimed (Wilson, arXiv:2607.23887).
- **Zhao's vanishing conjecture: false** (equivalent to JC: arXiv:math/0409534,
  arXiv:0704.1691), with an explicit Hessian-nilpotent quartic in 48 variables (EXP-041).
- **Image conjecture: false in some dimension** (implies the vanishing conjecture: van den
  Essen, arXiv:1006.5801).
- **Dixmier conjecture: false for every rank n >= 3**, since Dixmier(n) implies JC(n). The
  converse direction JC(2n) implies Dixmier(n) (Belov-Kanel-Kontsevich arXiv:math/0512171;
  independently Tsuchimoto, Osaka J. Math. 2005) gives only stable equivalence and says nothing
  about rank 2 from the falsity of JC(4). Ranks 1 and 2 remain open; a proof of rank 1 is
  claimed (Zheglov, arXiv:2410.06959).
- **Poisson conjecture: false for every index n >= 3** (JC(2n) implies Poisson(n) implies
  Dixmier(n) implies JC(n): Adjamagbo-van den Essen, arXiv:math/0608009, Theorem 7); indices 1
  and 2 remain open. A proof of JC(2) would give Dixmier(1) and Poisson(1); a counterexample to
  JC(2) would refute Dixmier(2) and Poisson(2).
