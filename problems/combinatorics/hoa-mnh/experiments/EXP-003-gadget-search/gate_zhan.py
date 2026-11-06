"""EXP-003 known-answer gate: Zhan's gadget (A_18, vertex 18) must show d = 2 and a non-clique omitted set.

A_17 on {1..18} minus {8}, upper neighbourhoods from Zhan arXiv:2608.00957v3 Section 2 (transcribed in the
2026-09-02 dossier); A_18 = K_1 join A_17 with the new vertex 8. Zhan: for distinct p, q in N(18) = {1, 8, 15}
the longest (p, q)-path of B_17 = A_18 - 18 has order 15 (Lemma 2(iii)), and the omitted pair is {16, 17}
(Lemma 6: the residual w16 + w17 = 2K_1). Also checks Lemma 2(ii) (B_17 homogeneously traceable).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gadgets import dp_invariants, is_clique  # noqa: E402

GAMMA = {1: [2, 3, 11, 15, 18], 2: [3, 14, 16], 3: [4, 5], 4: [5, 12, 17], 5: [6, 7, 11, 15], 6: [7],
         9: [10, 11], 10: [11], 11: [12, 13], 12: [13, 17], 13: [14, 15], 14: [15, 16], 15: [18]}
verts = [v for v in range(1, 19)]           # 1..18 including 8
edges = {(a, b) for a, bs in GAMMA.items() for b in bs}
edges |= {(8, v) for v in verts if v != 8}  # 8 is the universal vertex of A_18
x = 18
rest = [v for v in verts if v != x]
idx = {v: i for i, v in enumerate(rest)}
adj = [set() for _ in rest]
for a, b in edges:
    if x in (a, b):
        continue
    adj[idx[a]].add(idx[b])
    adj[idx[b]].add(idx[a])
N = sorted(idx[a if b == x else b] for a, b in edges if x in (a, b))
print("N(18) =", sorted(rest[i] for i in N), "(Zhan: [1, 8, 15])")
traceable, homog, starts, d, nonclique = dp_invariants(len(rest), adj, N)
print(f"|B_17| = {len(rest)}, traceable {traceable}, homogeneously traceable {homog}, d = {d}, "
      f"non-clique omitted set {nonclique}")
print("16 ~ 17:", idx[17] in adj[idx[16]], "(Zhan: nonadjacent)")
ok = d == 2 and nonclique and homog and sorted(rest[i] for i in N) == [1, 8, 15]
print("GATE", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
