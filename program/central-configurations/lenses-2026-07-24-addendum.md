# Lenses addendum (2026-07-24): the multi-factorial sweep after rounds 1-2

Per methodology/10's multi-factorial standing rule (adopted this day): fresh online
sweep, self-questioning of our own approaches against what rounds 1-2 measured, new
viewpoints and paths. Supplements lenses-2026-07-23.md; dispositions still live in
routes; new paths land as CCB-024..028.

## Load-bearing new findings (online sweep, 2026-07-24)

1. **Jensen-Leykin, "Smale's 6th problem for generic masses" (arXiv:2301.02305,
   v2 August 2025, 7 pages).** A NEW method aiming, for a GIVEN n, to prove generic
   finiteness of planar CCs; "the human part of the proof relies on tropical
   geometry", the rest is computation; COMPLETED for n <= 5 (confirming AK12
   generically). Authors: the Gfan author (and HJ11 co-author) + a numerical-AG
   monodromy expert. This is the closest active program to our spine and is DESIGNED
   to scale in n. Consequences: (a) read + transcribe (their pipeline likely reuses
   Gfan; code availability to check); (b) our CC-P2/P3 reproduction rungs should
   target THEIR pipeline as well as AK12's, since the n = 6 generic case may be a
   computation-scaling question rather than new mathematics; (c) novelty discipline:
   any generic-finiteness ambition of ours at n = 6 must be positioned relative to
   this program, not to AK12 alone. NEW PATH: CCB-024 (read; assess their n = 6
   feasibility barrier; contact only after we have a reproduction, per standing
   rule). [V: arXiv abstract fetched 2026-07-24.]
2. **msolve (Berthomieu-Eder-Safey el Din, open-source C; RUR + certified isolating
   boxes for 0-dim systems).** Industrial-strength exact solving: Groebner (F4) +
   rational univariate representation + real-root isolation with rational boxes:
   EXACTLY our census task, orders of magnitude faster than our sympy path. Our
   round-2 measurement (a single (1,2,3) enriched census exceeding 15+ minutes in
   sympy) is the self-questioning trigger: the census INSTRUMENT is sound but the
   ENGINE underneath should be msolve where available, with our exact residual
   acceptance kept as the independent verification layer (cross-implementation
   agreement, methodology/03 route 3). Windows caveat: msolve is Linux-first; wrap
   via WSL or the passagemath wheels; binaries + hashes recorded in-repo. NEW PATH:
   CCB-025. [Vs: msolve.lip6.fr + arXiv:2104.03572.]
3. **Modern tropical stack**: OSCAR/polymake/gfan remain the canonical prevariety
   tools (OSCAR 2025 Springer volume; zero-dim tropicalizations in OSCAR,
   arXiv:2511.23298; parallel prevariety computation, arXiv:1705.00720). Our CCB-008
   prevariety instrument should WRAP these (recorded binaries) rather than hand-roll
   polyhedral code, with exact spot-verification on HJ11's published f-vector.
   Updates CCB-008 disposition. [Vs: search pass.]
4. **Certified numerical algebraic geometry matured**: validated path tracking
   (arXiv:2401.17973), certified Galois/monodromy actions via homotopy graphs
   (arXiv:2603.17288, 2026). Relevant to the GPU landscaping rung: monodromy solving
   with a posteriori certification is now standard enough to be verdict-adjacent
   (still never verdict-carrying alone in our methodology). NEW PATH: CCB-026
   (evaluate HomotopyContinuation.jl + certification as the landscaping engine).
5. **Sun, "Degeneracy of planar central configurations" (arXiv:2510.25649, Oct
   2025).** Directly on our invariant-lens target (CCB-014, the Hessian/Morse-Bott
   detector): read before building, to avoid re-deriving known degeneracy structure.
   NEW PATH: folded into CCB-014 as a read-first gate. [U: abstract not yet read.]
6. **"Generalized Laura-Andoyer equations and the enumeration of some symmetrical
   classes of Dziobek configurations" (arXiv:2606.31582, June 2026).** A fourth
   equation formulation (beyond AC distances, HM z-system, AK12 delta-system) plus
   symmetric Dziobek enumeration: feeds the symmetry lens (CCB-018) and the spatial
   ladder (CC-P4). NEW PATH: CCB-027 (catalog + compare the four formulations;
   choose per-rung the one with the smallest certified computation). [U: not read.]

## Self-questioning record (what rounds 1-2 changed in our own view)

- Our sympy-only engine assumption is WRONG at scale: the (1,2,3) census timing shows
  the pure-sympy route saturates already at n = 3 enriched with ugly masses. Decision:
  keep sympy as the specification + verification layer; adopt msolve/OSCAR-class
  engines as the computation layer, always with independent exact acceptance checks
  (this mirrors HM06 itself: Mathematica computations CHECKED with Macaulay2).
- Our "reproduce HM06 then AK12 then Chang-Chen" ladder implicitly assumed the
  frontier is static; Jensen-Leykin shows the generic-masses frontier is ACTIVE and
  tropical-computational: our differentiation is the ALL-masses question (exceptional
  sets included), the certified-census instruments, and the record discipline; keep
  the reproduction ladder but track their program explicitly.
- EXP-002's P2 duplicates + caps were instrument artifacts, not mathematics: the
  correction (sqf dedup + charpoly eliminants + pre-filter) is in; the verdict must
  present P2's first-run failure honestly as an instrument finding.

## New backlog rows minted

CCB-024 Jensen-Leykin read + feasibility assessment (lens 11 + 3 + 9).
CCB-025 msolve engine wrap + cross-verification layer (instrument; lens 10 discipline).
CCB-026 certified homotopy/monodromy landscaping evaluation (lens 2/6 support).
CCB-027 four-formulations catalog (AC / HM-z / AK12-delta / Laura-Andoyer) with
per-rung engine choice (lens 7).
CCB-028 OSCAR/polymake/gfan wrap for the prevariety rung, validated on HJ11's
f-vector (upgrades CCB-008).
