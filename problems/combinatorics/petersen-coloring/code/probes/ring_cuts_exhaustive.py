"""Cross-check of EXP-012: cyclic edge connectivity of the rings R_1, R_2 by the exhaustive EXP-001
routine (all edge subsets of size at most 3), independent of the bridge-based search."""

import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

from pcclib import graphs, invariants  # noqa: E402

RINGS = Path("E:/_Datos/caos-research/petersen-coloring/EXP-012/rings")
OUT = HERE.parents[1] / "experiments" / "EXP-012-conduction-rings" / "artifacts" / "ring-cuts-exhaustive.json"

res = {}
for name in sys.argv[1:] or ["R1", "R2"]:
    g = graphs.load_edgelist(RINGS / f"{name}.edgelist")
    t0 = time.time()
    cut = invariants.cyclic_edge_cut_below(g, 4)
    res[name] = {"n": g.n, "digest": g.digest(), "cycle_separating_cut_below_4": list(cut) if cut else None, "seconds": round(time.time() - t0, 1)}
    print(name, res[name], flush=True)
    OUT.write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8", newline="\n")
