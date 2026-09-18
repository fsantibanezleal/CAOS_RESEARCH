import sys, itertools
sys.path.insert(0, r"E:/_Temp/caos-research-newproblem/problems/combinatorics/petersen-coloring/code")
from pcclib import graphs, invariants
D = r"E:/_Temp/caos-research-newproblem/problems/combinatorics/petersen-coloring/data/"
for name, fn in (("G52b", "gjmmmu-52-b.edgelist"), ("G68", "hog-57280-68.edgelist")):
    g = graphs.load_edgelist(D + fn)
    adj = g.adjacency()
    # all 5-cycles through each vertex
    cycles = set()
    for a in range(g.n):
        for b in adj[a]:
            for c in adj[b]:
                if c == a: continue
                for d in adj[c]:
                    if d in (a, b): continue
                    for e in adj[d]:
                        if e in (a, b, c): continue
                        if a in adj[e]:
                            cycles.add(frozenset((a, b, c, d, e)))
    found = None
    for c1, c2 in itertools.combinations(sorted(cycles, key=sorted), 2):
        if len(c1 & c2) == 2:
            S = set(c1 | c2)
            bnd = invariants.boundary_edges(g, S)
            if len(bnd) == 4 and invariants.is_cycle_separating(g, bnd):
                found = (sorted(S), tuple(bnd)); break
    print(name, "5-cycles", len(cycles), "cycle-separating 4-cut:", found)
