"""EXP-008: the invariant battery of EXP-002/003/004/006 on the second 52-vertex and the 68-vertex
counterexamples. Deterministic up to the solver's model choice, CPU only, resumable per stage.

Run from the repository root:

    .venv/Scripts/python.exe problems/combinatorics/petersen-coloring/experiments/EXP-008-battery-on-new-counterexamples/run.py --graph G52b --stage battery
    .venv/Scripts/python.exe .../run.py --graph G52b --stage pairs
    .venv/Scripts/python.exe .../run.py --graph G52b --stage edges
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBLEM = HERE.parents[1]
sys.path.insert(0, str(PROBLEM / "code"))

from pcclib import automorphisms, checkers, encoders, graphs, relaxed, solver  # noqa: E402

ARTIFACTS = HERE / "artifacts"
HEAVY = Path("E:/_Datos/caos-research/petersen-coloring/EXP-008")
DATA = PROBLEM / "data"
FILES = {"G52b": "gjmmmu-52-b.edgelist", "G68": "hog-57280-68.edgelist"}
CAP = 1800
PAIR_CAP = 600
EDGE_CAP = 900


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def save(path: Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, indent=1) + "\n", encoding="utf-8", newline="\n")


def solve(f, stem: str, cap: int = CAP) -> dict:
    cnf = HEAVY / f"{stem}.cnf"
    f.write(cnf, [f"EXP-008 {stem}"])
    rec = solver.solve(cnf, HEAVY / f"{stem}.drat", cap)
    rec.update({"instance": stem, "variables": f.nvars, "clauses": len(f.clauses)})
    return rec


def slim(rec: dict) -> dict:
    return {k: v for k, v in rec.items() if k not in ("model", "drat_trim_tail")}


def battery(name: str, g: graphs.Graph) -> dict:
    m = len(g.edges)
    out: dict = {"graph": name, "digest": g.digest(), "tools": solver.tool_versions(), "instances": {}}

    def put(rec: dict) -> dict:
        out["instances"][rec["instance"]] = slim(rec)
        tail = f"checker_ok={rec.get('checker_ok')}" if rec["status"] == "SAT" else f"verified={rec.get('drat_trim_verified')}"
        log(f"{rec['instance']}: {rec['status']} in {rec['seconds']} s, {tail}")
        save(ARTIFACTS / f"battery-{name}.json", out)
        return rec

    # P1 perfect matching covers
    for kind, count, enc, chk in (
        ("bf", 6, encoders.berge_fulkerson, checkers.check_berge_fulkerson),
        ("berge5", 5, lambda h: encoders.berge_cover(h, 5), checkers.check_berge_cover),
        ("berge4", 4, lambda h: encoders.berge_cover(h, 4), checkers.check_berge_cover),
        ("berge3", 3, lambda h: encoders.berge_cover(h, 3), checkers.check_berge_cover),
        ("fr", 3, encoders.fan_raspaud, checkers.check_fan_raspaud),
    ):
        f = enc(g)
        rec = solve(f, f"{name}_{kind}")
        if rec["status"] == "SAT":
            w = checkers.matchings_from_model(set(rec["model"]), f.names, m, count)
            rec["checker_ok"] = chk(g, w)
            rec["witness"] = [sorted(M) for M in w]
        put(rec)

    # P2 cycle double cover and flows
    f = encoders.cycle_double_cover(g, 5)
    rec = solve(f, f"{name}_cdc5")
    if rec["status"] == "SAT":
        model = set(rec["model"])
        cycles = [{e for e in range(m) if f.names[f"z_{e}_{i}"] in model} for i in range(5)]
        rec["checker_ok"] = checkers.check_cycle_double_cover(g, cycles)
        rec["witness"] = [sorted(C) for C in cycles]
    put(rec)
    for k in (5, 4):
        f = encoders.nowhere_zero_flow(g, k)
        rec = solve(f, f"{name}_flow{k}")
        if rec["status"] == "SAT":
            model = set(rec["model"])
            vals = [next(a for a in range(1, k) if f.names[f"w_{e}_{a}"] in model) for e in range(m)]
            rec["checker_ok"] = checkers.check_flow(g, vals, k)
            rec["witness"] = vals
        put(rec)

    # P3 oddness and resistance, from both sides
    for kind in ("odd", "res"):
        value = None
        for b in range(1, 7):
            f = encoders.oddness(g, b) if kind == "odd" else encoders.resistance(g, b)
            rec = solve(f, f"{name}_{kind}_{b}")
            if rec["status"] == "SAT":
                model = set(rec["model"])
                if kind == "odd":
                    M = {e for e in range(m) if f.names[f"m_{e}"] in model}
                    cnt = checkers.odd_cycles_of_two_factor(g, M)
                    rec["checker_odd_cycles"] = cnt
                    rec["checker_ok"] = cnt <= b
                    rec["witness"] = sorted(M)
                else:
                    deleted = {e for e in range(m) if f.names[f"del_{e}"] in model}
                    colors = {e: next(c for c in range(3) if f.names[f"x_{e}_{c}"] in model) for e in range(m) if e not in deleted}
                    rec["checker_ok"] = checkers.check_three_edge_colorable_minus(g, colors, deleted) and len(deleted) <= b
                    rec["witness"] = {"deleted": sorted(deleted), "colors": [colors.get(e, -1) for e in range(m)]}
            put(rec)
            if rec["status"] == "SAT" and rec.get("checker_ok"):
                value = b
                break
            if not (rec["status"] == "UNSAT" and rec.get("drat_trim_verified")):
                break
        out["oddness" if kind == "odd" else "resistance"] = value

    # P4 normal 6 and strong normal 6
    for strong in (False, True):
        f = encoders.normal_coloring(g, 6, strong=strong)
        rec = solve(f, f"{name}_normal6" + ("_strong" if strong else ""))
        if rec["status"] == "SAT":
            colors = checkers.edge_color_map(set(rec["model"]), f.names, m, 6)
            rec["checker_defect"] = checkers.normal_defect(g, colors)
            rec["checker_ok"] = rec["checker_defect"] == 0 and (not strong or checkers.is_strong_normal(g, colors))
            rec["witness"] = colors
        put(rec)

    # P6 upper bound: a proper 5-edge-coloring with at most two abnormal edges
    f = encoders.normal_coloring(g, 5, strong=False, defect_bound=2)
    rec = solve(f, f"{name}_normal5_defect_le2")
    if rec["status"] == "SAT":
        colors = checkers.edge_color_map(set(rec["model"]), f.names, m, 5)
        rec["checker_defect"] = checkers.normal_defect(g, colors)
        rec["checker_ok"] = rec["checker_defect"] <= 2
        rec["witness"] = colors
    put(rec)
    return out


def pairs(name: str, g: graphs.Graph) -> None:
    path = ARTIFACTS / f"pairs-{name}.json"
    res = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"graph": name, "pairs": {}}
    stars = {frozenset(s) for s in graphs.petersen().incidence()}
    inc = g.incidence()
    t0 = time.time()
    for u, v in itertools.combinations(range(g.n), 2):
        key = f"{u}-{v}"
        if key in res["pairs"]:
            continue
        f = relaxed.petersen_relaxed_vertices(g, {u, v})
        rec = solve(f, f"pairs/{name}_relax_{u}_{v}", PAIR_CAP)
        entry = {"status": rec["status"], "seconds": rec["seconds"]}
        if rec["status"] == "SAT":
            images = checkers.edge_color_map(set(rec["model"]), f.names, len(g.edges), 15, prefix="y")
            bad = [w for w in range(g.n) if len({images[e] for e in inc[w]}) != 3 or frozenset(images[e] for e in inc[w]) not in stars]
            entry.update({"bad_vertices": bad, "critical_pair": 1 <= len(bad) and set(bad) <= {u, v}, "witness": images})
        elif rec["status"] == "UNSAT":
            entry.update({"verified": rec.get("drat_trim_verified"), "proof_sha256": rec.get("proof_sha256")})
        res["pairs"][key] = entry
        if len(res["pairs"]) % 50 == 0:
            save(path, res)
            log(f"{name}: {len(res['pairs'])} pairs, {sum(1 for e in res['pairs'].values() if e.get('critical_pair'))} critical, {round(time.time() - t0)} s")
    crit = [k for k, e in res["pairs"].items() if e.get("critical_pair")]
    bad2 = [k for k, e in res["pairs"].items() if e.get("critical_pair") and len(e["bad_vertices"]) == 2]
    res["summary"] = {"pairs": len(res["pairs"]), "critical": len(crit), "critical_with_exactly_two_bad": len(bad2),
                      "unsat_verified": [k for k, e in res["pairs"].items() if e["status"] == "UNSAT" and e.get("verified")],
                      "undecided": [k for k, e in res["pairs"].items() if e["status"] not in ("SAT", "UNSAT")]}
    save(path, res)
    log(f"RESULT {name}: {len(crit)} of {len(res['pairs'])} pairs critical, undecided {len(res['summary']['undecided'])}")


def edges(name: str, g: graphs.Graph) -> None:
    path = ARTIFACTS / f"edges-{name}.json"
    perms = automorphisms.automorphisms(g)
    assert all(automorphisms.is_automorphism(g, p) for p in perms)
    orbits = automorphisms.edge_orbits(g, perms)
    res = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"graph": name, "edges": {}}
    res.update({"automorphisms": perms, "edge_orbits": orbits})
    log(f"{name}: {len(perms)} automorphisms, {len(orbits)} edge orbits")
    for orbit in orbits:
        e = orbit[0]
        if str(e) in res["edges"]:
            continue
        f = relaxed.normal5_relaxed_edge(g, e)
        rec = solve(f, f"edges/{name}_relax_e{e}", EDGE_CAP)
        entry = {"status": rec["status"], "seconds": rec["seconds"], "verified": rec.get("drat_trim_verified"), "cnf_sha256": rec.get("cnf_sha256")}
        if rec["status"] == "SAT":
            colors = checkers.edge_color_map(set(rec["model"]), f.names, len(g.edges), 5)
            entry.update({"checker_defect": checkers.normal_defect(g, colors), "witness": colors})
        res["edges"][str(e)] = entry
        save(path, res)
        log(f"{name} edge {e} {g.edges[e]}: {rec['status']} in {rec['seconds']} s, verified={rec.get('drat_trim_verified')}")
    res["all_representatives_refuted"] = all(res["edges"].get(str(o[0]), {}).get("status") == "UNSAT" and res["edges"][str(o[0])].get("verified") for o in orbits)
    save(path, res)
    log(f"RESULT {name}: all orbit representatives refuted: {res['all_representatives_refuted']}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", required=True, choices=sorted(FILES))
    ap.add_argument("--stage", required=True, choices=["battery", "pairs", "edges"])
    args = ap.parse_args()
    ARTIFACTS.mkdir(exist_ok=True)
    (HEAVY / "pairs").mkdir(parents=True, exist_ok=True)
    (HEAVY / "edges").mkdir(parents=True, exist_ok=True)
    g = graphs.load_edgelist(DATA / FILES[args.graph])
    {"battery": battery, "pairs": pairs, "edges": edges}[args.stage](args.graph, g)


if __name__ == "__main__":
    main()
