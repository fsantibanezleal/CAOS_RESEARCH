# EXP-011 - Verdict: CONFIRMED (2026-07-21)

Output: `artifacts/output-2026-07-21.txt`. All predictions verified exactly.

## Established results (ours, exact)

1. **Census rule.** For real targets with $C \ne 0$ off the discriminant surface, the number of
   real preimages of $F$ equals the number of real roots of the fiber cubic: 1 or 3. Two
   independent exact routes (Sturm real-root isolation of $W$ + reconstruction, versus Groebner
   fiber + real-root count) agree at all six sample targets.
2. **Both regions inhabited, sign rule.** $D > 0$ gives 3 real preimages (e.g. the collision
   target $(-16, -16, 1)$); $D < 0$ gives 1 (five samples). The discriminant surface
   $27A^2C^2 - 18ABC + 16A + B^3C - B^2 = 0$ is the real wall between the 3-sheet and 1-sheet
   regions.
3. **Real surjectivity (grid-certified).** No empty real fiber on a 36-target rational grid;
   structurally [D]: the fiber cubic is odd-degree with constant leading coefficient, so a real
   root always exists, and off the wall all roots are simple hence reconstruct finite real
   preimages; the $C = 0$ plane keeps the flat-sheet point.
4. **Recorded corollary.** $F|_{\mathbb{R}^3}$ is a surjective, orientation-reversing
   ($\det = -2 < 0$), non-proper, NON-INJECTIVE real Keller map: the constant-Jacobian real
   statement in dimension 3 falls with the same example. (Immediate from the announcement's
   rationality plus EXP-001; Pinchuk's 1994 planar counterexample concerned the non-constant
   case. Not claimed as a novel discovery; recorded with the census quantifying it.)

## Adversarial validation record

- Route 3 (cross-implementation agreement): the $w$-route and the Groebner route are
  independent computations (different eliminations, different root isolations); they agree on
  every target.

## How could this be wrong?

- The surjectivity claim beyond the grid rests on the odd-degree argument [D]; the grid
  certifies it at 36 points. Boundary strata ($D = 0$) were exhibited in EXP-007 (deficient
  but nonempty); a full stratified census of the wall itself (2 real preimages cases) is a
  cheap follow-up if the visualization needs it.

## Consequences

- The web visualization (M3) has its exact data model: the discriminant wall separating the
  1-region from the 3-region, the collision pairs living in the 3-region, and escapes on the
  wall. All artifacts can be baked from these exact scripts.
