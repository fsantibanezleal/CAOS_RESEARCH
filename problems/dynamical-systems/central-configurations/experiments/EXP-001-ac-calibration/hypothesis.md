# EXP-001: exact Albouy-Chenciner system builder, calibrated on n = 3, assembled for n = 4

Declared: 2026-07-23, BEFORE any run. Route: R1 (calibration ladder). Backlog: CCB-001.

## Question

Does an exact (sympy over QQ) implementation of the symmetric Albouy-Chenciner equations
reproduce the classical n = 3 central-configuration classification, and does it assemble
the Hampton-Moeckel planar n = 4 system with a machine-verifiable structural profile,
including the square as an exact solution for equal masses?

## Motivation

Method dossier (`context/2026-07-23-hampton-moeckel-method-dossier.md`), sections 1 and 4:
every finiteness certificate since 2005 runs over this polynomial system; before any
frontier work our builder must reproduce known answers exactly. n = 3 is fully classical
(Euler 1767, Lagrange 1772, Moulton 1910: 3 collinear classes + 1 equilateral class in
labeled mutual-distance space); the n = 4 equal-mass square is exactly solvable by hand.

## Setup

Variables $r_{ij}$, $1 \le i < j \le n$; masses rational parameters; $S_{ij} = r_{ij}^{-3} - 1$
(the $\Lambda = -1$ scale normalization); the symmetric AC equations
$f_{ij} = \sum_k m_k [S_{ik}(r_{jk}^2 - r_{ik}^2 - r_{ij}^2) + S_{jk}(r_{ik}^2 - r_{jk}^2 - r_{ij}^2)]$,
cleared of denominators to polynomials in QQ[m][r]. Planar 4-body realizability: the
bordered 5x5 Cayley-Menger determinant $e_{CM} = 0$. Sample positive mass vectors for
instantiated checks: (1,1,1), (1,2,3), (2,3,5), (1,1,2); equal masses (1,1,1,1) for n = 4.

## Falsifiable predictions

- **P1 (zero-dimensionality, n = 3).** For each sample mass vector, the ideal
  $\langle f_{12}, f_{13}, f_{23} \rangle \subset \mathbb{Q}[r_{12}, r_{13}, r_{23}]$
  (cleared forms, saturated by $r_{12} r_{13} r_{23}$) is zero-dimensional.
- **P2 (Lagrange, symbolic masses).** $r_{12} = r_{13} = r_{23} = 1$ satisfies all three
  cleared equations IDENTICALLY in symbolic masses $m_1, m_2, m_3$.
- **P3 (Euler-Moulton count).** For each sample mass vector and each of the 3 collinear
  orderings (imposing the degenerate-triangle relation of that ordering, e.g.
  $r_{13} = r_{12} + r_{23}$ for body 2 between 1 and 3), the restricted system has
  EXACTLY ONE solution with all distances real and positive (counted exactly, Sturm /
  real root isolation). For equal masses that solution has $r_{12} = r_{23}$.
- **P4 (the Euler eliminant, descriptive).** On the collinear chart with symbolic
  masses, eliminating to one variable yields a nonzero univariate eliminant; we record
  its degree and coefficient structure and count its positive roots for the sample
  masses. (No pre-committed coefficient values: the machine derives the polynomial; the
  comparison against the literature's "Euler quintic" is made at verdict time citing
  Moeckel's notes. This prediction fails only if elimination is degenerate, i.e. no
  univariate eliminant exists.)
- **P5 (labeled census, equal masses n = 3).** For masses (1,1,1) the full real positive
  solution set of the AC system consists of exactly 4 GEOMETRICALLY REALIZABLE points
  (triangle inequality, degenerate allowed): the equilateral point (1,1,1) and the 3
  collinear points; any additional real positive but non-realizable algebraic solutions
  are counted and recorded honestly (their existence does NOT refute P5; realizable
  count != 4 does).
- **P6 (n = 4 assembly).** The planar 4-body system (6 cleared AC equations + $e_{CM}$,
  equal masses) assembles to 7 nonzero polynomials in 6 variables; for each we record
  monomial count, total degree, and Newton support affine dimension; the profile is
  persisted as the baseline artifact for CC-P1. (Fails only if assembly is inconsistent,
  e.g. an identically-zero AC polynomial.)
- **P7 (the square, exactly).** Under the equal-mass rhombus-type ansatz
  $r_{12} = r_{23} = r_{34} = r_{14} = a$, $r_{13} = r_{24} = b$, the AC system reduces
  to a system in $(a, b)$ whose unique positive real solution satisfies $b^2 = 2 a^2$
  (the geometric square) and $e_{CM}(a, b) = 0$ exactly. Expected (hand derivation, to
  be machine-checked, not assumed): $a^3 = (4 + \sqrt{2})/2$, equivalently $a$ is a root
  of $2 x^6 - 8 x^3 + 7$.

## Success / failure criteria

- SUCCESS: P1, P2, P3, P5, P6, P7 all pass as machine asserts (run.py exits 0). P4 is
  descriptive (fails only on degenerate elimination).
- FAILURE: any assert fails (run.py exits nonzero). A failed prediction is reported as
  refuted in verdict.md; goalposts do not move; a corrected question becomes a new EXP.

## Method / environment

run.py, repo .venv (Python 3.13, sympy 1.14), CPU only, deterministic (no randomness).
Exact arithmetic throughout (QQ; algebraic numbers via minimal polynomials where
needed). Artifacts tee'd to `artifacts/` (log + JSON profile + derived polynomials).
