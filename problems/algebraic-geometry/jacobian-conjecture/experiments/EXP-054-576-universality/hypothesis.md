# EXP-054 - Universality of the 576 certificate (route N2, the closure step)

- **Question.** Is the EXP-053 certificate universal over ALL lower coefficients of the
  reduced P (every lattice point of N(P) below the forced top edge, including the
  (8,14) corner and the normalized (1,0))? If yes, the reduced (72, 108) system is
  EMPTY for the whole forced-top-edge stratum, and the case closes modulo the dossier's
  edge-forcing transcription.
- **Motivation (the declared derivation).** Lambda is supported on five rows
  S = {(2,0), (9,16), (16,32), (17,33), (18,34)}. A symbolic coefficient eps at a lower
  lattice point (p, q) perturbs Lambda^T M only via columns (alpha, beta) =
  s - (p, q) + (1, 1) for s in S, each with bracket factor (p beta - q alpha).
  Universality is therefore the FINITE check: for every (p, q) in N(P) off the top edge
  and every s in S, either (alpha, beta) lies outside the Q polygon or
  p beta - q alpha = 0. If it passes, Lambda^T M = 0 holds identically in ALL lower
  coefficients (and in t, already verified), so the pairing stays 576 and the system is
  inconsistent for EVERY P on the stratum: no pair with [P, Q] = x^2 exists there.
- **Falsifiable predictions.**
  1. [MV] (Lambda extracted) The bare-stratum certificate is recomputed and its five
     entries recorded exactly.
  2. [MV] (THE FINITE CHECK) All (p, q) x S combinations pass (column outside the
     polygon or vanishing bracket factor): the certificate is UNIVERSAL.
  3. [MV] (Adversarial confirmation) Two samples with (8,14) != 0 and dense lower
     terms: pairing still 576.
  4. [D] (Assembly) With 2: the reduced system is empty on the entire
     forced-top-edge stratum; what remains for the full (72, 108) closure is exactly
     the dossier's remaining forcing branches (normalizations; the optional (0,8)
     corner variant), stated for the next round; if those close, the JC(2) floor
     rises to 125.
- **Method.** sympy over QQ(t) for the certificate; pure lattice combinatorics for the
  check; caps 570 s.
- **Success criterion.** 1-3 verified; 4 stated.
- **Failure criterion.** A failing combination in 2 with nonzero bracket factor and
  in-polygon column: the certificate is NOT universal there; identify which lower
  monomials break it and whether a corrected covector exists (the honest fallback).

Declared 2026-07-22 before the run.
