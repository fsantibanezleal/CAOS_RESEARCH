# History log: unsplittable-flow cost conjecture

Append-only, dated. Dead ends and corrections stay in the record (methodology/05).

## 2026-07-24 - problem opened, and the 2026 claim adjudicated

**Opened.** Deep-research pass from primary sources: the literature status ladder with
per-claim verification tags, the four-conjecture implication lattice, the cost /
convex-combination equivalence, and the C1-C9 consistency battery
(`context/2026-07-24-literature-status-dossier.md`). Established, verbatim from
arXiv:2510.21287 (2025-10-24), that the conjecture was open in general, proved for
series-parallel digraphs (MSW25) and multiples-of-each-other demands (Sku02), known for
planar only at $2 d_{\max}$ (TVZ24), and that the $O(d_{\max})$ question "remains wide
open". Portfolio flipped scoped to exploring in the same commit as the first dossier
(commit 1b9053a).

**The live claim.** A refutation announced publicly on 2026-07-22/23, outside peer review,
with no preprint and no expert confirmation found. Felipe supplied the proposer's artifact
bundle (instance JSON, verifier, LaTeX certificate, SVG, full model transcript), archived
and hashed on E:. Adopted an independence rule: the bundle's verifier is never imported or
executed, and the instance is re-entered by hand rather than parsed, so that agreement
counts as evidence rather than as a shared-code artifact
(`context/2026-07-24-claimed-counterexample-dossier.md`).

**Plan.** Attack ladder UF-P0 to UF-P5, written to be well-posed whichever way the
adjudication landed, with the five candidate attack directions ranked from the research
rather than taken as given. Lens pass produced the round's exploration moment: the
conflict-graph / stable-set reading of the whole problem, which explains the counterexample
in one line, predicts that three terminals are necessary, and reformulates the open frontier
constant as a thinning threshold on conflict graphs (research lines RL1-RL6). Commit
00ddfd7.

**EXP-001 CONFIRMED.** The exact checker (`code/ufclib/`) reproduces every hand-fixed answer
on the validation set V1-V5. Arc-indexed so parallel arcs give distinct paths; vertex-guarded
enumeration so cyclic digraphs terminate; the congestion bound verified inclusive on an
instance engineered to sit exactly on it; feasibility rejection verified by negative control;
the DGG theorem wired in as a per-instance oracle. 14 pytest tests. One specification error
recorded rather than patched away: prediction P8's source scan flagged the deliberate float
inside its own negative control, so the scan (not the goalpost) was narrowed, and the verdict
says so explicitly. Commit 1dfead3.

**EXP-002 CONFIRMED.** The 2026 claimed counterexample VERIFIES under our own exact
enumeration. All sixteen predictions H1-H16 held with no post-hoc adjustment.

- Goemans' Conjecture 1.2 is FALSE: $c^T x = 58$; exactly two simple paths per terminal and
  eight routings found by our own search; the four congestion-good routings cost 90, 60, 60,
  60; the sets of congestion-good and cost-good routings are disjoint.
- $\alpha_{\mathrm{inst}} = 16/15$: the conjecture is refuted by exactly one unit of slack
  (16 needed where 15 is allowed). The $O(d_{\max})$ question is untouched.
- The instance is acyclic, so Morell-Skutella Conjecture 1.4 and the convex-combination form
  fall as corollaries (hypothesis machine-checked).
- Everything proved survives, each tested directly on the instance: the DGG theorem (4
  congestion-good routings exist), Conj 1.3 (4 witnesses), Conj 1.5 and TVZ24 (planar, and a
  cost-good routing exists well within $2 d_{\max}$), Skutella's multiples case (demands 15
  and 10 are not multiples), MSW25 (a $K_4$ subdivision on $\{s, u, v, w\}$ places the
  instance outside series-parallel), and the two-layer case (longest path has 4 arcs).
- Independent second route (methodology/03 rung 1): the conflict graph on the three free
  choices is a triangle with independence number 1, so every congestion-good routing pays
  for at least two expensive paths, giving the bound 60 without enumerating costs. Structural
  and enumerative routes agree.
- The invariant: $\rho = (1/3, 2/5, 1/3)$ with $\sum \rho_i = 16/15 > 1$, a triangle
  stable-set violation separated by nonnegative arc costs.
- Open question minted: $\sum \rho_i$ and $\alpha_{\mathrm{inst}}$ both equal $16/15$ here;
  whether that is structural or coincidence is undecided (UFB-032).

Commit 40786a5. Wiki 01-05 plus the instance SVG transcribed from the verdicts in the same
session. No version bump (methodology/08; the release step is serialized and owned
elsewhere).

**Standing gate honoured:** no external communication of any kind about the claim. Any
statement about whether the celebrated counterexample stands is Felipe's call.
