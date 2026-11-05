"""EXP-012 step 2 (addendum 1): alternating rings R_t(A, B) with A = G52 - e0 - e4 (connectors: ends
of e0 | ends of e4) and B = G52 - {2, 7} (connectors: ends at 2 | ends at 7).

Checks, in order, written to artifacts/ring.json:
 1. the fast cut routine against the exhaustive EXP-001 routine on three graphs of known type;
 2. D(B) under the u|v pairing (SAT per distance; UNSAT with checked proofs);
 3. R_1 has no Petersen coloring (checked proof);
 4. cyclic edge connectivity of R_1, R_2, R_3 (no cycle-separating cut of size at most 3; one
    explicit cycle-separating 4-cut: the two junctions around one block);
 5. consistency: "at most 2 bad vertices" is SAT for R_2 and UNSAT for R_3 (the ring theorem
    predicts pd(R_2) >= 2 and pd(R_3) >= 3).
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBLEM = HERE.parents[1]
sys.path.insert(0, str(PROBLEM / "code"))

from pcclib import checkers, encoders, graphs, invariants, poles, rings, solver  # noqa: E402

ARTIFACTS = HERE / "artifacts"
HEAVY = Path("E:/_Datos/caos-research/petersen-coloring/EXP-012/rings")
DATA = PROBLEM / "data"


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def save(obj: dict) -> None:
    (ARTIFACTS / "ring.json").write_text(json.dumps(obj, indent=1) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    HEAVY.mkdir(parents=True, exist_ok=True)
    out: dict = {}
    g52 = graphs.load_edgelist(DATA / "gjmmm-52.edgelist")

    # 1. validate the fast cut routine
    val = {}
    for name, g in (("G52", g52), ("ring_join_G52_2", graphs.ring_join(g52, 0, 2)),
                    ("K4_frame_G52", graphs.frame_substitution(graphs.k4(), g52, 0))):
        fast = rings.cyclic_cuts_below_4(g)
        slow = invariants.cyclic_edge_cut_below(g, 4)
        val[name] = {"fast_count": len(fast), "fast_first": list(fast[0]) if fast else None,
                     "slow": list(slow) if slow else None,
                     "agree_on_existence": bool(fast) == (slow is not None)}
        log(f"validation {name}: fast {len(fast)} cuts, slow {slow}")
    out["validation"] = val
    save(out)

    # blocks
    A = poles.pole(g52, removed_edges=(0, 4))
    u, v = 2, 7
    assert (min(u, v), max(u, v)) in g52.edges
    B = poles.pole(g52, removed_vertices=(u, v))
    uside = tuple(j for j, (w, ei) in enumerate(B.dangling) if u in g52.edges[ei])
    vside = tuple(j for j, (w, ei) in enumerate(B.dangling) if v in g52.edges[ei])
    assert len(uside) == 2 and len(vside) == 2
    pairA = ((0, 1), (2, 3))
    assert {A.parent.edges[A.dangling[0][1]], A.parent.edges[A.dangling[1][1]]} == {g52.edges[0]}
    pairB = (uside, vside)
    out["blocks"] = {"A": {"removed_edges": [0, 4], "edges": [list(g52.edges[0]), list(g52.edges[4])], "pairing": [list(x) for x in pairA]},
                     "B": {"removed_vertices": [u, v], "pairing": [list(uside), list(vside)],
                           "dangling": [list(x) for x in B.dangling]}}

    # 2. D(B) under the u|v pairing
    reps = poles.distance_representatives()
    dist = poles.line_distances()
    DB = {}
    for d in range(4):
        x, y = reps[d]
        f, yv = poles.pole_formula(B, fixed={uside[0]: x, uside[1]: y})
        stem = f"B_uv_d{d}"
        f.write(HEAVY / f"{stem}.cnf")
        rec = solver.solve(HEAVY / f"{stem}.cnf", HEAVY / f"{stem}.drat", 600)
        item = {"status": rec["status"], "verified": rec.get("drat_trim_verified"), "seconds": rec["seconds"]}
        if rec["status"] == "SAT":
            model = set(rec["model"])
            lab = {k: t for (k, t), var in yv.items() if var in model}
            item["checker_ok"] = poles.check_pole(B, lab)
            item["v_side_distance"] = dist[lab[("d", vside[0])]][lab[("d", vside[1])]]
        DB[str(d)] = item
        log(f"D(B) distance {d}: {item}")
    out["D_B"] = DB
    save(out)

    # 3-5. rings
    out["rings"] = {}
    for t in (1, 2, 3):
        R, blocks = rings.ring_of_poles([(A, pairA), (B, pairB)] * t)
        rec = {"n": R.n, "m": len(R.edges), "cubic": R.is_cubic(), "digest": R.digest(), "girth": invariants.girth(R),
               "edge_connectivity": invariants.edge_connectivity(R)}
        (HEAVY / f"R{t}.edgelist").write_text("".join(f"{a} {b}\n" for a, b in R.edges), encoding="utf-8", newline="\n")
        t0 = time.time()
        cuts = rings.cyclic_cuts_below_4(R)
        rec["cyclic_cuts_below_4"] = [list(c) for c in cuts]
        rec["cut_search_seconds"] = round(time.time() - t0, 1)
        block0 = set(blocks[0])
        four = invariants.boundary_edges(R, block0)
        rec["block0_boundary"] = list(four)
        rec["block0_boundary_cycle_separating"] = invariants.is_cycle_separating(R, four)
        if t == 1:
            f = encoders.petersen_coloring(R)
            f.write(HEAVY / "R1_petersen.cnf")
            s = solver.solve(HEAVY / "R1_petersen.cnf", HEAVY / "R1_petersen.drat", 3600)
            rec["petersen"] = {k: s.get(k) for k in ("status", "drat_trim_verified", "seconds", "drat_trim_seconds", "proof_sha256", "cnf_sha256")}
        if t in (2, 3):
            f = encoders.petersen_coloring(R, defect_bound=2)
            f.write(HEAVY / f"R{t}_pd_le2.cnf")
            s = solver.solve(HEAVY / f"R{t}_pd_le2.cnf", HEAVY / f"R{t}_pd_le2.drat", 7200, want_proof=(t == 3))
            item = {k: s.get(k) for k in ("status", "drat_trim_verified", "seconds", "drat_trim_seconds", "proof_sha256", "cnf_sha256")}
            if s["status"] == "SAT":
                images = checkers.edge_color_map(set(s["model"]), f.names, len(R.edges), 15, prefix="y")
                item["checker_defect"] = checkers.petersen_defect(R, images)
                stars = {frozenset(x) for x in graphs.petersen().incidence()}
                inc = R.incidence()
                bad = [w for w in range(R.n) if len({images[e] for e in inc[w]}) != 3 or frozenset(images[e] for e in inc[w]) not in stars]
                item["bad_blocks"] = sorted({i for i, bl in enumerate(blocks) for w in bad if w in bl})
            rec["pd_le2"] = item
        out["rings"][f"R{t}"] = rec
        save(out)
        log(f"R{t}: {({k: v for k, v in rec.items() if k not in ('cyclic_cuts_below_4', 'block0_boundary')})}")


if __name__ == "__main__":
    main()
