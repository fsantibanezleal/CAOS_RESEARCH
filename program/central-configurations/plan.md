# Central configurations (Smale 6) - problem plan

Opened 2026-07-23. Area: dynamical-systems. State: exploring.
Context dossiers: `problems/dynamical-systems/central-configurations/context/`.

## Goal

Build the exact, replayable machine pipeline for finiteness-of-central-configurations
certificates; CALIBRATE it by reproducing the Hampton-Moeckel n = 4 certificate objects
in our own exact toolchain; then work the n = 5 landscape (Albouy-Kaloshin structure and
its exceptional variety) and attack the n = 6 frontier (planar, equal masses first, then
the 24 residual Chang-Chen zw-diagram cases). Honest deliverables: exactly verified
reproductions, certified counts, sharpened exclusions at the open frontier, null results
where the mathematics says no.

## The attack ladder (each rung names its certificate form)

| Rung | Content | Certificate form | State |
|---|---|---|---|
| CC-P0 Foundation | Deep-research dossiers (done at open); exact Albouy-Chenciner system builder (F/G/H/CM/IU polynomial forms, cleared denominators, sympy over QQ); calibration on n = 3: recover the Lagrange equilateral point and, on each collinear ordering chart, the Euler quintic with its unique positive root; assemble the n = 4 planar HM system and record its structure (supports, Newton polytope dimensions). EXP-001. | Exact Groebner bases over QQ / QQ(m); machine-checked identities; run.py exits nonzero on any mismatch | active (EXP-001) |
| CC-P1 The HM n = 4 reproduction | Direct read of HM06 (CCB-002); reproduce the certificate: (a) exact solution census for chosen exact mass vectors (equal masses first: 4 classes mod symmetry, 50 rotation-only, per MZ19/Simo); (b) the BKK data: Newton polytopes and mixed volume of the reduced system (exact polyhedral instrument, staged); (c) the torus-direction exclusions (initial-form ideals, saturation, Groebner). Target: our pipeline certifies "n = 4 finite for all positive masses" end to end. | Exact mixed-volume number + per-direction initial-ideal exclusion certificates (each a Groebner run persisted with inputs/outputs); alpha-theory or exact-Krawczyk certificates for any numerically-found solution set | pending |
| CC-P2 The n = 5 landscape | Direct read of AK12 (CCB-003); transcribe the zw-diagram machinery; reproduce the equal-mass planar count (5 classes, MZ19) with our own certified listing instrument (interval/Krawczyk in exact rational arithmetic); map the AK12 codim-2 exceptional variety explicitly; reproduce HJ11's spatial tropical certificate (prevariety f-vector (1, 576, 1620, 1420, 450), 44 cases, Table 1) with our own prevariety instrument; cross-check MZ26's exceptional-case counts. | Certified listing (Krawczyk certificates persisted per box); tropical prevariety computation with exact ray-by-ray exclusion records | pending |
| CC-P3 The n = 6 frontier | Planar equal masses first: reproduce the 9 classes (MZ19) independently; then transcribe the 24 residual Chang-Chen diagram cases exactly (CCB-004) and attack individual diagrams: exact elimination (Groebner/resultants with modfrac mod-p preprocessing), GPU homotopy landscaping certified a posteriori, per-diagram exclusion or explicit exceptional-mass narrowing. Any single new diagram closed is a publishable sharpening of the frontier. | Per-diagram: initial-ideal exclusion certificate, or an explicit mass-relation narrowing with exact elimination record | pending |
| CC-P4 Spatial ladder and bounds | Dziobek structure (Moeckel 2001; Dias 2026 Veronese bounds): reproduce the generic-finiteness dimension count; explore uniform-bound improvements at n = 4/5; spatial equal-mass cross-checks (MZ20). | Exact dimension/degree computations on the Dziobek-Veronese variety | pending |
| CC-P5 Consolidate + publish | Wiki 01-05 per unit as verdicts land; theme-aware SVGs; web page (published state gates per methodology/06); manuscript when validated + novel material exists (methodology/09). | Wiki transcribed from verdicts only | rolling |

## Strategy notes

- **Calibration before frontier**: every instrument (system builder, Groebner exclusion,
  polytope/mixed volume, prevariety, Krawczyk listing, homotopy + certification) is first
  validated against a published, known answer (the calibration targets table in the
  method dossier). Only validated instruments touch the open n = 6 cases.
- **Exact arithmetic policy** (methodology/04): verdict-bearing computations run over QQ
  (sympy 1.14, repo .venv); float/GPU exploration allowed for landscaping but every
  candidate is re-checked exactly or with certified interval arithmetic; modfrac (the
  jacobian program's rational-mod-p instrument) is reused for heavy Groebner runs.
- **Isolation** (methodology/08): this program owns only its own folders; rounds close
  with NO version bump; the release step is serialized and owned elsewhere.
- **Novelty discipline**: reproductions are labeled replications, never claimed as new;
  the novel surface is the n = 6 diagram frontier, exceptional-mass cases at n = 5, and
  any bound improvements; adversarial novelty passes before any such claim.
- **GPU relevance**: massive homotopy-path parallelism and equal-mass sweeps at n >= 6;
  enters at CC-P3, never carries a verdict alone.
- **UNVERIFIED discipline**: the [U] items in context/references.md (Smale verbatim text,
  Roberts masses, HM06 internals, Chang-Chen tables, RCD23 uniqueness) must be upgraded
  by direct reads before any conclusion depends on them.
