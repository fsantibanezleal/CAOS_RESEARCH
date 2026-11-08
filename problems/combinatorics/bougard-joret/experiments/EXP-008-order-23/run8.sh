#!/usr/bin/env bash
# BJ EXP-008: the 8 open second-regime triples of order 23 (triples.json: n, alpha, k, Emin, Emax), each edge count
# capped at 3 hours, 24 hours in total (hypothesis.md). Run in WSL from this folder: bash run8.sh <nauty dir> <filter2>
set -u
N=${1:?nauty dir with geng_a<alpha>}
F2=${2:?filter2 binary}
cd "$(dirname "$0")"
start=$(date +%s)
python3 -c "import json; [print(*r) for r in json.load(open('triples.json'))]" | while read n a k lo hi; do
  for E in $(seq $lo $hi); do
    if [ $(( $(date +%s) - start )) -gt 86400 ]; then echo "BUDGET ($n,$a,$k) stopped before E=$E"; exit 0; fi
    timeout 10800 python3 run_enum.py $N/geng_a$a $F2 $n $a $k $E $E --jobs 28 --mod 56 || { echo "CAP ($n,$a,$k) E=$E"; continue 2; }
  done
  echo "DONE ($n,$a,$k)"
done
echo "total seconds=$(( $(date +%s) - start ))"
