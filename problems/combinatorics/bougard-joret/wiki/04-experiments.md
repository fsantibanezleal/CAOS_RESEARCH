# 4. Exact controls

[EXP-001](../experiments/EXP-001-tree-strip/verdict.md) is CONFIRMED, with a uniform proof and separately labeled finite evidence. The 86 nonstar constructions pass two independence and two connectivity implementations; six star controls fail independence. Independent residual enumeration includes disconnected degree-equality models and rejects them. All 32,768 labeled six-vertex graphs were checked, finding 60 extremals and verifying every maximum-independent-set representation.

The [JSON certificate](../experiments/EXP-001-tree-strip/artifacts/certificate.json) contains deterministic counts and tree edge lists. These controls are not a proof for all $k$; the separate combinatorial derivation supplies that statement. The first informal connectivity argument omitted the two-vertex case, which the adversarial audit found and repaired before computation.

## EXP-002: full first interior shell

The [certificate](../experiments/EXP-002-next-shell/artifacts/certificate.json) records PASS for 75 constructed graphs over $3\le k\le12$, every $2\le\alpha\le k+1$. There are 45 independent direct subset/cut checks, 36 Harary cases, 15 odd-degree-sum cases, 75 damaged-edge rejection controls, and eight complement-cycle controls. The full order-six census checks 32,768 labeled graphs and finds exactly 60 extremals, all complements of six-cycles.

These are finite controls, not an exhaustive census of larger orders. The [written proof](../experiments/EXP-002-next-shell/proof.md) supplies the universal quantifier; the [verdict](../experiments/EXP-002-next-shell/verdict.md) owns the final audit disposition. EXP-001's artifacts and theorem remain unchanged.

## EXP-003: the next triangle-free matching level

The [preflight](../experiments/EXP-003-triangle-free-next-matching/hypothesis.md) was committed and pushed at `f3fdda6` before computation. The [proof](../experiments/EXP-003-triangle-free-next-matching/proof.md) establishes the fixed-order upper bound and $T(d,d+1)=d^2+d+2$ for all $d\ge7$, plus the secondary one-edge Bougard-Joret bracket. Independent reasoning audit passed. The separate next-matching manuscript is [published v0.01](https://doi.org/10.5281/zenodo.22343022): all seven pages passed visual QA, no final LaTeX warnings remain, and 101 tests passed. The [publication receipt](../../../../manuscripts/bougard-joret/next-matching/publication-verification.json) confirms latest-version status and all 352,871 bytes against a fresh unauthenticated download. Scoped integration remains pending.

The [exact certificate](../experiments/EXP-003-triangle-free-next-matching/artifacts/certificate.json) is PASS for 24 degrees, $d=7,\ldots,30$, with two saved constructions per degree. It checks 48 graphs, rejects all 24 raw-complement connectivity shortcuts, and finds zero survivors among 287,564 positive five-type candidates with a designated singleton. The original checker performs full complement-flow checks on 24 graphs through $d=18$.

The separate [NetworkX audit](../experiments/EXP-003-triangle-free-next-matching/artifacts/independent-audit.json) reconstructs all 48 saved graphs and verifies matching number, complement independence, and full complement connectivity for every one of them. Both receipts retain the triangle-corruption rejection and the $d=6$ boundary control: a balanced five-cycle blowup has 45 edges, exceeding the out-of-range formula 44. The finite five-type enumeration corroborates the symbolic contradiction; it is not an arbitrary-graph census or the basis of the universal theorem.
