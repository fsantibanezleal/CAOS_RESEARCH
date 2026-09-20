# EXP-065 proof record

## Exact training result

For every `p=8,9,10` and `r=1,2`, the decoder found an integral witness with
one source coordinate and coefficient `-1`.  If

```text
L_p = [1,p] union [3p,4p-2]
E_{p,r} = (L_p minus {p-r,3p,3p+r}) union {6p,10p},
```

then the source is the labelled column `[S,E_{p,r};p-2]`, and direct
multiplication in the complete mask-58 carrier gives

```text
pi_58 d[S,E_{p,r};p-2] = -x_(0,r,p-2-r).
```

Thus all six training targets vanish integrally.  The witnesses have support
one, coefficient norm one and a single normalized semantic skeleton, improving
all declared P1 and P2 bounds.

## Independent audit

The auditor does not import the decoder.  It rebuilds each original source
boundary from the differential definition, reconstructs the labelled persistent
component independently, compares the restricted boundary with the frozen
carrier column, and then applies mask 58.  All six reconstructed columns have
exactly one retained entry: coefficient `-1` on the requested endpoint row.

The audit also changes each source coefficient and each target row.  All twelve
mutations are rejected.  The canonical audit artifact digest is
`b5ce59bae588e12cb89abcf13b4b80ecd04018f84784317d66b9380171a45440`.

## Formula suggested by the witnesses

The unprojected boundary of each discovered source has a much simpler pattern
than the decoder needed:

- low first-interval faces have semantic atom `R0`;
- low second-interval faces have semantic atom `R2`;
- deleting `10p` gives the requested `R5` endpoint with sign `-1`; and
- deleting `6p` gives no target basis element.

Mask 58 retains `R1,R3,R4,R5`, so it removes the first two families.  This
observation suggests a direct all-parameter proof before contraction.  It is
not part of EXP-065: the formula and the untouched `p=11` test must be frozen
before evaluation in a separate experiment.

## What could be wrong?

The finite identities could reflect training-range behaviour of the persistent
component rather than a uniform presentation.  The semantic atom calculation
might also correctly describe the original boundary while failing to identify
the same projected carrier used after contraction.  EXP-065 therefore proves
only the six exact training identities.  It makes no claim for `p=11`, for all
parameters, or for the complete mask-58 cokernel.
