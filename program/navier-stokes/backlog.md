# navier-stokes: backlog

Created 2026-09-11 at open time. Nothing below has run; every item with machine time carries a budget
and a kill criterion per methodology 12.

| id | title | axis | status | priority | effort | budget | kill criterion |
|---|---|---|---|---|---|---|---|
| NS-001 | Read Sections 3 to 10 of the Alpoge-Buckmaster Boussinesq paper; determine whether the dissipative analysis is already there | research | done | P0 | M | none | n/a |
| NS-002 | Obtain the two Cordoba-Martinez-Zoroa primary sources ([5] and [6] of the Boussinesq paper) and read the layer organization at implementation level | research | done | P0 | M | none | n/a |
| NS-003 | EXP-001: build `openai/NavierStokesAndEuler` and run both Comparator challenges | validation | todo | P1 | L | 6 h wall clock, 60 GB disk on E: | abandon if the mathlib cache plus one module smoke build exceeds 90 min or if peak RSS exceeds available RAM |
| NS-004 | Statement audit of the unforced Euler certificate, to the standard already applied to (C) and (D) | validation | done | P1 | M | none | n/a |
| NS-005 | EXP-002 part A: inviscid modulation system reproduced with the exact profile `F`, not just `sin` | implementation | done | P1 | S | CPU only | n/a |
| NS-006 | EXP-002 part B: 2D pseudo-spectral Boussinesq solver on the GPU; positive control that the reduced system tracks the PDE through a growth, steering and holding cycle; negative control with a corrupted coefficient that must fail | implementation | done | P1 | XL | 8 GB VRAM, 4 h per run, one heavy job at a time | abandon the resolution if a single cycle does not fit in VRAM at the coarsest useful grid |
| NS-007 | EXP-003: add the time budget and hold-interval damping to the recursion, then sweep the threshold as a batched GPU ensemble | implementation | done | P2 | L | 1e5 to 1e7 trajectories, 2 h | stop if the transition surface is not stable under a doubling of the stage horizon |
| NS-008 | Project `.venv` with torch for the GPU, never global, per the isolated-environments rule | implementation | done | P1 | S | none | n/a |
| NS-009 | Wiki pages transcribing the mechanism, with KaTeX equations, real DOIs and theme-aware SVG figures, authored per unit as the units land | documentation | done | P2 | L | none | n/a |
| NS-010 | Re-read the Alpoge-Buckmaster hypo-dissipative paper the day it appears and compare its exponent with ours; record whoever is first | research | blocked | P2 | S | none | unblocks when they post |

## Standing obligations

- Nothing here is described as our discovery of a blowup mechanism. The mechanism belongs to Cordoba
  and Martinez-Zoroa; Alpoge and Buckmaster pushed it to smooth forcing; OpenAI produced a different
  mechanism for the viscous case.
- The `1/4` bound is UNVERIFIED for novelty until NS-001 and NS-002 close.
- Any claim reaching a manuscript needs a verdict citation, per methodology 12.
