# EXP-015 verdict: CONFIRMED: no additive nine-gate seven-rooter anywhere; z_max(9) = 6

Date: 2026-11-05. The hypothesis, the filter library and the engine were committed before the production run;
the production scan finished on 2026-11-05 and its completeness audit passes (6 of 6 checks).

## Result

Over all 1,048,460,912 depth-7 states, all 200 eighth gates on their 10 operands, all 10 operands b and both
signs, that is 4,193,843,648,000 candidates f = t +- b, no candidate has 7 distinct integer roots. There is no
window: the 2-adic and 3-adic divisibility filter of `code/tclib/padic.py` is valid for roots anywhere in Z.

So no 9-gate constant-free program whose last gate is an addition or a subtraction computes a polynomial with 7
distinct integer roots. With EXP-012 (no multiplicative last gate, unconditional) and EXP-011 (z_max(8) = 6, so
a 9-gate seven-rooter's last gate must use the eighth value):

    z_max(9) = 6,   and the least number of gates for 7 distinct integer roots is exactly 10

(the two 10-gate seven-rooters of TCB-032 give the upper side). This removes the window from EXP-013 and closes
TCB-039. The ladder becomes z_max(tau) = 1, 2, 3, 3, 4, 5, 5, 6, 6 for tau = 1..9: a third plateau, at 8-9.

## Stage counts (artifacts/final.json, artifacts/audit.json)

| stage | candidates |
|---|---:|
| all candidates | 4,193,843,648,000 |
| dropped by degree (deg f <= max(deg t, deg b) < 7) | 4,026,692,708,694 |
| pass the 2-adic layer (16 points, mod 2^64) | 3,840,174,256 |
| pass the 3-adic layer (9 points, mod 3^20) | 2,937,472,943 |
| full-zero suspects tested for f == 0 exactly | 498,669,099 |
| identically zero (t = -b or t = b), built exactly | 92,943,826 |
| built exactly and root-counted | 2,345,860,018 |
| seven-rooters | 0 |

Every dropped candidate is dropped by a proof (degree bound, the divisibility lemma, or exact zero); every other
candidate was built exactly and its distinct integer roots counted by the rational root theorem.

## Completeness audit (`audit.py`, 6 checks, all PASS)

1. `artifacts/parts` holds exactly part000.json to part255.json.
2. No record carries an error; each names its own partition.
3. Each partition's SHA-256 and state count equal the EXP-011 manifest (the frontier was copied from the data
   drive marked read-only and every file was hashed before its scan).
4. The states total the manifest's 1,048,460,912.
5. Per partition: candidates = 4000 x states, and the stage counters are monotone.
6. Hits: 0.

## Adversarial validation

- Unit tests (`code/tclib/test_padic.py`, 4 pass): planted k-rooters (k = 4..7, roots up to 5000 in absolute
  value, x-powers, 2- and 3-power content) are never rejected for any m' <= m; random dense polynomials are
  rejected; the modular arithmetic is exact.
- Known-answer gates against building EVERY candidate exactly (`artifacts/gate-output-2026-11-02.txt`):
  k = 4 on partitions 0 and 231 (1535 = 1535, 864 = 864), k = 5 on partitions 0 and 73 (6 = 6, 15 = 15),
  k = 6 on partition 199 (0 = 0); repeated with the production polynomial store (1535 = 1535, 6 = 6).
- Residue tables re-checked against exact Python evaluation on 20,000 random polynomials (0 mismatches); the
  packed polynomial store round-trips all 2,161,049 polynomials exactly.
- Production partitions 0 and 1 were scanned in a trial run with the same code and kept (records identical in
  format; their hashes match the manifest).

## Prediction scorecard

Pre-registered: no additive nine-gate seven-rooter. CONFIRMED.

## How could this be wrong?

- The reduction rests on EXP-011 (the depth-7 frontier is the complete reached set and z_max(8) = 6) and on
  EXP-012; both are earlier verdicts, not re-derived here.
- The divisibility lemma and its table are proved in `code/tclib/padic.py` and tested, but an error in the
  table would drop candidates silently; the known-answer gates at k = 4, 5, 6 would have exposed an error that
  affects those thresholds, not necessarily one specific to k = 7. The k = 7 table is built by the same code.
- The exact zero test is cached by operand ids; an id collision in the store would be an error of the store,
  whose round trip is checked.

## Erratum, 2026-11-14: corrected stage labels

The stage table above (section "Stage counts") labels two rows wrongly, found by the independent audit of census v0.06
(`wip/caos-research/msaudit-misc-2026-11-10.md`, D3 finding 1). The counts are right, the labels are not, and the table
as printed does not add up: 2,937,472,943 - 92,943,826 = 2,844,529,117, not 2,345,860,018. The full counter set of
`artifacts/final.json` (totals) and what `engine.py` counts under each name:

| counter | value | what it counts (engine.py) |
|---|---:|---|
| candidates | 4,193,843,648,000 | 4000 x 1,048,460,912 states |
| deg_drop | 4,026,692,708,694 | dropped by the degree test |
| pass2 | 3,840,174,256 | pass the 2-adic layer |
| pass3 | 2,937,472,943 | pass the 3-adic layer |
| zero_suspect | 498,669,099 | full-residue-zero candidates tested for f == 0 exactly (`Engine._decide`, the `is_full` branch); each was dropped by the exact test |
| zero_exact | 92,943,826 | non-suspects whose exact build is empty (`Engine._decide`, the other branch): the eighth gate t is the zero polynomial, f = +-b, and `_build` returns t without forming f (`Engine._build`); NOT identically zero f |
| exact | 2,345,860,018 | built exactly and root-counted |
| hits | 0 | seven-rooters |

The row "identically zero (t = -b or t = b), built exactly | 92,943,826" should read "eighth gate t is the zero polynomial
(f = +-b), dropped without a root count", and the row "full-zero suspects tested for f == 0 exactly | 498,669,099" is
the set of genuinely full-residue-zero candidates, all dropped by the exact zero test.

Identity: pass3 = zero_suspect + zero_exact + exact, that is 498,669,099 + 92,943,826 + 2,345,860,018 =
2,937,472,943 (checked from `final.json`). Because the engine counts a suspect in `zero_suspect` and, when its exact
build is nonzero, again in `exact` (`Engine._decide`), the identity holds only if no suspect was nonzero; every one of
the 498,669,099 suspects was therefore dropped by the exact test. The exact test drops a candidate when the build is
the empty polynomial, which covers both f == 0 and t == 0.

Soundness of the t == 0 drop: f = 0 +- b = +-b, where b is one of the ten operands, a value of a program of at most
7 gates, so z(b) <= z_max(7) = 5 < 7 (EXP-004). The result of the verdict is unchanged; the `engine.py` module
docstring was corrected on the same date to state this argument.
