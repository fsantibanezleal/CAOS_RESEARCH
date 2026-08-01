# EXP-011 - Verdict: SMOKE AND CAP-SIGNATURE CONFIRMED, EMPTINESS AND PARTIAL-GB RUNGS FAILED TO SCALE AT DECLARED BUDGETS (2026-08-01; no refutation of dim = 4; the 6-to-10-variable wall is measured; the lane's engines change, not its mathematics)

Hypothesis: `hypothesis.md` (declared and committed before any run).
Runner: `run.py` + `pgb_worker.py`. Artifacts: `artifacts/` (seeded draws
verbatim, all msolve inputs, all 15 pgb job files, run log, results.json).

## Outcomes against the declared predictions

| Prediction | Outcome | Facts |
|---|---|---|
| P1 (three-way smoke gate) | PASS in 4 s | unit bipyramid (nine distances 1, r45^2 = 8/3) satisfies all 15 stripped products AND spatial Cayley-Menger by exact polynomial reduction; the all-ones 4-simplex is excluded by CM = -5 exactly; the collinear 0,3,7,12,20 control passes CM and violates all 15 products |
| P2 (codim-5 emptiness probes, dim <= 4 target, 300 s caps) | INCONCLUSIVE-CAP on both draws (the declared kill criterion for this instrument FIRED) | 328 s and 330 s wall, zero msolve output |
| P3 (codim-4 cap-signature control) | CONFIRMED AS EXPECTED | both draws inconclusive-cap (329 s, 313 s); the refuting outcome (a fast EMPTY at codim 4, which would force dim <= 3 against the Moeckel picture) did NOT occur |
| P4 (partial-GB union bound, 15 subideals x 120 s) | DECIDED, INFORMATIVE-WEAK (below the declared success threshold) | 1 of 15 subideals completed (16 leading monomials); d_pgb = 10 with independent set of size 10, i.e. the union bound excludes only the full torus dimension; declared threshold <= 4 not met |

No prediction was refuted algebraically; the expected dimension 4 remains
unrefuted and UNSUPPORTED by this run. What the experiment measured instead is
the instrument wall between 6 variables (EXP-010: emptiness in 1 s) and 10
variables (nothing decided in 300 s): the EXP-010 asymmetry does not persist
at n = 5 for this cut at these budgets.

## The load-bearing reading: it is the ENGINE, not the mathematics

Dias-Pan ran the SAME pattern our P4 attempted (leading-term harvests from
subideals of comparable size, on an 11-variable system) and report completion
"on a notebook with 16GB of memory in a few minutes". They used SINGULAR;
our worker used sympy's Buchberger, which is orders of magnitude slower on
precisely this workload, and our menu put the 130-term degree-8 Cayley-Menger
polynomial in every subideal. Two engine-level fixes follow, neither touching
the mathematics of the lane:

1. Swap the pgb worker's GB engine to msolve (`-g` prints reduced Groebner
   bases; it is already installed and hash-recorded in WSL) or to Singular,
   keeping sympy as the verification layer that re-checks harvested leading
   monomials by exact division. CCB-037 v2.
2. Lighten the menu: subideals of product PAIRS without Cayley-Menger (the
   stripped products are 6-term degree-9 binomial-like polynomials), plus one
   {CM, saturation} subideal whose leading monomial comes almost for free;
   pairs sharing three indices first (they interact most).

Both are new-experiment territory (EXP-012 candidate), not cap extensions of
this one: the budgets here were declared and are honored as spent.

## Consequences (per the declared ladder)

1. The msolve SECTION instruments (emptiness probes AND censuses) are closed
   for n >= 5 at these budgets; their validated domain is n = 4 (EXP-010).
2. CCB-034 (certified witness sets, HomotopyContinuation.jl) is PROMOTED to
   the next instrument spike: it is now the only proposed route to lower
   bounds, degrees, and component data at n >= 5.
3. CCB-037 v2 (engine swap + lighter menu) is the deterministic upper-bound
   route and the direct prerequisite for the n = 6 symmetric-strata campaign,
   whose quotient systems (9 variables) sit exactly at the measured wall; with
   the sympy engine they would wall too, with Singular-class engines Dias-Pan
   already demonstrated they do not.
4. The n = 5 spatial Dziobek dimension itself stays OPEN on our books:
   nothing here contradicts dim = 4, and the literature value is not imported
   as if we had verified it.

## Limitation restated (sections one-sidedness)

Random linear sections of codimension d see only components of dimension >= d;
components of smaller dimension are invisible, and the staircase bound reports
only the maximum. Had P2 decided, it would have certified only the MAXIMUM
dimension. This limitation is inherited by every instrument in this lane
except witness sets.

## Adversarial validation record (methodology/03)

- The caps were enforced by `timeout` inside WSL (probes) and by
  subprocess timeouts (pgb workers); the wall overshoots (313-330 s against
  300) are WSL startup and file-transfer overhead, not budget creep.
- The single completing subideal's 16 leading monomials were produced by a
  reduced grevlex Groebner basis; the union-bound argument (their Lemma 6.4:
  a SUBSET of LT(I) can only weaken the bound, never falsify it) makes
  d_pgb = 10 a valid, merely uninformative, bound. Nothing in the failure
  mode can have produced a spuriously LOW bound.
- The smoke gate's acceptances are exact rational or polynomial-reduction
  arithmetic; no numeric heuristics anywhere in the run.

## Records note

results.json carries the per-cell outcomes; the pgb union (16 exponent
vectors) is in pgb-union.json; every drawn section is in draws.json verbatim.
