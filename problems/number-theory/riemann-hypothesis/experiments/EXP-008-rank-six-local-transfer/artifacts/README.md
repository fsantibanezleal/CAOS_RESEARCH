# EXP-008 artifact index

The canonical evidence is in `canonical/`:

- `result.json`: directed rank-three and rank-six onset certificates, frozen
  point comparisons, optimized spectral correction, pinned sources, and the
  independent 100-decimal replay;
- `execution-receipt.json`: clean commit, runtime, budget, runner hash, and
  result hash;
- `checkpoint.json`: terminal stage marker; and
- `stdout.txt`: flushed stage log.

The portable canonical run passed from clean commit
`a26ba0d403d14d6d08f042503ce52b774c38bdfd`. The machine artifacts certify the
scalar consequences and interval computations. The rank-independent analytic
argument is in `mathematical-proof.md`. Pearce-Crump's rank-six profile and
constant remain an attributed source input because the public paper does not
print its coefficient matrix.

`windows-canonical-v1/` preserves the exact CRLF result bytes cited by
manuscript v0.07. The current canonical run uses fixed LF serialization so its
receipt hash is identical to the immutable Git blob on every platform.
