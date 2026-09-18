#!/usr/bin/env bash
# EXP-005 resume wrapper: continue a gfan 0.8beta prevariety run from its
# --saveas checkpoint (WSL restarts keep killing long runs; the checkpoint
# is the only thing that survives). Usage: run08-resume.sh <label> <bits> <threads>
# Requires input-<label>.txt and checkpoint-<label>.state already in ~/exp005b.
set -uo pipefail
LABEL=$1; BITS=$2; THREADS=$3
W=~/exp005b && cd $W
S=status-$LABEL.log
[ -f checkpoint-$LABEL.state ] || { echo "no checkpoint for $LABEL" | tee -a $S; exit 1; }
echo "$(date -Is) EXP-005/08beta/$LABEL RESUME from checkpoint ($(stat -c%s checkpoint-$LABEL.state) bytes)" | tee -a $S
timeout 604800 gfan08 _tropicalprevariety --usevaluation -j$THREADS --mint --minx --bits $BITS \
    --loadfrom checkpoint-$LABEL.state \
    --saveas checkpoint-$LABEL.state \
    < input-$LABEL.txt > prevariety-$LABEL.out 2>> prevariety-$LABEL.err
rc=$?
echo "$(date -Is) EXP-005/08beta/$LABEL finished rc=$rc" | tee -a $S
if [ $rc -eq 0 ] && [ -s prevariety-$LABEL.out ]; then
  HEAVY=/mnt/e/_Datos/caos-research/central-configurations/EXP-005
  mkdir -p $HEAVY && cp prevariety-$LABEL.out $HEAVY/
  grep -a -A2 "F_VECTOR" prevariety-$LABEL.out | head -3 | tee -a $S
  sha256sum input-$LABEL.txt prevariety-$LABEL.out >> hashes-$LABEL.txt
else
  tail -3 prevariety-$LABEL.err | tee -a $S
fi
