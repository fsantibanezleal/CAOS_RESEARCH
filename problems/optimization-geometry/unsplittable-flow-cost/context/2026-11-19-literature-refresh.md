# Literature refresh, 2026-11-19

Transcribed from the external refresh of the CAOS research portfolio on 2026-11-19 (the full report, with every search,
is kept in the private management mirror, `wip/caos-research/external-refresh-2026-11-19.md`, section D1.8 and items 2
to 5 of D2.1). Window: items after the 2026-11-07 refresh, plus version checks. Marks: [V] read on the primary page;
[V2] secondary. Every claim below is its author's; CAOS has not re-checked it (UFB-068).

| ID | Citation | Date | Claim | Mark | Overlap with CAOS records |
|---|---|---|---|---|---|
| N1 | S. Nikolenko, Deletion-Star Ceilings and a 1.28249 Lower Bound for Cost-Preserving Single-Source Unsplittable Flows, Zenodo [10.5281/zenodo.21716713](https://doi.org/10.5281/zenodo.21716713) | 2026-07-31 | C >= 1282494797984843521/10^18 = 1.2824948 from a 17-terminal common-point interval instance; refined by A. De la Fuente to 160325086265636045340018727271/125000000000000000000000000000 = 1.28260069 (repository PR #1, merged 2026-08-04) | [V] | Supersedes alpha* >= 9/8 (EXP-005). Same normalization as alpha* |
| N2 | S. Nikolenko, A Planar Lower Bound 1.1397... > 9/8, Zenodo [10.5281/zenodo.21701162](https://doi.org/10.5281/zenodo.21701162) | 2026-07-30 | Theorem 4.7: planar C >= (299 - 41 sqrt 41)/32 = 1.139747 from a four-terminal family; Proposition 5.2: 9/8 is the exact supremum of the symmetric three-terminal (triangle) template only | [V] | The template's limit point is the Muffatti family of EXP-005, so the 9/8 value precedes Muffatti's commit (2026-08-31) by a month; the planar part of EXP-005 is superseded |
| N3 | S. Nikolenko, Exact-Mean Decompositions for Cost-Preserving Single-Source Unsplittable Flows (Part III), Zenodo [10.5281/zenodo.21922203](https://doi.org/10.5281/zenodo.21922203) | 2026-08-13 | Mixture characterization; exact-two-path instances are totally unimodular; planar C >= 1.17353531974518; exact means E(3) = 9/8, E(4) = 1.1397; Open Problem 11.1 (is the factor-two merger constant K finite? K >= 2.5652 is a lower bound only) | [V] | "Series-parallel <= 1" is a corollary of Almoghrabi-Skutella-Warode arXiv:2412.05182, not new (skeptic correction). Two-valued instances have C <= 1 + d/D < 2 |
| N4 | Repository [snikolenko/unsplittable-flows](https://github.com/snikolenko/unsplittable-flows), HEAD a8324b3 (2026-08-13) | 2026-08-13 | Every numerical claim "certified in exact rational ... or symbolic ... arithmetic"; verify/ holds 18 Python verifiers; VERIFICATION.md covers Papers I and II with seven and five corrections; Paper III ships 37 certificate files and no verifier | [V] | AI-assisted, self-corrected, no external reviewer named: an independent check is attributable (UFB-068) |
| N5 | Debgupta, Morell, Skutella, Unsplittable Transshipments, ICALP 2026, arXiv:2602.07230 | 2026-02 | (snippet) | [V2] | Context |
| N6 | Single-source unsplittable flows in planar and bounded-genus graphs, Math. Programming, DOI 10.1007/s10107-026-02365-x | 2026 | (snippet) planar two-sided guarantees | [V2] | Journal version of the planar upper bound 2 |

A skeptic re-ran the author-side verifier `verify/k17_refined.py` for N1 (it printed SSUFP_EXACT_VERIFICATION_OK over
131072 routings); that is the author's verifier, not an independent check. The series was noted once in CAOS records
(`problems/combinatorics/bougard-joret/context/report-source.md:37`, accessed 2026-09-04) and never carried into this
problem until today.

Version checks [V]: Afrasyab arXiv:2609.17568, Bérczi et al. arXiv:2608.13983 and Cherniavskii et al. arXiv:2610.16079 are
at v1. SSRN 7423078 (UFB-064) still returns HTTP 403.

Consequences (portfolio review of 2026-11-19, decision 3): the records state Nikolenko's bounds and the corrected credit of
9/8 (RESUME, objects table and experiment index); the lower-bound focus is closed as superseded (UFB-070); EXP-007 re-checks
the records independently (UFB-068); the preprint is revised with that re-check as its new content (UFB-066).
