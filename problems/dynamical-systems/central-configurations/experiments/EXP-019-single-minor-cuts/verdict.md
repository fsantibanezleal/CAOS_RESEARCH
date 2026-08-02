# EXP-019 - Verdict: SMOKE CONFIRMED, BOTH SINGLE-MINOR CUTS INCONCLUSIVE-CAP (2026-08-02; the CM/Krull reduction stands as mathematics; the Groebner refusal is now measured down to a 32-term increment)

Hypothesis: `hypothesis.md`. Runner: `run.py`. Artifacts: results, run log,
the two capped scripts.

## Outcomes

| Rung | Outcome | Facts |
|---|---|---|
| Smoke (three minors nonzero at the rank-4 witness W1) | PASS | g4 has 377 terms, the two chosen 3x3 minors 32 terms each; all exactly nonzero at W1 |
| P1 (dim(SH + g4) <= 3, closes k = 4) | INCONCLUSIVE-CAP | 1800 s inner cap spent |
| P2 (dim(SH + g3) = 3, first k = 3 cut) | INCONCLUSIVE-CAP | 1800 s; P3 not reached by design |

## What stands and what is measured

The mathematical reduction is UNAFFECTED and remains the endgame's frame:
the shape ideal is a complete intersection (dim 4 = 13 - 9), hence
Cohen-Macaulay and unmixed, so single-polynomial dimension drops close
k = 3 and k = 4 without any component identification. What is now measured
is that Singular's std refuses even a THIRTY-TWO-TERM increment over the
one-second shape basis at half an hour: the mixing of the cleared minor
(degrees near 50 in the distance cubes) with the quadric tower is the
hard step, consistent with every prior wall.

## Declared continuations (next round)

1. MOD-P SCREEN FIRST on exactly these two systems (SH + g4, SH + g3),
   two primes, 300 s: if mod p completes, ONE overnight QQ run (declared
   6-12 h budget) is justified; if mod p walls, no human budget will do
   and route 2 is the path.
2. The closed-form route that has been winning: bordered-minor identities
   at the 3x3 level (the k = 3 case needs only TWO successive proper cuts,
   and properness can come from exact witnesses instead of Groebner
   dimensions, exactly as pieces 4 and 5 did at the 2x2 level). The
   borders of the piece-2 anti-diagonal corner inherit its clean entries;
   their brackets are the objects to tame by hand plus machine identity
   checks.
3. k = 4 keeps its two routes (a rank-4 CC witness, or the overnight cut
   if the screen approves).

## Soundness notes

- Caps enforced by timeout; the 1964/1960 s walls are cap plus WSL
  overhead; no partial output was parsed.
- The chain scoreboard is unchanged: k = 0, 1, 2 PROVEN; k = 3, 4 open
  with two live routes each.
