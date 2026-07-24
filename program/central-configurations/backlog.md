# Central configurations - problem backlog

| id | title | phase | status | updated | notes |
|---|---|---|---|---|---|
| CCB-001 | EXP-001 calibration: exact AC-system builder; n = 3 classification recovered (Lagrange point + Euler quintics per ordering); n = 4 planar HM system assembled with structure recorded | CC-P0 | doing | 2026-07-23 | hypothesis before run; the toolchain shakedown |
| CCB-002 | Direct read of HM06 (Invent. Math. 163): DONE (author PDF read in full; certificate anatomy transcribed to context/2026-07-24-hm06-direct-read-dossier.md; PDF archived on E: with SHA-256; tags upgraded) | CC-P1 | done | 2026-07-24 | reproduction targets now numeric: 12828/2980/53/19 faces, facets 22+33, Mixvol 25380 |
| CCB-003 | Direct read of AK12 (Annals 176): zw-diagrams, the explicit codim-2 exceptional variety for n = 5 | CC-P2 | todo | 2026-07-23 | also the basis of Chang-Chen |
| CCB-004 | Chang-Chen (I) JSC 2024 + (II) SIADS 2025: transcribe the 24 residual diagrams + mass relations exactly | CC-P3 | todo | 2026-07-23 | the frontier target list |
| CCB-005 | Fetch + archive HJ11 Sage worksheet (FiveBodySpatial.sws); diff against our prevariety reproduction | CC-P2 | todo | 2026-07-23 | |
| CCB-006 | Roberts 1999 PDF: the continuum construction, exact masses; upgrade [U] | CC-P0 | todo | 2026-07-23 | positivity-necessity exhibit |
| CCB-007 | Exact mixed-volume / BKK instrument (polyhedral, over QQ); validate on textbook examples then on the HM system | CC-P1 | todo | 2026-07-23 | staged; Gfan wrap as fallback |
| CCB-008 | Tropical prevariety instrument; validate against HJ11 f-vector (1, 576, 1620, 1420, 450) | CC-P2 | todo | 2026-07-23 | |
| CCB-009 | Certified listing instrument (Krawczyk in exact rational / directed-rounding interval); validate on n = 3, then n = 4 equal masses (4 classes), then n = 5 equal masses (5 classes) | CC-P2 | todo | 2026-07-23 | MZ19 is the ground truth |
| CCB-010 | Equal-mass n = 6 planar independent reproduction (9 classes) | CC-P3 | todo | 2026-07-23 | entry rung of the frontier |
| CCB-011 | Smale 1998 Intelligencer paper: verbatim problem 6 text; upgrade [U] | CC-P0 | todo | 2026-07-23 | |
| CCB-012 | Wiki 01-05 + SVGs + web page (published-state gates) | CC-P5 | todo | 2026-07-23 | vertical, per unit, from verdicts |
| CCB-013 | Roberts-continuum anatomy: exact reproduction, AC-Jacobian rank drop along the family, positivity obstruction target | CC-P2 | todo | 2026-07-23 | lens 2+4 (lenses-2026-07-23.md); gated on CCB-006 |
| CCB-014 | Hessian/degeneracy instrument: exact nullity of Hess(U at I=1) at exact CCs; Morse-Bott continuum detector; calibrate on EXP-001 exact points | CC-P1 | todo | 2026-07-23 | lens 4; feeds per-diagram exclusions |
| CCB-015 | Incidence-variety local-dimension certificates (Jacobian rank over QQ at exact sample points), n = 5, 6 planar | CC-P2 | todo | 2026-07-23 | lens 3 (recognition); generic-finiteness evidence |
| CCB-016 | Cluster-recursion reading of zw-diagrams (collapse hierarchy governed by sub-cluster CCs); literature check vs Moeckel notes cluster sections + Xia 1991 FIRST | CC-P3 | todo | 2026-07-23 | lens 9; novelty pass mandatory |
| CCB-017 | Two-sided construction attempt: certified local continuation at exact masses ON one Chang-Chen residual mass relation | CC-P3 | todo | 2026-07-23 | lens 6; gated on CCB-004 |
| CCB-018 | Symmetry-quotiented diagram exclusions (diagram automorphism groups shrink the Groebner certificates) | CC-P3 | todo | 2026-07-23 | lens 5; port of the jacobian GL2-orbit pattern |
| CCB-019 | Vortex/homogeneous-potential transfer: exponent-parametric certificates; vortex prototypes of diagram kills | CC-P4 | todo | 2026-07-23 | lens 7; route R6 promotion |
| CCB-020 | n = 7 zw-diagram-count scoping via Chang-Chen combinatorics (size the next frontier honestly) | CC-P3 | todo | 2026-07-23 | lens 8; scoping only |
| CCB-021 | Fetch + archive the HM06 companion Mathematica notebook (www.math.umn.edu/~rick, their ref [18]) for diffing against our reproduction | CC-P1 | todo | 2026-07-24 | |
| CCB-022 | Implement the HM06 z-variable square system (their eq. (13), 10 eqs / 10 unknowns) in cclib + the mixed-volume rung target 25380 | CC-P1 | todo | 2026-07-24 | BKK applies to the square system only |
| CCB-023 | AK12 direct read (Annals PDF archived on E: with SHA-256): zw-diagram machinery + the explicit exceptional variety; supersedes the fetch part of CCB-003 | CC-P2 | doing | 2026-07-24 | pp. 535-540 read (skim addendum); full anatomy pending |
| CCB-024 | Jensen-Leykin arXiv:2301.02305: READ IN FULL (direct-read dossier 2026-07-24; PDF archived with SHA-256). Barrier at n = 6 = valuation choice + equation variant at ~100-cpu-day scale; gfan one-liners published; opens CCB-029..031 | CC-P2/P3 | done | 2026-07-24 | the live generic-mass frontier |
| CCB-029 | DONE (EXP-003 CONFIRMED): gfan 0.7 built (cstdint patch, hashes recorded); both JL25 n = 5 f-vectors reproduced EXACTLY + pointedness independently verified; ~6 wall-min/valuation on 30 threads. HJ11 spatial f-vector validation folded into CCB-028 | instrument | done | 2026-07-24 | the tropical lane is open |
| CCB-030 | Valuation-search experiment series at n = 5 (systematic valuation families; map pointedness success/failure; minutes per try per JL25); produce a principled n = 6 shortlist | CC-P3 | todo | 2026-07-24 | hypothesis-first; novel, cheap, direct n = 6 leverage |
| CCB-031 | Equation-variant prevariety shrinking at n = 4, 5 (G / Dziobek / e_IU variants; f-vector + pointedness deltas): the EXP-002 P1 phenomenon at prevariety level, answering JL25's explicit call for "different versions of the AC equations" | CC-P3 | todo | 2026-07-24 | our sharpest candidate contribution to generic n = 6 |
| CCB-025 | msolve engine wrap (RUR + certified isolating boxes) as the census computation layer; sympy stays the specification + independent-verification layer; WSL/passagemath route on Windows; binaries + hashes recorded | instrument | todo | 2026-07-24 | triggered by the (1,2,3) census timing; HM06 precedent: Mathematica checked with Macaulay2 |
| CCB-026 | Evaluate HomotopyContinuation.jl + certification (arXiv:2011.05000, 2401.17973, 2603.17288) as the landscaping engine (never verdict-carrying alone) | instrument | todo | 2026-07-24 | |
| CCB-027 | Four-formulations catalog: AC distances / HM z-system / AK12 delta-system / Laura-Andoyer (arXiv:2606.31582); per-rung engine choice | CC-P1..P4 | todo | 2026-07-24 | lens 7 |
| CCB-028 | Wrap OSCAR/polymake/gfan for the tropical prevariety rung; validate on HJ11's f-vector (1, 576, 1620, 1420, 450); upgrades CCB-008 | CC-P2 | todo | 2026-07-24 | never hand-roll polyhedral code first |
