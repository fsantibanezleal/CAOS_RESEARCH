# Unsplittable-flow cost conjecture (Goemans) - problem plan

Opened 2026-07-24. Area: optimization-geometry. State: exploring.
Context dossiers: `problems/optimization-geometry/unsplittable-flow-cost/context/`.

## The situation this plan is built for

The research pass (literature dossier, 2026-07-24) established a peer-reviewed record in
which Goemans' Conjecture 1.2 was OPEN in general, PROVED for series-parallel digraphs
(MSW25) and for demands that are multiples of one another (Sku02), and known for planar
graphs only at the doubled violation $2 d_{\max}$ (TVZ24); and in which the question
"does it hold with $O(d_{\max})$" was described by the most recent primary source
(STVZ25, 2025-10-24) as wide open and a breakthrough target.

Into that record, a CLAIMED refutation arrived on 2026-07-22/23, outside peer review: a
7-vertex planar instance with a finite, integer-checkable certificate. Felipe supplied
the proposer's artifact bundle.

This plan therefore does NOT set out to prove or disprove the conjecture, which would be
planning against an unadjudicated claim. It sets out to (1) DECIDE the claim ourselves by
exact machine enumeration, and (2) attack the questions that a refutation leaves open,
which is where any contribution of ours can be genuine. The quantitative frontier and the
minimality question are open under EITHER outcome of the adjudication, so the programme
is well-posed no matter how EXP-002 lands.

## Goal

Own, in exact arithmetic and end to end, the decision procedure for single-source
unsplittable flow rounding with simultaneous congestion and cost constraints; adjudicate
the 2026 claim; and then measure what the record cannot yet state: the exact violation
constant that cost-preserving rounding requires, and the exact size of the smallest
obstruction.

## The attack ladder (each rung names its certificate form)

| Rung | Content | Certificate form | State |
|---|---|---|---|
| UF-P0 Foundation | The exact instance checker: parse an instance $(G,s,T,d,x,c)$ over the integers/rationals; verify $x$ is a feasible fractional flow; enumerate ALL simple $s$-$t_i$ paths by our own search; enumerate all unsplittable routings; decide congestion-goodness ($y_a \le x_a + d_{\max}$) and cost-goodness ($c^T y \le c^T x$) exactly; report per-arc violations, $\alpha_{\mathrm{inst}}$, and the full routing table. Validated on hand-built instances whose answer is known by inspection (single terminal; parallel paths; capacity-free instance; a DGG-tight instance). EXP-001. | Exact integer/rational arithmetic (Fraction/sympy Rational, no floats anywhere); pytest suite; run.py exits nonzero on any assertion failure | active (EXP-001) |
| UF-P1 Adjudication | Decide the 2026 claim with the UF-P0 checker, written independently of the proposer's verifier. Full C1-C9 consistency battery from the literature dossier plus Q1-Q9 of the counterexample dossier: feasibility, path-enumeration completeness, acyclicity, planarity, series-parallel / $K_4$-subdivision status, demand divisibility, survival of Conj 1.3, survival of Conj 1.5 at $2 d_{\max}$, and the exact $\alpha_{\mathrm{inst}}$ the instance forces. Derive and record the corollary cascade (Conj 1.4 and the convex-combination form) with its acyclicity hypothesis checked, not assumed. EXP-002. | An exact routing table (every routing, its load vector, cost, per-arc violation) plus a battery report in which every consistency test is a machine assertion, not a remark | next |
| UF-P2 Minimality | How small can an obstruction be? Exhaustive search over small instances up to isomorphism (canonical form on the arc-labelled digraph; demands and fractional loads bounded), deciding each by the separation LP so the cost vector is eliminated from the search space. Establish, by exhaustion, a lower bound on the size of any counterexample, and decide whether the 2026 instance is minimum in arcs, in vertices, in terminals, and in $d_{\max}$. | A search certificate: the canonical-form enumeration with its exact count, plus per-instance LP optima in exact rationals; the exhaustion must be provably complete, with the reduction that makes it finite stated and verified | planned |
| UF-P3 The quantitative frontier | The real open problem after a refutation. Define $\alpha^\* := \inf\{\alpha:$ every instance admits a cost-good routing with $y_a \le x_a + \alpha d_{\max}\}$. Lower bounds: maximise $\alpha_{\mathrm{inst}}$ over the certificate's parametric family, over conflict-structure generalisations (the triangle of pairwise-incompatible cheap choices generalises to odd cycles and to cliques, where the LP-integrality gap of the stable-set relaxation grows), and over the UF-P2 exhaustive search. Upper bounds: only $\alpha^\* \le 2$ for planar is known (TVZ24) and nothing in general; the honest target here is lower bounds plus a precise statement of what is NOT known. Also the dual budget $\beta$ (best cost factor at violation exactly $d_{\max}$) and the trade-off curve. | Per-family exact $\alpha$ values with a proof of the family's validity for all parameters (induction on the parametric certificate, machine-checked at sampled parameters and symbolically where possible) | planned |
| UF-P4 The surviving conjectures | Conj 1.3 (cost-free, two-sided, acyclic) survives a cost refutation and, by STVZ25 Theorem 1.6, implies a $2 d_{\max}$ cost statement, so it becomes the live route. The UF-P0/UF-P2 engine applies verbatim: hunt for counterexamples to Conj 1.3 over the same canonical enumeration (the cost clause is simply dropped, the two-sided bounds added). A counterexample there would be a strictly bigger result than the cost refutation; exhaustion evidence for it is valuable either way. | Same exhaustive-search certificate, retargeted; any positive find gets the full C-battery treatment before it is believed | planned |
| UF-P5 Consolidate and publish | Wiki 01-05 transcribed from verdicts as each unit closes; theme-aware SVGs (the instance, the conflict triangle, the class boundary); web page gated by methodology/06; manuscript per methodology/09 as soon as validated plus novel material exists, with the honest split between (a) reproduced/adjudicated external claim, (b) our verified results, (c) our conjectures. | Wiki transcribed from verdicts only; manuscript labels [MV]/[D]/[C] | rolling |

