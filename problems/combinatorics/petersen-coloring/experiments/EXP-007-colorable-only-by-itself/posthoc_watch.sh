#!/bin/sh
# EXP-007: for each tag, wait until the orphaned WSL solver that writes its proof has exited, then
# check the proof with certify_existing.py. Usage: sh posthoc_watch.sh G52b:42 G52:24 ...
EXP=problems/combinatorics/petersen-coloring/experiments/EXP-007-colorable-only-by-itself
for item in "$@"; do
  g=${item%%:*}; k=${item##*:}
  (
    while wsl -e bash -lc "ps -eo args | grep cadical | grep -q '${g}_k${k}\.drat'" 2>/dev/null; do sleep 60; done
    cp $EXP/artifacts/result-$g-k$k.json $EXP/artifacts/timeout-$g-k$k.json 2>/dev/null
    .venv/Scripts/python.exe $EXP/certify_existing.py --graph $g --k $k > $EXP/artifacts/certify-$g-k$k.log 2>&1
  ) &
done
wait
