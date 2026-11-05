"""The cut code of the Petersen graph and its cosets: the charge space of the charge formulation.

Prints the dimension of the cut space, the weight distribution of coset leaders, the orbits of
Aut(P) on cosets with their leader weights, which orbit the pairs of edges at line-graph distance
1, 2, 3 fall in, which orbits the vertex triples (labels at a bad vertex) fall in, and a
description of the weight-3 cosets. Writes code/probes/cut_code_cosets.json. No solver.
"""

from __future__ import annotations

import itertools
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from pcclib import automorphisms, graphs, poles  # noqa: E402

P = graphs.petersen()
M = len(P.edges)
inc = P.incidence()
stars = [sum(1 << e for e in inc[v]) for v in range(P.n)]
basis: list[int] = []
for s in stars:
    x = s
    for b in basis:
        x = min(x, x ^ b)
    if x:
        basis.append(x)
        basis.sort(reverse=True)


def red(x: int) -> int:
    for b in basis:
        x = min(x, x ^ b)
    return x


weight = [bin(x).count("1") for x in range(1 << M)]
leader: dict[int, int] = {}
for x in range(1 << M):
    c = red(x)
    if c not in leader or weight[x] < weight[leader[c]]:
        leader[c] = x
auts = automorphisms.automorphisms(P)
idx = {e: i for i, e in enumerate(P.edges)}
eperm = [[idx[(min(a[u], a[v]), max(a[u], a[v]))] for (u, v) in P.edges] for a in auts]


def act(p, x):
    y = 0
    for i in range(M):
        if x >> i & 1:
            y |= 1 << p[i]
    return y


orbit_of: dict[int, int] = {}
orbits: list[list[int]] = []
for c in sorted(leader, key=lambda c: (weight[leader[c]], c)):
    if c in orbit_of:
        continue
    orb = sorted({red(act(p, c)) for p in eperm})
    for d in orb:
        orbit_of[d] = len(orbits)
    orbits.append(orb)
dist = poles.line_distances()
pair_orbits = {}
for d in (1, 2, 3):
    pair_orbits[d] = Counter(orbit_of[red((1 << x) | (1 << y))] for x, y in itertools.combinations(range(M), 2) if dist[x][y] == d)
triple_orbits = Counter()
for x, y, z in itertools.combinations(range(M), 3):
    triple_orbits[orbit_of[red((1 << x) | (1 << y) | (1 << z))]] += 1
repeated = Counter(orbit_of[red(1 << y)] for y in range(M))
w3 = [c for c in leader if weight[leader[c]] == 3]
w3_leaders = {c: sorted({x for x in range(1 << M) if weight[x] == 3 and red(x) == c}) for c in w3}
w3_desc = {}
for c, xs in w3_leaders.items():
    kinds = Counter()
    for x in xs:
        es = [i for i in range(M) if x >> i & 1]
        ds = sorted(dist[a][b] for a, b in itertools.combinations(es, 2))
        kinds[tuple(ds)] += 1
    w3_desc[str(c)] = {"weight3_representatives": len(xs), "pairwise_line_distances": {str(k): v for k, v in kinds.items()}}
out = {
    "cut_space_dimension": len(basis),
    "classes": len(leader),
    "leader_weight_distribution": dict(Counter(weight[leader[c]] for c in leader)),
    "orbits": [{"size": len(o), "leader_weight": weight[leader[o[0]]]} for o in orbits],
    "pairs_by_distance_to_orbit": {str(d): {str(k): v for k, v in c.items()} for d, c in pair_orbits.items()},
    "distinct_triples_to_orbit": {str(k): v for k, v in triple_orbits.items()},
    "repeated_label_vertex_x_x_y_to_orbit": {str(k): v for k, v in repeated.items()},
    "weight3_cosets": w3_desc,
}
(HERE / "cut_code_cosets.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8", newline="\n")
print(json.dumps(out, indent=1))
