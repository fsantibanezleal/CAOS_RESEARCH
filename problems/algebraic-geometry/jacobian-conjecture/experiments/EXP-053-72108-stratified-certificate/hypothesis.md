# EXP-053 - The stratified certificate on the reduced (72, 108) system (route N2, decisive)

- **Question.** JCB-040. EXP-052 showed sampled emptiness of the reduced open case
  ([P, Q] = x^2 on the Prop 4.3 polygons). The full closure needs certificates over ALL
  P; a raw 61-parameter elimination is intractable. Can the STRATIFIED attack (the
  forced top-edge structure symbolic, lower coefficients swept) produce the first
  parametrized certificates?
- **Motivation (derivation, declared).** The GGHV reduction forces the top edge of the
  reduced P: the (0,8)-(8,16) edge carries a form of the shape y^8 (xy - t)^8 (the
  dossier's edge data up to normalization; t the structural parameter). The bracket
  [P, Q] = x^2 is linear in Q, and the certificate machinery applies verbatim with the
  rhs on the x^2 row. Efficiency: the half-plane restriction adapts (threshold moved to
  contain the x^2 row: H = {i - j <= 2}); columns with empty H-part drop out. If a
  cleared covector exists with pairing a nonzero polynomial in t alone for each sampled
  lower stratum, the open case is closed on those strata for ALL t: the first
  parametrized certificates on the last open pair below 125.
- **Falsifiable predictions.**
  1. [MV] (H-shrink) The H-restricted reduced system ({i - j <= 2} rows) is
     substantially smaller than the full one and still carries the x^2 row.
  2. [MV] (The stratified certificate) For P = y^8 (xy - t)^8 + x + (sampled lower
     terms), a cleared covector with c^T M = 0 identically in t exists with pairing a
     NONZERO polynomial in t: emptiness for ALL t on the sampled stratum (at least the
     bare stratum x + top; then two lower-term samples).
  3. [MV] (Support economy) The certificate's support row set is recorded; if it avoids
     the rows where generic lower coefficients enter, the pairing is lower-free on
     those rows (measured; feeds the all-lower argument).
  4. [D] (What remains) The precise gap to full closure is stated: the sweep over the
     remaining forced-structure parameters and the lower-coefficient generality
     (tower/annihilation-style), mapped onto our existing lemmas.
- **Method.** sympy over QQ(t); H-restricted cleared certificates; caps 570 s per part
  (degrade to smaller H or numeric t-grids before capping; any degradation recorded).
- **Success criterion.** 1-2 verified: the first all-t certificates at the open pair's
  reduced system; 3-4 recorded.
- **Failure criterion.** Nullspace intractable even H-restricted (record timings;
  fall back to t-grids and state the sound-but-sampled result); a pairing vanishing
  identically in t (the stratum escapes this certificate: investigate before any
  claim).

Declared 2026-07-22 before the run.
