# Changelog

All notable changes to this repository. Format: `X.XX.XXX` (display), see `researchlab.__version__`.
Tag every release. Pre-1.0 while the first problem is not `published`.

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
