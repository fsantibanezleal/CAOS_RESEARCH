"""Check every SAT model in artifacts/cfg-d*.jsonl with networkx, independently of z3.

For each model: order 2d+3, triangle-free, maximum degree <= d, exactly d*d+d+2 edges; then the prediction of
Theorem 2: two vertices share d neighbours (a K_(2,d)), and the complement is not (d+2)-connected.
Writes artifacts/models-check.json.
"""
import itertools
import json
from pathlib import Path

import networkx as nx

HERE = Path(__file__).resolve().parent
out = []
for path in sorted((HERE / "artifacts").glob("cfg-d*.jsonl")):
    for line in path.read_text(encoding="utf-8").splitlines():
        rec = json.loads(line)
        if rec["result"] != "sat":
            continue
        d = rec["d"]
        n = 2 * d + 3
        F = nx.Graph()
        F.add_nodes_from(range(n))
        F.add_edges_from(map(tuple, rec["edges"]))
        tri = sum(nx.triangles(F).values()) // 3
        k2d = [(u, v) for u, v in itertools.combinations(range(n), 2)
               if len(set(F[u]) & set(F[v])) >= d]
        kappa = nx.node_connectivity(nx.complement(F))
        row = {"d": d, "config": rec["config"], "mode": rec["mode"], "order": F.number_of_nodes(),
               "edges": F.number_of_edges(), "triangles": tri, "max_degree": max(dict(F.degree()).values()),
               "k2d_pairs": len(k2d), "complement_connectivity": kappa}
        row["valid_extremal"] = (row["order"] == n and row["edges"] == d * d + d + 2 and tri == 0
                                 and row["max_degree"] <= d)
        row["theorem_holds"] = len(k2d) > 0 and kappa <= d + 1
        out.append(row)
        print(row)
(HERE / "artifacts" / "models-check.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
print("all valid and consistent:", all(r["valid_extremal"] and r["theorem_holds"] for r in out), len(out))
