# Jacobian conjecture dossier (2026-07-20)

Deep-research dossier for the first CAOS Research problem. Every claim carries its source; anything
not confirmed against a primary source is flagged **UNVERIFIED**. Our own exact computations (the
strongest evidence in this dossier) live in `../validation/`.

---

## 1. Statement

Let $k$ be a field of characteristic 0 and $F = (F_1, \dots, F_N) : k^N \to k^N$ a polynomial map.
The Jacobian conjecture JC(N) asserts:

$$\det JF \in k^\times \ (\text{a nonzero constant}) \implies F \text{ has a polynomial inverse } G : k^N \to k^N.$$

A polynomial map with constant nonzero Jacobian determinant is called a **Keller map**. Over
$\mathbb{C}$, invertibility is equivalent to injectivity: an injective polynomial map
$\mathbb{C}^N \to \mathbb{C}^N$ is automatically surjective with polynomial inverse
(Bialynicki-Birula and Rosenlicht; see also van den Essen's book below). So refuting JC(N) needs
exactly one thing: a Keller map with two (or more) distinct points sharing an image.

## 2. History

- **1884, Ludwig Kraus.** The two-variable statement appears (with a flawed proof in the same paper)
  in an 1884 publication by L. Kraus. Source: L. O. Rodriguez Diaz, "On the origin of the Jacobian
  conjecture", Comptes Rendus. Mathematique 364 (2026) 363-370, arXiv:2512.23614. The paper notes
  that the root of Kraus's error, controlling ramification at infinity, is still the principal
  obstacle to algebro-geometric approaches.
- **1939, Ott-Heinrich Keller.** "Ganze Cremona-Transformationen", Monatshefte fur Mathematik und
  Physik 47(1): 299-306, doi:10.1007/BF01695502. The classical origin; Keller proved the birational
  case (where $k(X) = k(F)$).
- **1998, Smale's problem 16.** The Jacobian conjecture is number 16 in Smale's "Mathematical
  problems for the next century".
- **2026-07-19/20, the counterexample for N = 3.** Announced by Levent Alpoge (mathematician,
  Anthropic) on X (@__alpoge__, 2026-07-20, "hello there the jacobian conjecture is false"),
  crediting Akhil for posing the question and the LLM Claude Fable 5 for producing the example.
  Press: M. Sparkes, New Scientist, 2026-07-20 (reports that the one-line certificate was verified
  by many mathematicians within a day). **No arXiv paper exists yet as of 2026-07-20**; the primary
  artifact is the posted map plus the collision certificate, which is fully machine-checkable (and
  we checked it, section 5).

## 3. Classical positive results and reductions (the ladder the counterexample had to evade)

| Result | Statement | Source |
|---|---|---|
| Wang 1980 | JC holds for maps of degree 2 (any N) | S. S.-S. Wang, per Wikipedia "Jacobian conjecture" ref [11] |
| Moh 1983 | JC(2) holds up to degree 100 | T.-T. Moh, J. reine angew. Math. 340 (1983) 140-212 (degree bound per Wikipedia refs [18]-[19]) |
| Bass-Connell-Wright 1982 | JC (all N) reduces to degree 3, cubic homogeneous form $F = X + H$, $H$ cubic homogeneous | Bull. AMS (N.S.) 7(2) (1982) 287-330 |
| Druzkowski 1983 | Further reduces to cubic linear form: $H_i$ = cube of a linear form | Math. Ann. 264(3) (1983) 303-313 |
| de Bondt, van den Essen 2005 | Suffices to treat cubic homogeneous with symmetric Jacobian | Wikipedia refs [20]-[21] |
| Connell, van den Dries 1983 | If JC is false there is a counterexample with integer coefficients and det = 1 | Wikipedia ref [14] |
| Campbell 1973 / Razar 1979 / Wright 1981 | JC holds when $k(X)/k(F)$ is Galois | Wikipedia refs [15]-[17] |
| Pinchuk 1994 | The strong REAL Jacobian conjecture ($\det JF \neq 0$ everywhere, not constant $\implies$ injective) is FALSE in $\mathbb{R}^2$ | Math. Z. 217(1) (1994) 1-4 |

Notes.
- The degree numbers quoted for Pinchuk's example (Wikipedia summary said "total degree 35 and
  higher"; other literature quotes component degrees (10, 25)) are **UNVERIFIED** at this level of
  detail; pin down when the 2D dossier is built inside the repo.
- Pinchuk matters here because his mechanism (a locally invertible map failing properness) is the
  same *kind* of loophole the 2026 counterexample exploits, but Pinchuk's Jacobian is non-constant,
  so JC itself was untouched.

## 4. Equivalent / connected conjectures (now a falsification cascade)

- **Dixmier conjecture** (endomorphisms of the Weyl algebra are automorphisms): Dixmier(N) implies
  JC(N); conversely JC(2N) implies Dixmier(N) (Tsuchimoto 2005; Belov-Kanel and Kontsevich 2007).
  Direction of the cascade: the counterexample kills JC(3), which does NOT immediately decide
  Dixmier (Dixmier(N) implies JC(N), so falsity of JC(3) refutes any proof route via Dixmier(3),
  and stable equivalence JC iff Dixmier means the FULL Dixmier conjecture is now false; the exact
  smallest failing Weyl dimension is open). **Handle with care in the repo; verify the stable
  equivalence statement against Belov-Kanel-Kontsevich before publishing.**
- **Poisson conjecture**: equivalent to JC (Adjamagbo, van den Essen 2007); now false in some
  dimension.
- **Mathieu conjecture** (Mathieu 1997, integrals over compact connected Lie groups): implies JC;
  Z. Zhang's July 2026 note derives that the Mathieu conjecture fails for SU(3).
- **Gaussian moments conjecture** (Derksen, van den Essen, Zhao): GMC for all N implies JC, so GMC
  fails at some finite N (smallest failing N open).
- **Zhao's vanishing conjecture** (Hessian-nilpotent quartics, $\Delta^m(H^m) = 0 \implies
  \Delta^m(H^{m+1}) = 0$ for large $m$): equivalent to JC, now false; an explicit failing quartic
  is an open computational target.
