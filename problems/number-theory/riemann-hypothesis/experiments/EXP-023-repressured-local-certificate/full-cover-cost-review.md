# Revised full-cover cost review

Recorded before the revised full-cover launch, 2026-10-03 UTC.

The quarter-partition pilot ran from 20:08:02 to 20:33:47 UTC: 25 minutes
45 seconds, exceeding its twenty-minute planning budget by 345 seconds.
Manual budget monitoring was inadequate. The preserved receipt and validated
ZIP bind 1912832 nodes, 956079 splits, 956753 prunes, maximum depth 56,
683 initial boxes and nine pending boxes. This is incomplete. Neither the
pending-box count nor this shard's rate provides a reliable completion ETA.

The revised coordinate partitions independently cover exactly the old
domain, with no gaps or overlaps. Their 65536 Cartesian boxes give each of
96 shards either 682 or 683 initial boxes. The certified pruning rules are
unchanged, checked against the frozen source by the source-delta test.
The 41 targeted controls passed before the pilot; the full Riemann test
suite subsequently passed. EXP-020 continues at 24 workers.

Proceed with the admitted full cover at four additional workers and a
six-hour planning budget from its actual launch. Resume the pilot only
under its identical mathematical, source and table bindings. Preserve the
earlier unpartitioned pilot separately. Do not infer complete coverage from
any partial checkpoint. The independent complete-cover auditor, actual
cover adversarial checks and exact transfer remain mandatory.

Before launching, add and smoke-test a separate orchestration supervisor.
It starts the owned runner, records its actual start and budget, checks
completion frequently, and at the deadline validates a raw checkpoint
archive before stopping only the verified owned process tree. This changes
no proof decision or frozen verifier source. Its receipt is operational,
not an independent mathematical audit. Test it on a real owned child tree
while verifying an unrelated sentinel survives. Deadline handling and
snapshot durations are recorded, including any overshoot.

More than four workers remains gated on EXP-020's complete independent
audit. At any budget hit, retain the partial cover and review the bottleneck;
the research goal remains active. A stronger distinct-strip bound becomes
a result only after the complete universal certificate and attributed
analytic transfer pass. No manuscript or publication claim is made here.
