# EXP-048 - The proper-power odd resonance: mechanism hunt (route N1, last case)

- **Question.** EXP-046 proved the Tower Lemma except at proper-power tops, where odd
  resonances (e.g. (xy)^5 at (2,2,2)) do not reduce mod C[P] yet measured pairing zero.
  Why? Identify the mechanism; prove it if it is bookkeeping.
- **Motivation (derivation, declared).** For P = x + a (xy)^2 + b x^2:
  L((xy)^s) = s x^s y^{s-1} (1 + 2 b x) exactly (computed by hand: J(x, (xy)^s) +
  b J(x^2, (xy)^s), the T-part vanishing). For odd s this is NOT an in-window image
  (ker L = C[P] for primitive P, and (xy)^s is not in window + C[P]), so the kill cannot
  be the key identity; it must be a property of the certificate itself: either (i) the
  left-null space is 1-dimensional and its unique certificate is orthogonal to
  L((xy)^s) for a structural reason (support/class bookkeeping), or (ii) the kill is
  special to the constructed tower certificate. Either way the tower survives if the
  kill can be certified symbolically in (a, b) at each resonance; a closed proof needs
  the structural reason.
- **Falsifiable predictions.**
  1. [MV] (The operator form) L((xy)^s) = s x^s y^{s-1} (1 + 2bx) identically.
  2. [MV] (Not an image) rank([M | L((xy)^5)]) > rank(M) at N = 9: the kill is NOT the
     key identity's mechanism (if rank equal, the theory above is wrong somewhere:
     investigate ker L).
  3. [MV] (Certificate kill, symbolic) The cleared certificate's pairing against
     L((xy)^s) is IDENTICALLY zero over QQ(a, b) at (s, N) = (5, 9) and (6, 11), and
     the left-null space dimension at those windows is recorded.
  4. [C -> D] (Mechanism) The certificate's support misses the rows of L((xy)^s), or
     its entries on those rows satisfy a visible cancellation law; whichever is
     measured becomes the proof target and is derived if it is pure bookkeeping.
- **Method.** sympy over QQ and QQ(a, b); rank and nullity computations; support
  comparison. Caps 570 s.
- **Success criterion.** 1-3 verified; 4 at least measured with the mechanism named;
  proof if bookkeeping suffices.
- **Failure criterion.** Prediction 3 failing symbolically (the tower breaks at
  proper-power tops for some parameters: Theorem 5's scope there must be retracted to
  the tested windows, recorded prominently).

Declared 2026-07-22 before the run.
