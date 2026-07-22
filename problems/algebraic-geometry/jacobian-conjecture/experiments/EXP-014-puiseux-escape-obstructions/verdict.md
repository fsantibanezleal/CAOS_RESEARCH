# EXP-014 - Verdict: CONFIRMED; the properness instrument ships (2026-07-22). JCB-022 first contact done

Artifacts: `artifacts/output-2026-07-22.txt`. (Slot note: reserved in session 5, filled
in session 22; experiments 015..040 predate it chronologically.)

## Findings

1. **Properness certificates [MV].** For all 8 library automorphisms, the x-leading
   coefficient of Res_y(P - u, Q - v) and the y-leading coefficient of Res_x are nonzero
   CONSTANTS: exact, one-call properness certificates.
2. **The instrument sees escape [MV].** Control (xy, y): leading coefficient -v, so the
   asymptotic locus lies in {v = 0}, and the exact fiber over (1, 0) is EMPTY: the escape
   branch (t, c/t) tracks the corner ray of the component xy. Control (x^2, y): certified
   proper yet non-injective: properness and injectivity separate without Keller, which is
   exactly why the Keller hypothesis upgrades proper to invertible.
3. **The route [D/C].** JC(2) is equivalent to: every planar Keller map has an empty
   Jelonek set (proper + Keller implies covering of the simply connected C^2, hence
   invertible: classical). The escape picture is the dual of the staircase obstruction:
   a hypothetical counterexample must both manufacture the constant along the staircase
   (EXP-035/037) and carry an escape branch at infinity; the controls show the escape
   direction aligning with a Newton corner ray (observation [C], not a theorem).

## What this changes

- JCB-022 first contact is done; the certificate function is a permanent instrument: any
  future candidate completion gets an immediate proper/non-proper adjudication, which
  (with Keller) is an invertibility adjudication.
- Route status for the evaluation: the properness frame is a REFORMULATION with good
  instruments, not currently a proof engine; its value is cross-checking and the corner
  ray link (potentially connecting Jelonek geometry to the staircase classes).

## How could this be wrong?

- The leading-coefficient test is a sufficient certificate over each chart; a full
  Jelonek-set computation (all components, all charts) was not implemented (first
  contact scope).
- The corner-ray alignment is observed on controls only.
