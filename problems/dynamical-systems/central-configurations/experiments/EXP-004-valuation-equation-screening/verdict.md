# EXP-004 - Verdict: CONFIRMED, WITH TWO NEW WORKING VALUATION FAMILIES (2026-07-24; the symmetric equations are tropically essential)

Hypothesis: `hypothesis.md` (declared and committed BEFORE any run, commit 1a5fb84).
Pipeline: `run.sh` (16-cell grid), `comet_analysis.py` + `comet_sweep.sh` (exact
per-component pointedness). Artifacts: `artifacts/screening-table.txt` (f-vectors,
global pointedness, timings), `artifacts/comet-table.txt` (per-component verdicts),
inputs and hashes; raw prevariety outputs on `E:\_Datos\...\EXP-004\`.
Environment: gfan 0.7 (EXP-003 build), WSL2, 30 threads, --bits 64.

## Verdict: P2 and P3 CONFIRMED; P1 confirmed in its operational form, with a
## bonus and one honesty caveat. Two NEW working valuation families found.

### The screening table (n = 5, system S1 = asymmetric + symmetric AC + Cayley-Menger)

| Valuations | f-vector | global pointed | comets | comet verdict | time |
|---|---|---|---|---|---|
| V1 powers of 3 (1,3,9,27,81) | 1506 4744 8586 8787 4652 993 | YES | 281 | 281/281 pointed | 225 s |
| V2 squares (1,4,9,16,25) | 3586 12012 18531 15625 7072 1357 | no | 257 | **257/257 pointed** | 362 s |
| V3 powers of 2 (1,2,4,8,16) | 2266 7285 11782 10702 5185 1044 | no | 266 | **266/266 pointed** | 216 s |
| V4 primes (2,3,5,7,11) | 2745 8795 13472 11540 5365 1059 | no | 250 | **250/250 pointed** | 223 s |
| V5 arithmetic (0,1,2,3,4) | 3985 13796 20950 17331 7663 1438 | no | 181 | 180 pointed, 1 UNDECIDED (71 gens) | 379 s |
| V6 repeated (1,1,9,27,81) | 1953 5151 5569 3039 898 109 | no | 211 | 210 pointed, 1 UNDECIDED (95 gens) | 174 s |

### n = 5, system S2 (the ten dependent symmetric equations REMOVED)

Every S2 cell is strictly larger in every f-vector entry than its S1 counterpart, has
300-400+ positive unbounded directions globally, and leaves exactly one UNDECIDED
comet with a huge generator set (241, 289, 289, 289, 401, 2224 generators for V1..V6
respectively). No S2 cell yields a certificate at any valuation, including V1 where
S1 is globally pointed.

### n = 4 (system S1)

| Valuations | f-vector | global pointed | comets | comet verdict | time |
|---|---|---|---|---|---|
| (1,3,9,27) | 44 80 57 14 | YES | 10 | 10/10 pointed | 4 s |
| (1,2,4,8) | 63 119 82 19 | YES | 10 | 10/10 pointed | 2 s |
| (0,1,2,3) | 83 164 108 23 | no | 9 | 9/9 pointed | 2 s |
| (0,0,0,0) | 1 49 66 18 | no | 1 | UNDECIDED (49 gens) | 1 s |

### Predictions

- **P1 (valuation separation law): CONFIRMED in its operational form, with a bonus
  and a caveat.** V3 (powers of 2) is comet-pointed (266/266): a new working family,
  as predicted. BONUS beyond the declared prediction: V4 (primes) is also
  comet-pointed (250/250), so THREE geometric-growth families work at n = 5 where
  the literature published two. The degenerate controls V5 and V6 fail to yield a
  certificate, as predicted, but the honest form of that half is weaker than
  "not pointed": our analyzer returns UNDECIDED on exactly one comet in each case
  (it certifies pointedness by an exact separating vector and unpointedness by an
  exact zero combination; neither was found for those comets). JL25 report that
  valuations (0,1,2,3,4) fail; our data is consistent with that and localizes the
  failure to a single comet, but we do NOT claim a proof of unpointedness. A
  line-certificate instrument (exact LP feasibility for a lineality vector) is
  queued as CCB-032.
- **P2 (the symmetric equations refine): CONFIRMED, in the strongest available
  form.** Removing them enlarges every f-vector entry AND destroys the certificate
  at every tested valuation, including the one where the full system is globally
  pointed. The "redundant" symmetric Albouy-Chenciner equations carry essential
  tropical information: quantitatively, the undecided junk comet grows from 71-95
  generators (S1 controls) to 241-2224 (S2).
- **P3 (n = 4 generic pointedness): CONFIRMED exactly as declared.** Both geometric
  valuations are globally pointed (a purely polyhedral generic-finiteness
  replication for n = 4 in seconds), and (0,0,0,0) resists, exactly as JL25 predict
  for the HM06-equivalent case. Exploratory bonus: (0,1,2,3) is comet-pointed, so
  arithmetic valuations already suffice at n = 4 while they do not at n = 5.

## Second-level validation of the comet instrument

Our comet analyzer independently reports **257 connected components, all pointed**
for the squares valuation at n = 5. JL25 publish exactly 257 components, all comets
with pointed recession cones, for that same computation. This matches a number they
publish that is NOT the f-vector, so it validates the component-extraction logic and
the pointedness certificates, not just the polyhedral computation.

Instrument note (recorded per methodology/03): the first version of the analyzer
merged cones through shared UNBOUNDED rays and reported 245 fused components with 1
undecided; the t = 1 slice only connects through BOUNDED rays. The fix reproduced
the published 257. Both versions are in the git history; the corrected semantics is
documented in the parser docstring.

## Adversarial-validation record

- The published control (V2 squares) matches on two independent invariants:
  f-vector (EXP-003) and component count (this experiment).
- Pointedness certificates are exact: for each comet a rational separating vector is
  produced and verified with `Fraction` arithmetic (all recession generators
  strictly negative on it). Float LP is only used to PROPOSE the vector.
- Negative controls behave as the literature says they should (equal valuations at
  n = 4; arithmetic and repeated valuations at n = 5), which is evidence the pipeline
  is not trivially certifying everything.

## How could this be wrong?

- UNDECIDED is not "unpointed". Our negative-side conclusions are operational
  ("no certificate found"), not proofs. CCB-032 will close this with exact LP.
- Comet extraction depends on gfan's MAXIMAL_CONES_OF_CLOSURE semantics under
  `--usevaluation`; the 257 match is strong evidence the reading is right.
- `--bits 64` was used throughout (as in JL25's reported timings). Overflow is
  detected and aborts (see the consequence below), so silent wrong answers from the
  fast path are not the failure mode; a full arbitrary-precision rerun of the
  positive cells is nevertheless queued as hardening before any claim leaves the
  repo.

## Consequences for the strategy (and an immediate redirect)

1. **The n = 6 run was redirected by this experiment, within hours.** The first
   EXP-005 attempt (powers of 3, `--bits 64`) aborted after 6.5 minutes with
   `gfan::MVMachineIntegerOverflow`: at n = 6 powers of 3 reach $t^{243}$ and exceed
   the machine-integer fast path. Because EXP-004 established that powers of 2 and
   primes also certify at n = 5, the n = 6 attempt now runs two variants in
   parallel: powers of 2 (max exponent 32, fast path) and powers of 3 with
   arbitrary-precision integers (the slower path JL25 describe). Without this
   screening the redirect would have been guesswork.
2. Valuation choice is now a designed variable, not a lottery: three families work at
   n = 5, and the exponent magnitude is an operational constraint at n = 6.
3. Any equation-variant work must ADD equations (Dziobek at n >= 4, e_IU), never
   remove the symmetric ones: P2 settles that direction.
