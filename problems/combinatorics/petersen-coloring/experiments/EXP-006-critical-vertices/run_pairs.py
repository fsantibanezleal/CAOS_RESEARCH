"""EXP-006 addendum P6: pair relaxations of G52 (is the Petersen defect exactly 2?).

Resumable through artifacts/pairs.json. Run from the repository root with the repo .venv:

    .venv/Scripts/python.exe problems/combinatorics/petersen-coloring/experiments/EXP-006-critical-vertices/run_pairs.py [--graph G52]
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

from pcclib import checkers, graphs, relaxed, solver  # noqa: E402

ARTIFACTS = HERE / "artifacts"
HEAVY = Path("E:/_Datos/caos-research/petersen-coloring/EXP-006/pairs")
DATA = PROBLEM / "data"
CAP = 600
FILES = {"G52": "gjmmm-52.edgelist", "G112": "putman-112-main.edgelist", "H112": "putman-112-d3.edgelist"}


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", default="G52")
    ap.add_argument("--pairs", default="", help="optional explicit list u-v;u-v")
    args = ap.parse_args()
    ARTIFACTS.mkdir(exist_ok=True)
    HEAVY.mkdir(parents=True, exist_ok=True)
    g = graphs.load_edgelist(DATA / FILES[args.graph])
    mpath = ARTIFACTS / f"pairs-{args.graph}.json"
    res = json.loads(mpath.read_text(encoding="utf-8")) if mpath.exists() else {"graph": args.graph, "pairs": {}, "tools": solver.tool_versions()}
    p = graphs.petersen()
    stars = {frozenset(s) for s in p.incidence()}
    inc = g.incidence()
    pairs = [tuple(int(x) for x in t.split("-")) for t in args.pairs.split(";")] if args.pairs else list(itertools.combinations(range(g.n), 2))
    t0 = time.time()
    for u, v in pairs:
        key = f"{u}-{v}"
        if key in res["pairs"]:
            continue
        f = relaxed.petersen_relaxed_vertices(g, {u, v})
        cp = HEAVY / f"{args.graph}_relax_{u}_{v}.cnf"
        f.write(cp)
        rec = solver.solve(cp, HEAVY / f"{args.graph}_relax_{u}_{v}.drat", CAP)
        entry = {"status": rec["status"], "seconds": rec["seconds"]}
        if rec["status"] == "SAT":
            model = set(rec["model"])
            images = checkers.edge_color_map(model, f.names, len(g.edges), 15, prefix="y")
            bad = [w for w in range(g.n) if frozenset(images[e] for e in inc[w]) not in stars or len({images[e] for e in inc[w]}) != 3]
            entry.update({"bad_vertices": bad, "defect": len(bad), "critical_pair": set(bad) <= {u, v} and len(bad) >= 1, "witness": images})
            log(f"{args.graph} pair {u},{v}: SAT, bad {bad}")
        elif rec["status"] == "UNSAT":
            entry.update({"verified": rec.get("drat_trim_verified"), "proof_sha256": rec.get("proof_sha256")})
        else:
            log(f"{args.graph} pair {u},{v}: {rec['status']}")
        res["pairs"][key] = entry
        if len(res["pairs"]) % 25 == 0:
            sat = sum(1 for e in res["pairs"].values() if e["status"] == "SAT")
            log(f"{args.graph}: {len(res['pairs'])} pairs done, {sat} SAT, {round(time.time() - t0)} s")
            mpath.write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    mpath.write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    sat_pairs = [k for k, e in res["pairs"].items() if e["status"] == "SAT"]
    unsat = [k for k, e in res["pairs"].items() if e["status"] == "UNSAT" and e.get("verified")]
    other = [k for k, e in res["pairs"].items() if e["status"] not in ("SAT", "UNSAT")]
    res["summary"] = {"sat_pairs": sat_pairs, "unsat_verified": len(unsat), "undecided": other,
                      "defect_exactly_2": bool(sat_pairs), "defect_at_least_3": (not sat_pairs and not other and len(unsat) == len(res["pairs"]))}
    mpath.write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    log(f"RESULT {args.graph}: {len(sat_pairs)} critical pairs, {len(unsat)} verified UNSAT, {len(other)} undecided")


if __name__ == "__main__":
    main()
