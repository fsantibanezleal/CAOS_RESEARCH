# Claim audit - curvilinear conductor fiber cones v0.05 (draft source)

Audit date: 2026-11-14. Status: draft of the revision of v0.04 under the independent audit
`wip/caos-research/msaudit-hw-other-2026-11-10.md` (section D1, plan items 1 to 9), with the
second-solver experiment EXP-069 (CONFIRMED 2026-11-14). The PDF, the version DOI and the Zenodo
release are not part of this draft; a reader other than the writer reviews before release.

Marks: [D] derived by a written argument; [MV] machine-verified; "[D] conditional on [MV] input" a
derived statement whose proof uses a machine-verified premise of Proposition 3.1.

## Imported input (Proposition 3.1)

Pointers are to the consolidated paper `frobenius-minimality`, current text (PDF version 0.25,
DOI 10.5281/zenodo.22835108, concept 10.5281/zenodo.21763582). Theorem numbers were read from the
`.aux` of a clean build of that source (`\newlabel` entries) and confirmed in the text extraction.

| item | statement | mark | pointer | experiment |
|---|---|---|---|---|
| I1 | presentation, `G_p`, `E_n` | [D] | Theorem 15.4 and proof; equations (5) and (6) of the subsection "The defining ideal of the special fiber"; Theorems 12.1 and 13.1 | EXP-021 |
| I2 | value congruence | [MV] | proof of Theorem 15.5 | EXP-023 (133 UNSAT formulas, no checked proof object) |
| I3 | `E_n` equals the truncated n-fold sumset | [MV] | Theorem 15.4 power calculation; `analyze_parameter` of EXP-025 `run.py` and EXP-026 `run.py` (degrees up to 5 and 6, all `p=4..300`) | EXP-025, EXP-026 |
| I4 | CM, free of rank `q`, type `10p+1`, socle in two degrees | [D] | Theorem 15.4; Theorem 15.6 (`beta_(c,c+2)=10p`, `beta_(c,c+4)=1`) | EXP-021, EXP-024 |
| I5 | relation type three | [MV] | Theorem 15.5 | EXP-023 |

Remark 3.2 (sumset identity) derives `n=3` and `n>=4` from the shape of `E_2` by interval
arithmetic. This derivation is the writer's own (audit finding 6 only reports a hand check); it is
not in a record and needs the reviewer's check. The case `n=2` stays [MV] for `p<=300`.

## Results

| statement | mark | evidence |
|---|---|---|
| Theorem 4.1 truncated parametrization | [D] conditional on [MV] input | I2, I3, I4; EXP-025 `proof.md` section 1 |
| Corollary 4.2 dehomogenization | [D] conditional | I4 freeness; EXP-025 `proof.md` section 2 |
| Theorem 4.3 primary decomposition, nilindex `24p` | [D] conditional | CM no embedded primes; EXP-025 `proof.md` section 3 |
| Theorem 4.5 curvilinear fat point, local vs arithmetic Gorenstein | [D] conditional | EXP-025 `proof.md` section 4 |
| Proposition 4.7 differentials, characteristic split | [D] conditional | EXP-025 `proof.md` section 5 |
| Lemma 5.1 canonical staircase | [D] conditional | EXP-026 `proof.md` section 1 |
| Lemma 5.2 adding `X_0` (new) | [D] conditional | written proof in the paper; supports the degree-five argument and the layer count |
| Theorem 5.3(a) quadratic count and split | [D] conditional | EXP-026 `proof.md` section 2; all 297 rows (`quadratic_profile`) |
| Theorem 5.3(b) cubic and quartic leading monomials | [MV] | 16 obligations (EXP-026 `symbolic-certificate.json`, Z3 4.16.0) and EXP-069 (cvc5 1.4.2, same query digests); clique audit at 7 parameters |
| Theorem 5.3(c) reduced tails | [MV] | twelve tail obligations; Table 11 |
| Theorem 5.3(d) no element of degree at least five | [D] conditional | new argument (audit finding 5, plan item 8): dichotomy on `X_0`, Lemma 5.2, parity of `6p-1`; replaces the argument of EXP-026 `proof.md` section 4, which did not treat offset at least `q` |
| Theorem 5.3(e) no leading monomial contains `X_0` | [MV] | obligations; quadratics: `(0,a)` is the smallest pair |
| Corollary 5.4 flat CM degeneration, Hilbert function `(1,10p-1,12p,2p-1,1)` | [MV] | Theorem 5.3(e), I5, Lemma 5.2 |

No statement carries [D] alone while resting on a solver answer: the solver-based statements are
Theorem 5.3(b), (c), (e) and Corollary 5.4, all marked [MV].

## What EXP-069 established (EXP-069 `verdict.md`, `artifacts/results.json`)

16 of 16 rebuilt query digests equal the stored ones; cvc5 1.4.2 (LIA, 600 s per leaf) returns `unsat`
on 16 of 16 (13.98 s in all, slowest `quartic-completeness` 10.95 s); Z3 4.16.0 returns `unsat` on the
16 exported texts (33.94 s); four perturbed controls are `sat` for both solvers with a cvc5 model that an
exact evaluator accepts on the perturbed formula and rejects on the original. The class stays [MV]: no
proof object is checked and both solvers are premises, so the theorem is not [D]. The paper states
exactly this and does not call the result proved by a checked certificate.

## Plan items and findings of the audit

