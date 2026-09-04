# EXP-051 hypothesis - minimum-complexity unreduced Bockstein lifts

Date: 2026-09-03. Status at declaration: **DECLARED, NOT RUN**. CPU-only exact integer and binary
arithmetic.

## Question

Does each stable completion admit a simple exact rank-two basis before the Bockstein classes are
forced into the canonical EXP-048 quotient section?

For every binary kernel-basis cycle `z`, compute `b=Rz/2`, reduce `b mod 2` only to identify its
quotient class, and retain the minimum-complexity pair whose classes are independent.

## Predictions fixed before computation

- **P1 (small exact boundaries):** each completion and each `p=8,...,11` has a selected spanning
  pair with `Rz=2b`, `support(b)<=8p`, and `max_abs(b)<=2`.
- **P2 (small binary cycles):** every selected `z` has support at most `4p`; its coefficients are
  automatically zero or one.
- **P3 (stable size laws):** after sorting the selected pair by boundary support, both boundary
  support series and both cycle support series are integer-affine functions of `p` within each
  inclusion.

## Method

1. Verify frozen EXP-047 through EXP-050 hashes.
2. Build the image RREF and the deterministic binary kernel basis of each compact relative matrix.
3. For every kernel cycle, require an even integer boundary, divide by two, and reduce only its
   parity class modulo the image.
4. Keep the best exact candidate per nonzero quotient class under
   `(support(b),max_abs(b),support(z),hash(z))`, then choose the best independent pair.
5. Verify `Rz=2b` directly. Repeat with reversed relation order and high pivots; require an
   independent pair satisfying P1/P2 bounds even if its representatives differ.

## One-sidedness

- A **PASS of P1/P2** supplies finite exact torsion representatives dramatically simpler than the
  corrected canonical section. It does not prove a uniform formula or upper bound.
- A **FAIL of P1/P2** refutes the declared complexity bounds for these deterministic kernel bases,
  not for every possible integral basis.
- A **PASS of P3** supplies a finite size law only. A **FAIL** redirects semantic extraction to
  the actual row labels rather than extrapolating from counts.

## Premises, invariant, and budget

Premises are EXP-047 CONFIRMED FINITELY, EXP-048 retained rank-two classes, EXP-049 retained duals,
and EXP-050 P1 finite exact corrected representatives. The invariant is divided-boundary
complexity before quotient normalization. The full run is capped at 60 seconds and 4 GiB with
per-inclusion checkpoints. Hash, parity, rank, or exact-identity failures stop the run. A budget
stop is inconclusive.

No manuscript or Zenodo update is authorized by declaration.
