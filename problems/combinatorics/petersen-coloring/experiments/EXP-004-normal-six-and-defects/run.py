"""EXP-004: normal 6-edge-colorings and exact normality defects of the certified counterexamples.

Deterministic, headless, CPU only (CaDiCaL in WSL, drat-trim). Exits nonzero on any check
failure. Run from the repository root with the repo .venv:

    .venv/Scripts/python.exe problems/combinatorics/petersen-coloring/experiments/EXP-004-normal-six-and-defects/run.py
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
HEAVY = Path("E:/_Datos/caos-research/petersen-coloring/EXP-004")
DATA = PROBLEM / "data"
SAT_CAP = 1800
MAX_DEFECT = 6


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def run(name: str, kind: str, g: graphs.Graph, bound: int | None = None) -> dict:
    m = len(g.edges)
    if kind == "normal6":
        f = encoders.normal_coloring(g, 6)
    elif kind == "strong6":
        f = encoders.normal_coloring(g, 6, strong=True)
    elif kind == "ndef":
        f = encoders.normal_coloring(g, 5, defect_bound=bound)
    elif kind == "pdef":
        f = encoders.petersen_coloring(g, defect_bound=bound)
    else:
        raise ValueError(kind)
    stem = f"{name}_{kind}" + (f"_{bound}" if bound is not None else "")
    cnf_path = HEAVY / f"{stem}.cnf"
    f.write(cnf_path, [f"EXP-004 {stem}"])
    rec = solver.solve(cnf_path, HEAVY / f"{stem}.drat", SAT_CAP)
    rec.update({"instance": stem, "variables": f.nvars, "clauses": len(f.clauses)})
    if rec["status"] == "SAT":
        model = set(rec.pop("model"))
        if kind in ("normal6", "strong6"):
            colors = checkers.edge_color_map(model, f.names, m, 6)
            d = checkers.normal_defect(g, colors)
            rec["checker_defect"] = d
            rec["checker_ok"] = d == 0 and (kind != "strong6" or checkers.is_strong_normal(g, colors))
            rec["witness"] = colors
        elif kind == "ndef":
            colors = checkers.edge_color_map(model, f.names, m, 5)
            d = checkers.normal_defect(g, colors)
            rec["checker_defect"] = d
            rec["checker_ok"] = d <= bound
            rec["witness"] = colors
        else:
            images = checkers.edge_color_map(model, f.names, m, 15, prefix="y")
            d = checkers.petersen_defect(g, images)
            rec["checker_defect"] = d
            rec["checker_ok"] = d <= bound
            rec["witness"] = images
    log(f"{stem}: {rec['status']} in {rec['seconds']} s" + (
        f", checker_ok={rec.get('checker_ok')}, defect={rec.get('checker_defect')}" if rec["status"] == "SAT"
        else f", verified={rec.get('drat_trim_verified')} ({rec.get('drat_trim_seconds')} s)" if rec["status"] == "UNSAT" else ""))
    return rec


def ladder(name: str, kind: str, g: graphs.Graph, res: dict, start: int = 0) -> tuple[int | None, int, int]:
    """Least bound with SAT; returns (value or None, lowest undecided, highest decided UNSAT)."""
    last_unsat = start - 1
    for b in range(start, MAX_DEFECT + 1):
        r = run(name, kind, g, b)
        res[r["instance"]] = r
        if r["status"] == "SAT" and r.get("checker_ok"):
            return b, b, last_unsat
        if r["status"] == "UNSAT" and r.get("drat_trim_verified"):
            last_unsat = b
            continue
        return None, b, last_unsat
    return None, MAX_DEFECT + 1, last_unsat


def main() -> None:
    ARTIFACTS.mkdir(exist_ok=True)
    HEAVY.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []
    manifest: dict = {"experiment": "EXP-004", "tools": solver.tool_versions(), "predictions": {}}
    targets = {
        "G112": graphs.load_edgelist(DATA / "putman-112-main.edgelist"),
        "H112": graphs.load_edgelist(DATA / "putman-112-d3.edgelist"),
        "G52": graphs.load_edgelist(DATA / "gjmmm-52.edgelist"),
    }
    controls = {"petersen": graphs.petersen(), "J5": graphs.flower_snark(5)}
    res: dict = {}

    # invariant-first
    r = run("G112", "normal6", targets["G112"])
    res[r["instance"]] = r

    # P1 controls: defect 0 SAT on colorable controls
    p1 = True
    for name, g in controls.items():
        for kind in ("ndef", "pdef"):
            r = run(name, kind, g, 0)
            res[r["instance"]] = r
            p1 &= r["status"] == "SAT" and r.get("checker_ok", False)
        r = run(name, "strong6", g)
        res[r["instance"]] = r
    manifest["predictions"]["P1_controls"] = p1

    # P6 corrupted witness on the Petersen graph normal-5 witness
    pw = res["petersen_ndef_0"]["witness"]
    pg = controls["petersen"]
    inc = pg.incidence()
    a, b = inc[0][0], inc[0][1]
    corrupted = list(pw)
    corrupted[a], corrupted[b] = corrupted[b], corrupted[a]
    p6 = not checkers.check_proper(pg, corrupted) or checkers.normal_defect(pg, corrupted) > 0
    if not p6:
        failures.append("P6 corrupted witness accepted")
    manifest["predictions"]["P6"] = p6

    values: dict = {}
    for name, g in targets.items():
        r = res.get(f"{name}_normal6") or run(name, "normal6", g)
        res[r["instance"]] = r
        if not (r["status"] == "SAT" and r.get("checker_ok")):
            failures.append(f"P2 {name} normal6: {r['status']}")
        r = run(name, "strong6", g)
        res[r["instance"]] = r
        strong = r["status"] == "SAT" and r.get("checker_ok") or (False if r["status"] == "UNSAT" and r.get("drat_trim_verified") else None)
        if strong is None:
            failures.append(f"P3 {name} strong6 undecided: {r['status']}")
        nd, nd_lo, nd_unsat = ladder(name, "ndef", g, res)
        pd, pd_lo, pd_unsat = ladder(name, "pdef", g, res)
        if nd is None:
            failures.append(f"P4 {name} normal-5 defect undecided (> {nd_unsat})")
        if pd is None:
            failures.append(f"P5 {name} P-defect undecided (> {pd_unsat})")
        # bound-0 instances must be UNSAT with proofs (P1 second half)
        for kind in ("ndef", "pdef"):
            r0 = res[f"{name}_{kind}_0"]
            if not (r0["status"] == "UNSAT" and r0.get("drat_trim_verified")):
                p1 = False
        values[name] = {"normal_6": res[f"{name}_normal6"]["status"], "strong_normal_6": strong,
                        "normal5_defect": nd, "normal5_defect_lower_bound_exclusive": nd_unsat,
                        "petersen_defect": pd, "petersen_defect_lower_bound_exclusive": pd_unsat}
    if not p1:
        failures.append("P1 controls or bound-0 reproduction")
    manifest["predictions"]["P1"] = p1
    manifest["predictions"]["P2"] = not any(x.startswith("P2") for x in failures)
    manifest["predictions"]["P3"] = {"decided": not any(x.startswith("P3") for x in failures), "committed_expectation": True}
    manifest["predictions"]["P4"] = {"decided": not any(x.startswith("P4") for x in failures), "committed_expectation": 1}
    manifest["predictions"]["P5"] = {"decided": not any(x.startswith("P5") for x in failures), "committed_expectation": 1}
    manifest["target_values"] = values
    manifest["instances"] = {k: {kk: vv for kk, vv in v.items() if kk != "witness"} for k, v in res.items()}
    manifest["heavy_files"] = {q.name: {"bytes": q.stat().st_size, "sha256": solver.sha256_file(q)} for q in sorted(HEAVY.glob("*")) if q.is_file()}
    manifest["failures"] = failures
    solver.write_json(ARTIFACTS / "manifest.json", manifest)
    witnesses = {k: v["witness"] for k, v in res.items() if v.get("witness") is not None and not k.startswith(("petersen", "J5"))}
    (ARTIFACTS / "witnesses.json").write_text(json.dumps(witnesses, separators=(",", ":")) + "\n", encoding="utf-8")
    log("RESULT " + ("ALL PREDICTIONS PASS" if not failures else "FAILURES: " + "; ".join(failures)))
    sys.exit(0 if not failures else 1)


if __name__ == "__main__":
    main()
