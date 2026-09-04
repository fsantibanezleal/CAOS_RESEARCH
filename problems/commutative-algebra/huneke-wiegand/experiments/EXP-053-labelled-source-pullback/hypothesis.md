# EXP-053 hypothesis - labelled source pullback

Date declared: 2026-09-04. Status before computation: **DECLARED**.

## Question

Do the two HNF-kernel coordinates behind the EXP-052 exact boundaries pull back to a simple,
parameter-compatible chain in the original labelled source complex?

## Frozen predictions

- **P1 (exact reconstruction):** for `p=8,9,10`, independently reconstruct the labelled component,
  identify every frozen matrix column with an original source or kernel-domain label, rebuild the
  saturated kernel, and recover the stored two-column EXP-051 cycle and `Rz=2b` identity exactly.
- **P2 (structural compression):** after summing the two selected saturated-kernel rows, the
  original labelled chain has coefficients bounded by four and at most twelve
  coefficient-sensitive semantic skeletons in each stable completion.
- **P3 (holdout gate):** only if a complete source-chain formula is frozen from `p=8,9,10`, open
  untouched labelled source data at `p=11` and require exact equality of the complete
  coefficient-label multiset and direct source/target boundaries.

P2 is intentionally falsifiable. If it fails, persist the coefficient/support obstruction and
redirect away from HNF pullback toward a direct chain whose image is the already-frozen EXP-052
boundary. Do not compute `p=12` as a substitute for a symbolic source identity.

## Independence and budgets

The extractor must rebuild exact labels from the frozen EXP-042 matrix rather than trust HNF
indices as semantic data. It must pin all premise hashes, enforce exact matrix and kernel hashes,
and stop between parameter stages. The training budget is 600 seconds and 10 GiB private memory.

No all-parameter, manuscript, or Zenodo claim is permitted from a finite pass.
