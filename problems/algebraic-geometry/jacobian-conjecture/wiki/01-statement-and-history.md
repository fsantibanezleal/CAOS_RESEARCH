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

## Consequence cascade (to be re-verified from primary sources; UNVERIFIED as stated)

Via known implications, the refutation propagates to: the Mathieu conjecture (fails for SU(3)),
the Gaussian moments conjecture (fails at some finite N), Zhao's vanishing conjecture, the Image
conjecture, and (via stable equivalence, Tsuchimoto 2005 / Belov-Kanel-Kontsevich 2007) the
Dixmier conjecture. Each chain is queued for primary-source verification (JCB-009) before this
wiki asserts it without the UNVERIFIED flag.