## Ranking of the attack directions (asked for, and derived from the research)

The opening brief listed candidate directions without ranking them. Ranked against what
the literature actually shows:

1. **Exhaustive small-instance search with an isomorphism reduction: FIRST.** It was
   proposed as a way to find an obstruction; its value is now different and higher. With
   an obstruction already in hand, exhaustion answers MINIMALITY, which nobody has
   published, and it simultaneously serves UF-P3 (largest forced $\alpha$) and UF-P4
   (Conj 1.3 hunt) with one engine. It is also the direction where exactness and honest
   completeness accounting are decisive, which is our comparative advantage.
2. **The quantitative relaxations ($\alpha$, $\beta$, the trade-off curve): SECOND, and
   the highest-value target mathematically.** STVZ25 names the $O(d_{\max})$ question a
   breakthrough target, and it is untouched by a counterexample to the constant 1. Our
   first-round expectation, recorded before the run, is that the 2026 instance forces only
   $\alpha \ge 16/15$, i.e. the minimum possible integer margin, which leaves an enormous
   gap to the only known upper bound (2, planar only).
3. **Graph classes: THIRD, and mostly already settled, in an interesting way.** MSW25
   proves the conjecture for series-parallel digraphs; series-parallel is exactly
   $K_4$-subdivision-free; and the claimed counterexample is reported to be a $K_4$
   subdivision. If both hold, the class boundary is TIGHT and that is a clean statement
   worth making precisely and verifying by machine, rather than a research direction with
   room left in it. The residual live question is planar: since the counterexample is
   planar, TVZ24's constant 2 for planar cannot be improved to 1, which is a sharp
   corollary nobody has stated in print.
4. **LP/IP duality and the discrepancy view: FOURTH, as a lens rather than a lane.** It is
   TVZ24's own machinery (they route through a structured discrepancy problem) and it is
   where an UPPER bound on $\alpha^\*$ would have to come from. We do not have a credible
   plan to beat their machinery; we do have a use for the dual view, namely the separation
   LP that eliminates the cost vector from every search. That use is immediate and is
   already wired into UF-P2.
5. **The invariant-first probe: RUN IT FIRST IN TIME, though it is not a rung.** Per
   methodology/10 lens 4 and methodology/11, the cheap invariant here is the fractional
   selection mass on a set of pairwise congestion-incompatible cheap choices. The
   mechanism of the claimed counterexample is exactly "that mass exceeds 1 while any
   integral routing takes at most 1". Reading it as an invariant costs nothing and
   predicts where to look next (odd cycles, then cliques of conflicts): see
   `lenses-2026-07-24.md`.

The direction NOT taken, and why: attempting a proof of the conjecture. The claim in hand
is finite and checkable, and the pre-registered expectation is that it verifies. Planning
a proof effort against it would be planning to be wrong.

## Strategy notes

- **Exactness policy** (methodology/04): every verdict-bearing computation runs in exact
  integer or rational arithmetic (`fractions.Fraction` / sympy `Rational`); floats are
  banned from this problem entirely, including in the LP layer, where an exact rational
  simplex or an exact certificate check is required before any LP result carries a
  verdict. There is no numerical-tolerance regime here to hide in: every quantity in this
  problem is a rational number of modest size.
- **Independence discipline**: the proposer's verifier is archived, hashed, and never
  imported or executed. Our checker is written from the conjecture statement. Any
  agreement is then evidence; agreement by shared code would be worthless.
- **Completeness discipline**: the single historical failure mode of candidate
  counterexamples in this area (documented in the proposer's own transcript) is
  INCOMPLETE PATH ENUMERATION. Every routing enumeration in this programme therefore
  derives its path set by its own graph search, asserts the count, and is regression-gated
  against hand-built instances with known path counts.
- **Isolation** (methodology/08): this programme owns only
  `problems/optimization-geometry/unsplittable-flow-cost/`,
  `program/unsplittable-flow-cost/`, its frontend page, and its mirror in
  `_CAOS_MANAGE/plans/caos-research/unsplittable-flow-cost/`. Rounds close with NO version
  bump; the release step is serialized and owned elsewhere. Parallel sessions run
  jacobian-conjecture and central-configurations.
- **Novelty discipline**: adjudicating someone else's claim is a REPLICATION and is
  labeled as one, however decisive it is. The novel surface is minimality (UF-P2), the
  $\alpha$ frontier (UF-P3), the Conj 1.3 hunt (UF-P4), and the precise class-boundary and
  planar-sharpness statements. Novelty passes (literature re-search) precede any such
  claim, because this area is active and a preprint may appear at any time.
- **External communication**: gated on Felipe, always. This programme does not contact
  authors, does not post, and does not publish a statement about anyone's claim without
  his explicit go. Zenodo publication of OUR manuscript follows methodology/09 once there
  is validated plus novel material, and even then the framing of the external claim is
  Felipe's call.
- **GPU relevance**: partial and late. Nothing in UF-P0/UF-P1 needs it. UF-P2's exhaustive
  search over canonical forms is embarrassingly parallel and CPU-bound in exact rational
  arithmetic; GPU enters only if a float pre-filter is used to shortlist candidates, and
  by policy every shortlisted candidate is then re-decided exactly.
- **Feasibility class A**: the entire problem is finite, decidable, and exactly checkable
  per instance, which is the strongest experimental surface in the portfolio.
