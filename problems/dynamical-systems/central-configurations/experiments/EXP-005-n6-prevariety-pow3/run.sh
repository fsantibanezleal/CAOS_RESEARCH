#!/usr/bin/env bash
# EXP-005: n = 6 tropical prevariety, powers-of-3 valuations (detached multi-day run).
# Launch (detached): wsl -d Ubuntu-24.04 -- bash -lc 'nohup bash /mnt/d/.../run.sh > ~/exp005/nohup.log 2>&1 & disown; echo started'
set -uo pipefail
W=~/exp005 && mkdir -p $W && cd $W
HEAVY=/mnt/e/_Datos/caos-research/central-configurations/EXP-005
mkdir -p $HEAVY
echo "$(date -Is) EXP-005 start (pid $$)" | tee -a status.log
echo $$ > run.pid

gfan _nbody -N6 --masses --alsosymmetric --cayleymenger2 > system-n6.txt
sed -e"s/Q\[m1,m2,m3,m4,m5,m6,/Q(t)[/" \
    -e"s/\bm1\b/t^1/g" -e"s/\bm2\b/t^3/g" -e"s/\bm3\b/t^9/g" \
    -e"s/\bm4\b/t^27/g" -e"s/\bm5\b/t^81/g" -e"s/\bm6\b/t^243/g" \
    system-n6.txt > input-n6-pow3.txt
echo "$(date -Is) system generated: $(sed 's/^[^{]*{//' system-n6.txt | tr -cd ',' | wc -c) commas (+1 = polynomial count)" | tee -a status.log

# checkpointed prevariety run (saveas allows resume after interruption)
timeout 345600 gfan _tropicalprevariety --usevaluation -j30 --mint --minx --bits 64 \
    --saveas checkpoint-n6-pow3.state \
    < input-n6-pow3.txt > prevariety-n6-pow3.out 2> prevariety-n6-pow3.err
rc=$?
echo "$(date -Is) prevariety finished rc=$rc" | tee -a status.log
if [ $rc -eq 0 ]; then
  cp prevariety-n6-pow3.out $HEAVY/
  grep -a -A2 "F_VECTOR" prevariety-n6-pow3.out | head -3 | tee -a status.log
  sha256sum system-n6.txt input-n6-pow3.txt prevariety-n6-pow3.out | tee hashes.txt
fi
echo "$(date -Is) EXP-005 run.sh done" | tee -a status.log
