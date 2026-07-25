# 04 - Our programme

Mirrors `../../../../program/unsplittable-flow-cost/plan.md`; that file is authoritative.

## Why the programme is not "prove or disprove the conjecture"

The conjecture arrived here already carrying a public refutation claim, and a
counterexample is a finite object. So the first act was adjudication, not proof: decide the
claim by our own exact enumeration (EXP-002, CONFIRMED). What is worth building after that
is what a refutation leaves open, and the plan was written so that it is well-posed under
either outcome.

## The ladder

| Rung | Content | State |
|---|---|---|
| UF-P0 Foundation | The exact instance checker `ufclib`: feasibility, our own path enumeration, all routings, exact congestion and cost decisions, per-arc violations, $\alpha_{\mathrm{inst}}$. Validated on hand-built instances with known answers. | DONE (EXP-001) |
| UF-P1 Adjudication | Decide the 2026 claim independently; run the full C1-C9 consistency battery against every proved theorem; derive the corollary cascade with its hypotheses checked. | DONE (EXP-002) |
| UF-P2 Minimality | How small can an obstruction be? Exhaustive search over small instances up to isomorphism, each decided by an exact rational separation LP so the cost vector leaves the search space. | next |
| UF-P3 The frontier | $\alpha^\* = \inf\{\alpha:$ a cost-good routing always exists within $x + \alpha d_{\max}\}$. Known: $\ge 16/15$ (ours), $\le 2$ for planar (TVZ24), no finite bound in general. Lower bounds from odd-cycle and clique conflict families; the trade-off curve against the cost budget. | planned |
| UF-P4 The survivors | Morell-Skutella Conj 1.3 (cost-free, two-sided) survives and, by STVZ25 Theorem 1.6, implies a $2 d_{\max}$ cost statement. The same exhaustive engine retargets to it. | planned |
| UF-P5 Publish | Wiki as verdicts land; manuscript per methodology/09; web page gated by methodology/06. | rolling |

## The instruments

| Instrument | Status |
|---|---|
| `ufclib.instance` exact arc-indexed model (parallel arcs representable, floats refused at the constructor) | built, tested |
| `ufclib.enumerate_routings` vertex-guarded simple-path search (terminates on cyclic digraphs) | built, tested |
| `ufclib.decide` exact congestion and cost decisions, per-routing $\alpha$, two-sided bounds helper | built, tested |
| `ufclib.graphs` acyclicity, $K_4$-subdivision search, Kuratowski-by-degrees planarity (returns None rather than guessing), demand-multiplicity predicate | built, tested |
| Exact rational separation LP (eliminates the cost vector from any search) | UFB-010, not built |
| Canonical form for instance enumeration up to isomorphism | UFB-011, not built |
| Conflict-graph invariant and stable-set pre-filter | partially built inside EXP-002; to be promoted to the library (UFB-023) |

## Standing disciplines

- Exact rational arithmetic only; floats are refused by the constructor, and a token-level
  scan keeps float literals out of the library.
- Paths are never supplied, always searched for, and the count is asserted.
- The Dinitz-Garg-Goemans theorem is wired in as a per-instance oracle: zero congestion-good
  routings means our data or our code is wrong.
- Third-party verifiers are archived and hashed, never imported or executed.
- Statement-level claims about anyone's conjecture status, and every external action, are
  gated on Felipe.
