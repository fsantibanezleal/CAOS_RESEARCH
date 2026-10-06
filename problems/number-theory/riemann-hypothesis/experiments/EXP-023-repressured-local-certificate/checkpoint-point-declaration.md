# Pending-box point diagnostic

Declared before execution, 2026-10-04. This is a bounded diagnostic within EXP-023,
not a new universal certificate or a new distinct-zero transfer.

Copy one atomic shard-000 checkpoint to a new external output directory. Validate
its wrapper checksum, schema, pressure, target, grid, packet hash and incomplete
status. Inspect at most the last 32 pending boxes, in their recorded order, and
evaluate their exact rational midpoints `(lo+hi+1)/(2*4000)` at 256 bits. Compare
the pinned derivative-based kernel with an independently written native 0F1
expression using the same rational coefficients and FLINT/Arb library. Preserve
the snapshot, script hash and both enclosures for every inspected point.

Stop at 60 seconds. Do not mutate, prepare, resume or stop the frozen worker, its
tables or checkpoints. A strict energy upper bound below 52231/5000000 would be
a counterexample candidate requiring a separate 512-bit confirmation before
changing EXP-023's verdict. Otherwise record only pointwise agreement/slack or
unresolved comparison. No inference of global validity from finitely many points.

The two expressions are independent code paths, not independent arithmetic
libraries. GPU sampling would not replace the required interval cover.
