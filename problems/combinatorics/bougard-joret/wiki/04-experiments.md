# 4. Exact controls

[EXP-001](../experiments/EXP-001-tree-strip/verdict.md) is CONFIRMED, with a uniform proof and separately labeled finite evidence. The 86 nonstar constructions pass two independence and two connectivity implementations; six star controls fail independence. Independent residual enumeration includes disconnected degree-equality models and rejects them. All 32,768 labeled six-vertex graphs were checked, finding 60 extremals and verifying every maximum-independent-set representation.

The [JSON certificate](../experiments/EXP-001-tree-strip/artifacts/certificate.json) contains deterministic counts and tree edge lists. These controls are not a proof for all $k$; the separate combinatorial derivation supplies that statement. The first informal connectivity argument omitted the two-vertex case, which the adversarial audit found and repaired before computation.
