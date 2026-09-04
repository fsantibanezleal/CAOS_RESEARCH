"""EXP-002: perfect matching covers of the certified counterexamples.

Deterministic, headless, CPU only (CaDiCaL in WSL, drat-trim). Exits nonzero on any check
failure. Run from the repository root with the repo .venv:

    .venv/Scripts/python.exe problems/combinatorics/petersen-coloring/experiments/EXP-002-perfect-matching-covers/run.py
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
HEAVY = Path("E:/_Datos/caos-research/petersen-coloring/EXP-002")
DATA = PROBLEM / "data"
SAT_CAP = 1800


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def instance(name: str, kind: str, g: graphs.Graph) -> tuple[dict, list[set[int]] | None]:
    count = {"bf": 6, "berge5": 5, "berge4": 4, "berge3": 3, "fr": 3}[kind]
    if kind == "bf":
        f = encoders.berge_fulkerson(g)
    elif kind == "fr":
        f = encoders.fan_raspaud(g)
    else:
        f = encoders.berge_cover(g, count)
    stem = f"{name}_{kind}"
    cnf_path = HEAVY / f"{stem}.cnf"
    f.write(cnf_path, [f"EXP-002 {stem}"])
    rec = solver.solve(cnf_path, HEAVY / f"{stem}.drat", SAT_CAP)
    rec.update({"instance": stem, "variables": f.nvars, "clauses": len(f.clauses)})
    witness = None
    if rec["status"] == "SAT":
        model = set(rec.pop("model"))
        witness = checkers.matchings_from_model(model, f.names, len(g.edges), count)
        if kind == "bf":
            ok = checkers.check_berge_fulkerson(g, witness)
        elif kind == "fr":
            ok = checkers.check_fan_raspaud(g, witness)
        else:
            ok = checkers.check_berge_cover(g, witness)
        rec["checker_ok"] = ok
        rec["witness"] = [sorted(M) for M in witness]
    log(f"{stem}: {rec['status']} in {rec['seconds']} s" + (
        f", checker_ok={rec.get('checker_ok')}" if rec["status"] == "SAT" else
        f", verified={rec.get('drat_trim_verified')}" if rec["status"] == "UNSAT" else ""))
    return rec, witness


def main() -> None:
    ARTIFACTS.mkdir(exist_ok=True)
    HEAVY.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []
    manifest: dict = {"experiment": "EXP-002", "tools": solver.tool_versions(), "predictions": {}}
    targets = {
        "G112": graphs.load_edgelist(DATA / "putman-112-main.edgelist"),
        "H112": graphs.load_edgelist(DATA / "putman-112-d3.edgelist"),
        "G52": graphs.load_edgelist(DATA / "gjmmm-52.edgelist"),
    }
    controls = {"petersen": graphs.petersen(), "K4": graphs.k4(), "prism": graphs.prism(), "J5": graphs.flower_snark(5)}

    # P1 controls
    expected = {
        ("petersen", "bf"): "SAT", ("petersen", "berge5"): "SAT", ("petersen", "berge4"): "UNSAT", ("petersen", "fr"): "SAT",
        ("K4", "bf"): "SAT", ("K4", "berge4"): "SAT", ("K4", "berge3"): "SAT", ("K4", "fr"): "SAT",
        ("prism", "bf"): "SAT", ("prism", "berge4"): "SAT", ("prism", "berge3"): "SAT", ("prism", "fr"): "SAT",
        ("J5", "bf"): "SAT", ("J5", "fr"): "SAT",
    }
    ctrl = {}
    for (name, kind), want in expected.items():
        rec, _ = instance(name, kind, controls[name])
        ctrl[f"{name}_{kind}"] = rec
        good = rec["status"] == want and (rec.get("checker_ok", True) if want == "SAT" else rec.get("drat_trim_verified", False))
        if not good:
            failures.append(f"P1 control {name} {kind}: {rec['status']} wanted {want}")
    rec, _ = instance("J5", "berge4", controls["J5"])
    ctrl["J5_berge4"] = rec
    manifest["controls"] = ctrl
    manifest["predictions"]["P1"] = not any(x.startswith("P1") for x in failures)

    # P5 corrupted witnesses (on the Petersen graph's BF witness)
    bf_p = ctrl["petersen_bf"]["witness"]
    ms = [set(M) for M in bf_p]
    swapped = [ms[1], ms[0]] + ms[2:]
    moved = [set(M) for M in ms]
    e = next(iter(moved[0]))
    moved[0].remove(e)
    moved[0].add(next(x for x in range(15) if x not in moved[0] and x != e))
    p5 = checkers.check_berge_fulkerson(controls["petersen"], swapped) and not checkers.check_berge_fulkerson(controls["petersen"], moved)
    if not p5:
        failures.append("P5 corrupted witness handling")
    manifest["predictions"]["P5"] = p5

    # P2-P4 targets: BF first (invariant-first), then berge5, fr, berge4
    tg = {}
    index = {}
    for name, g in targets.items():
        for kind in ("bf", "berge5", "fr", "berge4"):
            rec, _ = instance(name, kind, g)
            tg[f"{name}_{kind}"] = rec
            if kind in ("bf", "berge5", "fr"):
                if rec["status"] != "SAT" or not rec.get("checker_ok"):
                    failures.append(f"P{2 if kind == 'bf' else 3} {name} {kind}: {rec['status']}")
            else:
                if rec["status"] == "SAT" and rec.get("checker_ok"):
                    index[name] = 4
                elif rec["status"] == "UNSAT" and rec.get("drat_trim_verified"):
                    index[name] = 5
                else:
                    failures.append(f"P4 {name} berge4 undecided: {rec['status']}")
    manifest["targets"] = tg
    manifest["perfect_matching_index"] = index
    manifest["predictions"]["P2"] = not any(x.startswith("P2") for x in failures)
    manifest["predictions"]["P3"] = not any(x.startswith("P3") for x in failures)
    manifest["predictions"]["P4"] = {"decided": not any(x.startswith("P4") for x in failures), "index": index, "committed_expectation": 4}
    manifest["heavy_files"] = {p.name: {"bytes": p.stat().st_size, "sha256": solver.sha256_file(p)} for p in sorted(HEAVY.glob("*")) if p.is_file()}
    manifest["failures"] = failures
    solver.write_json(ARTIFACTS / "manifest.json", manifest)
    # compact witness file for the wiki and manuscript
    witnesses = {k: v["witness"] for k, v in tg.items() if v.get("witness")}
    (ARTIFACTS / "witnesses.json").write_text(json.dumps(witnesses, separators=(",", ":")) + "\n", encoding="utf-8")
    log("RESULT " + ("ALL PREDICTIONS PASS" if not failures else "FAILURES: " + "; ".join(failures)))
    sys.exit(0 if not failures else 1)


if __name__ == "__main__":
    main()
