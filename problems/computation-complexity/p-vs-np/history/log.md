# p-vs-np history

## 2026-11-24 - opened

- Path map from a delegated dossier (18 rows, 11 cross-field) and the decision of the Millennium review, Section 9.
- Primary sources read by the coordinating session: the official description; the Anthropic artifact (README,
  `Statement.lean`, the paper's pages 4 to 11, 29 to 31, 56, 57, 60, 61); three arXiv abstracts on the algorithms of
  October 2026. Copies with SHA-256 under the data root.
- One candidate unit dropped after a search: the circuit lower bound that follows from the algorithms is already
  written by others.
- PNP-001 written. One error found by its writer before the commit: a claimed equivalence by duality between "no
  conversion shortens the metric" and "the metric is a price"; prices are not a convex set, so only one direction
  holds. The sentence in the path map was corrected in the same change.
- EXP-001 run and closed, CONFIRMED. Its script was run before its hypothesis file was written; the hypothesis file
  says so and records which values had been computed by hand beforehand.
- PNP-001 reviewed by a reader other than the writer (reviewer on opus): correct after fixes. Two blockers: the
  extension of the contracting case was stated over every field and holds over F_2 only (the paper's reduction puts
  each clause weight minus one into the matrix, so the entries -1 and a - 1 appear; the coordinating session read
  page 32 again and confirmed it); a sentence said that the top of the ladder does not follow from NP not inside
  P/poly, and it does (Valiant and Vazirani). Two major and eight minor findings. All applied the same day.
- PNP-006 proved: maps of Mat_mu(F_2) into a Hilbert space contract with the constant 2 - 2^(1-mu), for every mu.
  EXP-002 CONFIRMED.
- PNP-003, first step (delegated reading): nothing in the paper's Appendices A to C or in the literature read settles
  whether the Euclidean unit square is a price on four parties.
