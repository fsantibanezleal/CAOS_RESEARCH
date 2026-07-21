# Changelog

All notable changes to this repository. Format: `X.XX.XXX` (display), see `researchlab.__version__`.
Tag every release. Pre-1.0 while the first problem is not `published`.

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
