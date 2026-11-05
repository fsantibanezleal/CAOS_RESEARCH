#!/bin/bash
# EXP-007 addendum 6: portfolio solve of one final formula, each configuration writing a DRAT proof;
# the first UNSAT answer wins, the others are stopped, and the winner's proof is checked by drat-trim.
# Runs inside WSL. Usage: portfolio_certify.sh <cnf> <proof-prefix> <result-json> <solve-limit-s> <check-limit-s>
set -u
CNF=$1; PRE=$2; OUT=$3; TS=$4; TC=$5
DT=/mnt/e/_Datos/caos-research/huneke-wiegand/tools/drat-trim/drat-trim
CFGS=(default unsat seed7)
OPTS=("" "--unsat" "--seed=7")
declare -A PID
t0=$(date +%s)
for i in 0 1 2; do
  timeout "$TS" cadical -q ${OPTS[$i]} "$CNF" "$PRE.${CFGS[$i]}.drat" > "$PRE.${CFGS[$i]}.out" 2>&1 &
  PID[${CFGS[$i]}]=$!
done
winner=""; code=""
deadline=$((t0 + TS + 120))
while [ -z "$winner" ] && [ ${#PID[@]} -gt 0 ] && [ "$(date +%s)" -lt "$deadline" ]; do
  sleep 30
  for cfg in "${!PID[@]}"; do
    if ! kill -0 "${PID[$cfg]}" 2>/dev/null; then
      wait "${PID[$cfg]}"; c=$?
      unset "PID[$cfg]"
      if [ "$c" -eq 20 ]; then winner=$cfg; code=$c; break; fi
      if [ "$c" -eq 10 ]; then winner=$cfg; code=$c; break; fi
      echo "config $cfg ended with exit code $c" >&2
    fi
  done
done
for cfg in "${!PID[@]}"; do kill "${PID[$cfg]}" 2>/dev/null; done
solve_s=$(( $(date +%s) - t0 ))
cnf_sha=$(sha256sum "$CNF" | cut -d' ' -f1)
if [ -z "$winner" ]; then
  printf '{"status": "TIMEOUT", "portfolio": "default,unsat,seed7", "solve_seconds": %d, "cnf_sha256": "%s"}\n' "$solve_s" "$cnf_sha" > "$OUT"
  exit 0
fi
if [ "$code" -eq 10 ]; then
  printf '{"status": "SAT", "winner": "%s", "portfolio": "default,unsat,seed7", "solve_seconds": %d, "cnf_sha256": "%s", "model_file": "%s"}
' "$winner" "$solve_s" "$cnf_sha" "$PRE.$winner.out" > "$OUT"
  exit 0
fi
P="$PRE.$winner.drat"
t1=$(date +%s)
chk=$(timeout "$TC" "$DT" "$CNF" "$P" -t "$TC" 2>&1 | tail -3 | tr '\n' ' ' | tr -d '"')
check_s=$(( $(date +%s) - t1 ))
ver=false; case "$chk" in *"s VERIFIED"*) ver=true;; esac
printf '{"status": "%s", "verified": %s, "winner": "%s", "portfolio": "default,unsat,seed7", "solve_seconds": %d, "check_seconds": %d, "cnf_sha256": "%s", "proof_sha256": "%s", "proof_bytes": %d, "drat_trim_tail": "%s"}\n' \
  "$([ $ver = true ] && echo UNSAT || echo UNVERIFIED)" "$ver" "$winner" "$solve_s" "$check_s" "$cnf_sha" "$(sha256sum "$P" | cut -d' ' -f1)" "$(stat -c %s "$P")" "$chk" > "$OUT"
