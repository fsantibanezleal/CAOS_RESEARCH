# Frobenius-minimality preprint

`main.tex` and `main.pdf` are version 0.01 of the CAOS Research preprint proving that the public
Huneke-Wiegand numerical-semigroup counterexample has the least possible Frobenius number, 181,
within the nonprincipal two-generated monomial-ideal class.

Attribution is binding: Son Pham discovered the counterexample; CAOS contributes the certified
minimality extension. Professor Craig Huneke's verification is external evidence, not authorship of
this paper.

Build twice from this directory:

```powershell
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

Render for visual QA:

```powershell
pdftoppm -png -r 150 main.pdf tmp/pdfs/hw-minimality
```

Zenodo identifiers:

- concept DOI: `10.5281/zenodo.21763582`
- version 0.01 DOI: `10.5281/zenodo.21763583`
- licence: CC BY 4.0

Evidence sources are EXP-001 through EXP-006 under
`problems/commutative-algebra/huneke-wiegand/`. The heavy proof archive is hash-addressed by the
committed EXP-004 and EXP-005 manifests.
