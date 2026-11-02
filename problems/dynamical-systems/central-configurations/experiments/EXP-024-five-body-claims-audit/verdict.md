# EXP-024 verdict: CONFIRMED (statement faithful; no kernel bypass in any stored or generated source)

Date: 2026-11-02. Hypothesis frozen at `1270529a` before the scan was written.

## Result

Tomar's Lean theorem `CC5Full.Core.Compose.MainTheorem_holds : CC5Full.MainTheorem` states exactly the
classical claim: for every positive mass vector, the planar Newtonian five-body problem has finitely many
central configurations up to similarity (P1). No stored source of the formalization in `CC5Full` and none
of the 85,756 generated modules contains a construct that bypasses the kernel (P2). The audit does not
rebuild the proof; the author reports a full build of about 863 CPU-hours and acceptance of the closure by
two independent kernels (nanoda, lean4lean), which we did not reproduce.

## P1: the statement (PASS)

Read in `CC5Full/System.lean` and `CC5Full/Basic.lean` of the stored archive:

- `Masses := Fin 5 -> R`; `Conf := Fin 5 -> C` (planar configurations).
- `CollisionFree q`: pairwise distinct points.
- `IsCC m q`: collision free and there are `lam : R`, `c : C` with
  `lam m_i (q_i - c) = sum_{j != i} m_i m_j (q_i - q_j) / |q_i - q_j|^3` for every `i`. This is the
  Newtonian central-configuration equation with exponent 3; the sign of the force is absorbed by `lam`.
  The value `lam = 0` admits no configuration for positive masses (it would be an equilibrium, which the
  virial identity excludes), so allowing it adds nothing.
- `Similar q q'`: `q' = a q + b` or `q' = a conj(q) + b` with `a != 0`: every similarity of the plane,
  reflections included.
- `FinitelyManyCC m`: a finite set of configurations such that every central configuration is similar to
  one of them, that is, finitely many similarity classes.
- `MainTheorem := forall m, (forall i, 0 < m i) -> FinitelyManyCC m`, and `MainTheorem_holds : MainTheorem`
  in `CC5Full/Core/Compose/Main.lean` has no hypotheses.

Deviation list: none affecting the content. Counting up to all similarities rather than up to rotations,
dilations and translations only changes counts by a factor of at most two, not finiteness.

## P2: static scan (PASS)

- Stored archive `cc50-rung2-lean_full.tar.xz` (SHA-256 matches the supplement): 2,751 `.lean` files scanned
  with comments stripped. Three hits, all `unsafe` in `tools/kernel2/kexport3` (the exporter used to feed the
  independent kernels), none in `CC5Full`.
- Generated families (`D14a/B`, `ResidualCert/All`, `E3/Run`, `Strata/Big/F1_2_3_4_5`; each archive's SHA-256
  matches the supplement): 85,756 `.lean` files, about 3.0 GB, raw search including comments: zero files with
  any of `sorry`, `admit`, an `axiom` declaration, `native_decide`, `implemented_by`, `@[extern`,
  `ofReduceBool`, `unsafe`, `skipKernelTC`.

## P3: dependency boundary (PASS)

`Main.lean` imports `Compose.Assembly`, `Compose.MainAssembly` and `E3.Run.Final`, all present. The parts that
live only in generated families are the four archives above, now scanned. Not covered by this audit: the
kernel check itself, the correctness of the paper's mathematics outside what the kernel checks, and the
non-Lean computations of the supplement (Singular, msolve, Macaulay2 runs).

## Consequence

The Lean statement is the right theorem and its sources are clean, so planar five-body finiteness for all
positive masses (Smale's sixth problem for n = 5) rests, as formalized, on the Lean kernel. The CAOS n = 5
programme (tropical replication, the certified cross-family atlas) is superseded as a route to that theorem;
priority belongs to Tomar, Chen and Tong, and Liu and Liu. The open window is n = 6.

Artifacts: `artifacts/scan.json`; the scanner `scan.py`.
