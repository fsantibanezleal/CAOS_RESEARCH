# Changelog

All notable changes to this repository. Format: `X.XX.XXX` (display), see `researchlab.__version__`.
Tag every release. Pre-1.0 while the first problem is not `published`.

## [0.14.000], 2026-07-21

### Added
- EXP-024: sound all-parameter certificates for the (4,6) window via cleared left-null
  vectors (the fraction-field RREF instrument was refuted first: it normalizes the
  obstruction away). Pure-slice theorem: the pairing -8 a^2 empties the (4, <= 6) window for
  EVERY a != 0. The 8-parameter certificate capped at 540 s, documented; staged variants
  queued (JCB-028).

## [0.13.000], 2026-07-21

### Added
- EXP-023: first contact with the primitive stratum: the (4, <= 6) completion window is EMPTY
  on the sampled slice (25/25 primitive-top samples admit no Keller partner of degree <= 6;
  one descent step extends the exclusion to <= 8); positive controls certify the scan
  non-vacuous. Residual ladder (4, 4k+2) and composite gcd queued (JCB-028/029).
- Manuscript v0.06: new section on the planar machine (uniform theorem, quasi-triangular
  closure, the descent algorithm, the primitive stratum), clearing the EXP-021/022 debt.
- Wiki 04: uniform theorem + descent + primitive stratum section; repaired a latent
  alpha/beta escape corruption in the machine section.

## [0.12.000], 2026-07-21

### Added
- EXP-022: the quasi-triangular program: shear closure for ANY section f (with the closed
  inverse); the (3,3) cube-case alignment FORCED at the radical level (quasi-triangular
  conjecture holds there); and the descent inverter as running code (all 8 library maps
  explicitly inverted, 0-4 steps, no primitive hits). JC(2) sharpened to the primitive
  stratum (shared base of degree >= 2, non-power tops): JCB-027.

## [0.11.000], 2026-07-21

### Added
- EXP-021: THE UNIFORM THEOREM: every planar Keller map with min degree <= 2 is
  (x + ell^2, ell/beta + H(x + ell^2)) up to affine gauge, invertible by one closed formula
  (shear-PDE sufficiency generic; completeness by exact kernel dimensions; inverse verified).
  The JC(2) frontier moves to min degree >= 3 (JCB-026: the quasi-triangular conjecture).
- methodology/07-session-handoff.md + program/jacobian-conjecture/RESUME.md: the resume
  contract: every session closes by persisting the full problem state for zero-loss restart.

### Changed
- Home feed: a summary of the 20 most recent experiments, newest first, problem-labeled.

## [0.10.000], 2026-07-21

### Added
- EXP-020: the JC(2) machine proves full cases: THEOREMS at (2,3), (2,4) and (2,5) (one-branch
  completions on the discriminant variety, explicit polynomial inverses verified by exact
  composition, symbolically in all parameters); the (2,4) consistency ideal equals the (2,3)
  one (completion-degree independence, as predicted); the (3,4) monolithic elimination
  documented as exceeding the window (staged strategy queued). Next: the uniform (2,n)
  theorem attempt (JCB-025).

## [0.09.000], 2026-07-21

### Added
- EXP-019: the Keller floors: floor identities and h-divisibility certified on the library;
  wider exhaustive JC(2) certificates at (2,4), (2,5), (3,4); and the FULL-A closure of
  (2,3): the consistency ideal is the single equation (4 A0 A2 - A1^2)^2 = 0, exactly the
  leading-form degeneracy predicted by EXP-013: the tropical theory and the elimination agree
  in one equation. The JC(2) machine (eliminate, parametrize, complete linearly, fiber-test)
  is established.

## [0.08.000], 2026-07-21

### Added
- EXP-018: cascade closure: the Poisson equivalence verified (full Poisson conjecture false,
  minimal dimension open) and the symmetric/gradient corollary recorded; sweep for further
  X-implies-JC statements executed (none found; exclusions documented).
- Web: "Collateral impact" tab on the Jacobian page: the eight status rows (was/now/chain)
  baked from the cascade payload, credit-first framing, screenshot-verified.
- manuscript-cascade/: the companion document "The Collateral Impact of the Three-Dimensional
  Jacobian Counterexample: a Source-Verified Cascade" (built PDF committed).

## [0.07.001], 2026-07-21

### Changed
- Home: "The experiment log" is now the cross-problem feed "Latest experiments across the
  program": every entry carries a problem chip linked to its problem page (scales to wave-2
  problems; each problem page keeps its own filtered log). Screenshot-verified.

### Fixed
- Version drift: the shell footer reads the frontend package version, which had lagged the
  repository version; frontend/pyproject/researchlab now move together (0.7.1 / 0.07.001).

## [0.07.000], 2026-07-21

### Added
- EXP-017: the bilinear harness (the Keller condition is linear in Q's coefficients per fixed
  P): exhaustive-in-Q JC(2) certificates at (2, 3) (216-vector P-grid, 32 instances) and
  (3, 3) (45 vectors, 10 instances), all injective; the EXP-013 solver artifact resolved by
  design (triangular witnesses recovered at the A = 0 samples).
- EXP-015: the JC(2) certificate checker and the executable m = 1 bridge extractor
  (jclib.jc2), tested in CI: exact adjudication for any claimed planar Keller map or collision.
- Wiki 05 and program records updated; JCB-021 advances to the rank-conditions stage.

## [0.06.000], 2026-07-21

### Added
- EXP-013: the leading-form cascade: at every sampled weight ray, real planar Keller maps are
  the degenerate boundary of the EXP-010 equivariant classification (the certified bridge to
  the Newton-polygon program); exhaustive JC(2) certificate at degrees (2, 2) in the affine
  gauge; the (2, 3) sympy empty-solve documented as a solver artifact with an explicit witness
  (continuation queued, JCB-021).
