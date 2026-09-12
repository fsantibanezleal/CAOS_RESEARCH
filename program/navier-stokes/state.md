# navier-stokes: state (heartbeat)

| Date | From | To | Evidence |
|---|---|---|---|
| 2026-09-11 | proposed | scoped | Scoping decided by the two 2026-09-05 portfolio reviews plus the deep-research pass of 2026-09-11; primary sources read and hashed |
| 2026-09-11 | scoped | opened | Context dossiers persisted at `3f8d76d`; `plan.md`, `state.md`, `backlog.md`, `RESUME.md` written; strategy chosen and scope limits declared |

- **State:** opened (2026-09-11). No experiment has been run. The plan is awaiting Felipe's validation
  before any machine time, per the mandatory build sequence step 3.
- **Area:** analysis-pde. This is the first problem opened in that area; it was previously an area
  name with nothing on disk.
- **Feasibility:** the portfolio row stays B. The Clay problem is not our target and the 2026-09-05
  verdict that numerical regularity cannot replace the breakdown argument still holds. The restricted
  question we opened (dissipation threshold of the layer-cascade ansatz) has a class A surface, and
  that distinction is recorded in `plan.md` rather than by inflating the row.

## Done, 2026-09-11 (opening round, research only)

Deep-research pass persisted before any plan. Primary sources downloaded, hashed and read to the depth
recorded in `problems/analysis-pde/navier-stokes/context/references.md`: the OpenAI Navier-Stokes and
Euler manuscripts, the three Alpoge-Buckmaster papers, Buckmaster's priority statement, Fefferman's
official Clay text, and eleven background references.

Findings recorded:

- OpenAI Theorem 1.1 matches Fefferman alternative (C) clause by clause, and is stronger than (C)
  requires in two respects: compactly supported force rather than merely rapidly decaying, and zero
  initial velocity.
- Their companion Euler theorem is **unforced**, which is the stronger mathematical claim and the one
  with no Clay reference statement to be audited against.
- Lean statement audit: `openai/NavierStokesAndEuler` states (C) and (D) faithfully. 2,659 files,
  641,332 lines, zero `sorry` outside the comparator reference stubs, zero added axioms, and the
  reference statement is adapted from DeepMind's Formal Conjectures, so it was authored by a third
  party before the claim existed. The Euler certificate has not been audited.
- The Alpoge-Buckmaster modulation system transcribed exactly. The growth rate is
  `sqrt(A) sin(phi)`, settled by computing the matrix rather than by reading mangled PDF glyphs, and
  it carries no dependence on the wave frequency.
- Derived here: the dissipative modulation system, the frequency cap
  `lambda <= A^(1/(4 alpha)) nu^(-1/(2 alpha))`, and an upper bound of `1/4` on the cascade
  dissipation exponent.

## Refuted inside the same session, and preserved

The first draft of the evaluation read the recursion coefficient crossing as a clean critical exponent
`alpha_c = 1/4`. The smoke test in `problems/analysis-pde/navier-stokes/code/modulation_smoke.py`
refuted that reading: over 4,000 stages, two legal amplitude budgets and four viscosities, escape below
`1/4` is not automatic (at `alpha = 0.24` it happens in 4 of 8 settings), so the transition depends on
`nu` and on how the budget is spent. The surviving statement is the weaker one, that `1/4` is an upper
bound and no escape was observed above it. Two omissions are recorded and both push the real threshold
down: the recursion has no time axis, and dissipation is not charged during the holding intervals.

The part that survives untouched, and the reason the line is worth pursuing: classical viscosity is
`alpha = 1`, four times the bound, and the failure there is not marginal in any parameter setting
tried. The naive layer cascade does not reach classical Navier-Stokes.

## Next

Phase 0 of `plan.md`: close the primary-source gap on Sections 3 to 10 of the Alpoge-Buckmaster
Boussinesq paper and on the two Cordoba-Martinez-Zoroa sources. If the dissipative analysis is already
published there, the plan is rewritten rather than executed.
