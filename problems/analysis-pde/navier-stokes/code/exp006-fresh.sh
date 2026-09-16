#!/usr/bin/env bash
# EXP-006, second strategy: one environment, kernel-replayed from scratch.
#
# The prefix sweep (exp006-kernel-replay.sh) queues one task per module, and each task
# loads its own import closure: 2659 closures, which on this machine is I/O bound and
# grows without bound in memory (11.6 GB resident after 80 minutes for 144 seconds of
# CPU). `--fresh` instead imports ONE module's closure once and replays every constant in
# it, mathlib included, into an empty kernel environment. It checks strictly more, in one
# bounded process.
set -o pipefail
export ELAN_HOME='E:\_Temp\elan'
export LEAN_NUM_THREADS="${LEAN_NUM_THREADS:-8}"
LAKE=E:/_Temp/elan/bin/lake.exe
CHECKER=E:/_Temp/elan/toolchains/leanprover--lean4---v4.34.0-rc2/bin/leanchecker.exe
LOG=E:/_Temp/exp006
mkdir -p "$LOG"
cd E:/_Temp/lean-ns || exit 90
for target in NavierStokes Euler; do
  echo "=== --fresh $target, start $(date -Is) ==="
  start=$(date +%s)
  "$LAKE" env "$CHECKER" --fresh -v "$target" > "$LOG/fresh-$target.log" 2>&1
  rc=$?
  echo "$target exit=$rc seconds=$(( $(date +%s) - start ))"
  echo "$rc" > "$LOG/fresh-$target.exit"
  tail -3 "$LOG/fresh-$target.log"
done
echo "=== done $(date -Is) ==="