- **Image conjecture** (van den Essen, Wright, Zhao): implies the vanishing conjecture, hence fails
  in some finite dimension.

Source for the five consequences: Zihan Zhang, "Direct consequences of the three-dimensional
counterexample to the Jacobian conjecture" (web note, July 2026,
https://zzhang-iu.github.io/papers/direct-consequences-jacobian/). Secondary source; each
implication chain must be re-verified against its primary reference before we transcribe it into
the public repo. Status here: **UNVERIFIED (secondary)**.

- Standard monograph for everything classical: A. van den Essen, "Polynomial Automorphisms and the
  Jacobian Conjecture", Progress in Mathematics 190, Birkhauser, 2000. (From prior knowledge;
  confirm edition details at transcription time.)

## 5. The counterexample, and our independent validation (VERIFIED, exact)

The map $F = (P, Q, R) : \mathbb{C}^3 \to \mathbb{C}^3$, with $u = 1 + xy$:

$$P = u^3 z + y^2 u (4 + 3xy), \qquad Q = y + 3x u^2 z + 3x y^2 (4 + 3xy), \qquad R = 2x - 3x^2 y - x^3 z.$$

Our exact sympy verification (`../validation/validate_alpoge_counterexample.py`, output captured
2026-07-20, all checks PASS):

1. $\det JF = -2$ identically (expanded symbolically; no numeric step).
2. $F(0, 0, -\tfrac14) = F(1, -\tfrac32, \tfrac{13}{2}) = F(-1, \tfrac32, \tfrac{13}{2}) =
   (-\tfrac14, 0, 0)$: three distinct preimages, so $F$ is not injective and has no inverse of any
   kind. JC(3) is false; adding dummy coordinates ($F \times \mathrm{id}_{k^{N-3}}$ is again Keller
   and non-injective) falsifies JC(N) for every $N \ge 3$.
3. Bonus (our Groebner computation, lex order): the fiber over $(-\tfrac14, 0, 0)$ is EXACTLY those
   three points. The eliminant in $z$ is $z^2 - \tfrac{25}{4} z - \tfrac{13}{8} =
   \tfrac18 (2z - 13)(4z + 1)$; branch $z = \tfrac{13}{2}$ gives $y = \pm\tfrac32$, $x = -\tfrac23 y$;
   branch $z = -\tfrac14$ gives $x = y = 0$. Basis relations: $3x + 2y = 0$ on the fiber,
   $12 y^2 = 4z + 1$, $y(2z - 13) = 0$.

