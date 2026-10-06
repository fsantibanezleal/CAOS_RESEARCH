"""EXP-013: conducted charge orbits of 6-poles (shape a: H - u - w; shape b: H - e1 - e2 - e3).

    .venv/Scripts/python.exe .../run.py --source P --shape a [--workers 8]

One formula per (6-pole, split, orbit): every vertex good and the first connector's charge equal to
the orbit's representative class. Writes artifacts/conduct-<source>-<shape>.json.
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
import time
from multiprocessing import Pool
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBLEM = HERE.parents[1]
sys.path.insert(0, str(PROBLEM / "code"))

from pcclib import automorphisms, charges, graphs, invariants, poles, solver  # noqa: E402

ARTIFACTS = HERE / "artifacts"
HEAVY = Path("E:/_Datos/caos-research/petersen-coloring/EXP-013")
DATA = PROBLEM / "data"
CAP = 120


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def generalized_petersen(n: int, k: int) -> graphs.Graph:
    edges = [(i, (i + 1) % n) for i in range(n)] + [(i, n + i) for i in range(n)] + [(n + i, n + (i + k) % n) for i in range(n)]
    return graphs.Graph.from_edges(edges)


def load(name: str) -> graphs.Graph:
    return {"P": graphs.petersen, "J5": lambda: graphs.flower_snark(5), "J7": lambda: graphs.flower_snark(7),
            "Dodeca": lambda: generalized_petersen(10, 2),
            "G52": lambda: graphs.load_edgelist(DATA / "gjmmm-52.edgelist")}[name]()


def orbit_reps(g: graphs.Graph, items: list[tuple], perms, act) -> list[tuple]:
    reps, seen = [], set()
    for it in items:
        if it in seen:
            continue
        reps.append(it)
        for p in perms:
            seen.add(act(p, it))
    return reps


def poles_for(g: graphs.Graph, shape: str):
    perms = automorphisms.automorphisms(g)
    adj = g.adjacency()
    if shape == "a":
        pairs = [(u, w) for u, w in itertools.combinations(range(g.n), 2) if w not in adj[u]]
        reps = orbit_reps(g, pairs, perms, lambda p, it: tuple(sorted((p[it[0]], p[it[1]]))))
        out = []
        for u, w in reps:
            pl = poles.pole(g, removed_vertices=(u, w))
            uend = [j for j, (x, ei) in enumerate(pl.dangling) if u in g.edges[ei]]
            wend = [j for j, (x, ei) in enumerate(pl.dangling) if w in g.edges[ei]]
            out.append((f"v{u}-v{w}", pl, [(tuple(uend), tuple(wend))]))
        return out, len(perms)
    idx = {e: i for i, e in enumerate(g.edges)}
    triples = [t for t in itertools.combinations(range(len(g.edges)), 3)
               if len({x for i in t for x in g.edges[i]}) == 6]

    def act(p, t):
        return tuple(sorted(idx[(min(p[g.edges[i][0]], p[g.edges[i][1]]), max(p[g.edges[i][0]], p[g.edges[i][1]]))] for i in t))

    reps = orbit_reps(g, triples, perms, act)
    out = []
    for t in reps:
        pl = poles.pole(g, removed_edges=t)
        splits = [(c1, tuple(j for j in range(6) if j not in c1)) for c1 in itertools.combinations(range(6), 3) if 0 in c1]
        out.append(("e" + "-e".join(map(str, t)), pl, splits))
    return out, len(perms)


def add_class(f, y, ends, target_sig):
    for i, c in enumerate(charges.cycle_basis()):
        bits = []
        for j in ends:
            b = f.fresh()
            ts = [t for t in range(15) if c >> t & 1]
            for t in ts:
                f.add(-y[("d", j), t], b)
            f.add(-b, *[y[("d", j), t] for t in ts])
            bits.append(b)
        r = target_sig[i]
        for signs in itertools.product((0, 1), repeat=3):
            if sum(signs) % 2 != r:
                f.add(*[(-bits[k] if signs[k] else bits[k]) for k in range(3)])


def job(args):
    src, shape, name, splitno, c1, c2, orbit = args
    g = load(src)
    if shape == "a":
        u, w = [int(x[1:]) for x in name.split("-")]
        pl = poles.pole(g, removed_vertices=(u, w))
    else:
        pl = poles.pole(g, removed_edges=tuple(int(x[1:]) for x in name.split("-")))
    name_of, reps = charges.orbit_table()
    target = charges.signature(charges.vec(reps[orbit]))
    f, y = poles.pole_formula(pl)
    add_class(f, y, c1, target)
    stem = f"{src}_{shape}_{name}_s{splitno}_{orbit}"
    cnf = HEAVY / f"{stem}.cnf"
    f.write(cnf, [f"EXP-013 {stem}"])
    rec = solver.solve(cnf, HEAVY / f"{stem}.drat", CAP)
    item = {"pole": name, "split": splitno, "c1": list(c1), "orbit": orbit, "status": rec["status"], "seconds": rec["seconds"]}
    if rec["status"] == "SAT":
        model = set(rec["model"])
        lab = {key: t for (key, t), var in y.items() if var in model}
        ok = poles.check_pole(pl, lab)
        s1 = charges.signature(charges.vec(lab[("d", j)] for j in c1))
        s2 = charges.signature(charges.vec(lab[("d", j)] for j in c2))
        item.update({"checker_ok": ok and s1 == target and s2 == target})
    elif rec["status"] == "UNSAT":
        item["verified"] = rec.get("drat_trim_verified")
    return item


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--shape", required=True, choices=["a", "b"])
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()
    ARTIFACTS.mkdir(exist_ok=True)
    HEAVY.mkdir(parents=True, exist_ok=True)
    g = load(args.source)
    cut5 = invariants.cyclic_edge_cut_below(g, 5) if len(g.edges) <= 45 else "not computed"
    cut4 = invariants.cyclic_edge_cut_below(g, 4) if len(g.edges) <= 45 else "see EXP-001"
    plist, naut = poles_for(g, args.shape)
    jobs = [(args.source, args.shape, name, si, c1, c2, orb) for name, pl, splits in plist for si, (c1, c2) in enumerate(splits) for orb in charges.ORBITS]
    log(f"{args.source} shape {args.shape}: |Aut| = {naut}, {len(plist)} 6-poles, {len(jobs)} formulas; cyclic cut below 5: {cut5}")
    # Every answer is appended as it arrives, so a killed run resumes where it stopped.
    partial = HEAVY / f"conduct-{args.source}-{args.shape}.partial.jsonl"
    rows = [json.loads(x) for x in partial.read_text(encoding="utf-8").splitlines() if x.strip()] if partial.exists() else []
    done = {(r["pole"], r["split"], r["orbit"]) for r in rows}
    todo = [j for j in jobs if (j[2], j[3], j[6]) not in done]
    log(f"resuming with {len(rows)} stored answers, {len(todo)} formulas to run")
    with Pool(args.workers) as pool, partial.open("a", encoding="utf-8", newline="\n") as fh:
        for r in pool.imap_unordered(job, todo, chunksize=1):
            rows.append(r)
            fh.write(json.dumps(r) + "\n")
            fh.flush()
    table: dict = {}
    for r in rows:
        key = f"{r['pole']}|s{r['split']}"
        table.setdefault(key, {"pole": r["pole"], "split": r["split"], "c1": r["c1"], "orbits": {}})["orbits"][r["orbit"]] = {k: v for k, v in r.items() if k in ("status", "seconds", "checker_ok", "verified")}
    for v in table.values():
        v["D"] = [o for o in charges.ORBITS if v["orbits"][o]["status"] == "SAT"]
        v["undecided"] = [o for o in charges.ORBITS if v["orbits"][o]["status"] not in ("SAT", "UNSAT")]
    out = {"source": args.source, "shape": args.shape, "n": g.n, "aut_order": naut,
           "cyclic_cut_below_5": list(cut5) if isinstance(cut5, tuple) else cut5,
           "cyclic_cut_below_4": list(cut4) if isinstance(cut4, tuple) else cut4,
           "poles": table}
    (ARTIFACTS / f"conduct-{args.source}-{args.shape}.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8", newline="\n")
    from collections import Counter
    log(f"RESULT {args.source} {args.shape}: D-set counts {dict(Counter(tuple(v['D']) for v in table.values()))}; "
        f"checker failures {sum(1 for r in rows if r['status'] == 'SAT' and not r.get('checker_ok'))}; "
        f"unverified UNSAT {sum(1 for r in rows if r['status'] == 'UNSAT' and not r.get('verified'))}; undecided {sum(1 for r in rows if r['status'] not in ('SAT', 'UNSAT'))}")


if __name__ == "__main__":
    main()
