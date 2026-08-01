# Exploration moment, 2026-08-01 (methodology/10 + 11)

Trigger: EXP-009's double cap and the EXP-010 design work done today. Three
threads, one adversarial question, one cross-problem instrument candidate.

## 1. What the double cap says about ENGINES, not about the problem

The route-B z-system is SMALL as text (347 bytes, twelve sparse equations) and
still produced nothing in an hour. So the wall is not encoding size or density:
it is intrinsic Groebner/RUR degree growth. This matters beyond this problem:
across the program, the choice "solve exactly vs bound vs certify a dimension"
should be made from DEGREE estimates, not from how big the input looks. The
mixed volume HM06 computed (25380 for their system) is, in retrospect, also a
cost forecast for any solver that must touch all complex solutions: a
Groebner-based census has to pay for thousands of solutions even when only
dozens are real and positive. Lesson adopted in EXP-010's design: never ask an
engine for more than the quantity the claim needs (a dimension needs sections,
not censuses).

## 2. Adversarial question against our own new lane

Random linear sections of codimension d SEE only components of dimension >= d;
components of dimension < d are invisible (a generic codim-3 plane misses every
curve and surface). So EXP-010's P1/P2, even if perfect, certify "max component
dimension = 3", NOT "every component has dimension 3". For generic finiteness
of the mass projection this is the right one-sided direction (what must be
excluded is dimension > 3 among dominating components), but the record must not
overstate: small components (if any) stay invisible to this instrument, and the
deterministic P3 rung also reports only the maximum (Krull dimension). If the
component STRUCTURE ever becomes the question (excess low-dimensional loci,
continua candidates), the witness-set lane (CCB-034) is the instrument, not
sections. This limit goes into the EXP-010 verdict text verbatim.

## 3. Cross-problem instrument candidate (lens: recognition / reusable tooling)

The pattern "recorded seeded random draws + exact arithmetic at the drawn
parameters + a posteriori Schwartz-Zippel-style failure bound from measured
degree data" is not specific to central configurations. It is a general
randomized-certificate discipline usable wherever a dimension or a rank is the
claim (the jacobian program's rank probes, future incidence computations at
n = 5, 6). If EXP-010 passes, factor the section-drawing and bound-reporting
into cclib (or a shared module) so the n = 5 spatial-Dziobek run (EXP-011) and
any other problem can reuse it with the same evidentiary shape: draw recorded,
bound computed, claim labeled probabilistic-exact vs deterministic. Candidate
backlog row after the verdict.

## Null-result honesty

No new mathematical fact was produced by this exploration; it produced one
design correction (state the sections' one-sidedness in the verdict), one
engine-strategy rule (degree forecasts before engine choice), and one tooling
candidate (shared randomized-certificate module). Recorded as required even
though modest.
