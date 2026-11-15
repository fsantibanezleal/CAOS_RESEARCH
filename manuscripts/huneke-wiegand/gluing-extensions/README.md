# Tensor factorization of extension ideals under gluing

Focused companion of the Huneke-Wiegand programme (focus `HW-F8`).

- Main theorem: EXP-068 (`problems/commutative-algebra/huneke-wiegand/experiments/EXP-068-gluing-tensor-factorization/`):
  for a gluing `a1*Gamma1 + a2*Gamma2`, `I_A (x) I_(A*) = T1 (x)_(k[y]) T2` for the extension
  `A = a1*A1 + a2*A2`, the torsion-length law, multiplicativity of minimal generators, and the
  characterization of the Huneke-Wiegand property for extensions.
- Corollaries: Propositions 9 and 10 of García-Sánchez and Leamer (arXiv:1211.4554), re-proved with
  credit; the case they leave open; four-generated counterexamples over symmetric semigroups
  (Frobenius numbers 23645 and 53599); EXP-067 as a credited corollary.
- Build: three-pass `pdflatex main.tex`; voice gate `scripts/check_manuscript_voice.py`; tables and figures regenerate with `python make_results.py` (reads the EXP-068 and EXP-070 artifacts).
- v0.02 (current): version DOI [10.5281/zenodo.24240435](https://doi.org/10.5281/zenodo.24240435), published 2026-11-15; 27 pages, 773,736 bytes,
  SHA-256 `1e20b8d6f1d4540e6b08d9f637d592c5ce0afaaa2f271ea364a17e086c572acb`.
- v0.01: version DOI [10.5281/zenodo.23821498](https://doi.org/10.5281/zenodo.23821498), concept DOI
  [10.5281/zenodo.23821497](https://doi.org/10.5281/zenodo.23821497). Reserved 2026-10-30 and the PDF frozen
  (sha256 `730e7ae0651b95ee9def05ed98556f67611e1fe9be476ac96464b175e7087fa1`); published 2026-11-01, public download verified against the frozen file.
- Approval record: [`publication-gate.json`](publication-gate.json).
- v0.02 (draft source, not released): validation on gluings with a counterexample factor (EXP-070), algorithms and degree-bound lemma, results tables, re-pointed citations, extended related work, derived Frobenius and symmetry, embedding-dimension proof, completion argument; claim audit in [`claim-audit-v0.02.md`](claim-audit-v0.02.md). The committed `main.pdf` is the v0.01 file until the release builds the new one.
