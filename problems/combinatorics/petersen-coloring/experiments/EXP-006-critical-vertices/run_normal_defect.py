"""EXP-006 addendum 4: normal-5 defect of G52 by symmetry (lower bound) and explicit witnesses (upper bound).

Run from the repository root:
    .venv/Scripts/python.exe problems/combinatorics/petersen-coloring/experiments/EXP-006-critical-vertices/run_normal_defect.py
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBLEM = HERE.parents[1]
sys.path.insert(0, str(PROBLEM / "code"))

from pcclib import automorphisms, checkers, encoders, graphs, solver  # noqa: E402

ARTIFACTS = HERE / "artifacts"
HEAVY = Path("E:/_Datos/caos-research/petersen-coloring/EXP-006")
DATA = PROBLEM / "data"
FILES = {"G52": "gjmmm-52.edgelist", "G112": "putman-112-main.edgelist", "H112": "putman-112-d3.edgelist"}


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def main() -> None:
    HEAVY.mkdir(parents=True, exist_ok=True)
    out: dict = {"symmetry": {}, "upper_bound": {}}
    manifest = json.loads((ARTIFACTS / "manifest.json").read_text(encoding="utf-8"))
    for name, fn in FILES.items():
        g = graphs.load_edgelist(DATA / fn)
        perms = automorphisms.automorphisms(g)
        assert all(automorphisms.is_automorphism(g, p) for p in perms)
        orbits = automorphisms.edge_orbits(g, perms)
        rec = {"automorphisms": perms, "edge_orbits": orbits}
        if name == "G52":
            done = {int(e) for e, v in manifest["edges"]["G52"].items() if v["status"] == "UNSAT" and v["verified"] is True}
            rec["refuted_edges"] = sorted(done)
            rec["orbit_representatives"] = [next((e for e in o if e in done), None) for o in orbits]
            rec["all_orbits_refuted"] = all(r is not None for r in rec["orbit_representatives"])
        out["symmetry"][name] = rec
        log(f"{name}: {len(perms)} automorphisms, {len(orbits)} edge orbits" + (f", all orbits refuted: {rec['all_orbits_refuted']}" if name == "G52" else ""))
    for name, fn in FILES.items():
        g = graphs.load_edgelist(DATA / fn)
        f = encoders.normal_coloring(g, 5, strong=False, defect_bound=2)
        cnf = HEAVY / f"{name}_normal5_defect_le2.cnf"
        f.write(cnf)
        r = solver.solve(cnf, HEAVY / f"{name}_normal5_defect_le2.drat", 1800, want_proof=False)
        rec = {"status": r["status"], "seconds": r["seconds"], "cnf_sha256": r.get("cnf_sha256")}
        if r["status"] == "SAT":
            colors = checkers.edge_color_map(set(r["model"]), f.names, len(g.edges), 5)
            rec["colors"] = colors
            rec["checker_defect"] = checkers.normal_defect(g, colors)
        out["upper_bound"][name] = rec
        log(f"{name}: bound 2 {r['status']} in {r['seconds']} s, checker defect {rec.get('checker_defect')}")
    (ARTIFACTS / "normal-defect.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
