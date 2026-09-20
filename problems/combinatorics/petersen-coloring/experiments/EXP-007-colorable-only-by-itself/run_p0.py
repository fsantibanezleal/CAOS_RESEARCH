"""EXP-007 addendum 3, P0: the new graphs have no Petersen coloring and no normal 5-edge-coloring
(our encoders, DRAT proofs checked by drat-trim). Run from the repository root."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBLEM = HERE.parents[1]
sys.path.insert(0, str(PROBLEM / "code"))
sys.path.insert(0, str(HERE))

from pcclib import encoders, invariants, solver  # noqa: E402
from run import load  # noqa: E402

HEAVY = Path("E:/_Datos/caos-research/petersen-coloring/EXP-007")


def main() -> None:
    HEAVY.mkdir(parents=True, exist_ok=True)
    out = {}
    for name in sys.argv[1:] or ["G52b", "G68"]:
        g = load(name)
        rec = {"n": g.n, "m": len(g.edges), "digest": g.digest(), "girth": invariants.girth(g),
               "edge_connectivity": invariants.edge_connectivity(g),
               "cyclic_cut_below_4": invariants.cyclic_edge_cut_below(g, 4)}
        for label, f in (("petersen", encoders.petersen_coloring(g)), ("normal5", encoders.normal_coloring(g, 5))):
            cnf = HEAVY / f"P0_{name}_{label}.cnf"
            f.write(cnf)
            r = solver.solve(cnf, HEAVY / f"P0_{name}_{label}.drat", 7200, want_proof=True)
            rec[label] = {k: r.get(k) for k in ("status", "drat_trim_verified", "seconds", "drat_trim_seconds", "cnf_sha256", "proof_sha256", "proof_bytes")}
            print(time.strftime("%H:%M:%S"), name, label, rec[label], flush=True)
        out[name] = rec
        (HERE / "artifacts" / f"p0-{name}.json").write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
