# Literature status of the Goemans SSUF cost conjecture (deep-research dossier)

Dated 2026-07-24. Produced as step 1 of the opening sequence, from primary sources only.
Companion to `2026-07-24-base-review.md` (the statement-only sheet), which deliberately
carried no status; this dossier establishes the status with evidence.

Tags used throughout:

- **[VERIFIED]** read directly in a primary source we hold on disk (arXiv source or PDF,
  hashed in `sources-manifest.md`), quoted or transcribed at statement level.
- **[CLAIMED]** asserted by a named party in a non-peer-reviewed venue; not yet checked
  by us. A claim keeps this tag no matter how plausible it looks.
- **[UNVERIFIED]** we have not read the source itself (typically paywalled); the content
  is reported by a source we did read, and nothing here may depend on it.

## 0. Sources actually read for this dossier

| Source | What we hold | Status |
|---|---|---|
| Traub, Vargas Koch, Zenklusen, "Single-Source Unsplittable Flows in Planar Graphs", arXiv:2308.02651v1 (2023-08-04) | full LaTeX source (`main.tex`, 155797 bytes) + PDF | read, statement level [VERIFIED] |
| Swamy, Traub, Vargas Koch, Zenklusen, "Unsplittable Cost Flows from Unweighted Error-Bounded Variants", arXiv:2510.21287v1 (2025-10-24) | PDF, pp. 1-6 read | read, statement level [VERIFIED] |
| Majthoub Almoghrabi, Skutella, Warode, "Integer and Unsplittable Multiflows in Series-Parallel Digraphs", arXiv:2412.05182v2 (2025-07-21) | PDF, pp. 0-2 read | read, statement level [VERIFIED] |
| Shepherd, Vetta, "The Inapproximability of Maximum Single-Sink Unsplittable, Priority and Confluent Flow Problems", arXiv:1504.00627 | PDF held, abstract read | partially read |
| Dinitz, Garg, Goemans, Combinatorica 19(1) 1999, 17-41 | not held (paywalled, Springer 10.1007/s004930050043) | [UNVERIFIED] in itself; its THEOREM is transcribed verbatim from three independent primary sources that state it |

The DGG theorem statement is therefore [VERIFIED] as a statement (three independent
primary transcriptions agree verbatim), while the DGG PROOF TECHNIQUE remains
[UNVERIFIED] until the Combinatorica paper is obtained. No argument in this programme
may depend on the proof technique until that read happens (backlog UFB-002).

## 1. The formal setting, verbatim from arXiv:2308.02651

An SSUF instance is a tuple $(G=(V,A), s, T, d, x)$: a digraph $G$, a source $s$,
terminals $T$ with demands $d \in \mathbb{Q}_{\geq 0}^T$, and a splittable (fractional)
flow $x \in \mathbb{Q}_{\geq 0}^A$ routing $d_t$ to each $t$. Write

$$\mathrm{flow}_{\mathcal{P}}(a) := \sum_{t \in T:\, a \in P^t} d_t$$

for the load of an unsplittable flow $\mathcal{P} = \{P^t\}_{t \in T}$ (one $s$-$t$ path
per terminal), and $d_{\max} := \max\{d_t : t \in T\}$.

A point that matters for reading every statement below, quoted from arXiv:2308.02651:
"this can be interpreted as a worst-case assumption where the capacity $u(a)$ of an arc
$a$ is equal to $x(a)$". Capacity violation is measured against the FRACTIONAL FLOW $x$,
not against a separate capacity vector. [VERIFIED]

**Theorem (Dinitz, Garg, Goemans 1999).** Given an SSUF instance, one can compute in
polynomial time an unsplittable flow $\mathcal{P}$ with
$\mathrm{flow}_{\mathcal{P}}(a) \leq x(a) + d_{\max}$ for all $a \in A$. [VERIFIED as a
statement; identical in arXiv:2308.02651 Thm 1.1 area, arXiv:2510.21287 Thm 1.1, and
arXiv:2412.05182 eq. (2)]

**Conjecture 1.2 (Goemans), verbatim from arXiv:2510.21287.** Let $(V,A,s,T,d,c)$ be a
weighted SSUF network and let $x \in \mathbb{R}_{\geq 0}^A$ be a fractional flow. Then
there is a polynomial-time algorithm that finds an unsplittable flow $\mathcal{P}$
satisfying

- $f^{\mathcal{P}}(a) \leq x(a) + d_{\max}$ for all $a \in A$, and
- $c^T f^{\mathcal{P}} \leq c^T x$.

