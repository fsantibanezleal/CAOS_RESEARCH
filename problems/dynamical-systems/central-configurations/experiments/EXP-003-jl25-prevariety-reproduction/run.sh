#!/usr/bin/env bash
# EXP-003 recorded pipeline (WSL2 Ubuntu 24.04; gfan 0.7 built from the author
# tarball with GMP + libcdd-dev; two source patches: `#include <cstdint>` prepended
# to src/gfanlib_z.h and src/gfanlib_q.h for gcc 13). Hashes: artifacts/hashes.txt.
# Reproduces Jensen-Leykin arXiv:2301.02305v2 Section 4.1/4.1.1 exactly.
set -euo pipefail
mkdir -p ~/exp003 && cd ~/exp003

# System: 20 asymmetric AC + 10 symmetric AC + 5 planar Cayley-Menger, n = 5.
gfan _nbody -N5 --masses --alsosymmetric --cayleymenger2 > system-n5.txt

# Valuation substitutions (masses into Q(t) with chosen valuations).
sed -e"s/Q\[m1,m2,m3,m4,m5,/Q(t)[/" \
    -e"s/\bm1\b/t^1/g" -e"s/\bm2\b/t^3/g" -e"s/\bm3\b/t^9/g" \
    -e"s/\bm4\b/t^27/g" -e"s/\bm5\b/t^81/g" system-n5.txt > input-pow3.txt
sed -e"s/Q\[m1,m2,m3,m4,m5,/Q(t)[/" \
    -e"s/\bm1\b/t^1/g" -e"s/\bm2\b/t^4/g" -e"s/\bm3\b/t^9/g" \
    -e"s/\bm4\b/t^16/g" -e"s/\bm5\b/t^25/g" system-n5.txt > input-squares.txt

# Tropical prevarieties (min convention, valuation-aware, 64-bit fast pass).
gfan _tropicalprevariety --usevaluation -j30 --mint --minx --bits 64 \
    < input-pow3.txt > prevariety-pow3.out
gfan _tropicalprevariety --usevaluation -j30 --mint --minx --bits 64 \
    < input-squares.txt > prevariety-squares.out

# Pointedness check (powers-of-3): unbounded directions must be all-non-positive.
awk '/^RAYS/{f=1;next} f&&/^$/{exit} f{print}' prevariety-pow3.out > rays-pow3.txt
python3 check_pointedness.py prevariety-pow3.out
