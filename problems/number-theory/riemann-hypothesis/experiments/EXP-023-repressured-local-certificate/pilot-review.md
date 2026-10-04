# Pilot cost review and deterministic parallel partition revision

The pilot began 19:35:50 UTC and was stopped at 19:57:22 UTC after a
validated snapshot. The twenty-minute planning budget was exceeded by
about 92 seconds during proof writing and snapshot/ownership checks; this
deviation is recorded, not omitted. The checkpoint has 2823168 processed
nodes, 1411589 splits, 1411579 prunes, depth 72 and eleven pending boxes.
It is incomplete and proves no universal inequality.

The snapshot ZIP SHA-256 is
cb3f95942722ff5838092f5c217f357d39de248281ac7beda149919884b5bfac.
Only the verified owned launcher PID 35716 and child PID 75004 were stopped.
EXP-020 continues. The pilot's measured rate is not a completion estimate:
pending-box count does not measure remaining geometric volume or proof cost.

Independent domain reconstruction reveals one surviving interval per
coordinate, hence exactly ONE Cartesian initial box. Under the inherited
96-way modulo partition only shard zero has work. Merely launching the
other 95 shards would not parallelize this changed-pressure certificate.
The stronger pressure changes this domain geometry relative to EXP-020.

## Revision declared before implementation

Keep the same exact mathematical inequality and existing immutable pruner.
Clone its core into a separately bound file whose sole mathematical-domain
change is splitting each surviving coordinate component into four exact
contiguous integer ranges. The 4^8=65536 Cartesian boxes cover the former
single box without gaps or overlaps and are assigned modulo 96. This is
an engineering revision, not a new numerical bound or priority claim.

Verify the per-coordinate exact union/disjointness, independent Cartesian
partition/accounting, actual flushed checkpoint/resume smoke and the source
delta against the frozen quadratic core before another launch. Keep all
earlier source files and pilot bytes unchanged. New wrappers, core and
auditor receive new hashes and an external `exp023-partitioned-local-20261003`
directory; the earlier checkpoint cannot be imported into this new cover.

Pilot planning budget: twenty minutes for one revised actual shard, one CPU,
with checkpoint every sixty seconds and progress every thirty seconds.
At budget retain partial state and review cost. A full revised cover gets
at most four workers while EXP-020 runs and a six-hour planning budget from
full launch. If EXP-020 subsequently finishes and its independent complete
audit passes, its freed resources may be reassigned up to 24 workers via an
explicit complete-audit receipt gate, without changing frozen runtime source.
One pilot's cost remains an unreliable worst-case estimate. Incomplete
coverage at any budget is inconclusive, not a failure or the user's stopping gate.
