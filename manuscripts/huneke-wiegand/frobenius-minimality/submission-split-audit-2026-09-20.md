# Submission split audit

Date: 2026-09-20. Source record: published consolidated manuscript v0.25,
version DOI `10.5281/zenodo.22835108`.

## Decision

The 53-page source record contains three coherent research narratives with
different central questions, proof toolkits, and likely audiences. A focused
submission split is warranted. A second Zenodo publication is not yet
warranted: rearranging already published text is not a new mathematical result,
and each candidate paper still needs a self-contained dependency and overlap
pass.

The v0.25 source and PDF remain immutable. Future submission files will cite
that record, identify reused results explicitly, and avoid presenting a split
as a new discovery.

## Candidate A: counterexample classification and families

Central question: how isolated is the public numerical-semigroup
counterexample?

Owned results:

- complete certified frontier below Frobenius value 181;
- least Frobenius value 181 and minimum-layer uniqueness;
- the explicit infinite family;
- its endomorphism, type, trace, conductor, and Ext/Tor escape mechanism.

Primary evidence: EXP-001--013, with EXP-003 and EXP-006 retained as
calibration rather than theorem ownership.

Imported dependencies: Pham's public counterexample and exact certificate;
standard numerical-semigroup and canonical-ideal criteria.

Readiness gate: update the primary-source overlap search, isolate the exact
minimality and uniqueness certificate interface, and obtain specialist review
of the family-level priority claim. This is the highest-priority submission.

## Candidate B: conductor and special-fiber algebra

Central question: what uniform local and graded algebra is carried by the
conductor family?

Owned results:

- conductor stability, corrected defect, and reduction number;
- tangent cone, Buchsbaum, and Noether-normalization structure;
- special-fiber presentation and one-cubic defining ideal;
- the coherent Betti consequences needed by those defining equations.

Primary evidence: EXP-013--024. EXP-015's failed formula remains a negative
control and EXP-016 owns the correction.

Imported dependencies: only the family and conductor formula from candidate A.
The paper must restate those premises without importing the full
counterexample narrative.

Readiness gate: prove that every displayed homological claim is needed for the
conductor-algebra story, or move it to candidate C; then run a dedicated
literature comparison for fiber cones of numerical-semigroup ideals.

## Candidate C: integral and characteristic-dependent homological anatomy

Central question: which strands of the graded resolution admit uniform exact
descriptions, and where does characteristic dependence enter?

Owned results:

- relative and complete second Betti rows;
- colon/Koszul diagonal and cubic-colon idealization;
- complete colon resolution and minimal cubic mapping cone;
- two-layer kernels, survival, and finite characteristic-dependent cells.

Primary evidence: EXP-027--037. EXP-037 is retained only to state the boundary
between theorem and unsupported recurrence.

Imported dependencies: the special-fiber presentation from candidate B and
the family definition from candidate A.

Readiness gate: obtain an external significance review and choose one complete
strand as the organizing theorem. If the story remains a list of Betti entries,
do not instantiate this paper.

## Cross-paper controls

1. Candidate A owns the family definition and direct Huneke-Wiegand relevance.
2. Candidate B owns conductor, tangent-cone, and special-fiber structure.
3. Candidate C owns resolution and characteristic-dependence results.
4. The already published curvilinear paper owns EXP-025--026; focused
   submissions may cite but not absorb its complete theorem.
5. The integral connecting-annihilator paper owns EXP-054--066 and is not part
   of this split.
6. Shared premises are restated with explicit citations and are not counted as
   new results in more than one paper.

No new manuscript directory, version number, DOI, or experiment is authorized
by this audit alone.
