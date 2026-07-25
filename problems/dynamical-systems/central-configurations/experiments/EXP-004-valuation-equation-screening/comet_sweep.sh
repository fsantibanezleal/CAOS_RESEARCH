#!/usr/bin/env bash
# EXP-004 comet sweep: per-component pointedness for every prevariety output.
# (Inline $-vars are mangled crossing the Windows->WSL boundary; hence this file.)
set -uo pipefail
cd ~/exp004
EXP=/mnt/d/_Repos/Research_Caos/CAOS_RESEARCH/problems/dynamical-systems/central-configurations/experiments/EXP-004-valuation-equation-screening
OUT=$EXP/artifacts/comet-table.txt
: > $OUT
for f in out-*.out; do
  [ -s "$f" ] || { echo "$f EMPTY-OR-MISSING" >> $OUT; continue; }
  python3 $EXP/comet_analysis.py "$f" >> $OUT 2>&1
done
cat $OUT
