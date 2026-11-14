# EXP-012 verdict: CONFIRMED; the pipeline is exact at the production parameters

Date: 2026-11-14. Hypothesis frozen at 78cc42fb before any computation.

## Result [MV]

| Gate | What | Scope | Outcome |
|---|---|---|---|
| F | provenance | filter2 and geng_a3 to geng_a7 rebuilt from the committed sources (`artifacts/provenance.txt`) | all six byte-identical to the production binaries |
| A | filter on constructed graphs | 3,519 graphs, orders 10 to 24, alpha 1 to 12, kappa 0 to 22; 26,005 decisions at (alpha +- 1, kappa +- 1), k' <= 9 | 0 disagreements with NetworkX |
| B | filter on production streams | the 11 triples with k >= 6 or alpha = 7, E = c-1, c, c+1; 21,196 graphs in 33 slices | 0 disagreements; no graph above the alpha bound |
| C | prune hook alone | 3,876 graphs x bounds 2 to 8 = 27,132 decisions | 0 disagreements |
| D | res/mod split under the hook | (17,5,3) E=29, (19,3,6) E=60, (20,4,4) E=48 | one part and the union of 56 parts byte-identical (sorted) |
| E | generator counts | A001349 n = 9, 10; A002851 at 16, 18, 20, 22 vertices; A006820 n = 12 to 15 | 10 of 10 equal |

## Deviations from the hypothesis, all recorded

- Gate F, the filter2 build line: the hypothesis said `gcc -O3`, but the recorded build line (EXP-006 verdict) is
  `gcc -O2`, and `build.sh` uses the recorded one. The `geng_a<A>` binaries match only with nauty's makefile CFLAGS
  (`-O4 -mpopcnt -march=native`). The line in `prune_alpha.c`'s header uses `-O3` without `-mpopcnt` and `-march=native`, and gives other
  bytes.
  Both rebuilds are recorded.
- Gate B, the slice sizing: the first sizing by graph count made one slice the whole run of an expensive edge count,
  and the run was stopped. The resumed run sized slices by recorded CPU time. 19 of the 33 slices came out empty
  (corrected on 2026-11-14 from "12", after the independent review), because a slice is a fixed part of the generation
  tree. The 14 nonempty slices cover:
  - k = 6 at (19,3,6) E = 59, 60, 61; (20,3,6) E = 65, 66; (21,3,6) E = 71; (22,3,6) E = 78, 79, 80;
  - k = 7 only at (22,3,7), E = 82 = c + 1, which is not a production edge count;
  - alpha = 7 at (22,7,3) E = 34, 35 and (23,7,3) E = 37, 39.
  No slice at order 24 and no production edge count with k = 7 is covered; there the filter rests on its proofs and
  on Gate A (constructed graphs up to order 24, k' <= 9).
- Gate D, first run: parallel parts written into one pipe interleaved lines, giving different hashes for equal
  counts. That run is kept as `artifacts/gate-d-first-run-harness-defect.json`. With one file per part the outputs
  agree byte for byte. A separate probe confirmed this on (17,5,3).
- Gate E, first run: `wsl.exe -- bash -c` re-parses its argument, so `$1` in the awk program was expanded, and every
  count read -1. That run is kept as `artifacts/gate-e-first-run-parse-defect.json`. The harness now uses
  `wsl.exe --exec`.
  - The stopped first run's Python process kept running and wrote into the same log file, so the log
    `artifacts/gate-e-run-log-interleaved.txt` mixes both runs.
  - `artifacts/gate-e.json` holds only the corrected run.

## Reading

- Both predictions hold:
  - the binaries are byte-identical to the committed sources once the correct flags are used;
  - Gates A to E show zero disagreements.
- The filter was validated before only at order 8, k <= 5, alpha <= 6. It is now validated at the production orders,
  at k = 6, 7 and at alpha = 7.
- The hook and the res/mod split are validated directly. The generator's completeness is validated against OEIS up to
  22 vertices.
- No published count exists for the restricted classes the search enumerates. Their completeness rests on the
  generator together with the hook's soundness lemma, which Gate C tests.
