"""EXP-010 step 1: Petersen colorability of the 4-poles M(G; e1, e2) = G - e1 - e2 with four pendant
edges, one representative per orbit of unordered pairs of independent edges.

Run from the repository root (one worker of `--workers`, selected by `--worker`):

    .venv/Scripts/python.exe problems/combinatorics/petersen-coloring/experiments/EXP-010-sublinear-approximation/run.py --graph G52 --workers 6 --worker 0
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBLEM = HERE.parents[1]
sys.path.insert(0, str(PROBLEM / "code"))

from pcclib import automorphisms, graphs, solver  # noqa: E402
from pcclib.cnf import CNF  # noqa: E402

ARTIFACTS = HERE / "artifacts"
HEAVY = Path("E:/_Datos/caos-research/petersen-coloring/EXP-010")
DATA = PROBLEM / "data"
CAP = 600
FILES = {"G52": "gjmmm-52.edgelist", "G52b": "gjmmmu-52-b.edgelist", "G68": "hog-57280-68.edgelist",
         "G112": "putman-112-main.edgelist", "H112": "putman-112-d3.edgelist"}


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def load(name: str) -> graphs.Graph:
    if name == "J5":
        return graphs.flower_snark(5)
    return graphs.load_edgelist(DATA / FILES[name])


def pair_orbit_representatives(g: graphs.Graph) -> list[tuple[int, int]]:
    perms = automorphisms.automorphisms(g)
    index = {e: i for i, e in enumerate(g.edges)}

    def image(p, i):
        u, v = g.edges[i]
        return index[(min(p[u], p[v]), max(p[u], p[v]))]

    eperms = [[image(p, i) for i in range(len(g.edges))] for p in perms]
    reps = []
    for i, j in itertools.combinations(range(len(g.edges)), 2):
        if set(g.edges[i]) & set(g.edges[j]):
            continue
        canon = min(tuple(sorted((ep[i], ep[j]))) for ep in eperms)
        if canon == (i, j):
            reps.append((i, j))
    return reps


def multipole_formula(g: graphs.Graph, e1: int, e2: int, symmetry: bool = True) -> tuple[CNF, dict]:
    """Edge map to E(P): kept edges and four pendant edges; pairwise adjacency at every vertex of G."""
    p = graphs.petersen()
    padj = [[j for j in range(15) if j != i and set(p.edges[i]) & set(p.edges[j])] for i in range(15)]
    f = CNF()
    kept = [i for i in range(len(g.edges)) if i not in (e1, e2)]
    a, b = g.edges[e1]
    c, d = g.edges[e2]
    labels = {("edge", i): None for i in kept}
    for end in (("pend", a, e1), ("pend", b, e1), ("pend", c, e2), ("pend", d, e2)):
        labels[end] = None
    y = {}
    for key in labels:
        for t in range(15):
            y[key, t] = f.var("y_" + "_".join(str(x) for x in key) + f"_{t}")
        f.exactly_one([y[key, t] for t in range(15)])
    inc = g.incidence()
    for v in range(g.n):
        items = [("edge", i) if i not in (e1, e2) else ("pend", v, i) for i in inc[v]]
        for k1, k2 in itertools.combinations(items, 2):
            for s in range(15):
                for t in range(15):
                    if s == t or t not in padj[s]:
                        f.add(-y[k1, s], -y[k2, t])
    # symmetry: P is edge-transitive (switched off when the caller fixes pendant labels itself)
    if symmetry:
        f.add(y[("edge", kept[0]), 0])
    return f, y


def check(g: graphs.Graph, e1: int, e2: int, lab: dict) -> bool:
    p = graphs.petersen()
    stars = {frozenset(s) for s in p.incidence()}
    inc = g.incidence()
    for v in range(g.n):
        imgs = [lab[("edge", i)] if i not in (e1, e2) else lab[("pend", v, i)] for i in inc[v]]
        if len(set(imgs)) != 3 or frozenset(imgs) not in stars:
            return False
    return True


def pattern(g: graphs.Graph, e1: int, e2: int, lab: dict) -> str:
    a, b = g.edges[e1]
    c, d = g.edges[e2]
    sa, sb, sc, sd = lab[("pend", a, e1)], lab[("pend", b, e1)], lab[("pend", c, e2)], lab[("pend", d, e2)]
    if sa == sb and sc == sd:
        return "restorable"
    if len({sa, sb, sc, sd}) == 2:
        return "crossed"
    if len({sa, sb, sc, sd}) == 4:
        return "four-distinct"
    return "other"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", required=True)
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--worker", type=int, default=0)
    args = ap.parse_args()
    ARTIFACTS.mkdir(exist_ok=True)
    (HEAVY / args.graph).mkdir(parents=True, exist_ok=True)
    g = load(args.graph)
    reps = pair_orbit_representatives(g)
    mine = reps[args.worker::args.workers]
    log(f"{args.graph}: {len(reps)} orbit representatives of independent edge pairs, this worker {len(mine)}")
    path = ARTIFACTS / f"poles-{args.graph}-w{args.worker}of{args.workers}.json"
    res = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"graph": args.graph, "representatives": len(reps), "pairs": {}}
    for n, (e1, e2) in enumerate(mine):
        key = f"{e1}-{e2}"
        if key in res["pairs"]:
            continue
        f, y = multipole_formula(g, e1, e2)
        cnf = HEAVY / args.graph / f"M_{e1}_{e2}.cnf"
        f.write(cnf, [f"EXP-010 {args.graph} M({e1},{e2})"])
        rec = solver.solve(cnf, HEAVY / args.graph / f"M_{e1}_{e2}.drat", CAP)
        entry = {"status": rec["status"], "seconds": rec["seconds"], "cnf_sha256": rec.get("cnf_sha256")}
        if rec["status"] == "SAT":
            model = set(rec["model"])
            lab = {key2: t for (key2, t), var in y.items() if var in model}
            entry.update({"checker_ok": check(g, e1, e2, lab), "pattern": pattern(g, e1, e2, lab)})
        elif rec["status"] == "UNSAT":
            entry.update({"verified": rec.get("drat_trim_verified"), "proof_sha256": rec.get("proof_sha256"), "proof_bytes": rec.get("proof_bytes")})
            log(f"{args.graph} M({e1},{e2}) edges {g.edges[e1]} {g.edges[e2]}: UNSAT verified={rec.get('drat_trim_verified')} in {rec['seconds']} s")
        res["pairs"][key] = entry
        if (n + 1) % 20 == 0:
            path.write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8", newline="\n")
            sat = sum(1 for e in res["pairs"].values() if e["status"] == "SAT")
            log(f"{args.graph} worker {args.worker}: {len(res['pairs'])} of {len(mine)} done, {sat} SAT")
    path.write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8", newline="\n")
    unsat = [k for k, e in res["pairs"].items() if e["status"] == "UNSAT"]
    log(f"RESULT {args.graph} worker {args.worker}: {len(res['pairs'])} pairs, UNSAT {unsat}")


if __name__ == "__main__":
    main()
