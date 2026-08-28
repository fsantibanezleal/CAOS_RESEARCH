# Claim audit - manuscript v0.21

Date: 2026-08-27. Publication status: validated candidate reserved at DOI
`10.5281/zenodo.22135689`; upload and publication are pending.

## Claim-to-evidence matrix

| claim or boundary | primary evidence | audit status |
|---|---|---|
| discovery priority | Pham public repository and recorded Huneke verification | PASS; CAOS does not claim discovery of the original counterexample |
| imported kernel structure | EXP-033 exact sequence, offset bases, Hilbert series, and regular element | PASS; reduction modulo `X_0` preserves the sequence and minimal Betti numbers |
| two-layer Artinian kernel | EXP-034 proof and independent semigroup reconstruction | PASS; the layers have offset bases `H_p` and `B_p`, dimensions `8p` and `10p`, and the degree-two layer is socle |
| incidence reduction | EXP-034 integral Koszul differential | PASS; the two unresolved kernel strands are kernels and cokernels of the displayed incidence maps |
| primitive minimum-offset cell | representation-set identity `R_(8p-1)={1,...,p}` | PASS; the selected cokernel component is free of rank one over the integers |
| connecting-map exclusion | unique low source and the nonzero `X_pX_l` unit coordinate | PASS; no source cycle can hit the distinguished kernel class |
| exact survival in `A_p` | long exact Tor sequence and the EXP-032 row-two start at `2p-2>p` | PASS; `beta_(p,(p+2,tau_p))(A_p)=1` over every field |
| exact survival in `C_p` | EXP-033 minimal multigraded cone and gap `(p-2)(6p-1)>0` | PASS; `beta_(p,(p+2,tau_p))(C_p)=1` over every field |
| ordinary lower bounds | offset summation and the shifted high-variable diagonal | PASS; `beta_(p,p+2)(A_p)>=1` and `beta_(p,p+2)(C_p)>=binom(8p,p-1)+1` |
| finite validation | EXP-034 canonical, rank, independent, and symbolic artifacts | PASS; 297 canonical rows, two-field rank probes, independent reconstruction, and symbolic exclusions agree |
| scope | EXP-034 verdict and manuscript scope section | PASS; one exact lower-strand point is proved, not either complete lower strand or the full resolution |
| manuscript split decision | EXP-034 preflight and verdict | PASS; the theorem directly continues the v0.20 kernel and mapping-cone narrative and belongs in the main manuscript |
| publication identity | reserved Zenodo record `22135689`, metadata JSON, and page-one block | PASS locally; version, DOI, concept DOI, date, CC BY 4.0, sole author, and sole ORCID agree |

## Evidence identities

- canonical aggregate:
  `65ef176dcd9f5bd5467c09e763fdb20c67798de9743443ce5d0e34958c1645ce`;
- finite-rank aggregate:
  `31d70c09d251bb6009b610be05c33a42ccd50e417b84aff2c0db561018e6acc5`;
- independent-audit aggregate:
  `31479abd3c7247fe0ba464eefe06e437a595812c3d6055d0de8d0ced25d12794`;
- symbolic aggregate:
  `b3f461298706a394cc0f1a296557e10f52435f78d2f1039452fb726871b79a4d`;
- canonical artifact SHA-256:
  `6df7f70cab4f16f207288dd29dc06658a153629b0fda4c9ff05335e10d602b61`;
- independent artifact SHA-256:
  `b1c433d600a4d9f03d47c61589302ebabdfb52fff7442fb72850de8a7e1ef9f9`;
- symbolic artifact SHA-256:
  `f8c5178ace6d4e3c3740677a90b97e8d1e476855556f5ad36b30485da486f7ee`.

## Proof boundary

The result is deductive. The finite campaigns validate the bases, incidence implementation, unit
pivots, interval exclusions, frozen premises, and adversarial controls; they do not replace the
proof. The proof imports the EXP-030/032/033 canonical idealization, colon Betti polynomial,
regular-element, kernel-basis, exact-sequence, and minimal-cone theorems. Within that boundary it
uses regular reduction, a two-layer Koszul complex, a primitive minimum-offset cokernel cell, an
integral unit boundary, and long exact Tor sequences. Z3 only checks negations of elementary
interval identities and is not a proof dependency.

The result determines one exact multigraded point in the regularity-two strand and supplies new
ordinary lower bounds. It does not determine either complete lower strand, explicit differential
matrices, or the full minimal resolution of the conductor special fiber.

## Publication gates

- claim-to-evidence, attribution, and scope audit: PASS;
- two consecutive stable LaTeX builds: PASS; no LaTeX/package warnings, unresolved references,
  overfull boxes, or underfull boxes in either retained v0.21 log;
- PDF metadata, extraction, page count, hashes, and all-page rendered inspection: PASS; all 48 pages
  inspected at 150 DPI, with full-size inspection of page one and pages 41--48 containing the
  imported theorem, new theorem and proof, trust boundary, scope, and references; 792,863 bytes,
  MD5 `13b92773205a49977abb88cd7ab8dde1`, SHA-256
  `c717fbb4d6d3178e0fb0786a8a61c9e2c109d97d77a7b9e1308a2274c0f97539`;
- sole-author and sole-ORCID audit: PASS; Felipe Santibanez-Leal is the sole author and
  `0000-0002-0150-3246` is the sole ORCID; no machine authorship or coauthorship appears;
- repository tests, pipeline, and artifact consistency: PENDING;
- exact Zenodo metadata and one-file upload validation: PENDING;
- publication, concept-latest check, and fresh unauthenticated download: PENDING.

The manuscript candidate is frozen for repository gates and exact Zenodo upload. Publication is
not yet claimed.
