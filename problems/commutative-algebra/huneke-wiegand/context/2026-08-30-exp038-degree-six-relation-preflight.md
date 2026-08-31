# EXP-038 preflight - first degree-six relation correction

Date: 2026-08-30. Scope: the `t=2` parity-sensitive connecting quotient only.

## Why a new experiment is justified

EXP-037 exactly refutes the OEIS-derived free-lattice count at its first out-of-sample point:
`e_10=72`, not 73. The one-unit deficit begins at `n=p-4=6`. The lowest-complexity structural
repair that preserves the old denominator is not another polynomial interpolation; it is one
degree-six relation in the candidate graded defect module:

```text
G(x)=(1+2x+x^2+x^3-x^6)/((1-x)^2(1-x^2)(1-x^3)).
```

This formula is fitted through `p=10` and is therefore only a falsification target. It predicts
the genuinely new value `e_11=102` (the rejected formula predicted 104).

## Source and novelty boundary

- OEIS A254874 supplied the now-refuted positive-numerator sequence; it is heuristic evidence
  only: https://oeis.org/A254874.
- The current Huneke-Wiegand and characteristic-dependent Betti-number literature does not state
  this family-specific connecting-quotient series. The relevant background remains the primary
  sources already pinned by EXP-037, including https://arxiv.org/abs/1009.4243 and
  https://arxiv.org/abs/math/0408016.
- No database lookup or finite fit can prove the new series. An all-parameter result would require
  an explicit signed presentation or recurrence for the parity defect.

## Frozen premises

```text
EXP-037 proof       ae2c3be4ec509264717fef48dd2cd73a47fe51c46a37240372a7a117ff5cc330
EXP-037 verdict     ccc185190e885c334bcf6f401d47c2f4b1f44d8a3931226b240b3528e07b70bb
EXP-037 run.py      1abebc24c99398dded97aa08216211db089889e154736ed9eb5a7202de0b5df0
EXP-037 p=10 target ca97087466fdd705e22f69e79cdfecfc7dbce0684475b98bd99757cfed030d7b
EXP-037 audit       03682871743842bb8a3224b70aee72436ed21056de3d83dfb178f9023c7ad088
```

## Validation plan

1. Reconstruct the exact sequence `1,4,9,18,31,49,72` from frozen artifacts.
2. Derive the corrected coefficients independently as the rejected lattice coefficient minus the
   shifted denominator coefficient.
3. Compute the complete `(11,2)` block over `GF(2)` and `GF(3)` using the frozen two-sided
   fill-controlled engine.
4. If the new prediction passes, rerun with canonical residual order and `GF(5)`; exact agreement
   is mandatory before any structural claim.
5. Search for the proposed first relation only after the numerical gate. Finite agreement is not
   a relation certificate.

## Budget and stopping rule

- formula and premise gate: 30 seconds, 2 GB;
- primary `(11,2)` target: 3,600 seconds, 40 GB private memory;
- audit: the same envelope, only after primary completion;
- conditional `(12,2)` phase: 7,200 seconds, 40 GB, opened only after the audited `p=11` pass;
- stop immediately at an exact mismatch or a resource boundary; neither is silently promoted to
  evidence for a different claim.

No manuscript or Zenodo update opens at declaration. A second out-of-sample value plus a concrete
relation certificate would trigger reassessment; another finite fit alone would not.

## Phase-two activation

The primary `(11,2)` run completed in 330.533246 seconds and the canonical-order/`GF(5)` audit in
176.288232 seconds. Both give exact excess 102, with identical bases, structural profiles, and
same-field ranks. This measured headroom activates the already declared `e_12=138` prediction
under the conditional budget above. The second finite value still cannot substitute for the
relation or recurrence proof.
