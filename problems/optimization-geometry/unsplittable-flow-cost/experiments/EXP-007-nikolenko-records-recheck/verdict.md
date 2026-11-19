# EXP-007 verdict: CONFIRMED. The record instances of Nikolenko and De la Fuente force exactly their claimed values, are planar or non-planar as stated, and are optimally priced

Date: 2026-11-19. Hypothesis frozen in commit 4f51d68b before any computation. Exact rational arithmetic throughout
(`ufclib`, which refuses floats; `fractions.Fraction`). Data: `instances.json` of the archive
`sources/nikolenko-2026/` (SHA-256 `b52cf950cbe53cc2a55724b0dab25ec5fde46ceaa8452bb4059c9a1a9583adc9`), transcribed from
the three Zenodo preprints and four repository certificates; the authors' code was never run or imported. Stage R3
and the tests rerun by the coordinating session.

## Outcome per claim

| Claim | Outcome |
|---|---|
| R1 values | Holds on 11 of 11 entries. Each x is a feasible flow, each terminal has exactly two simple paths (enumerated by `ufclib`, compared with the transcription, never taken from it), and alpha_inst with the authors' pricing equals the claimed value exactly: 1282494797984843521/10^18 (UF-K17-RECORD, 131,072 routings, 15 minimizing), 160325086265636045340018727271/(125 x 10^27) (UF-K17-REFINED, 7 minimizing), 12058053/10720000, 3060103/2720000, 182199/160000 and 8867/7800 (four-interval), 58676765987259/(5 x 10^13) (UF-PLANAR-K6), 841/800, 16/15, 25/32, 41209/36992. |
| R2 families | Holds. Four-interval family at t = 3/20, eps = 1/n: alpha_inst = 182359/160000 - 1/n for n = 67, 68, 100, 1000, 10^4, 10^6 (below 9/8 only at n = 67). On the grid t = k/400, 40 <= k <= 80, eps = 10^-6: alpha_inst = (1-t)^2 (1 + 4t - t^2) - eps at all 41 points; the maximum 4558971/4000000 is at k = 60 and lies within 4.4 x 10^-6 below (299 - 41 sqrt 41)/32, compared through exact rational bounds on sqrt 41. Ternary core: alpha_inst = (3 - eta)^2/8 for eta = 1/2, 1/10, 1/100, 1/1000, each below 9/8. |
| R3 planarity | Holds. Both 17-terminal instances are non-planar (a Kuratowski subgraph of 28 edges, a subdivision of K3,3, accepted by the separate checker). The four-interval instances, UF-PLANAR-K6 and the seven-vertex instance are planar (rotation systems with V - E + F = 2). The triangle template and the ternary core, whose planarity the papers do not state, are planar. The repository rotation system of the K6 instance has genus 0 (16 vertices, 21 edges, 7 faces as stored). |
| R4 pricing | The frontier value equals the claimed value on all 11 entries: the authors' cost vectors are optimal for their instances. For the two 17-terminal instances the cutting-plane evaluator finished (13 levels tested each); the claimed value is the largest level proved positive and the next level is proved not positive, with the witness cost vector re-checked by plain enumeration over the 131,072 routings. |

Controls: a 17-terminal entry with one demand changed in its last printed digit no longer gives the claim (two
variants); with the costs zeroed no entry gives its claim; the planarity checker rejects a certificate of another
graph, a rotation system with one edge replaced, and one with two neighbours swapped.

## Verdict

CONFIRMED (P1 to P4). The current lower bounds on the cost-preserving constant, 1.28260069... in general and
1.17353531974518 for planar instances, are reproduced by an exact instrument written before and independently of the
series that holds them, from instances re-entered from the printed sources. The results are their authors'
(S. Nikolenko; the refinement of the general bound by A. De la Fuente); what is added here is the independent check, the
certified planarity statements (including two the papers do not state) and the optimality of the pricing on each
instance.

## Findings beyond the claims

- No record instance forces more than its paper states: re-pricing gains nothing on any of the eleven.
- The repository topology certificate of the K6 instance contains one arc (v8 to v9, with zero flow) that the instance
  printed in the paper does not have; planarity and the face count 7 hold with and without it.
- 9/8 and (299 - 41 sqrt 41)/32 are suprema that no member attains; the members checked approach them as the papers
  state.

## Deviations from the hypothesis

- The 17-terminal values of R1 were computed by a streaming loop with the library's own routing, load and violation
  functions (the library's report object would hold every routing in memory); it agrees with `decide_instance` on the
  small entries.
- The 17-terminal frontier runs used a resumable driver that repeats the library's binary search with a state file.
- Control (a) keeps the flow feasible by carrying the changed demand on one path.
- The hypothesis predicted the counts 16, 21, 7 for the repository certificate; they hold for the certificate as
  stored, which has the extra arc noted above.

## What this does not establish

The theorems of the three papers (the suprema, the class results, the mixture characterization, the open problem on the
factor-two merger constant) are not re-proved. The transcription of the refined 17-terminal instance comes from the
repository certificate, since no paper prints it. The cost convention of the ternary-core figure is assumed (it
reproduces the printed value).

## Consequences

- The preprint revision (UFB-066) states the current bounds with their authors and reports this verification as new
  content, with the planarity certificates and the pricing optimality.
- A new lower bound cannot come from re-pricing the known instances; it needs a new instance or family (the open
  direction named by Nikolenko's Open Problem 11.1 is recorded as UFB-069).

## How could this be wrong?

- A transcription error that both the extractor and this experiment share: the instance file is the common input.
  Guard: every value equals the printed claim to the last digit, and control (a) shows that a change in the last
  printed digit of one demand is detected.
- A shared misreading of the definition (cost-good, violation, normalization by d_max): the seven-vertex instance,
  decided independently by EXP-002 of this programme, gives 16/15 under the same code path.
- The planarity solver is wrong: the answers are accepted only through certificates checked by separate code.