[VERIFIED] Both arXiv:2510.21287 and arXiv:2308.02651 note that one may assume the
underlying graph acyclic without loss of generality (cancel flow on cycles, delete
zero-flow arcs; the resulting $x' \leq x$ instance is no easier). [VERIFIED]

**The three neighbouring conjectures** (arXiv:2510.21287, Section 1, [VERIFIED]):

| Label | Statement | Costs | Bounds | Acyclic required |
|---|---|---|---|---|
| Conj 1.2 (Goemans) | $f^{\mathcal{P}} \le x + d_{\max}$, $c^T f^{\mathcal{P}} \le c^T x$ | yes | upper only | no (WLOG) |
| Conj 1.3 (Morell-Skutella, weaker) | $x - d_{\max} \le f^{\mathcal{P}} \le x + d_{\max}$ | no | two-sided | yes |
| Conj 1.4 (Morell-Skutella, stronger) | Conj 1.3 bounds AND $c^T f^{\mathcal{P}} \le c^T x$ | yes | two-sided | yes |
| Conj 1.5 | $x - 2d_{\max} \le f^{\mathcal{P}} \le x + 2d_{\max}$ AND $c^T f^{\mathcal{P}} \le c^T x$ | yes | two-sided, doubled | yes |

**The implication lattice** (all [VERIFIED] from the statements themselves; the trivial
implications are one-line and re-derived in our own words):

- Conj 1.4 $\Rightarrow$ Conj 1.3 (drop the cost clause).
- Conj 1.4 $\Rightarrow$ Conj 1.2 restricted to acyclic instances (drop the lower bounds);
  and since Conj 1.2 is WLOG acyclic, Conj 1.4 $\Rightarrow$ Conj 1.2 outright.
- Conj 1.2 $\Rightarrow$ Conj 1.5's upper half with the constant 1 instead of 2.
- **Theorem 1.6 of arXiv:2510.21287: if Conj 1.3 holds, then so does Conj 1.5.**
  So the cost-free two-sided conjecture implies a cost statement with violation
  $2 d_{\max}$. [VERIFIED]

**The convex-combination reformulation.** arXiv:2412.05182 footnote 1, verbatim:
"Goemans' original conjecture asserts that, for any arc costs, an unsplittable flow can
be found that satisfies (2) and whose cost does not exceed that of $(x_e)$. This is
equivalent to the stated existence of a convex combination" (their reference [10] is
Martens, Salazar, Skutella, "Convex combinations of single source unsplittable flows").
[VERIFIED as a statement of equivalence; the equivalence PROOF is [UNVERIFIED] pending a
read of Martens-Salazar-Skutella, backlog UFB-003. The easy direction, convex
combination $\Rightarrow$ cost statement, is immediate: if $x = \sum_i \lambda_i y_i$
with each $y_i$ congestion-good, then $\min_i c^T y_i \leq c^T x$ for every $c \geq 0$.]

## 2. What is PROVED (the positive ladder), with dates

| Result | Class / hypothesis | Guarantee | Source | Tag |
|---|---|---|---|---|
| DGG theorem | all instances | congestion only, $+d_{\max}$, poly time | Combinatorica 19(1) 1999 | [VERIFIED] statement |
| Skutella 2002 | demands all multiples of one another | full Goemans conjecture (Conj 1.2) | reported in arXiv:2510.21287 Sec 1.1 and arXiv:2412.05182 p.2, both citing Sku02 | [VERIFIED] as reported; primary Sku02 not read |
| Lenstra-Shmoys-Tardos-style techniques | source plus two layers, arcs source-to-layer-1 and layer-1-to-layer-2 | Conj 1.2 | arXiv:2308.02651, citing lenstra1990approximation | [VERIFIED] as reported |
| Morell-Skutella 2022 | all instances | lower bounds alone: $f^{\mathcal{P}}(a) \geq x(a) - d_{\max}$ | arXiv:2308.02651; also obtainable by reversing DGG augmentations | [VERIFIED] as reported |
| Morell-Skutella 2022 | demands all multiples of one another | Conj 1.4 (hence 1.3) | arXiv:2510.21287 Sec 1.1 | [VERIFIED] as reported |
| Traub, Vargas Koch, Zenklusen 2023/24 | PLANAR, single source | Conj 1.5: cost-good with violation $2 d_{\max}$; and Conj 1.3 (cost-free two-sided) for planar | arXiv:2308.02651 abstract + Sec 1; journal version Math. Prog. 10.1007/s10107-026-02365-x | [VERIFIED] |
| Majthoub Almoghrabi, Skutella, Warode 2024/25 | SERIES-PARALLEL digraphs, general multiflows (distinct source-sink pairs) | Conj 1.4 (hence Goemans Conj 1.2), in the convex-combination form, with STRICT deviation "less than $d_{\max}$" | arXiv:2412.05182v2 abstract; IPCO 2025; Math. Prog. 10.1007/s10107-026-02392-8 | [VERIFIED] |
| Swamy, Traub, Vargas Koch, Zenklusen 2025 | all acyclic instances | Theorem 1.6: Conj 1.3 $\Rightarrow$ Conj 1.5 | arXiv:2510.21287 | [VERIFIED] |
| same | weighted ring loading | unsplittable with $c^T$ guarantee and $\frac{13}{5} d_{\max}$ | arXiv:2510.21287 Thm 1.7 | [VERIFIED] |

