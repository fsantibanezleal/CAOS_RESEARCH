# navier-stokes: backlog

Created 2026-09-11 at open time. Nothing below has run; every item with machine time carries a budget
and a kill criterion per methodology 12.

| id | title | axis | status | priority | effort | budget | kill criterion |
|---|---|---|---|---|---|---|---|
| NS-001 | Read Sections 3 to 10 of the Alpoge-Buckmaster Boussinesq paper; determine whether the dissipative analysis is already there | research | done | P0 | M | none | n/a |
| NS-002 | Obtain the two Cordoba-Martinez-Zoroa primary sources ([5] and [6] of the Boussinesq paper) and read the layer organization at implementation level | research | done | P0 | M | none | n/a |
| NS-003 | EXP-001: build `openai/NavierStokesAndEuler` | validation | done (both halves build clean, 0 sorryAx) | P1 | L | 6 h wall clock, 60 GB disk on E: | abandon if the mathlib cache plus one module smoke build exceeds 90 min or if peak RSS exceeds available RAM |
| NS-011 | EXP-004: does the multi-layer handoff survive in the PDE? | implementation | done | P1 | L | 8 GB VRAM, one heavy job at a time | abandon a config above the 2/3 dealiasing limit (now a loud guard) |
| NS-012 | Euler certificate build: repair the mathlib cache corrupted by the disk-deletion storm and rebuild | validation | done | P2 | L | forced cache re-fetch 2 h, build 8 h | abandon below 5 GB free on E: |
| NS-004 | Statement audit of the unforced Euler certificate, to the standard already applied to (C) and (D) | validation | done | P1 | M | none | n/a |
| NS-005 | EXP-002 part A: inviscid modulation system reproduced with the exact profile `F`, not just `sin` | implementation | done | P1 | S | CPU only | n/a |
| NS-006 | EXP-002 part B: 2D pseudo-spectral Boussinesq solver on the GPU; positive control that the reduced system tracks the PDE through a growth, steering and holding cycle; negative control with a corrupted coefficient that must fail | implementation | done | P1 | XL | 8 GB VRAM, 4 h per run, one heavy job at a time | abandon the resolution if a single cycle does not fit in VRAM at the coarsest useful grid |
| NS-007 | EXP-003: add the time budget and hold-interval damping to the recursion, then sweep the threshold as a batched GPU ensemble | implementation | done | P2 | L | 1e5 to 1e7 trajectories, 2 h | stop if the transition surface is not stable under a doubling of the stage horizon |
| NS-008 | Project `.venv` with torch for the GPU, never global, per the isolated-environments rule | implementation | done | P1 | S | none | n/a |
| NS-009 | Wiki pages transcribing the mechanism, with KaTeX equations, real DOIs and theme-aware SVG figures, authored per unit as the units land | documentation | done | P2 | L | none | n/a |
| NS-013 | Reconstruct the published threshold from Cordoba-Martinez-Zoroa-Zheng's own exponent budget, and re-examine the round-1 calibration | research | done 2026-09-14 (calibration withdrawn as tautological) | P1 | M | none | n/a |
| NS-014 | EXP-005: transcribe the first-stage steering control and run the growth, steering and hold cycle in the PDE, then the dynamical two-layer handoff | implementation | done 2026-09-15 (DECIDED IN PART: A, B, C pass; committed parameters refuted; D at 0.808 below its 0.9 gate) | P1 | XL | 8 GB VRAM, one heavy job at a time | abandon a configuration whose wave exceeds the 2/3 dealiasing limit (loud guard) |
| NS-015 | EXP-006: independent kernel replay of the certificate with the toolchain's `leanchecker` | validation | done 2026-09-16 (CONFIRMED: both halves replayed from an empty environment) | P1 | L | 6 h wall clock, 4 Lean threads | abandon if resident memory exceeds available RAM or a module exceeds 30 min |
| NS-016 | Add a force-regularity budget to our cascade model, the constraint that actually sets the published constant | implementation | done 2026-09-17: the force budget of the smooth-forcing design transcribed from its Sections 5-8 (`ab_force_budget.py`); it corrected the v0.04 design bound, republished as v0.05 | P2 | L | CPU only | n/a |
| NS-017 | Apply our dissipative extension to the published Alpoge-Buckmaster schedule and record the prediction it implies, with a falsification criterion | research | done 2026-09-16 (prediction UNVERIFIED by construction; NS-010 checks it) | P2 | M | CPU only | n/a |
| NS-018 | EXP-007: does localization break the dissipative reduction? | validation | done 2026-09-17 (CONFIRMED: cost is 3.6 alpha/(ell lambda), negligible at their separations) | P1 | S | GPU seconds, no time stepping | n/a |
| NS-019 | Transcribe the Euler paper's force budget the same way (Section 12: J = 2k + 8, N^(-7/8), Q_i = q_0 + i, k <= Q/c_Q) and settle whether its growth scale is the square root of the background gradient | research | todo | P2 | L | CPU only, 112-page reading unit | n/a |
| NS-010 | Re-read the Alpoge-Buckmaster hypo-dissipative paper the day it appears and compare its exponent with ours; record whoever is first | research | blocked | P2 | S | none | unblocks when they post |

## Standing obligations

- Nothing here is described as our discovery of a blowup mechanism. The mechanism belongs to Cordoba
  and Martinez-Zoroa; Alpoge and Buckmaster pushed it to smooth forcing; OpenAI produced a different
  mechanism for the viscous case.
- The `1/4` bound is UNVERIFIED for novelty until NS-001 and NS-002 close.
- Any claim reaching a manuscript needs a verdict citation, per methodology 12.
