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

## 4. In flight

Nothing mid-run. Rounds 1-2 closed with EXP-001 and EXP-002 decided.

## 5. Next actions, ordered

1. CCB-029: install gfan 0.7 (WSL; record binary + hash); reproduce the Jensen-Leykin
   n = 5 prevariety one-liner; validate both published f-vectors; this opens the
   tropical lane (the LIVE generic-mass frontier: JL25 direct-read dossier).
2. EXP-003 (hypothesis FIRST): msolve-engine census completion for P2's capped
   samples + the n = 4 equal-mass PLANAR census against the 4-classes ground truth
   (CC-P1 entry). Requires CCB-025 (msolve wrap; WSL/passagemath; sympy stays the
   verification layer).
3. CCB-030/031 (the frontier experiments JL25 explicitly calls for): valuation search
   at n = 5; equation-variant prevariety shrinking at n = 4/5 (our EXP-002 P1
   phenomenon at prevariety level). Hypothesis-first, after CCB-029 validates.
4. Reads: Sun degeneracy (arXiv:2510.25649; gate for CCB-014); AK12 full anatomy
   (CCB-023); Chang-Chen tables (CCB-004).
5. Exploration moment every round (methodology/10 multi-factorial rule + 11):
   next lenses on deck: invariant (Hessian, CCB-014) and anatomy (Roberts, CCB-013).

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