## 3. What was OPEN as of the last peer-reviewed word (2025-10-24)

Verbatim from arXiv:2510.21287, Section 1: "We note that it remains wide open whether
Goemans' conjecture holds even with a weaker capacity violation of $O(d_{\max})$, and it
seems fair to say that proving such a weaker form of Goemans' conjecture would already
be considered a breakthrough." [VERIFIED]

And from arXiv:2308.02651 (2023): "This intriguing conjecture remains open. More so,
there are arguably no non-trivial graph classes for which it is known to hold."
[VERIFIED] That last sentence was overtaken by MSW25 (series-parallel) and by the
authors' own planar result at the $2 d_{\max}$ level.

So the state of the peer-reviewed record entering 2026:

1. Goemans Conj 1.2: OPEN in general; PROVED for series-parallel digraphs and for
   multiple-demands; the planar case known only at $2 d_{\max}$.
2. Morell-Skutella Conj 1.3 and 1.4: OPEN in general; both proved for series-parallel;
   1.3 proved for planar.
3. No published counterexample to any of the four conjectures, and no published
   lower-bound instance showing the constant 1 is not achievable.

## 4. The 2026 CLAIMED refutation (status: unadjudicated)

On or about 2026-07-22/23, a refutation of the Goemans cost conjecture was announced
publicly and outside peer review, attributed to Dmitry Rybin working with a large
language model (GPT-5.6 Pro), with reports that another model (Grok 4.5) produced a
comparable object independently. Secondary coverage repeats a common core: a 7-vertex
instance, demands 15, 10, 15, fractional cost 58, every congestion-good unsplittable
routing of cost at least 60, and the underlying undirected graph a subdivision of $K_4$.
[CLAIMED] Sources seen: a thread mirror of x.com/DmitryRybin1/status/2079904005652893709,
mathlab.drummerduck.com/p/goemans-unsplittable-flow, vibemathed.com, windowsnews.ai,
digg.com. None is a primary mathematical venue; no arXiv preprint was found; no response
from Traub, Vargas Koch, Zenklusen, Skutella, Warode or Morell was found. As of this
dossier, no independent expert confirmation is on record. [VERIFIED that we searched and
found none; absence of evidence is recorded as such]

Felipe supplied the proposer's artifact bundle directly (instance JSON, a Python
verifier, a LaTeX certificate with proof, an SVG figure, and the full model transcript);
these are archived and hashed. The bundle's instance matches the publicly reported
numbers, which cross-validates the reporting. Its content, provenance, and the exact
verification programme it triggers are the subject of the companion dossier
`2026-07-24-claimed-counterexample-dossier.md`.

**Adjudication rule adopted for this programme.** The claim is a hypothesis, not a
status. It is decided in-repo by our own independently written exact enumerator, never
by running the proposer's verifier and never by the reputation of any announcement. A
counterexample is a finite object: once the instance data is fixed, its validity is a
decidable arithmetic fact and requires no trust in whoever produced it. Symmetrically,
the fact that a model produced it is not evidence against it either.

## 5. The consistency battery a valid counterexample must survive

A genuine counterexample to Conj 1.2 must not contradict any [VERIFIED] positive result
above. This yields an exact, machine-checkable test battery, which is the strongest
available adversarial validation short of an independent expert (methodology/03, rung 4:
stress families engineered to break the finding):

