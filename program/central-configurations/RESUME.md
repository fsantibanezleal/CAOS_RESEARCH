# RESUME - Central configurations program (updated 2026-07-23, session 1 in progress)

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
- **Our state:** program OPENED 2026-07-23. Dossiers persisted; plan/backlog/routes
  written; EXP-001 (calibration) is the current experiment. No results of our own yet.
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

- EXP-001 (in flight): calibration; exact AC builder; n = 3 classification; n = 4
  system assembly. Hypothesis committed before run.

## 4. In flight

EXP-001. Hypothesis declared (see the experiment folder); run pending at last update.

## 5. Next actions, ordered

1. Finish EXP-001: run.py with the repo .venv, artifacts tee'd, verdict.md honoring the
   machine; wiki 01-05 initial pages; close the round (no version bump).
2. CCB-002: obtain + read HM06; upgrade [HM-via-*] tags; then design EXP-002 (n = 4
   equal-mass exact census against the 4-classes / 50-rotation-classes ground truth).
3. CCB-007: the exact mixed-volume instrument (staged; needed for the BKK rung).
4. CCB-003/004: AK12 + Chang-Chen reads; transcribe the 24 frontier cases.

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
