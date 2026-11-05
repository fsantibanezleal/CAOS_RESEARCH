"""EXP-012 addendum 2: P4 (a map of R_3 with exactly three bad vertices) and P5 (ten sampled pair
relaxations of R_3, each expected UNSAT with a verified proof). Writes artifacts/r3-checks.json."""

from __future__ import annotations

import json
import random
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBLEM = HERE.parents[1]
sys.path.insert(0, str(PROBLEM / "code"))

from pcclib import checkers, encoders, graphs, poles, relaxed, rings, solver  # noqa: E402

HEAVY = Path("E:/_Datos/caos-research/petersen-coloring/EXP-012/rings")
DATA = PROBLEM / "data"


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def bad_vertices(g, images):
    stars = {frozenset(x) for x in graphs.petersen().incidence()}
    inc = g.incidence()
    return [w for w in range(g.n) if len({images[e] for e in inc[w]}) != 3 or frozenset(images[e] for e in inc[w]) not in stars]


def main() -> None:
    g52 = graphs.load_edgelist(DATA / "gjmmm-52.edgelist")
    A = poles.pole(g52, removed_edges=(0, 4))
    B = poles.pole(g52, removed_vertices=(2, 7))
    uside = tuple(j for j, (w, ei) in enumerate(B.dangling) if 2 in g52.edges[ei])
    vside = tuple(j for j, (w, ei) in enumerate(B.dangling) if 7 in g52.edges[ei])
    R, blocks = rings.ring_of_poles([(A, ((0, 1), (2, 3))), (B, (uside, vside))] * 3)
    ref = graphs.load_edgelist(HEAVY / "R3.edgelist")
    assert R.digest() == ref.digest(), "R_3 differs from the graph of run_ring.py"
    block_of = {w: i for i, bl in enumerate(blocks) for w in bl}
    out = {"digest": R.digest()}

    # P4: upper bound 3
    f = encoders.petersen_coloring(R, defect_bound=3)
    f.write(HEAVY / "R3_pd_le3.cnf")
    s = solver.solve(HEAVY / "R3_pd_le3.cnf", HEAVY / "R3_pd_le3.drat", 3600, want_proof=False)
    item = {"status": s["status"], "seconds": s["seconds"]}
    if s["status"] == "SAT":
        images = checkers.edge_color_map(set(s["model"]), f.names, len(R.edges), 15, prefix="y")
        bad = bad_vertices(R, images)
        item.update({"checker_defect": checkers.petersen_defect(R, images), "bad_vertices": bad,
                     "bad_blocks": sorted(block_of[w] for w in bad)})
    out["P4_pd_le3"] = item
    log(f"P4: {item}")
    (HERE / "artifacts" / "r3-checks.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8", newline="\n")

    # P5: ten sampled pairs
    rng = random.Random(12)
    pairs = []
    while len(pairs) < 5:
        b = rng.randrange(len(blocks))
        x, y = rng.sample(blocks[b], 2)
        pairs.append((min(x, y), max(x, y)))
    while len(pairs) < 10:
        b1, b2 = rng.sample(range(len(blocks)), 2)
        x, y = rng.choice(blocks[b1]), rng.choice(blocks[b2])
        pairs.append((min(x, y), max(x, y)))
    out["P5_pairs"] = {}
    for x, y in pairs:
        f = relaxed.petersen_relaxed_vertices(R, {x, y})
        stem = f"R3_relax_{x}_{y}"
        f.write(HEAVY / f"{stem}.cnf")
        s = solver.solve(HEAVY / f"{stem}.cnf", HEAVY / f"{stem}.drat", 1800)
        item = {"blocks": [block_of[x], block_of[y]], "status": s["status"], "verified": s.get("drat_trim_verified"),
                "seconds": s["seconds"], "proof_sha256": s.get("proof_sha256")}
        if s["status"] == "SAT":
            images = checkers.edge_color_map(set(s["model"]), f.names, len(R.edges), 15, prefix="y")
            item["bad_vertices"] = bad_vertices(R, images)
        out["P5_pairs"][f"{x}-{y}"] = item
        log(f"P5 {x}-{y}: {item}")
        (HERE / "artifacts" / "r3-checks.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
