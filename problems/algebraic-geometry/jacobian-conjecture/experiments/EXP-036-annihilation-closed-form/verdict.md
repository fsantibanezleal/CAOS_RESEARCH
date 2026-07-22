# EXP-036 - Verdict: CONFIRMED after a REFUTED first derivation (2026-07-22). JCB-033 closed

Artifacts: `artifacts/output-2026-07-22.txt` (final) and
`artifacts/output-refuted-Ptop-version-2026-07-22.txt` (the refuted first attempt, kept).

## The refutation, first

The declared derivation used sources of the form P_top^{k-1} J(P_top, m) and argued they lie
in the image of L_top. The machine refuted it on both tests: with in-window preimages the
pairings were NONZERO (part C) and the rank test placed the vectors OUTSIDE the column space
(part D). The error was precise and worth recording: the operator whose image the certificate
covector annihilates is L = J(P, .) built from the FULL P, not L_top = J(P_top, .); the two
differ by the linear part's contribution. Conflating them broke the argument.

## The corrected lemma (closed form)

1. **Leibniz [MV].** J(f, f^{k-1} g) = f^{k-1} J(f, g) identically (generic symbolic f, g,
   k <= 4), since J(f, f) = 0.
2. **Sources are images [MV].** The sources entering the constant's equation are
   J(m, P^k) with the FULL P, and J(m, P^k) = -k L(P^{k-1} m) exactly (grid of (u, v),
   k <= 3, five monomials): every source is L applied to the EXPLICIT preimage P^{k-1} m.
3. **Hence annihilation, with no case analysis [MV].** The certificate covector Lambda is
   left-null on the completion matrix, whose columns are precisely L(m) for the ansatz
   monomials: Lambda annihilates the image of L, hence every source whose preimage lies in
   the ansatz span. Rank tests confirm the matrix form: rank([M | S]) = rank(M) for each
   source (part D).
4. **The window criterion, and the old artifact fully explained [MV].** Lambda_N(S) = 0
   exactly when deg(P^{k-1} m) <= N. The nonzero pairings of EXP-031's first run are
   retrodicted precisely: at window 6 the out-of-window sources gave 15, 30a, 30, 45 and at
   window 10 the last gave 945 a^2, matching that record entry number for number; every
   in-window source pairs to zero.

## Consequence: THEOREMS 2, 3 AND 4 ARE NOW UNCONDITIONAL

The annihilation step was the single derived gap in the tail machinery of the perturbed
weight-class theorem (2), the full-edge theorem (3) and the vertex dichotomy (4). It is
closed in general: sources live in the image, the certificate kills the image, and the only
subtlety (windowing) is exactly the finite-truncation bookkeeping, resolved by taking the
window to contain the preimage, which any fixed polynomial allows. JCB-033 is done.

## How could this be wrong?

- The lemma is stated and verified for the pure-slice certificate family used by Theorems
  2-4; certificates for other P families need the same (identical) argument re-instantiated,
  which the identity supports uniformly.
