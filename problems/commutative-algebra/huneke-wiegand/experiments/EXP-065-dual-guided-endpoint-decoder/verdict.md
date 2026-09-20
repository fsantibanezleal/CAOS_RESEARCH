# EXP-065 verdict

Status: **SUPPORTED on the frozen training range**.

- P1 passes: all six endpoint targets have exact integral witnesses, found
  without a full transformed HNF and with zero expansion rounds beyond the
  target-incident initialization.
- P2 passes strongly: every witness has support one, coefficient `-1`, and the
  same normalized semantic skeleton.
- P3 passes: direct full-matrix multiplication, reverse-order reconstruction,
  independent original-boundary reconstruction, and twelve negative controls
  all agree.

The result is a finite constructive theorem for `p=8,9,10`.  It does not use or
open the locked `p=11` holdout.  The emergent formula is promoted only to a new
frozen hypothesis, not to a theorem here.

Publication decision: no manuscript split and no Zenodo update.  The training
formula must first pass the holdout and a symbolic all-parameter audit.  A
uniform endpoint theorem would belong in the existing integral connecting-map
manuscript; a separate manuscript remains unjustified without a general
decoding/Morse theorem or a complete complementary-cokernel result.
