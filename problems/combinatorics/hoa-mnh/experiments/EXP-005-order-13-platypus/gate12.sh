#!/usr/bin/env bash
# Gate at order 12 in 8 parts, 2 at a time.
G=~/caos-nauty/genhypo/gen_hypohamiltonian-1.2.1/gen_hypohamiltonian
O=${1:?output directory}; mkdir -p $O
start=$(date +%s)
seq 0 7 | xargs -P 2 -I{} bash -c "$G 12 platypus mod {} 8 2> $O/p{}.err | ~/caos-nauty/mc2g6 > $O/p{}.g6"
cat $O/p*.g6 > $O/plat12.g6
echo "order 12: platypuses $(wc -l < $O/plat12.g6); mnh filter: $(~/caos-nauty/mnh < $O/plat12.g6 2>&1 > $O/mnh12.txt); seconds=$(( $(date +%s) - start ))"
