# EXP-023 verdict: budget-stopped incomplete local cover

[MV] The owned full-cover supervisor reached its declared six-hour limit on
2026-10-04. Budget action: 02:48:13.665049 UTC; completed process shutdown and
receipt: 02:48:18.712730 UTC. Elapsed 21,605.049 seconds, including 5.049 seconds
of bounded shutdown/preservation overhead. The six owned process IDs were
checked absent after shutdown. No unrelated process was stopped.

Coverage is 95 of 96 completed shards. The last sealed checkpoint contains
21,772,288 nodes and 19 pending boxes; the last progress log shows 21,777,408
nodes. The difference is unsaved progress, not a completed box certificate.
All 52,240 native table-input controls passed before the budget stop, but a
missing shard prevents the universal inequality. No completion, corruption-
control or exact-byte reproducibility success is inferred from partial work.

The frozen source/table/archive, all stable stopped checkpoints and reports,
run binding, supervisor receipt and log are preserved in a poststop ZIP:
1,053,509 bytes, SHA256
c4316f289694754df3beb0d8fc795a4e4f30d610ea999be8c24357d77dd508e2.
Every member's CRC, size and bytes were compared against stable source bytes
before and after archiving. Heavy data remain outside git; the compact receipt
is in artifacts/poststop-preservation.json. Existing smoke/pilot receipts and
all failure/partial-rejection records remain untouched.

Disposition: research-record, inconclusive. The candidate distinct-strip bound
2340938143167/2795532013000 remains unproved. Issue #362 remains open; no
restart is licensed without another cost/value review. RH-F4's EXP-028 analytic
gain now takes priority over another expensive local traversal. No claim in
the immutable distinct-zero-gram v0.01 publication depends on this candidate.

## How could this be wrong?

A point diagnostic is not a box proof, pending-stack size is not an ETA,
and preserved checkpoints do not establish the remaining local inequality.
Only complete 96-shard coverage with every declared independent verification
gate could license the proposed zero bound. This record supplies none of that.
