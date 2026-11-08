#!/usr/bin/env bash
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
N=~/caos-nauty/nauty2_8_9
G=~/caos-nauty/genhypo
mkdir -p $G && cd $G
ZIP=${1:?path of gen_hypohamiltonian-1.2.1.zip}; python3 -c "import sys, zipfile; zipfile.ZipFile(sys.argv[1]).extractall('.')" "$ZIP"
D=$(find . -maxdepth 2 -name 'gen_hypohamiltonian.c' -printf '%h\n' | head -1); cd $D
( cd $N && make nautyW1.a > /dev/null 2>&1 || true; ls -la nautyW1.a )
cp $N/nausparse.h $N/nauty.h $N/nautyW1.a $N/naututil.h $N/planarity.c $N/naurng.h $N/splay.c $N/planarity.h .
cc -DWORDSIZE=32 -DMAXN=WORDSIZE -mpopcnt -O4 gen_hypohamiltonian.c planarity.c nautyW1.a -o gen_hypohamiltonian 2>&1 | grep -v warning | head -5
ls -la gen_hypohamiltonian
gcc -O2 -o ~/caos-nauty/mc2g6 "$HERE/mc2g6.c"
echo "built in $(pwd)"