| # | Test | Why the claim must pass it |
|---|---|---|
| C1 | demands are NOT all multiples of one another | else it contradicts Skutella 2002 |
| C2 | the digraph is NOT series-parallel (equivalently, contains a $K_4$ subdivision) | else it contradicts MSW25 |
| C3 | the digraph is not a source-plus-two-layers network | else it contradicts the Lenstra-style case |
| C4 | if the digraph is planar, some unsplittable routing must be cost-good with violation at most $2 d_{\max}$ | else it contradicts TVZ24 (Conj 1.5 for planar) |
| C5 | some unsplittable routing must satisfy the cost-free two-sided bounds $x - d_{\max} \le f \le x + d_{\max}$ | else it would also refute Conj 1.3, a much bigger claim requiring separate scrutiny |
| C6 | some unsplittable routing must be congestion-good | else it would contradict the DGG THEOREM itself, i.e. the instance data would be wrong |
| C7 | $x$ is a genuine feasible fractional flow (conservation at every node, nonnegative) | the conjecture assumes it |
| C8 | the path enumeration is complete: every $s$-$t_i$ path in the digraph is considered, not only the intended ones | the proposer's own transcript records this exact failure mode in earlier attempts |
| C9 | costs are nonnegative | the conjecture assumes $c \in \mathbb{Q}_{\geq 0}^A$ |

C6 and C8 are the two tests that kill almost all naive candidate counterexamples, and
C8 is documented as having killed several of the proposer's own earlier attempts (its
transcript states that "checking only intended paths, or even hundreds of discovered
paths, is insufficient").

## 6. What a valid refutation would and would not settle

If the claim verifies, the following are immediate and are themselves worth stating
precisely, because the public reporting does not distinguish them:

- Conj 1.2 (Goemans) FALSE.
- Conj 1.4 (Morell-Skutella with costs) FALSE, provided the instance is acyclic, since
  Conj 1.4 $\Rightarrow$ Conj 1.2 on acyclic instances.
- The convex-combination form (arXiv:2412.05182 footnote 1) FALSE in general, by the
  easy direction of the equivalence.
- Conj 1.3 (cost-free, two-sided) UNTOUCHED, if C5 passes.
- Conj 1.5 UNTOUCHED, if C4 passes; and Theorem 1.6 of arXiv:2510.21287 is unaffected,
  which means the cost-free conjecture Conj 1.3 remains the live route to a $2 d_{\max}$
  cost statement.
- The DGG theorem itself UNTOUCHED (it has no cost clause).
- MSW25 and TVZ24 UNTOUCHED, and they become sharper: they mark the exact classes where
  the cost strengthening survives.

And critically, what a single counterexample does NOT settle, which is where this
programme's own contribution lies: **the quantitative frontier**. Define

$$\alpha^\* := \inf\{\alpha : \text{every SSUF instance admits an unsplittable } \mathcal{P} \text{ with } f^{\mathcal{P}} \leq x + \alpha d_{\max} \text{ and } c^T f^{\mathcal{P}} \leq c^T x\}.$$

The conjecture asserts $\alpha^\* \le 1$. A counterexample only pushes $\alpha^\*$ above 1
by whatever margin that single instance forces. The open question that the community
called a breakthrough target, whether $\alpha^\* = O(1)$, remains exactly as open the day
after the refutation as the day before, and the best known upper bound is 2 for planar
(TVZ24), with no finite bound known in general. Measuring the margin an instance forces,
and maximising it over families and over exhaustive small-instance search, is a
well-posed programme that a refutation does not close.

## 7. Adjacent hardness context

Shepherd and Vetta (arXiv:1504.00627) prove that maximum-cardinality single-sink
unsplittable flow is hard to approximate within $n^{1/2 - \epsilon}$ absent the
no-bottleneck assumption, even for demands in $[1, 1+\Delta]$, and that single-sink
confluent flow admits no constant-factor approximation even with the no-bottleneck
assumption. [VERIFIED at abstract level] This concerns the maximization/routability
regime rather than the rounding-with-violation regime of the conjecture, so it neither
supports nor obstructs it; it is recorded here so that the programme does not later
mistake it for evidence either way.

## 8. Open questions this dossier leaves for the programme

1. Is the claimed counterexample valid under our own exact enumeration and the full C1-C9
   battery? (EXP-002)
2. What exact $\alpha$ does it force, i.e. what is the minimum over cost-good routings of
   the maximum violation, in units of $d_{\max}$? (EXP-002)
3. Can the parametric family the certificate sketches push that $\alpha$ higher, and what
   is its supremum? (EXP-003 target)
4. Over ALL small instances up to isomorphism, what is the largest forced $\alpha$?
   (EXP-004 target; needs the cost vector eliminated by LP separation, see the companion
   dossier section 5)
5. Does the DGG augmentation argument have a cost-augmentable form, and exactly where
   does it break? Requires the Combinatorica read. (UFB-002)
