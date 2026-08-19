#!/usr/bin/env bash
# One-shot relauncher used after WSL restarts (see run08-resume.sh header).
set -uo pipefail
EXP=/mnt/e/_Temp/wt-cc-research/problems/dynamical-systems/central-configurations/experiments/EXP-005-n6-prevariety-pow3
mkdir -p ~/exp005b
tr -d '\r' < "$EXP/run08-resume.sh" > ~/exp005b/run08-resume.sh
tr -d '\r' < "$EXP/run08.sh" > ~/exp005b/run08.sh
chmod +x ~/exp005b/run08-resume.sh ~/exp005b/run08.sh
cd ~/exp005b
nohup ./run08-resume.sh pow2-08b64r 64 10 >> nohup-r1.log 2>&1 &
nohup ./run08.sh pow3-08b0 0 10 1 3 9 27 81 243 >> nohup-r2.log 2>&1 &
sleep 6
ps -eo pid,etime,args | grep gfan08 | grep -v grep
