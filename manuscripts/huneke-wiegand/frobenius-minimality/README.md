# Frobenius-minimality preprint

`main.tex` and `main.pdf` are version 0.02 of the CAOS Research preprint proving that the public
Huneke-Wiegand numerical-semigroup counterexample has the least possible Frobenius number, 181,
and is the unique normalized pair attaining that minimum within the nonprincipal two-generated
monomial-ideal class.

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
- version 0.01 DOI: `10.5281/zenodo.21763583` (frozen)
- version 0.02 DOI: `10.5281/zenodo.21764868`
- licence: CC BY 4.0

Evidence sources are EXP-001 through EXP-007 under
`problems/commutative-algebra/huneke-wiegand/`. The heavy proof archive is hash-addressed by the
committed EXP-004, EXP-005 and EXP-007 manifests.

Version 0.02 public-file verification:

- bytes: `350524`
- MD5: `5c5b20c2a69ad2ddf7de6724b235f5d6`
- SHA-256: `93a07d124c7b3f2cf144a5343d31ca40e312a80d99308b3ef567c7065f126bb9`
- the concept latest, public metadata, sole author/ORCID and downloaded PDF all match the committed record
