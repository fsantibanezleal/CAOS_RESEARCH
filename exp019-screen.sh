#!/bin/bash
set -u
SRC=/mnt/e/_Temp/wt-cc-research/problems/dynamical-systems/central-configurations/experiments/EXP-019-single-minor-cuts/artifacts
mkdir -p /root/exp019s
for prime in 32003 1073741789; do
  for f in p1-sh-g4 p2-sh-g3; do
    sed "s/^ring r=0,/ring r=${prime},/" "$SRC/${f}.sing" > /root/exp019s/${f}-p${prime}.sing
    start=$(date +%s)
    timeout 300 Singular -q /root/exp019s/${f}-p${prime}.sing > /root/exp019s/${f}-p${prime}.out 2>&1
    rc=$?
    secs=$(( $(date +%s) - start ))
    dim=$(grep -o "SINGDIM=[0-9-]*" /root/exp019s/${f}-p${prime}.out | head -1)
    echo "${f} p=${prime} rc=${rc} secs=${secs} ${dim:-NODIM}"
  done
done
