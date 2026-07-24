#!/usr/bin/env bash
# EXP-004 screening grid (WSL; gfan 0.7 from EXP-003, hashes recorded there).
# Grid: n=5 {S1 baseline, S2 asym-only} x {V1..V6}; n=4 S1 x 4 valuations.
# Per-cell outputs: f-vector, pointedness verdict, timing. Heavy raw outputs to E:.
set -uo pipefail
W=~/exp004 && mkdir -p $W && cd $W
EXP=/mnt/d/_Repos/Research_Caos/CAOS_RESEARCH/problems/dynamical-systems/central-configurations/experiments/EXP-004-valuation-equation-screening
HEAVY=/mnt/e/_Datos/caos-research/central-configurations/EXP-004
mkdir -p $EXP/artifacts $HEAVY
CHECK=$EXP/../EXP-003-jl25-prevariety-reproduction/check_pointedness.py

gfan _nbody -N5 --masses --alsosymmetric --cayleymenger2 > sys-n5-S1.txt
gfan _nbody -N5 --masses --cayleymenger2 > sys-n5-S2.txt
gfan _nbody -N4 --masses --alsosymmetric --cayleymenger2 > sys-n4-S1.txt

subst () { # subst <sysfile> <n> <v1> <v2> ... -> stdout
  local f=$1; shift; local n=$1; shift
  local sedargs=(-e "s/Q\[$(for i in $(seq 1 $n); do printf "m%d," $i; done | sed 's/,$//'),/Q(t)[/")
  local i=1
  for v in "$@"; do sedargs+=(-e "s/\bm$i\b/t^$v/g"); i=$((i+1)); done
  sed "${sedargs[@]}" "$f"
}

runcell () { # runcell <label> <sysfile> <n> <cap> <v...>
  local label=$1 sysf=$2 n=$3 cap=$4; shift 4
  echo "=== $label (valuations: $*)"
  subst $sysf $n "$@" > in-$label.txt
  local t0=$(date +%s)
  timeout $cap gfan _tropicalprevariety --usevaluation -j30 --mint --minx --bits 64 \
      < in-$label.txt > out-$label.out 2> err-$label.txt
  local rc=$? t1=$(date +%s)
  if [ $rc -ne 0 ]; then
    echo "$label CAP-OR-ERROR rc=$rc elapsed=$((t1-t0))s" | tee -a $EXP/artifacts/screening-table.txt
    return
  fi
  local fv=$(grep -a -A1 "^F_VECTOR" out-$label.out | tail -1)
  python3 $CHECK out-$label.out > point-$label.txt 2>&1
  local prc=$? pline=$(cat point-$label.txt | head -1)
  echo "$label | fvec: $fv | pointed(global): $([ $prc -eq 0 ] && echo YES || echo NO) | $pline | ${cap}s-cap | $((t1-t0))s" \
      | tee -a $EXP/artifacts/screening-table.txt
  cp out-$label.out $HEAVY/
}

: > $EXP/artifacts/screening-table.txt
# n=5 S1 baseline
runcell n5-S1-V1pow3    sys-n5-S1.txt 5 2400 1 3 9 27 81
runcell n5-S1-V2squares sys-n5-S1.txt 5 2400 1 4 9 16 25
runcell n5-S1-V3pow2    sys-n5-S1.txt 5 2400 1 2 4 8 16
runcell n5-S1-V4primes  sys-n5-S1.txt 5 2400 2 3 5 7 11
runcell n5-S1-V5arith   sys-n5-S1.txt 5 2400 0 1 2 3 4
runcell n5-S1-V6repeat  sys-n5-S1.txt 5 2400 1 1 9 27 81
# n=5 S2 asymmetric-only
runcell n5-S2-V1pow3    sys-n5-S2.txt 5 2400 1 3 9 27 81
runcell n5-S2-V2squares sys-n5-S2.txt 5 2400 1 4 9 16 25
runcell n5-S2-V3pow2    sys-n5-S2.txt 5 2400 1 2 4 8 16
runcell n5-S2-V4primes  sys-n5-S2.txt 5 2400 2 3 5 7 11
runcell n5-S2-V5arith   sys-n5-S2.txt 5 2400 0 1 2 3 4
runcell n5-S2-V6repeat  sys-n5-S2.txt 5 2400 1 1 9 27 81
# n=4 S1
runcell n4-S1-pow3      sys-n4-S1.txt 4 600 1 3 9 27
runcell n4-S1-pow2      sys-n4-S1.txt 4 600 1 2 4 8
runcell n4-S1-arith     sys-n4-S1.txt 4 600 0 1 2 3
runcell n4-S1-equal     sys-n4-S1.txt 4 600 0 0 0 0

cp sys-n5-S1.txt sys-n5-S2.txt sys-n4-S1.txt $EXP/artifacts/
sha256sum in-*.txt out-*.out > $EXP/artifacts/hashes.txt 2>/dev/null
echo "GRID DONE"
cat $EXP/artifacts/screening-table.txt
