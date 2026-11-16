# EXP-147 verdict - CONFIRMED: GGHV Theorem 5.1 applies to every polygon class of Proposition 4.2, so the (9,24) case is discarded by the printed theorem

Date: 2026-11-16. Hypothesis frozen at `4d26fbdf` (pushed before any code of this experiment ran). Backlog JCB-107.
Instrument: `run.py` (exact integer geometry, Python 3.13.14, standard library only); `run.py` exits 0;
`artifacts/results.json` (SHA-256 17ae3e01...3b553171) and `artifacts/run-log.txt` carry every value.

## Result

For each of the three classes of GGHV 2022 Proposition 4.2 (the case A0 = (9,24), (m,n) = (2,3), max deg 99), the
polynomials P and Q satisfy the three hypotheses of Theorem 5.1 as printed: [P,Q] = x is x + g(y) with g = 0; P and Q lie in
K[x,y] (every corner of N(P) and N(Q) has nonnegative coordinates, and P, Q are in L^(1) = K[x, x^{-1}, y] with support in
those polygons); and the starting and end points are the required ones. Theorem 5.1 therefore excludes every class, so the
(9,24) case of the floor (Theorem 2.1) rests on a printed theorem and needs no unprinted bridge.

| class | N(P) after (6,18) | (-1,1)-face of P | N(Q) after (9,27) | (-1,1)-face of Q | successor of (1,0), P and Q | A1 | A3 | A4 |
|---|---|---|---|---|---|---|---|---|
| 1 | (0,12) | edge (6,18) to (0,12) | (0,18) | edge (9,27) to (0,18) | (-1,1), (-1,1) | yes | yes | yes |
| 2 | (0,6) | vertex (6,18) | (0,9) | vertex (9,27) | (-2,1), (-2,1) | yes | yes | yes |
| 3 | (0,0) | vertex (6,18) | (0,0) | vertex (9,27) | (-3,1), (-3,1) | yes | yes | yes |

In every class the (3,-1)-face of N(P) is the edge from (1,1) to (6,16) and its (1,0)-face the edge from (6,16) to (6,18),
so en_{3,-1}(P) = st_{1,0}(P) = (6,16) and en_{1,0}(P) = st_{-1,1}(P) = (6,18); for N(Q) the edges run from (1,0) to (9,24) and
from (9,24) to (9,27), so en_{3,-1}(Q) = st_{1,0}(Q) = (9,24) and en_{1,0}(Q) = st_{-1,1}(Q) = (9,27) (`results.json`,
`classes.<k>.P.faces`, `classes.<k>.Q.faces`). Every computed pair satisfies GGV1's cross-product rule
(`cross_rule_ok` true in every class).

## The derivation, by hand [D]

The starting point st and end point en of a face are the first and last points of that face met when running counterclockwise
along the boundary of the Newton polygon (GGV1, arXiv:1401.1784, Notation at lines 368 to 372); equivalently, for a face that
is an edge, (rho,sigma) x (en - st) > 0 (GGV1, Remark at lines 381 to 386). Run counterclockwise, the polygons of
Proposition 4.2 visit (0,0), (1,1), (6,16), (6,18) and then (0,12), (0,6) or nothing before returning to (0,0) (for N(P)), and
(0,0), (1,0), (9,24), (9,27) and then (0,18), (0,9) or nothing (for N(Q)). The edge from (1,1) to (6,16) has outward normal
(3,-1) and is met in that order, so its end is (6,16); the vertical edge from (6,16) to (6,18) has normal (1,0) and is met from
(6,16) to (6,18); the next edge has normal (-1,1), (-2,1) or (-3,1), so the (-1,1)-face starts at (6,18): it is the next edge
in class 1 and the vertex (6,18) in classes 2 and 3, whose next normals lie beyond (-1,1) counterclockwise. The same walk on
N(Q) gives (9,24) and (9,27). This is exactly what Corollary 5.7 had to establish by a shift of x for the (9,27) case
("Succ(1,0) >= (-1,1)", lines 1799 to 1811); for the (9,24) classes no shift is needed.

## Predictions and controls

| item | outcome | evidence |
|---|---|---|
| A1 to A4 in all three classes (prediction, confidence 0.95) | CONFIRMED | `classes.<k>.theorem_5_1_applies` true for k = 1, 2, 3 |
| K1: Corollary 5.7's polygon before its shift fails A3 with st_{-1,1}(P) = (0,18) | behaves as declared | `controls.K1_cor57_unshifted` |
| K2: the paper's usage at line 380, st_{1,0} = (8,28) on the face from (8,28) to (8,32) | behaves as declared | `controls.K2_line380_st` |
| K3: the clockwise walk (orientation mutant) fails A3 and A4 in every class | behaves as declared | `controls.K3_clockwise_mutant` |
| K4: a planted polygon whose (-1,1)-face is the vertex (2,18) fails A3 | behaves as declared | `controls.K4_planted` |

K1 and K2 tie the instrument to the paper's own usage: the convention that makes Theorem 5.1 hold for its intended
application (Corollary 5.7 after the shift) and makes line 380 true is the counterclockwise one, and K3 shows the result
depends on it.

## Sources (archived in the data root, `jacobian-conjecture/sources/gghv/`, `SHA256SUMS`)

- arXiv:2204.14178v1 e-print, `2204.14178.tex` (SHA-256 fd8cf496...be5116bf): Proposition 4.2 lines 668 to 680, Theorem 5.1
  lines 1402 to 1409, Corollary 5.7 lines 1788 to 1811, the direction-order note line 380, the case table lines 304 to 320.
- arXiv:1401.1784 (GGV1) e-print, `1401.1784.tex` (SHA-256 b4908fd5...0e6004d5): the definitions of st, en,
  successor and predecessor.
- arXiv:1708.07936 (GGHV17) e-print, `1708.07936.tex`: line 1246, the end point of a (rho,sigma)-homogeneous element with
  rho > 0 is its monomial of greatest degree in y (the same convention).
The PDFs and the gzip e-prints are archived next to the extracted sources, all hashed.

## Scope, and how could this be wrong?

- Checked: that the hypotheses of Theorem 5.1 hold for the three classes as printed. Not checked: the proof of Theorem 5.1,
  the exhaustiveness of Proposition 4.2 or of the case table, or any other row of the floor (Theorem 2.1 as a whole).
- The convention: GGHV 2022 says it uses the order on directions of GGHV17, opposed to GGV1's (line 380). The order on
  directions changes how directions are compared, not which point of a face is met first on the counterclockwise walk; the
  paper's own statements (Theorem 5.1 for Corollary 5.7, line 380) hold only under the counterclockwise reading (K1, K2,
  K3). A different reading would make Theorem 5.1 vacuous for the case it was written for.
- The polygons are those printed in Proposition 4.2; a transcription error there would change nothing here only if the
  printed corners are what the proof produces, which this experiment does not re-derive.

## Consequences

JCB-107 is closed: the floor statement no longer inherits the (66,99) bridging gap recorded by the audit of 2026-07-22
(dossier `context/2026-07-22-beyond125-and-audit-dossier.md`, D1 and item 6). The exclusion of (72,108) (EXP-137, EXP-146) and
GGHV Theorem 2.1 then give max deg >= 125 for a counterexample to JC(2), conditional on Proposition 4.3 being exhaustive and
on the encoding of its polygons, and on the rest of GGHV's printed argument.
