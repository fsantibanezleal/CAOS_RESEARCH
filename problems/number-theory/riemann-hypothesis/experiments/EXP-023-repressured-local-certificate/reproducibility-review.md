# Completed-output control and archive gates

These gates are prepared while the full interval cover remains incomplete.
Their actual 95-report admission rejections are bound in
`artifacts/prepared-tools-partial-rejection.json`. No complete-output control
pass or archive creation is inferred from those negative controls.

After the independently audited 96-shard completion, run
`actual_cover_controls.py` against the real output. It first audits that
output, then makes ordinary copies in a separate temporary directory.
Twelve corruptions test missing and duplicated shards, false verdicts,
wrong targets, changed source/table bytes, corrupt checkpoints, unfinished
or pending state, changed initial domains, invalid tree accounting and a
boolean counter. Semantic checkpoint corruptions recompute both transport
hashes. Each corruption must fail at its specified gate; afterward a fresh
audit must agree with the original. Synthetic completed receipts are not
used. These controls do not independently reproduce every interval leaf.

`reproducibility_archive.py` requires both the full exact transfer and the
source-bound twelve-case control receipt. It verifies the original baseline
cache against the prefix-source binding and preserves physical source bytes,
including licensed upstream originals. This avoids line-ending changes from
Git extraction invalidating runtime hashes. It includes only scoped source,
input, tables, completed reports/checkpoints and proof reviews. It checks
every ZIP member's bytes and CRC, extracts into a separate temporary tree,
and runs the stdlib cover and exact-transfer auditors from that extracted
tree. The complete interval traversal is not rerun by this archive builder.
Existing archives are preserved rather than overwritten.

The stdlib accounting and exact-transfer auditors normalize path separators.
The runtime binding used by full workers includes Windows path spellings;
the full-worker execution has been tested on Windows. No verified Linux
full-worker replay, formal proof certificate or external review is claimed.
Python/FLINT/Arb and the executed interval source remain explicit trust bases.

CI run 37155303536 passed on commit
`098c0476dffe8991ced26871d381bf0f22d5c743`:
<https://github.com/fsantibanezleal/CAOS_RESEARCH/actions/runs/37155303536>.
Its guards and artifact-contract checks do not execute the mathematical
Riemann test suite or the full interval traversal. New helper sources pass
targeted Ruff checks; their complete-output paths remain pending.

The local unscoped research-structure checker reports missing other-problem
directories because this working tree deliberately has a Riemann-only sparse
checkout. Its output is not reported as a pass or a mathematical failure.
The scoped governance checker passes. Full-tree structure is checked by CI;
the sparse checkout is preserved while byte-bound workers remain active.
