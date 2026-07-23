# The (72, 108) closure statement - AMENDED AFTER THE ADVERSARIAL AUDIT (2026-07-22)

STATUS: AMENDED. Felipe validated the prior state (2026-07-22); the commissioned
adversarial audit (context/2026-07-22-beyond125-and-audit-dossier.md, Part 2) then
found the headline OVERCLAIMED relative to its own residuals: Prop 4.3 forces NO
interior coefficients, so the closure must hold for ALL interior values, and
axis-symbolic + sampled coverage does not suffice (our own EXP-054 proved slice
extrapolation fails); the statement also cited EXP-063 before its artifact existed.
The claim below is therefore DOWNGRADED to the certified scope until hardening task 2
(the simultaneous-symbolic certificate) completes. External actions remain gated.

## The claim (AMENDED to the certified scope)

Machine certificates cover the three reduced GGHV branches on their FORCED-EDGE
families with interior coefficients certified axis-symbolically (each free with
others sampled) plus dense mixed sampling: strong evidence toward, but NOT YET a
proof of, the closure of (72, 108). The floor-raise statement (108 -> 125) becomes
assertable ONLY after the simultaneous-symbolic interior certificate (hardening
task 2: via ladder termination, a minor chart cover, or symbolic rank). The audit's
nine ranked hardening tasks (dossier Part 2) are the queue; GGHV outreach is LAST.

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
