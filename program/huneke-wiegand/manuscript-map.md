# Huneke-Wiegand result and manuscript map

Updated 2026-09-20. This map separates mathematical evidence, strategic value,
manuscript coverage, and external novelty. Experiment verdicts remain the
authority for proofs and refutations.

## Status boundary

The broad Huneke-Wiegand conjecture is already false. Son Pham retains priority
for the first public numerical-semigroup counterexample. The CAOS program is an
extension and classification program. It does not claim the original disproof.

Internal exact validation and Zenodo persistence do not establish peer review
or worldwide novelty. The source searches recorded in the context dossiers did
not locate exact matches for the results below, but specialist confirmation is
still required.

## Result blocks

| block | experiments | result status | value | manuscript home |
|---|---|---|---|---|
| Public-candidate replication and overring baseline | EXP-001--003 | reproduced, not novel | trusted starting point | `frobenius-minimality`, provenance only |
| Frobenius minimum and minimum-layer uniqueness | EXP-004, EXP-005, EXP-007 | all-parameter or complete finite classification | direct, high | `frobenius-minimality`; future focused submission A |
| Infinite family and endomorphism/trace anatomy | EXP-006--013 | proved with preserved refutations | direct, high | `frobenius-minimality`; future focused submission A |
| Conductor, reduction, tangent cone, and special fiber | EXP-014--024 | uniform theorems with negative controls | specialized, coherent | `frobenius-minimality`; future focused submission B |
| Curvilinear and Groebner geometry | EXP-025--026 | uniform focused theorems | specialized, coherent | `curvilinear-fiber-cones` |
| Betti rows, idealization, mapping cone, and lower cells | EXP-027--036 | several uniform theorems plus finite boundaries | specialized, significance review required | `frobenius-minimality`; future focused submission C |
| Recurrence and carrier search | EXP-037--053 | mostly refuted, inconclusive, or finite bridge evidence | research record | no standalone manuscript trigger |
| Full-map torsion family | EXP-054--062 | uniform direct-summand theorem | potentially strong homological result | `integral-connecting-annihilators` |
| Carrier comparison and endpoint sources | EXP-063--066 | finite exact comparison plus uniform projected endpoint theorem | conditional on canonical comparison | `integral-connecting-annihilators` v0.04 |

## Published manuscripts

### Consolidated source: Frobenius minimality

- Current public version: v0.25.
- Version DOI: `10.5281/zenodo.22835108`.
- Concept DOI: `10.5281/zenodo.21763582`.
- Coverage: EXP-001--037, with refuted predictions retained as results.
- Decision: freeze as the immutable consolidated record. It is too broad for a
  single future journal submission.

Focused submission split:

1. **Submission A, counterexample classification and families.** Minimality,
   minimum-layer uniqueness, the infinite family, and the endomorphism/trace
   mechanism. Central question: how isolated is the public counterexample?
2. **Submission B, conductor algebra.** Stability, reduction, tangent cone,
   Buchsbaumness, Noether normalization, special fiber, and defining ideal.
   Central question: what algebraic structure does the conductor family carry?
3. **Submission C, homological anatomy.** Betti rows, cubic-colon idealization,
   mapping cone, and characteristic-dependent lower cells. Central question:
   which parts of the graded resolution admit uniform integral normal forms?

These are submission restructurings, not new results. They are instantiated as
new manuscript directories only after a dependency and overlap audit produces
three self-contained papers. The published consolidated paper is never edited
or withdrawn. The initial dependency and overlap audit is
[`submission-split-audit-2026-09-20.md`](../../manuscripts/huneke-wiegand/frobenius-minimality/submission-split-audit-2026-09-20.md);
candidate A is closest to submission readiness, candidate B needs a dedicated
fiber-cone literature comparison, and candidate C remains significance-gated.

### Focused companion: Curvilinear fiber cones

- Current public version: v0.04.
- Version DOI: `10.5281/zenodo.22835118`.
- Concept DOI: `10.5281/zenodo.21997377`.
- Coverage: EXP-025--026, importing only the required special-fiber premises.
- Decision: coherent and complete; no split.

### Focused companion: Integral connecting annihilators

- Current public version: v0.04.
- Version DOI: `10.5281/zenodo.22859408`.
- Concept DOI: `10.5281/zenodo.22342975`.
- Coverage: EXP-054--066, with the main theorem owned by EXP-060--062 and the
  projected endpoint strengthening owned by EXP-065--066.
- Decision: coherent but gated. No new version for further finite carrier data.
  The next trigger is a canonical comparison, a complete kernel or quotient, or
  a reusable general matching theorem. The exact v0.04 boundary is recorded in
  its [claim audit](../../manuscripts/huneke-wiegand/integral-connecting-annihilators/claim-audit-v0.04.md).

## Current research routing

The Kunz preflight corrected a category error: because the family multiplicity
is `24p`, its members lie in different Kunz cones. Small exact cases lie on
one-dimensional faces, but the stronger invariant is the simple gluing
`m*N+q*Gamma`. Focus `HW-F6` is therefore redirected, not silently abandoned.

The active focus is `HW-F7`, the general transfer of the two-generated rigidity
identity through that simple gluing. EXP-067 is declared and frozen. A focused
gluing-transfer manuscript is created only if the symbolic exponent-set lemma,
independent exact validation, adverse controls, and two-parameter corollary all
pass. Standard gluing itself is not claimed as new.

The prior endpoint/cokernel route is `HW-F5` and is gated. It may resume only
with a theorem preflight aimed at a canonical comparison plus a complete kernel
or upper bound. Another bounded carrier table is a stop condition.
