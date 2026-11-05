"""Cyclic edge connectivity of the ten dot products G52 . G52 of EXP-010 (addendum 2).

Rebuilds each graph with EXP-010's `dot_product`, checks its digest against
`EXP-010/artifacts/dot-products.json`, searches exhaustively for a cycle-separating edge cut of
size at most 3 (`invariants.cyclic_edge_cut_below`, the routine used in EXP-001), and checks that
the four edges joining the two parts form a cycle-separating 4-cut. Writes
`EXP-011/artifacts/dot-products-cyclic-connectivity.json`. One process per graph.
"""

from __future__ import annotations

import json
import sys
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBLEM = HERE.parents[1]
sys.path.insert(0, str(PROBLEM / "code"))
sys.path.insert(0, str(PROBLEM / "experiments" / "EXP-010-sublinear-approximation"))

from pcclib import graphs, invariants  # noqa: E402
from run_dot import dot_product  # noqa: E402

EXP010 = PROBLEM / "experiments" / "EXP-010-sublinear-approximation" / "artifacts"
OUT = PROBLEM / "experiments" / "EXP-011-adjacent-pair-criticality" / "artifacts" / "dot-products-cyclic-connectivity.json"


def check(name: str) -> dict:
    g52 = graphs.load_edgelist(PROBLEM / "data" / "gjmmm-52.edgelist")
    _, e1, e2, uv = name.split("_")
    d = dot_product(g52, int(e1), int(e2), g52, int(uv))
    first = set(range(g52.n))
    joining = tuple(i for i, (a, b) in enumerate(d.edges) if (a in first) != (b in first))
    small = invariants.cyclic_edge_cut_below(d, 4)
    return {"name": name, "digest": d.digest(), "n": d.n, "girth": invariants.girth(d),
            "edge_connectivity": invariants.edge_connectivity(d),
            "cycle_separating_cut_below_4": list(small) if small else None,
            "joining_edges": list(joining), "joining_cut_cycle_separating": invariants.is_cycle_separating(d, joining)}


def main() -> None:
    recorded = json.loads((EXP010 / "dot-products.json").read_text(encoding="utf-8"))
    with Pool(len(recorded)) as pool:
        rows = pool.map(check, sorted(recorded))
    for r in rows:
        r["digest_matches_exp010"] = r["digest"] == recorded[r["name"]]["digest"]
        r["cyclic_edge_connectivity"] = 4 if (r["cycle_separating_cut_below_4"] is None and r["joining_cut_cycle_separating"]) else None
    OUT.write_text(json.dumps(rows, indent=1) + "\n", encoding="utf-8", newline="\n")
    for r in rows:
        print(r["name"], r["digest_matches_exp010"], r["girth"], r["edge_connectivity"], r["cycle_separating_cut_below_4"], r["joining_cut_cycle_separating"], r["cyclic_edge_connectivity"])


if __name__ == "__main__":
    main()
