"""EXP-007 incremental runner: the lazy cut loop runs in-process (PySAT CaDiCaL 1.9.5); the final
formula (base plus every learned cut) is then certified by WSL CaDiCaL with a DRAT proof checked
by drat-trim. One process per (graph, k). Requires the worktree venv with python-sat.

    .venv/Scripts/python.exe .../run_inc.py --graph G52 --k 50 [--cap 21600]
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBLEM = HERE.parents[1]
sys.path.insert(0, str(PROBLEM / "code"))
sys.path.insert(0, str(HERE))

from pysat.solvers import Cadical195  # noqa: E402

from pcclib import encoders, hcolor, solver  # noqa: E402
from pcclib.cnf import CNF  # noqa: E402
from run import load  # noqa: E402

ARTIFACTS = HERE / "artifacts"
HEAVY = Path("E:/_Datos/caos-research/petersen-coloring/EXP-007")


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def attach_clauses(inst: hcolor.HColorInstance) -> list[tuple[int, ...]]:
    """Static necessary condition for a connected target: if class i is the first unused class,
    some slot pair joins a class below i to a class from i on."""
    n, k = inst.g.n, inst.k
    out = []
    for i in range(1, k):
        lits = [inst.used[n - 1, i], -inst.used[n - 1, i - 1]]
        for (a, b), var in inst.p.items():
            if (a[0] < i) != (b[0] < i):
                lits.append(var)
        out.append(tuple(lits))
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", default="G52")
    ap.add_argument("--k", type=int, required=True)
    ap.add_argument("--cap", type=int, default=6 * 3600)
    ap.add_argument("--unreduced", action="store_true", help="attempt-1 formula, without Lemmas A and B")
    ap.add_argument("--suffix", default="")
    args = ap.parse_args()
    ARTIFACTS.mkdir(exist_ok=True)
    HEAVY.mkdir(parents=True, exist_ok=True)
    name, k = args.graph, args.k
    tag = f"{name}_k{k}{args.suffix}"
    out_path = ARTIFACTS / f"result-{name}-k{k}{args.suffix}.json"
    t0 = time.time()
    state = {"rounds": 0, "cuts": 0}

    def on_timeout():
        res = {"graph": name, "k": k, "status": "TIMEOUT", "rounds": state["rounds"], "learned_cuts": state["cuts"], "seconds": round(time.time() - t0, 1)}
        out_path.write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
        log("RESULT " + json.dumps(res))
        os._exit(3)

    timer = threading.Timer(args.cap, on_timeout)
    timer.daemon = True
    timer.start()

    g = load(name)
    inst = hcolor.HColorInstance(g, k, reduced=not args.unreduced)
    base = inst.f
    static = attach_clauses(inst)
    log(f"{tag}: base {base.nvars} vars, {len(base.clauses)} clauses, {len(static)} attach clauses ({round(time.time()-t0,1)} s)")
    s = Cadical195()
    for cl in base.clauses:
        s.add_clause(list(cl))
    for cl in static:
        s.add_clause(list(cl))
    learned: list[dict] = []
    result = None
    while True:
        state["rounds"] += 1
        sat = s.solve()
        if not sat:
            break
        model = {v for v in s.get_model() if v > 0}
        vmap, hedges, edge_image = inst.decode(model)
        chk = hcolor.check_hcoloring(g, k, hedges, edge_image)
        if not (chk["cubic_loopless"] and chk["coloring"]):
            result = {"graph": name, "k": k, "status": "CHECKER-REJECT", "check": chk}
            break
        if not chk["connected"]:
            comp = next(c for c in chk["components"] if 0 not in c)
            clause = inst.cut_clause(set(comp))
            learned.append({"kind": "disconnected", "side": comp, "clause": list(clause)})
        elif chk["bridge"] is not None:
            idx, side = chk["bridge"]
            a, b = hedges[idx]
            clause = inst.cut_clause(set(side), exclude=(a, b))
            learned.append({"kind": "bridge", "bridge": [list(a), list(b)], "side": side, "clause": list(clause)})
        else:
            H = hcolor.target_as_graph(k, hedges)
            result = {"graph": name, "k": k, "status": "SAT", "fibers_odd": (inst.q in model) if inst.q else None, "check": {kk: vv for kk, vv in chk.items() if kk != "components"},
                      "used_target_vertices": len(set(vmap)), "target_edges": [list(e) for e in H.edges], "vertex_map": vmap}
            pf = encoders.petersen_coloring(H, symmetry=False)
            pc = HEAVY / f"{tag}_target_petersen.cnf"
            pf.write(pc)
            prec = solver.solve(pc, HEAVY / f"{tag}_target_petersen.drat", 3600)
            result["target_petersen"] = {"status": prec["status"], "verified": prec.get("drat_trim_verified"), "seconds": prec["seconds"]}
            break
        state["cuts"] = len(learned)
        if not clause:
            result = {"graph": name, "k": k, "status": "UNSAT-BY-EMPTY-CUT"}
            break
        s.add_clause(list(clause))
        if state["rounds"] % 200 == 0:
            kinds = {}
            for c in learned:
                kinds[c["kind"]] = kinds.get(c["kind"], 0) + 1
            log(f"{tag}: round {state['rounds']}, cuts {kinds}, {round(time.time()-t0)} s")
    if result is None:
        # in-process UNSAT: certify the final formula with a checked DRAT proof
        f = CNF()
        f.nvars = base.nvars
        f.names = base.names
        f.clauses = list(base.clauses) + list(static) + [tuple(c["clause"]) for c in learned]
        cnf_path = HEAVY / f"{tag}.cnf"
        f.write(cnf_path, [f"EXP-007 {tag} final formula: base + {len(static)} attach + {len(learned)} learned cuts"])
        log(f"{tag}: in-process UNSAT after {state['rounds']} rounds and {len(learned)} cuts ({round(time.time()-t0)} s); certifying")
        remaining = max(600, int(args.cap - (time.time() - t0)))
        rec = solver.solve(cnf_path, HEAVY / f"{tag}.drat", remaining, want_proof=True)
        result = {"graph": name, "k": k, "status": rec["status"], "verified": rec.get("drat_trim_verified"),
                  "proof_bytes": rec.get("proof_bytes"), "proof_sha256": rec.get("proof_sha256"), "cnf_sha256": rec.get("cnf_sha256"),
                  "reduced": not args.unreduced, "variables": f.nvars, "clauses": len(f.clauses), "certify_solve_seconds": rec.get("seconds"),
                  "check_seconds": rec.get("drat_trim_seconds")}
    timer.cancel()
    result.update({"rounds": state["rounds"], "learned_cuts": len(learned), "seconds": round(time.time() - t0, 1)})
    full = dict(result)
    full["learned"] = [{kk: vv for kk, vv in c.items() if kk != "clause"} for c in learned]
    out_path.write_text(json.dumps(full, indent=1) + "\n", encoding="utf-8")
    log("RESULT " + json.dumps({kk: vv for kk, vv in result.items() if kk not in ("target_edges", "vertex_map")}))


if __name__ == "__main__":
    main()
