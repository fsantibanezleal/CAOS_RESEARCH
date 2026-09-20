"""EXP-011: criticality of the adjacent vertex pairs of the ten dot products G52 . G52 (and of G52
as a control).

Run from the repository root:
    .venv/Scripts/python.exe problems/combinatorics/petersen-coloring/experiments/EXP-011-adjacent-pair-criticality/run.py --object G52
    .venv/Scripts/python.exe .../run.py --object D_0_3_0
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
sys.path.insert(0, str(HERE.parent / "EXP-010-sublinear-approximation"))

from pcclib import checkers, graphs, relaxed, solver  # noqa: E402
from run_dot import dot_product  # noqa: E402

ARTIFACTS = HERE / "artifacts"
HEAVY = Path("E:/_Datos/caos-research/petersen-coloring/EXP-011")
DATA = PROBLEM / "data"
CAP = 600


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def build(name: str) -> graphs.Graph:
    g52 = graphs.load_edgelist(DATA / "gjmmm-52.edgelist")
    if name == "G52":
        return g52
    _, e1, e2, uv = name.split("_")
    return dot_product(g52, int(e1), int(e2), g52, int(uv))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--object", required=True)
    args = ap.parse_args()
    ARTIFACTS.mkdir(exist_ok=True)
    out_dir = HEAVY / args.object
    out_dir.mkdir(parents=True, exist_ok=True)
    g = build(args.object)
    stars = {frozenset(s) for s in graphs.petersen().incidence()}
    inc = g.incidence()
    path = ARTIFACTS / f"adjacent-pairs-{args.object}.json"
    res = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"object": args.object, "n": g.n, "digest": g.digest(), "pairs": {}}
    for idx, (u, v) in enumerate(g.edges):
        key = f"{u}-{v}"
        if key in res["pairs"] and res["pairs"][key]["status"] in ("SAT", "UNSAT"):
            continue
        f = relaxed.petersen_relaxed_vertices(g, {u, v})
        cnf = out_dir / f"relax_{u}_{v}.cnf"
        f.write(cnf, [f"EXP-011 {args.object} relax {u} {v}"])
        rec = solver.solve(cnf, out_dir / f"relax_{u}_{v}.drat", CAP)
        entry = {"status": rec["status"], "seconds": rec["seconds"]}
        if rec["status"] == "SAT":
            images = checkers.edge_color_map(set(rec["model"]), f.names, len(g.edges), 15, prefix="y")
            bad = [w for w in range(g.n) if len({images[e] for e in inc[w]}) != 3 or frozenset(images[e] for e in inc[w]) not in stars]
            entry.update({"bad_vertices": bad, "critical": sorted(bad) == sorted((u, v)), "witness": images})
        elif rec["status"] == "UNSAT":
            entry.update({"verified": rec.get("drat_trim_verified"), "proof_sha256": rec.get("proof_sha256"), "cnf_sha256": rec.get("cnf_sha256")})
            log(f"{args.object} pair {u}-{v}: UNSAT verified={rec.get('drat_trim_verified')} in {rec['seconds']} s")
        res["pairs"][key] = entry
        if (idx + 1) % 10 == 0:
            path.write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8", newline="\n")
            log(f"{args.object}: {len(res['pairs'])} of {len(g.edges)} adjacent pairs, critical {sum(1 for e in res['pairs'].values() if e.get('critical'))}")
    crit = sum(1 for e in res["pairs"].values() if e.get("critical"))
    res["summary"] = {"adjacent_pairs": len(g.edges), "critical": crit,
                      "unsat_verified": [k for k, e in res["pairs"].items() if e["status"] == "UNSAT" and e.get("verified")],
                      "undecided": [k for k, e in res["pairs"].items() if e["status"] not in ("SAT", "UNSAT")]}
    path.write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8", newline="\n")
    log(f"RESULT {args.object}: {crit} of {len(g.edges)} adjacent pairs critical; non-critical {res['summary']['unsat_verified']}; undecided {len(res['summary']['undecided'])}")


if __name__ == "__main__":
    main()
