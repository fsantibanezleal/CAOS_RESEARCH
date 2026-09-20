#!/bin/sh
# EXP-007 control (addendum 2): the reduced and the unreduced runner must agree on small graphs.
# Run from the repository root. Writes artifacts/agreement/*.log and result-*-{red,unred}.json.
EXP=problems/combinatorics/petersen-coloring/experiments/EXP-007-colorable-only-by-itself
mkdir -p $EXP/artifacts/agreement
jobs=""
for k in 2; do jobs="$jobs K4:$k"; done
for k in 2 4; do jobs="$jobs prism:$k"; done
for k in 2 4 6 8; do jobs="$jobs petersen:$k"; done
for k in 2 4 6 8 10; do jobs="$jobs J3:$k"; done
for k in 2 4 6 8 10 12 14 16 18; do jobs="$jobs J5:$k"; done
for j in $jobs; do for m in red unred; do echo "$j:$m"; done; done | xargs -P 14 -I{} sh -c '
  g=$(echo {} | cut -d: -f1); k=$(echo {} | cut -d: -f2); m=$(echo {} | cut -d: -f3)
  flag=""; [ "$m" = "unred" ] && flag="--unreduced"
  .venv/Scripts/python.exe '$EXP'/run_inc.py --graph $g --k $k --cap 3600 --suffix=-$m $flag > '$EXP'/artifacts/agreement/$g-k$k-$m.log 2>&1'
echo done > $EXP/artifacts/agreement/all.done
