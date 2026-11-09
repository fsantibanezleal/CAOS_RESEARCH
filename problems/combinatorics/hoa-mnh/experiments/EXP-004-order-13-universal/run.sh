#!/usr/bin/env bash
# hoa-mnh EXP-004: order 13, MNH graphs with a universal vertex (case A). Gates at orders 10-12, then production in
# 2000 disjoint parts with 6 processes; a part is recorded only when its pipeline finishes (resumable).
# Run in WSL: bash run.sh <out_dir>
set -u
OUT=${1:?out dir}
GA=${GA:?set GA to the geng binary built with prune_degsumA.c (see EXP-006/run.sh)}
M=~/caos-nauty/mnh
J=~/caos-nauty/join6
mkdir -p "$OUT/parts"
for h in 9 10 11; do
  start=$(date +%s)
  res=$($GA -q $h | $J | $M 2>&1 >/dev/null)
  echo "gate order $((h + 1)): $res seconds=$(( $(date +%s) - start ))"
done | tee "$OUT/gates.txt"
start=$(date +%s)
seq 0 1999 | xargs -P 6 -I{} bash -c \
  "[ -s '$OUT/parts/p{}.err' ] || { $GA -q 12 {}/2000 | $J | $M > '$OUT/parts/p{}.txt' 2> '$OUT/parts/p{}.tmp' && mv '$OUT/parts/p{}.tmp' '$OUT/parts/p{}.err'; }"
echo "production done seconds=$(( $(date +%s) - start ))"
echo "parts=$(ls $OUT/parts/*.err | wc -l) $(cat $OUT/parts/*.err | awk '{r+=$2; p+=$4; m+=$6} END {print "read", r, "pruned", p, "mnh", m}')"
cat "$OUT"/parts/*.txt > "$OUT/mnh-n13-caseA.txt"
echo "total mnh=$(wc -l < "$OUT/mnh-n13-caseA.txt")"
