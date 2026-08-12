# Claim audit - manuscript v0.08

Audited: 2026-08-12. Final result: PASS.

Version 0.08 retains the v0.06 duality correction and all v0.07 reduction results. It adds only
the theorem-level consequences of the committed EXP-018 symbolic proof. Exact campaigns support
the proof and do not replace it.

| manuscript claim | evidence | audit result |
|---|---|---|
| prior minimality, uniqueness, family, endomorphism, type, trace, stability, and reduction results | claim audits v0.05--v0.07; EXP-001--017 | PASS; scope and attribution unchanged |
| exact nonzero quotient `(Q_p intersect T_p^2)/(Q_pT_p)` | EXP-018 proof intersecting the EXP-016 square with `v(Q_p)` | PASS; exact level-nine residue block stated |
| unique Valabrega--Valla defect has length `p` | complement `D minus (A_p union B_p)` | PASS; two singletons plus an interval of size `p-2` |
| all intersection quotients at `n=0` and `n>=2` vanish | EXP-017 cubic, quartic, quintic, and stabilization formulas | PASS; infinite tail proved, not inferred from the campaign |
| tangent cone has depth zero and is not Cohen--Macaulay | Valabrega--Valla criterion with `x=t^(4s)` a regular superficial minimal-reduction generator | PASS; dimension, regularity, residue-field, and reduction hypotheses explicit |
| Hilbert function `(p+1,10p,22p,24p-1,24p,...)` | EXP-017 Sally quotients plus exact parameter-quotient length | PASS |
| Hilbert numerator `(p+1)+(9p-1)z+12pz^2+(2p-1)z^3+z^4` | direct first-difference derivation | PASS; all coefficients positive for `p>=4` |
| computational support through `p=300` | EXP-018 `results.json`, `audit.json`, and independent bounded-bitset implementation | PASS; campaign `9631c644...5971`, audit `7c2abcd2...81ff` |
| tangent-cone criterion source | Valabrega--Valla, DOI `10.1017/S0027763000018225` | PASS; primary source cited |
| authorship | title page and `zenodo.json` | PASS; Felipe Santibanez-Leal is sole author; no automated system named |
| publication identity | public Zenodo record, page-one block, and fresh download | PASS; version DOI `10.5281/zenodo.21908490`, concept DOI `10.5281/zenodo.21763582`, sole author/ORCID, and public SHA-256 match Git |

## Scope boundaries

- EXP-018 concerns only the explicit conductor family `T_p`.
- It does not claim that arbitrary conductors, trace ideals, or reduction-number-four ideals have
  non-Cohen--Macaulay tangent cones.
- Positive Hilbert numerator coefficients are recorded as an exact feature of this family, not as
  a general diagnostic theorem.
- The broad Huneke--Wiegand conjecture was already disproved by the public seed; discovery priority
  remains Son Pham's.

## Build and rendered-document gate

- final stable two-pass MiKTeX `pdflatex`: PASS;
- warning, reference, and box audit: PASS; zero warnings, undefined references, overfull boxes, or
  underfull boxes in both stable passes;
- complete 20-page rendered inspection at 150 DPI: PASS; title/DOI block, theorem statement,
  multiline equations, hashes, references, running headers, and page numbers are legible without
  clipping or overlap;
- frozen candidate PDF: 552905 bytes, MD5 `29a4c70d45517a61d6eb01f028487b39`, SHA-256
  `c8a038adf042a71126e0b0dac170803340e12300521aad1ca05f88bbc3c32f69`;
- public record status, concept latest, sole author/ORCID, CC-BY-4.0 licence, filename, hashes, and
  fresh downloaded-file equality: PASS.
