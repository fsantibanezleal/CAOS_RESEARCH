# Claim and scope audit, version 0.06 (draft, unreleased)

Date: 2026-11-14. Publication status: source revision on branch
`work/huneke-wiegand/integral-revision-20261114`; not built into a release PDF, not published. Version 0.05 is the
published correction of the sign in the support-one endpoint theorem. This audit lists every theorem of the v0.06
source with its mark and its evidence, and the scope of each new section. Theorem numbers are those of the v0.06
build (sections 5 to 11 renumber because of the new sections 2 and 3, and the numbering of v0.05 is not retained).

## Theorem-to-evidence map

| statement (v0.06 number) | mark | owner and evidence | audit boundary |
|---|---|---|---|
| Proposition 5.1, original representative transfer `M_p(s_p+q_p)=b_p+eta_p` | [D] | EXP-056, EXP-057 | exact integral identity in the full original presentation |
| Theorem 6.1, integral potential basis in the fixed-high sector | [D] | EXP-059: signed reconstruction; 861 chains checked [MV] | one D kernel only; not a normal form of the cokernel |
| Lemma 7.1, full shifted boundary | [D] | EXP-060 | construction for the shifted potentials, no basis theorem |
| Lemma 8.1, signed interval triangle | [D] | EXP-060, EXP-062 | exact original boundary `y_ia - y_ib` |
| Proposition 8.2, twice-edge source | [D] | EXP-060 | `M_p P(F_j)=2 x_0j`, j=1,2 |
| Lemma 8.3, exact short corrections | [D] | EXP-060 | the two corrections `B`, `D` with their full boundaries |
| Theorem 8.4, uniform original-map annihilation `M_p V_p = 2 eta_p` | [D] | EXP-060; 18 parameters checked by two encodings [MV]; source support `32p-146` observed at all 18 | order dividing two; the support law is an observation |
| Corollary 8.5, base change with two invertible | [D] | tensoring Theorem 8.4 | the two tracked classes only |
| Lemma 9.1, complete K-source annihilation | [D] | EXP-061 | all original K sources |
| Proposition 9.2, complete generalized potential reconstruction | [D] | EXP-061 | complete D kernels over F2 |
| Proposition 9.3, relative reflection functional | [D] | EXP-061; 65 sector row-span certificates at p=8..12 [MV] | annihilates `d_K^K` and `d_K^S(ker d_D)` |
| Theorem 9.4, exact order two of the tracked class | [D] | EXP-061 | exact order two for every p>=8 |
| Proposition 10.1, full original triangle sources | [D] | EXP-062: 70 sources checked [MV] | `M_p W_T = 2 x_T` |
| Theorem 10.2, independent triangle classes and exact count | [D] | EXP-062: independent sector certificates for all 27 triangles at p=8..12 [MV] | exact relation lattice `2 Z^T`; count `floor(((p-2)^2+3)/12)` |
| Corollary 10.3, direct summand `(Z/2)^q` | [D] | EXP-062 | existence of a retraction; the complement is not described |
| Proposition 10.4, transfer of the tracked class to one triangle | [D] | EXP-062: five transfers at p=8..12 [MV] | quotient equality with an explicit source |
| Theorem 11.1, support-one endpoint sources, `Pi_58 M_p s_(p,r) = (-1)^(p+1) x_(0,r,p-2-r)` | [D] | EXP-065, EXP-066: 586 endpoint checks, 2,930 altered cases rejected [MV] | two endpoint rows after one projection; no independence for the other rows |

## Premise and marks added in v0.06

| statement | mark | evidence | audit boundary |
|---|---|---|---|
| `M_p` equals the Koszul-strand block matrix `[d_D 0; J delta_K]` in the cell `(p,2)` | [MV] for p=8,9,10; [C] for every other p | EXP-036 cells (8,2), (9,2) and EXP-037 cell (10,2); EXP-054 regression on 15,405 retained rows | no all-parameter derivation was found; the abstract and the title claim only the explicit matrix |
| Block identity `dim = rows(delta_K) + rank d_D - rank M` and the incidence map `delta_K` | [D] | v0.25 of the consolidated preprint (DOI 10.5281/zenodo.22835108), Theorem 15.14 and its proof, and the EXP-035 block identity | holds for every p once `M` is given |
| Zero-row classification and cubic-source exclusion at every cell `(p,t)` | [D] | the same preprint, Theorems 15.15 and 15.16 | kernel side only |
| Finite carrier comparison at p=8..11, masks 56, 58, 59, 62 | [MV] | EXP-063 (19 triangle rows, 12 mutation controls), EXP-064 (16 carriers, 1,100 prime-rank pairs) | finite; integral vanishings follow from exponent certificates, not from explicit sources |
| Complete cokernel, upper bound, odd torsion, free rank | [C] | open | the direct summand is a lower bound only |

## Exact scope

For every `p>=8`, EXP-060 to EXP-062 prove a direct summand `(Z/2)^floor(((p-2)^2+3)/12)` in the specified full
integer presentation `coker_Z M_p`. This is a statement about the explicit matrix of Section 4. Its reading as the
integral group behind the characteristic dependence of the Betti numbers of the quadratic quotient and the fiber cone
in the cell `(p,2)` rests on the premise above. At `p=8,9,10` the proved summand has 3, 4, 5 factors while the exact
characteristic-two excess of the full target is 31, 49, 72 (EXP-036, EXP-037), so the summand is a small part of what
the finite data show.

The paper does not prove a canonical all-parameter identification between the semantic projection and the persistent
isolated carrier. It does not give the complete projected kernel, a complete 2-primary quotient, a global retraction,
a free rank, an exclusion of odd torsion, or a full Smith form.

## Plan items of the independent audit and where each is addressed

| audit item | place in v0.06 |
|---|---|
| 1, problem and context | Section 2 (conjecture and disproofs, the complex and strand and module, what integral two-torsion says) and Section 3 (related work) |
| 2, derivation or premise of `M_p` | Section 4.1 and Table 3: premise, [MV] for p=8,9,10, [C] otherwise; abstract and title restricted to the explicit matrix |
| 3, sign of Theorem 11.1 | kept as published in v0.05; the p=11 entries are on unsigned rows (Section 11 and Section 13.7) |
| 4, algorithms and reproducibility | Section 12: Algorithms 1 to 4, Tables 7 to 10 |
| 5, EXP-063 and EXP-064 in the appendix table | Appendix Table 14 (records) and Section 13.6 with the generated Table 13 |
| 6, related work on adjacent methods | Section 3 |
| 7, figure, one abstract, a title naming the complex | Figure 1; the abstract of 218 printed words; the title names the Koszul-strand presentation |

## Validation and build identity

- Three pdflatex passes exit 0 with no warning, no overfull and no underfull box.
- The scientific-voice guard prints `manuscript voice: clean`.
- The depth checker in research mode reports 10,663 words, 116 display equations, 14 tables, 26 references and
  4 algorithms; the remaining findings are 1 figure against a floor of 6 and the absence of a reported statistical
  uncertainty, which does not apply to exact computations.
- The artifact-derived tables are generated by `generate_tables.py` from the stored artifacts; `--check` confirms
  that `main.tex` is current.
- `\versiondoi` and the publication date are set by the release; no PDF of this source is published.

## Next-version decision

The manuscript remains one source/duality paper. A later version requires a derivation of the premise for all `p`, a
canonical comparison, a complete kernel or quotient theorem, a reusable integral matching theorem, a correction, or a
material reproducibility change. The route is governed as `HW-F5` and is gated.
