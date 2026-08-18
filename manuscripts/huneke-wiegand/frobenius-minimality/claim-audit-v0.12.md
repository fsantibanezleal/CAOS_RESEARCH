# Claim audit - manuscript v0.12

Audited: 2026-08-18. Final publication result: PASS.

Version 0.12 retains all v0.11 claims and adds only the defining-ideal results closed by EXP-022
and EXP-023. The quadratic conjecture remains visibly refuted. The all-parameter presentation
theorem is labeled machine-verified because its exact Presburger UNSAT leaves do not have a
separately checked proof object.

| manuscript claim | evidence | audit result |
|---|---|---|
| prior minimality, uniqueness, family, endomorphism, type, trace, stability, reduction, tangent-cone, Buchsbaum, Noether-normalization, and special-fiber results | claim audits v0.05--v0.11; EXP-001--021 | PASS; scope and attribution unchanged |
| value-congruence description of the special-fiber kernel | EXP-022 semantic proof; monomial linear independence in the semigroup ring | PASS; zero monomials and equal-offset binomials exhaust each homogeneous kernel |
| exact quadratic count `50p^2-17p` | `10p` degree-one variables and `dim(F_p)_2=22p` from EXP-021 | PASS; no linear equation, so every quadratic kernel vector is minimal |
| necessary cubic `X_0^2X_(3p)-X_p^3` | EXP-022 pair-sum isolation proof | PASS; equal nonzero total and no quadratic move from either monomial for any `p>=4` |
| state-graph component defect equals the number of new degree-`d` equations | EXP-023 proof and two independent graph implementations | PASS; the states present variable multiples of the complete preceding kernel, including zero components |
| exactly one cubic and no quartic or quintic equation | EXP-023 exact Presburger component cover | PASS with disclosed solver boundary; all 133 terminal negated queries UNSAT, no SAT or unresolved leaf |
| no equation above degree five | EXP-017 reduction number four; EXP-021 Cohen--Macaulayness; Abdolmaleki--Kumashiro Theorem 2.8 | PASS; source hypotheses checked and the general theorem used only as a degree bound |
| full presentation, Betti row, relation type, and equation count | preceding four rows | PASS; `((a_p)_2,f_p)`, Betti row `(50p^2-17p,1,0,0,...)`, relation type three, and `mu=50p^2-17p+1` |
| non-Koszul special fiber | necessary minimal cubic | PASS; a standard graded Koszul algebra has a quadratic defining ideal |
| bounded computational support | EXP-023 `results.json` and `audit.json` | PASS; campaign `p=4,...,23`, all 20 rows rehashed, and `p=4,13,23` independently rebuilt |
| preserved first budget attempt | EXP-023 `attempt-1-budget-checkpoint.json` | PASS; recorded as `INCONCLUSIVE_BUDGET`, not mathematical failure |
| source identity | Abdolmaleki--Kumashiro, IJAC 34(7) (2024), 1099--1109, DOI `10.1142/S0218196724500437` | PASS; journal metadata and Theorem 2.8 checked against the primary source |
| solver trust boundary | EXP-023 verdict, proof, symbolic artifact, and manuscript trust section | PASS; no claim of proof-carrying or proof-assistant verification |
| authorship | title page and `zenodo.json` | PASS; Felipe Santibanez-Leal is sole author; no automated system named |
| publication identity before upload | reserved Zenodo draft and page-one block | PASS; version `0.12`, reserved DOI `10.5281/zenodo.21988601`, concept DOI, date, licence, and sole author/ORCID agreed before upload |
| public record and immutable file | Zenodo record `21988601` plus fresh unauthenticated download | PASS; concept-latest, version, DOI, sole author/ORCID, CC-BY-4.0, filename, 615,252 bytes, MD5, and SHA-256 agree with Git exactly |

## Scope boundaries

- EXP-023 concerns only the conductor special fibers in the explicit EXP-009 family.
- It does not classify arbitrary conductor ideals, fiber cones, numerical semigroup rings, or
  modules over arbitrary one-dimensional Gorenstein domains.
- The theorem determines only the minimal defining equations. It does not determine the higher
  syzygies, the full resolution over the presentation ring, or a Groebner basis.
- The all-parameter result relies on exact Z3 UNSAT answers without separately checked proof
  objects. The independent graph implementation and finite campaign lower implementation risk but
  do not remove solver soundness from the trusted base.
- The broad Huneke--Wiegand conjecture was already disproved by the public seed; discovery priority
  remains Son Pham's.

## Build and rendered-document gate

- final warning-free MiKTeX `pdflatex` passes: PASS;
- stable-pass log audit: PASS; zero warnings, undefined references, overfull boxes, or underfull
  boxes;
- complete 27-page render at 150 DPI: PASS; every page was inspected in five contact sheets, with
  full-resolution checks of the title/DOI block, the special-fiber theorem, the complete new
  defining-ideal theorem and proof, the trust-boundary table, scope/open questions, and references;
- visual defects: none; formulas, long hashes, tables, citations, headers, footers, and page numbers
  are legible with no clipping or overlap;
- frozen candidate PDF: 615,252 bytes, MD5 `c8b810a763b9bb55d076a454df49b413`, SHA-256
  `98d730fb8afaf40149d028bdde0b1c3ba9851f1dbcd15475567e56bb7eb17d3f`;
- public-record gate: PASS; the fresh public file is byte-identical to the committed PDF, MD5
  `c8b810a763b9bb55d076a454df49b413`, SHA-256
  `98d730fb8afaf40149d028bdde0b1c3ba9851f1dbcd15475567e56bb7eb17d3f`.
