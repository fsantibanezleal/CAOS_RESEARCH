# The (72, 108) closure statement - DRAFT PENDING FELIPE'S VALIDATION (2026-07-22)

STATUS: DRAFT. Nothing here leaves the repository (no outreach, no manuscript claim,
no diffusion) until Felipe validates the phrasing, per 72108-assembly-checklist.md.

## The claim (draft phrasing)

Machine-certified closure of the missing case of the Guccione-Guccione-Horruitiner-
Valqui program: no Jacobian pair of degrees (72, 108) exists. Combined with GGHV
(arXiv:2204.14178, Theorem 2.1), any counterexample to the two-variable Jacobian
conjecture has max degree at least 125: THE VERIFIED FLOOR RISES FROM 108 TO 125.

Division of labor, stated exactly: GGHV's Proposition 4.3 (their reduction, as
published, verified against their LaTeX sources in our transcription dossier) reduces
the case to the existence of P, Q with [P, Q] = x^2 on explicit small Newton polygons
in three branches (cases a, b, c with forced edges); OUR contribution is the exact
machine certificates that these reduced systems are inconsistent across their forced
families.

## The evidence chain (all in-repo, exact arithmetic)

1. Transcription: context/2026-07-22-gghv-72108-dossier.md (tex-line-referenced;
   two source typos flagged).
2. The reduced systems on the bench: EXP-052 (sampled emptiness).
3. The certificate family: EXP-053 (576 pairings), EXP-054/055/056 (the perturbative
   analysis; ten-for-ten honest refutations recorded on the road).
4. The kernel: EXP-057/058 (rank 124; the kernel is the constants; all-orders
   solvability in one line).
5. The forced-family closures: EXP-061 (cases a/b: monomial pairings on two charts;
   vanishing loci excluded by the polygons' own vertex forcing; Q-side covered by
   bigger-polygon emptiness); EXP-062 (case c: the torus gauge normalizes t to 1,
   verified concretely; beta-symbolic pairing 23592960 beta; beta = 0 covered by the
   stratum certificates).
6. The edge verification: the reduced top edge y^8 (xy - t)^8 is the VERBATIM forced
   form under GGHV's stated inversion (assembly checklist, session 36).
7. Interior generality: axis-symbolic certificates (constant pairings; EXP-062/063)
   plus dense multi-coefficient samples (EXP-052/053/055); see Honest residuals.
8. Orientation: the (108, 72) reading is the same reduced object with the bracket
   sign absorbed by Q -> -Q (EXP-063 remark + spot check).

## Honest residuals (must accompany any statement of the claim)

- Interior-coefficient generality is certified AXIS-SYMBOLICALLY (each coefficient
  free with the others sampled) plus densely sampled in mixed directions; the
  fully-simultaneous-symbolic certificate over all interior coefficients at once is
  NOT computed (the EXP-054 lesson forbids extrapolating it). Upgrade paths: the
  perturbative ladder (solvability proved; termination open) or per-point
  finite-cover arguments.
- The claim is conditional on GGHV's Prop 4.3 as published (their reduction is used,
  not re-proved; our dossier verified the transcription, including two typos).
- The H-restricted row pool defines our systems; pool-boundary caveats are recorded
  in the experiment verdicts.

## Proposed next steps (Felipe decides)

1. Validate or amend this phrasing.
2. If validated: the planar manuscript gains the closure section; GGHV contact
   (they explicitly wrote "with enough computing power we would be able to raise it
   up from 108 to 125"): offering them the certificates for verification would be
   the collegial route and would also externally audit the residuals.
3. The interior simultaneous-symbolic upgrade as a hardening task before any
   preprint.