Component degrees: $\deg P = 7$, $\deg Q = 6$, $\deg R = 4$. All coefficients are real (indeed
rational), so the same map also refutes the constant-Jacobian statement over $\mathbb{R}$ in the
non-injectivity sense.

## 6. Why it works: structural analysis (secondary source, to re-verify in-repo)

Source: "The Jacobian counterexample, explained" (https://jacobianfun.org/jacobian-explained,
July 2026). Rich but **UNVERIFIED (secondary)**; re-deriving every item below with exact symbolic
computation is the first experiment block of the repo.

1. **Weighted scaling symmetry.** Under $(x, y, z) \mapsto (\lambda x, y/\lambda, z/\lambda^2)$ the
   outputs transform as $(A, B, C) \mapsto (A/\lambda^2, B/\lambda, \lambda C)$. Invariants:
   $v = xy$, $t = x^2 z$, $u = 1 + v$. The map is a weighted lift of a ONE-variable problem.
2. **Seed polynomial.** The construction is generated by the seed $p(w) = 2w - 3w^2$; inversion of
   $F$ compresses to a single cubic equation $\Phi(w) = w^2 - w^3$ intersected with a line, so the
   generic fiber has exactly 3 points (matching our Groebner result over one special target).
3. **Mechanism: non-properness, not critical points.** Sheets of the covering cannot merge at a
   finite point (that would force $\det JF \to 0$); they merge AT INFINITY. Over the plane $C = 0$
   the flat sheet $x = 0$ and the curved sheet $x^2 z = 2 - 3xy$ have images that approach each
   other while the preimages diverge (like $2/x^2$). $F$ is a local diffeomorphism everywhere but
   not proper, so it is not a covering map onto its image, and global injectivity fails. This is
   consistent with the classical fact that a PROPER Keller map is invertible, and with Kraus's
   original obstacle: ramification/behavior at infinity.
4. **A parametric family (the "weighted-lift family").** Any seed polynomial $p$ with
   $$p(0) = 0, \qquad p(1) = -c \ne 0, \qquad \int_0^1 p(w)\, dw = 0$$
   yields a Keller map $F_p$ with constant $\det JF_p = bc$ and generic fiber degree
   $\deg p + 1$. The announced map is the minimal seed (degree 2). An explicit degree-4-fiber
   instance: seed $p(w) = w - 2w^3$ gives a map $G$ with $\det JG = -6$ and component degrees
   $(12, 11, 4)$. Seeds exist realizing every fiber degree $n \ge 3$, e.g.
   $p_d(w) = 2w - 3w^2 + w(1 - w)\left(w^{d-2} - \tfrac{6}{d(d+1)}\right)$.
5. **Inequivalence invariant.** Generic fiber degree is invariant under invertible polynomial
   coordinate changes on either side, so the degree-4-fiber map $G$ is genuinely new, not $F$ in
   disguise.
6. **What it does NOT do.** The page states explicitly that these three-variable constructions do
   not settle the two-variable case.

## 7. Why the classical reductions did not block this

- Bass-Connell-Wright / Druzkowski say a counterexample can be CONVERTED (in higher dimension) to
  cubic-homogeneous / cubic-linear form; they never bounded the search space in dimension 3 itself.
  A corollary task for the repo: push $F$ through the BCW reduction to produce an explicit
  cubic-homogeneous counterexample and find in which dimension it lands.
- Moh's degree-100 verification is specific to N = 2.
- Wang's degree-2 theorem: the counterexample has degree 7, comfortably above.
- The positive "injective implies invertible" results are vacuous here: the whole point is that
  injectivity fails.

## 8. The two-variable case (open target of the program)

- JC(2) remains open as of 2026-07-20; specialist literature has long treated its evidential status
  as different from the general case (Wikipedia; Rodriguez Diaz 2026 for the Kraus history).
- Known for N = 2: degree $\le 100$ (Moh); many structural results tie JC(2) to the geometry of the
  curve at infinity, Newton polygon constraints, and Abhyankar's work. (Prior knowledge,
  **UNVERIFIED**; build the dedicated 2D dossier from primary sources when that experiment block
  opens.)
