# EXP-136 - Verdict: CONFIRMED (2026-09-18). Four cascade rows restated at the level of indices

Artifacts: `artifacts/output-2026-09-18.txt` (14 checks, all PASS; two runs byte-identical),
`artifacts/result.json`, `artifacts/sources.md` (every load-bearing statement transcribed, with
the SHA-256 of the fetched PDF).

## Results

1. **Dixmier: CONFIRMED.** With DC(n) => JC(n) and JC(2n) => DC(n) (Belov-Kanel and Kontsevich,
   introduction and Theorem 1), the closure (Part A) gives DC(n) false for every n >= 3, and
   leaves DC(1) and DC(2) undecided. The implication JC(2n) => DC(n) carries truth from JC(4)
   to DC(2), never falsity, so the falsity of JC(4) says nothing about DC(2). Conditional
   closures: a proof of JC(2) would give DC(1); a counterexample to JC(2) would refute DC(2).
2. **Poisson: CONFIRMED.** Adjamagbo and van den Essen, Theorem 7: JC(2n) => PC(n) => DC(n) =>
   JC(n), PC(n) being the conjecture for the canonical Poisson algebra in 2n variables. The
   closure gives PC(n) false for every n >= 3; PC(1) and PC(2) are undecided and follow JC(2)
   exactly as DC(1) and DC(2) do.
3. **Gaussian moments: CONFIRMED for n = 1 and n >= 3; n = 2 refined by the search pass.**
   GMC(n) is false for every n >= 3 (Long, arXiv:2607.18186, Theorem 5.1 and the
   dummy-variable remark); GMC(1) is true (Derksen, van den Essen and Zhao, Proposition 4.2).
   For n = 2 a proof is claimed (Wilson, arXiv:2607.23887, preprint), not verified here.
4. **Mathieu: CONFIRMED, (a) and (b).** (a) The ideal of all second partial derivatives of F is
   the unit ideal (Part B, Groebner basis [1], reproduced by the direct certificate B3). F has
   total degree 7, so it is not affinely equivalent to any map x - h with h homogeneous, and the
   located proof of Mathieu's implication (Zwart, Theorems 4.16 and 4.23) does not reach SU(3)
   through F. (b) The 24-variable form G = x + H of EXP-041 has H homogeneous cubic (54
   monomials) and an exact collision (Part C), and it is Keller by the nilpotency of JH
   (EXP-041). Theorems 4.23 and 4.16 at N = 24, and at every N > 24 after adjoining identity
   coordinates (which keeps the form x - h), give: the Mathieu conjecture is false for SU(N),
   N >= 24.
