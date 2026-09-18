"""EXP-010 addendum 2: Petersen colorability and defect witnesses of dot products of G52 with itself."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBLEM = HERE.parents[1]
sys.path.insert(0, str(PROBLEM / "code"))
sys.path.insert(0, str(HERE))

from pcclib import checkers, encoders, graphs, invariants, solver  # noqa: E402
from run import HEAVY, load, pair_orbit_representatives  # noqa: E402


def dot_product(g: graphs.Graph, e1: int, e2: int, h: graphs.Graph, uv: int) -> graphs.Graph:
    a, b = g.edges[e1]
    c, d = g.edges[e2]
    u, v = h.edges[uv]
    hadj = h.adjacency()
    u1, u2 = [x for x in hadj[u] if x != v]
    v1, v2 = [x for x in hadj[v] if x != u]
    keep = [x for x in range(h.n) if x not in (u, v)]
    loc = {x: g.n + i for i, x in enumerate(keep)}
    edges = [e for i, e in enumerate(g.edges) if i not in (e1, e2)]
    edges += [(loc[x], loc[y]) for x, y in h.edges if u not in (x, y) and v not in (x, y)]
    edges += [(a, loc[u1]), (b, loc[u2]), (c, loc[v1]), (d, loc[v2])]
    return graphs.Graph.from_edges(edges)


def main() -> None:
    g = load("G52")
    reps = pair_orbit_representatives(g)[:5]
    out = {}
    (HEAVY / "dot").mkdir(parents=True, exist_ok=True)
    for uv in (0, 1):
        for e1, e2 in reps:
            name = f"D_{e1}_{e2}_{uv}"
            d = dot_product(g, e1, e2, g, uv)
            rec = {"n": d.n, "cubic": d.is_cubic(), "girth": invariants.girth(d), "edge_connectivity": invariants.edge_connectivity(d), "digest": d.digest()}
            f = encoders.petersen_coloring(d)
            cnf = HEAVY / "dot" / f"{name}_pd0.cnf"
            f.write(cnf)
            r = solver.solve(cnf, HEAVY / "dot" / f"{name}_pd0.drat", 1800)
            rec["bound0"] = {"status": r["status"], "verified": r.get("drat_trim_verified"), "seconds": r["seconds"]}
            if r["status"] == "UNSAT":
                for bound in (2, 3, 4):
                    f = encoders.petersen_coloring(d, defect_bound=bound)
                    cnf = HEAVY / "dot" / f"{name}_pd{bound}.cnf"
                    f.write(cnf)
                    r2 = solver.solve(cnf, HEAVY / "dot" / f"{name}_pd{bound}.drat", 600, want_proof=False)
                    entry = {"status": r2["status"], "seconds": r2["seconds"]}
                    if r2["status"] == "SAT":
                        images = checkers.edge_color_map(set(r2["model"]), f.names, len(d.edges), 15, prefix="y")
                        entry["checker_defect"] = checkers.petersen_defect(d, images)
                    rec[f"bound{bound}"] = entry
                    if r2["status"] == "SAT":
                        break
            out[name] = rec
            print(time.strftime("%H:%M:%S"), name, rec, flush=True)
            (HERE / "artifacts" / "dot-products.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
