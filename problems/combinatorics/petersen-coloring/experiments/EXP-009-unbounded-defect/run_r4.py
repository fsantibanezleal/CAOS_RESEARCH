"""EXP-009 addendum 1: designated one-vertex-per-copy relaxations of R_4 (witness search)."""

from __future__ import annotations

import itertools
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBLEM = HERE.parents[1]
sys.path.insert(0, str(PROBLEM / "code"))
sys.path.insert(0, str(HERE))

from pcclib import checkers, relaxed, solver  # noqa: E402
from run import HEAVY, build, save  # noqa: E402


def main() -> None:
    g, t, size = build("R4")
    locals_ = [18, 46, 20, 50, 44, 41]
    combos = [(18, 46, 20, 18), (50, 44, 41, 50), (18, 46, 20, 46), (50, 44, 41, 44)]
    combos += [c for c in itertools.product(locals_[:3], repeat=4)][:8]
    out = {}
    for combo in combos[:12]:
        relax = {i * size + w for i, w in enumerate(combo)}
        f = relaxed.petersen_relaxed_vertices(g, relax)
        stem = "R4_relax_" + "_".join(str(w) for w in combo)
        cnf = HEAVY / f"{stem}.cnf"
        f.write(cnf, [f"EXP-009 {stem}"])
        rec = solver.solve(cnf, HEAVY / f"{stem}.drat", 600, want_proof=False)
        entry = {"status": rec["status"], "seconds": rec["seconds"]}
        if rec["status"] == "SAT":
            images = checkers.edge_color_map(set(rec["model"]), f.names, len(g.edges), 15, prefix="y")
            entry.update({"checker_defect": checkers.petersen_defect(g, images), "witness": images, "relaxed": sorted(relax)})
        out[stem] = entry
        print(time.strftime("%H:%M:%S"), stem, {k: v for k, v in entry.items() if k != "witness"}, flush=True)
        save(HERE / "artifacts" / "r4-designated.json", out)
        if entry.get("checker_defect") == 4:
            break


if __name__ == "__main__":
    main()
