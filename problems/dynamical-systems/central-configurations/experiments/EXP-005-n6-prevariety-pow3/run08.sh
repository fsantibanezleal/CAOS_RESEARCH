#!/usr/bin/env bash
# EXP-005 continuation on gfan 0.8beta (built 2026-07-25 from the author tarball,
# SHA-256 fa7884e5f317c50f8fb4f37bcf5d419f0fd5f7b90d6037349d1957ea73cebbee; binary
# installed as gfan08, SHA-256 0f177e6a4f7829fc41910ed0395254b2d1e895322bd5705c2c803225bbb5f661).
#
# Motivation: gfan 0.7 failed at n = 6 in BOTH arithmetic modes (machine-integer
# overflow regardless of valuation magnitude; a CircuitTableInteger assertion after
# 15 h in arbitrary precision). 0.8beta reproduces our n = 5 control f-vector
# (1506 4744 8586 8787 4652 993) exactly, so it is validated before use here.
#
# Usage: run08.sh <label> <bits> <threads> <v1..v6>
set -uo pipefail
LABEL=$1; BITS=$2; THREADS=$3; shift 3
W=~/exp005b && mkdir -p $W && cd $W
HEAVY=/mnt/e/_Datos/caos-research/central-configurations/EXP-005
mkdir -p $HEAVY
S=status-$LABEL.log
echo "$(date -Is) EXP-005/08beta/$LABEL start (bits=$BITS threads=$THREADS valuations: $*)" | tee -a $S

[ -f system-n6.txt ] || gfan08 _nbody -N6 --masses --alsosymmetric --cayleymenger2 > system-n6.txt
sedargs=(-e "s/Q\[m1,m2,m3,m4,m5,m6,/Q(t)[/")
i=1
for v in "$@"; do sedargs+=(-e "s/\bm$i\b/t^$v/g"); i=$((i+1)); done
sed "${sedargs[@]}" system-n6.txt > input-$LABEL.txt

timeout 604800 gfan08 _tropicalprevariety --usevaluation -j$THREADS --mint --minx --bits $BITS \
    < input-$LABEL.txt > prevariety-$LABEL.out 2> prevariety-$LABEL.err
rc=$?
echo "$(date -Is) EXP-005/08beta/$LABEL finished rc=$rc" | tee -a $S
if [ $rc -eq 0 ] && [ -s prevariety-$LABEL.out ]; then
  cp prevariety-$LABEL.out $HEAVY/
  grep -a -A2 "F_VECTOR" prevariety-$LABEL.out | head -3 | tee -a $S
  sha256sum system-n6.txt input-$LABEL.txt prevariety-$LABEL.out >> hashes-$LABEL.txt
else
  tail -3 prevariety-$LABEL.err | tee -a $S
fi
