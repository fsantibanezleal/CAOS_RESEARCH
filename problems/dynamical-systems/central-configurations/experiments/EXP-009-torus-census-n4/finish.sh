#!/usr/bin/env bash
# EXP-009 continuation, detached so the declared budget is enforced even if the
# controlling shell dies (methodology/12 P6: 3600 s per route, no silent retries).
# Route A was launched by run.py and is enforced here; route B follows.
set -uo pipefail
W=/root/exp009
ART=/mnt/d/_Repos/Research_Caos/CAOS_RESEARCH/problems/dynamical-systems/central-configurations/experiments/EXP-009-torus-census-n4/artifacts
S=$ART/finish-log.txt
: > $S
echo "$(date -Is) finish.sh start" >> $S

# --- enforce the route-A cap
pid=$(pgrep -f "msolve -f $W/routeA.ms" | head -1)
if [ -n "${pid:-}" ]; then
  start_s=$(ps -o etimes= -p $pid | tr -d ' ')
  remain=$(( 3600 - start_s ))
  [ $remain -lt 0 ] && remain=0
  echo "$(date -Is) routeA running ${start_s}s, allowing ${remain}s more (cap 3600)" >> $S
  sleep $remain
  if kill -0 $pid 2>/dev/null; then
    kill -9 $pid 2>/dev/null
    echo "$(date -Is) routeA CAP STRUCK at 3600 s: killed, recorded inconclusive-cap" >> $S
  fi
fi
if [ -s $W/routeA.out ]; then
  echo "$(date -Is) routeA produced output" >> $S
  cp $W/routeA.out $ART/routeA.out
  head -c 200 $W/routeA.out >> $S
fi

# --- route B: the Hampton-Moeckel z-system (written by run.py if it got that far)
if [ -f $W/routeB.ms ]; then
  echo "$(date -Is) routeB start (cap 3600)" >> $S
  timeout 3600 msolve -f $W/routeB.ms -o $W/routeB.out
  rc=$?
  echo "$(date -Is) routeB finished rc=$rc" >> $S
  [ -s $W/routeB.out ] && cp $W/routeB.out $ART/routeB.out && head -c 200 $W/routeB.out >> $S
else
  echo "$(date -Is) routeB input not present; run.py did not reach it" >> $S
fi
echo "$(date -Is) finish.sh done" >> $S
