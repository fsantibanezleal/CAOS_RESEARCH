# Frobenius-minimality preprint

`main.tex` and `main.pdf` are version 0.05 of the CAOS Research preprint. It proves that the public
Huneke-Wiegand numerical-semigroup counterexample has the least possible Frobenius number, 181,
and is the unique normalized pair attaining that minimum within the nonprincipal two-generated
monomial-ideal class. It also proves an explicit infinite family in the same class for every
integer parameter `p>=4`, and determines the endomorphism overring, pseudo-Frobenius set, reduced
type, trace ideals, and conductor uniformly across that family. The common trace/conductor defect
equals the birational extension defect `p+1`.

Attribution is binding: Son Pham discovered the first public counterexample; CAOS contributes the
certified minimality, minimum-layer uniqueness, and parametric-family extensions. Professor Craig
Huneke's verification is external evidence, not authorship of this paper.

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
- version 0.03 DOI: `10.5281/zenodo.21873911`
- version 0.04 DOI: `10.5281/zenodo.21876338`
- version 0.05 DOI: `10.5281/zenodo.21907297` (reserved draft until final QA and publication)
- licence: CC BY 4.0

Evidence sources are EXP-001 through EXP-013 under
`problems/commutative-algebra/huneke-wiegand/`. The heavy proof archive is hash-addressed by the
committed EXP-004, EXP-005, EXP-006 and EXP-007 manifests. EXP-009 contains the family proof,
finite exact campaign, formula-independent auditor, and adversarial controls. EXP-011 contains the
uniform endomorphism-overring proof, two-route campaign, independent auditor, and negative controls.
EXP-012 contains the exact pseudo-Frobenius proof and two independent routes. EXP-013 contains the
trace/conductor proof, the preserved smoke correction, two exact routes, and an independent audit.

Version 0.02 remains frozen with this public-file verification:

- bytes: `350524`
- MD5: `5c5b20c2a69ad2ddf7de6724b235f5d6`
- SHA-256: `93a07d124c7b3f2cf144a5343d31ca40e312a80d99308b3ef567c7065f126bb9`
- the concept latest, public metadata, sole author/ORCID and downloaded PDF all match the committed record

Version 0.03 public-file verification:

- bytes: `399272`
- MD5: `bd9767de4a530150073f654c76ba84a0`
- SHA-256: `f2edff24e924a8d38bc7becd380a69f30fa6b2466c3f584802b829f14d1393cf`
- all 11 pages passed rendered inspection; the two-pass build has no LaTeX warnings, undefined
  references, overfull boxes, or underfull boxes
- the concept latest resolves to record `21873911`; public title, version, sole author/ORCID,
  CC-BY-4.0 licence, filename, bytes, MD5, and SHA-256 match the committed record

Version 0.04 public-file verification:

- bytes: `491757`
- MD5: `248297d0a833ba21dce27d738a50e92f`
- SHA-256: `025cea4c59c4301ff6925cfe43353c7ac1c6cd8b4fc56a8c6d648347f418e825`
- all 12 pages passed rendered inspection; the two-pass build has no LaTeX warnings, undefined
  references, overfull boxes, or underfull boxes
- the concept latest resolves to record `21876338`; public title, version, sole author/ORCID,
  CC-BY-4.0 licence, filename, bytes, MD5, and SHA-256 match the committed record
- a fresh public download matches the committed PDF exactly

Version 0.05 pre-publication verification:

- reserved DOI: `10.5281/zenodo.21907297`; no upload or publication occurred before QA
- candidate bytes: `515650`
- candidate MD5: `75a1102cc9dab8785ee00ba7f93012e7`
- candidate SHA-256: `4bd2cfd7351cb6cec1b3fa006c7eb3018732c283b5bb5a1e5c86015435275276`
- all 15 pages passed rendered inspection; the final two-pass build has no warnings, undefined
  references, overfull boxes, or underfull boxes
- public metadata and fresh-download verification remain pending until publication
