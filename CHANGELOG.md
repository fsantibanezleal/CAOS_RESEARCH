# Changelog

All notable changes to this repository. Format: `X.XX.XXX` (display), see `researchlab.__version__`.
Tag every release. Pre-1.0 while the first problem is not `published`.

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
