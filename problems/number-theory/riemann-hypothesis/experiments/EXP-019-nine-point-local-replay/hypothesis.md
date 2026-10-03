# EXP-019: packet-bound independent replay of the nine-point local inequality

Declared 2026-10-03 before implementation, arithmetic probes or replay.
User continuation explicitly rejects the conditional EXP-018 target as a
stopping point. Public issue #356 tracks the open input obligation.

## Target and predictions

Replay the universal eight-gap inequality for the exact packet SHA-256
9f113eb52fba9c3a1fd7d5f2714e925ef19d3104b8fdaa982661fa96794d0c0d,
source revision 1610b97b7895ff34982260f8dcaf04a0f7b82cf7,
delta=15211/2500000, pressure=1/2500, grid=4000, precision=128 bits.
All 96 disjoint initial-box shards must verify, with source/code/table
bindings and coverage checked. This closes the missing packet-to-run
binding only if every shard completes successfully. The matrix/counting
consequence is the separately validated conditional implication EXP-018.

Before the long replay, audit the source's table and pruning arithmetic,
particularly the binary64 pressure term, by exact rational comparison over
the complete relevant cell-index range. A source arithmetic failure stops
use of that path; retain it and implement a sign-correct enclosure before
the replay. Preserve upstream license and exact source hashes. Added
progress/checkpoint instrumentation must leave mathematical pruning
decisions unchanged, except for an explicitly documented rounding repair.

## Premises and invariant first

EXP-018 confirms capacity, window and transfer compatibility but not the
local inequality. The source manifest supplies version/size/hash/license
bindings. The raw kernel and complete generalized verifier have now been
read; Arb, IEEE-754 and interval-derivative trust bases remain explicit.
Invariant first: reject a packet/source/hash/capacity mismatch before
building tables. Audit representative singularities and exact pressure
rounding before the exhaustive cover. Do not infer certification from a
finite gap sample or matching table hashes alone.

## Method, budgets and checkpoints

32 logical CPUs and about 47.7 GiB physical memory are available. Use at
most 24 worker processes, leaving capacity for concurrent sessions.
GPU arithmetic is not used for outward-rounded decisions. First run a
tooling smoke test proving flushed stage/progress output, atomic checkpoint
creation and resume equivalence on a small explicit cover; its result is
not the nine-point proof. Parallel table chunks are cached with hashes.
Full search checkpoints preserve each shard's pending subdivision stack,
counters, table/spec bindings and completed status. Checkpoint at least
every 60 seconds; flush progress at least every 30 seconds.

Initial planning budget: 12 wall-clock hours for all 96 shards after smoke
and table construction, with a 30-minute table budget and a 10-minute
preflight/audit budget. This is an estimate, not a success claim. A budget
hit records incomplete coverage and retained checkpoints; it does not
confirm or refute the local inequality. Resume within a newly recorded
budget, without treating a bounded run as fulfillment of the user's goal.

## Pass, failure and adversarial checks

PASS: complete disjoint cover, all terminal branches certified, independent
coverage/binding aggregation and controls rejecting corruption, plus a
written audit of every mathematical change. This supplies an independent
computational replay with the stated trust base, not external peer review.
FAIL: unresolved terminal cell or invalid enclosure refutes this proposed
certificate implementation; a source/candidate mismatch invalidates the
import. Neither outcome settles RH. Test omitted/duplicate shard, corrupt
checkpoint, table/packet mismatch and interrupted-resume equivalence.

Manuscript reassessment follows complete replay and mathematical review of
the distinct-strip consequence. No automatic worldwide novelty, onset
improvement, RH solution or early publication is claimed. Continue the
research requirement beyond operational commits or partial coverage.
