"""EXP-011 step 1: regenerate every extremal graph at the conjectured edge count c = t(n,alpha) + ceil(k alpha/2).

For each triple, `geng_a<alpha> -q -d<k> n c:c res/mod` piped into `filter2 alpha k --print`, over `mod` disjoint parts
run in parallel; all qualifying graph6 lines are written to artifacts/extremal/<n>_<alpha>_<k>.g6 and the counts to
artifacts/collect.jsonl. Runs inside WSL (Linux binaries).

Usage: python3 collect.py <nauty dir with geng_a*> <filter2> <triples: n,a,k;n,a,k;...> [--jobs J] [--mod M]
"""
import argparse
import json
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from math import ceil, comb
from pathlib import Path

HERE = Path(__file__).resolve().parent


def t(n, a):
    q, r = divmod(n, a)
    return r * comb(q + 1, 2) + (a - r) * comb(q, 2)


def part(geng, filt, n, a, k, c, res, mod):
    p1 = subprocess.Popen([geng, "-q", f"-d{k}", str(n), f"{c}:{c}", f"{res}/{mod}"], stdout=subprocess.PIPE)
    p2 = subprocess.run([filt, str(a), str(k), "--print"], stdin=p1.stdout, capture_output=True, text=True)
    p1.stdout.close()
    if p1.wait() != 0:
        raise SystemExit(f"geng failed on part {res}/{mod}")
    tail = p2.stderr.strip().split()
    return int(tail[1]), int(tail[3]), p2.stdout.split()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("nauty")
    ap.add_argument("filter")
    ap.add_argument("triples")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--mod", type=int, default=56)
    a = ap.parse_args()
    out = HERE / "artifacts" / "extremal"
    out.mkdir(parents=True, exist_ok=True)
    for spec in a.triples.split(";"):
        n, al, k = (int(x) for x in spec.split(","))
        c = t(n, al) + ceil(k * al / 2)
        t0 = time.time()
        geng = f"{a.nauty}/geng_a{al}"
        with ThreadPoolExecutor(a.jobs) as ex:
            res = list(ex.map(lambda r: part(geng, a.filter, n, al, k, c, r, a.mod), range(a.mod)))
        graphs = [g for r in res for g in r[2]]
        (out / f"{n}_{al}_{k}.g6").write_text("\n".join(graphs) + ("\n" if graphs else ""), encoding="utf-8")
        rec = {"n": n, "alpha": al, "k": k, "E": c, "generated": sum(r[0] for r in res),
               "kept": sum(r[1] for r in res), "seconds": round(time.time() - t0, 1)}
        with open(HERE / "artifacts" / "collect.jsonl", "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec) + "\n")
        print(json.dumps(rec), flush=True)


if __name__ == "__main__":
    main()
