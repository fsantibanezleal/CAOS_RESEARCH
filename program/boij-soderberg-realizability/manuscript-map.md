# Boij-Soderberg realizability in three variables: result and manuscript map

Updated 2026-11-19. This map separates mathematical evidence, strategic value, manuscript coverage and external novelty
(methodology 13). Experiment verdicts remain the authority for every count and statement.

## Status boundary

Question 6.1 of Erman and Sam (arXiv:1606.01867) is already answered negatively over every field: Jiang, Li, Sun, Wang,
Xiao and Yu (arXiv:2605.25259, Theorem 3.7) give (1,2,9,8) on (0,6,20,21), excluded over k[x,y,z] by Krull's theorem and
over U(H) by a parity test; their Theorem 3.8 answers Question 6.2. Boocher, Huang and Wolf (arXiv:2512.24320) classify
the rays with two generators over the polynomial ring. The pure modules over U(H) given by Kostant's theorem are stated
by Erman and Sam and announced by Sam. The obstructions used over k[x,y,z] are published ones. None of this is ours.

The CAOS programme contributes explicit modules and exact computations: an infinite family of pure modules over U(H)
with its sharp characteristic condition, a point whose realizability depends on the characteristic, the table of the
rays with d3 <= 12, and the least d3 of a counterexample in characteristic 0. Internal exact validation and two internal
reviews do not establish peer review or worldwide novelty; the searches of 2026-11-19 are recorded in the literature
pass and in the review records, and a negative search is not a proof of novelty.

## Result blocks

| block | experiments | result status | value | manuscript home |
|---|---|---|---|---|
| U(H)/U(H)(x^e, y^e) has the pure resolution of type (0, e, 3e, 4e) with table (1,2,2,1) if and only if the characteristic is 0 or at least 2e; Hilbert series, socle, structure over k[z] | EXP-002, EXP-003; derivation in the context note | proved on paper, reviewed by an independent reader (correct after minor fixes, applied); machine-checked for e <= 8 over the rationals and for the primes up to 23 at e <= 5 | an infinite family of pure modules over U(H) outside the Kostant family, on rays excluded over k[x,y,z] | BSR-F2 (not yet written) |
| The point (1,2,2,1) of (0,2,6,8) is realized over U(H) in characteristic 0 and in every odd characteristic and over neither ring in characteristic 2 | EXP-003 (and EXP-002) | proved on paper for every field of characteristic 2, reviewed; exhaustive over GF(2) and GF(4); explicit pairs in characteristic 3 and at least 5 | the answer to Question 6.1 on a point that passes the parity test depends on the characteristic | BSR-F2 |
| In characteristic 2 a module with a generators in degree 0 and at most a + 1 relations, all of one degree e >= 2, never has finite length over U(H); so the point (1,2,2,1) of (0, e, 3e, 4e) is realized over neither ring for every e >= 2, and the point of (0,2,10,12) is excluded | derivation in the context note (2026-11-19-characteristic-two-general); EXP-003 for the three observed rays | derived on paper, under review (backlog BSB-017); its three predicted eventual Hilbert functions (2, 4, 6) agree with the EXP-003 artifacts | an infinite family of rays on which the answer to Question 6.1 depends on the characteristic | BSR-F2, after the review |
| All ten rays with d3 <= 12 that pass parity and are excluded over k[x,y,z] are realized over U(H) in characteristic 0 (Kostant modules, the family above, 2 by 3 matrices of quadrics on (0,2,10,12)) | EXP-002 | confirmed by two instruments over the rationals | in characteristic 0 a counterexample with d3 <= 12 lies on a parity-failing ray | BSR-F2 |
| The table over k[x,y,z] for the 220 rays with d3 <= 12: primitive point realized on 193 (147 in characteristic 0), excluded on 12 (least multiple 2 on each), open on 15 | EXP-001 | confirmed; every hit recomputed in a second system; 64 of 66 completed rational rechecks pass | the least realizable multiple on 205 rays; the search space left | BSR-F2 |
| In characteristic 0 no counterexample to Question 6.1 has d3 <= 9; (0,4,9,10) and (0,1,6,10) are counterexamples with d3 = 10 over every field | EXP-001, EXP-002 | machine-verified modules plus cited constructions; the exclusion over S is Erman's (2009), the half over U(H) is the parity test; reviewed 2026-11-19 by an independent reader (correct after fixes, applied; all 29 explicit modules recomputed over QQ in a second system) | the least d3 of a counterexample in characteristic 0 is 10, against 21 in print | BSR-F2 |
| A general pair of forms of degree e >= 4 is not pure; characteristic 2 on (0,3,9,12) and (0,2,10,12); the substitution in the Kostant presentations | EXP-003 | machine observations and open questions | candidates for further characteristic-dependent points | research record; BSR-F3 |

## Manuscripts

None yet. The first manuscript is the current focus BSR-F2 (route
`manuscripts/boij-soderberg-realizability/primitive-points-realizability`); `manuscripts` is an empty list in
`research-governance.json` until it is published.

## Focus record

| focus | status | what it decides |
|---|---|---|
| BSR-F1 | closed (gate met 2026-11-19) | the table for d3 <= 12 and the least counterexample in characteristic 0 |
| BSR-F2 | active (current) | the first manuscript |
| BSR-F3 | proposed | the open rays and the open characteristic questions |

## Experiment dispositions

EXP-001 to EXP-003 are research records until the manuscript of BSR-F2 is published; they become its primary evidence.
