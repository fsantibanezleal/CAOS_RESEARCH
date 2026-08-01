# RESUME - Central configurations program (updated 2026-07-24, rounds 1-2 closed; ALL ENGLISH always, incl. chat)

The single first-read for a fresh session (contract: methodology/07-session-handoff.md).

## 1. State in one screen

- **The problem (Smale 6):** for fixed positive masses $m_1, \dots, m_n$, is the number
  of planar central configurations (relative equilibria), up to symmetry, finite? CC
  equation: $\lambda (x_i - c) = \sum_{j \ne i} m_j (x_j - x_i) / r_{ij}^3$.
- **World state (verified 2026-07-23, dossier):** n = 3: 5 CCs (Euler + Lagrange).
  n = 4 planar: FINITE for all positive masses, count in [32, 8472] (Hampton-Moeckel
  2006, BKK, computer-assisted; reproved sans computer by Albouy-Kaloshin 2012).
  n = 5 planar: finite except an explicit codim-2 mass subvariety (AK12, Annals);
  equal masses ARE inside that subvariety and were settled separately (MZ19). Spatial
  n = 5: Moeckel 2001 generic + Hampton-Jensen 2011 explicit exceptional list
  (tropical). n = 6 planar: OPEN, reduced by Chang-Chen (2023-2025) to 24 residual
  zw-diagram cases at codim >= 2 masses. n >= 7: fully open, even generically.
  Roberts 1999: with one negative mass a CONTINUUM exists (positivity necessary).
  Equal-mass rigorous counts n = 3..7 (MZ19, mod rotation+reflection+permutation):
  2, 4, 5, 9, 14.
- **Our state:** program OPENED 2026-07-23; EXP-001 (calibration) DECIDED 2026-07-24:
  the exact AC builder is validated on n = 3 (Euler-Moulton counts exact on 4 mass
  samples; Lagrange identical in symbolic masses; symbolic Euler eliminant degree 54
  persisted); the n = 4 planar HM system is assembled with a recorded profile; the
  equal-mass n = 3 saturated ideal is 0-dim (certificate persisted). THE REFUTATION
  that recalibrates the pipeline: the bare symmetric AC distance system is
  DIMENSION-BLIND (regular tetrahedron a = b = 1 coexists with the square
  a^3 = (4 + sqrt(2))/8, minpoly 32x^6 - 32x^3 + 7, in the equal-mass rhombus
  stratum; planarity = adjoin Cayley-Menger, then the square is unique there). All
  planar statements now run on the ENRICHED system (F + G + e_CM + e_IU). Counting
  instrument of record: the eliminant census (lex-GB univariates + CRootOf + exact
  residual acceptance); sympy solve_poly_system is BANNED from verdict-bearing counts
  (returned incomplete lists; caught by hand-check). Open at cap: P1 saturation for
  unequal masses, P5 full census (instrument upgrade = CCB-007).
- **The working equations** (exact polynomial forms after clearing denominators;
  $S_{ij} = r_{ij}^{-3} + \Lambda$, fix $\Lambda = -1$):
  symmetric Albouy-Chenciner
  $f_{ij} = \sum_k m_k [S_{ik}(r_{jk}^2 - r_{ik}^2 - r_{ij}^2) + S_{jk}(r_{ik}^2 - r_{jk}^2 - r_{ij}^2)] = 0$;
  asymmetric (Roberts) $g_{ij} = \sum_k m_k S_{ik}(r_{jk}^2 - r_{ik}^2 - r_{ij}^2) = 0$;
  Dziobek $h_{ijkl} = (r_{ij}^{-3} - 1)(r_{kl}^{-3} - 1) - (r_{ik}^{-3} - 1)(r_{jl}^{-3} - 1) = 0$;
  Cayley-Menger bordered determinant = 0 for the target dimension; redundant
  $e_{IU} = U - MI$. Source: HJ11 PDF (read); full forms in the method dossier.

## 2. The objects table

