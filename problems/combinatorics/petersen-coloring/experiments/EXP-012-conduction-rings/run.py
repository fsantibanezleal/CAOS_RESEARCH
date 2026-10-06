"""EXP-012 step 1: conducted distance sets D(M) of candidate 4-poles under their three pairings.

For each candidate 4-pole and pairing, and each distance d in 0..3, one formula: the 4-pole maps
into E(P) with every vertex good and its first connector {p, q} carries a fixed pair of labels at
distance d (WLOG by the distance-transitivity of the line graph of P on ordered pairs). SAT
answers are checked from the definition; UNSAT answers carry DRAT proofs checked by drat-trim.

    .venv/Scripts/python.exe .../run.py --family W        (W, Pe2, Pe3, A, G52uv)
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

from pcclib import automorphisms, graphs, poles, solver  # noqa: E402

ARTIFACTS = HERE / "artifacts"
HEAVY = Path("E:/_Datos/caos-research/petersen-coloring/EXP-012")
DATA = PROBLEM / "data"
CAP = 600


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def pairings(n_dangling: int = 4) -> dict[str, tuple[tuple[int, int], tuple[int, int]]]:
    return {"01|23": ((0, 1), (2, 3)), "02|13": ((0, 2), (1, 3)), "03|12": ((0, 3), (1, 2))}


def candidates(family: str) -> dict[str, poles.Pole]:
    p = graphs.petersen()
    g52 = graphs.load_edgelist(DATA / "gjmmm-52.edgelist")
    out = {}
    if family == "W":
        u, v = p.edges[0]
        out["W"] = poles.pole(p, removed_vertices=(u, v))
    elif family in ("Pe2", "Pe3"):
        dist = poles.line_distances()
        want = 2 if family == "Pe2" else 3
        j = min(t for t in range(15) if dist[0][t] == want)
        out[f"P-e0-e{j}"] = poles.pole(p, removed_edges=(0, j))
    elif family == "A":
        # the first five edge pairs (e0, e) of G52 with distance set {1} in EXP-010
        rows = []
        for f in sorted((PROBLEM / "experiments" / "EXP-010-sublinear-approximation" / "artifacts").glob("dist-G52-e*-w*.json")):
            d = json.loads(f.read_text(encoding="utf-8"))
            for e, v in d["edges"].items():
                if v.get("dist_set") == [1]:
                    rows.append((d["e0"], int(e)))
        for e0, e in sorted(rows)[:5]:
            out[f"G52-e{e0}-e{e}"] = poles.pole(g52, removed_edges=(e0, e))
    elif family == "G52uv":
        perms = automorphisms.automorphisms(g52)
        for orbit in automorphisms.edge_orbits(g52, perms):
            u, v = g52.edges[orbit[0]]
            out[f"G52-v{u}-v{v}"] = poles.pole(g52, removed_vertices=(u, v))
    else:
        raise ValueError(family)
    return out


def dangling_order(pl: poles.Pole) -> list[int]:
    """Dangling ends in a readable order: for vertex deletions, the two ends at the first removed
    vertex's side first; for edge deletions, the two ends of the first deleted edge first."""
    return list(range(len(pl.dangling)))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", required=True)
    args = ap.parse_args()
    ARTIFACTS.mkdir(exist_ok=True)
    HEAVY.mkdir(parents=True, exist_ok=True)
    reps = poles.distance_representatives()
    path = ARTIFACTS / f"conduction-{args.family}.json"
    res = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"family": args.family, "poles": {}}
    for name, pl in candidates(args.family).items():
        assert len(pl.dangling) == 4, (name, len(pl.dangling))
        entry = res["poles"].setdefault(name, {"dangling": [list(x) for x in pl.dangling], "pairings": {}})
        for pname, ((i, j), (k, l)) in pairings().items():
            if pname in entry["pairings"] and all(entry["pairings"][pname][str(d)]["status"] in ("SAT", "UNSAT") for d in range(4)):
                continue
            row = {}
            for d in range(4):
                x, y = reps[d]
                f, yv = poles.pole_formula(pl, fixed={i: x, j: y})
                stem = f"{args.family}_{name}_{pname.replace('|', '-')}_d{d}"
                cnf = HEAVY / f"{stem}.cnf"
                f.write(cnf, [f"EXP-012 {stem}"])
                rec = solver.solve(cnf, HEAVY / f"{stem}.drat", CAP)
                item = {"status": rec["status"], "seconds": rec["seconds"]}
                if rec["status"] == "SAT":
                    model = set(rec["model"])
                    lab = {key: t for (key, t), var in yv.items() if var in model}
                    item["checker_ok"] = poles.check_pole(pl, lab)
                    dist = poles.line_distances()
                    item["other_connector_distance"] = dist[lab[("d", k)]][lab[("d", l)]]
                elif rec["status"] == "UNSAT":
                    item.update({"verified": rec.get("drat_trim_verified"), "proof_sha256": rec.get("proof_sha256")})
                row[str(d)] = item
            row["D"] = [d for d in range(4) if row[str(d)]["status"] == "SAT"]
            row["undecided"] = [d for d in range(4) if row[str(d)]["status"] not in ("SAT", "UNSAT")]
            entry["pairings"][pname] = row
            path.write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8", newline="\n")
            log(f"{name} pairing {pname}: D = {row['D']}, undecided {row['undecided']}")


if __name__ == "__main__":
    main()
