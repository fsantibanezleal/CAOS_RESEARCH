# EXP-015 - Verdict: CONFIRMED (2026-07-21)

Artifacts: `tests/test_jc2_checker.py` (pytest green; runs in CI permanently), module
`code/jclib/jc2.py`.

## Shipped

1. **The JC(2) certificate checker.** `check_keller2(P, Q)` returns an exact machine-readable
   verdict (Keller or not, with the reason); `check_collision2(P, Q, p1, p2)` decides a claimed
   disproof certificate exactly (distinct points, equal images, constant nonzero determinant),
   answering with the reason on rejection. This is the neutral verdict format for any future
   search output, ours or external.
2. **The m = 1 bridge extractor.** `bridge_extract(f1, f2, f3, X1, X2)` executes EXP-012's
   bridge: from reduced class data over weights (1, -1, -1) and two claimed colliding 3D
   points, it constructs the reduced planar pair (V', T') = (f1 f3, f2 f3) and hands the
   induced planar points to the checker; 3D points with equal invariants are refused (nothing
   to extract). The pipeline is demonstrated end to end on synthetic data WITHOUT any existence
   claim.

## Verified behavior (pytest)

- Accepts a genuine automorphism as Keller; rejects a non-Keller pair; rejects fake collisions
  with the exact reason (images differ / points equal).
- The extractor produces a checkable planar pair from formal data and refuses degenerate input.

## How could this be wrong?

- The tools decide certificates; they prove nothing about existence. The bridge direction
  implemented is: 3D m = 1 collision gives a planar counterexample; the converse embedding is
  not needed for the disproof direction and is not claimed.

## Consequences

- Any candidate from the queued searches (Puiseux inverse design, wider bilinear scans, or the
  m = 1 class) now has a one-call exact adjudication path, wired into CI.
