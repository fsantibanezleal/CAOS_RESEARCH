import sys, json, itertools, collections
sys.path.insert(0, r"E:/_Temp/caos-research-newproblem/problems/combinatorics/petersen-coloring/code")
from pcclib import graphs, automorphisms as A
P = graphs.petersen()
E = P.edges
inc = P.incidence()
# cut space basis: stars; class of a vector = its coset; represent cosets by reducing modulo the cut space (Gaussian elimination)
stars = [sum(1 << e for e in inc[v]) for v in range(10)]
basis = []
for s in stars:
    x = s
    for b in basis:
        x = min(x, x ^ b)
    if x:
        basis.append(x)
        basis.sort(reverse=True)
def reduce(x):
    for b in basis:
        x = min(x, x ^ b)
    return x
print("cut space dim", len(basis))
classes = {reduce(x) for x in range(1 << 15)}
print("number of classes", len(classes))
au = A.automorphisms(P)
idx = {e: i for i, e in enumerate(E)}
eperm = [[idx[(min(a[u], a[v]), max(a[u], a[v]))] for (u, v) in E] for a in au]
def act(p, x):
    y = 0
    for i in range(15):
        if x >> i & 1:
            y |= 1 << p[i]
    return y
orbit_of = {}
orbits = []
for c in sorted(classes):
    if c in orbit_of:
        continue
    orb = {reduce(act(p, c)) for p in eperm}
    for d in orb:
        orbit_of[d] = len(orbits)
    # minimal weight representative description
    minw = min(bin(x).count("1") for x in range(1 << 15) if reduce(x) == c) if c else 0
    orbits.append((len(orb), minw))
print("orbits (size, min weight of a representative):", orbits)
# zero-sum triples of nonzero classes by orbit type
zs = collections.Counter()
nz = [c for c in classes if c]
for a, b in itertools.combinations(nz, 2):
    c = reduce(a ^ b)
    if c and c != a and c != b:
        zs[tuple(sorted((orbit_of[a], orbit_of[b], orbit_of[c])))] += 1
print("zero-sum triples by orbit types:", dict(zs))
# classes of the bad triples in the stored G52 pair witnesses
d = json.load(open(r"E:/_Temp/caos-research-newproblem/problems/combinatorics/petersen-coloring/experiments/EXP-006-critical-vertices/artifacts/pairs-G52.json", encoding="utf-8"))
g = graphs.load_edgelist(r"E:/_Temp/caos-research-newproblem/problems/combinatorics/petersen-coloring/data/gjmmm-52.edgelist")
ginc = g.incidence()
adj = g.adjacency()
cnt = collections.Counter(); cnt_adj = collections.Counter(); mism = 0
for key, e in d["pairs"].items():
    if e["status"] != "SAT":
        continue
    u, v = map(int, key.split("-"))
    w = e["witness"]
    cu = reduce(sum((1 << w[i]) for i in ginc[u]) if len({w[i] for i in ginc[u]}) == 3 else __import__("functools").reduce(lambda a, b: a ^ b, [1 << w[i] for i in ginc[u]]))
    cv = reduce(__import__("functools").reduce(lambda a, b: a ^ b, [1 << w[i] for i in ginc[v]]))
    cu = reduce(__import__("functools").reduce(lambda a, b: a ^ b, [1 << w[i] for i in ginc[u]]))
    if cu != cv:
        mism += 1
    (cnt_adj if v in adj[u] else cnt)[orbit_of[cu]] += 1
print("pairs with unequal classes (must be 0):", mism)
print("orbit type of the bad class, non-adjacent pairs:", dict(cnt), " adjacent pairs:", dict(cnt_adj))
