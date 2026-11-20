# Central configurations: result and manuscript map

Updated 2026-11-19. This map separates mathematical evidence, strategic value, manuscript coverage and external novelty
(methodology 13). Experiment verdicts remain the authority for every finite result. The programme is on hold (portfolio
reviews of 2026-10-30 and 2026-11-19).

## Status boundary

Smale's sixth problem is open. The planar five-body case is settled outside this programme: finiteness for every positive
mass vector is claimed by Tomar (arXiv:2610.13100, with a Lean 4 formalization and certificates at Zenodo
10.5281/zenodo.23202861), by Chen and Tong (arXiv:2610.16107) and by Liu and Liu (arXiv:2610.28168); none is refereed. The
n = 4 finiteness is Hampton and Moeckel's (2006) and, without a computer, Albouy and Kaloshin's (2012); the n = 5
exceptional mass subvariety is Albouy and Kaloshin's; the tropical n = 5 certificate that EXP-003 reproduces is Jensen and
Leykin's (arXiv:2301.02305); the 24 residual six-body diagrams are Chang and Chen's; the Lean proof audited in EXP-024 is
Tomar's. The case n = 6 and every n >= 7 are open and nothing in this programme settles them.

The CAOS contributions are: the exact instruments and their calibration (the dimension-blindness of the bare
Albouy-Chenciner system, the enrichment law, the eliminant census, the exact per-comet pointedness decision); exact
replications of published certificates, labelled as replications; measured limits of routes (the direct n = 4 census, the
n = 5 Dziobek dimension, the Groebner loci bounds, the n = 6 tooling barrier); the status of a six-body symmetric stratum
as the records support it (the quadruple corner is not closed); and the audit of the statement of Tomar's Lean theorem.

Internal exact validation and Zenodo persistence do not establish peer review or worldwide novelty. Nothing here has been
expert reviewed or refereed. The literature refresh of 2026-11-19 found, for this problem, Liu-Liu arXiv:2610.32751, a
Tomar Zenodo companion and a newer Nagy working paper, with no rebuild or critique of the five-body claims (portfolio
review of 2026-11-19, section 1). Every claim of another author recorded here is theirs and, except where a row below says
otherwise, not re-checked by CAOS.

## Result blocks

| block | experiments | result status | value | manuscript home |
|---|---|---|---|---|
| Calibration of the exact Albouy-Chenciner builder on n = 3 and the n = 4 planar system; the bare symmetric system is dimension-blind (tetrahedron and square coexist); enrichment makes the system zero-dimensional and the decided censuses classical | EXP-001, EXP-002 | confirmed in part (EXP-001: P7 uniqueness refuted, unequal-mass saturation and full census inconclusive at caps); confirmed on every decided prediction (EXP-002) | instrument | `tropical-replication` |
| Exact reproduction of the Jensen-Leykin n = 5 prevariety certificate (both f-vectors digit for digit), the valuation and equation screening with two new working families, the exact per-comet decision of all 16 cells | EXP-003, EXP-004, EXP-007 | confirmed, exact; a replication of an external certificate plus screening and decision content | opened the tropical lane on validated infrastructure | `tropical-replication` v0.13 |
| Equation enrichment in the prevariety: Dziobek is tropically active but does not rescue the hard equal-valuation case; the comet count is the monotone invariant | EXP-008 | P1 and P2 refuted, P3 confirmed | negative result with an invariant | `tropical-replication` v0.13 |
| Cross-engine censuses (msolve against sympy) on n = 3; the n = 4 affine system has dimension 1 | EXP-006 | P1 and P2 confirmed, P3 refuted as posed | instrument | `tropical-replication` v0.13 |
| Direct n = 4 torus census and Dziobek dimension probes, the partial-Groebner engine spike, the n = 5 products ideal (dimension 5 exact), the incremental cut | EXP-009 to EXP-014 | inconclusive at caps (EXP-009, EXP-011, EXP-014), confirmed at bounds (EXP-010, EXP-012 dim <= 7, EXP-013 products dimension 5, cut <= 5; 5 versus 4 undecided) | measured limits of routes | research record, reported in `tropical-replication` |
| n = 6 tropical prevariety (gfan 0.7 and 0.8beta) | EXP-005 | no verdict; both gfan 0.7 modes abort, the 0.8beta runs were killed and parked | measured infrastructure barrier | none (research record, no verdict.md) |
| Six-body symmetric stratum: shape dimension 5 ungauged and 4 gauged, generic rank 4, hexagon verified as a stratum central configuration with rank 3 at its symmetry | EXP-015, EXP-016, EXP-018 | confirmed | stage results of the stratum chain | research record, reported in `tropical-replication` |
| Loci bounds and single-minor cuts by Groebner bases | EXP-017, EXP-017b, EXP-017c, EXP-019 | all inconclusive at caps; the Groebner route is closed at the budgets tried | measured limit | research record |
| Free-atom chamber relaxation for k = 3 | EXP-020 | does not close k = 3 (125,097,984 residual assignments over 24 chambers) | negative result | research record |
| Verified interval covering of the core, collar coverings and the atlas; the (0,3) stratum | EXP-021, EXP-022, EXP-023 | EXP-021 declared success on the core; EXP-022 atlas verdict (CCB-042): m2w sound, the quadruple corner NOT closed, several charts are budget stops with unprocessed stacks; EXP-023 findings only | the atlas is incomplete; no stratum theorem | research record, status stated in `tropical-replication` v0.13 |
| Audit of the Lean statement of Tomar's five-body theorem; kernel-bypass scan of 2,751 source files and 85,756 generated modules | EXP-024 | confirmed: statement faithful, no bypass; the rebuild was not done | statement-level check of an external claim | `tropical-replication` v0.11 onward |