- The central research question our program can genuinely attack computationally: WHY does the
  weighted-lift mechanism need three variables? Conjecture-shaped question: a 2-variable Keller map
  is proper (equivalently, has no asymptotic values / finite asymptotic variety obstruction), which
  would make JC(2) true via properness; where exactly does the 3-variable construction break in
  2 variables (the weight vector $(1, -1, -2)$ needs a third coordinate to carry negative weight
  while keeping polynomiality)? This is experimentally explorable: exhaustive small-degree searches
  for 2-variable Keller maps with nontrivial fiber structure, asymptotic-variety computation via
  elimination, and attempts to transplant the seed construction with 2-variable weight vectors.

## 9. Research directions for the repo (feed the problem plan)

- **JC-RD-1 (verify).** Re-derive, in exact arithmetic, every claim of section 6: the scaling
  symmetry, the seed reduction, the family conditions, det $JF_p = bc$, fiber degrees, the
  degree-4 instance, the fiber-degree invariance argument. Publish scripts + outputs.
- **JC-RD-2 (minimality).** Is degree 7 (or the degree vector (7,6,4), or fiber degree 3) minimal
  for a 3-variable counterexample? Systematic search over weighted-homogeneous ansatz spaces;
  GPU-accelerated coefficient search where symbolic pruning leaves finite boxes.
- **JC-RD-3 (geometry).** Compute the asymptotic variety (non-properness locus) of $F$ exactly; map
  where the sheets merge at infinity; visualize the real slice for the web app.
- **JC-RD-4 (cascade).** Push $F$ through Bass-Connell-Wright / Druzkowski to explicit cubic forms;
  extract the explicit failing objects for Mathieu/GMC/vanishing conjectures where feasible; verify
  the implication chains from primary sources.
- **JC-RD-5 (2D obstruction).** Formalize why the mechanism needs $N \ge 3$; survey and reproduce
  the strongest known 2D partial results; run the 2-variable searches of section 8.
- **JC-RD-6 (char p and R).** Behavior of $F$ mod small primes (JC is classically false in char p
  via $x - x^p$; the interesting question is what the NEW mechanism does there); real-topology
  study of $F|_{\mathbb{R}^3}$ (covering degrees of the real sheets).

## 10. Reference list (as gathered 2026-07-20)

1. L. Kraus, 1884 paper (exact citation via Rodriguez Diaz 2026). Historical origin, 2 variables.
2. O.-H. Keller, "Ganze Cremona-Transformationen", Monatsh. Math. Phys. 47 (1939) 299-306,
   doi:10.1007/BF01695502.
3. H. Bass, E. Connell, D. Wright, Bull. AMS (N.S.) 7(2) (1982) 287-330 (degree reduction).
4. L. M. Druzkowski, Math. Ann. 264(3) (1983) 303-313 (cubic linear form).
5. T.-T. Moh, degree $\le 100$ for N = 2 (1983).
6. S. S.-S. Wang, degree 2 case (1980).
7. S. Pinchuk, "A counterexample to the strong real Jacobian conjecture", Math. Z. 217 (1994) 1-4.
8. M. de Bondt, A. van den Essen, symmetric reduction (2005).
9. A. van den Essen, "Polynomial Automorphisms and the Jacobian Conjecture", Birkhauser PM 190, 2000.
10. Y. Tsuchimoto (2005); A. Belov-Kanel, M. Kontsevich (2007): JC vs Dixmier.
11. P. K. Adjamagbo, A. van den Essen (2007): Poisson equivalence.
12. L. O. Rodriguez Diaz, C. R. Math. 364 (2026) 363-370, arXiv:2512.23614 (Kraus history).
13. L. Alpoge, X post @__alpoge__, 2026-07-20 (the counterexample; credit: Akhil, Claude Fable 5).
14. M. Sparkes, New Scientist, 2026-07-20 (verification reportage).
15. Z. Zhang, "Direct consequences of the 3D counterexample to the JC", web note, 2026-07
    (https://zzhang-iu.github.io/papers/direct-consequences-jacobian/). Secondary.
16. "The Jacobian counterexample, explained", https://jacobianfun.org/jacobian-explained, 2026-07.
    Secondary; source of the weighted-lift family analysis.
17. Wikipedia, "Jacobian conjecture" (as of 2026-07-20): reference hub used to locate primary items.
18. Wikipedia, "Smale's problems" (as of 2026-07-20): problem 16 listing + statuses.
