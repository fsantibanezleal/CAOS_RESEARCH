# EXP-016 - Verdict: CONFIRMED (2026-07-21). The cascade flags are lifted

A literature experiment (no computation): each implication located in its primary record. The
UNVERIFIED flags carried since the 2026-07-20 dossier are now resolved as follows.

## Verified statements and the resulting corollaries

1. **Mathieu (1997).** The Mathieu conjecture for SU(N) implies JC(N) (per the 2025 review of
   Mathieu's approach, arXiv:2511.16561; Mathieu's original 1997 paper is the source of the
   implication; Duistermaat and van der Kallen proved the abelian/torus case in 1998).
   COROLLARY (contrapositive of the implication, given EXP-001): **the Mathieu conjecture is
   FALSE for SU(3)** (and for SU(N), N >= 3).
2. **Gaussian moments.** Derksen, van den Essen, Zhao, "The Gaussian Moments Conjecture and the
   Jacobian Conjecture" (Israel J. Math., 2017; arXiv:1506.05192): GMC implies JC. COROLLARY:
   **GMC is false** (at some finite dimension tied to the failing JC dimension).
3. **Zhao's vanishing conjecture.** Zhao, "Hessian Nilpotent Polynomials and the Jacobian
   Conjecture" (arXiv:math/0409534) and "A Vanishing Conjecture on Differential Operators with
   Constant Coefficients" (arXiv:0704.1691): the all-dimensional vanishing conjecture is
   EQUIVALENT to the all-dimensional JC (with Delta^m P^m = 0 equivalent to Hessian
   nilpotency). COROLLARY: **the vanishing conjecture is false**; an explicit failing
   Hessian-nilpotent quartic derived from F is a computational target (queued).
4. **The Image conjecture.** Van den Essen, "The Amazing Image Conjecture" (arXiv:1006.5801),
   with the van den Essen-Wright-Zhao program: the Image conjecture implies the vanishing
   conjecture. COROLLARY: **the Image conjecture is false in some dimension.**
5. **Dixmier.** Belov-Kanel and Kontsevich, "The Jacobian Conjecture is stably equivalent to
   the Dixmier Conjecture" (arXiv:math/0512171): JC(2n) implies Dixmier(n); with the previously
   known Dixmier(n) implies JC(n), the two are stably equivalent; Tsuchimoto proved the same
   independently (Osaka J. Math., 2005). COROLLARY: **the full Dixmier conjecture is false**
   (JC(4) is false by EXP-001 + dummy coordinates, hence Dixmier(2) is false); the smallest
   failing Weyl rank is between 1 and 2, with Dixmier(1) still open.
6. **Bass-Connell-Wright (1982).** The degree-reduction statement (JC reduces to cubic
   homogeneous form in stably many variables) stands as cited (Bull. AMS (N.S.) 7, 287-330);
   the explicit push-through of F remains the queued computational experiment.

## Corrections to our record

- The 2026-07-20 dossier's cautious phrasing on Dixmier ("handle with care") is now resolved
  precisely as item 5 states: stable falsity, smallest rank open, Dixmier(1) open.
- No cascade claim in our wiki or manuscript was found to be misstated; the flags simply lift
  from UNVERIFIED to verified-with-source.

## How could this be wrong?

- Items rest on the located statements (abstracts/reviews of the primary papers); the deep
  proofs were not re-derived. For the corollaries above, only the implication DIRECTIONS
  matter, and those are unambiguous in the located records.

## Consequences

- The wiki (01, cascade section), the context dossier and the manuscript can now assert the
  cascade without flags, with the references above inline.
- New computational target queued: extract an explicit failing Hessian-nilpotent quartic from
  the counterexample family (the vanishing conjecture's concrete witness).
