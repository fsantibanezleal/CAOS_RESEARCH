#!/bin/bash
# EXP-017c mod-p triage: reuse EXP-017/017b archived scripts with the ring
# characteristic changed; 300 s per cell; SCREEN-ONLY data.
set -u
SRC17=/mnt/e/_Temp/wt-cc-research/problems/dynamical-systems/central-configurations/experiments/EXP-017-stratum22-loci-bounds/artifacts
SRC17B=/mnt/e/_Temp/wt-cc-research/problems/dynamical-systems/central-configurations/experiments/EXP-017b-stratum22-loci-svars/artifacts
OUT=/mnt/e/_Temp/wt-cc-research/problems/dynamical-systems/central-configurations/experiments/EXP-017c-loci-modp-triage/artifacts
mkdir -p "$OUT" /root/exp017c
for prime in 32003 1073741789; do
  for src in "$SRC17/p1-delta4-full.sing" "$SRC17/p2-delta3-full.sing" \
             "$SRC17/p3-delta2-full.sing" "$SRC17/p4-delta1-full.sing" \
             "$SRC17B/p0a-shape-s.sing"; do
    base=$(basename "$src" .sing)
    tgt=/root/exp017c/${base}-p${prime}.sing
    sed "s/^ring r=0,/ring r=${prime},/" "$src" > "$tgt"
    start=$(date +%s)
    timeout 300 Singular -q "$tgt" > "$OUT/${base}-p${prime}.out" 2>&1
    rc=$?
    secs=$(( $(date +%s) - start ))
    dim=$(grep -o 'SINGDIM=[0-9-]*' "$OUT/${base}-p${prime}.out" | head -1)
    echo "${base} p=${prime} rc=${rc} secs=${secs} ${dim:-NODIM}" | tee -a "$OUT/screen-table.txt"
  done
done
echo SCREEN_DONE | tee -a "$OUT/screen-table.txt"
