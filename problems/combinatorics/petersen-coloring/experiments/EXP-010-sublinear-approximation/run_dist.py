"""EXP-010 addendum 3: distance sets Dist(e0, e) of the pendant labels at the ends of e0 in the
4-poles M(G; e0, e).

    .venv/Scripts/python.exe .../run_dist.py --graph G52 --e0 0 --workers 6 --worker 0
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBLEM = HERE.parents[1]
sys.path.insert(0, str(PROBLEM / "code"))
sys.path.insert(0, str(HERE))

from pcclib import graphs, solver  # noqa: E402
from run import HEAVY, check, load, multipole_formula  # noqa: E402


def label_distances() -> dict[int, int]:
    """Distance in the line graph of P from edge 0 to every edge."""
    p = graphs.petersen()
    adj = {i: [j for j in range(15) if j != i and set(p.edges[i]) & set(p.edges[j])] for i in range(15)}
    dist = {0: 0}
    frontier = [0]
    while frontier:
        nxt = []
        for x in frontier:
            for y in adj[x]:
                if y not in dist:
                    dist[y] = dist[x] + 1
                    nxt.append(y)
        frontier = nxt
    return dist


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", default="G52")
    ap.add_argument("--e0", type=int, default=0)
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--worker", type=int, default=0)
    args = ap.parse_args()
    g = load(args.graph)
    dist = label_distances()
    rep = {d: min(t for t, dd in dist.items() if dd == d) for d in (1, 2, 3)}
    a, b = g.edges[args.e0]
    others = [i for i in range(len(g.edges)) if i != args.e0 and not set(g.edges[i]) & {a, b}]
    mine = others[args.worker::args.workers]
    out_dir = HEAVY / f"dist-{args.graph}-e{args.e0}"
    out_dir.mkdir(parents=True, exist_ok=True)
    path = HERE / "artifacts" / f"dist-{args.graph}-e{args.e0}-w{args.worker}of{args.workers}.json"
    res = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"graph": args.graph, "e0": args.e0, "label_representatives": rep, "edges": {}}
    for e in mine:
        if str(e) in res["edges"]:
            continue
        entry = {}
        for d in (1, 2, 3):
            f, y = multipole_formula(g, args.e0, e, symmetry=False)
            f.add(y[("pend", a, args.e0), 0])
            f.add(y[("pend", b, args.e0), rep[d]])
            cnf = out_dir / f"M_{args.e0}_{e}_d{d}.cnf"
            f.write(cnf)
            rec = solver.solve(cnf, out_dir / f"M_{args.e0}_{e}_d{d}.drat", 600)
            item = {"status": rec["status"], "seconds": rec["seconds"]}
            if rec["status"] == "SAT":
                model = set(rec["model"])
                lab = {k2: t for (k2, t), var in y.items() if var in model}
                item["checker_ok"] = check(g, args.e0, e, lab)
            elif rec["status"] == "UNSAT":
                item["verified"] = rec.get("drat_trim_verified")
                item["proof_sha256"] = rec.get("proof_sha256")
            entry[str(d)] = item
        entry["dist_set"] = [d for d in (1, 2, 3) if entry[str(d)]["status"] == "SAT"]
        res["edges"][str(e)] = entry
        print(time.strftime("%H:%M:%S"), args.graph, "e0", args.e0, "e", e, g.edges[e], "Dist", entry["dist_set"], flush=True)
        path.write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
