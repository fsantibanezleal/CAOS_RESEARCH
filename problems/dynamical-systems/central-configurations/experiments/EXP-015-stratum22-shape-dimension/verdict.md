# EXP-015 - Verdict: CONFIRMED ON ALL PREDICTIONS (2026-08-01; the stratum's shape variety has dimension 5 ungauged and 4 gauged, in one second each; stage (i) of the Dias-Pan pipeline is done for k = 2, p = 2)

Hypothesis: `hypothesis.md` (declared before any run). Runner: `run.py`
(smoke fixed once before any solver time: the first evaluator wrongly
demanded all-even exponents, tripping on E1's odd wA*wB term; replaced by
exact sqrt substitution, commit 335d7bf; the failed first invocation spent
zero Singular seconds). Artifacts: `artifacts/`.

## Outcomes

| Prediction | Outcome | Facts |
|---|---|---|
| Smoke (exact rational witness ON, perturbed OFF) | PASS | the (3, -1, 2, 1, 1, -2) geometry gives exact zeros on E1..E5 via sqrt substitution (pure exact arithmetic; the odd term wA*wB is rational at this witness by construction); the cx-perturbed tuple violates |
| P1 (cost) | CONFIRMED, emphatically | both Singular runs completed in about ONE second each against 300 s caps: the twice-measured cost law (sparse quadratic/quartic realizability equations, no Cayley-Menger monsters) holds exactly |
| P2 (ungauged dimension = 5) | CONFIRMED, two-way agreement | our staircase 5, Singular dim() 5 |
| P3 (gauged dimension = 4, adjoining r12 = 1) | CONFIRMED, two-way agreement | our staircase 4, Singular dim() 4; the exact analogue of Dias-Pan's dim(E) = 4 for the cross stratum |

## What this establishes for the campaign

Stage (i) of the Dias-Pan pipeline for the k = 2, p = 2 stratum is COMPLETE:
the gauged shape variety has dimension 4 (and the ghost sign branches
introduced by chain-squaring do NOT raise the top dimension, since 4 is
exactly the parametrization count; had ghosts dominated, the dimension would
have exceeded it). The campaign arithmetic is therefore the exact sibling of
Dias-Pan Section 7: with the four mass unknowns (m1, m2, mA, mB) after the
pair-equality lemma, the fiber inequality reads dim_P(fiber) <=
4 - rank(dL/dm at P) over the 6 x 4 mass-coefficient matrix of the reduced
block {L13, L15, L23, L25, L35, L36}, and the case split over
dim(projection) in {0..4} with determinantal loci Delta_k plus one rank-4
witness closes dim(Omega_stratum) <= 4 = the mass count, which is generic
finiteness for the stratum (off the q = v sub-stratum, which the campaign
scope excludes explicitly until its own lemma is settled).

Next declarations, in order: EXP-016 = the rank analysis (build the 6 x 4
mass-coefficient matrix in the quotient distance variables exactly, push the
order-k minors to distance-only form, and run the Dias-Pan Lemma 7.3/7.5
pattern with our validated engines); EXP-017 = the witness (an explicit
stratum central configuration with exact rank-4 certificate, our
census/eliminant machinery). A completed chain would be the stratum theorem;
its statement wording goes to Felipe BEFORE anything leaves the repo.

## Soundness notes

- Both dimension readings agree with Singular's own dim() on both runs; the
  parser and order conventions are the EXP-012-validated ones.
- The cut is an overvariety (ghost sign branches); a dimension EQUAL to the
  parametrization count certifies that ghosts do not dominate the top; lower
  strata ghosts are irrelevant to the fiber-dimension argument.
- The smoke evaluator bug was caught by the gate itself before any solver
  time, fixed in one commit, and is recorded here rather than hidden.
