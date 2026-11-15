# EXP-006 preflight: the frontier value on Afrasyab's odd-cycle family, uniform and non-uniform (UFB-065)

Date: 2026-11-14. Status: frozen before any computation of this experiment. CPU only, exact rationals.

Numbering note: this is the conflict-structure experiment that UFB-037 planned and UFB-065 re-scoped.

## Question

Afrasyab (arXiv:2609.17568 v1, Theorems 5, 7 and 8) realises any odd cycle as an acyclic single-source
unsplittable-flow instance. On the uniform family his cost vector gives tau* = 1 - t (Theorem 8), below 2/3 for C5;
the 2026-11-07 preflight found the frontier value of his C5 instance (eps = 1/120) to be exactly 79/120, so his
pricing is optimal there. The programme's best lower bound on the cost-preserving constant is alpha* >= 9/8 (EXP-005,
Muffatti's planar family). Does any member of the odd-cycle family on C5, uniform or not, have a frontier value above
9/8, and what is the largest value the family reaches on the sampled space?

## Instrument

- `ufclib.frontier_value_cp` (exact cutting-plane frontier evaluator) and `ufclib.odd_cycle_instance` /
  `ufclib.afrasyab_uniform`, merged in CAOS_RESEARCH PR #425 (commit 2e064021). The evaluator agrees with
  `frontier_value` on every instance where both finish (37 tests) and returns 79/120 on the uniform C5 member in about
  30 s on one process. Spec of the family: CAOS_MANAGE `wip/caos-research/uf-afrasyab-construction-2026-11-14.md`
  (D2, D3).
- A member is valid when the builder accepts it: acyclic, single source, every flow nonnegative and conservation
  exact, so the fractional flow is feasible; every terminal has 3 simple paths. The realisation conditions of the paper
  are not imposed (decision of 2026-11-14); the odd-cycle violation sum_i x(final_i)/b_i - 2 (R4 of the spec) is
  recorded per member as a descriptor.
- The frontier value is invariant under scaling every demand and flow by one positive factor, so each member is
  normalised to d_max = max(max_i b_i, max_i delta_i) = 1.

## Stages

- Stage A (calibration, uniform C5, Afrasyab's construction): eps in {1/120, 1/60, 1/24, 1/16, 1/13}.
- Stage B (symmetric members, every gadget equal): (b, delta) in {(1/3, 1), (2/3, 1), (1, 1), (1, 1/3), (1, 2/3)};
  r, u, approach in {0, 1/6, ..., 6/6}; every valid combination.
- Stage C (non-uniform random members): 2,000 valid members, each gadget's five parameters drawn independently
  (b, delta from {1/6, ..., 6/6}, r, u, approach from {0, 1/12, ..., 12/12}), then normalised to d_max = 1; seed
  20261114; invalid draws are redrawn and counted.
- Stage D (local search): from the 10 best members of B and C, steps of +-1/24 on one parameter of one gadget,
  accepting strict improvements, at most 150 evaluations per start.

## Predictions

- P1 (calibration): at each eps of Stage A the frontier value equals 2/3 - eps exactly (tau* of Theorem 8 with
  k = 2), so Afrasyab's pricing is optimal across the uniform family.
- P2 (main): no member of stages B, C or D has a frontier value above 9/8.
- P3: no member has a frontier value above 1 (no member of the family is a counterexample instance at all).
- P4 (exploration, no value predicted): the largest value of each stage, with its parameters, its witness cost vector
  and its R4 descriptor.

## Consequences fixed in advance

- P2 holds: UFB-065 is answered on the sampled space: the odd-cycle family on C5 does not raise alpha* past 9/8 there.
  The record states the sampled space; nothing is claimed beyond it.
- P2 fails: the member is re-checked by an independent route (an exact enumeration of the routings that cost no more
  than the fractional flow under the witness pricing, with their least violation) before any claim; a confirmed value
  above 9/8 would raise the programme's lower bound.
- P1 fails at some eps: the optimal pricing beats Afrasyab's there; reported with the witness cost vector.

## Budget

At most 4 hours of 14 processes for stages B to D; stage A takes minutes. Stopping early is allowed; the record states
what ran.
