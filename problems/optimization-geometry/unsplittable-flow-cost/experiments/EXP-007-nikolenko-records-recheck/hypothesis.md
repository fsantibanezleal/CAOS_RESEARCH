# EXP-007 preflight: independent exact re-check of Nikolenko's record instances, their planarity and their pricing (UFB-068)

Date: 2026-11-19. Status: frozen before any computation of this experiment. CPU only, exact rationals.

## Question

S. Nikolenko's three Zenodo preprints (10.5281/zenodo.21701162, 21716713, 21922203; 2026-07-30 to 2026-08-13) and the
repository snikolenko/unsplittable-flows (HEAD a8324b31, with A. De la Fuente's refinement in PR #1) hold the current
lower bounds on the cost-preserving single-source unsplittable-flow constant: 1.2824948 and 1.28260069 in general,
(299 - 41 sqrt 41)/32 = 1.139747 and 1.17353531974518 for planar instances, and the exact means E(3) = 9/8 and E(4).
Every value is certified by the author's own verifiers; no external check is named
([refresh of 2026-11-19](../../context/2026-11-19-literature-refresh.md)). Three questions:

1. Do the instances, re-entered from the papers and certificates and run through the CAOS exact library `ufclib`
   (written before and independently of that series), force exactly the claimed values?
2. Is each instance planar or non-planar as the papers state, by a test whose answer carries a checkable certificate?
3. Is the pricing of each instance optimal: does the frontier value (the forced violation maximised over all
   nonnegative cost vectors) equal the claimed value, or exceed it?

## Sources and data (data root `caos-research/unsplittable-flow-cost/sources/nikolenko-2026/`, SHA256SUMS there)

`instances.json` (13 entries: 11 concrete, 2 parametric), transcribed on 2026-11-19 from the three PDFs and four
repository certificates, each entry with its page, theorem or file; the author's code was read as text and never run or
imported (private management mirror, `wip/caos-research/uf-nikolenko-extract-2026-11-19.md`). The transcription was
cross-checked by its extractor with a plain enumeration, which is not this experiment. The run reads the file from the
data root given by `--data-root` or the environment variable `CAOS_RESEARCH_DATA` and pins its SHA-256 in the results.

Entries: UF-K17-RECORD (17 terminals, 67 arcs; Paper II Theorem 4.1 and Appendix A), UF-K17-REFINED (repository
certificate `commonpoint_k17_refined_exact.json`), UF-4INT-n67, -n68, -n1000, UF-4INT-8867 (Paper I, the four-interval
family at t = 3/20, eps = 1/n, and the first certified point), UF-PLANAR-K6 (Paper III Proposition 8.3),
UF-E3-TERNARY-eta1over10 (Paper III Theorem 8.14, cost convention of the figure assumed, marked UNVERIFIED by the
transcription), UF-7VERTEX-16over15 (Paper I Proposition 5.1; the 2026 counterexample of EXP-002), UF-TRIANGLE-n2,
-n68 (Paper I Proposition 5.2), and the parametric UF-4INT-FAMILY and UF-E3-TERNARY-FAMILY.

## Instruments

- `ufclib.Instance` (refuses floats, checks conservation), `enumerate_routings.simple_paths` (own path enumeration,
  never a supplied path list), `decide_instance` (alpha_inst with the stated costs), `frontier_value` and
  `frontier_value_cp` (exact frontier value with a witness cost vector, Bland-rule simplex), all validated by EXP-001
  to EXP-006.
- Planarity: `networkx.check_planarity` (3.4.1) as the solver, and a checker written for this experiment that accepts
  only a certificate: for a planar answer, the returned combinatorial embedding is face-traced and V - E + F = 2 is
  verified on each connected component; for a non-planar answer, the returned Kuratowski subgraph is verified to be a
  subgraph of the instance and, after suppressing its degree-2 vertices, to be isomorphic to K5 or K3,3.

## Claims

- R1 (values with the authors' pricing): for each of the 11 concrete entries, the vector x is a feasible fractional
  flow, every terminal has exactly the paths the source describes (two per terminal on the interval instances), and
  alpha_inst equals the claimed value exactly: 1282494797984843521/10^18, 160325086265636045340018727271/(125 x 10^27),
  12058053/10720000, 3060103/2720000, 182199/160000, 8867/7800, 58676765987259/(5 x 10^13), 841/800, 16/15, 25/32 and
  41209/36992.
- R2 (families): on the four-interval family, alpha_inst at t = 3/20, eps = 1/n equals 182359/160000 - 1/n for
  n in {67, 68, 100, 1000, 10^4, 10^6}; on a grid t in {k/400 : 40 <= k <= 80}, eps = 10^-6, alpha_inst equals the
  closed form of Paper I Lemma 4.6 as transcribed in UF-4INT-FAMILY, its maximum over the grid is attained at
  t = 59/400 or 60/400 and lies in the interval ((299 - 41 sqrt 41)/32 - 10^-4, (299 - 41 sqrt 41)/32), compared by
  exact rational bounds on sqrt 41. On the ternary core, alpha_inst = (3 - eta)^2/8 for eta in {1/2, 1/10, 1/100,
  1/1000}, each below 9/8.
- R3 (planarity): UF-K17-RECORD and UF-K17-REFINED are non-planar; the four-interval instances, UF-PLANAR-K6 and
  UF-7VERTEX-16over15 are planar; the rotation system of the repository's topology certificate for UF-PLANAR-K6 has
  genus 0 by face tracing (16 vertices, 21 edges, 7 faces). The planarity of the triangle template and of the ternary
  core, which the papers do not state, is determined and reported (no prediction).
- R4 (pricing): the frontier value of each concrete entry is computed; where it equals the claimed value the author's
  pricing is optimal on that instance; where it exceeds it, the instance forces more than its paper states.

## Predictions

- P1: R1 holds for all 11 entries (confidence 0.95; the transcription's own enumeration already agreed, so the risk is
  a disagreement between the two readings of cost and violation, which would itself be a finding).
- P2: R2 holds (0.9).
- P3: R3 holds as stated (0.9); the triangle template and the ternary core are planar (0.7).
- P4: the frontier value equals the claimed value on UF-PLANAR-K6, UF-K17-RECORD and UF-K17-REFINED (0.7 each: Paper
  III calls the K6 value an exact hull entry, and the records were found by search over prices), and on the
  four-interval members (0.6). No frontier value exceeds its claim by more than 10^-3 (0.85).

## Consequences fixed in advance

- P1 to P3 hold: the current records are independently reproduced by an exact instrument that predates them; the
  CAOS preprint revision reports this as a verification of others' results, credited to their authors.
- R1 fails on an entry: the entry is re-read on its primary page before anything is concluded; a confirmed mismatch is
  reported with both values and both readings of the definition.
- A frontier value exceeds the claimed value on a record instance: the witness cost vector is re-checked by an
  independent enumeration (every routing that costs no more than the fractional flow, with its least violation) and
  the planarity certificate is attached before any statement; a confirmed excess on UF-PLANAR-K6 or on a K17 instance
  would be a new lower bound, stated with the instance credited to its authors.
- A planarity statement fails: reported with the certificate; the bound that relied on it is flagged.

## What a PASS proves and what a FAIL proves

R1 to R3 are two-sided on the finite instances (exact enumeration decides each value; the planarity certificates
decide each graph). They verify the instances, not the general theorems of the papers (the suprema, the class results,
the mixture characterization), which are not re-proved here. R4 is two-sided per instance when the evaluator finishes.

## Premise dependencies

- `ufclib` decides instances correctly: EXP-001 (hand-built cases), EXP-002 (the 2026 instance), EXP-003 and EXP-004
  (separation LP, frontier value), EXP-006 (cutting-plane evaluator, 37 tests).
- The transcription of `instances.json` is faithful: its entries name their pages; a mismatch in R1 triggers a
  re-read, so a transcription error cannot pass silently as a refutation.
- The normalization of Nikolenko's C equals that of alpha* (refresh of 2026-11-19, skeptic note) [V].

## Budget and kill criterion

R1 to R3: minutes (the K17 enumerations are 131,072 routings each). R4: `frontier_value` on the entries with at most
64 routings (seconds); `frontier_value_cp` on the two K17 instances with a limit of 6 hours each on one process, with
flushed progress and a resumable log of tested levels. If a K17 run reaches the limit, the tested levels are reported
(the largest level proved positive is a certified lower bound on the frontier value, the smallest level proved
non-positive an upper bound) and R4 is stated as that interval.

## Invariant-first note

The value of an interval instance with the authors' pricing is decided by enumeration alone; no cheaper invariant
replaces it. For planarity, the degree test of `ufclib.graphs` (fewer than five vertices of degree at least 4 and fewer
than six of degree at least 3) decides the small instances at once and is recorded next to the certificate.
