# EXP-002 verdict: the 2026 claimed counterexample is VALID

Run 2026-07-24 with the repo `.venv` (Python 3.13.0), CPU only, exact rational arithmetic,
no randomness, no network, no use of the proposer's verifier.
Artifacts: `artifacts/run-log.txt` (the complete tee'd run, including the full routing
table). Reproduce from the repository root:

```
.venv/Scripts/python.exe problems/optimization-geometry/unsplittable-flow-cost/experiments/EXP-002-adjudicate-2026-claim/run.py
```

## Verdict: CONFIRMED

All sixteen declared predictions H1-H16 hold, with no correction to the hypothesis and no
adjustment after the fact. By our own exact enumeration:

**Goemans' Conjecture 1.2 is FALSE.** The instance
$(G, s, \{t_1, t_2, t_3\}, d = (15, 10, 15), x)$ with the nine arcs of the counterexample
dossier admits a feasible fractional flow of cost $c^T x = 58$, and every one of its eight
unsplittable routings either violates the bound $y_a \le x_a + d_{\max}$ on some arc or
costs at least 60. No routing is both congestion-good and cost-good.

This is a complete mathematical fact about a finite object, established here independently
of the announcement, of the proposer's code, and of any external authority.

## What the machine reported

$d_{\max} = 15$, $c^T x = 58$, exactly two simple $s$-$t_i$ paths per terminal found by our
own depth-first search (call them $E_i$, the expensive direct choice, and $Z_i$, the free
detour), hence exactly 8 routings. The complete table:

| $t_1$ | $t_2$ | $t_3$ | cost | $\alpha$ | status | violated arcs |
|---|---|---|---|---|---|---|
| $E_1$ | $E_2$ | $E_3$ | 90 | 1/3 | congestion-good | - |
| $E_1$ | $E_2$ | $Z_3$ | 60 | 2/3 | congestion-good | - |
| $E_1$ | $Z_2$ | $E_3$ | 60 | 2/5 | congestion-good | - |
| $E_1$ | $Z_2$ | $Z_3$ | 30 | 16/15 | cost-good only | $v \to w$ by 1 |
| $Z_1$ | $E_2$ | $E_3$ | 60 | 2/3 | congestion-good | - |
| $Z_1$ | $E_2$ | $Z_3$ | 30 | 16/15 | cost-good only | $u \to v$ by 1 |
| $Z_1$ | $Z_2$ | $E_3$ | 30 | 16/15 | cost-good only | $s \to u$ by 1 |
| $Z_1$ | $Z_2$ | $Z_3$ | 0 | 26/15 | cost-good only | $s \to u$ by 1, $u \to v$ by 11, $v \to w$ by 1 |

The two sets are disjoint: four congestion-good routings costing 90, 60, 60, 60, and four
cost-good routings costing 30, 30, 30, 0. The minimum congestion-good cost is 60 and the
fractional cost is 58, a strict gap of 2.

## The quantitative content the announcement did not state

$\alpha_{\mathrm{inst}} = 16/15$ exactly: the smallest violation budget, in units of
$d_{\max}$, at which some cost-good routing becomes admissible. In absolute terms, a
cost-preserving rounding of this instance needs to exceed the fractional load by 16 units
on one arc where the conjecture allows 15. **The conjecture is refuted by one unit.**

This matters for how the result should be read, and the public coverage does not make the
distinction. The instance shows the constant 1 is not achievable. It says nothing about
whether the conjecture holds with violation $O(d_{\max})$, which the most recent primary
source (STVZ25, 2025-10-24) calls the real breakthrough target: even $\alpha = 16/15$ would
be consistent with everything this instance shows, and the only known upper bound remains 2
for planar graphs (TVZ24).

## The corollary cascade (each hypothesis machine-checked, not assumed)

The digraph is ACYCLIC (verified, H13), so the refutation propagates:

- **Morell-Skutella Conjecture 1.4 (two-sided bounds plus cost, acyclic) is FALSE.** Any
  routing satisfying Conj 1.4's conclusion satisfies Conj 1.2's; none exists here. [D, with
  the acyclicity hypothesis verified by machine]
