# Claim audit - curvilinear conductor fiber cones v0.01

Audit date: 2026-08-18. Decision: **PASS - validated DOI-bearing upload candidate**.

Publication is not yet claimed. Zenodo draft `21997378` reserved version DOI
`10.5281/zenodo.21997378` and concept DOI `10.5281/zenodo.21997377`; the draft remains unpublished
and no file upload is yet claimed.

## Claim map

| manuscript claim | evidence owner | audit result |
|---|---|---|
| truncated standard-graded parametrization inside `k[x,y]/(y^(24p))` | EXP-025 Theorem/P1 and `proof.md` Section 1 | PASS |
| exact dehomogenization `k[y]/(y^(24p))` | EXP-025 P2 and `proof.md` Section 2 | PASS |
| `radical(J_p)=L_p` and `J_p` is `L_p`-primary | EXP-025 P3 and no-embedded-primes argument | PASS |
| nilradical has sharp index `24p` | EXP-025 P4; witness `X_1^(24p-1)` | PASS |
| saturation and length-`24p` curvilinear fat point | EXP-025 P5 and `proof.md` Section 4 | PASS |
| locally Gorenstein but homogeneous ring nonlevel/non-Gorenstein | EXP-025 P6 plus frozen EXP-021 type `10p+1` | PASS |
| exact Kahler differential module and characteristic split | EXP-025 P7 and conormal-sequence derivation | PASS |
| 297-row campaign and independent all-row audit | EXP-025 deterministic artifacts | PASS |

The manuscript treats EXP-021/023/024 as frozen input, states that finite computation does not
prove the infinite theorem, and retains the EXP-023 solver/encoding boundary. It makes no claim
for arbitrary fiber cones, arbitrary conductor ideals, arbitrary modules, or arbitrary
one-dimensional Gorenstein domains.

## Source and novelty boundary

- Herzog--Qureshi--Saem supplies context for explicit and nonradical monomial fiber cones.
- Herzog--Zhu supplies additional defining-ideal and Cohen--Macaulay fiber-cone context.
- Kreuzer--Linh--Long supplies the curvilinear and differential-scheme context.
- The earlier CAOS preprint, DOI `10.5281/zenodo.21995498`, is cited as the owner of the family and
  frozen input theorems.
- The negative search is not presented as a proof of novelty.

## Build and render QA

- clean two-pass pdfLaTeX build;
- no LaTeX warnings, undefined references, overfull boxes, or underfull boxes;
- PDF metadata title and author match the manuscript;
- all six pages rendered at 150 DPI and inspected after the final style change;
- no clipping, overlap, broken equations, unreadable glyphs, table overflow, or bibliography
  defects;
- inconsistent draft running headers were removed; the final note uses a uniform footer-only page
  style.

Frozen candidate:

```text
file    = main.pdf
pages   = 6
bytes   = 424886
MD5     = 43ce7ec181d26c38b17678b453a8e27e
SHA-256 = e9d51bb63492c37eae4ddb7a6790e50c1a3292006bd23660a0bbe2c69c19be4a
```

## Identity, attribution, and metadata QA

- sole author: Felipe Santibañez-Leal;
- ORCID: `0000-0002-0150-3246`;
- Son Pham's first-counterexample discovery priority is explicit;
- Professor Craig Huneke's verification is described as independent external evidence;
- neither is presented as an author or endorser of this theorem;
- no LLM, AI system, tool, or model is named as author or co-author;
- CC BY 4.0, version `0.01`, English language, keywords, subjects, and related identifiers are
  internally consistent;
- `zenodo.json` is valid JSON and contains Felipe as its only creator.

## Publication gate

The reversible concept draft is reserved and both assigned DOIs are printed in the PDF. The
warning-free rebuild, complete six-page render inspection, identity checks, and new hash freeze
pass. This exact candidate may now be attached to draft `21997378`; publication remains gated on
the attached-file verification and must be followed by public metadata and fresh-download checks.
