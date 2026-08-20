# Frobenius-minimality preprint

`main.tex` is version 0.18 of the CAOS Research preprint; version 0.17 and all earlier versions
remain frozen. Version 0.18 adds the EXP-031 integral degree-seven contraction, proves
`beta_(3,7)=0`, and completes the third homological row over every field. DOI
`10.5281/zenodo.22030743` is reserved; upload and publication remain gated on complete
claim/build/render validation. Version 0.17 passed the complete claim/build/render, authenticated
upload, publication, concept-latest, and fresh-download workflow and is published at DOI
`10.5281/zenodo.22030167`. Version 0.16 passed the complete claim/build/render, authenticated upload,
publication, concept-latest, and fresh-download workflow and is published at DOI
`10.5281/zenodo.22029468`. Version 0.15 is published at DOI
`10.5281/zenodo.22016550`, and a fresh unauthenticated download matches the committed PDF exactly.
Version 0.14 remains
published at DOI `10.5281/zenodo.22013515`, and a fresh unauthenticated download matches the
committed v0.14 PDF exactly.
Version 0.13 remains published at DOI
`10.5281/zenodo.21995498`, and a fresh unauthenticated download matches the committed PDF exactly.
Version 0.12 remains published at DOI
`10.5281/zenodo.21988601`, and matches a fresh public download exactly. Version 0.11 remains
published and fresh-download verified at DOI `10.5281/zenodo.21909961`.
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
Version 0.11 proves `T_p^2=m_pT_p`, identifies the conductor special fiber canonically with
`G_p/H^0(G_p)`, and computes Cohen--Macaulay type `10p+1`. Its Artinian socle lies in degrees two
and four, so the fiber cone is neither level nor Gorenstein.
Version 0.12 determines the complete defining ideal of that special fiber. It has
`50p^2-17p` minimal quadrics and the single additional cubic
`X_0^2X_(3p)-X_p^3`, hence relation type three and non-Koszulness. The all-parameter state-graph
connectivity calculation is exact Presburger verification; the separately encoded audit and the
absence of a checked solver proof object are both recorded.
Version 0.13 determines exact edges of the minimal resolution over the full `10p`-variable
presentation ring: projective dimension `10p-1`, regularity four,
`beta_(2,3)=2p(500p^2-330p+31)/3`, the complete last row, the penultimate extremal entry `8p`,
and the canonical-module generator degrees.
Version 0.14 determines the first previously open interior strand. It proves
`beta_(2,4)=8p`, gives its complete multiplicity-free multigraded support, and derives
`beta_(3,4)=p(5p-1)(500p^2-440p+47)/2`. The relative homology is integrally free on the stated
support, so the result is characteristic-free. It also proves that the quadratic part of the
defining ideal is linearly presented through this first nonlinear position. The remaining
interior Betti table is still open.
Version 0.15 completes the second Betti row. It proves
`beta_(2,5)=p(2p-3)` with complete three-block offset multiplicities and
`beta_(2,6)=0`. Integral lexicographic matching and a unit Smith form prove characteristic
independence. The higher interior rows remain open.
Version 0.16 determines the complete degree-five third-syzygy profile. If
`H_p={a in G_p:a>=6p}`, then `beta_(3,(5,b))` counts unordered pairs of distinct elements of
`H_p` with sum `b-3p`, so `beta_(3,5)=4p(8p-1)` and the support is
`[15p+1,39p-3] minus {33p-1}`. The integral normal form is free on this pair basis. Together with
EXP-028 and the exact Hilbert numerator, it gives
`beta_(4,5)=2p(5p-1)(10p-3)(100p^2-110p+13)/3` and completes internal degree five over every
field. The third row, full Betti table, and full resolution remain open.
Version 0.17 identifies the complete cubic-colon quotient as the canonical idealization
`V_p semidirect omega_(V_p)` of the `p`-th Veronese rational normal curve ring. Its multigraded
Hilbert numerator and an integral relative normal form prove
`beta_(3,6)=8p(7p^2-12p+2)/3` over every field, with exact support
`[3p+4,29p-5] minus ([6p-3,6p+1] union [9p-3,9p])`.
Version 0.18 proves `beta_(3,7)=0` integrally. Zero-vertex matching leaves only residual-hole
triangles, and a low positive vertex gives each one a distinct same-offset tetrahedral filler with
a single unit critical boundary entry. Together with versions 0.14, 0.16, and 0.17, the complete
third row is

```text
beta_(3,4)=p(5p-1)(500p^2-440p+47)/2,
beta_(3,5)=4p(8p-1),
beta_(3,6)=8p(7p^2-12p+2)/3,
beta_(3,7)=0,
beta_(3,j)=0 otherwise.
```

