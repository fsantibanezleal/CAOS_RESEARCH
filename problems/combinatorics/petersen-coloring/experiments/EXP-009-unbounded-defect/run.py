"""EXP-009: exact Petersen defect and abnormal-edge number of rings and frames built from G52.

Run from the repository root:

    .venv/Scripts/python.exe problems/combinatorics/petersen-coloring/experiments/EXP-009-unbounded-defect/run.py --part controls
    .venv/Scripts/python.exe .../run.py --part pd --object R2      (R2, R3, R4, K4G52)
    .venv/Scripts/python.exe .../run.py --part ab --object R2
    .venv/Scripts/python.exe .../run.py --part p5
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

from pcclib import checkers, encoders, graphs, invariants, relaxed, solver  # noqa: E402

ARTIFACTS = HERE / "artifacts"
HEAVY = Path("E:/_Datos/caos-research/petersen-coloring/EXP-009")
DATA = PROBLEM / "data"
CAP = 1800


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def save(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, indent=1) + "\n", encoding="utf-8", newline="\n")


def build(name: str) -> tuple[graphs.Graph, int, int]:
    """Returns (graph, number of copies, vertices per copy)."""
    g52 = graphs.load_edgelist(DATA / "gjmmm-52.edgelist")
    j5 = graphs.flower_snark(5)
    table = {
        "R2": (lambda: graphs.ring_join(g52, 0, 2), 2, 52),
        "R3": (lambda: graphs.ring_join(g52, 0, 3), 3, 52),
        "R4": (lambda: graphs.ring_join(g52, 0, 4), 4, 52),
        "K4G52": (lambda: graphs.frame_substitution(graphs.k4(), g52, 0), 4, 51),
        "R2J5": (lambda: graphs.ring_join(j5, 0, 2), 2, 20),
        "R3J5": (lambda: graphs.ring_join(j5, 0, 3), 3, 20),
        "K4J5": (lambda: graphs.frame_substitution(graphs.k4(), j5, 0), 4, 19),
    }
    make, t, size = table[name]
    return make(), t, size


def structure(g: graphs.Graph) -> dict:
    return {"n": g.n, "m": len(g.edges), "cubic": g.is_cubic(), "digest": g.digest(),
            "girth": invariants.girth(g), "edge_connectivity": invariants.edge_connectivity(g)}


def petersen_at_bound(name: str, g: graphs.Graph, bound: int, size: int) -> dict:
    f = encoders.petersen_coloring(g, defect_bound=bound) if bound > 0 else encoders.petersen_coloring(g)
    stem = f"{name}_pd_le{bound}"
    cnf = HEAVY / f"{stem}.cnf"
    f.write(cnf, [f"EXP-009 {stem}"])
    rec = solver.solve(cnf, HEAVY / f"{stem}.drat", CAP, want_proof=(bound == 0))
    out = {"instance": stem, "status": rec["status"], "seconds": rec["seconds"], "verified": rec.get("drat_trim_verified"),
           "cnf_sha256": rec.get("cnf_sha256"), "variables": f.nvars, "clauses": len(f.clauses)}
    if rec["status"] == "SAT":
        images = checkers.edge_color_map(set(rec["model"]), f.names, len(g.edges), 15, prefix="y")
        stars = {frozenset(s) for s in graphs.petersen().incidence()}
        inc = g.incidence()
        bad = [w for w in range(g.n) if len({images[e] for e in inc[w]}) != 3 or frozenset(images[e] for e in inc[w]) not in stars]
        out.update({"checker_defect": checkers.petersen_defect(g, images), "bad_vertices": bad,
                    "bad_copies": sorted(w // size for w in bad), "witness": images})
    log(f"{stem}: {out['status']} in {out['seconds']} s, checker defect {out.get('checker_defect')}, bad copies {out.get('bad_copies')}")
    return out


def normal_at_bound(name: str, g: graphs.Graph, bound: int, size: int) -> dict:
    f = encoders.normal_coloring(g, 5, strong=False, defect_bound=bound)
    stem = f"{name}_ab_le{bound}"
    cnf = HEAVY / f"{stem}.cnf"
    f.write(cnf, [f"EXP-009 {stem}"])
    rec = solver.solve(cnf, HEAVY / f"{stem}.drat", CAP, want_proof=False)
    out = {"instance": stem, "status": rec["status"], "seconds": rec["seconds"], "cnf_sha256": rec.get("cnf_sha256"),
           "variables": f.nvars, "clauses": len(f.clauses)}
    if rec["status"] == "SAT":
        colors = checkers.edge_color_map(set(rec["model"]), f.names, len(g.edges), 5)
        out.update({"checker_abnormal": checkers.normal_defect(g, colors), "witness": colors})
    log(f"{stem}: {out['status']} in {out['seconds']} s, checker abnormal {out.get('checker_abnormal')}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", required=True, choices=["controls", "pd", "ab", "p5"])
    ap.add_argument("--object", default="R2")
    args = ap.parse_args()
    ARTIFACTS.mkdir(exist_ok=True)
    HEAVY.mkdir(parents=True, exist_ok=True)
    if args.part == "controls":
        out = {}
        for name in ("R2J5", "R3J5", "K4J5"):
            g, t, size = build(name)
            out[name] = {"structure": structure(g), "pd0": petersen_at_bound(name, g, 0, size)}
        for name in ("R2", "R3", "R4", "K4G52"):
            g, t, size = build(name)
            out[name] = {"structure": structure(g)}
            log(f"{name}: {out[name]['structure']}")
        save(ARTIFACTS / "controls.json", out)
        return
    if args.part in ("pd", "ab"):
        g, t, size = build(args.object)
        res = {"object": args.object, "copies": t, "structure": structure(g), "bounds": {}}
        path = ARTIFACTS / f"{args.part}-{args.object}.json"
        for bound in range(t, 2 * t + 1):
            rec = petersen_at_bound(args.object, g, bound, size) if args.part == "pd" else normal_at_bound(args.object, g, bound, size)
            res["bounds"][str(bound)] = rec
            save(path, res)
            if rec["status"] == "SAT":
                res["least_satisfiable_bound_found"] = bound
                break
        save(path, res)
        return
    # P5: same-copy pair relaxations of R2 must be UNSAT
    g, t, size = build("R2")
    pairs = [(u, v) for u in range(0, 20, 2) for v in (u + 21, u + 30)]
    res = {"object": "R2", "pairs": {}}
    for u, v in pairs:
        f = relaxed.petersen_relaxed_vertices(g, {u, v})
        stem = f"R2_relax_{u}_{v}"
        cnf = HEAVY / f"{stem}.cnf"
        f.write(cnf, [f"EXP-009 {stem}"])
        rec = solver.solve(cnf, HEAVY / f"{stem}.drat", CAP)
        res["pairs"][f"{u}-{v}"] = {"status": rec["status"], "verified": rec.get("drat_trim_verified"), "seconds": rec["seconds"],
                                    "same_copy": u // size == v // size}
        log(f"{stem}: {rec['status']} verified={rec.get('drat_trim_verified')} in {rec['seconds']} s")
        save(ARTIFACTS / "p5-R2.json", res)


if __name__ == "__main__":
    main()
