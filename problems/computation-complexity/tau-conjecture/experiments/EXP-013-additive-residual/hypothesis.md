# EXP-013: the ADDITIVE residual at depth 9 (final gate + or -)

Declared 2026-08-20 (code and gates validated before the production run;
the method was designed in `context/2026-08-20-additive-residual-design.md`
before any result was known). Companion to EXP-012, which decides the
multiplicative case; together they decide whether a 9-gate polynomial can
have 7 distinct integer roots (windowed on the additive side, see scope).

## Question

Is there a depth-7 state S7, a one-gate extension v8, an operand b of S7
(or an input), and a sign, such that f = v8 +- b has 7 distinct integer
roots in the window W = [-32, 32]? By the last-gate lemma plus
z_max(8) = 6 (EXP-011), the final gate of any 9-gate 7-rooter must
involve v8; EXP-012 covers the multiplicative case, this one covers +-.

## Method (validated, with the numerical traps recorded)

Values, not polynomials: every operand is evaluated on W modulo a 31-bit
prime; extensions are obtained by one vectorized operation; f = v8 +- b
vanishes at r only if the residues agree, so counting modular agreements
never misses a witness. Candidates are promoted to exact polynomial
construction and exact integer-root counting.

Two traps found and fixed BEFORE production, each caught by the gate:
1. 61-bit primes overflow int64 under modular multiplication (products
   reach 10^36), which produced ~85 garbage candidates per state. Fixed
   by 31-bit primes (residue products stay below 2^63).
2. Identically-zero polynomials (t equal to b, so f = 0) agree at all 65
   window points and flooded the promotion stage (1.4M promotions per
   20k states). Excluded RIGOROUSLY, not heuristically: a nonzero
   polynomial of degree < |W| cannot vanish at |W| distinct points, so a
   full-window agreement is discarded only when both degrees are < 65;
   higher-degree full-window agreements are still promoted.
Effect: promotions per 20k states fell from 1,435,054 to 84 with the hit
count unchanged (41 at threshold 5): a 17,000x cost reduction that loses
nothing.

## Gate (run before production; PASSED)

Threshold 5 on 20,000 states of partition 0: 41 hits, each promoted and
verified exactly. Additive 5-rooters certainly exist at depth 9, so a
zero result would have condemned the pipeline.

## Falsifiable predictions

1. Production (threshold 7) finds NO additive 9-gate 7-rooter. This is
   emptiness commitment number eight; the record is 2-for-7, so
   confidence is stated MODERATE.
2. Combined with EXP-012 (if that is also empty), the seven-root
   threshold is 10, windowed: no 9-gate witness has all seven roots in
   [-32, 32].

## Soundness scope (stated in advance)

A hit is unconditional (exact witness, replayed). Emptiness is WINDOWED:
it excludes only witnesses whose seven roots all lie in [-32, 32]. Every
census record ever observed has roots within [-4, 4], so the window is
generous, but the caveat is real and must appear in any paper text: this
is weaker than the depth-8 theorem, which is unconditional.

## Budget

~700 states/s per core measured; ~19 h at 20 workers for the full
1,048,460,912-state frontier. Resumable per partition; runs under the
Windows Task Scheduler so it survives session teardown. Starts at 8
workers alongside EXP-012 and moves to 20 when that finishes.

## Engine upgrade (2026-08-23), validated by exact regression

The per-state engine was numpy-overhead bound (~700 states/s), projecting
~35 h even at 20 workers. A BATCHED engine (`scan9add_fast.py`, 48 states
per tensor operation, identical mathematics, filter, zero-exclusion and
exact promotion) replaces it. It was not allowed to contribute a single
new result until it reproduced already-completed partitions EXACTLY:

    part 0: ref(states=4095733, hits=0, promoted=4818)
            new(states=4095733, hits=0, promoted=4818)   MATCH
    part 1: ref(states=4094166, hits=0, promoted=4856)
            new(states=4094166, hits=0, promoted=4856)   MATCH

i.e. the old engine's finished work is the new engine's ground truth,
down to the promotion counts. Measured speedup about 3x; the remaining
~200 partitions project to roughly 11 h at 20 workers. Operational note
recorded for the program: a Windows batch launcher fails instantly if its
append-target log is still held open by another process (a `tail -f`
monitor or a killed run), which presents as a scheduled task going
straight to "Ready" with no output; use a fresh log name when swapping
engines.

## Launcher engineering (2026-08-23): three Windows failure modes, all diagnosed

Getting a 20-way parallel scan to run detached on this machine took three
fixes, recorded so the program does not rediscover them:

1. `multiprocessing.Pool` under the Task Scheduler dies with
   `PermissionError: [WinError 5]` when a spawned child tries to
   duplicate the parent's pipe handle. Fix: SHARD mode: 20 independent
   single-process runs (`--shard k --nshards 20`), each taking the
   partitions with p mod 20 == k. No pipes, no handle duplication.
2. `start "..." prog >> log` inside a batch file applies the redirection
   to `start`, not to the child, and the children then hang without a
   usable console. Fix: one batch file per shard, redirecting directly.
3. A batch launcher fails instantly if its append-target log is still
   held open by another process (a `tail -f` monitor, or a killed run);
   the symptom is a scheduled task that jumps straight to "Ready" with
   no output at all. Fix: fresh log names when swapping engines.

Also note: twenty shards each load the 69 MB polynomial catalog at
startup, so the first minutes show processes with ~0 CPU while they read
from disk. That is not a hang; the per-shard logs appear once loading
finishes.

## Operational incidents (2026-08-23/24), recorded

1. **We killed another session's processes.** While clearing what looked
   like stale workers, the filter selected python processes by NAME and
   START TIME with no path or command-line predicate, on a machine where
   other CAOS sessions run their own python work (`cb1.py --resume` from
   the CAOS_MANAGE venv). Those were terminated too. Rule adopted: NEVER
   select processes to kill by image name alone; always require a
   command-line or executable-path match for this experiment
   (`*scan9add_fast.py*`). The keepalive guard is written that way.
2. **A "hung" launch was actually CPU starvation.** Twenty freshly
   launched shards showed ~0 CPU and ~2 MB RSS, which read as wedged; the
   machine was in fact pinned at 100% by other work, so the new processes
   were simply not scheduled. Diagnose saturation before declaring a
   launcher broken.
3. **PowerShell variables are case-insensitive**: a loop variable `$n`
   silently overwrote the shard-count `$N`, so shards launched with
   `--nshards 00, 01, 02, ...` and exited immediately ("shard 2/2: 0
   partitions"). Renamed to `$tag`. No results were affected: mismatched
   shards either did nothing or recomputed existing partitions, and all
   partition writes are atomic and skip-if-present.
4. **Self-healing launcher adopted**: `keepalive.ps1` under the scheduled
   task `tau_keepalive` (every 15 minutes) relaunches only the shards
   that still have unfinished partitions, and only when none of ours are
   running. This survives session teardown, which killed the scan twice.
