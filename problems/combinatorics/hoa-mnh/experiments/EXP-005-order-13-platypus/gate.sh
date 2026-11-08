#!/usr/bin/env bash
G=~/caos-nauty/genhypo/gen_hypohamiltonian-1.2.1/gen_hypohamiltonian
for n in ${@}; do
  start=$(date +%s)
  $G $n platypus 2> /tmp/gh$n.err | ~/caos-nauty/mc2g6 > /tmp/plat$n.g6
  cnt=$(wc -l < /tmp/plat$n.g6)
  m=$(~/caos-nauty/mnh < /tmp/plat$n.g6 2>&1 >/tmp/mnh$n.txt)
  echo "order $n: platypuses $cnt; mnh filter: $m; seconds=$(( $(date +%s) - start ))"
  tail -2 /tmp/gh$n.err
done
