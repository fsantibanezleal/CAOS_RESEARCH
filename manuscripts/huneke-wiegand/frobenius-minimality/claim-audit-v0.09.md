# Claim audit - manuscript v0.09

Audited: 2026-08-12. Prepublication result: PASS.

Version 0.09 retains all v0.08 claims and adds only the theorem-level consequences of the
committed EXP-019 symbolic proof. Exact campaigns support the proof and do not replace it.

| manuscript claim | evidence | audit result |
|---|---|---|
| prior minimality, uniqueness, family, endomorphism, type, trace, stability, reduction, and depth-zero tangent-cone results | claim audits v0.05--v0.08; EXP-001--018 | PASS; scope and attribution unchanged |
| homogeneous colon-saturation formula for `H^0` | definition of homogeneous local cohomology applied directly to `gr_T(R)` | PASS; conductor filtration treated directly, not by importing maximal-ideal Apery formulas |
| stable saturation threshold `v>=4(n+1)s` | EXP-017 tail `v(T^k)=[4ks,infinity)` for every `k>=4` | PASS; both directions and persistence from smaller killing powers proved |
| complete `H^0` is `k^p` in degree zero | exact consecutive conductor-power profiles and `v(R) minus v(T)={0} union (5s+K_p)` | PASS; unit removed by threshold, all positive degrees excluded |
| full homogeneous maximal ideal annihilates `H^0` | separate `m_p/T_p` and `G_(p,+)` product containments | PASS; exceptional value `13s-1` excluded by the empty level-seven ring block |
| tangent cone is Buchsbaum but not Cohen--Macaulay | dimension-one local-cohomology criterion plus EXP-018 depth zero | PASS; full maximal ideal, not only the irrelevant ideal, is tested |
| Buchsbaum invariant is `p` and unbounded | complete `H^0` basis of cardinality `p` | PASS |
| quotient by `H^0` is Cohen--Macaulay with numerator `1+(10p-1)z+12pz^2+(2p-1)z^3+z^4` | positive depth after quotient and exact subtraction of the degree-zero torsion series `p` | PASS |
| computational support through `p=300` | EXP-019 `results.json`, `audit.json`, two exact routes, independent bounded-bitset implementation | PASS; campaign `854d7889...dbf7`, audit `0b01853f...c68a` |
| Buchsbaum criterion sources | D'Anna--Mezzasalma--Micale DOI `10.1080/00927870802116521`; D'Anna--Micale--Sammartano DOI `10.1216/JCA-2011-3-2-147` | PASS; primary sources cited and filtration-specific boundary stated |
| authorship | title page and `zenodo.json` | PASS; Felipe Santibanez-Leal is sole author; no automated system named |
| publication identity | reserved Zenodo draft and page-one block | PASS prepublication; version DOI `10.5281/zenodo.21908785`, concept DOI `10.5281/zenodo.21763582` |

## Scope boundaries

- EXP-019 concerns only the conductor filtration in the explicit EXP-009 family.
- It does not classify Buchsbaum tangent cones of arbitrary ideals or numerical-semigroup rings.
- The unbounded invariant is a theorem across this family, not a universal extremal statement.
- The broad Huneke--Wiegand conjecture was already disproved by the public seed; discovery priority
  remains Son Pham's.

## Build and rendered-document gate

- final stable two-pass MiKTeX `pdflatex`: PASS;
- warning, reference, and box audit: PASS; zero warnings, undefined references, overfull boxes, or
  underfull boxes in the stable pass;
- complete 21-page rendered inspection at 150 DPI: PASS; title/DOI block, new theorem and proof,
  multiline formulas, hashes, references, running headers, and page numbers are legible without
  clipping or overlap;
- frozen candidate PDF: 567854 bytes, MD5 `c0605ace2b60d6830fd6e68d68d883b0`, SHA-256
  `ecf4d1ebe504ad3af74d123c949a953a7f397dabd72ec11c94a631962e1501db`;
- public record, concept latest, and fresh-download equality gates: pending publication.
