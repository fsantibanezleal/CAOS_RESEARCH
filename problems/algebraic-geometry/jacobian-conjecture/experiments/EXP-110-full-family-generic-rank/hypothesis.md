# EXP-110 - The generic rank of the FULL 51-parameter GGHV family

## Question

Is the reduced GGHV matrix \(M(\varepsilon)\) of maximal rank 125 GENERICALLY
over the whole 51-parameter family, and if so what is the exact zero locus of a
witnessing maximal minor?

## Why this and not EXP-109 (the plan redirect)

EXP-101 through EXP-108 closed 2- and 3-coefficient SLICES. A slice fixes the
other 48+ coefficients, so its rank statement does not extend to the family, and
enumerating slices cannot terminate: C(51,3) = 20,825 and C(51,4) = 249,900,
each currently costing hours of exact elimination with fiber degrees growing per
added coefficient. EXP-109 continues that enumeration and is therefore NOT the
highest-value next step.

EXP-098 already identified the correct stronger object: a CONSTRUCTIBLE RANK
STRATIFICATION of the parameter space. The first step of that recursion, run on
the FULL family rather than on a slice, is a single computation.

## Preflight (methodology/12)

- P1 source-complete: the matrix construction is our own transcription
  (EXP-052 onward, GGHV Prop 4.3); no external source gates this step.
- P3 premise dependencies: (a) M has 125 output rows and the pool construction of
  EXP-064/067 [verdicts]; (b) uniform inconsistency does not require a global
  covector [EXP-098, independently re-verified this session]; (c) no global
  polynomial covector exists at degree <= 3 [EXP-067/072/075].
- P4 one-sidedness, stated BEFORE the run:
  * generic rank 125 found => the certificate holds on a dense open set, and the
    residual stratum is the proper closed subvariety cut by the chosen minor.
    This does NOT by itself close the family; it names the next target exactly.
  * generic rank < 125 found => a genuine obstruction: a nonzero kernel over the
    function field, i.e. a global covector over Q(eps). That would be a MAJOR
    positive result and must be reported to Felipe before any claim.
- P5 invariant-first: the deciding invariant is a single rank over the rational
  function field Q(eps_1..eps_51), computed at a random rational specialisation
  first (cheap, one-sided: full rank at a point PROVES generic full rank).
- P6 budget: 20 minutes for the specialisation probe; kill and report if the
  matrix build exceeds it. Exact/symbolic minor work only after the probe.

## Predictions

1. [MV] The reduced matrix builds with the recorded shape (125 output rows).
2. [MV] At a random rational parameter point the rank is 125 (=> generic rank is
   125 over the function field, since rank is lower-semicontinuous and a single
   full-rank point certifies genericity).
3. [D] Consequently the certificate class of interest is supported on the proper
   closed locus where all maximal minors vanish, and the next exact target is
   that locus, computed once for the whole family rather than slice by slice.

Declared 2026-07-26 before implementation.