| Object | Definition | Owner |
|---|---|---|
| The AC system builder | exact construction of F/G/H/CM/IU over QQ for given n, masses | EXP-001 (being built) |
| Euler quintic (n = 3) | per-ordering collinear eliminant, unique positive root | EXP-001 target |
| The HM n = 4 system | 6 AC f-equations + planar Cayley-Menger in 6 distance variables | EXP-001 assembly; CC-P1 certificate |
| Calibration targets table | published counts/objects our instruments must reproduce | method dossier section 4 |
| zw-diagrams | AK12/Chang-Chen bicolored graphs encoding possible finiteness failures | CCB-003/004 (to transcribe) |

## 3. Experiment index

- EXP-001 ac-calibration: confirmed in part / P7-uniqueness REFUTED / P1-unequal +
  P5 inconclusive at caps. Load-bearing: dimension-blindness of the bare AC system
  (tetrahedron vs square); the eliminant census instrument; the equal-mass saturation
  certificate; the n = 4 profile baseline. Long form: wiki/05 + the verdict.
- EXP-002 enriched-census: confirmed on every decided prediction; P2 inconclusive at
  caps on (1,2,3), (2,3,5). Load-bearing: F + G + e_IU is 0-dim DIRECTLY (no
  saturation; 0.7 s/sample); decided censuses perfectly classical; planar rhombus =
  the square alone; U = M I exact; engine limit measured (sympy census saturates on
  integer-separated masses).
- EXP-003 jl25-prevariety-reproduction: CONFIRMED, exact. Both published JL25 n = 5
  f-vectors digit-for-digit; pointedness independently verified; ~6 wall-min per
  valuation on 30 threads. THE TROPICAL LANE IS OPEN on validated infrastructure
  (gfan 0.7 in WSL, hashes recorded; ~25 cpu-min per wall-min throughput; a JL25-
  scale n = 6 attempt is ~2.8 wall-days here).

- EXP-006 msolve-census: P1/P2 CONFIRMED (both capped censuses closed cross-engine,
  exact box-containment verification, classical answer on four mass vectors),
  P3 REFUTED AS POSED (the n = 4 AFFINE enriched system has dimension 1: the census
  belongs in the torus; class count recorded as untested).
- EXP-007 exact-pointedness: CONFIRMED. All 16 EXP-004 cells decided in 33 s by an
  exact phase-I simplex; zero flips; each failing control PROVABLY unpointed. This
  is now the lane's default decision procedure, including for the n = 6 outputs.
- EXP-008 equation-enrichment: P1/P2 REFUTED, P3 CONFIRMED. Dziobek is tropically
  active (comets 10 -> 7, 9 -> 6) but does not rescue the hard equal-valuation case;
  the comet count, not the f-vector, is the monotone invariant; e_IU is inert.
- EXP-009 torus-census-n4: INCONCLUSIVE-CAP on both exact msolve routes. The
  route-A enriched planar saturation and route-B Hampton-Moeckel z-system each
  ran the declared 3600-second cap with zero output. The exact square smoke test
  passed. Published counts 50 and 4 remain untested by us; direct solving is
  closed at current budgets and the incidence-dimension/BKK routes are promoted.
- EXP-004 valuation-equation-screening: P2/P3 CONFIRMED, P1 operational + bonus.
  TWO NEW working valuation families at n = 5 (powers of 2, primes); JL25's
  257-component count reproduced exactly (comet-instrument validation); the
  dependent symmetric equations are tropically ESSENTIAL (S2 fails everywhere);
  n = 4 generic finiteness replicated in seconds; negatives honestly "no
  certificate" (CCB-032 queued).

## 4. In flight

**EXP-005 (n = 6): a TOOLING barrier, now characterized on four attempts.**

| attempt | arithmetic | outcome |
|---|---|---|
| pow3 (1,3,9,27,81,243) | --bits 64 | ABORT at 6.5 min: `gfan::MVMachineIntegerOverflow` |
| pow2 (1,2,4,8,16,32) | --bits 64 | ABORT: same overflow, despite max exponent 32 |
| pow2 | --bits 0 | ABORT after 15 h wall (about 6 cpu-days): `gfanlib_hypersurfaceintersection.cpp:505 Assertion !cone.isEmpty(mr)` with CircuitTableInteger |
| pow3 | --bits 0 | RUNNING (16 h wall, about 7 cpu-days, no output yet) |

