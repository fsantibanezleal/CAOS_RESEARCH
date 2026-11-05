# EXP-024 hypothesis: statement and source audit of the claimed five-body finiteness

Date: 2026-11-02. Frozen before the scan script is written or run.

## Source preflight

- Tomar, arXiv:2610.13100 (v1 2026-10-09, v2 2026-10-15), and its supplement Zenodo record 23202861
  (v1.0, 2026-10-09), held outside git in the data root under
  `caos-research/central-configurations/sources/tomar-23202861/`; the Lean archive
  `cc50-rung2-lean_full.tar.xz` matches its listed SHA-256
  `3ea1feef89003fa9844f5b2a42a70a25374c9644a7e166d01b6872c128e32bed` (2751 `.lean` files, toolchain
  `leanprover/lean4:v4.35.0-rc3`). The README states that a full rebuild of the generated families takes
  about 863 CPU-hours and that two independent kernels (nanoda, lean4lean) accepted the closure.
- Chen and Tong, arXiv:2610.16107 (v4 2026-10-29), and Liu and Liu, arXiv:2610.28168, claim the same theorem
  without Lean.
- Read so far: `CC5Full/System.lean` (definitions of `IsCC`, `Similar`, `FinitelyManyCC`, `MainTheorem`) and
  `CC5Full/Core/Compose/Main.lean` (`MainTheorem_holds`).

## Question

Does Tomar's Lean statement `MainTheorem` say exactly that the planar Newtonian five-body problem has
finitely many central configurations up to similarity for every positive mass vector, and do the stored
Lean sources contain any construct that would let a proof bypass the kernel?

## Predictions

- P1 (statement): `MainTheorem`, `FinitelyManyCC`, `Similar`, `IsCC`, `CollisionFree` and `Masses` together
  state the classical theorem: planar configurations in `C`, collision free, Newtonian force law with
  exponent 3 in the denominator, a real multiplier and a centre, all similarities of the plane, finitely
  many classes, for all positive masses. Any deviation is listed with its effect.
- P2 (static scan): no stored `.lean` file of `lean_full` contains `sorry`, `admit`, a user `axiom`
  declaration, `native_decide`, `implemented_by`, `@[extern`, `ofReduceBool`, `unsafe`, or
  `Lean.ofReduceBool`, outside comments; the scan reports every hit with file and line.
- P3 (dependency boundary): the theorems that `MainTheorem_holds` composes are located in the stored sources
  (files and declarations named), and the parts that live only in the generated families (not in the
  stored sources) are listed, so that the audit states exactly what it does not cover.

## What PASS and FAIL prove

PASS shows that the claimed Lean theorem is the right statement and that the stored sources carry no
kernel bypass; it does not replace the rebuild, which this audit does not perform, nor a check of the
generated families. FAIL locates a statement deviation or a bypass, either of which would void the claim as
formalized.

## Budget

Minutes; reading and text scanning only.
