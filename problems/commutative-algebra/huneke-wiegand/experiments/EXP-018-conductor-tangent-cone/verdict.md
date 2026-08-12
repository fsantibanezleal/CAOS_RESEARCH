# EXP-018 verdict - CONFIRMED

Run date: 2026-08-12. Exact integer and bitset arithmetic, CPU only.

## Result

For every integer `p>=4`, the tangent cone of the conductor ideal has depth zero:

```text
G_p=gr_(T_p)(R_p),  depth(G_p)=0.
```

Its complete Valabrega--Valla module with respect to `Q_p=t^(4s)R_p` is concentrated in one
degree. The only nonzero component is

```text
(Q_p intersect T_p^2)/(Q_pT_p),
```

whose value classes are exactly

```text
9s+({2p-1,4p-1} union [4p+1,5p-2])
```

and whose length is `p`. Every intersection quotient at `n=0` and `n>=2` vanishes. By the
Valabrega--Valla criterion, `G_p` is not Cohen--Macaulay for every member of the family.

The exact Hilbert series is

```text
H_(G_p)(z)
 = ((p+1)+(9p-1)z+12p z^2+(2p-1)z^3+z^4)/(1-z).
```

All numerator coefficients are positive. This shows that the Hilbert numerator alone conceals the
depth-zero defect.

## Symbolic proof

The proof in `proof.md` is load-bearing. Intersecting the exact EXP-016 square with `v(Q_p)` leaves
one additional level-nine block beyond `Q_pT_p`, of size `p`. The EXP-017 cubic, quartic, and
stabilized profiles prove all later intersection equalities. The criterion's regularity,
superficiality, dimension, and infinite-residue-field hypotheses are stated explicitly.

## Computational and adversarial record

- The mandatory `p=4` smoke gate passed before the campaign artifact was written.
- Both exact routes pass for all 297 parameters `p=4,...,300` in 11.6 seconds.
- A separately written bounded-bitset audit reconstructs `p=4,5,17,73,151,300` and rehashes all
  297 campaign rows.
- Campaign aggregate:
  `9631c644732f0921be3b3027e18a01110f23dad897fbf2cb14dd3a493eda5971`.
- Audit aggregate:
  `7c2abcd290bc3461fc5251bc3372e20a7fa25c888e3b2ed635368b4dda0781ff`.
- `results.json` SHA-256:
  `e2a811bb1986e29a5f09ca3a0705d4d3ff49a5a9118bde0bfb6e2ef621418211`.
- `audit.json` SHA-256:
  `2705894aac3089ce7c311186abbca0c9b7adb234e61395ff8aace8554fd9fb30`.
- Deleted-witness, false-later-defect, perturbed-length, false-Cohen--Macaulay, and altered-Hilbert
  controls are rejected.

## Prediction ledger

- P1 PASS: the unique nonzero intersection quotient has the predicted exact value block.
- P2 PASS: its length is exactly `p`.
- P3 PASS: every other component vanishes, including the stabilized infinite tail.
- P4 PASS: the tangent cone has depth zero and is not Cohen--Macaulay.
- P5 PASS: the exact Hilbert function and rational series match.
- P6 PASS: campaign, independent audit, and corruptions agree.

Verdict: **CONFIRMED**.

## Consequence and scope

This is an exact theorem for the explicit conductor family attached to the CAOS Huneke--Wiegand
counterexamples. It does not assert that conductors or trace ideals generally have non-Cohen--
Macaulay tangent cones, nor does it classify all ideals with reduction number four.

The theorem is a manuscript-worthy structural extension, but it does not by itself force an
immediate Zenodo version. Publication remains conditional on claim-audit, clean build, full render,
metadata, sole-human-authorship, and immutable-download verification.

## How could this be wrong?

The proof depends on the corrected EXP-013/016 value sets and EXP-017 stabilization. The finite
sweep cannot replace those formulas. The Valabrega--Valla implication uses that `Q_p` is generated
by a superficial regular element in a one-dimensional Cohen--Macaulay local ring with infinite
residue field. The result has not been journal peer reviewed or formalized in a proof assistant.
