# Unsplittable-flow cost conjecture: result and manuscript map

Updated 2026-11-19. This map separates mathematical evidence, strategic value, manuscript coverage and external novelty
(methodology 13). Experiment verdicts remain the authority for every finite result.

## Status boundary

Goemans' cost-preserving unsplittable-flow conjecture (Conjecture 1.2 of STVZ25) is already false. The counterexample is
Rybin's seven-vertex planar instance, announced on 2026-07-22/23 outside peer review (and formalized in Isabelle/HOL as an
AFP entry); it is not ours. The current lower bounds on the frontier constant are not ours either: S. Nikolenko's three
Zenodo preprints (2026-07-30 to 2026-08-13) and repository give the general bound 1.2824948, refined by A. De la Fuente to
1.28260069 (merged 2026-08-04), the planar family (299 - 41 sqrt 41)/32 (credited jointly to M. Protti, release of 2026-07-23, in Nikolenko's third
preprint), and the planar record 1.17353531974518; the bound 9/8 and its status as the supremum of the symmetric
three-terminal family are Muffatti's (note dated 2026-07-24) and, independently, Nikolenko's (2026-07-30, Proposition 5.2). Conjecture 1.3 is false by Berczi, Liu, Reis and Tarnawski (arXiv:2608.13983,
Theorem 17).

The CAOS contributions are: the independent exact verification of the 2026 counterexample and what it forces (alpha_inst =
16/15 on that instance); the exact instruments (the separation LP, the frontier value, the single-terminal theorem); the
exact checks of published families (the Muffatti family, Afrasyab's odd-cycle family on C5); and, once EXP-007 closes, the
independent exact re-verification of the current record instances, credited to their authors.

Internal exact validation and Zenodo persistence do not establish peer review or worldwide novelty. The literature
refreshes of 2026-11-07 and 2026-11-19 (`problems/optimization-geometry/unsplittable-flow-cost/context/`) did not find the
CAOS results below elsewhere; specialist confirmation is still required. Every claim of another author recorded here is
theirs and, except where a row below says otherwise, not re-checked by CAOS.

## Result blocks

| block | experiments | result status | value | manuscript home |
|---|---|---|---|---|
| Exact instance checker `ufclib`, validated on hand-built cases | EXP-001 | confirmed; 14 pytest tests; adopted as ground truth | instrument | `counterexample-verification` (method) |
| Independent verification of the 2026 counterexample: Conjecture 1.2 false on it, alpha_inst = 16/15, C1-C9 battery, K4 class boundary, planar constant pinched between 1 and 2 | EXP-002 | confirmed (a replication of an external claim, plus the quantitative and structural content); Morell-Skutella Conjecture 1.4 falls with it (acyclicity checked) | trusted baseline and what the instance forces | `counterexample-verification` v0.03 |
| Separation LP: optimum 2/7 on the 2026 instance, attained by the published prices; single-terminal theorem; the two-terminal case open | EXP-003 | confirmed; the k <= 2 claim of round 1 retracted in writing | instrument, minimality rung 1 | `counterexample-verification` v0.03 |
| Frontier value: 16/15 on the 2026 instance; it is the only counterexample over 3456 parameter points of its family | EXP-004 | instruments confirmed, F4 refuted (null result) | the published prices are optimal; extremal, not typical | `counterexample-verification`, next version (UFB-066) |
| Muffatti planar family forces 9/8 - (3/4) eps exactly, with his pricing optimal | EXP-005 | confirmed as an exact check of the family; the bound 9/8 is Nikolenko's and is superseded by his records | none beyond the check | research record |
| Afrasyab's odd-cycle family on C5: frontier value at most 1 on the sampled space (largest 42/43), uniform pricing optimal with frontier 2/3 - eps | EXP-006 | confirmed on the sampled space; whether the supremum is 1 is open (UFB-067) | exact check, negative on the route to 9/8 | research record |
| Independent exact re-verification of the record instances (values, planarity with certificates, optimality of pricing) | EXP-007 | no verdict: hypothesis frozen (4f51d68b), run in progress; no disposition until it closes | verification attributable as such | `counterexample-verification`, next version (UFB-066, UFB-068) |

## Manuscripts

| slug | version | version DOI | concept DOI | central question |
|---|---|---|---|---|
| `counterexample-verification` | v0.03 | [10.5281/zenodo.22835200](https://doi.org/10.5281/zenodo.22835200) | [10.5281/zenodo.21554258](https://doi.org/10.5281/zenodo.21554258) | does the 2026 counterexample to Goemans' conjecture verify under an independent exact checker, and what does it force |

Split decision (2026-11-19): one manuscript. The next version carries the stale-statement corrections (the current lower
bounds with their authors, the credit of 9/8, Conjecture 1.3 false), the frontier value of EXP-004 and the verification of
EXP-007; a separate paper only if lower-bound or minimality results become a central question of their own.

## Focus record

- Closed: UF-F0, independent exact verification of the 2026 counterexample (EXP-001, EXP-002); UF-F1, the separation LP and
  the frontier value as instruments (EXP-003, EXP-004).
- Closed as superseded on 2026-11-19: UF-F2, lower bounds from the Muffatti and odd-cycle families (EXP-005, EXP-006;
  backlog UFB-070). Nikolenko's series holds the bounds; EXP-005 stays an exact check of the family.
- Current: **UF-F3**, independent exact re-verification of the current record instances of Nikolenko and De la Fuente, their
  planarity with certificates and the optimality of their pricing (EXP-007, hypothesis frozen 4f51d68b; portfolio review of
  2026-11-19, decision 3).
- Proposed: UF-F4, Open Problem 11.1 of Nikolenko's Part III (is the factor-two merger constant finite; UFB-069).
- Dormant: UF-F5, the smallest counterexample (two terminals open; canonical forms and minimality, UFB-011, UFB-012,
  UFB-034).

## Open obligations

- UFB-066: the next version of `counterexample-verification` states the current lower bounds with their authors, credits
  9/8 to Nikolenko with the Muffatti family as its limit point, keeps alpha_inst = 16/15, records that Conjecture 1.3 is
  false, and carries the verification of UFB-068 as new content.
- UFB-068: EXP-007 closes (verdict pending), then its results enter the revision.
- UFB-064: SSRN 7423078 unread (HTTP 403).
- UFB-067: the supremum of the odd-cycle family on C5 (research record).
