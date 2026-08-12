# Claim audit - manuscript v0.07

Audited: 2026-08-12. Prepublication result: PASS. Public-artifact verification: PENDING.

Version 0.07 retains the v0.06 duality correction and adds only theorem-level consequences of the
committed EXP-017 block proof. Exact campaigns support the symbolic proof and do not replace it.

| manuscript claim | evidence | audit result |
|---|---|---|
| prior minimality, uniqueness, family, endomorphism, type, trace, and stability results | claim audits v0.05/v0.06; EXP-001--016 | PASS; scope and attribution unchanged |
| `Q_p=t^(4s)R_p` is a reduction of `T_p` | EXP-017 proof; exact formula `T_p^5=Q_pT_p^4` | PASS |
| reduction number is exactly four | EXP-017 proof; three preceding nonzero Sally quotients | PASS; no earlier stabilization |
| quotient profile `23p-1,14p,2p,1,0` | EXP-013/016 formulas and EXP-017 block subtraction | PASS; exact sets and cardinalities explicit |
| power formulas for `T_p^3,T_p^4,T_p^5` | EXP-017 residue proof | PASS; symbolic interval identities are load-bearing |
| `Q_p` is minimal | one-dimensional maximal-primary setting plus one-generated reduction | PASS; no claim for arbitrary reductions |
| Hilbert function `24pn-39p` for `n>=4` and `(e0,e1)=(24p,39p)` | EXP-017 nonzerodivisor length identity and quotient sum | PASS; derived in text, not inferred from the campaign |
| computational support through `p=300` | EXP-017 `results.json`, `audit.json`, and independent tail-set implementation | PASS; campaign `e9c3c887...6030`, audit `0f6ed706...c781` |
| reduction terminology | Northcott--Rees, DOI `10.1017/S0305004100029194` | PASS; definition and attribution only |
| authorship | title page and `zenodo.json` | PASS; Felipe Santibanez-Leal is sole author; no automated system named |
| publication identity | reserved Zenodo record and page-one block | PENDING; DOI `10.5281/zenodo.21908188` is reserved, but no public record is claimed before upload, publication, and fresh-download verification |

## Scope boundaries

- EXP-017 concerns only the explicit conductor family `T_p`.
- No reduction-number or Hilbert-coefficient statement is claimed for arbitrary conductors, trace
  ideals, finite birational extensions, or numerical semigroup rings.
- The broad Huneke--Wiegand conjecture was already disproved by the public seed; discovery priority
  remains Son Pham's.

## Build and rendered-document gate

- two-pass MiKTeX `pdflatex`: PASS;
- warning, reference, and box audit: PASS; zero warnings, undefined references, overfull boxes, or
  underfull boxes in the final pass;
- complete 18-page rendered inspection at 150 DPI: PASS; title block, theorem table, multiline
  equations, hashes, references, running headers, and page numbers are legible without clipping;
- frozen candidate PDF: 539211 bytes, MD5 `5ed0616521a3363fb9cb6507babf9745`, SHA-256
  `2dca97dc100424afbeffd525fe66aa4aa43ce65c82c11b9ac43250cd33771e19`;
- public record status, concept latest, sole author/ORCID, CC-BY-4.0 licence, filename, hashes, and
  fresh downloaded-file equality: PENDING.