5. **Mathieu for SU(2) (amendment): CONFIRMED on the checked range.** Long's F = (1 + c)(ad + b),
   G = -c (arXiv:2607.19012, Theorem 4.2 with lambda = mu = 1) satisfy int F^n dg = 0 and
   int F^n G dg = (-1)^(n-1)/(n+1) exactly for n = 1..12 (Part D). The Mathieu conjecture for
   SU(2) is false (the all-n statement rests on Long's proof).
6. **GMC(3), explicit (amendment): CONFIRMED on the checked range.** Long's P3 expands to the
   printed five-term quartic, and E(P3^m) = 0, E(Z P3^m) = m! exactly for m = 1..10 (Part E).

## Statements superseded (EXP-016 and EXP-018 are not edited)

- EXP-016 item 1: "the Mathieu conjecture is FALSE for SU(3) (and for SU(N), N >= 3)". Restated:
  false for SU(2) (Long) and for SU(N), N >= 24; not decided for 3 <= N <= 23 by the located
  proofs.
- EXP-016 item 2: "GMC is false (at some finite dimension tied to the failing JC dimension)".
  Restated: false for every n >= 3, true for n = 1, n = 2 proof claimed.
- EXP-016 item 5 and the first bullet of its "Corrections to our record": "JC(4) is false by
  EXP-001 + dummy coordinates, hence Dixmier(2) is false; the smallest failing Weyl rank is
  between 1 and 2, with Dixmier(1) still open". Restated: DC(n) false for n >= 3; ranks 1 and 2
  open; the smallest failing rank is 1, 2 or 3.
- EXP-018 item 1, the parenthetical "(as with Dixmier, where rank 1 stays open)". Restated:
  indices 1 and 2 open for both.
- EXP-018 status board, rows Mathieu, Dixmier, Poisson and Gaussian moments: replaced by the
  board below.
- EXP-016 and EXP-018, "How could this be wrong?": "only the implication DIRECTIONS carry
  weight". The dimension indices carry weight as well; misreading one of them is the error this
  experiment corrects.

## The status board (supersedes the EXP-018 board; rows marked * restated here)

| Statement | Status on 2026-09-18 | Chain, with the indices as located |
|---|---|---|
| Jacobian conjecture / Smale 16 | false for N >= 3; N = 2 open | the counterexample (EXP-001) |
| Mathieu conjecture* | false for SU(2) (explicit; Long 2026, preprint) and for SU(N), N >= 24; SU(N) for 3 <= N <= 23 and the other groups not decided | Mathieu(SU(N)) => every Keller map x - h of C^N with h homogeneous is invertible (Zwart, Thms 4.16, 4.23); the 24-variable cubic-homogeneous form (EXP-041) |
| Dixmier conjecture* | false for every rank n >= 3; ranks 1 and 2 open (a proof of rank 1 is claimed: Zheglov, preprint) | DC(n) => JC(n); JC(2n) => DC(n) |
| Poisson conjecture* | false for every index n >= 3 (2n variables); indices 1 and 2 open | JC(2n) => PC(n) => DC(n) => JC(n) |
| Gaussian moments conjecture* | false for every n >= 3 (explicit; Long 2026, preprint); true for n = 1; n = 2 proof claimed (Wilson 2026, preprint) | GMC(n) for all n => JC (DEZ); explicit P3, Q3 (Long) |
| Zhao vanishing conjecture | false; explicit witness in 48 variables (EXP-041) | vanishing (all n) <=> JC (all n) |
| Image conjecture | false in some dimension | Image => vanishing |
| Symmetric / gradient JC | false; explicit witness in dimension 48 (EXP-041) | symmetric JC <=> JC (stably) |

## Adversarial validation record

- **Route 1 (independent re-derivation).** The Part A closure was re-derived by hand for
  n <= 4. The only implications touching DC(2) are DC(2) => JC(2) (JC(2) unknown),
  JC(4) => DC(2) (premise false: no information), PC(2) => DC(2) (PC(2) unknown),
  DC(n) => DC(2) for n > 2 (premises false: no information) and DC(2) => DC(1) (DC(1)
  unknown); nothing decides DC(2). The same holds for PC(2). Part B's Groebner result is
  reproduced by the substitution certificate B3, which does not use the Groebner routine.
  Part C re-parses the hash-matched EXP-041 input with fresh code. Parts D and E use
  closed-form moment rules and do not reuse any step of the authors' proofs.
- **Route 2 (source attack).** Each index was read from the statement in the body of the paper,
  not from an abstract alone. For Mathieu, seven statements of the implication were collected
  (`artifacts/sources.md`). Six state it without a fixed dimension ("for all compact connected
  Lie groups", "for all n"). Zwart's Theorem 2.2 and Corollary 4.24 state the fixed-dimensional
  form for general maps, and Zhang's note cites Theorem 2.2 for it. Zwart's proof supplies the
  fixed-dimensional statement only for maps x - h with h homogeneous, and passes to general
  maps through Theorem 4.4, whose Bass-Connell-Wright reduction adds variables.
- **Route 3 (bounded search pass, 2026-09-18).** Queries on Dixmier ranks 1 and 2, GMC(2), and
  the Mathieu conjecture for SU(3) and SU(N). Found: Long, arXiv:2607.19012 (SU(2) false,
  explicit); Wilson, arXiv:2607.23887 (GMC(2) proof claimed); Zheglov, arXiv:2410.06959v5
  (Dixmier(1) proof claimed). Nothing was found on SU(N) for 3 <= N <= 23, on DC(2), or on
  PC(1) and PC(2). The Wikipedia article on the Jacobian conjecture agrees with Part A for
  Dixmier and Poisson.
- **Observation.** Long's fixed-dimensional reading of the Derksen-van den Essen-Zhao proof (a
  non-invertible cubic-homogeneous Keller map in r variables forces the failure of GMC(2r))
  applied to the 24-variable form of EXP-041 gives the route-based failure of GMC(48), against
  the GMC(158) that Long derives from F by his own reduction count. It adds nothing to the
  status, since GMC(n) fails explicitly for every n >= 3.

## How could this be wrong?

- Mathieu's 1997 paper was not located. If it contains a dimension-preserving argument for
  general Keller maps, F would decide SU(N) for 3 <= N <= 23 and the EXP-016 statement would
  hold for those N. The restated row claims only what the located proofs support.
- The bound N >= 24 rests on Zwart's rendering of Mathieu's Theorems 5.3 and 5.4 as
  statements at fixed N for the homogeneous form. If that rendering fails at fixed N, only the
  stable statement remains: the Mathieu conjecture fails for SU(N) for some N.
- Part B excludes F only. A non-invertible Keller map of homogeneous type in some dimension
  below 24 would lower the Mathieu bound; none is known to this record.
- Long's two papers, Wilson's and Zheglov's are preprints. Parts D and E check Long's explicit
  identities for finitely many powers. Wilson's and Zheglov's proofs are not verified here.
- The closure uses only the located implications. A result not located here, for instance a
  direct proof or disproof of DC(2), would change an undecided entry.

## Consequences

- Record: the cascade paragraph of `wiki/01-statement-and-history.md`, the EXP-016, EXP-018
  and EXP-136 rows of `wiki/05-experiments.md`, the web cascade table (export stage and baked
  payload) and the Jacobian page text are restated from the board above.
- Manuscripts: the cascade and foundational papers take the Mathieu, Poisson and Gaussian
  moments statements from this board.
- Queued, not started: a search for a non-invertible Keller map x - h of homogeneous type in
  dimension below 24 (it would lower the Mathieu bound); an in-house check of Wilson's GMC(2)
  argument.
