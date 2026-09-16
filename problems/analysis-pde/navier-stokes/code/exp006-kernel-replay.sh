#!/usr/bin/env bash
# EXP-006: independent kernel replay of the OpenAI certificate.
#
# Hypothesis committed at problems/analysis-pde/navier-stokes/experiments/EXP-006-kernel-replay/.
# leanchecker ships with the toolchain since Lean v4.28.0; the certificate pins v4.34.0-rc2.
#
# CLI semantics, read from src/LeanChecker.lean in the Lean repository rather than guessed:
#   * a target argument matches every module whose name it is a PREFIX of;
#   * -v prints one "replaying <module>" line per module, which is the only way to count
#     what was actually checked (the tool is silent on success, so a run that checked
#     nothing also exits 0: gate E2 exists for exactly that reason);
#   * failure prints "leanchecker found a problem in <module>" and exits nonzero.
set -o pipefail
export ELAN_HOME='E:\_Temp\elan'
export LEAN_NUM_THREADS="${LEAN_NUM_THREADS:-4}"
LAKE=E:/_Temp/elan/bin/lake.exe
CHECKER=E:/_Temp/elan/toolchains/leanprover--lean4---v4.34.0-rc2/bin/leanchecker.exe
LOG=E:/_Temp/exp006
mkdir -p "$LOG"
cd E:/_Temp/lean-ns || exit 90

echo "=== EXP-006 start $(date -Is) ==="
echo "toolchain pin: $(cat lean-toolchain)"
"$CHECKER" --version > "$LOG/checker-version.txt" 2>&1 || true

# E2 input: how many modules the package actually built.
find .lake/build/lib/lean -name '*.olean' | wc -l > "$LOG/olean-count.txt"
echo "package oleans: $(cat "$LOG/olean-count.txt")"

echo "--- replay, all three top-level namespaces, threads=$LEAN_NUM_THREADS ---"
start=$(date +%s)
"$LAKE" env "$CHECKER" -v NavierStokes Euler ComparatorChallenges > "$LOG/replay.log" 2>&1
rc=$?
end=$(date +%s)
echo "exit=$rc  seconds=$((end - start))"
echo "$rc" > "$LOG/replay.exit"
echo "modules replayed: $(grep -c '^replaying ' "$LOG/replay.log")"
grep -c '^replaying ' "$LOG/replay.log" > "$LOG/replayed-count.txt"
tail -5 "$LOG/replay.log"
echo "=== EXP-006 end $(date -Is) ==="
