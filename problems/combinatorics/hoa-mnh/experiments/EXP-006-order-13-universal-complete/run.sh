#!/usr/bin/env bash
# hoa-mnh EXP-006: complete order-13 case A over EXP-004's 2,000 parts. A part with a recorded .err is kept.
# Run in WSL: bash run.sh <geng_mnhA> <join6> <mnh> <out_dir> <jobs>
set -u
GA=${1:?geng_mnhA}; J=${2:?join6}; M=${3:?mnh}; OUT=${4:?out dir}; P=${5:?jobs}
mkdir -p "$OUT/parts"
start=$(date +%s)
seq 0 1999 | xargs -P $P -I{} bash -c \
  "[ -s '$OUT/parts/p{}.err' ] || { $GA -q 12 {}/2000 | $J | $M > '$OUT/parts/p{}.txt' 2> '$OUT/parts/p{}.tmp' && mv '$OUT/parts/p{}.tmp' '$OUT/parts/p{}.err'; }"
echo "production done seconds=$(( $(date +%s) - start ))"
echo "parts=$(ls $OUT/parts/*.err | wc -l) $(cat $OUT/parts/*.err | awk '{r+=$2; p+=$4; m+=$6} END {print "read", r, "pruned", p, "mnh", m}')"
for f in $OUT/parts/*.err; do cat "${f%.err}.txt"; done > "$OUT/mnh-n13-caseA.txt"
echo "total mnh=$(wc -l < "$OUT/mnh-n13-caseA.txt")"
