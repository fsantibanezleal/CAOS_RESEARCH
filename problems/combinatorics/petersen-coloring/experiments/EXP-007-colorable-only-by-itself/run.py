"""EXP-007: is G colored by some bridgeless cubic multigraph on k vertices? One process per (graph, k).

Deterministic up to the solver's model choice, headless, CPU only (CaDiCaL in WSL, drat-trim).
Writes artifacts/result-<graph>-k<k>.json on completion. Run from the repository root:

    .venv/Scripts/python.exe problems/combinatorics/petersen-coloring/experiments/EXP-007-colorable-only-by-itself/run.py --graph G52 --k 50
    .venv/Scripts/python.exe .../run.py --controls
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

from pcclib import encoders, graphs, hcolor, solver  # noqa: E402
from pcclib.cnf import CNF  # noqa: E402

ARTIFACTS = HERE / "artifacts"
HEAVY = Path("E:/_Datos/caos-research/petersen-coloring/EXP-007")
DATA = PROBLEM / "data"
CAP = 6 * 3600


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def load(name: str) -> graphs.Graph:
    table = {
        "G52": lambda: graphs.load_edgelist(DATA / "gjmmm-52.edgelist"),
        "G112": lambda: graphs.load_edgelist(DATA / "putman-112-main.edgelist"),
        "H112": lambda: graphs.load_edgelist(DATA / "putman-112-d3.edgelist"),
        "petersen": graphs.petersen,
        "J5": lambda: graphs.flower_snark(5),
        "K4": graphs.k4,
    }
    return table[name]()


def decide(name: str, k: int, cap: int = CAP) -> dict:
    g = load(name)
    t0 = time.time()
    inst = hcolor.HColorInstance(g, k)
    base = inst.f
    log(f"{name} k={k}: base formula {base.nvars} vars, {len(base.clauses)} clauses ({round(time.time()-t0,1)} s to build)")
    learned: list[dict] = []
    tag = f"{name}_k{k}"
    cnf_path = HEAVY / f"{tag}.cnf"
    rounds = 0
    while True:
        rounds += 1
        f = CNF()
        f.nvars = base.nvars
        f.names = base.names
        f.clauses = list(base.clauses) + [tuple(c["clause"]) for c in learned]
        f.write(cnf_path, [f"EXP-007 {tag} round {rounds}"])
        remaining = int(cap - (time.time() - t0))
        if remaining <= 0:
            return {"graph": name, "k": k, "status": "TIMEOUT", "rounds": rounds, "learned": learned, "seconds": round(time.time() - t0, 1)}
        rec = solver.solve(cnf_path, HEAVY / f"{tag}.drat", remaining, want_proof=False)
        if rec["status"] == "UNSAT":
            rec2 = solver.solve(cnf_path, HEAVY / f"{tag}.drat", max(remaining, 600), want_proof=True)
            return {"graph": name, "k": k, "status": "UNSAT", "rounds": rounds, "learned": learned,
                    "verified": rec2.get("drat_trim_verified"), "proof_bytes": rec2.get("proof_bytes"),
                    "proof_sha256": rec2.get("proof_sha256"), "cnf_sha256": rec2.get("cnf_sha256"),
                    "variables": f.nvars, "clauses": len(f.clauses),
                    "solve_seconds": rec["seconds"], "proof_solve_seconds": rec2.get("seconds"),
                    "check_seconds": rec2.get("drat_trim_seconds"), "seconds": round(time.time() - t0, 1)}
        if rec["status"] != "SAT":
            return {"graph": name, "k": k, "status": rec["status"], "rounds": rounds, "learned": learned, "seconds": round(time.time() - t0, 1)}
        model = set(rec["model"])
        vmap, hedges, edge_image = inst.decode(model)
        chk = hcolor.check_hcoloring(g, k, hedges, edge_image)
        if not (chk["cubic_loopless"] and chk["coloring"]):
            return {"graph": name, "k": k, "status": "CHECKER-REJECT", "check": chk, "seconds": round(time.time() - t0, 1)}
        if not chk["connected"]:
            comp = next(c for c in chk["components"] if 0 not in c)
            clause = inst.cut_clause(set(comp))
            learned.append({"kind": "disconnected", "side": comp, "clause": list(clause)})
            log(f"{tag}: round {rounds} target disconnected (side of {len(comp)}); cut learned")
            if not clause:
                return {"graph": name, "k": k, "status": "UNSAT-BY-EMPTY-CUT", "rounds": rounds, "seconds": round(time.time() - t0, 1)}
            continue
        if chk["bridge"] is not None:
            idx, side = chk["bridge"]
            a, b = hedges[idx]
            clause = inst.cut_clause(set(side), exclude=(a, b))
            learned.append({"kind": "bridge", "bridge": [list(a), list(b)], "side": side, "clause": list(clause)})
            log(f"{tag}: round {rounds} target has a bridge; cut learned")
            continue
        # a genuine coloring by a connected bridgeless cubic multigraph on k vertices
        H = hcolor.target_as_graph(k, hedges)
        used = sorted(set(vmap))
        out = {"graph": name, "k": k, "status": "SAT", "rounds": rounds, "learned": learned,
               "check": {kk: vv for kk, vv in chk.items() if kk != "components"},
               "used_target_vertices": len(used), "target_edges": [list(e) for e in H.edges],
               "vertex_map": vmap, "seconds": round(time.time() - t0, 1)}
        # is the target Petersen colorable? (it must not be when G is a counterexample)
        pf = encoders.petersen_coloring(H, symmetry=False)
        pc = HEAVY / f"{tag}_target_petersen.cnf"
        pf.write(pc)
        prec = solver.solve(pc, HEAVY / f"{tag}_target_petersen.drat", 3600)
        out["target_petersen"] = {"status": prec["status"], "verified": prec.get("drat_trim_verified"), "seconds": prec["seconds"]}
        return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", default="G52")
    ap.add_argument("--k", type=int, default=0)
    ap.add_argument("--controls", action="store_true")
    ap.add_argument("--cap", type=int, default=CAP)
    args = ap.parse_args()
    ARTIFACTS.mkdir(exist_ok=True)
    HEAVY.mkdir(parents=True, exist_ok=True)
    jobs = [("K4", 2), ("petersen", 2), ("petersen", 4), ("petersen", 6), ("petersen", 8), ("J5", 10)] if args.controls else [(args.graph, args.k)]
    for name, k in jobs:
        res = decide(name, k, args.cap)
        slim = {kk: vv for kk, vv in res.items() if kk != "learned"}
        slim["learned_cuts"] = len(res.get("learned", []))
        (ARTIFACTS / f"result-{name}-k{k}.json").write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
        log("RESULT " + json.dumps({kk: vv for kk, vv in slim.items() if kk not in ("target_edges", "vertex_map")}))


if __name__ == "__main__":
    main()
