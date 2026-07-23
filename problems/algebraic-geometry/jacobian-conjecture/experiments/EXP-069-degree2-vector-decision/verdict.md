# EXP-069 stage a - Verdict: all diagonal triples feasible; degree 2 stays OPEN

**Status: DECIDED (stage a). Prediction 2's declared expectation refuted: no
diagonal triple obstructs.**

## Results (artifacts/output-2026-07-23.txt, 13 s)

1. **[MV, PASS]** Setup invariants reproduce EXP-067/068: rank 124, kernel 165,
   51 operators.
2. **[MV, DECIDED; expectation refuted]** ALL 51 diagonal-triple systems
   (unknowns (u_i, v_ii), 125 x 330 affine, per operator) are FEASIBLE mod both
   primes 2147483629 and 2147483587. The level-1 gauge u_i is enough to clear
   the diagonal order-3 condition for EVERY operator, including the 8 that
   blocked degree 1. The declared expectation (the degree-1 obstruction pattern
   persisting) was WRONG: raising the truncation degree gains real power.

## Meaning and the staged follow-up

Degree 2 is NOT closed by the cheap necessary conditions. The decision now
requires the JOINT order-3 system: 23426 triple blocks (125 rows each, about
2.9M sparse equations mod p) in the joint gauge (u: 8415, v: 218790 unknowns),
with all mixed triples coupling up to three v-blocks and two u-blocks. Stage b
(declared): sparse mod-p elimination with early-abort on inconsistency, ordered
so the most-constrained triples (those touching the 8 degree-1 blockers) come
first; a feasible outcome stages an exact confirmation (a degree-2 covector
candidate, upgrade proposal FOR FELIPE); an infeasible outcome closes degree 2
conclusively. If stage b exceeds practical limits, the fallback is the
restricted joint system on the 8 blockers' triple-neighborhood (a further
necessary condition, cheap).
