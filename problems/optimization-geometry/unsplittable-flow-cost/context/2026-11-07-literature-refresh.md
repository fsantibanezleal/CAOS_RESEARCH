# Literature refresh before EXP-005 (UFB-061, UFB-062), 2026-11-07

Marks: [V] read in the primary text; [V2] two secondary sources, primary not read; [U] unverified; [D] our
derivation. Primary reads by a delegated reader (CAOS_MANAGE `wip/caos-research/ufb061-literature-2026-11-07.md`);
the three statements that change our records (Bérczi et al. Conjecture 4 and Theorem 17, the Morell-Skutella 2022
numbering, the STVZ25 labels) were re-read in the primary PDFs by the main session the same day. Sources archived in
the data root under `caos-research/unsplittable-flow-cost/sources/ufb061/` (SHA-256 in `references.md`).

## 1. What changes in our records

1. **Conjecture 1.3 is false in general.** Bérczi, Liu, Reis, Tarnawski, arXiv:2608.13983v1 (14 Aug 2026), state
   as their Conjecture 4 (Morell, Skutella): on a directed acyclic graph with one source, for every flow x >= 0
   satisfying the demands there is an unsplittable flow y >= 0 with |x_a - y_a| <= max_j d_j for every arc. Their
   Theorem 17 [V]: "For each k >= 4, the construction in Figure 2 is a counterexample to Conjecture 4 with
   max_j d_j = 8k, and for every unsplittable flow y, max_a |x_a - y_a| >= 9k - 3 = (9/8 - 3/(8k)) max_j d_j."
   Their Conjecture 4 is Morell-Skutella 2022 Conjecture 1 and STVZ25 Conjecture 1.3 (STVZ25 states it in
   polynomial-time form, which falls a fortiori). It is cost-free, so this refutation is independent of Rybin's.
   Our records listed Conjecture 1.3 as a survivor; that holds on Rybin's instance only.
2. **Consequences [D].** Conjecture 1.4 (two-sided plus cost) implies 1.3, so it now falls twice: on Rybin's
   instance and through 1.3. STVZ25 Theorem 1.6 (1.3 implies 1.5) has a false hypothesis and no longer gives a
   route to Conjecture 1.5, which stays open (no source read disproves it). UFB-040 (a hunt for a 1.3
   counterexample) is superseded.
3. **Numbering (UFB-062).** Morell and Skutella 2022 (Math. Program. 192 (2022) 477-496, authors Sarah Morell and
   Martin Skutella) number their two conjectures 1 and 2 [V]: Conjecture 1, "For a given flow x, there exists an
   unsplittable flow y such that x_a - d_max <= y_a <= x_a + d_max for all a in A"; Conjecture 2, the same with
   arbitrary costs and c(y) <= c(x), which they call equivalent to a convex-combination form and a strengthening of
   Goemans' conjecture. There is no Conjecture 1.3 or 1.4 in that paper. The labels 1.3 and 1.4 are STVZ25's
   (arXiv:2510.21287v1, Section 1, tagged "[MS22]") [V]. Our wiki already declares that labels follow STVZ25; our
   prose "Morell-Skutella Conjecture 1.4" is corrected to "STVZ25 Conjecture 1.4 (Morell-Skutella 2022,
   Conjecture 2)".

## 2. The four sources

- **Afrasyab, arXiv:2609.17568v1** [V], "Independence-System Realisations in Single-Source Unsplittable Flow"
  (dated 27 July 2026 on the PDF; the arXiv identifier and the date do not match, unresolved). Theorem 5: every
  finite loopless independence system has a strong realisation in an acyclic single-source instance (fractional
  split 1/4, unit demands). Theorem 7: in the uniform odd-cycle instance the 1-good cheap selections are exactly
  the stable sets of C_n. Theorem 8: for that family the cost-preserving threshold is tau = 1 - bq. Within the
  symmetric family sup tau = (k+2)/(2(k+1)) (3/4 for the triangle); the C5 certificate (Section 8) gives
  tau(C5) = 79/120 < 1. Bearing: tau is our alpha_inst; the odd-cycle family stays below Rybin's 16/15, so EXP-004's
  extremality of the triangle in its family is not contradicted. Theorems 5 and 7 realise any odd cycle in an
  acyclic single-source digraph (not with a linear spine), so the obstacle named in UFB-037 is quantitative, not
  realisability. States neither 16/15 nor 2/7.
- **Bérczi, Liu, Reis, Tarnawski, arXiv:2608.13983v1** [V], "Weighted Equitability and Matroid-Constrained
  Discrepancy": Section 1 above. Their weighted-carpool Conjecture 2 is a special case of Conjecture 4; Theorem 18
  disproves it, which disproves Conjecture 4 as well, and Theorem 17 is the simpler direct counterexample
  (Section 1 and their Figure 1). They cite Rybin's refutation of Goemans' conjecture, note that Conjecture 4 holds
  for divisible demands (Morell-Skutella) and for acyclic planar digraphs (TVZ), and state that the counterexamples
  were first found with AI models and verified by the authors. Open question: the Morell-Skutella statement with
  discrepancy 2 max_j d_j. The planarity of their Figure 2 instance is not checked [U].
- **Cherniavskii, Kupavskii, Moiseev, Shekhovtsov, arXiv:2610.16079v1** [V], "Approximation algorithms via
  discrepancy with hard constraints" (12 Oct 2026). Theorem 7 (Section 3.1.2): for min-cost unsplittable flow on
  directed multigraphs where every admissible path has at most D hops, a polynomial-time unsplittable y with cost
  not above the LP's and load L_e(y) <= L_e(x) + O(rho_max^e sqrt(D)) on every edge. It does not mention Goemans,
  Rybin, Morell-Skutella, 16/15 or 2/7. Reading for our problem [D]: on hop-bounded instances the cost-preserving
  constant is O(sqrt(D)); Rybin's instance (longest path 4 arcs) is consistent with it.
- **AFP entry** [V], "A Formal Counterexample to the Cost-Preserving Single-Source Unsplittable Flow Conjecture"
  (session Dinitz_Garg_Goemans_Counterexample; A. Freitas Ramos, D. Barros Hulak, R. J. G. B. de Queiroz;
  https://isa-afp.org/entries/Dinitz_Garg_Goemans_Counterexample.html; current document dated 26 Oct 2026, an
  earlier release 7 Aug 2026). It formalises Rybin's nine-arc instance (demands 15, 10, 15; fractional cost 58) and
  proves that every routing with load at most x + 15 on every arc costs at least 60, in weak and strict forms. It
  does not formalise 16/15, the separation LP optimum 2/7, or the acyclicity corollaries; those remain ours [MV].
  Every constant matches our counterexample dossier.

## 3. Other sources after 2026-07-22 (not read in the primary text)

- Muffatti, GitHub `terrorproforma/maths`, folder `planar-cost-lower-bound`: claims a planar lower bound
  (9/8 - o(1)) D for cost-preserving rounding, above our alpha* >= 16/15; read at README level only [V2 at most];
  the unit D is not confirmed. Priority read (UFB-063).
- Ge, Xie, Li, Li, "Goemans's Unsplittable-flow Conjecture: The Anatomy of AI-assisted Counterexample Discovery",
  SSRN 7423078: HTTP 403, unread (UFB-064).
- Lean import of the counterexample, https://github.com/Vilin97/lean-pool/pull/469: unread.
- Debgupta, Morell, Skutella, "Unsplittable Transshipments", arXiv:2602.07230 (Feb 2026, before the
  counterexample): abstract only.

No other arXiv paper on the cost conjecture after 2026-07-22 was found by web search (absence not proven).