FINDING: gfan 0.7 fails at n = 6 in BOTH arithmetic modes, in two different ways,
and the 64-bit failure is independent of valuation magnitude. The n = 6 barrier we
are hitting is INFRASTRUCTURAL, not a compute-budget question; JL25 report their own
n = 6 computation as completing (and inconclusive), so their run differed in version,
flags or valuation. gfan 0.8beta (author tarball SHA-256
fa7884e5f317c50f8fb4f37bcf5d419f0fd5f7b90d6037349d1957ea73cebbee, binary gfan08
SHA-256 0f177e6a4f7829fc41910ed0395254b2d1e895322bd5705c2c803225bbb5f661) was
VALIDATED on our n = 5 control (exact f-vector match) and CLEARED the first
barrier: it ran hours past 0.7's 6.5-minute abort point. Outreach to the author is
NOT taken without Felipe.

UPDATE 2026-07-25, after a WSL idle-shutdown killed three detached runs (the
0.8beta pow2 run at 1 h 41 m, the 0.7 pow3-b0 run at about 7.5 cpu-days, and
EXP-009's route B): PERMANENT FIX in the WSL user `.wslconfig`
(vmIdleTimeout=-1, memory 26GB, processors 30) plus a keepalive process, `setsid`
launches, and `--saveas` checkpoints in run08.sh. The 0.7 pow3-b0 investment was
NOT restarted on 0.7 (its sibling died at the same assertion class); pow3
continues on 0.8beta.

UPDATE 2026-08-01 (evening): EXP-011 DECIDED: smoke and cap-signature
confirmed, emptiness and partial-GB rungs FAILED TO SCALE at declared budgets
(all probes capped at 300 s; pgb 1/15 completers, vacuous d_pgb = 10; no
refutation of dim = 4; the 6-to-10-variable wall measured). ENGINE LESSON:
Dias-Pan ran the same pattern in minutes on Singular; CCB-037 v2 = swap the GB
engine to msolve -g (installed) + product-pair menu; CCB-034 witness sets
promoted to the next instrument spike. SAME DAY: Chang-Chen programme first
read (CCB-004 stage 1: the 24 now QUOTED verbatim; the full n = 4
mass-relation ladder transcribed; cross-engine re-derivation of those
relations declared as the calibration gate for the residual-diagram lane);
the n = 6 reflection-strata map persisted (two types OPEN, both 9-variable
quotients, CCB-036 stage 2).

UPDATE 2026-08-01 (later): EXP-010 DECIDED: emptiness probes CONFIRMED in
seconds (two independent codim-4 sections empty, `[-1]:`, probabilistic-exact
support for dim D4 <= 3), census probes REFUTED BY CAP (both codim-3 draws and
the sympy staircase walled; kill criterion fired; no degree data). Lane
reshaped: cheap recorded-section emptiness probes + the Dias-Pan partial-GB
device (CCB-037, deterministic upper bounds) carry the upper-bound direction;
witness sets (CCB-034) promoted for lower bounds. Dias-Pan arXiv:1811.08681
read IN FULL the same morning (cross stratum of n = 6 generically closed;
dossier + ladder row + references landed). EXP-011 (n = 5 spatial Dziobek) is
shaped as the Dias-Pan proof pattern on our exact instruments.

UPDATE 2026-08-01: the fix has held since the current relaunch. Both gfan 0.8beta
n = 6 runs were verified alive at 07:54 local time after about 74 minutes:
gfan08 pow2 --bits 64 (label pow2-08b64r, 10 threads) and gfan08
pow3 --bits 0 (label pow3-08b0, 10 threads), both with --saveas checkpoints.
Heartbeat: `wsl -d Ubuntu-24.04 -- bash -lc 'ps -o etime,args -C gfan08 -C msolve;
cat /root/exp005b/status-*.log'`. EXP-009 is DECIDED: INCONCLUSIVE-CAP ON BOTH
ROUTES (route A and the z-system route B each produced zero msolve output at their
enforced 3600 s caps; input hashes recorded; the published 50/4 counts remain
untested by us). Consequence adopted: counts go to the BKK bounding rung
(CCB-007/022, target 25380), and finiteness goes to the incidence-dimension lane.
EXP-010 (n = 4 Dziobek-variety dimension calibration) is declared; no run has
started.

STRATEGY DOSSIER (Felipe's request, 2026-07-25):
`program/central-configurations/approaches-evaluation-2026-07-25.md`: the measured
ranking of every approach we ran, and four alternative views with first
experiments: the INCIDENCE-DIMENSION lane (CCB-033, the valuation-free second
route to generic n = 6), witness sets (CCB-034), continuum-exclusion at named
exceptional masses (CCB-035), and the symmetric-strata ladder (CCB-036, on top of
arXiv:1811.08681 which already closes a symmetric class of n = 6).
A POINTED result (all comets certified) would give generic-mass finiteness for
n = 6: statement-level, so it goes to Felipe FIRST, then to an
arbitrary-precision hardening rerun, before anything leaves the repo.

## 5. Next actions, ordered (multi-front; see research-lines-2026-07-24.md)

1. Monitor EXP-005 (front A3) without blocking: heartbeat
   `wsl -d Ubuntu-24.04 -- bash -lc 'cat /root/exp005/status-pow3-b0.log'` (and
   pow2-b0). On completion: decide every comet with the EXP-007 instrument, write
   the verdict, and if POINTED go to Felipe FIRST, then the hardening rerun.
2. Run EXP-010 (CCB-033, hypothesis already declared): the n = 4 Dziobek-variety
   dimension calibration (sections keep msolve zero-dimensional; deterministic
   grevlex rung under its own cap). n = 5 only after n = 4 passes; n = 6 only
   after both. Keep the HM06 mixed-volume value 25380 as the separate BKK
   reproduction target; do not silently extend EXP-009's direct-solve budget.
3. Reads (front E): Sun-Xie-You (arXiv:2510.25649, gate for the Hessian instrument
   CCB-014); AK12 full anatomy (CCB-023); Chang-Chen tables (CCB-004).
4. Statement-level claims and any outreach: to Felipe first, always.
5. Exploration moment every round (methodology/10 multi-factorial rule + 11).

Closed this round: CCB-025 (msolve engine wrapped and used), CCB-032 (exact LP),
CCB-031 (the ADD direction measured; ADD is not a rescue mechanism).

## 6. Where everything lives

- Problem tree: `problems/dynamical-systems/central-configurations/` (context/,
  experiments/, history/log.md, wiki/, code/, scripts/).
- Program files: `program/central-configurations/` (this file, plan.md, backlog.md,
  state.md, routes-2026-07-23.md).
- Mirror (management repo): `_CAOS_MANAGE/plans/caos-research/central-configurations/`
  (status.md + findings.md + history.md; per-problem, never touch other problems').
- Heavy data (when it appears): `E:\_Datos\caos-research\central-configurations\` with
  in-repo SHA-256 manifests.

## 6b. Lenses ledger (methodology/10 + the exploration cadence of methodology/11)

Plan-stage declaration (lenses-2026-07-23.md): spine (exclusion) + anatomy (Roberts
continuum) + invariant (Hessian/critical-value) standing; recognition
(incidence-dimension certificates) and at-infinity (cluster recursion) as exploratory
bets; two-sided gated on the Chang-Chen transcription. New paths minted at open:
CCB-013..020. Session 1 exploration moment: produced lenses-2026-07-23.md itself (11
lenses swept; 8 new backlog rows). Cadence rule (methodology/11, Felipe 2026-07-23):
every session = spine work + at least one persisted exploration moment.

## 7. Gotchas

- Isolation (methodology/08): a parallel session runs jacobian-conjecture on the same
  develop branch. NEVER `git add -A` (their in-flight artifacts show as modified);
  add by explicit path only. Rounds close WITHOUT version bumps; the release step is
  serialized and owned elsewhere; the bake runs only inside a release.
- Repo .venv is Python 3.13 + sympy 1.14 (no pypdf; the management repo's .venv has it
  for PDF work).
- Convention traps: no em-dash, no emoji, English only, no co-author trailers.
- Verification tags: [U] items in context/references.md (Smale verbatim text, Roberts
  masses, HM06 internals, Chang-Chen tables, RCD23) may not carry conclusions.
- The n = 3 collinear rung needs the right chart: the AC distance variety contains
  collinear solutions only together with the degenerate-triangle condition (handled as
  the Cayley-Menger 3-point determinant, i.e. one distance = sum of the others, per
  ordering); the machine decides the exact incidence, not memory.