Higher rows, the full Betti table, and the full resolution remain open.

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
- version 0.11 DOI: `10.5281/zenodo.21909961`
- version 0.12 DOI: `10.5281/zenodo.21988601` (published and fresh-download verified)
- version 0.13 DOI: `10.5281/zenodo.21995498` (published and fresh-download verified)
- version 0.14 DOI: `10.5281/zenodo.22013515` (published and fresh-download verified)
- version 0.15 DOI: `10.5281/zenodo.22016550` (published and fresh-download verified)
- version 0.16 DOI: `10.5281/zenodo.22029468` (published and fresh-download verified)
- version 0.17 DOI: `10.5281/zenodo.22030167` (published and fresh-download verified)
- version 0.18 DOI: `10.5281/zenodo.22030743` (reserved; publication gated on QA)
- licence: CC BY 4.0

Evidence sources are EXP-001 through EXP-031 under
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
EXP-021 contains the exact square and natural-kernel proof, a 297-parameter reconstruction of the
fiber cone and Artinian socle, the preserved first budget-only attempt, an independently encoded
six-parameter/all-row-hash audit, and corrupted-square, kernel, socle, and type controls.
EXP-022 preserves the refuted quadratic-presentation conjecture and proves the universal necessary
cubic. EXP-023 proves the corrected one-cubic presentation with an exact all-parameter Presburger
component cover, a bounded campaign through `p=23`, an independently encoded total-graph audit,
and the preserved first over-budget attempt.
EXP-024 contains the symbolic homological proof, two independent linear-syzygy derivations, exact
297-row campaign, all-row independent rebuild, frozen premise hashes, and adversarial controls
against false edge data and full-table overclaim.
EXP-027 proves the first interior strand using relative squarefree-divisor complexes, an integral
unit matching, an exact linear-colon computation, explicit semigroup paths, a parity obstruction,
and a minimal mapping cone. Its exact campaign covers `p=4,...,300`; independently encoded audits,
all-offset small cases, two-characteristic checks, and six symbolic UNSAT obligations support the
deductive proof without replacing it.
EXP-028 completes the second Betti row using total-degree-five and degree-six relative complexes,
an integral interval matching, a unit Smith normal form, 297 formula rows, complete small-parameter
profiles, two-characteristic checks, and an independently encoded rational/Smith audit.
EXP-029 proves the free colon--Koszul pair basis and the complete internal-degree-five diagonal.
Its exact campaign checks 297 parameters through `p=300`, complete relative `H_2` profiles at
`p=4,5,6`, two characteristics at `p=4`, an independent rational support-boundary audit, and a
constant-memory arithmetic/Z3 support certificate through `p=10000`. The first symbolic
implementation is preserved as non-evidence after exceeding its declared budget.
EXP-030 identifies the complete cubic-colon quotient with a canonical idealization and proves the
complete total-degree-six third-syzygy profile. Its canonical campaign checks 297 formula rows and
complete relative profiles for `p=4,5,6`; a separately encoded audit matches every coefficient
and selected rational ranks, and a symbolic certificate checks the scalar and support formulas.
The audit's first implementation incorrectly inserted the forbidden offset `8p-1`; it is retained
as invalid non-evidence, while the corrected implementation passes.
EXP-031 proves the final degree-seven vanishing and completes the third row. Its all-parameter
integral proof uses an acyclic zero-vertex matching and a signed unit filler block. The canonical
campaign checks residual formulas through `p=300`, every critical filler through `p=12`, and exact
small profiles; a separately encoded opposite-order audit and arithmetic certificate agree. The
first tuple-only filler key is retained as invalid non-evidence because it compared cells from
different multigraded offsets.

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

Version 0.11 public-file verification:

- reserved DOI: `10.5281/zenodo.21909961`; no upload or publication occurred before
  claim/build/render QA
- bytes: `589535`
- MD5: `1ad22a6a87c0c6a5a80f8a913d06ca95`
- SHA-256: `0b3a9131e3c419c0a89cb064ea6beb7c696006171fe18bec578e7ba963a520ce`
- all 25 pages passed rendered inspection at 150 DPI; the final stable two-pass build has no
  warnings, undefined references, overfull boxes, or underfull boxes
- sole authorship, ORCID, version, reserved DOI, concept DOI, and CC-BY-4.0 metadata gates pass
- the concept latest resolves to record `21909961`; public version, sole author/ORCID, CC-BY-4.0
  licence, filename, bytes, MD5, and SHA-256 match the committed record
- a fresh unauthenticated public download matches the committed PDF exactly

Version 0.12 public-file verification:

- DOI: `10.5281/zenodo.21988601`; no upload or publication occurred before claim/build/render QA
- bytes: `615252`
- MD5: `c8b810a763b9bb55d076a454df49b413`
- SHA-256: `98d730fb8afaf40149d028bdde0b1c3ba9851f1dbcd15475567e56bb7eb17d3f`
- all 27 pages passed rendered inspection at 150 DPI; the final build has no warnings, undefined
  references, overfull boxes, or underfull boxes
- sole authorship, ORCID, version, reserved DOI, concept DOI, CC-BY-4.0 metadata, and new source
  citation gates pass
