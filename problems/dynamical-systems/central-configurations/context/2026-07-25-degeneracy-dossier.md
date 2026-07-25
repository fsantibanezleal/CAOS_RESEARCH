# Dossier: degeneracy of planar central configurations (the invariant lens gate)

Date: 2026-07-25. Source: Sun, Xie and You, "Degeneracy of Planar Central
Configurations in the N-Body Problem", arXiv:2510.25649v2 (11 Feb 2026), pages 1-4
read directly (front matter, abstract, full introduction with its literature map);
PDF fetched this session. Purpose: the read-first gate for CCB-014 (our Hessian /
degeneracy instrument), per methodology/12 P1 (source-complete before compute).

## Why this paper is the right gate

It answers exactly the question our instrument would have had to solve from scratch:
how to separate the TRIVIAL zero eigenvalues of the Jacobian (from translation,
rotation and scaling invariance) from genuine degeneracy, in the FULL configuration
space rather than in a symmetry-reduced subspace. They give four formulations, each
matched to one of the forms in which the central-configuration system appears in the
literature, and they apply them to the canonical examples.

## Load-bearing content (verified from the pages read)

- **Work in the FULL configuration space.** Their central methodological claim, with
  a concrete cautionary example from Liu and Xie: in a one-parameter family of
  symmetric kite configurations analysed inside a symmetry-restricted subspace, the
  Jacobian generically has corank one and only a fold bifurcation appears; in the
  full planar configuration space ADDITIONAL degeneracies emerge, and at a critical
  mass a configuration that looks nondegenerate in the reduced subspace becomes
  degenerate, producing a pitchfork and asymmetric central configurations. Their
  conclusion, quoted in substance: degeneracy is not a property of a symmetry class
  but an intrinsic feature of the full space, so restricting to symmetric subspaces
  can obscure essential degeneracy mechanisms and give an incomplete bifurcation
  picture. This directly constrains our instrument design: any Hessian/degeneracy
  detector we build must live in the full space with the trivial directions removed
  explicitly, not in a reduced ansatz.
- **The classical anchors they revisit**: Lagrange's equilateral triangle with
  arbitrary masses; the SQUARE with four equal masses; the equilateral triangle with
  a central mass, "revealing specific mass values for which degeneracy occurs". These
  are exactly the configurations our EXP-001/EXP-002 pinned exactly (the square with
  side minimal polynomial 32x^6 - 32x^3 + 7), so they are ready-made cross-checks
  for a future instrument.
- **Rhombus nondegeneracy for arbitrary masses**, established by combining their
  formulation with an INTERVAL ALGORITHM: a computer-assisted result, in the same
  methodological family as Moczurad-Zgliczynski's Krawczyk work.
- **Historical pinning we can now cite precisely** (their introduction, primary):
  Palmore 1975 answered a question of Smale (1974) by exhibiting a degenerate planar
  4-body central configuration: three equal masses at the vertices of an equilateral
  triangle with a fourth mass at the centre, degenerate when
  m_4 / m_1 = (2 + 3 sqrt(3)) / (18 - 5 sqrt(3)); Palmore 1976 extended it to
  (N+1)-body regular polygons with a central mass; Meyer and Schmidt (1987, 1988)
  analysed bifurcations for 4 <= N <= 13; Moeckel and Simo (1995) showed N-gons
  bifurcate to spatial central configurations; Simo 1977 gave the complete numerical
  bifurcation study for the 4-body problem; Rusu and Santoprete (2015) gave rigorous
  computer-assisted bifurcation proofs using the Krawczyk operator; Albouy (1996) is
  cited as the enumeration for four EQUAL masses; Xia 1991 estimated counts on open
  mass sets; Figueras, Tucker and Zgliczynski (2024) reproved degeneracy and
  enumeration for the planar circular restricted 4-body problem.

Note that this last set upgrades several items our references file carried as
recalled or secondary, in particular Palmore's degenerate example, whose exact mass
ratio we can now quote from a primary source rather than from a survey.

## Consequences for our program

1. **CCB-014 is re-scoped, not cancelled.** Building a naive Hessian-nullity
   detector was the plan; this paper supplies the correct framework (four
   formulations, explicit removal of the trivial eigenvalues) and already covers the
   canonical examples. Our instrument should therefore (a) implement their
   full-space formulation exactly rather than a reduced one, and (b) be validated
   against their published anchors: the Palmore mass ratio above, the equal-mass
   square, and rhombus nondegeneracy.
2. **A genuine novelty check before any work.** Their scope is degeneracy and
   bifurcation, not finiteness certificates. Our interest in degeneracy came from
   the two-sided lens (a continuum would force degeneracy along it), so the useful
   question for us is narrower and, as far as this paper shows, unaddressed: whether
   an exact degeneracy certificate can EXCLUDE continua at specific exceptional
   masses, complementing the tropical route. That question survives the read.
3. **Cross-check opportunity.** The equal-mass square is degenerate or not
   according to their analysis, and we hold it exactly; evaluating our own
   formulation there is a one-point regression test with a published answer.

Tagging: the items above are [V] against the pages read this session; the detailed
statements inside their Sections 3 and 4 (the four formulations in full, the rhombus
theorem's hypotheses) remain [U] until those sections are read, and no conclusion of
ours may depend on them before that.
