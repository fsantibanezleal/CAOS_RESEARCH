# EXP-063 - Verdict: CONFIRMED; the case-c interior axis sweep is COMPLETE (2026-07-22)

Artifacts: `artifacts/output-2026-07-22.txt` (4605 s background; cap discipline noted).

## Findings

1. **[MV]** ALL 44 remaining interior lattice points of the case-c reduced polygon
   admit one-symbol certificates at t = 1 with NONZERO CONSTANT pairings (368640 at
   most points; 2949120 / 1105920 / 737280 at edge-adjacent points; up to
   6957847019520 near the corner): with EXP-062's four points and the trivially-free
   (0,0), the axis-symbolic interior coverage is COMPLETE: every interior coefficient
   is certified free for ALL its values with the others sampled.
2. **[MV]** The orientation spot-check passes (targets x^2 and -x^2 both EMPTY):
   the (108,72) reading adds nothing.
3. Hardening task 1a is DONE. Task 1b (the a/b interior sweep) and the gate (task 2,
   EXP-064, in flight) remain; the amended statement's scope is unchanged until the
   gate decides.

## How could this be wrong?

- Axis coverage only (the audit's central point stands): the simultaneous-symbolic
  statement is exactly what EXP-064 is deciding.