## Manuscripts

| slug | version | version DOI | concept DOI | central question |
|---|---|---|---|---|
| `tropical-replication` | v0.13 | [10.5281/zenodo.24232708](https://doi.org/10.5281/zenodo.24232708) | [10.5281/zenodo.21542483](https://doi.org/10.5281/zenodo.21542483) | can the tropical finiteness certificates for central configurations be replicated and screened exactly, and what is the status of a six-body symmetric stratum |

Split decision: none recorded. The paper carries three questions (tropical screening and exact comet decisions, the stratum
status, the five-body claims audit); the next version review decides whether they split. No manuscript exists for a
proposed method of this programme.

## Focus record

- Closed: CC-F0, calibration of the exact instruments (EXP-001, EXP-002); CC-F1, replication of the n = 4 and n = 5
  certificates and the limits of direct solving (EXP-003, EXP-004, EXP-006 to EXP-014); CC-F3, audit of the external
  five-body claims (EXP-024).
- Closed with the gate not met: CC-F2, the six-body symmetric stratum chain and atlas (EXP-015 to EXP-023; the quadruple
  corner is open; the atlas was retired as a route to the n = 5 theorem at the review of 2026-11-02).
- Current: **CC-F4**, the replication paper at its published version with the corrected atlas status (success gate met
  2026-11-14 by tropical-replication v0.13, 10.5281/zenodo.24232708; CCB-042, CCB-044).
- Proposed: CC-F5, n = 6 generic-mass finiteness by the tropical route (CCB-041); CC-F6, independent replay of the Tomar
  certificates and Lean proof (CCB-040, done in part).

## Open obligations

- CCB-041: n = 6 needs a fresh hypothesis and a budget before any run, or a recorded stop with the measured cost.
- CCB-040: whether the rebuild of Tomar's formalization (about 863 CPU-hours reported by its author) is run is not decided.
- CCB-043: the informative attack on the pair-equality statement (ten equations in ten unknowns) is not tested; the paper
  states the gap.
- The quadruple corner of the six-body stratum atlas is not closed (CCB-042 verdict); the unprocessed shares of the
  budget-stopped charts are stated in the paper.
- The five-body claims of Tomar, Chen and Tong and Liu and Liu are unrefereed; the paper states them as claimed.
