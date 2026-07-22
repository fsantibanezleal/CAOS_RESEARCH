# EXP-049 - THEOREM 6: the universal tower (routes N1 + M2)

- **Question.** Does the Tower Lemma generalize to ARBITRARY P = x + R? If yes, every
  certified window on a suitable shape becomes an all-degree exclusion: the
  staircase-length induction (route M2) collapses to per-shape base certificates.
- **Motivation (derivation, declared).** Take T = P_D, the FULL total-degree top form of
  P (not just a monomial). Then T = P - lower BY DEFINITION, so
  T^k = (P - lower)^k = P^k + (terms of degree <= kD - 1): every T-power resonance
  reduces in-window modulo ker L, for EVERY P. The kernel of J(T, .) on degree-(N+1)
  forms is spanned by g-powers where T = lambda g^e (dependence of binary forms): when
  T is NOT a proper power (e = 1), the kernel is exactly the T-powers, all of which
  reduce. The bookkeeping and extension steps of EXP-046 are P-agnostic. HENCE:
  **THEOREM 6 (candidate): if the total-degree top form of P = x + R is not a proper
  power, then window inconsistency with a certificate at any N >= deg P - 1 propagates
  to every window: ONE certified window = exclusion at ALL partner degrees.** Proper-
  power tops fall outside and need the half-plane mechanism (EXP-048).
- **Falsifiable predictions.**
  1. [MV] (Kernel classification) For sample non-proper-power tops (a primitive
     monomial; x^2(ay + cx); a dense cubic form), the kernel of J(T, .) on degree-M
     forms is zero unless deg T divides M, and then exactly the span of T^{M/deg T}
     (exact linear solves).
  2. [MV] (Universal reduction) deg(T^k - P^k) <= k deg P - 1 on multi-term samples
     (three shapes, k = 2, 3), and the rank test puts L(T^k) inside the old-column
     space.
  3. [MV] (The harvest) For a zoo of staircase shapes with non-proper-power tops
     (including MULTI-EDGE staircases and 3-term tops), one cleared window certificate
     each: by Theorem 6, each becomes an ALL-DEGREE exclusion; the harvest list is
     recorded.
  4. [D] (Scope statement) The frontier R0^m shapes have proper-power tops (gcd(4m,
     12m) = 4m): they need EXP-048's half-plane construction; stated, connecting the
     two mechanisms.
- **Method.** sympy over QQ and QQ(a,...); exact kernel solves on homogeneous forms;
  cleared certificates; caps 570 s per part.
- **Success criterion.** 1-3 verified: THEOREM 6 stands with the same [MV/D] strength
  as the Tower Lemma, and the harvest converts prior window results into all-degree
  exclusions.
- **Failure criterion.** A non-proper-power top with extra kernel (the dependence
  classification misapplied); a reduction exceeding the window bound.

Declared 2026-07-22 before the run.
