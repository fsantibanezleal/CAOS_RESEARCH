"""EXP-007 addendum 7: write the reduced final formula (base plus attach clauses) for one (graph, k),
and decode a satisfying assignment produced by portfolio_certify.sh.

    .venv/Scripts/python.exe .../write_formula.py --graph G68 --k 52
    .venv/Scripts/python.exe .../write_formula.py --graph G68 --k 52 --decode <solver stdout file>

The decode step checks the coloring from the definition (check_hcoloring) and, if the target is a
connected bridgeless cubic graph, refutes it for Petersen colorability with a checked proof.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBLEM = HERE.parents[1]
sys.path.insert(0, str(PROBLEM / "code"))
sys.path.insert(0, str(HERE))

from pcclib import encoders, hcolor, solver  # noqa: E402
from pcclib.cnf import CNF  # noqa: E402
from run import load  # noqa: E402
from run_inc import attach_clauses  # noqa: E402

HEAVY = Path("E:/_Datos/caos-research/petersen-coloring/EXP-007")


def build(name: str, k: int):
    g = load(name)
    inst = hcolor.HColorInstance(g, k, reduced=True)
    static = attach_clauses(inst)
    f = CNF()
    f.nvars = inst.f.nvars
    f.names = inst.f.names
    f.clauses = list(inst.f.clauses) + list(static)
    return g, inst, f, len(static)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", required=True)
    ap.add_argument("--k", type=int, required=True)
    ap.add_argument("--decode", default="")
    args = ap.parse_args()
    g, inst, f, n_attach = build(args.graph, args.k)
    tag = f"{args.graph}_k{args.k}-portfolio"
    if not args.decode:
        path = HEAVY / f"{tag}.cnf"
        f.write(path, [f"EXP-007 {tag} final formula: base + {n_attach} attach + 0 learned cuts (reduced)"])
        print(json.dumps({"cnf": str(path), "variables": f.nvars, "clauses": len(f.clauses), "sha256": solver.sha256_file(path)}))
        return
    model = set()
    for line in Path(args.decode).read_text(encoding="utf-8", errors="replace").splitlines():
        if line.startswith("v "):
            model.update(int(x) for x in line[2:].split() if int(x) > 0)
    vmap, hedges, edge_image = inst.decode(model)
    chk = hcolor.check_hcoloring(g, args.k, hedges, edge_image)
    out = {"graph": args.graph, "k": args.k, "status": "SAT", "check": {kk: vv for kk, vv in chk.items() if kk != "components"}}
    if chk["ok"]:
        H = hcolor.target_as_graph(args.k, hedges)
        out["target_edges"] = [list(e) for e in H.edges]
        out["vertex_map"] = vmap
        pf = encoders.petersen_coloring(H, symmetry=False)
        pc = HEAVY / f"{tag}_target_petersen.cnf"
        pf.write(pc)
        rec = solver.solve(pc, HEAVY / f"{tag}_target_petersen.drat", 7200)
        out["target_petersen"] = {"status": rec["status"], "verified": rec.get("drat_trim_verified"), "seconds": rec["seconds"]}
    (HERE / "artifacts" / f"result-{args.graph}-k{args.k}-decoded.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({kk: vv for kk, vv in out.items() if kk not in ("target_edges", "vertex_map")}))


if __name__ == "__main__":
    main()
