# The seven Millennium Prize problems on 2026-11-22: status, claims, what stays open, and the paths this programme takes

Date: 2026-11-22. Written by the coordinating session on Felipe's orders of 2026-11-22: "is any millennium problem still
open? review in maximum detail, decide online for proposal and advances on each one, persist all the relevant"; and
"define a real path, exploring new fields, and try to solve the most promising one. don't stop". Marks: [P] read by
this session on the primary source the same day; [N] read only in news or secondary reports, not yet on a primary
source; [K] standard knowledge of the field, not re-read here; [D] derived here. Sources with SHA-256 under the data
root, `caos-research/millennium-review-2026-11-22/` (`SHA256SUMS.txt`).

Why this file exists, in Felipe's words of 2026-11-22: "I asked to explore the problem, you explored what you
wanted instead"; "for your fault we lost the opportunity to explore relevant solutions when it was pertinent". From
2026-07 to 2026-11 the Riemann programme worked only with zero-proportion machinery and never opened the fields the
proof of 2026-11-20 came from (Stepanov's method, theta correspondence, automorphic periods, Arakelov slopes, Galois
deformation, Iwasawa theory). Methodology 10 and 11 required a multi-field map and were not applied. This review
applies them to every problem, and each problem below carries paths from fields that are not its native ones.

## 0. The answer

Yes. [P, claymath.org, read 2026-11-22] The Clay Mathematics Institute lists five problems as "Unsolved" (Birch and
Swinnerton-Dyer, Hodge, P vs NP, the Riemann hypothesis, Yang-Mills and the mass gap), the Navier-Stokes problem as
"Active", and only the Poincare conjecture as solved. Clay considers a solution only after publication in a refereed
outlet and two years of acceptance [K, rules]. Three of the six have 2026 claims produced with AI systems; none is
accepted by Clay.

