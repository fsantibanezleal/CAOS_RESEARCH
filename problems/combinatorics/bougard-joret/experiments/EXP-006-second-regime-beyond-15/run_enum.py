"""EXP-005 exhaustive route: f(n, alpha, k) by complete enumeration (nauty geng + the exact C filter).

For one triple and one edge count E, `geng -q -d<k> <n> <E>:<E> <res>/<mod>` lists every non-isomorphic graph on
n vertices with E edges and minimum degree >= k (necessary for k-connectivity), split into <mod> disjoint parts
run in parallel; `filter <alpha> <k>` keeps those with independence number exactly alpha and connectivity >= k.
f(n, alpha, k) is the least E with a kept graph. Runs inside WSL (geng and filter are Linux binaries).

Usage (in WSL): python3 run_enum.py <geng> <filter> <n> <alpha> <k> <Emin> <Emax> [--jobs J] [--mod M]
Appends one JSON line per E to artifacts/enum.jsonl: graphs generated, kept, seconds.
"""
import argparse
import json
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent


def part(geng, filt, n, alpha, k, E, res, mod):
    p1 = subprocess.Popen([geng, "-q", f"-d{k}", str(n), f"{E}:{E}", f"{res}/{mod}"], stdout=subprocess.PIPE)
    p2 = subprocess.run([filt, str(alpha), str(k), "--print"], stdin=p1.stdout, capture_output=True, text=True)
    p1.stdout.close()
    if p1.wait() != 0:
        raise SystemExit(f"geng failed on part {res}/{mod}")
    tail = p2.stderr.strip().split()
    return int(tail[1]), int(tail[3]), p2.stdout.split()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("geng")
    ap.add_argument("filter")
    for name in ("n", "alpha", "k", "Emin", "Emax"):
        ap.add_argument(name, type=int)
    ap.add_argument("--jobs", type=int, default=24)
    ap.add_argument("--mod", type=int, default=96)
    a = ap.parse_args()
    for E in range(a.Emin, a.Emax + 1):
        t0 = time.time()
        with ThreadPoolExecutor(a.jobs) as ex:
            res = list(ex.map(lambda r: part(a.geng, a.filter, a.n, a.alpha, a.k, E, r, a.mod), range(a.mod)))
        rec = {"n": a.n, "alpha": a.alpha, "k": a.k, "E": E, "generated": sum(r[0] for r in res),
               "kept": sum(r[1] for r in res), "examples": [g for r in res for g in r[2]][:5],
               "mod": a.mod, "seconds": round(time.time() - t0, 1)}
        (HERE / "artifacts").mkdir(exist_ok=True)
        with open(HERE / "artifacts" / "enum.jsonl", "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec) + "\n")
        print(json.dumps({k: v for k, v in rec.items() if k != "examples"}), flush=True)


if __name__ == "__main__":
    main()
