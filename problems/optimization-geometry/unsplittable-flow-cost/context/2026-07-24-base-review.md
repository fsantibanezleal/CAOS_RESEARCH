# Statement: the Goemans / Dinitz-Garg-Goemans unsplittable-flow COST conjecture

Dated 2026-07-24. Statement-only dossier (deliberately scoped: no resolution
status, no literature verdicts beyond the two anchors below, so that the
exploration is unbiased). Labels: [VERIFIED] = read directly in a primary source;
[TO FETCH] = named source not yet read.

## 1. The setting

Single-source unsplittable flow. Let G be a digraph with:
- a single source s;
- terminals t_1, ..., t_k with demands d_1, ..., d_k;
- arc capacities u_a >= 0;
- arc costs c_a >= 0.

A FRACTIONAL flow x routes every demand d_i from s to t_i, respecting capacities
(x_a <= u_a on every arc); flow may split across several paths.

An UNSPLITTABLE routing y sends each terminal's ENTIRE demand d_i along a single
s-t_i path. Write D := max_i d_i for the maximum demand.

## 2. The background theorem [VERIFIED]

Dinitz, Garg and Goemans: whenever a fractional flow exists respecting the
capacities, there is an unsplittable one violating the capacities by at most the
maximum demand.

(Stated verbatim in arXiv:2308.02651, which we read directly. Original source:
Dinitz-Garg-Goemans, "On the single-source unsplittable flow problem", FOCS 1998 /
Combinatorica 19(1), 1999. [TO FETCH])

Definition. Given the fractional flow x, call an unsplittable routing y
CONGESTION-GOOD if
        y_a <= x_a + D    on every arc a.
The theorem says a congestion-good routing always exists.

## 3. THE CONJECTURE (the target of this problem)

Call an unsplittable routing y COST-GOOD (with respect to x) if
        c^T y <= c^T x    for every nonnegative cost vector c.

    CONJECTURE (Goemans; the cost version of Dinitz-Garg-Goemans).
    Given a single-source fractional flow x meeting all demands within
    capacity, does there ALWAYS exist an unsplittable routing y that is
    simultaneously CONGESTION-GOOD (y_a <= x_a + D on every arc) and
    COST-GOOD (c^T y <= c^T x)?

That is: can one always match the fractional cost while paying at most the
Dinitz-Garg-Goemans congestion price?

## 4. Immediate remarks (elementary, for orientation)

- Each of the two conditions is achievable ALONE. Congestion-goodness alone is
  the theorem of section 2. Cost-goodness alone is easy: route every demand on a
  cheapest s-t_i path (this ignores capacities entirely). The conjecture is
  precisely about achieving BOTH AT ONCE. [UNVERIFIED, elementary; confirm]
- The problem is finite and exactly checkable per instance: for a fixed finite
  graph with integer data, there are finitely many unsplittable routings (a
  choice of one s-t_i path per terminal), so any single instance can be decided
  by exhaustive exact enumeration.
- Quantitative relaxations that the conjecture does not address, and that are
  natural targets in their own right: a cost factor (c^T y <= alpha c^T x), a
  congestion budget (y_a <= x_a + beta D), and the trade-off curve between them;
  restriction to graph classes (planar, series-parallel, DAGs).

## 5. Source anchors
- arXiv:2308.02651, Single-Source Unsplittable Flows in Planar Graphs (READ, the
  source of the theorem statement and of the conjecture's phrasing).
- Dinitz-Garg-Goemans, Combinatorica 19(1) 1999 (the original theorem) [TO FETCH].
- arXiv:2412.05182, Integer and Unsplittable Multiflows in Series-Parallel
  Digraphs [TO FETCH].
- arXiv:2510.21287, Unsplittable Cost Flows from Unweighted Error-Bounded
  Variants [TO FETCH].
- arXiv:1504.00627, Inapproximability of Maximum Single-Sink Unsplittable,
  Priority and Confluent Flow Problems [TO FETCH].

## 6. Scope note for the exploring session
This dossier gives the STATEMENT and its immediate context only. The literature
status of the conjecture (who has attacked it, what is settled, what is claimed)
is deliberately NOT summarised here: establish it yourself from primary sources as
the first research step, and record what you find with its own evidence.
