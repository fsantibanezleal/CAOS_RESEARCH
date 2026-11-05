"""EXP-012 addendum 3: the ten P5 pair relaxations of R_3 in parallel (same seed and selection as
run_r3_checks.py). Writes artifacts/r3-pairs.json."""

from __future__ import annotations

import json
import random
import sys
import time
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBLEM = HERE.parents[1]
sys.path.insert(0, str(PROBLEM / "code"))

from pcclib import checkers, graphs, poles, relaxed, rings, solver  # noqa: E402

HEAVY = Path("E:/_Datos/caos-research/petersen-coloring/EXP-012/rings")
DATA = PROBLEM / "data"


def build():
    g52 = graphs.load_edgelist(DATA / "gjmmm-52.edgelist")
    A = poles.pole(g52, removed_edges=(0, 4))
    B = poles.pole(g52, removed_vertices=(2, 7))
    uside = tuple(j for j, (w, ei) in enumerate(B.dangling) if 2 in g52.edges[ei])
    vside = tuple(j for j, (w, ei) in enumerate(B.dangling) if 7 in g52.edges[ei])
    return rings.ring_of_poles([(A, ((0, 1), (2, 3))), (B, (uside, vside))] * 3)


def pairs_for(blocks):
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
    return pairs


def one(pair):
    R, blocks = build()
    x, y = pair
    block_of = {w: i for i, bl in enumerate(blocks) for w in bl}
    f = relaxed.petersen_relaxed_vertices(R, {x, y})
    stem = f"R3_pairrelax_{x}_{y}"
    f.write(HEAVY / f"{stem}.cnf")
    s = solver.solve(HEAVY / f"{stem}.cnf", HEAVY / f"{stem}.drat", 7200)
    item = {"blocks": [block_of[x], block_of[y]], "status": s["status"], "verified": s.get("drat_trim_verified"),
            "seconds": s["seconds"], "check_seconds": s.get("drat_trim_seconds"), "proof_sha256": s.get("proof_sha256")}
    if s["status"] == "SAT":
        images = checkers.edge_color_map(set(s["model"]), f.names, len(R.edges), 15, prefix="y")
        item["checker_defect"] = checkers.petersen_defect(R, images)
    print(time.strftime("%H:%M:%S"), pair, item, flush=True)
    return f"{x}-{y}", item


def main() -> None:
    R, blocks = build()
    assert R.digest() == graphs.load_edgelist(HEAVY / "R3.edgelist").digest()
    pairs = pairs_for(blocks)
    with Pool(len(pairs)) as pool:
        rows = pool.map(one, pairs)
    (HERE / "artifacts" / "r3-pairs.json").write_text(json.dumps({"digest": R.digest(), "pairs": dict(rows)}, indent=1) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
