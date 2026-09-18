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

- Pages 1-6 and 41-46 are read (see the addendum below for the second range);
  everything cited sits on those pages. The algorithm internals (Sections 3-8),
  the full n = 5 diagram data, the n = 6 elimination record and the 24-case
  list are NOT yet transcribed; no conclusion may rest on them until the deep
  read.
- Part (II) (mass relations, announced in the same programme) remains
  search-only ([U]); nothing here upgrades it.

## 6. ADDENDUM same day: Section 9 (n = 4) and the head of Section 10 (n = 5) read

Pages 41-46 read directly. The n = 4 case is now fully transcribable and gives
us the exact shape of what "solving a diagram" means in their machinery:

| Diagram (their Fig. 1) | Geometry | Outcome |
|---|---|---|
| 1 | fully-edged | NO mass relation reachable by their algorithms (25 type-3 order matrices, too many leading orders); finiteness comes from AK12 section 5.6's dominant-polynomial argument: excluding the other four diagrams suffices |
| 2 | fully-edged isolated triangle | mass relation f_{4,2} = 0 in sqrt(m_i), SIX factors (their (9.1)): three give 1/sqrt(m_i) = 1/sqrt(m_j) + 1/sqrt(m_k) over {i,j,k} = {2,3,4} (their (9.2)); three are m_i(sqrt(m_j) - sqrt(m_k))^2 + m_j m_k, never zero for positive masses |
| 3 | "kite diagram" (w-edge + fully-edged triangle) | f_{4,3} with ELEVEN factors: six equal to (9.1); two short ones, one equivalent to (m2 m3)^3 = m4^2 (m2 + m3)^4 (their (9.3)), the other m2^3 - (m2 + m3) m4^2; three long factors mu_15, mu_21, mu_33 deferred to Appendix IV |
| 4 | disconnected z-edge + w-edge | wedge equations with four sign choices; four give (m1^2 - m1 m2 + m2^2)(m3^2 - m3 m4 + m4^2) = 0, impossible for positive masses; four give a sum of two squares equal to zero, equivalent to m1 m3 = m2 m4 AND m1 m4 = m2 m3, i.e. m1 = m2 and m3 = m4 (their (9.4)) |
| 5 | square diagram | m1 m3 = m2 m4 (their (9.5)) |

All five coincide with AK12 sections 5.1-5.4 (their statement). These
relations are exact, machine-checkable statements: re-deriving (9.2), (9.4),
(9.5) independently with our exact stack is a natural cross-engine replication
experiment (the EXP-003/EXP-006 tradition applied to Algorithm III), and the
right calibration BEFORE touching any of the 24 unsolved n = 6 diagrams.

n = 5 head (Section 10, p. 45): Algorithm I produces TWENTY diagrams
(their Figure 2); Algorithm II excludes diagrams 9, 11, 13, 17; the remaining
SIXTEEN are precisely AK12 Figure 11. This sharpens our record, which carried
only the 16. Diagram-level order-matrix data continues past p. 46 (not yet
read).
