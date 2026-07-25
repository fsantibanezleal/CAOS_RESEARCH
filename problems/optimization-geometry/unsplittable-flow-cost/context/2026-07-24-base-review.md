# Base review: the Dinitz-Garg-Goemans / Goemans unsplittable-flow COST conjecture

Dated 2026-07-24. Source-anchored first pass (methodology/01: research before plan).
Labels: [VERIFIED] = stated in a primary/peer-reviewed source read directly;
[CLAIMED] = asserted in a non-peer-reviewed source, NOT yet independently checked;
[UNVERIFIED] = our reading, needs a source.

## 1. The setting

Single-source unsplittable flow. A digraph with a single source s, terminals t_i
with demands d_i, arc capacities, and nonnegative arc costs c_a. A fractional flow
x meets all demands within capacity. An UNSPLITTABLE routing y sends each
terminal's whole demand along ONE s-t_i path.

D := max_i d_i (the maximum demand).

## 2. The theorem (settled) [VERIFIED]

Dinitz, Garg, Goemans: whenever a fractional flow exists respecting the
capacities, there is an unsplittable one violating the capacities by at most the
maximum demand. Source: restated verbatim in arXiv:2308.02651 (Single-Source
Unsplittable Flows in Planar Graphs), which we read directly. Original:
Dinitz-Garg-Goemans, "On the single-source unsplittable flow problem"
(FOCS 1998 / Combinatorica 1999) - PRIMARY NOT YET FETCHED, queued.

Call a routing CONGESTION-GOOD if y_a <= x_a + D on every arc.

## 3. The conjecture (the target) [VERIFIED as a statement and as open-in-2023]

Goemans' cost version: is there always an unsplittable routing that is
simultaneously congestion-good AND cost-good, i.e. c^T y <= c^T x, for every
nonnegative cost vector c?

arXiv:2308.02651 (2023) describes it as "a very natural cost version of the same
result, where the unsplittable flow is required to be no more expensive than the
fractional one", states it "remains open", and notes there are "arguably no
non-trivial graph classes for which it is known to hold". That paper's own
contribution is a WEAKENED planar version (violations at most twice as large),
plus a resolution of a related Morell-Skutella conjecture. So as of 2023 the cost
conjecture was open with essentially no positive instances.

## 4. Status 2026: a DISPROOF IS CLAIMED [CLAIMED - our EXP-001 must check it]

A counterexample was announced in 2026, found in an AI-assisted (ChatGPT/GPT-5.6
Pro) reasoning session, reported publicly by Dmitry Rybin (X post) and echoed by
secondary write-ups. The claimed instance:
- a small (reported 7-vertex, planar) graph, single source, three terminals;
- demands 15, 10, 15, so D = 15;
- a spine s -> u -> v -> w; each terminal has a unit-cost direct path and a
  zero-cost detour through the spine;
- fractional flow cost 58; every congestion-good unsplittable routing costs
  >= 60. Hence no routing is simultaneously congestion-good and cost-good.

RELIABILITY NOTE: the sources we could read for the instance details are a social
post and AI-generated aggregator pages, NOT a peer-reviewed paper or a preprint we
have verified. Treat the counterexample as CLAIMED. It is, however, FINITE and
INTEGER-CHECKABLE: the entire claim can be settled by exhaustive exact-arithmetic
enumeration of unsplittable routings on the stated instance. That is exactly our
spine's first move.

## 5. Why this problem fits the programme

- It is the Jacobian pattern again: a decades-old conjecture, an AI-assisted
  counterexample in 2026, and a residual landscape that nobody has mapped yet.
  Our playbook applies verbatim: validate exactly, ANATOMIZE the mechanism
  (methodology/10 lens 2), then decide what survives.
- The verification is genuinely decidable: finite graph, integer demands and
  costs, finitely many unsplittable routings. Exhaustive exact enumeration gives
  a machine-checkable verdict, unlike most of our targets.
- The interesting mathematics is what remains OPEN after the disproof, which the
  announcement does not address:
  (a) what is the true cost/congestion trade-off? Is there alpha with
      cost <= alpha * c^T x among congestion-good routings? The claimed instance
      gives 60/58, so alpha >= 30/29 [UNVERIFIED, to compute exactly];
  (b) is a weaker congestion budget (y_a <= x_a + beta*D, beta > 1) enough to
      restore cost-goodness? What is the minimal beta?
  (c) which graph classes DO satisfy the cost conjecture (2308.02651 says
      essentially none are known; series-parallel is a candidate, cf.
      arXiv:2412.05182 on series-parallel digraphs);
  (d) is the claimed instance MINIMAL (vertices, terminals, demand values)? A
      minimality census is a clean, finite, publishable result.

## 6. Sources
- arXiv:2308.02651, Single-Source Unsplittable Flows in Planar Graphs (READ).
- arXiv:2412.05182, Integer and Unsplittable Multiflows in Series-Parallel
  Digraphs (found, NOT yet read).
- arXiv:2510.21287, Unsplittable Cost Flows from Unweighted Error-Bounded
  Variants (found, NOT yet read).
- arXiv:1504.00627, Inapproximability of Maximum Single-Sink Unsplittable,
  Priority and Confluent Flow (found, NOT yet read).
- Dinitz-Garg-Goemans, Combinatorica 19(1) 1999 (PRIMARY, to fetch).
- 2026 counterexample announcement: Dmitry Rybin, X post (CLAIMED, secondary).
