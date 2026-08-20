# Claim audit - manuscript v0.18

Date: 2026-08-20. Publication status: DOI reserved; upload and publication are blocked until every
prepublication gate below passes.

## Claim-to-evidence matrix

| claim or boundary | primary evidence | audit status |
|---|---|---|
| discovery priority | Pham public repository and recorded Huneke verification | PASS; CAOS does not claim the original counterexample discovery |
| imported degree-four strand | EXP-027 proof and verdict | PASS; exact formula and integral freeness unchanged |
| imported degree-five strand | EXP-029 proof and verdict | PASS; exact pair basis and formula unchanged |
| imported degree-six strand | EXP-030 proof, verdict, and corrected audit | PASS; exact support and formula unchanged |
| degree-seven residual sets | EXP-031 proof and symbolic certificate | PASS; `E_(p,5)=E_(p,4)` is full and `E_(p,3)` has only hole `6p-1` |
| integral degree-seven vanishing | EXP-031 zero-vertex matching and signed filler block | PASS; `beta_(3,(7,b))=0` for every offset, parameter, and field |
| complete third row | EXP-027/029/030/031 plus minimum shift and regularity four | PASS; the only allowed shifts are four through seven and all are determined |
| total third Betti rank | exact sum of the three nonzero formulas | PASS; `p(7500p^3-7988p^2+2025p-133)/6` |
| finite validation | EXP-031 results, independent audit, and symbolic certificate | PASS; exact small profiles, opposite filler order, and 297 arithmetic rows agree |
| corrected failed attempt | `attempt-1-global-filler-key.json` | PASS; retained as `INVALID_IMPLEMENTATION` and excluded from evidence |
| scope | EXP-031 verdict and manuscript scope section | PASS; higher rows, full table, full resolution, and general classification remain open |
| manuscript split decision | EXP-031 verdict | PASS; the adjacent final third-row strand belongs in this existing manuscript |
| reserved publication identity | Zenodo draft `22030743` and page-one block | PASS before upload; version `0.18`, DOI `10.5281/zenodo.22030743`, concept DOI, date, CC BY 4.0, and sole author/ORCID agree |

## Evidence identities

- canonical aggregate:
  `d68afbb5c54ebb86abbf420c389e1cacf666071cb35f83e5d2b67eccbc354858`;
- independent-audit aggregate:
  `0be4b659126064328b5ef14a40e488a836f874d2eed9b048d4d3f19da971346e`;
- symbolic aggregate:
  `e4bf2e0ae303e905efc9f985b239d059a5255b02d2ddc1d37abab5cc5cb2fc1f`;
- complete exact profiles: 374 offsets at `p=4` over `GF(2)` and `GF(1000003)`, and 470
  offsets at `p=5` over `GF(2)`, all with integral-homology rank zero;
- canonical and independently ordered unit fillers: all critical triangles for `p=4,...,12`;
- residual and arithmetic certificate: all 297 parameters `p=4,...,300`.

## Proof boundary

The all-parameter result is deductive. Characteristic independence follows from an integral acyclic
matching and a signed identity block, not from agreement over two finite fields. The exact campaigns
test the implementation and arithmetic reductions but do not replace the written proof. EXP-023's
previously disclosed Presburger solver boundary remains inherited by the defining-ideal premise;
EXP-031 introduces no new solver dependency.

The result determines the third homological row only for the conductor special fibers in the
explicit EXP-009 family. It does not determine the higher rows, full Betti table, full minimal
resolution, or classify arbitrary Huneke--Wiegand counterexamples.

## Prepublication gates

- source standards, structure, Ruff, and repository test suite: PASS;
- two-pass LaTeX build with no warnings, unresolved references, or box warnings: PASS;
- page count, PDF hashes, and metadata inspection: PASS; 42 pages and 725,554 bytes, MD5
  `558532167c4f2a39e03d1bcced9de18d`, SHA-256
  `0e40aa5ed4feb02209137c2982184a93cfd402ac03cc9d4aa6f9ba86ae4327b7`;
- all-page rendered visual inspection: PASS; all 42 final pages inspected at 150 DPI, with full-size
  inspection of the front matter and new theorem/trust/scope pages;
- sole-author and ORCID audit: PASS; Felipe Santibanez-Leal is the sole author and
  `0000-0002-0150-3246` is the sole ORCID; no machine authorship or coauthorship appears;
- exact Zenodo draft metadata/file validation: PASS; draft `22030743` reports version `0.18`, the
  reserved DOI, one creator with the sole ORCID, the v0.18 description, and exactly one committed
  file with the expected filename, 725,554 bytes, and MD5;
- publication, concept-latest check, and fresh unauthenticated download: PENDING.

Publication is now authorized by the completed prepublication and exact-draft gates. The public
concept-latest and fresh-download gates remain mandatory after publication.
