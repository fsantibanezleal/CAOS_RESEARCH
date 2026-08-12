# Frobenius-minimality preprint

`main.tex` is version 0.10 of the CAOS Research preprint; version 0.09 and all earlier versions
remain frozen. Version 0.10 is published at DOI `10.5281/zenodo.21909127` after the complete
claim/build/render and public-file verification workflow passed.
It proves that the public
Huneke-Wiegand numerical-semigroup counterexample has the least possible Frobenius number, 181,
and is the unique normalized pair attaining that minimum within the nonprincipal two-generated
monomial-ideal class. It also proves an explicit infinite family in the same class for every
integer parameter `p>=4`, and determines the endomorphism overring, pseudo-Frobenius set, reduced
type, trace ideals, and conductor uniformly across that family. It also separates the general
one-dimensional Gorenstein duality identity behind the two equal colengths from the
family-specific common ideal and value `p+1`, proves that the conductor is nonstable, and computes
the exact one-step stability defect `length(T_p^2/t^(4s)T_p)=14p`. Version 0.07 continues the
conductor powers, proving reduction number four, quotient lengths `23p-1,14p,2p,1,0`, and
Hilbert-Samuel coefficients `(e0,e1)=(24p,39p)`. Version 0.08 proves that every conductor tangent
cone has depth zero, identifies its unique Valabrega--Valla defect of length `p`, and computes its
coefficientwise-positive Hilbert numerator.
Version 0.09 proves that the complete zeroth local cohomology is `k^p`, concentrated in degree
zero and annihilated by the full homogeneous maximal ideal. Thus the tangent cones are Buchsbaum
but not Cohen--Macaulay with unbounded Buchsbaum invariant `p`; their quotients by `H^0` are
Cohen--Macaulay with an exact Hilbert series.
Version 0.10 determines the complete graded module over the minimal-reduction polynomial ring: a
rank-`24p` free part with explicit shifts plus `p` exponent-one cyclic torsion summands. It derives
the minimal resolution, projective dimension one, regularity four, top-local-cohomology
`a`-invariant three, and `length(G_p/x_pG_p)=25p=e0(T_p)+I(G_p)`.

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
- version 0.05 DOI: `10.5281/zenodo.21907297`
- version 0.06 DOI: `10.5281/zenodo.21907943`
- version 0.07 DOI: `10.5281/zenodo.21908188`
- version 0.08 DOI: `10.5281/zenodo.21908490`
- version 0.09 DOI: `10.5281/zenodo.21908785`
- version 0.10 DOI: `10.5281/zenodo.21909127`
- licence: CC BY 4.0

Evidence sources are EXP-001 through EXP-020 under
`problems/commutative-algebra/huneke-wiegand/`. The heavy proof archive is hash-addressed by the
committed EXP-004, EXP-005, EXP-006 and EXP-007 manifests. EXP-009 contains the family proof,
finite exact campaign, formula-independent auditor, and adversarial controls. EXP-011 contains the
uniform endomorphism-overring proof, two-route campaign, independent auditor, and negative controls.
EXP-012 contains the exact pseudo-Frobenius proof and two independent routes. EXP-013 contains the
trace/conductor proof, the preserved smoke correction, two exact routes, and an independent audit.
EXP-014 proves conductor nonstability by theorem and direct witness. EXP-015 preserves the failed
first square formula, refuted at its mandatory `p=4` smoke gate. EXP-016 proves the corrected exact
square and defect formulas by symbolic residue identities, two complete routes through `p=300`,
and an independent reconstruction audit.
EXP-017 contains the exact conductor-power and Hilbert proof, complete campaign, independent
tail-set reconstruction, and corrupted-profile controls.
EXP-018 contains the exact Valabrega--Valla intersection proof, two-route campaign, independently
written bounded-bitset audit, and Hilbert-series controls.
EXP-019 contains the complete colon-saturation proof, full homogeneous-maximal-annihilator test,
two-route campaign, independent bounded-bitset audit, and Buchsbaum/quotient-series controls.
EXP-020 contains the graded-PID proof, recursive-power Apery-column reconstruction, Hilbert/torsion
route, independently written closed-form audit, exact Betti data, and corrupted-module controls.

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

Version 0.05 public-file verification:

