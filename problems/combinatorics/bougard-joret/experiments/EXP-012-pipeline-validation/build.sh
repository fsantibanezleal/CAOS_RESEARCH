#!/bin/bash
# EXP-012 Gate F: rebuild the production binaries from the committed sources with the recorded build lines and
# compare their SHA-256 with the production binaries; build the Gate C harness at ALPHA_BOUND = 2..8.
# Usage (in WSL): bash build.sh <nauty dir> <production filter2> <build dir>
set -euo pipefail
NAUTY=$1; PFILTER=$2; BUILD=$3
HERE=$(cd "$(dirname "$0")" && pwd)
SRC=$HERE/../EXP-006-second-regime-beyond-15
mkdir -p "$BUILD"
OBJS="gtoolsW.o nautyW1.o nautilW1.o naugraphW1.o schreier.o naurng.o"
echo "gcc: $(gcc --version | head -1)"
echo "prune_alpha.c in the nauty dir equal to the committed source: $(cmp -s "$SRC/prune_alpha.c" "$NAUTY/prune_alpha.c" && echo yes || echo NO)"
echo "geng.c sha256: $(sha256sum "$NAUTY/geng.c" | cut -d' ' -f1)"
# filter2, recorded line (EXP-006 verdict): gcc -O2 -o filter2 filter2.c, from the source folder
( cd "$SRC" && gcc -O2 -o "$BUILD/filter2" filter2.c )
echo "filter2 rebuilt $(sha256sum "$BUILD/filter2" | cut -d' ' -f1) production $(sha256sum "$PFILTER" | cut -d' ' -f1)"
# geng_a<A>: the line in prune_alpha.c's header (-O3), and the nauty makefile's CFLAGS (-O4 -mpopcnt -march=native)
CFLAGS=$(sed -n 's/^CFLAGS= *//p' "$NAUTY/makefile")
echo "nauty makefile CFLAGS: $CFLAGS"
for A in 3 4 5 6 7; do
  ( cd "$NAUTY" && gcc -O3 -o "$BUILD/geng_a$A.O3" -DMAXN=WORDSIZE -DWORDSIZE=32 -DPRUNE=prune_alpha -DALPHA_BOUND=$A \
      geng.c prune_alpha.c $OBJS )
  ( cd "$NAUTY" && gcc $CFLAGS -o "$BUILD/geng_a$A" -DMAXN=WORDSIZE -DWORDSIZE=32 -DPRUNE=prune_alpha \
      -DALPHA_BOUND=$A geng.c prune_alpha.c $OBJS )
  echo "geng_a$A production $(sha256sum "$NAUTY/geng_a$A" | cut -d' ' -f1)"
  echo "  rebuilt with the makefile CFLAGS $(sha256sum "$BUILD/geng_a$A" | cut -d' ' -f1)"
  echo "  rebuilt with the header line -O3 $(sha256sum "$BUILD/geng_a$A.O3" | cut -d' ' -f1)"
done
for A in 2 3 4 5 6 7 8; do
  ( cd "$NAUTY" && gcc $CFLAGS -o "$BUILD/prune_test_$A" -DMAXN=WORDSIZE -DWORDSIZE=32 -DALPHA_BOUND=$A -I. \
      "$HERE/prune_test.c" prune_alpha.c $OBJS )
done
echo "harness built for ALPHA_BOUND 2..8"
