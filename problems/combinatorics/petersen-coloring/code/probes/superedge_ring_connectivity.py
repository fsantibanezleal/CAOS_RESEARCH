"""Girth and cyclic edge connectivity of rings of Petersen superedges (EXP-014, descriptive).

    .venv/Scripts/python.exe problems/combinatorics/petersen-coloring/code/probes/superedge_ring_connectivity.py

Rings of t copies of the superedge P - u - w (u, w at distance 2), the same junction permutation at
every junction, t = 3..5, all six permutations; non-simple rings are recorded as such, the girth is
measured, and rings of girth at least 5 get the exhaustive search for cycle-separating edge cuts with
at most four edges. Writes superedge_ring_connectivity.json next to this file.
"""

import importlib.util
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from pcclib import invariants, transfer  # noqa: E402

spec = importlib.util.spec_from_file_location("exp014", HERE.parents[1] / "experiments" / "EXP-014-transfer-semigroups" / "run.py")
exp014 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exp014)

rows = []
s = exp014.superedge()
for t in range(3, 6):
    for pi in transfer.PERMS:
        t0 = time.time()
        try:
            g = transfer.build_ring([(s, pi)] * t)
        except ValueError:
            rows.append({"t": t, "pi": list(pi), "simple": False})
            print(rows[-1], flush=True)
            continue
        row = {"t": t, "pi": list(pi), "simple": True, "order": g.n, "girth": invariants.girth(g),
               "edge_connectivity": invariants.edge_connectivity(g)}
        if row["girth"] >= 5:
            cut = invariants.cyclic_edge_cut_below(g, 5)
            row["cycle_separating_cut_below_5"] = list(cut) if cut else None
        row["seconds"] = round(time.time() - t0, 1)
        rows.append(row)
        print(row, flush=True)
(HERE / "superedge_ring_connectivity.json").write_text(json.dumps(rows, indent=1) + "\n", encoding="utf-8", newline="\n")
