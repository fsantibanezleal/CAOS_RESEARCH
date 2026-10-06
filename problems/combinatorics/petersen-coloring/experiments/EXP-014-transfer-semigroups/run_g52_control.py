"""EXP-014 addendum 1: the zero-trace control (G52 split along a 6-edge cut).

    .venv/Scripts/python.exe .../run_g52_control.py [--workers 10]

Finds a cycle-separating 6-edge cut delta(X) of G52 with both sides of at least 20 vertices (greedy
descent from random balanced sets, fixed seed), splits the six cut edges into two triples c1, c2 in
all ten ways, computes the sector matrices of G52[X] (L = c1, R = c2) and G52[V - X] (L = c2,
R = c1) with every cut edge in the same position on both sides, and checks that the product (the
ring of length 2, which is G52 again) has a zero diagonal in all six sectors.
Writes artifacts/g52-control.json.
"""

from __future__ import annotations

import argparse
import itertools
import json
import random
import sys
import time
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBLEM = HERE.parents[1]
sys.path.insert(0, str(PROBLEM / "code"))

from pcclib import graphs, invariants, poles, transfer  # noqa: E402

G52 = PROBLEM / "data" / "gjmmm-52.edgelist"


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def find_cut(g: graphs.Graph, seed: int = 20261006) -> list[int]:
    rng = random.Random(seed)

    def cut(s: set[int]) -> int:
        return sum(1 for u, v in g.edges if (u in s) != (v in s))

    # Randomized growth: adding a boundary vertex with k edges into X changes the cut by 3 - 2k;
    # vertices with more edges into X are preferred while the cut is above 6.
    adj = g.adjacency()
    for _ in range(20000):
        s = {rng.randrange(g.n)}
        c = 3
        while len(s) < 33:
            bnd = {}
            for v in s:
                for w in adj[v]:
                    if w not in s:
                        bnd[w] = bnd.get(w, 0) + 1
            if not bnd:
                break
            pool = list(bnd)
            weights = [(4 ** bnd[w]) if c > 6 else (4 ** (3 - bnd[w])) for w in pool]
            w = rng.choices(pool, weights)[0]
            s.add(w)
            c += 3 - 2 * bnd[w]
            if c == 6 and 18 <= len(s) <= 34:
                comps = invariants.components(g, {i for i, (u, v) in enumerate(g.edges) if (u in s) != (v in s)})
                if len(comps) == 2:
                    assert cut(s) == 6
                    return sorted(s)
    raise RuntimeError("no balanced 6-edge cut found")


def side_block(g: graphs.Graph, side: list[int], first: tuple[int, ...], second: tuple[int, ...], name: str) -> transfer.Block:
    keep = set(side)
    pl = poles.pole(g, removed_vertices=[v for v in range(g.n) if v not in keep])
    by_edge = {ei: j for j, (x, ei) in enumerate(pl.dangling)}
    return transfer.Block(name, pl, tuple(by_edge[e] for e in first), tuple(by_edge[e] for e in second))


def job(args):
    split, x, c1, c2 = args
    g = graphs.load_edgelist(G52)
    y = [v for v in range(g.n) if v not in set(x)]
    t0 = time.time()
    mx = transfer.sector_matrices(side_block(g, x, c1, c2, f"X|s{split}"))
    my = transfer.sector_matrices(side_block(g, y, c2, c1, f"Y|s{split}"))
    prod = transfer.product([mx, my])
    return {"split": split, "c1": list(c1), "c2": list(c2),
            "X_conducted": [o for o in transfer.SECTORS if mx[o].any()],
            "Y_conducted": [o for o in transfer.SECTORS if my[o].any()],
            "ring_diagonal_sectors": transfer.colorable_sectors(prod),
            "seconds": round(time.time() - t0, 1)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=10)
    args = ap.parse_args()
    g = graphs.load_edgelist(G52)
    x = find_cut(g)
    xs = set(x)
    cut_edges = [i for i, (u, v) in enumerate(g.edges) if (u in xs) != (v in xs)]
    log(f"6-edge cut found: |X| = {len(x)}, |V - X| = {g.n - len(x)}, cut edges {cut_edges}")
    splits = [(c1, tuple(e for e in cut_edges if e not in c1)) for c1 in itertools.combinations(cut_edges, 3) if cut_edges[0] in c1]
    with Pool(args.workers) as pool:
        rows = pool.map(job, [(i, x, c1, c2) for i, (c1, c2) in enumerate(splits)], chunksize=1)
    out = {"graph": "G52", "X": x, "cut_edges": cut_edges, "splits": rows,
           "all_zero": all(not r["ring_diagonal_sectors"] for r in rows),
           "sides_colorable": all(r["X_conducted"] and r["Y_conducted"] for r in rows)}
    (HERE / "artifacts" / "g52-control.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8", newline="\n")
    log(f"control: ring diagonal zero in all sectors for all splits: {out['all_zero']}; sides colorable: {out['sides_colorable']}")


if __name__ == "__main__":
    main()
