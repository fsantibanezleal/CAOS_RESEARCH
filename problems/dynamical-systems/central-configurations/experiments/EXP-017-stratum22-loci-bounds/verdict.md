# EXP-017 - Verdict: SMOKES CONFIRMED, ALL FOUR LOCI BOUNDS INCONCLUSIVE-CAP (2026-08-02; the failure is a formulation cost, not a wall: premature elimination inflated the minors; the Dias-Pan-faithful s-variable model is the declared successor)

Hypothesis: `hypothesis.md`. Runner: `run.py` (one serializer fix before any
mathematical outcome: fractions reached Singular as fake rational exponents
and its silent exit-0-after-parse-error faked the OK sentinel; fixed and
committed, error markers now count as failure). Artifacts: all scripts,
outputs, entry sizes, run log.

## Outcomes

| Rung | Outcome | Facts |
|---|---|---|
| P0a (shape dim in the enlarged ghost-free ring) | PASS | dim = 4, two-way agreement, one second: EXP-015 re-verified in the better formulation |
| P0b (matrix cross-validation vs EXP-016 at W1) | PASS | entrywise exact agreement after row-LCM clearing: the enlarged-ring construction is certified correct |
| P1 (dim SH + 4x4 minors <= 3) | INCONCLUSIVE-CAP | full std capped at 300 s; all 13 per-minor subideals capped at 60 s |
| P2 (3x3, <= 2) | INCONCLUSIVE-CAP | full + all 80 subideals capped |
| P3 (2x2, <= 1) | INCONCLUSIVE-CAP | full + all 84 subideals capped |
| P4 (entries, <= 0) | INCONCLUSIVE-CAP | full + all 20 subideals capped |

No bound was met, no bound was refuted: the theorem chain stays OPEN with
the loci route walled at these budgets and in THIS formulation.

## The load-bearing diagnosis

The mass-matrix entries are tiny (2 to 13 terms), but clearing each row by
its inverse-cube denominator LCM multiplies every entry by distance cubes of
total degree about 24, so the 4x4 minors reach degrees near 100 (their
sympy expansion alone took 19 minutes). Dias-Pan faced the identical
structure and did NOT eliminate: their C^32 model keeps the S-quantities as
RING VARIABLES tied by sparse defining relations, so their minors stay
degree <= 6 and their Delta_3 subideal bases completed in minutes on a
laptop. Our EXP-017 unknowingly reproduced the expensive variant of their
choice point. The successor formulation (EXP-017b, to be declared fresh):
adjoin one s-variable per distinct inverse-cube difference appearing in the
block (about 20), with defining relations s * a^3 * b^3 = b^3 - a^3; the
matrix entries become bilinear in (s, heights), minors of the 4x4 have
degree about 8, and the loci ideals become sparse low-degree systems of
exactly the class Singular has been eating in seconds all day.

## Also recorded

- The per-rung cost cartography (13/80/84/20 subideals, all capped) is the
  baseline against which EXP-017b's reformulation gain will be measured.
- The q = v exclusion by saturation (f invertible) worked as designed in
  P0a; the scope discipline holds in the new ring.

## Consequences

1. EXP-017b (s-variable model) is the next declaration; its smoke reuses
   P0b's cross-validation pattern at W1.
2. Nothing in the chain is lost: stages (i) and (ii-rank) stand; the case
   arithmetic is unchanged; only the loci bounds await the leaner ring.
3. The stratum theorem remains genuinely within reach; no statement exists
   yet and none is claimed.
