"""EXP-006: critical vertices and edges of the certified counterexamples by designated relaxation.

Deterministic, headless, CPU only (CaDiCaL in WSL, drat-trim). Resumable through the manifest.
Run from the repository root with the repo .venv:

    .venv/Scripts/python.exe problems/combinatorics/petersen-coloring/experiments/EXP-006-critical-vertices/run.py [--edges-112]
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

from pcclib import checkers, compose, encoders, graphs, relaxed, solver  # noqa: E402

ARTIFACTS = HERE / "artifacts"
HEAVY = Path("E:/_Datos/caos-research/petersen-coloring/EXP-006")
DATA = PROBLEM / "data"
VERTEX_CAP = 600
EDGE_CAP = 1800


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def free_vertices(g: graphs.Graph) -> list[int]:
    """Vertices outside a maximum packing of disjoint copies of F (EXP-005 routine)."""
    sys.path.insert(0, str(PROBLEM / "experiments" / "EXP-005-f-composition-search"))
    from run import count_disjoint_f  # noqa: E402
    _ = count_disjoint_f
    F = compose.F_GRAPH
    Fadj = [set(a) for a in F.adjacency()]
    Fdeg = [len(a) for a in Fadj]
    adj = g.adjacency()
    from pcclib import invariants

    def iso(S):
        sub = {v: {w for w in adj[v] if w in S} for v in S}
        if sorted(len(sub[v]) for v in S) != sorted(Fdeg):
            return False
        order = sorted(range(8), key=lambda i: -Fdeg[i])
        mp = {}

        def rec(i):
            if i == 8:
                return True
            fi = order[i]
            for v in S:
                if v in mp.values() or len(sub[v]) != Fdeg[fi]:
                    continue
                if all((mp[fj] in sub[v]) == (fj in Fadj[fi]) for fj in mp):
                    mp[fi] = v
                    if rec(i + 1):
                        return True
                    del mp[fi]
            return False
        return rec(0)

    found = set()
    for s in range(g.n):
        stack = [(frozenset([s]), set(adj[s]))]
        seen = set()
        while stack:
            cur, frontier = stack.pop()
            if cur in seen:
                continue
            seen.add(cur)
            if len(cur) == 8:
                if len(invariants.boundary_edges(g, set(cur))) == 4 and iso(cur):
                    found.add(cur)
                continue
            for w in sorted(frontier):
                if w < s:
                    continue
                nxt = cur | {w}
                stack.append((nxt, (frontier | set(adj[w])) - nxt))
    cs = list(found)
    best: list[frozenset] = []

    def pack(i, chosen, used):
        nonlocal best
        if len(chosen) > len(best):
            best = list(chosen)
        for jj in range(i, len(cs)):
            if not (cs[jj] & used):
                pack(jj + 1, chosen + [cs[jj]], used | cs[jj])
    pack(0, [], frozenset())
    covered = set().union(*best) if best else set()
    return sorted(v for v in range(g.n) if v not in covered)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--edges-112", action="store_true", help="also sweep the free-vertex edges of the 112-vertex graphs")
    ap.add_argument("--skip-vertices", action="store_true", help="addendum 2: skip the single-vertex sweeps (decided by the parity lemma)")
    args = ap.parse_args()
    ARTIFACTS.mkdir(exist_ok=True)
    HEAVY.mkdir(parents=True, exist_ok=True)
    mpath = ARTIFACTS / "manifest.json"
    manifest = json.loads(mpath.read_text(encoding="utf-8")) if mpath.exists() else {
        "experiment": "EXP-006", "tools": solver.tool_versions(), "vertices": {}, "edges": {}, "predictions": {}}
    failures: list[str] = []
    targets = {
        "G52": graphs.load_edgelist(DATA / "gjmmm-52.edgelist"),
        "G112": graphs.load_edgelist(DATA / "putman-112-main.edgelist"),
        "H112": graphs.load_edgelist(DATA / "putman-112-d3.edgelist"),
    }

    def save():
        mpath.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # P5 reproduction: bound-0 on G52 (plain Petersen encoding) is UNSAT
    g = targets["G52"]
    f0 = encoders.petersen_coloring(g)
    c0 = HEAVY / "G52_bound0.cnf"
    f0.write(c0)
    r0 = solver.solve(c0, HEAVY / "G52_bound0.drat", VERTEX_CAP)
    manifest["reproduction_G52_bound0"] = {k: v for k, v in r0.items() if k != "model"}
    if not (r0["status"] == "UNSAT" and r0.get("drat_trim_verified")):
        failures.append("P5 bound-0 reproduction")

    for name, g in targets.items():
        fv = free_vertices(g)
        manifest.setdefault("free_vertices", {})[name] = fv
        log(f"{name}: free vertices {fv}")
        if args.skip_vertices:
            continue
        order = fv + [v for v in range(g.n) if v not in fv]
        res = manifest["vertices"].setdefault(name, {})
        for v in order:
            if str(v) in res:
                continue
            f = relaxed.petersen_relaxed_vertex(g, v)
            cp = HEAVY / f"{name}_relax_v{v}.cnf"
            f.write(cp)
            rec = solver.solve(cp, HEAVY / f"{name}_relax_v{v}.drat", VERTEX_CAP)
            entry = {"status": rec["status"], "seconds": rec["seconds"], "cnf_sha256": rec["cnf_sha256"]}
            if rec["status"] == "SAT":
                model = set(rec["model"])
                images = checkers.edge_color_map(model, f.names, len(g.edges), 15, prefix="y")
                d = checkers.petersen_defect(g, images)
                inc = g.incidence()
                p = graphs.petersen()
                stars = {frozenset(s) for s in p.incidence()}
                bad = [u for u in range(g.n) if frozenset(images[e] for e in inc[u]) not in stars or len({images[e] for e in inc[u]}) != 3]
                entry.update({"checker_defect": d, "bad_vertices": bad, "critical": d == 1 and bad == [v], "witness": images})
                if v == fv[0] and name == "G52":
                    # P5 corrupted witness: swap two edge images at a non-relaxed vertex
                    w = next(u for u in range(g.n) if u != v and v not in g.adjacency()[u])
                    a, b = inc[w][0], inc[w][1]
                    corrupted = list(images)
                    corrupted[a], corrupted[b] = corrupted[b], corrupted[a]
                    manifest["predictions"]["P5_corrupted_rejected"] = checkers.petersen_defect(g, corrupted) > 1
            elif rec["status"] == "UNSAT":
                entry.update({"verified": rec.get("drat_trim_verified"), "proof_sha256": rec.get("proof_sha256"), "critical": False})
            res[str(v)] = entry
            log(f"{name} vertex {v}: {rec['status']} in {rec['seconds']} s" + (f", defect {entry.get('checker_defect')}, bad {entry.get('bad_vertices')}" if rec["status"] == "SAT" else ""))
            save()
        crit = [int(v) for v, e in res.items() if e.get("critical")]
        noncrit = [int(v) for v, e in res.items() if e.get("status") == "UNSAT" and e.get("verified")]
        manifest.setdefault("critical_vertices", {})[name] = crit
        manifest.setdefault("noncritical_vertices_verified", {})[name] = noncrit
        log(f"{name}: critical {crit}; non-critical verified {len(noncrit)}; undecided {[int(v) for v, e in res.items() if e.get('status') not in ('SAT', 'UNSAT')]}")
        save()

    # edges: all edges of G52; free-vertex edges of the 112s only with --edges-112
    edge_plan = {"G52": list(range(len(targets["G52"].edges)))}
    if args.edges_112:
        for name in ("G112", "H112"):
            g = targets[name]
            fv = set(manifest["free_vertices"][name])
            edge_plan[name] = [e for e, (u, v) in enumerate(g.edges) if u in fv or v in fv]
    for name, edges in edge_plan.items():
        g = targets[name]
        res = manifest["edges"].setdefault(name, {})
        for e in edges:
            if str(e) in res:
                continue
            f = relaxed.normal5_relaxed_edge(g, e)
            cp = HEAVY / f"{name}_relax_e{e}.cnf"
            f.write(cp)
            rec = solver.solve(cp, HEAVY / f"{name}_relax_e{e}.drat", EDGE_CAP)
            entry = {"status": rec["status"], "seconds": rec["seconds"], "cnf_sha256": rec["cnf_sha256"]}
            if rec["status"] == "SAT":
                model = set(rec["model"])
                colors = checkers.edge_color_map(model, f.names, len(g.edges), 5)
                d = checkers.normal_defect(g, colors)
                entry.update({"checker_defect": d, "critical": d == 1, "witness": colors})
            elif rec["status"] == "UNSAT":
                entry.update({"verified": rec.get("drat_trim_verified"), "critical": False})
            res[str(e)] = entry
            log(f"{name} edge {e} {g.edges[e]}: {rec['status']} in {rec['seconds']} s" + (f", defect {entry.get('checker_defect')}" if rec["status"] == "SAT" else ""))
            save()
            if name != "G52" and entry.get("critical"):
                break  # one critical edge suffices for the 112-vertex graphs
        manifest.setdefault("critical_edges", {})[name] = [int(e) for e, r in res.items() if r.get("critical")]
        save()

    cv = manifest.get("critical_vertices", {})
    manifest["predictions"]["P1"] = bool(cv.get("G52"))
    manifest["predictions"]["P2"] = bool(cv.get("G112")) and bool(cv.get("H112"))
    manifest["predictions"]["P3"] = bool(manifest.get("noncritical_vertices_verified", {}).get("G52"))
    manifest["predictions"]["P4"] = bool(manifest.get("critical_edges", {}).get("G52"))
    manifest["predictions"]["P5"] = (not any(x.startswith("P5") for x in failures)) and bool(manifest["predictions"].get("P5_corrupted_rejected"))
    for k in ("P1", "P2", "P4", "P5"):
        if not manifest["predictions"][k]:
            failures.append(k)
    manifest["failures"] = failures
    save()
    log("RESULT " + ("ALL PREDICTIONS PASS" if not failures else "FAILURES: " + "; ".join(failures)))
    sys.exit(0 if not failures else 1)


if __name__ == "__main__":
    main()