| item | where addressed |
|---|---|
| 1 marks, abstract sentence | abstract, Section 1, marks on every result, Table 7 (`tab:marks`) |
| 2 appendix of the 16 obligations, EXP-069 | Appendix A (formulas `gen`, `valid`, `standard`, `minbd`, `cub`, `qua`, Table 11), Appendix B, Sections 6 (Algorithm 5), 7, 8.3, 9, 11 |
| 3 Proposition 2.1 pointers, `isDerivedFrom` | Proposition 3.1; `zenodo.json` `isDerivedFrom` set to 10.5281/zenodo.22835108 |
| 4 Section 9 rewritten | Section 10 (Discussion), Table 9 (`tab:betti`), questions Q1 and Q2 |
| 5 algorithms and implementation | Section 6, Algorithms 1 to 5, costs in `p`, commands in Section 12, full hashes in Tables 1, 3, 10 (`tab:premises`, `tab:aggregates`, `tab:manifest`) |
| 6 results table, capped first attempt | Table 2, Table 4 (row hashes), Section 8.2 |
| 7 EXP-026 controls | Table 8 (`tab:controls026`) and the limits of the controls |
| 8 degree five and later | Theorem 5.3(d) and its proof |
| 9 related work, conjecture stated | Section 2; HW conjecture stated in Section 1 with `HunekeWiegand1994` cited |
| finding 6 (sumset identity not stated) | I3 and Remark 3.2 |
| finding 8 (title) | singular "Degeneration" |

Hardened by this revision (not in the plan): the Huneke-Wiegand 1994 DOI was corrected to
10.1007/BF01459794 after Crossref returned the title "Tensor products of modules and the rigidity of
Tor" for it (the previous DOI, 10.1007/BF01459793, resolves to a different paper, "Higher integrability
of the gradient in linear elasticity", pages 435-448).

## Sources of every table, figure and algorithm

All generated by `gen_artifacts.py` from committed artifacts; no mathematics is computed there.

| item | source |
|---|---|
| Figure 1 strips `p=4` | closed formulas of I1; sizes asserted against EXP-026 `results.json` row `p=4` |
| Figure 2 pipeline | hand drawn from the dependence of EXP-025, EXP-026, EXP-069 |
| Figure 3 profile; Figure 4 split; Figure 5 layers | EXP-026 `results.json`, rows `p=4,5,6,17,73,151,300` |
| Figure 6 solver times | EXP-026 `symbolic-certificate.json` `leaves[*].elapsed_seconds`; EXP-069 `results.json` `leaves[*].z3.seconds`, `leaves[*].cvc5.seconds` |
| Table 1 premises | EXP-026 `results.json` `premise_hashes` |
| Table 2 results | EXP-026 `results.json` rows |
| Table 3 aggregates | EXP-025 `results.json` and `audit.json`; EXP-026 `results.json`, `audit.json`, `symbolic-certificate.json` |
| Table 4 row hashes | EXP-026 `results.json` `rows[*].row_hash` |
| Table 5 obligations | EXP-026 `symbolic-certificate.json`; EXP-069 `results.json` |
| Table 6 controls of EXP-069 | EXP-069 `results.json` `controls` |
| Table 7 marks | this audit |
| Table 8 controls of EXP-026 | EXP-026 `run.py` `analyze_parameter`, `controls` |
| Table 9 Betti entries | EXP-024, EXP-027 to EXP-035 `verdict.md`; theorem numbers from the `.aux` of the consolidated paper |
| Table 10 manifest | SHA-256 and sizes of the five artifact files, computed from the files by `gen_artifacts.py` |
| Table 11 tails | EXP-026 `symbolic_certificate.py` `cases` and `run.py` `cubic_relations`, `quartic_relations` |
| Algorithm 1 | EXP-025 and EXP-026 `run.py` `analyze_parameter` |
| Algorithm 2 | EXP-025 `audit.py` `disjoint_layers`, `reconstruct` |
| Algorithm 3 | EXP-026 `run.py` `Staircase`, `is_standard_from_boundary`, `validate_relation` |
| Algorithm 4 | EXP-026 `audit.py` `reconstruct` |
| Algorithm 5 | EXP-069 `run.py` driver and `second_solver.py` |

Complexity statements in Section 6 are derived from the structure of the scripts, not measured.

## Discrepancies and items not confirmed (UNVERIFIED)

- EXP-026 `verdict.md` gives 0.598 s for the clique recomputation; the committed `audit.json` records
  0.819 s. The paper quotes the artifact (0.819 s).
- Python version and hardware of the original runs are not recorded in any artifact; the paper says so.
- References for Z3 and cvc5 are not in any record; the paper names the solvers and versions without
  a bibliography entry.
- The primary text of Huneke and Wiegand (1994) was not opened; the conjecture is stated as in the
  introduction of the consolidated paper, and the DOI was confirmed on Crossref only (title, authors,
  journal, pages).
- The characterizations of arXiv:1711.08775, 1904.04988, 2302.11903, 2609.07615 and 2608.21666 follow
  the arXiv abstract pages read on 2026-11-14 (title, authors and abstract); the full texts were not read.
  The preflight record for 1711.08775, 1904.04988 and 2302.11903 (archived PDFs) is not on this device.
- References from the consolidated paper (Garcia-Sanchez and Leamer, Landeros et al., Dey, Dey and Lyle,
  Herzog and Kumashiro, Lindo et al., Maitra and Mukundan, Blanco and Rosales, Valabrega and Valla,
  D'Anna et al., Cortadellas and Zarzuela, Abdolmaleki and Kumashiro, Northcott and Rees, Bruns and
  Herzog, Stamate) are described only as that paper describes them; none was re-opened.
- Lemma 5.2 and Remark 3.2 are new derivations by the writer; both need independent review.
