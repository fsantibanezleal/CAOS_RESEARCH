# EXP-004: valuation and equation-variant screening of tropical prevarieties (n = 4, 5)

Declared: 2026-07-24, BEFORE any run. Route: R2/tropical lane (the JL25 frontier).
Backlog: CCB-030 + CCB-031 (screening stage). Builds on EXP-003 (validated gfan
toolchain, exact JL25 reproduction).

## Question

Across mass-valuation families and equation-system variants, which n = 4 and n = 5
tropical prevarieties come out POINTED (the JL25 generic-finiteness certificate
condition), and do the "redundant" symmetric Albouy-Chenciner equations genuinely
refine the prevariety? The goal is an EVIDENCED shortlist for an n = 6 attempt
(JL25's single tried valuation was inconclusive at ~100 cpu-days; ours would be
~2.8 wall-days, spent only on screening evidence, and only after Felipe's go).

## Setup

gfan 0.7 (EXP-003 install, hashes recorded), WSL, 30 threads, --bits 64.
Systems (gfan `_nbody` variants + our substitutions):
  S1 baseline (JL25): asymmetric + symmetric AC + planar Cayley-Menger;
  S2 asymmetric-only + Cayley-Menger (drop the 10 dependent symmetric equations);
Valuation families at n = 5 (applied as m_i -> t^{v_i}):
  V1 powers of 3 (1, 3, 9, 27, 81) [EXP-003 control, pointed globally];
  V2 squares (1, 4, 9, 16, 25) [EXP-003 control, f-vector matched];
  V3 powers of 2 (1, 2, 4, 8, 16);
  V4 primes (2, 3, 5, 7, 11);
  V5 arithmetic (0, 1, 2, 3, 4) [JL25 reports FAILURE: negative control];
  V6 repeated value (1, 1, 9, 27, 81) [symmetry-degenerate control];
At n = 4: S1 with valuations (1, 3, 9, 27), (1, 2, 4, 8), (0, 1, 2, 3), (0, 0, 0, 0)
[the last = the HM06-equivalent hard case per JL25 4.2: negative control].

## Falsifiable predictions

- **P1 (valuation separation law, n = 5, S1).** V3 (powers of 2) yields a POINTED
  prevariety (globally or per-component); V5 (arithmetic) and V6 (repeated) do NOT.
  In words: at least one geometric-growth family beyond JL25's published two
  succeeds, and both degenerate controls fail. (V4 primes is exploratory: recorded,
  not predicted.)
- **P2 (the symmetric equations refine, n = 5).** For at least one valuation where
  S1 is pointed, S2 (asymmetric-only) either loses pointedness or strictly enlarges
  the prevariety (f-vector strictly larger in some entry): the dependent symmetric
  equations do real tropical work (HJ11 kept them for exactly this reason; our
  EXP-002 P1 is the affine-level analog).
- **P3 (n = 4 generic pointedness).** S1 at n = 4 with valuations (1, 3, 9, 27) and
  (1, 2, 4, 8) is POINTED (a pure-polyhedral generic-finiteness replication for
  n = 4), while (0, 0, 0, 0) is NOT (JL25 4.2's reduction to the hard HM06 case).
  (0, 1, 2, 3) is exploratory: recorded.

## Success / failure criteria

SUCCESS: every declared run completes within cap (2400 s at n = 5, 600 s at n = 4)
and P1, P2, P3 hold as stated. FAILURE: any declared prediction refuted (recorded;
a refutation here is itself frontier knowledge: e.g. a pointed V5 would falsify the
separation intuition). Caps produce inconclusive-cap entries, honestly. All
f-vectors and pointedness verdicts persisted per run; the screening table is the
deliverable regardless of pass/fail.

## Method / environment

run.sh (gfan pipelines per grid cell) + check_pointedness.py (EXP-003's exact
parser; per-component analysis via gfan's connected-components output where global
pointedness fails). Deterministic. Artifacts: per-cell f-vectors, pointedness,
timings, hashes; heavy raw outputs to E:\_Datos with a manifest.
