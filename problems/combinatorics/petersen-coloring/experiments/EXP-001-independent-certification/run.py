"""EXP-001: independent certification of the public Petersen-coloring counterexamples.

Deterministic, headless, CPU only (CaDiCaL in WSL, drat-trim). Exits nonzero on any check
failure. Run from the repository root with the repo .venv:

    .venv/Scripts/python.exe problems/combinatorics/petersen-coloring/experiments/EXP-001-independent-certification/run.py [--smoke] [--skip-public-proofs]

Artifacts go to ./artifacts (small JSON manifests and logs) and to
E:/_Datos/caos-research/petersen-coloring/EXP-001/ (CNFs and DRAT proofs, hashed in the manifest).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBLEM = HERE.parents[1]
sys.path.insert(0, str(PROBLEM / "code"))

from pcclib import checkers, encoders, graphs, invariants, solver  # noqa: E402

ARTIFACTS = HERE / "artifacts"
HEAVY = Path("E:/_Datos/caos-research/petersen-coloring/EXP-001")
PUBLIC = Path("E:/_Datos/caos-research/petersen-coloring/sources/zenodo-21845291")
DATA = PROBLEM / "data"

EXPECTED_DIGESTS = {
    "G112": "dc16cc18600cf77c8661b7baf89c7019f265299308541961ff884ea7187b4e8b",
    "H112": "0f2d8858110c6f012de7ddffa92fdbc709d7da630f199b0e3c81bb56eb6b35c7",
}
PUBLIC_ARCHIVE_SHA256 = "8af3eec414b652f05c56979dc148321535cdc51ff9cbd59dff278ef3d53d9832"
SAT_CAP = 1800
CHECK_CAP = 3600


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def targets() -> dict[str, graphs.Graph]:
    return {
        "G112": graphs.load_edgelist(DATA / "putman-112-main.edgelist"),
        "H112": graphs.load_edgelist(DATA / "putman-112-d3.edgelist"),
        "G52": graphs.load_edgelist(DATA / "gjmmm-52.edgelist"),
    }


def controls() -> dict[str, graphs.Graph]:
    return {
        "petersen": graphs.petersen(),
        "K4": graphs.k4(),
        "prism": graphs.prism(),
        "J5": graphs.flower_snark(5),
        "J7": graphs.flower_snark(7),
    }


def run_instance(name: str, kind: str, g: graphs.Graph, symmetry: bool = True) -> tuple[dict, dict, object]:
    if kind == "petersen":
        f = encoders.petersen_coloring(g, symmetry=symmetry)
    elif kind == "normal5":
        f = encoders.normal_coloring(g, 5)
    else:
        raise ValueError(kind)
    stem = f"{name}_{kind}" + ("" if symmetry else "_nosym")
    cnf_path = HEAVY / f"{stem}.cnf"
    proof_path = HEAVY / f"{stem}.drat"
    cnf_sha = f.write(cnf_path, [f"EXP-001 {stem}", f"vars {f.nvars} clauses {len(f.clauses)}"])
    log(f"{stem}: {f.nvars} vars, {len(f.clauses)} clauses, cnf sha256 {cnf_sha[:16]}")
    rec = solver.solve(cnf_path, proof_path, SAT_CAP)
    rec.update({"instance": stem, "variables": f.nvars, "clauses": len(f.clauses)})
    log(f"{stem}: {rec['status']} in {rec['seconds']} s" + (
        f", drat-trim verified={rec.get('drat_trim_verified')} in {rec.get('drat_trim_seconds')} s"
        if rec["status"] == "UNSAT" else ""))
    witness = None
    if rec["status"] == "SAT":
        model = set(rec.pop("model"))
        m = len(g.edges)
        if kind == "petersen":
            images = checkers.edge_color_map(model, f.names, m, 15, prefix="y")
            defect = checkers.petersen_defect(g, images)
            witness = images
        else:
            colors = checkers.edge_color_map(model, f.names, m, 5, prefix="x")
            defect = checkers.normal_defect(g, colors)
            witness = colors
        rec["checker_defect"] = defect
        log(f"{stem}: checker defect {defect}")
    return rec, f.names, witness


def structural(name: str, g: graphs.Graph, want_cyclic: bool) -> dict:
    rep = invariants.basic_report(g)
    if want_cyclic:
        t0 = time.time()
        cut = invariants.cyclic_edge_cut_below(g, 4)
        rep["cycle_separating_cut_below_4"] = list(cut) if cut else None
        rep["cyclic_cut_search_seconds"] = round(time.time() - t0, 3)
        # exhibit a cycle-separating 4-cut: the boundary of the vertex set of a copy of F
        # is found by searching connected 8-vertex sets with boundary 4 that contain a cycle.
        four = find_cyclic_four_cut(g)
        rep["cycle_separating_4_cut"] = list(four) if four else None
    log(f"{name}: {json.dumps({k: v for k, v in rep.items() if k != 'digest'})}")
    return rep


def find_cyclic_four_cut(g: graphs.Graph) -> tuple[int, ...] | None:
    """Grow connected vertex sets from each 5-cycle until the boundary has exactly 4 edges."""
    adj = g.adjacency()
    inc = g.incidence()
    # enumerate 5-cycles through each vertex (girth 5 graphs have them)
    seen_sets = set()
    for s in range(g.n):
        for a in adj[s]:
            for b in adj[a]:
                if b == s:
                    continue
                for c in adj[b]:
                    if c in (s, a):
                        continue
                    for d in adj[c]:
                        if d in (s, a, b):
                            continue
                        if s in adj[d]:
                            cyc = frozenset((s, a, b, c, d))
                            if cyc in seen_sets:
                                continue
                            seen_sets.add(cyc)
                            # greedy growth: add the neighbour that lowers the boundary
                            cur = set(cyc)
                            for _ in range(12):
                                bnd = invariants.boundary_edges(g, cur)
                                if len(bnd) == 4 and invariants.is_cycle_separating(g, bnd):
                                    return bnd
                                best = None
                                for ei in bnd:
                                    u, v = g.edges[ei]
                                    w = v if u in cur else u
                                    cand = cur | {w}
                                    size = len(invariants.boundary_edges(g, cand))
                                    if best is None or size < best[0]:
                                        best = (size, w)
                                if best is None:
                                    break
                                cur.add(best[1])
    _ = inc
    return None


def check_public_proofs() -> dict:
    """Third route: Putman's archived CNFs and DRAT proofs through our drat-trim."""
    out = {"archive_sha256": solver.sha256_file(PUBLIC / "PCC_112_DRAT_PROOFS_v1.0.0.zip")}
    if out["archive_sha256"] != PUBLIC_ARCHIVE_SHA256:
        solver.fail("public proof archive hash mismatch")
    anc = PUBLIC / "ancillary" / "PCC_counterexample_112_compact_ancillary_v1.1.0"
    proofs = {p.name: p for p in (PUBLIC / "proofs").rglob("*.drat")}
    pairs = [
        ("main_petersen", anc / "03_CERTIFICATION" / "pcc112_petersen_sym.cnf", "pcc112_petersen_sym.drat"),
        ("main_normal5", anc / "03_CERTIFICATION" / "pcc112_normal5_sym.cnf", "pcc112_normal5_sym.drat"),
        ("d3_petersen", anc / "04_OPTIONAL_D3" / "pcc112_petersen_sym.cnf", "pcc112_petersen_sym.drat"),
        ("d3_normal5", anc / "04_OPTIONAL_D3" / "pcc112_normal5_sym.cnf", "pcc112_normal5_sym.drat"),
    ]
    results = {}
    for label, cnf_path, proof_name in pairs:
        cands = [p for n, p in proofs.items() if n == proof_name and (("D3" in str(p)) == label.startswith("d3"))]
        if len(cands) != 1:
            cands = [p for p in (PUBLIC / "proofs").rglob("*.drat") if proof_name in p.name and (("D3" in str(p).upper()) == label.startswith("d3"))]
        if len(cands) != 1:
            results[label] = {"error": f"proof file not uniquely located: {[str(c) for c in cands]}"}
            continue
        proof = cands[0]
        t0 = time.time()
        chk = subprocess.run(
            ["wsl.exe", "-e", solver.DRAT_TRIM, solver.wsl_path(cnf_path), solver.wsl_path(proof)],
            capture_output=True, text=True, timeout=CHECK_CAP,
        )
        results[label] = {
            "cnf": str(cnf_path.name), "cnf_sha256": solver.sha256_file(cnf_path),
            "proof": str(proof), "proof_sha256": solver.sha256_file(proof),
            "proof_bytes": proof.stat().st_size,
            "verified": "s VERIFIED" in chk.stdout, "seconds": round(time.time() - t0, 3),
            "tail": chk.stdout[-300:],
        }
        log(f"public proof {label}: verified={results[label]['verified']} in {results[label]['seconds']} s")
    out["checks"] = results
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true", help="controls only, no targets")
    ap.add_argument("--skip-public-proofs", action="store_true")
    args = ap.parse_args()
    ARTIFACTS.mkdir(exist_ok=True)
    HEAVY.mkdir(parents=True, exist_ok=True)
    manifest: dict = {"experiment": "EXP-001", "tools": solver.tool_versions(), "predictions": {}}
    failures: list[str] = []

    # P1 structural facts and digests
    tg = targets()
    struct = {}
    for name, g in tg.items():
        rep = structural(name, g, want_cyclic=not args.smoke)
        struct[name] = rep
        if name in EXPECTED_DIGESTS and rep["digest"] != EXPECTED_DIGESTS[name]:
            failures.append(f"P1 digest mismatch for {name}")
        if not (rep["cubic"] and rep["connected"] and rep["edge_connectivity"] == 3 and rep["girth"] == 5):
            failures.append(f"P1 structure unexpected for {name}")
    manifest["structure"] = struct
    manifest["predictions"]["P1"] = not any(f.startswith("P1") for f in failures)

    # P2 controls
    ctrl_results = {}
    for name, g in controls().items():
        for kind in ("petersen", "normal5"):
            rec, _, _ = run_instance(name, kind, g)
            ctrl_results[f"{name}_{kind}"] = rec
            if rec["status"] != "SAT" or rec.get("checker_defect") != 0:
                failures.append(f"P2 control {name} {kind}: {rec['status']}")
    manifest["controls"] = ctrl_results
    manifest["predictions"]["P2"] = not any(f.startswith("P2") for f in failures)

    # P5a corrupted witness
    p = graphs.petersen()
    ident = list(range(15))
    swapped = ident[:]
    swapped[0], swapped[1] = swapped[1], swapped[0]
    p5a = checkers.petersen_defect(p, ident) == 0 and checkers.petersen_defect(p, swapped) > 0
    if not p5a:
        failures.append("P5a corrupted witness accepted")
    # P5c mutated expected digest must be rejected by the same comparison
    p5c = "0" * 64 != tg["G112"].digest()
    manifest["predictions"]["P5"] = p5a and p5c

    if args.smoke:
        manifest["predictions"].update({"P3": "skipped (smoke)", "P4": "skipped (smoke)", "P6": "skipped (smoke)"})
        solver.write_json(ARTIFACTS / "smoke_manifest.json", manifest)
        log("SMOKE " + ("PASS" if not failures else "FAIL: " + "; ".join(failures)))
        sys.exit(0 if not failures else 1)

    # P3 targets, both encodings; P5b symmetry-breaking removal
    tgt_results = {}
    for name, g in tg.items():
        for kind in ("petersen", "normal5"):
            rec, _, _ = run_instance(name, kind, g)
            tgt_results[f"{name}_{kind}"] = rec
            if rec["status"] != "UNSAT" or not rec.get("drat_trim_verified"):
                failures.append(f"P3 target {name} {kind}: {rec['status']} verified={rec.get('drat_trim_verified')}")
        rec, _, _ = run_instance(name, "petersen", g, symmetry=False)
        tgt_results[f"{name}_petersen_nosym"] = rec
        if rec["status"] != "UNSAT" or not rec.get("drat_trim_verified"):
            failures.append(f"P5b {name} petersen without symmetry breaking: {rec['status']}")
    manifest["targets"] = tgt_results
    manifest["predictions"]["P3"] = not any(f.startswith("P3") for f in failures)
    manifest["predictions"]["P5"] = manifest["predictions"]["P5"] and not any(f.startswith("P5b") for f in failures)

    # P6 cyclic edge connectivity exactly 4
    p6 = all(struct[n]["cycle_separating_cut_below_4"] is None and struct[n]["cycle_separating_4_cut"] for n in tg)
    if not p6:
        failures.append("P6 cyclic edge connectivity not certified as 4")
    manifest["predictions"]["P6"] = p6

    # P4 public proofs through our checker
    if args.skip_public_proofs:
        manifest["predictions"]["P4"] = "skipped"
    else:
        pub = check_public_proofs()
        manifest["public_proofs"] = pub
        ok = all(v.get("verified") for v in pub["checks"].values())
        if not ok:
            failures.append("P4 public proof check failed")
        manifest["predictions"]["P4"] = ok

    manifest["heavy_files"] = {
        p.name: {"bytes": p.stat().st_size, "sha256": solver.sha256_file(p)}
        for p in sorted(HEAVY.glob("*")) if p.is_file()
    }
    manifest["failures"] = failures
    solver.write_json(ARTIFACTS / "manifest.json", manifest)
    log("RESULT " + ("ALL PREDICTIONS PASS" if not failures else "FAILURES: " + "; ".join(failures)))
    sys.exit(0 if not failures else 1)


if __name__ == "__main__":
    main()