**Correction of 2026-11-24 (Felipe: "is the generalization part of the millennium problem?", "navier stokes is
resolved too").** The last column of the table below mixes two things: what is open inside a prize statement and what
is open around it. Read against the prize statements only [K, the official problem descriptions]:

- The Riemann problem is the hypothesis for the Riemann zeta function. The generalized hypothesis (Dirichlet, Dedekind,
  Hecke, Artin, automorphic L-functions) is context in the official description, not part of the prize statement. If
  the certified Lean proof stands, the prize statement is settled.
- The Navier-Stokes problem is settled by any one of four statements; C and D are breakdown with a smooth force. The
  claim of 2026-09-08 is C and D. If it stands, the prize statement is settled. The unforced question is outside it.
  Clay's page still said "Active" and named no claim when read again on 2026-11-24; arXiv:2610.08144 disputes the
  faithfulness of the Lean formalization [N].
- Clay's page of the Riemann problem carried the label "Active" when read on 2026-11-24 (it read "Unsolved" on the 22nd); Lean's own kernels and an end-to-end Comparator run have accepted the proof (watch reading 2 in the Riemann claimed-proof review, Section 10).
- **Open inside their prize statements: four problems.** P vs NP, Hodge, Birch and Swinnerton-Dyer, and the mass gap
  of Yang-Mills (its existence half is claimed and judged established by a committee [N]).

Consequence for Section 8: ranks 1 and 3 (the non-abelian extension of the Riemann mechanism, the Navier-Stokes force
budget) are not paths on an open Millennium problem. The decision of Section 8 is superseded: the target is chosen
among the four problems above, after the cross-field path map of methodology 11 for each. Rank 1 (line F of the
Riemann programme) continues only where its reading feeds the Birch and Swinnerton-Dyer path (rank 4).

| Problem | Clay page, 2026-11-22 | 2026 claims | What stays open in any case |
|---|---|---|---|
| Riemann hypothesis | Unsolved | Alpoge with Claude, 2026-11-20: Lean proof of RH and of GRH for Dirichlet L-functions, certified by the Lean and Mathlib communities (2026-11-21); Masullo (human, 2026-11-20): draft claiming GRH for Hecke L-functions of every number field | the hypothesis for Dedekind zeta functions of non-abelian fields, Artin and automorphic L-functions (unless Masullo's draft holds); simplicity, pair correlation, moments |
| Navier-Stokes | Active | OpenAI, 2026-09-08: forced blow-up from smooth data at rest (statements C and D of the official formulation), with Lean; OpenAI: unforced Euler blow-up; Alpoge and Buckmaster: forced Euler blow-up | blow-up or regularity without forcing (A, B, or a breakdown with f = 0) |
| Yang-Mills and mass gap | Unsolved | OpenAI, 2026-10-26: existence of quantum Yang-Mills theory, judged established by a committee chaired by D. Gross [N]; the committee says the mass gap is not established | the mass gap |
| P vs NP | Unsolved | Lean artifacts of 2026-06 (P = NP) and 2026-07 (P != NP) that declare their key steps as axioms [N]; OpenAI, 2026-10: a claimed refutation of the exponential time hypothesis [N] | all of it |
| Hodge | Unsolved | a self-published Zenodo claim (not credible on its abstract) [N]; the formal statement itself is disputed (a Lean statement found vacuous) [N] | all of it |
| Birch and Swinnerton-Dyer | Unsolved | an unrefereed claim of 2026-10 [N]; established progress on families (Burungale, Skinner, Tian, Wan) [N] | all of it beyond analytic rank 0 and 1 |
| Poincare | Solved (Perelman) | a Lean formalization of Hamilton-Perelman, arXiv:2609.33842 [N] | nothing |

## 1. The Riemann hypothesis

Status. [P] dossier `problems/number-theory/riemann-hypothesis/context/2026-11-21-claimed-proof-review.md`, sections 1
to 10: five Lean theorems (RH, and GRH for every Dirichlet L-function), accepted by independent kernels and certified
by the joint statement of 2026-11-21; no written proof; no statement of Anthropic or Clay.

New on 2026-11-22 [P]:
- A 73-page reading of the mathematics, R. Zhang (IHES), "A preliminary note on Alpoge's proposed proof of the
  generalized Riemann hypothesis", dated 2026-11-21, `ihes.fr/~rzhang/files/GRH note.pdf` (SHA-256 `2cbd7e9b...2ad9`);
  its author says most of the text from Section 2 on was written with an AI system and cannot be claimed faithful to
  the Lean code. The mechanism it describes: the product formula (a nonzero algebraic integer highly divisible at
  finite primes cannot be small at every archimedean place); sums over prime powers enter lower bounds for the
  valuations of automorphic periods on unitary groups over the totally real subfield of an abelian CM field E; m
  successive theta lifts increase the divisibility; Arakelov geometry (Harder-Narasimhan-Stuhler-Grayson filtration,
  Bost's slope inequality, arithmetic Hilbert-Samuel, integral p-adic Hodge theory) bounds the archimedean size; Galois
  cohomology (Tate-Poitou, Taylor-Wiles, Kato's Euler system, Iwasawa theory with Ferrero-Washington) bounds the
  denominators; Behrend's sets without three-term progressions choose the places. The two main errors are x/m and m,
  so m near sqrt(x) gives the exponent 1/2: this is the "chain of length sqrt(X)" of the author's note.
- A community reading blueprint, `github.com/chrisflav/riemann-blueprint` (461 statements, each labelled published,
  modified from the literature, or new in the proof), made by static analysis of the source without a build.
- A second proposed proof, human, of GRH for Hecke L-functions of all unitary Hecke characters of every number field,
  by A. M. Masullo, released 2026-11-20 by R. Vakil (Math 216 site), reviewed for months by B. Conrad; problems found
  with AI assistance are reported [N]. If correct, it covers the extended hypothesis that the formal proof does not.

What stays open, and the paths: `program/riemann-hypothesis/research-lines-2026-11-22.md`. The path chosen for an
attempt is there (Section 3): the extension of the mechanism from abelian to non-abelian Galois CM fields, toward the
hypothesis for Dedekind zeta functions.

## 2. Navier-Stokes

Status [P, openai.com/index/navier-stokes-solution, 2026-09-08, updated 2026-09-10]: "an initially smooth fluid at rest
can develop a singularity in a finite time. The fluid has a smooth force applied to it, and its energy remains finite";
"This resolves the Navier-Stokes Millennium Prize problem by establishing statement 'C' (and also 'D')"; the agents
also resolved the unforced Euler regularity problem (blow-up without force); L. Alpoge and T. Buckmaster, with an
Anthropic model, resolved the forced Euler problem first, and OpenAI recognizes that priority; "We do not intend to
claim the Millennium Prize". Clay marks the problem "Active". arXiv:2610.08144 argues that the Lean formalization is
not a faithful translation of the written proof [N here; read by the programme's Navier-Stokes scoping of 2026-11-02].

What stays open, outside the prize statement (correction of 2026-11-24 in Section 0): the unforced equations
(global regularity or blow-up with f = 0), the physically central question;
uniqueness of Leray solutions without force; the critical role of the force.

Programme position: `program/navier-stokes/` is dormant (manuscript v0.10; its blow-up design class has a measured
ceiling, NS-021).

Paths from other fields:
- Anatomy of the forced construction [lens 2]: measure what the force does. A "force budget" (the smallest norm of a
  force that keeps a given ansatz exact) is an invariant of a blow-up scenario; computing it for the published
  spiralling-vortex construction and for the unforced Euler construction shows how far each is from an unforced
  Navier-Stokes blow-up. First step: read the OpenAI Euler and Navier-Stokes papers and the Alpoge-Buckmaster forced
  Euler paper and tabulate the force and its scaling against the dissipation.
- Computer-assisted proofs [K]: Chen and Hou's proof of Euler blow-up with boundary (2022-2023) and Hou's numerical
  candidates for Navier-Stokes blow-up; interval arithmetic around approximate self-similar profiles.
- Convex integration [K] (Buckmaster-Vicol non-uniqueness; Albritton-Brue-Colombo non-uniqueness with force):
  non-uniqueness is the other face of breakdown.

## 3. Yang-Mills and the mass gap

Status [N]: OpenAI, 2026-10-26, a proof of the existence part; a five-member committee chaired by D. Gross concluded
that the machine-checked proof establishes existence and not the mass gap, and that it does not yet fully understand the
proof; OpenAI is writing its own account. Clay page [P]: "no proof of this property is known".

What stays open: the mass gap.

Paths from other fields [K]: lattice gauge theory (Chatterjee's reduction of the gap to uniform exponential decay of
correlations; Cao-Park-Sheffield on Wilson loops), stochastic quantization (Chandra-Chevyrev-Hairer-Shen for two and
three dimensions), spectral theory of transfer matrices, reflection positivity. First step: read the existence proof's
construction once it is public and record which Osterwalder-Schrader axioms it verifies and whether a lattice
approximation with uniform estimates appears in it; a gap statement on a lattice uniform in the spacing is the
natural bridge.

Programme position: no programme. Value for this programme: low feasibility; recorded, not opened.

## 4. P vs NP

Status: Clay "Unsolved" [P]. The Lean artifacts of 2026 that claim either answer declare their decisive steps as
axioms [N] and carry no weight. OpenAI's claimed refutation of the exponential time hypothesis (2026-10) [N]: a
2^(o(n)) algorithm for 3-SAT would not settle P vs NP.

Paths from other fields:
- Algorithms to lower bounds [K]: R. Williams' method turns a nontrivial satisfiability algorithm for a circuit class C
  into the lower bound NEXP not in C (ACC0, 2011). If the ETH refutation is real, the question is which class its
  algorithm covers (CNF only, or circuits) and what lower bound it yields through this method. First step: read the
  claim on its primary source; derive the Williams-type consequence; record it. This is the cheapest path with real
  value of this review.
- Barriers [K]: relativization, natural proofs, algebrization; any claim is checked against them first.
- Geometric complexity theory, proof complexity, meta-complexity (Kolmogorov complexity characterizations of one-way
  functions) [K]: recorded.

Programme position: no programme.

## 5. Hodge

Status: Clay "Unsolved" [P]. No credible claim [N]. The formal statement is a bottleneck: a Lean statement registered
in a public repository was found trivially provable, and the statement proposed to DeepMind's Formal Conjectures
imports over 250,000 lines [P, Xena post of 2026-11-12]. An AI-produced manuscript on the rational Hodge conjecture for
CM abelian varieties is listed in arXiv:2607.07779 [N].

Paths from other fields:
- Abelian varieties of CM type connect to the Riemann proof's own inputs (CM periods, Chowla-Selberg, Anderson,
  Shimura-Taniyama): the Hodge conjecture for abelian varieties reduces to Hodge classes of Weil type in many cases [K];
  first step: read the 2026 CM manuscript and the recent literature on Weil-type classes.
- Statement fidelity as a deliverable: a Mathlib-only statement for a restricted class (abelian varieties over C) is a
  contribution that does not exist; first step: survey what Mathlib has (complex manifolds, de Rham, algebraic cycles).

Programme position: no programme. Recorded.

## 6. Birch and Swinnerton-Dyer

Status: Clay "Unsolved" [P]; a Clay workshop on recent results was held in Oxford, 2026-09-21 to 25 [N]. Known [K]:
analytic rank 0 and 1 give the rank and finite Sha (Gross-Zagier, Kolyvagin); p-parts of the leading term formula
for many curves (Skinner-Urban, Zhang, and others); infinite families of quadratic twists with the full formula
(Burungale, Skinner, Tian, Wan) [N].

Path from another field: the Riemann proof bounds Tate-Shafarevich groups of Tate twists and Bloch-Kato Selmer groups
of two-dimensional modular representations by Kato's Euler system and Taylor-Wiles deformation (Zhang, Section 5)
[P]. These are BSD-type objects. First step: read Zhang Section 5 and the blueprint nodes for it, and record whether
any bound there is new for Bloch-Kato Selmer groups of Tate twists (a statement of BSD type for motives of weight
other than elliptic curves).

Programme position: no programme. Recorded; the first step is cheap and shares its reading with Section 1.

## 7. Poincare

Solved (Perelman, 2002-2003; prize declined in 2010) [K]; a Lean formalization of Hamilton-Perelman is announced in
arXiv:2609.33842 [N]. Nothing to do.

## 8. Ranking and decision

| Rank | Path | Why | First bounded step |
|---|---|---|---|
| 1 | Extension of the Riemann mechanism to non-abelian Galois CM fields (Dedekind zeta functions) | the method exists, is formally checked in the abelian case, and its abelian inputs can be listed one by one; a human draft (Masullo) claims a different route to the wider statement, so the question is live | `program/riemann-hypothesis/research-lines-2026-11-22.md`, Section 3: the first attempt (done in part on 2026-11-22) |
| 2 | Williams-type consequences of the claimed ETH refutation | cheap, real value if the claim stands | read the claim on its primary source |
| 3 | Force budget of the Navier-Stokes and Euler constructions | the programme has a dormant Navier-Stokes line and a measured design ceiling | read the three papers, tabulate force and scaling |
| 4 | Bloch-Kato bounds inside the Riemann proof | shares its reading with rank 1 | Zhang Section 5 against the blueprint |
| 5 | Yang-Mills gap via uniform lattice estimates; Hodge statement fidelity | low feasibility for this programme now | recorded |

Superseded on 2026-11-24 (see the correction in Section 0). Decision of 2026-11-22: path 1 is attempted now (the order "try to solve the most promising one"); paths 2 to 4 get their first
step in the following rounds; every round keeps a cross-field exploration entry (methodology 11).

## 9. Decision of 2026-11-24: the four path maps and the target

Order (Felipe, 2026-11-24): "continue with the four open ones, dont stop". Each of the four problems open inside its
prize statement now has its path map, written before any target was chosen (methodology 11):

| Problem | Path map | Dossier status | Rows (cross-field) |
|---|---|---|---|
| P versus NP | `program/p-vs-np/research-lines-2026-11-24.md` | 7 of 8 deliverables done | 18 (11) |
| Hodge | `program/hodge/research-lines-2026-11-24.md` | 7 of 8 | 18 (13) |
| Birch and Swinnerton-Dyer | `program/bsd/research-lines-2026-11-24.md` | 4 of 8 | 18 (11) |
| Yang-Mills mass gap | `program/yang-mills-mass-gap/research-lines-2026-11-24.md` | 7 of 8 | 16 (11) |

Each dossier was written by a delegated research agent; the coordinating session re-read the four prize statements
on Clay's official descriptions and re-checked the claims the choice rests on (Section 10 of each file). No step of
any path map was run by the agents.

Selection criteria, written in the coordination record before the dossiers were read. A problem ranks higher when
(1) one named statement is missing between what is established and the prize statement; (2) machinery produced or
formally checked in 2026 is reusable for it; (3) it has a surface where a step can fail visibly on one workstation;
(4) no theorem excludes the class of methods the path uses; (5) a statement strictly on the route can be proved or
refuted in days and checked by a reader other than the writer. The prior of the coordinating session before the
dossiers was that Birch and Swinnerton-Dyer and the Yang-Mills gap ranked above Hodge and P versus NP.

What the dossiers showed:

- Birch and Swinnerton-Dyer. The machinery of the Riemann proof that looked native to it (Tate-Shafarevich bounds,
  an Euler system) is for Tate twists of cyclotomic fields and for newforms of weight at least 3; weight 2 is
  excluded. After the unrefereed claims of October 2026 the prize statement is open exactly on the curves whose
  Selmer corank is at least 2 at every prime, and nothing constructs a class from a second derivative. Criteria 1, 2
  and 5 fail.
- Yang-Mills. The committee-checked construction takes the infinite-volume limit along a subsequence and proves no
  decay. The missing statement is one in name (uniform exponential clustering) and is the infrared problem that the
  official description says needs new ideas. Criterion 5 gives readings only.
- Hodge. A theorem for abelian varieties with complex multiplication is claimed with a formal proof; the prize
  statement is for every smooth projective variety and nothing reduces it to a family. Criterion 1 fails.
- P versus NP. Two formal-proof-backed claims of 2026-11-23 give a superpolynomial lower bound for general arithmetic
  circuits (the algebraic analogue of the problem), and one of the papers names the two lemmas at which its proof
  stops for Boolean circuits. Criteria 2, 3 and 5 are met best here; criterion 1 is met in part; criterion 4 is the
  known risk (relativization, natural proofs, algebrization).

Decision. The prior is overturned: the target is P versus NP, through the transfer of the algebraic lower bound of
2026-11-23 towards Boolean circuits. What is attempted, in this order: (a) the ladder of statements S(c) between the
algebraic theorem and the Boolean one (circuits correct on inputs 0 and 1 whose polynomial has degree at most c in
each variable), with the first results of the coordinating session to be written with proofs and reviewed; (b) the
question the paper leaves open, which of its two cases occurs, in the form "is the metric sqrt(rank) on the matrices
over the field with two elements a price", with its first finite instance; (c) the written test of the proof against
an oracle gate. Limits, stated here so that no later record overstates them: the claims of 2026-11-23 are one day
old, unrefereed and unread by a human mathematician; the Boolean end of the ladder separates P from the counting
classes, which the prize statement implies and which does not imply it; nothing in this decision is a claim of
progress on the prize statement. The other three problems keep their path maps and stay in the state "proposed".

## How could this be wrong?

- Rows marked [N] rest on news reports; each is to be read on its primary source before it is used in an argument.
- Clay's page was read on 2026-11-22; its labels can change.
- The mechanism of the Riemann proof is read through Zhang's note, which its author says is partly AI-written and not
  checked against the Lean code; the blueprint is a static reading without a build.
