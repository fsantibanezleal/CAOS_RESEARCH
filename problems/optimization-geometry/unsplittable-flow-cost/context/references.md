# References: unsplittable-flow-cost

Primary sources for this problem, with verification tags. [VERIFIED] = we read the source
itself (held on disk, hashed below). [PARTIAL] = read at abstract or statement level only.
[UNVERIFIED] = not read by us; its content is reported by a source we did read, and no
conclusion in this programme may depend on it until it is upgraded.

## Core

| Key | Reference | DOI / arXiv | Tag |
|---|---|---|---|
| DGG99 | Y. Dinitz, N. Garg, M. X. Goemans, "On the single-source unsplittable flow problem", Combinatorica 19(1) (1999) 17-41 (FOCS 1998) | 10.1007/s004930050043 | [UNVERIFIED] (paywalled; theorem statement verified via three independent transcriptions) |
| TVZ24 | V. Traub, L. Vargas Koch, R. Zenklusen, "Single-Source Unsplittable Flows in Planar Graphs" | arXiv:2308.02651v1; journal: Math. Prog., 10.1007/s10107-026-02365-x ("planar and bounded-genus graphs") | [VERIFIED] (full LaTeX source read at statement level) |
| MSW25 | M. Majthoub Almoghrabi, M. Skutella, P. Warode, "Integer and Unsplittable Multiflows in Series-Parallel Digraphs" | arXiv:2412.05182v2; IPCO 2025, 10.1007/978-3-031-93112-3_31; Math. Prog., 10.1007/s10107-026-02392-8 | [VERIFIED] (pp. 0-2) |
| STVZ25 | C. Swamy, V. Traub, L. Vargas Koch, R. Zenklusen, "Unsplittable Cost Flows from Unweighted Error-Bounded Variants" | arXiv:2510.21287v1 | [VERIFIED] (pp. 1-6: all conjecture statements, Thm 1.6, Thm 1.7, related work) |
| SV15 | F. B. Shepherd, A. Vetta, "The Inapproximability of Maximum Single-Sink Unsplittable, Priority and Confluent Flow Problems" | arXiv:1504.00627 | [PARTIAL] (abstract) |

## Cited by the core, not yet read (upgrade targets)

| Key | Reference | Where it is used | Tag |
|---|---|---|---|
| Sku02 | M. Skutella, "Approximating the single source unsplittable min-cost flow problem", Math. Prog. 91 (2002) | Goemans' conjecture for demands that are multiples of one another | [UNVERIFIED] |
| MS22 | A. Morell, M. Skutella, "Single source unsplittable flows with arc-wise lower and upper bounds" | Conjectures 1.3 and 1.4; the lower-bound theorem | [UNVERIFIED] |
| MSS07 | Martens, Salazar, Skutella, "Convex combinations of single source unsplittable flows", ESA 2007, 10.1007/978-3-540-75520-3_36 | the equivalence of the cost form and the convex-combination form | [UNVERIFIED], and load-bearing: UFB-003 |
| LS18 | Linhares, Swamy, chain-constrained spanning trees | the technique STVZ25 generalises | [UNVERIFIED] |
| KS02 | Kolliopoulos, Stein, "Approximation algorithms for single-source unsplittable flow" | the flow-augmentation method behind Sku02 | [UNVERIFIED] |
| Kol07 | Kolliopoulos, survey on unsplittable flow | orientation | [UNVERIFIED] |

## The 2026 claimed refutation (non-peer-reviewed)

All [CLAIMED]; provenance, hashes and adjudication rule in
`2026-07-24-claimed-counterexample-dossier.md`. Sources seen: the X announcement (via
threadnavigator mirror of status 2079904005652893709), mathlab.drummerduck.com,
vibemathed.com, windowsnews.ai, digg.com, officechai.com, finance.biggo.com, plus the
proposer artifact bundle supplied by Felipe (instance JSON, verifier, LaTeX certificate,
SVG, model transcript). No primary mathematical venue, no arXiv preprint found as of
2026-07-24.

## Local source archive

`E:\_Datos\caos-research\unsplittable-flow-cost\sources\` (SHA-256):

- `2510.21287.pdf` `ac1e6aab37fe999a32e46c3b2fefbb012b0c2d20ef75f335c1e375d8a71feb38`
- `2412.05182.pdf` `cb989d7544dc2f50ed03dcc65f0f1e31c3565dbcb5c44ec2e5e07917524c776a`
- `1504.00627.pdf` `216984831dd4eecd3516c260259ff25e8df057ede4db06aaed63f5f60c93b7c1`
- arXiv:2308.02651 source tree at `E:\_Temp\ufc-sources\2308.02651\` (from the bundle
  tarball, hash in the counterexample dossier)

Claimed-counterexample bundle hashes: see the counterexample dossier, section 1.