- the concept latest resolves to record `21988601`; public version, sole author/ORCID, CC-BY-4.0
  licence, filename, bytes, MD5, and SHA-256 match the committed record
- a fresh unauthenticated public download matches the committed PDF exactly

Version 0.13 public-file verification:

- DOI: `10.5281/zenodo.21995498`; no upload or publication occurred before claim/build/render QA
- bytes: `635617`
- MD5: `d6ce72589100d1f57986da000501fdc7`
- SHA-256: `cc9e721c3f0155181b963095a0b0efcc37e023546b32c6dd61b772a3d30ec7ed`
- all 29 pages passed rendered inspection at 150 DPI; the final build has no warnings, undefined
  references, overfull boxes, or underfull boxes
- sole authorship, ORCID, version, DOI, concept DOI, CC-BY-4.0 metadata, source, and scope gates pass
- the concept latest resolves to record `21995498`; public title, version, sole author/ORCID,
  licence, filename, bytes, MD5, and SHA-256 match the committed record
- a fresh unauthenticated public download matches the committed PDF exactly

Version 0.14 public-file verification:

- DOI: `10.5281/zenodo.22013515`; no publication occurred before claim/build/render QA and exact
  post-upload draft validation
- bytes: `656437`
- MD5: `f5c44834c94832c3c2c8d7d29389ff9a`
- SHA-256: `df5e12d2256f4967881df0f35df44b415777c4826f38447a33cfdeb1b7399e10`
- all 31 pages passed rendered inspection; the final build has no warnings, undefined references,
  overfull boxes, or underfull boxes
- the concept latest resolves to record `22013515`; public title, version, sole author/ORCID,
  CC-BY-4.0 licence, filename, bytes, MD5, and SHA-256 match the committed record
- a fresh unauthenticated public download matches the committed PDF exactly

Version 0.15 public-file verification:

- DOI: `10.5281/zenodo.22016550`; no publication occurred before claim/build/render QA and exact
  post-upload draft validation
- bytes: `674169`
- MD5: `204eb3575d1bebcd95eb25f48bae58cb`
- SHA-256: `e7d3fb747f01b6c44c84ca9c2cf25a746cd2d05eb0996163f4a18e9e3cea1be9`
- all 34 pages passed rendered inspection; the final build has no warnings, undefined references,
  overfull boxes, or underfull boxes
- the concept latest resolves to record `22016550`; public title, version, sole author/ORCID,
  CC-BY-4.0 licence, filename, bytes, MD5, SHA-256, and v0.15 description addendum match
- a fresh unauthenticated public download matches the committed PDF exactly

Version 0.16 public-file verification:

- DOI: `10.5281/zenodo.22029468`; no upload or publication occurred before claim/build/render QA
  and exact post-upload draft validation
- bytes: `691569`
- MD5: `ad69991f41c4f35da3c03f2c1ce343e9`
- SHA-256: `4c2a49ae6e1a959afb8df4a365feb4c815d408f3746b5ef1df14ee5746abd554`
- all 36 pages passed rendered inspection; the final build has no warnings, undefined references,
  overfull boxes, or underfull boxes
- the concept latest resolves to record `22029468`; public title, version, sole author/ORCID,
  CC-BY-4.0 licence, filename, bytes, MD5, SHA-256, and v0.15/v0.16 description addendum match
- a fresh unauthenticated public download matches the committed PDF exactly

Version 0.17 public-file verification:

- DOI: `10.5281/zenodo.22030167`; no upload or publication occurred before claim/build/render QA
  and explicit DOI reservation
- bytes: `714021`
- MD5: `4c7daffba7539f37ea4ecb6d52fad9d9`
- SHA-256: `480f135b9ecf8dbcec0fb91e85491f8fcf11e1e3c7417f6415ebeda366b5d640`
- all 40 pages passed rendered inspection; the final build has no warnings, undefined references,
  overfull boxes, or underfull boxes
- the concept latest resolves to record `22030167`; public title, version, sole author/ORCID,
  CC-BY-4.0 licence, filename, bytes, MD5, SHA-256, and v0.15/v0.16/v0.17 description addendum match
- a fresh unauthenticated public download matches the committed PDF exactly

Version 0.18 prepublication verification:

- reserved DOI: `10.5281/zenodo.22030743`; no upload or publication occurred before claim,
  two-pass build, metadata, authorship, and rendered-page QA
- bytes: `725554`
- MD5: `558532167c4f2a39e03d1bcced9de18d`
- SHA-256: `0e40aa5ed4feb02209137c2982184a93cfd402ac03cc9d4aa6f9ba86ae4327b7`
- all 42 pages passed final rendered inspection at 150 DPI; the final build has no warnings,
  unresolved references, overfull boxes, or underfull boxes
- sole authorship, ORCID, version, DOI, concept DOI, CC BY 4.0, source, attribution, and scope gates
  pass; the exact draft metadata and one-file upload also pass; publication, concept-latest, and
  fresh-download gates remain pending
