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

## 2026-07-24 - round 2: the separation LP, and a retraction

**EXP-003 CONFIRMED.** The separation LP (SEP) is built, re-derived in our own words with
both directions of the equivalence committed BEFORE the run, and implemented exactly over
the rationals (sympy's rational simplex; no floats). It decides, without searching over cost
vectors, whether an instance admits ANY nonnegative cost vector making it a counterexample.

- On the 2026 instance the optimum is exactly $2/7$, and the witness is the published cost
  vector divided by its coordinate sum. The prediction was only "at least $2/7$", so the
  equality is new information: that cost vector is an OPTIMAL separator for this graph and
  flow, and the 58-versus-60 gap is the best the instance can produce.
- Round trip: under the witness costs, `ufclib` independently reports the counterexample and
  the same exact gap $2/7$. Two independent code paths, polyhedral and combinatorial, agree.
- On V1-V5 the optimum is exactly 0: no cost vector breaks them, and the ties at 0 show that
  "obeys the conjecture" can hold with no slack at all.
- **Minimality rung 1 is a theorem:** no single-terminal instance is a counterexample, for
  any cost vector (every routing is congestion-good because $d \le x_a + d$; the
  cheapest-path routing is cost-good by flow decomposition). Machine-checked on six
  adversarially shaped instances.
- **RETRACTION.** The round-1 RESUME recorded a derivation that no counterexample exists
  with at most two terminals, via "a conflict graph on at most two nodes has no odd cycle".
  That argument is invalid: a terminal may have many path choices, so the conflict graph is
  not a two-node graph, and the step from an integral stable-set polytope to the absence of a
  separating nonnegative cost vector was asserted, not proved. The claim was flagged as
  suspect in the EXP-003 hypothesis before the run and is withdrawn in the verdict, in the
  RESUME, and here. Replacing it: at $k = 2$ the all-cheapest routing is always cost-good and
  is congestion-good exactly when every arc on both cheapest paths carries
  $x_a \ge \min(d_1, d_2)$, so a two-terminal counterexample must contain a shared arc below
  that threshold. A 184-instance sweep found none, recorded as evidence and explicitly not as
  a proof. The $k = 2$ question is OPEN.

New backlog rows: UFB-033 (an independent exact LP route or dual certificate, since sympy's
simplex is currently a single point of failure), UFB-034 (constraint generation, because
(SEP) enumerates every congestion-good routing and will not scale to the exhaustion),
UFB-035 (the distribution of (SEP) optima as the natural frontier statistic, not just the
sign). Commit 82e9b08. No version bump.

## 2026-07-25 - manuscript published, and a documentation-standard gap closed

**Preprint published on Zenodo** (Felipe authorised autonomous publication):
"An independent exact verification of the 2026 counterexample to Goemans'
unsplittable-flow cost conjecture, with the violation constant it forces",
v0.01, CC-BY 4.0. Version DOI 10.5281/zenodo.21554259, concept DOI
10.5281/zenodo.21554258, record verified live with the PDF attached and the
resource type shown as Preprint. Seven pages, transcribed from the EXP-001,
EXP-002 and EXP-003 verdicts, never from memory: the verification, the constant
16/15, the consistency battery, the K4 class-boundary placement, the
separation-LP optimality of the published cost vector, the single-terminal
theorem, the two-terminal characterisation, and the retraction of our own
refuted two-terminal prediction, which stays in the paper because it is part of
the record.

**A gap Felipe caught, closed.** Reviewing the built PDF he observed that our
manuscripts never state on page 1 what KIND of document they are. The audit
confirmed it across all four existing manuscripts: the type hides in the date
line ("working manuscript, v0.09", "companion document, v0.03") or in a subtitle
("Machine record v0.02 (draft)"), and none prints its licence or DOI. Fixed here
by a standard page-1 header block (document type from a controlled vocabulary
matching the Zenodo publication_type, version, date, licence, programme and
problem identity, both DOIs, an explicit "not peer reviewed", and the source
repository), persisted as a binding convention in the vault
(conventions/manuscript-header-standard.md).

Printing a paper's own DOI required a new publication flow, since the existing
uploader creates the deposit and attaches the PDF in one step: reserve the DOI
first (tools/zenodo/reserve_doi.py), print it, rebuild, then attach
(attach_pdf.py) and publish. The other three problems' manuscripts were NOT
edited: they belong to parallel sessions (methodology/08), and their retrofit is
Felipe's call since each would ship as a Zenodo new version.

**External communication: none.** Felipe's standing decision of 2026-07-25 is
that nothing goes out beyond the Zenodo deposit itself: no post, no email to the
authors of the positive results, no comment on the announcement.

## 2026-07-25 - round 3: the frontier value, a null result, and the web page

**EXP-004 CONFIRMED in its instruments, with F4 REFUTED as a null result.**

- **The frontier value.** Defined and implemented: $\alpha_{\max} = \max_{c \ge 0}
  \min\{\alpha(y) : c^T y \le c^T x\}$, the largest violation any pricing can force,
  computed exactly as the separation LP restricted to routings below a threshold.
  An instance is a counterexample exactly when $\alpha_{\max} > 1$, so EXP-003's
  separation LP is recovered as the special case at the threshold just above 1.
- For the 2026 instance $\alpha_{\max} = 16/15$, witnessed by the same normalised
  cost vector that maximised the cost gap. So the published prices are optimal in
  BOTH senses, and the $26/15$ consumed by the all-free routing cannot be forced by
  any pricing. Predicted at $16/15$ and confirmed.
- **The null result, sharper than expected.** Over 3456 parameter points of the
  spine family that contains the counterexample (verified to reproduce it arc for
  arc), the ONLY counterexample is that instance at exactly its published
  parameters: 1 point in 2448 at three terminals, 0 in 1008 at four. It is isolated
  and extremal in its own family. A larger forced violation will not come from
  tuning these parameters; it needs a different conflict structure (UFB-037).
- **A predicted tooling failure materialised.** sympy's rational simplex cycled
  ("Oscillating system led to invalid solution") on a degenerate family member,
  which is exactly the single-point-of-failure risk EXP-003's verdict had recorded
  as UFB-033. Response: an exact simplex with Bland's rule of our own
  (code/ufclib/simplex.py), which cannot cycle. Added after the hypothesis and
  labelled as such: a cross-check of the two independent LP implementations on the
  six cases where sympy succeeds; they agree exactly. UFB-033 closed.
- **A specification error, again caught and recorded rather than smoothed over.**
  F1's first run failed because the comparison was vertex-name sensitive (family
  spine v1, v2, v3 versus published u, v, w). The family reproduced the instance
  exactly; only the check was wrong. Fixed by passing an EXPLICIT relabelling, not
  by loosening the comparison.

**Web page.** The problem page shipped (frontend/src/pages/UnsplittableFlowCost.tsx):
six sections EN/ES per methodology/06, the citation spine, the manuscript concept
DOI, and the results split into machine-verified items and the corrections kept in
the record. Screenshot-verified in light and dark across all six tabs with zero
console errors. The shared footer was updated: it claimed the site covered "both
open problems" and named only two, and its disclaimer now also states that the
unsplittable-flow cost conjecture is refuted while its quantitative frontier stays
open. Experiment counts on the page come from the baked records, so they appear at
the next release bake; the bake is NOT run here (methodology/08: it belongs to the
serialized release step).

New backlog rows: UFB-036 (choose the split fractions by LP instead of sampling
them), UFB-037 (conflict structures not realisable on a linear spine). Commits
9a8cf40, e869055. No version bump.

