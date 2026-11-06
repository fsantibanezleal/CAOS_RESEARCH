"""EXP-001 gate 3: independent re-check of the graphs mnh.c reports, by plain backtracking (no subset DP).

For every line of artifacts/mnh-n<N>.txt: decode the graph6 string, then verify by depth-first backtracking that
(a) the graph has no Hamilton cycle, (b) every nonadjacent pair is joined by a Hamilton path, (c) the
circumference, and the set of longest-cycle vertex sets, equal what mnh.c printed (circumference and count), and
(d) the residual flags hoa, q2, q3 and maxcomp equal mnh.c's. Exits 1 on any disagreement.

Usage: python verify.py N [N ...]
"""
import sys
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent


def decode(g6):
    data = [ord(c) - 63 for c in g6]
    n = data[0]
    bits = []
    for x in data[1:]:
        bits.extend((x >> (5 - i)) & 1 for i in range(6))
    adj = [set() for _ in range(n)]
    k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]:
                adj[i].add(j)
                adj[j].add(i)
            k += 1
    return n, adj


def ham_path(adj, verts, a, b):
    """Is there a path from a to b visiting exactly the vertex set verts?"""
    target = len(verts)

    def dfs(v, seen):
        if len(seen) == target:
            return v == b
        for w in adj[v]:
            if w in verts and w not in seen and (w != b or len(seen) == target - 1):
                seen.add(w)
                if dfs(w, seen):
                    return True
                seen.remove(w)
        return False

    return dfs(a, {a})


def cycle_on(adj, verts):
    if len(verts) < 3:
        return False
    s = min(verts)
    return any(ham_path(adj, verts, s, t) for t in adj[s] if t in verts)


def components(adj, R):
    left, comps = set(R), []
    while left:
        stack, comp = [left.pop()], set()
        while stack:
            v = stack.pop()
            comp.add(v)
            for w in adj[v]:
                if w in left:
                    left.remove(w)
                    stack.append(w)
        comps.append(comp)
    return comps


def check(line):
    g6, *fields = line.split()
    got = dict(f.split("=") for f in fields)
    n, adj = decode(g6)
    V = set(range(n))
    if cycle_on(adj, V):
        return "Hamiltonian"
    for u, v in combinations(range(n), 2):
        if v not in adj[u] and not ham_path(adj, V, u, v):
            return f"pair {u},{v} not joined"
    c, sets = 0, []
    for size in range(n, 2, -1):
        sets = [set(S) for S in combinations(range(n), size) if cycle_on(adj, set(S))]
        if sets:
            c = size
            break
    hoa, q2, q3, maxcomp = 1, 1, 0, 0
    for S in sets:
        comps = components(adj, V - S)
        complete = [all(adj[x] >= comp - {x} for x in comp) for comp in comps]
        if not (len(comps) == 1 and complete[0]):
            hoa = 0
        if not all(complete):
            q2 = 0
        if len(comps) == 1 and not complete[0]:
            q3 = 1
        maxcomp = max(maxcomp, len(comps))
    mine = {"c": c, "sets": len(sets), "hoa": hoa, "q2": q2, "q3": q3, "maxcomp": maxcomp}
    diff = {k: (got[k], v) for k, v in mine.items() if int(got[k]) != v}
    return f"differs {diff}" if diff else None


bad = 0
for N in sys.argv[1:]:
    lines = (HERE / "artifacts" / f"mnh-n{N}.txt").read_text(encoding="utf-8").split("\n")
    lines = [ln for ln in lines if ln.strip()]
    errs = [(ln.split()[0], e) for ln in lines if (e := check(ln))]
    bad += len(errs)
    print(f"n={N}: {len(lines)} graphs re-checked, disagreements {len(errs)}", errs[:3], flush=True)
sys.exit(1 if bad else 0)
