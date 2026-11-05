"""EXP-012 addendum 4: upper bound pd(R_3) <= 3 by designated relaxation.

Step 1 regenerates a map of R_2 with two bad vertices (cardinality bound 2; the R_2 record of
run_ring.py kept the bad blocks but not the vertices) and reads the local index of the bad vertex
in each B-block. Step 2 relaxes exactly one vertex in each of the three B-blocks of R_3 at that
local index (then at the next local indices, at most four combinations). Writes
artifacts/r3-upper.json.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBLEM = HERE.parents[1]
sys.path.insert(0, str(PROBLEM / "code"))

from pcclib import checkers, encoders, graphs, poles, relaxed, rings, solver  # noqa: E402

HEAVY = Path("E:/_Datos/caos-research/petersen-coloring/EXP-012/rings")
DATA = PROBLEM / "data"
OUT = HERE / "artifacts" / "r3-upper.json"


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def bad_vertices(g, images):
    stars = {frozenset(x) for x in graphs.petersen().incidence()}
    inc = g.incidence()
    return [w for w in range(g.n) if len({images[e] for e in inc[w]}) != 3 or frozenset(images[e] for e in inc[w]) not in stars]


def ring(t):
    g52 = graphs.load_edgelist(DATA / "gjmmm-52.edgelist")
    A = poles.pole(g52, removed_edges=(0, 4))
    B = poles.pole(g52, removed_vertices=(2, 7))
    uside = tuple(j for j, (w, ei) in enumerate(B.dangling) if 2 in g52.edges[ei])
    vside = tuple(j for j, (w, ei) in enumerate(B.dangling) if 7 in g52.edges[ei])
    return rings.ring_of_poles([(A, ((0, 1), (2, 3))), (B, (uside, vside))] * t)


def main() -> None:
    out: dict = {}
    R2, b2 = ring(2)
    assert R2.digest() == graphs.load_edgelist(HEAVY / "R2.edgelist").digest()
    f = encoders.petersen_coloring(R2, defect_bound=2)
    f.write(HEAVY / "R2_pd_le2_rerun.cnf")
    s = solver.solve(HEAVY / "R2_pd_le2_rerun.cnf", HEAVY / "R2_pd_le2_rerun.drat", 3600, want_proof=False)
    if s["status"] != "SAT":
        out["R2_witness"] = {"status": s["status"], "seconds": s["seconds"]}
        OUT.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8", newline="\n")
        log(f"R2 witness not regenerated: {s['status']}")
        return
    images = checkers.edge_color_map(set(s["model"]), f.names, len(R2.edges), 15, prefix="y")
    bad = bad_vertices(R2, images)
    local = sorted({bl.index(w) for bl in b2 for w in bad if w in bl})
    out["R2_witness"] = {"status": "SAT", "seconds": s["seconds"], "bad_vertices": bad,
                         "bad_blocks": sorted(i for i, bl in enumerate(b2) for w in bad if w in bl), "local_indices": local}
    log(f"R2 witness: bad {bad}, local indices {local}")
    OUT.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8", newline="\n")

    R3, b3 = ring(3)
    assert R3.digest() == graphs.load_edgelist(HEAVY / "R3.edgelist").digest()
    bblocks = [i for i in range(len(b3)) if i % 2 == 1]
    candidates = list(dict.fromkeys(local + list(range(len(b3[1])))))[:4]
    out["R3_tries"] = []
    for li in candidates:
        relax = {b3[i][li] for i in bblocks}
        f = relaxed.petersen_relaxed_vertices(R3, relax)
        stem = f"R3_upper_local{li}"
        f.write(HEAVY / f"{stem}.cnf")
        s = solver.solve(HEAVY / f"{stem}.cnf", HEAVY / f"{stem}.drat", 1800, want_proof=False)
        item = {"local_index": li, "relaxed": sorted(relax), "status": s["status"], "seconds": s["seconds"]}
        if s["status"] == "SAT":
            images = checkers.edge_color_map(set(s["model"]), f.names, len(R3.edges), 15, prefix="y")
            item["checker_defect"] = checkers.petersen_defect(R3, images)
            item["bad_vertices"] = bad_vertices(R3, images)
        out["R3_tries"].append(item)
        OUT.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8", newline="\n")
        log(f"R3 local {li}: {item['status']} {item.get('checker_defect')}")
        if item.get("checker_defect") == 3:
            out["pd_R3"] = 3
            break
    OUT.write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
