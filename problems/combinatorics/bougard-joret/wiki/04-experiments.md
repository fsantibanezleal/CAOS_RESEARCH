# 4. Exact controls

[EXP-001](../experiments/EXP-001-tree-strip/verdict.md) is CONFIRMED, with a uniform proof and separately labeled finite evidence. The 86 nonstar constructions pass two independence and two connectivity implementations; six star controls fail independence. Independent residual enumeration includes disconnected degree-equality models and rejects them. All 32,768 labeled six-vertex graphs were checked, finding 60 extremals and verifying every maximum-independent-set representation.

The [JSON certificate](../experiments/EXP-001-tree-strip/artifacts/certificate.json) contains deterministic counts and tree edge lists. These controls are not a proof for all $k$; the separate combinatorial derivation supplies that statement. The first informal connectivity argument omitted the two-vertex case, which the adversarial audit found and repaired before computation.

## EXP-002: full first interior shell

The [certificate](../experiments/EXP-002-next-shell/artifacts/certificate.json) records PASS for 75 constructed graphs over $3\le k\le12$, every $2\le\alpha\le k+1$. There are 45 independent direct subset/cut checks, 36 Harary cases, 15 odd-degree-sum cases, 75 damaged-edge rejection controls, and eight complement-cycle controls. The full order-six census checks 32,768 labeled graphs and finds exactly 60 extremals, all complements of six-cycles.

These are finite controls, not an exhaustive census of larger orders. The [written proof](../experiments/EXP-002-next-shell/proof.md) supplies the universal quantifier; the [verdict](../experiments/EXP-002-next-shell/verdict.md) owns the final audit disposition. EXP-001's artifacts and theorem remain unchanged.
