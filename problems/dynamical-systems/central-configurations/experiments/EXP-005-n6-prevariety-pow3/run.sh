#!/usr/bin/env bash
# EXP-005: n = 6 tropical prevariety (detached multi-day run).
# Usage: run.sh <label> <bits> <threads> <v1..v6>
#   e.g. run.sh pow2-b64 64 15 1 2 4 8 16 32
#        run.sh pow3-b0   0 15 1 3 9 27 81 243
# Attempt 1 (pow3, --bits 64, 30 threads) ABORTED after 6.5 min with
# gfan::MVMachineIntegerOverflow ("Overflow ... in tropical homotopy"): powers of 3
# at n = 6 reach t^243 and exceed the machine-integer fast path. Recorded in the
# verdict; the two follow-up variants are the evidence-driven redirect (EXP-004
# screening showed powers of 2 and primes are comet-pointed at n = 5, with much
# smaller exponents), plus the arbitrary-precision rerun JL25 themselves describe.
set -uo pipefail
LABEL=$1; BITS=$2; THREADS=$3; shift 3
W=~/exp005 && mkdir -p $W && cd $W
HEAVY=/mnt/e/_Datos/caos-research/central-configurations/EXP-005
mkdir -p $HEAVY
S=status-$LABEL.log
echo "$(date -Is) EXP-005/$LABEL start (bits=$BITS threads=$THREADS valuations: $*)" | tee -a $S

[ -f system-n6.txt ] || gfan _nbody -N6 --masses --alsosymmetric --cayleymenger2 > system-n6.txt
sedargs=(-e "s/Q\[m1,m2,m3,m4,m5,m6,/Q(t)[/")
i=1
for v in "$@"; do sedargs+=(-e "s/\bm$i\b/t^$v/g"); i=$((i+1)); done
sed "${sedargs[@]}" system-n6.txt > input-$LABEL.txt

timeout 604800 gfan _tropicalprevariety --usevaluation -j$THREADS --mint --minx --bits $BITS \
    < input-$LABEL.txt > prevariety-$LABEL.out 2> prevariety-$LABEL.err
rc=$?
echo "$(date -Is) EXP-005/$LABEL finished rc=$rc" | tee -a $S
if [ $rc -eq 0 ] && [ -s prevariety-$LABEL.out ]; then
  cp prevariety-$LABEL.out $HEAVY/
  grep -a -A2 "F_VECTOR" prevariety-$LABEL.out | head -3 | tee -a $S
  sha256sum system-n6.txt input-$LABEL.txt prevariety-$LABEL.out >> hashes-$LABEL.txt
else
  tail -3 prevariety-$LABEL.err | tee -a $S
fi