- EXP-016: the consequence cascade verified from primary sources and flags lifted (Mathieu
  false for SU(3); Gaussian moments, vanishing and Image conjectures false; full Dixmier false,
  Dixmier(1) open). Wiki 01 cascade section and the manuscript discussion updated accordingly.
- Program: JCB-020..024 (cascade continuation, Puiseux obstructions, JC(2) certificate checker,
  Hessian-nilpotent quartic extraction).

## [0.05.000], 2026-07-21

### Added
- M3, the web app: shell-based SPA (@fasl-work/caos-app-shell ^0.3.0; header/footer, EN/ES,
  light/dark, KaTeX, ADR-0058 architecture modal with four theme-aware SVGs). Pages: Program
  (portfolio board + experiment log), Methodology (the six binding documents + the loop), and
  the Jacobian problem page with five tabs (summary, context and history, strategy, experiments
  and results, open questions), inline Cite/Refs against 12 primary sources, the family table,
  and two interactive replays of exact results: the fiber-cubic explorer and the escape-wall
  census map (redraw-on-input only, no animation loops).
- Real export pipeline (researchlab): the SIR template example is fully replaced by the
  export_registry stage baking portfolio/experiments/jacobian JSON artifacts with SHA-256
  manifests (CONTRACT 2 kept; artifact guard green); tests rewritten (bake contract, tmp-only
  writes); template residue guard green (205 files clean).
- Screenshot verification: all 3 routes x 2 themes x 5 problem tabs captured headless with zero
  console/page errors; census wall rendered as a crisp sign-change edge; cubic explorer window
  covers all three roots of the default collision target.
- GitHub Pages deploy via Actions (bake + build + deploy-pages) at research.fasl-work.com.

## [0.04.000], 2026-07-21

### Added
- EXP-012: the weighted mechanism landscape (weights (1, -1, -m)): determinant lemma and
  pairing reductions certified generically; m = 1 identified as the JC(2) bridge class (93
  instances, all injective); m = 3 classes empty (valuation proof) or rigid (60 instances);
  the m = 4 potential-form family proved EMPTY (Groebner certificate, seed degree <= 5). The
  parity-law design hypothesis was refuted by its own experiment; the finding is the
  UNIQUENESS of the m = 2 mechanism within the scanned landscape.
- Wiki 03/05 landscape sections; manuscript v0.04 (landscape subsection); PDF rebuilt.

### Changed
- EXP-012 runs as parts (A..E) after a monolithic timeout; instrumentation lessons (t-free
  sections, auxiliary-symbol filters) recorded in the verdict.

## [0.03.000], 2026-07-21

### Added
- EXP-010: 2D equivariant rigidity proved for ARBITRARY weights: every Gm-equivariant Keller
  map of C^2 is LINEAR (classification via the bracket determinant identity, 648 symbolic
  checks; mixed shapes never Keller; the Keller ODE kills nonconstant (f, g) through the
  strictly positive factor 1 + w1 dg + w2 df). The wiki-04 conjecture is now a theorem.
- EXP-011: real fiber census of F: 1 or 3 real preimages split by the discriminant wall
  (D > 0: 3, D < 0: 1); two independent exact routes agree; real surjectivity certified on a
  36-target grid; recorded corollary: the constant-Jacobian real statement in dimension 3
  falls with the same example.
- Wiki 04/05 updated (conjecture upgraded to theorem; census section); manuscript v0.03 with
  the rigidity and real-census theorems; PDF rebuilt.

## [0.02.000], 2026-07-20

### Added
- EXP-006: branch-symbolic 2D equivariant Keller enumeration (valuation-aware ansatz): 216
  polynomial Keller instances, all LINEAR and injective; the rigidity conjecture survives a
  real bounded-degree attack.
- EXP-007: the asymptotic variety, exact: escape roots are multiple fiber roots (s = -W'/m);
  A(F) = {C = 0} union the discriminant surface 27A^2C^2 - 18ABC + 16A + B^3C - B^2 = 0;
  end-to-end escape demonstration and C = 0 flat-sheet fibers.
- EXP-008: degree laws (5d-3, 5d-4, 4) for d = 2..5; fiber-degree floor 3; NEW fiber-degree-6
  counterexample (seed w - 3w^5, k = 5, det = -20) with rational collision; the announced F is
  degree-minimal within the family.
- EXP-009: characteristic-p certificates: the d = 3 instance reduces mod 13 and 101 to explicit
  non-injective Keller maps of degree 12 below the characteristic.
- Wiki pages 02/03/04/05 updated from the verdicts; manuscript v0.02 (new theorems: asymptotic
  variety, degree laws/minimality, char-p remark, EXP-006 coverage) with rebuilt PDF.

## [0.01.000], 2026-07-20

### Added
- Instantiated from the CAOS product-repo template (ADR-0057); package renamed to `researchlab`;
  MIT license.
- `methodology/`: the research operating system (lifecycle, EXP-NNN experiment standard,
  adversarial validation ladder, code standards, writing standards, web publication gates).
- `program/`: portfolio status board (`portfolio.yaml`) + per-problem plan/state/backlog for
  `jacobian-conjecture`.
- `problems/algebraic-geometry/jacobian-conjecture/`: context dossiers (transcribed from the
  persisted 2026-07-20 research), investigation history, and EXP-001 (exact validation of the
  Alpöge/Fable N=3 counterexample: det J = -2 identically; the fiber over (-1/4, 0, 0) is exactly
  the three announced points, via lex Groebner basis).
- `manuscript/`: LaTeX manuscript skeleton mapping findings and approaches.