- DOI: `10.5281/zenodo.21907297`; the draft was reserved before build and no upload occurred before QA
- bytes: `515650`
- MD5: `75a1102cc9dab8785ee00ba7f93012e7`
- SHA-256: `4bd2cfd7351cb6cec1b3fa006c7eb3018732c283b5bb5a1e5c86015435275276`
- all 15 pages passed rendered inspection; the final two-pass build has no warnings, undefined
  references, overfull boxes, or underfull boxes
- the concept latest resolves to record `21907297`; public title, version, sole author/ORCID,
  CC-BY-4.0 licence, filename, bytes, MD5, and SHA-256 match the committed record
- a fresh public download matches the committed PDF exactly

Version 0.06 public-file verification:

- reserved DOI: `10.5281/zenodo.21907943`; no upload or publication occurred before claim/build/render QA
- bytes: `526699`
- MD5: `4ff26288ef70a875ebf3f17cb726ff16`
- SHA-256: `10cc2bd31026cfe6a921c4cf54832a7df018b0f0b0f38ee196bc597954255dd4`
- all 17 pages passed rendered inspection at 150 DPI after correcting the section-13 heading;
  the final two-pass build has no warnings, undefined references, overfull boxes, or underfull boxes
- the concept latest resolved to record `21907943`; public title, version, sole author/ORCID,
  CC-BY-4.0 licence, filename, bytes, MD5, and SHA-256 matched the committed record
- a fresh public download matched the committed PDF exactly

Version 0.07 public-file verification:

- DOI: `10.5281/zenodo.21908188`; no upload or publication occurred before claim/build/render QA
- bytes: `539211`
- MD5: `5ed0616521a3363fb9cb6507babf9745`
- SHA-256: `2dca97dc100424afbeffd525fe66aa4aa43ce65c82c11b9ac43250cd33771e19`
- all 18 pages passed rendered inspection at 150 DPI; the final two-pass build has no warnings,
  undefined references, overfull boxes, or underfull boxes
- the concept latest resolves to record `21908188`; public version, sole author/ORCID, filename,
  bytes, MD5, and SHA-256 match the committed record
- a fresh public download matches the committed PDF exactly

Version 0.08 public-file verification:

- reserved DOI: `10.5281/zenodo.21908490`; no upload or publication occurred before
  claim/build/render QA
- bytes: `552905`
- MD5: `29a4c70d45517a61d6eb01f028487b39`
- SHA-256: `c8a038adf042a71126e0b0dac170803340e12300521aad1ca05f88bbc3c32f69`
- all 20 pages passed rendered inspection at 150 DPI; the final stable two-pass build has no
  warnings, undefined references, overfull boxes, or underfull boxes
- the concept latest resolves to record `21908490`; public version, sole author/ORCID, CC-BY-4.0
  licence, filename, bytes, MD5, and SHA-256 match the committed record
- a fresh public download matches the committed PDF exactly

Version 0.09 public-file verification:

- reserved DOI: `10.5281/zenodo.21908785`; no upload or publication occurred before
  claim/build/render QA
- bytes: `567854`
- MD5: `c0605ace2b60d6830fd6e68d68d883b0`
- SHA-256: `ecf4d1ebe504ad3af74d123c949a953a7f397dabd72ec11c94a631962e1501db`
- all 21 pages passed rendered inspection at 150 DPI; the final stable two-pass build has no
  warnings, undefined references, overfull boxes, or underfull boxes
- the concept latest resolves to record `21908785`; public version, sole author/ORCID, CC-BY-4.0
  licence, filename, bytes, MD5, and SHA-256 match the committed record
- a fresh public download matches the committed PDF exactly

Version 0.10 public-file verification:

- reserved DOI: `10.5281/zenodo.21909127`; no upload or publication occurred before
  claim/build/render QA
- bytes: `578949`
- MD5: `830ae1fd2e2fbf923a86cbf575e9a841`
- SHA-256: `00a78fd8101f106724877b3fdbc933c51024a872a2b9a4f05692358b4d1a9d03`
- all 22 pages passed rendered inspection at 150 DPI; the final stable two-pass build has no
  warnings, undefined references, overfull boxes, or underfull boxes
- the concept latest resolves to record `21909127`; public version, sole author/ORCID, CC-BY-4.0
  licence, filename, bytes, MD5, and SHA-256 match the committed record
- a fresh public download matches the committed PDF exactly