- **The convex-combination form is FALSE in general.** If $x$ were a convex combination of
  congestion-good unsplittable load vectors $y_i$, then $\min_i c^T y_i \le c^T x = 58$
  would give a congestion-good routing of cost at most 58, and none exists. [D; this is the
  easy direction of the MSS07 equivalence and does not depend on the unread direction]
- Since the conjecture is refuted in its EXISTENCE form, the algorithmic form (which asks
  additionally for polynomial time) falls a fortiori.

## What SURVIVES, verified on this very instance

| Result | Test | Outcome |
|---|---|---|
| Dinitz-Garg-Goemans theorem (1999) | H6: a congestion-good routing must exist | 4 of them exist. The theorem is untouched; only its cost strengthening fails |
| Morell-Skutella Conjecture 1.3 (two-sided, no costs) | H10 | 4 witnesses satisfy $x_a - d_{\max} \le y_a \le x_a + d_{\max}$, e.g. $E_1 E_2 E_3$. NOT refuted |
| Conjecture 1.5 / TVZ24 planar at $2 d_{\max}$ | H11 | witnesses exist; the cheapest-violation cost-good routing has $\alpha = 16/15 \le 2$. NOT refuted, and since the instance is planar this was a genuine test of TVZ24 |
| STVZ25 Theorem 1.6 (Conj 1.3 implies Conj 1.5) | unaffected | its hypothesis, Conj 1.3, still stands |
| Skutella 2002 (demands multiples of one another) | H7 | demands $\{10, 15\}$ are not multiples of one another. No contradiction |
| MSW25 (series-parallel digraphs) | H8 | the underlying graph contains a $K_4$ subdivision with branch vertices $\{s, u, v, w\}$, so the instance lies outside the series-parallel class. No contradiction |
| Lenstra-style two-layer case | H12 | the longest $s$-$t$ path uses 4 arcs, so this is not a two-layer network. No contradiction |

The counterexample therefore contradicts nothing that is proved. That is the strongest
available evidence, short of expert review, that it is not an artifact of a
misunderstanding of the statement.

## Two structural facts worth stating precisely

**1. The class boundary is tight.** MSW25 prove the conjecture (in the stronger
convex-combination form, with strict deviation $< d_{\max}$) for series-parallel digraphs,
whose underlying graphs are exactly the $K_4$-minor-free ones. This counterexample's
underlying graph is a $K_4$ subdivision, that is, the minimal structure outside that class,
verified by machine at $\{s, u, v, w\}$ with the six internally disjoint connecting paths.
So the correct summary is not "the conjecture is false" but "it holds on the series-parallel
side of the $K_4$ boundary and fails at the first structure past it". [MV for the $K_4$
subdivision; [D] for the boundary reading, which combines it with MSW25's theorem]

**2. The planar constant is now pinched, strictly.** The instance is planar (H9: no vertex
has degree 4 or more and only four vertices have degree 3, so neither a $K_5$ nor a
$K_{3,3}$ subdivision can exist, and Kuratowski gives planarity without any embedding
computation). Hence for planar single-source instances the true constant lies strictly
between 1 (refuted here) and 2 (proved by TVZ24). Neither endpoint appears in the
literature we read: TVZ24 could not know the lower endpoint, and the announcement did not
state it. [MV for planarity and $\alpha_{\mathrm{inst}}$; [D] for the pinching statement]

## Adversarial validation (methodology/03)

**Rung 1, exact re-derivation by an independent route: PASSED.** The decision was
re-derived structurally, in fresh code, without costing the eight routings. Build the
conflict graph $H$ on the three free choices, joining $Z_i$ and $Z_j$ when EVERY completion
of the third terminal violates some arc bound. The machine found all three edges, so $H$ is
a triangle with independence number 1; therefore every congestion-good routing uses at
least two expensive paths; the two cheapest expensive paths cost $30 + 30 = 60$; and
$60 > 58$. The structural bound (60) equals the enumerated minimum (60). Two independent
arguments, same number.

