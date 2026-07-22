# EXP-044 - Verdict: CONFIRMED; Theorem 5 all-degree stands at [D] via the certificate tower (2026-07-22)

Artifacts: `artifacts/output-A-2026-07-22.txt`, `artifacts/output-BCD-2026-07-22.txt`.

## Findings

1. **Window independence [MV-generic].** The NORMALIZED transport constant-class equation
   is IDENTICALLY -2a = 0 at every window N = 5..13 at (2,1,2) and N = 6..11 at (2,2,2):
   the obstruction does not change form as the window grows; only its clearing does.
2. **The clearing law [MV].** The cleared pairing is -c_N a^N with c_N =
   420, 1260, 13860, 180180, 180180, 3063060, 58198140 for N = 5..11; every consecutive
   ratio is a positive rational (3, 11, 13, 1, 17, 19), and from N = 7 on the nontrivial
   ratios are the odd primes 2N - 3 (content normalization occasionally absorbs a
   factor, e.g. the N = 9 step).
3. **THE CERTIFICATE TOWER [MV].** The window-(N+1) cleared certificate, restricted to
   the window-N rows, equals the window-N certificate times ONE common ratio (11a, 13a,
   a at the tested steps), on ALL rows: the certificates form a coherent tower, which is
   the machine form of the induction step for the all-degree statement.
4. **Forward-only injection [D, bookkeeping checked].** Window growth adds unknowns only
   in classes processed BEFORE the constant's row in the ascending sweep; the constant's
   row gains no new unknown, so persistence of the obstruction reduces exactly to the
   tower of item 3.

## Consequence

**THEOREM 5 (all-degree, [D]):** for the staircase family P = x + a x^u y^v + b x^d
(grid-verified shapes), no Keller partner exists at ANY degree for a != 0: the
window-form certificates (EXP-042, sound at every parameter) extend along the coherent
tower, whose ratio is a positive multiple of a at every tested step, and window growth
cannot repair the constant's row. Residual gap to unconditional: a closed proof that the
tower ratio is a nonzero multiple of a for ALL N (verified N <= 11; the 2N - 3 pattern is
the conjectured form). This is now a single sharply-stated lemma (the TOWER LEMMA),
replacing the previous open-ended "closed form of the chain".

## How could this be wrong?

- Part A is generic in (a, b) (fraction-field transport); soundness at every parameter
  value rests on the cleared certificates (EXP-042) plus the tower at tested windows.
- The tower is verified at steps 6->7, 7->8, 8->9 and mirrored by the clearing ratios to
  N = 11; the all-N tower lemma is the remaining [D -> unconditional] step.
