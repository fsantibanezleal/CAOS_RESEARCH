# Unsplittable-flow cost conjecture - state (heartbeat)

- **State:** exploring (opened 2026-07-24).
- **Done (2026-07-24, session 1, research pass):** deep-research dossiers from primary
  sources: the literature status ladder with per-claim verification tags (DGG99 theorem;
  Sku02 multiples-of-each-other; MS22 conjectures 1.3 and 1.4 plus the lower-bound theorem;
  TVZ24 planar at 2 d_max; MSW25 series-parallel, the first non-trivial class where the full
  conjecture holds; STVZ25 Theorem 1.6 and the record that the O(d_max) question was wide
  open as of 2025-10-24), the four-conjecture implication lattice, the cost /
  convex-combination equivalence, and the C1-C9 consistency battery. The 2026 CLAIMED
  refutation recorded with provenance, hashes and an independence rule. Portfolio flipped
  scoped to exploring in the same commit as the first dossier. Plan, lenses pass, research
  lines RL1-RL6, backlog written.
- **Done (2026-07-24, round 1 close): EXP-001 CONFIRMED and EXP-002 CONFIRMED.**
  The exact checker (ufclib) reproduces every hand-fixed answer on V1-V5 and is adopted as
  ground truth (14 pytest tests). The 2026 claimed counterexample VERIFIES under our own
  exact enumeration: Goemans' Conjecture 1.2 is FALSE (c^T x = 58; the four congestion-good
  routings cost 90, 60, 60, 60), Morell-Skutella Conjecture 1.4 and the convex-combination
  form fall with it (acyclicity machine-checked), and everything proved survives its direct
  test on the instance. Beyond the announcement: alpha_inst = 16/15 exactly, so the
  conjecture is refuted by ONE unit; a K4 subdivision on {s, u, v, w} places the instance one
  structure outside the series-parallel class where it is proved; planarity pins the planar
  constant strictly between 1 and 2; and an independent structural route (conflict triangle,
  independence number 1) reproduces the bound 60 without enumerating costs.
- **Done (2026-07-24, round 2 close): EXP-003 CONFIRMED.** The separation LP (SEP), derived
  by us before the run and implemented exactly over the rationals, decides whether an
  instance admits ANY nonnegative cost vector making it a counterexample. On the 2026
  instance the optimum is exactly 2/7, attained by the published cost vector normalised, so
  those prices are an OPTIMAL separator for that graph and flow (the prediction was only
  ">= 2/7"). Round trip through ufclib agrees on the exact gap. Minimality rung 1 is a
  THEOREM (no single-terminal counterexample, for any cost vector). The round-1 claim about
  k <= 2 terminals was RETRACTED as invalid and replaced by a sharp necessary condition at
  k = 2 plus a 184-instance sweep that found nothing, recorded as evidence and not proof;
  k = 2 remains open.
- **Done (2026-07-25, round 3 close): EXP-004 CONFIRMED in its instruments, F4 REFUTED as a
  null result.** The FRONTIER VALUE (the largest violation any pricing can force, computed
  exactly as the separation LP restricted below a threshold) equals 16/15 for the 2026
  instance, so its published cost vector is optimal both for the cost gap and for the
  violation forced. Over 3456 parameter points of the spine family that contains it, the ONLY
  counterexample is that instance at exactly its published parameters (1 in 2448 at k = 3, 0
  in 1008 at k = 4): it is isolated and extremal in its own family. sympy's simplex cycled on
  a degenerate member (the UFB-033 risk materialising), so we wrote an exact Bland-rule
  simplex; the two implementations cross-validate on all six decidable cases.
- **Also 2026-07-25:** the preprint published on Zenodo (v0.01, DOI 10.5281/zenodo.21554259,
  concept 10.5281/zenodo.21554258), carrying the new page-1 header standard via a
  DOI-prereserve flow; and the web problem page shipped (6 sections EN/ES,
  screenshot-verified in light and dark, zero console errors).
- **Now:** round 4. UFB-037 (conflict structures a linear spine cannot realise) is the
  evidenced next step, since parameter tuning inside the spine family is exhausted.
- **Next experiments:** EXP-005 (a non-spine conflict structure toward a larger forced
  violation), then the canonical form plus constraint generation (UFB-011, UFB-034) opening
  the minimality exhaustion (UFB-012).
- **Open question minted this round:** sum(rho_i) and alpha_inst are both 16/15 on the 2026
  instance; whether that equality is structural is undecided (UFB-032).
- **Isolation note:** rounds close with NO version bump (methodology/08); the release step is
  serialized and owned elsewhere; parallel sessions run jacobian-conjecture and
  central-configurations.
- **Standing gate:** statement-level claims about anyone's conjecture status, and every
  external action (posting, contacting authors, publishing), go to Felipe first. Nothing has
  left this repository.
