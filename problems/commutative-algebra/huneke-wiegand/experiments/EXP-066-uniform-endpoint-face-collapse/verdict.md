# EXP-066 verdict

Status: **PROVED**.

- P1 passes: the untouched `p=11` frozen component has unique matching columns
  210 and 308, projecting to `-x_(0,1,8)` and `-x_(0,2,7)`.
- P2 passes by a symbolic all-parameter proof: the complete source boundary has
  only `R0^(p-3)`, `R2^(p-3)` and one negative `R5` endpoint row, so mask 58
  leaves exactly that endpoint.
- P3 passes: 586 producer identities, 586 independent reverse-order identities,
  and 2,930 negative controls agree. Permanent focused tests pass.

The new theorem is

```text
Pi_58 d(s_(p,r)) = -x_(0,r,p-2-r)  for p>=8 and r=1,2.
```

It supplies explicit support-one integral sources for the two mask-58 endpoint
classes uniformly in `p`. This is more than the finite existence result of
EXP-064 and the training extraction of EXP-065.

Scope boundary: this is a theorem in the full semantic row projection plus an
exact finite comparison with the frozen persistent carrier. It is not a uniform
identification with the isolated component, not an upper bound for the projected
cokernel, and not a solution of the complete complementary-cokernel problem or
the original Huneke-Wiegand conjecture.

Publication decision: expand the existing integral connecting manuscript in
place; do not split a new manuscript. Under methodology 09 this validated novel
constructive theorem opens a v0.04 Zenodo new-version workflow. The paper must
state the projection boundary prominently and must not upgrade the result to a
complete isolated/relative comparison.
