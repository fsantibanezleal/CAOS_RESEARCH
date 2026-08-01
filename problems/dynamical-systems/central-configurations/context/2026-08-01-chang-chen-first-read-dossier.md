# First read: Chang-Chen programme preprint (CCB-004 stage 1)

Read 2026-08-01: pages 1-6 of 117 (title, abstract, ToC, introduction, Section 2
through the singular-sequence setup). Deep read of Section 11 + Appendix IV is
the declared next stage.

- Source: arXiv:2303.02853v1 (math.DS, 6 Mar 2023), "Toward finiteness of
  central configurations for the planar six-body problem by symbolic
  computations", Ke-Ming Chang and Kuo-Chang Chen. MSC 70F10, 70F15; 68W30,
  03B35. Part (I) of the programme appeared as J. Symbolic Comput. 123 (2024)
  102277 (bibliographic pin via JL25; the preprint is the full 117-page
  document with all three algorithms, Mathematica sources and mass-relation
  appendix).
- Archive: `E:\_Datos\caos-research\central-configurations\papers\arxiv-2303.02853.pdf`,
  SHA-256 a4cd360feefbcebf3e5c49bf55f92dce4481fb0b1bdee72fa16b7801eadec49a.
  (The `file` utility reports "6 page(s)" from stale linearization metadata;
  the table of contents runs to page 117 and the extraction of pages 1-6
  matches it.)

## 1. RECORD UPGRADE: the 24 is now a QUOTED statement

Verbatim from the abstract: "our first algorithm effectively narrows the proof
for finiteness down to 117 zw-diagrams, the second algorithm eliminates 31 of
them, the last algorithm eliminates 62 other diagrams except for masses in
some co-dimension 2 variety in the mass space, and leaving 24 cases unsolved."
And from p. 4: "Our first algorithm narrows down the case n = 6 to 117
zw-diagrams, the second algorithm eliminates 31 of them, and the third
algorithm finds mass relations for 62 diagrams, one of which is impossible for
positive masses. This leaves finiteness of 24 cases unsolved."

Until today our records carried 24 as OUR arithmetic (117 - 31 - 62) with an
explicit not-a-quoted-statement caveat. That caveat is now RETIRED: the number
is printed twice in the primary source. New detail gained: of the 62
mass-relation diagrams, ONE is impossible for positive masses.

## 2. Formulations transcribed (Section 2, all [V: read])

- Normalized central configurations (their (2.1)): center of mass at origin,
  multiplier lambda = 1, rotation fixed by y_12 = 0; then x_k = sum_l m_l
  r_lk^-3 x_lk, same for y_k.
- Complexified polynomial system (2.2): complex x_k, y_k, m_k, plus delta_kl
  for r_kl^-1; equations x_k = sum m_l delta_lk^3 x_lk, y_k likewise,
  1 = delta_kl^2 (x_kl^2 + y_kl^2), y_12 = 0. Definition 2.1: normalized /
  real normalized / positive normalized (positive delta_kl) central
  configurations.
- Weak mass hypothesis imposed throughout: sum_{k in I} m_k != 0 for every
  nonempty subset I (needed once masses are complexified).
- Lemma 2.1: the potential U takes finitely many values on the set of
  normalized central configurations (their finiteness anchor for U-levels).
- Singular sequences: z_k = x_k + i y_k, w_k = x_k - i y_k (conjugate
  coordinates), z_kl w_kl = r_kl^2; Z_kl = z_kl^{-1/2} w_kl^{-3/2},
  W_kl = z_kl^{-3/2} w_kl^{-1/2}; system (2.3) is z_k = sum m_l Z_lk,
  w_k = sum m_l W_lk, 1 = delta_kl^2 z_kl w_kl, z_12 = w_12. Singular
  sequences are extracted by max-norm normalization of the vectors Z, W with
  two regimes (both bounded / at least one unbounded); zw-diagrams encode the
  blow-up combinatorics (their Section 2.2 onward; coloring rules start p. 5).

## 3. Structure map for the deep read (declared plan)

| Target | Pages | What it holds |
|---|---|---|
| Sections 3-5 | 10-33 | matrix rules, order matrices, equation collection: the machinery our exact instruments would re-verify |
| Section 6-8 | 33-41 | the three algorithms (diagram generation; order determination; eliminations + mass relations) |
| Section 9-10 | 41-54 | reproductions of n = 4 (5 diagrams) and n = 5 (16 diagrams): OUR CALIBRATION TARGETS |
| Section 11 | 54-76 | the n = 6 application: 117 diagrams, the eliminations, and the residual list |
| Appendix IV | 111-117 | "frequently appeared factors in mass relations": the explicit mass-relation polynomials |

Their n = 4 and n = 5 sections are natural calibration rungs (their diagram
counts 5 and 16 are the published anchors); the 24 unsolved n = 6 diagrams and
the 62 mass relations are the frontier target list (CCB-004 stage 2, then
CCB-017's two-sided attempt at one residual relation).

## 4. Notes for our lanes

- Their variables are CONJUGATE-COORDINATE (z, w), not mutual-distance: a
  per-diagram exclusion certificate from us would work in their coordinates
  (new builders needed in cclib: the (2.2)/(2.3) systems) or via transfer to
  distance coordinates where possible. Sizing that is part of the deep read.
- Their source code is Mathematica (Appendices I-III, open-sourced in the
  document). An independent re-verification by our exact stack (sympy/msolve)
  of Algorithm II or III outputs on the n = 4 or n = 5 sections would be a
  genuine cross-engine replication in the EXP-003/EXP-006 tradition.
- The weak mass hypothesis (no vanishing subset sums) is a COMPLEXIFIED-mass
  artifact; positive-mass exclusions do not need it, but any replication of
  their intermediate steps must impose it to match.

## 5. Honesty

- Only pages 1-6 are read; everything cited above sits on those pages. The
  algorithms, the diagram tables, the 24-case list and the mass relations are
  NOT yet transcribed; no conclusion may rest on them until the deep read.
- Part (II) (mass relations, announced in the same programme) remains
  search-only ([U]); nothing here upgrades it.