**The invariant (RL1, lens 4): PASSED and quantified.** The fractional selection vector is
$\rho = (x_{v \to t_1}/15,\ x_{w \to t_2}/10,\ x_{w \to t_3}/15) = (1/3, 2/5, 1/3)$, whose
sum is exactly $16/15 > 1$, violating the triangle stable-set inequality. The fractional
flow buys $16/15$ units of free routing where any congestion-good integral routing buys at
most 1. The entire counterexample is that one-line LP-integrality gap, dressed as a flow.

**Coincidence flagged, not claimed.** $\sum_i \rho_i = 16/15$ and
$\alpha_{\mathrm{inst}} = 16/15$ are numerically equal. The hypothesis explicitly declined
to predict that this is structural, and this verdict does not claim it is. It is either a
theorem waiting to be found (a relation between the stable-set violation and the forced
violation budget) or an artifact of this instance's calibration. Deciding which is now a
first-class research question: it goes to the backlog as UFB-032, and the honest status is
[C], conjectural, until an argument or a counterexample settles it.

**Rung 4, stress tests: PASSED** as the C1-C9 battery above, every item a machine
assertion.

**Independence: maintained.** The proposer's verifier was never imported or executed; the
instance was re-entered by hand from the dossier table rather than parsed from their JSON;
and the comparison with their reported numbers (H16) was made only after our own decision
was computed. Agreement is therefore evidence, not a shared-code artifact.

## How could this be wrong?

Residual failure modes this experiment does NOT exclude:

1. **Shared misreading of the conjecture.** Our checker implements the statement as
   transcribed in the literature dossier from arXiv:2510.21287 Conjecture 1.2 (inclusive
   inequalities, capacities equal to $x$, one simple path per terminal). If that reading
   were wrong, our verification and the proposer's certificate would be wrong in the same
   way, since both are built on the same published statement. Mitigation applied: the
   statement was cross-read in three independent primary sources (arXiv:2510.21287,
   arXiv:2308.02651, arXiv:2412.05182) which agree verbatim. The Combinatorica original
   remains unread (UFB-002).
2. **Transcription of the instance.** We re-entered the data by hand, which protects
   against a shared parse but not against our own copying error. Mitigation: feasibility
   (H1) and the DGG floor (H6) are strong data-integrity checks, since a mistyped load
   would almost certainly break conservation or the theorem's guarantee. Both passed.
3. **The simple-path restriction** is argued rather than machine-proved (EXP-001 verdict,
   item 2). Since costs are nonnegative and appending cycles only adds load and cost, walks
   cannot rescue the conjecture here, but the code assumes this rather than verifying it.
4. **Scope.** This settles one instance. It does not establish minimality (is there a
   smaller counterexample?), it does not bound $\alpha^\*$ from above, and it says nothing
   about the $O(d_{\max})$ question. Claiming more from this run would be exactly the
   overreach the programme exists to avoid.
5. **Priority and attribution are not mathematical facts** and are outside this
   experiment's scope. This verdict establishes that the object works, not who found it or
   how the community will receive it.

## Consequences for the strategy

- UF-P1 is CLOSED: the adjudication is done, and the answer is that the claim stands.
- The programme's spine moves to the questions a refutation leaves open, exactly as
  `plan.md` anticipated: UF-P2 minimality (is 7 vertices, 9 arcs, 3 terminals, $d_{\max} =
  15$ the smallest possible?), UF-P3 the frontier constant $\alpha^\*$ (now known to be
  $> 1$, and $\ge 16/15$ from this instance), UF-P4 the surviving Conjecture 1.3.
- New backlog rows from this run: UFB-032 (is $\sum \rho_i = \alpha_{\mathrm{inst}}$
  structural?), and the minimality ladder gains a concrete target since the conflict-graph
  argument shows three terminals are necessary (a conflict graph on two nodes has no
  triangle, and more generally no odd cycle, so its stable-set polytope is integral).
- Publication: this is a REPLICATION of someone else's claim plus original quantitative and
  structural content. The manuscript trigger (methodology/09) is met by the combination,
  but the framing of any statement about the external claim is Felipe's call and no
  external action is taken here.
