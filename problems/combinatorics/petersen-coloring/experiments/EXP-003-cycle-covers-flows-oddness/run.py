"""EXP-003: cycle double covers, flows, oddness and resistance of the certified counterexamples.

Deterministic, headless, CPU only (CaDiCaL in WSL, drat-trim). Exits nonzero on any check
failure. Run from the repository root with the repo .venv:

    .venv/Scripts/python.exe problems/combinatorics/petersen-coloring/experiments/EXP-003-cycle-covers-flows-oddness/run.py
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBLEM = HERE.parents[1]
sys.path.insert(0, str(PROBLEM / "code"))

from pcclib import checkers, encoders, graphs, solver  # noqa: E402

ARTIFACTS = HERE / "artifacts"
HEAVY = Path("E:/_Datos/caos-research/petersen-coloring/EXP-003")
DATA = PROBLEM / "data"
SAT_CAP = 1800


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def run(name: str, kind: str, g: graphs.Graph, bound: int | None = None) -> dict:
    m = len(g.edges)
    if kind == "cdc5":
        f = encoders.cycle_double_cover(g, 5)
    elif kind == "flow5":
        f = encoders.nowhere_zero_flow(g, 5)
    elif kind == "flow4":
        f = encoders.nowhere_zero_flow(g, 4)
    elif kind == "odd":
        f = encoders.oddness(g, bound)
    elif kind == "res":
        f = encoders.resistance(g, bound)
    else:
        raise ValueError(kind)
    stem = f"{name}_{kind}" + (f"_{bound}" if bound is not None else "")
    cnf_path = HEAVY / f"{stem}.cnf"
    f.write(cnf_path, [f"EXP-003 {stem}"])
    rec = solver.solve(cnf_path, HEAVY / f"{stem}.drat", SAT_CAP)
    rec.update({"instance": stem, "variables": f.nvars, "clauses": len(f.clauses)})
    if rec["status"] == "SAT":
        model = set(rec.pop("model"))
        if kind == "cdc5":
            cycles = [{e for e in range(m) if f.names[f"z_{e}_{i}"] in model} for i in range(5)]
            rec["checker_ok"] = checkers.check_cycle_double_cover(g, cycles)
            rec["witness"] = [sorted(C) for C in cycles]
        elif kind in ("flow5", "flow4"):
            k = 5 if kind == "flow5" else 4
            vals = [next(a for a in range(1, k) if f.names[f"w_{e}_{a}"] in model) for e in range(m)]
            rec["checker_ok"] = checkers.check_flow(g, vals, k)
            rec["witness"] = vals
        elif kind == "odd":
            M = {e for e in range(m) if f.names[f"m_{e}"] in model}
            odd = checkers.odd_cycles_of_two_factor(g, M)
            rec["checker_odd_cycles"] = odd
            rec["checker_ok"] = odd <= bound
            rec["witness"] = sorted(M)
        elif kind == "res":
            deleted = {e for e in range(m) if f.names[f"del_{e}"] in model}
            colors = {e: next(c for c in range(3) if f.names[f"x_{e}_{c}"] in model) for e in range(m) if e not in deleted}
            rec["checker_ok"] = checkers.check_three_edge_colorable_minus(g, colors, deleted) and len(deleted) <= bound
            rec["witness"] = {"deleted": sorted(deleted), "colors": [colors.get(e, -1) for e in range(m)]}
    log(f"{stem}: {rec['status']} in {rec['seconds']} s" + (
        f", checker_ok={rec.get('checker_ok')}" + (f", odd={rec.get('checker_odd_cycles')}" if kind == "odd" else "")
        if rec["status"] == "SAT" else f", verified={rec.get('drat_trim_verified')}" if rec["status"] == "UNSAT" else ""))
    return rec


def decide_min(name: str, kind: str, g: graphs.Graph, lo: int, hi: int, results: dict) -> int | None:
    """Least bound b in [lo, hi] with SAT, given UNSAT (verified) at b-1; None if undecided."""
    for b in range(lo, hi + 1):
        rec = run(name, kind, g, b)
        results[rec["instance"]] = rec
        if rec["status"] == "SAT" and rec.get("checker_ok"):
            return b
        if not (rec["status"] == "UNSAT" and rec.get("drat_trim_verified")):
            return None
    return None


def main() -> None:
    ARTIFACTS.mkdir(exist_ok=True)
    HEAVY.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []
    manifest: dict = {"experiment": "EXP-003", "tools": solver.tool_versions(), "predictions": {}}
    targets = {
        "G112": graphs.load_edgelist(DATA / "putman-112-main.edgelist"),
        "H112": graphs.load_edgelist(DATA / "putman-112-d3.edgelist"),
        "G52": graphs.load_edgelist(DATA / "gjmmm-52.edgelist"),
    }
    controls = {"petersen": graphs.petersen(), "K4": graphs.k4(), "prism": graphs.prism(), "J5": graphs.flower_snark(5)}
    res: dict = {}

    # invariant-first: the 5-CDC of G112
    first = run("G112", "cdc5", targets["G112"])
    res[first["instance"]] = first

    # P1 controls
    p1 = True
    for name, g in controls.items():
        r = run(name, "cdc5", g)
        res[r["instance"]] = r
        p1 &= r["status"] == "SAT" and r.get("checker_ok", False)
        r = run(name, "flow5", g)
        res[r["instance"]] = r
        p1 &= r["status"] == "SAT" and r.get("checker_ok", False)
        r = run(name, "flow4", g)
        res[r["instance"]] = r
        if name in ("petersen", "J5"):
            p1 &= r["status"] == "UNSAT" and r.get("drat_trim_verified", False)
        else:
            p1 &= r["status"] == "SAT" and r.get("checker_ok", False)
        want = 0 if name in ("K4", "prism") else 2
        odd = decide_min(name, "odd", g, 0 if want == 0 else 1, 2, res)
        rs = decide_min(name, "res", g, 0 if want == 0 else 1, 2, res)
        p1 &= odd == want and rs == want
        manifest.setdefault("control_values", {})[name] = {"oddness": odd, "resistance": rs}
    if not p1:
        failures.append("P1 controls")
    manifest["predictions"]["P1"] = p1

    # P6 corrupted witnesses on the Petersen graph
    p = controls["petersen"]
    cdc = [set(C) for C in res["petersen_cdc5"]["witness"]]
    broken = [set(C) for C in cdc]
    broken[0].discard(next(iter(broken[0])))
    flow = list(res["petersen_flow5"]["witness"])
    zeroed = flow[:]
    zeroed[0] = 0
    p6 = checkers.check_cycle_double_cover(p, cdc) and not checkers.check_cycle_double_cover(p, broken) \
        and checkers.check_flow(p, flow, 5) and not checkers.check_flow(p, zeroed, 5)
    if not p6:
        failures.append("P6 corrupted witnesses")
    manifest["predictions"]["P6"] = p6

    # P2-P5 targets
    values: dict = {}
    for name, g in targets.items():
        r = res.get(f"{name}_cdc5") or run(name, "cdc5", g)
        res[r["instance"]] = r
        if not (r["status"] == "SAT" and r.get("checker_ok")):
            failures.append(f"P2 {name} cdc5: {r['status']}")
        r = run(name, "flow5", g)
        res[r["instance"]] = r
        if not (r["status"] == "SAT" and r.get("checker_ok")):
            failures.append(f"P3 {name} flow5: {r['status']}")
        r = run(name, "flow4", g)
        res[r["instance"]] = r
        if not (r["status"] == "UNSAT" and r.get("drat_trim_verified")):
            failures.append(f"P3 {name} flow4: {r['status']}")
        odd = decide_min(name, "odd", g, 1, 4, res)
        rs = decide_min(name, "res", g, 1, 4, res)
        values[name] = {"oddness": odd, "resistance": rs}
        if odd is None:
            failures.append(f"P4 {name} oddness undecided")
        if rs is None:
            failures.append(f"P5 {name} resistance undecided")
    manifest["target_values"] = values
    manifest["predictions"]["P2"] = not any(x.startswith("P2") for x in failures)
    manifest["predictions"]["P3"] = not any(x.startswith("P3") for x in failures)
    manifest["predictions"]["P4"] = {"decided": not any(x.startswith("P4") for x in failures), "committed_expectation": 2, "values": {k: v["oddness"] for k, v in values.items()}}
    manifest["predictions"]["P5"] = {"decided": not any(x.startswith("P5") for x in failures), "committed_expectation": 2, "values": {k: v["resistance"] for k, v in values.items()}}
    manifest["instances"] = {k: {kk: vv for kk, vv in v.items() if kk != "witness"} for k, v in res.items()}
    manifest["heavy_files"] = {q.name: {"bytes": q.stat().st_size, "sha256": solver.sha256_file(q)} for q in sorted(HEAVY.glob("*")) if q.is_file()}
    manifest["failures"] = failures
    solver.write_json(ARTIFACTS / "manifest.json", manifest)
    witnesses = {k: v["witness"] for k, v in res.items() if v.get("witness") is not None and not k.startswith(("petersen", "K4", "prism", "J5"))}
    (ARTIFACTS / "witnesses.json").write_text(json.dumps(witnesses, separators=(",", ":")) + "\n", encoding="utf-8")
    log("RESULT " + ("ALL PREDICTIONS PASS" if not failures else "FAILURES: " + "; ".join(failures)))
    sys.exit(0 if not failures else 1)


if __name__ == "__main__":
    main()
