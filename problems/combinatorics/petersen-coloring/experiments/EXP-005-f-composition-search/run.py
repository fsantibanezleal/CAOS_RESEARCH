"""EXP-005: counterexample-guided search over compositions of the Petersen 4-pole F.

Deterministic up to solver model choice (CaDiCaL default seed), headless, CPU only. Resumable:
learned clauses are appended per class to E:/_Datos/caos-research/petersen-coloring/EXP-005/.
Exits nonzero on control failure. Run from the repository root with the repo .venv:

    .venv/Scripts/python.exe problems/combinatorics/petersen-coloring/experiments/EXP-005-f-composition-search/run.py [--classes 5,0;5,2] [--budget 7200]
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

from pcclib import compose, graphs, invariants, solver  # noqa: E402

ARTIFACTS = HERE / "artifacts"
HEAVY = Path("E:/_Datos/caos-research/petersen-coloring/EXP-005")
DATA = PROBLEM / "data"
CONTROLS = [(2, 0), (3, 2), (4, 4)]
POSITIVE = (6, 4)
TARGETS = [(5, 0), (5, 2), (5, 4), (6, 0), (6, 2), (5, 6), (5, 8), (5, 10), (4, 6), (4, 8), (4, 10), (4, 12), (4, 14), (4, 16), (4, 18)]


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def count_disjoint_f(g: graphs.Graph) -> tuple[int, int]:
    """Number of copies of F (8-sets with boundary 4 inducing F) and the max disjoint packing."""
    F = compose.F_GRAPH
    Fadj = [set(a) for a in F.adjacency()]
    Fdeg = [len(a) for a in Fadj]
    adj = g.adjacency()

    def iso(S: frozenset) -> bool:
        sub = {v: {w for w in adj[v] if w in S} for v in S}
        if sorted(len(sub[v]) for v in S) != sorted(Fdeg):
            return False
        order = sorted(range(8), key=lambda i: -Fdeg[i])
        mp: dict[int, int] = {}

        def rec(i: int) -> bool:
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
    best = 0

    def pack(i: int, chosen: int, used: frozenset) -> None:
        nonlocal best
        best = max(best, chosen)
        for jj in range(i, len(cs)):
            if not (cs[jj] & used):
                pack(jj + 1, chosen + 1, used | cs[jj])
    pack(0, 0, frozenset())
    return len(cs), best


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--classes", default="")
    ap.add_argument("--budget", type=int, default=7200)
    ap.add_argument("--max-iter", type=int, default=20000)
    ap.add_argument("--skip-controls", action="store_true")
    args = ap.parse_args()
    ARTIFACTS.mkdir(exist_ok=True)
    HEAVY.mkdir(parents=True, exist_ok=True)
    manifest_path = ARTIFACTS / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {
        "experiment": "EXP-005", "tools": solver.tool_versions(), "classes": {}, "predictions": {}}
    failures: list[str] = []

    if not args.skip_controls:
        # P2 first half: copies of F in the public counterexamples
        fcount = {}
        for name, fn in [("G52", "gjmmm-52.edgelist"), ("G112", "putman-112-main.edgelist"), ("H112", "putman-112-d3.edgelist")]:
            g = graphs.load_edgelist(DATA / fn)
            copies, disjoint = count_disjoint_f(g)
            fcount[name] = {"copies": copies, "max_disjoint": disjoint, "free_vertices": g.n - 8 * disjoint}
            log(f"{name}: {copies} copies of F, {disjoint} disjoint, {g.n - 8 * disjoint} free vertices")
        manifest["f_copies"] = fcount
        manifest["pcol_F_size"] = None
        compose.init_pcol(HEAVY)
        manifest["pcol_F_size"] = len(compose.PCOL_F)
        manifest["f_semiedge_automorphisms"] = [list(p) for p in compose.F_AUTS]
        for k, m in CONTROLS:
            res = compose.search(compose.Composition(k, m), HEAVY, args.budget, args.max_iter, log)
            manifest["classes"][res["class"]] = res
            log(f"control ({k},{m}) n={8*k+m}: {res['status']} after {res['iterations']} iterations, {res['learned']} clauses, {res['seconds']} s, found {len(res['found'])}")
            if not res["status"].startswith("exhausted") or res["found"]:
                failures.append(f"P1 control ({k},{m}): {res['status']} found {len(res['found'])}")
        k, m = POSITIVE
        res = compose.search(compose.Composition(k, m), HEAVY, args.budget, args.max_iter, log)
        manifest["classes"][res["class"]] = res
        log(f"positive control ({k},{m}): {res['status']} after {res['iterations']} iterations, found {len(res['found'])}")
        ok = bool(res["found"]) and all(f.get("petersen_verified") and f.get("normal5_verified") for f in res["found"][:1])
        if fcount["G52"]["max_disjoint"] != 6 or not ok:
            failures.append(f"P2 positive control: G52 disjoint {fcount['G52']['max_disjoint']}, found {len(res['found'])}")
        manifest["predictions"]["P1"] = not any(x.startswith("P1") for x in failures)
        manifest["predictions"]["P2"] = not any(x.startswith("P2") for x in failures)
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    classes = TARGETS if not args.classes else [tuple(int(x) for x in c.split(",")) for c in args.classes.split(";")]
    for k, m in classes:
        res = compose.search(compose.Composition(k, m), HEAVY, args.budget, args.max_iter, log)
        manifest["classes"][res["class"]] = res
        log(f"class ({k},{m}) n={8*k+m}: {res['status']} after {res['iterations']} iterations, {res['learned']} clauses, {res['seconds']} s, found {len(res['found'])}")
        manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    decided = {c: r["status"] for c, r in manifest["classes"].items()}
    found_small = [(c, f["n"], f["digest"]) for c, r in manifest["classes"].items() for f in r["found"] if f["n"] < 52]
    manifest["predictions"]["P3"] = {"committed_expectation": "no counterexample below 52 in the listed classes", "found_below_52": found_small, "statuses": decided}
    manifest["failures"] = failures
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    log("RESULT " + ("controls pass" if not failures else "FAILURES: " + "; ".join(failures)) + f"; found below 52: {found_small}")
    sys.exit(0 if not failures else 1)


if __name__ == "__main__":
    main()
