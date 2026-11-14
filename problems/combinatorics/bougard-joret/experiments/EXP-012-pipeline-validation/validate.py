"""EXP-012 Gates A to E: the production filter, prune hook, res/mod splitting and generator against independent truth.

Ground truth is networkx (Windows), which shares no code with the C programs; the C programs run in WSL.
  independence number: maximum clique of the complement (max_weight_clique, unit weights)
  vertex connectivity: node_connectivity

Usage: python validate.py <gate> [--build /root/exp012-build] [--nauty /root/caos-nauty/nauty2_8_9] [--jobs 4]
  cases  build the constructed graph set (Gates A and C) with its ground truth: artifacts/cases.jsonl
  a      Gate A: filter2 on every constructed graph at (a, k) in {alpha-1, alpha, alpha+1} x {kappa-1, kappa, kappa+1}
  b      Gate B: filter2 on slices of the production streams (k >= 6 or alpha = 7) at E = c-1, c, c+1
  c      Gate C: prune_alpha alone, ALPHA_BOUND = 2..8
  d      Gate D: the res/mod partition of the pruned generator (mod 1 against the union of mod 56)
  e      Gate E: generator counts against OEIS A001349, A002851, A006820
Each gate writes artifacts/gate-<x>.json and prints a one-line summary; the exit code is 1 on any disagreement.
"""
import argparse
import json
import random
import re
import subprocess
import sys
import time
import urllib.request
from collections import Counter
from math import ceil, comb
from multiprocessing import Pool
from pathlib import Path

import networkx as nx

HERE = Path(__file__).resolve().parent
ART = HERE / "artifacts"
EXPS = HERE.parent
# --exec: the command string reaches bash unchanged (without it wsl.exe re-parses it and expands $1 and the like)
WSL = ["wsl.exe", "-d", "Ubuntu-24.04", "--exec"]


def wpath(p):
    s = str(Path(p).resolve()).replace("\\", "/")
    return "/mnt/" + s[0].lower() + s[2:]


def wsl(cmd, stdin=None, timeout=None):
    r = subprocess.run(WSL + ["bash", "-c", cmd], input=stdin, capture_output=True, text=True, timeout=timeout)
    return r


def g6(G):
    return nx.to_graph6_bytes(G, header=False).decode().strip()


def alpha_of(G):
    return nx.max_weight_clique(nx.complement(G), weight=None)[1]


def truth(line):
    G = nx.from_graph6_bytes(line.encode())
    return alpha_of(G), nx.node_connectivity(G)


def t(n, a):
    q, r = divmod(n, a)
    return r * comb(q + 1, 2) + (a - r) * comb(q, 2)


# ---------------------------------------------------------------- the constructed graphs (Gates A and C)

def constructed():
    rng = random.Random(20261111)
    out = []

    def add(G, fam):
        if 2 <= G.number_of_nodes() <= 24:
            out.append((g6(nx.convert_node_labels_to_integers(G)), fam))

    for k in range(2, 10):
        for n in (10, 13, 16, 19, 22, 24):
            if n > k:
                add(nx.hkn_harary_graph(k, n), "harary")
    for _ in range(600):
        n = rng.randint(10, 24)
        S = rng.sample(range(1, n // 2 + 1), rng.randint(1, min(4, n // 2)))
        add(nx.circulant_graph(n, S), "circulant")
    for _ in range(600):
        d = rng.randint(3, 9)
        n = rng.randint(max(10, d + 1), 24)
        if n * d % 2:
            n -= 1
        add(nx.random_regular_graph(d, n, seed=rng.randrange(1 << 30)), "regular")
    for _ in range(600):
        n = rng.randint(10, 24)
        m = rng.randint(n // 2, 3 * n)
        add(nx.complement(nx.gnm_random_graph(n, m, seed=rng.randrange(1 << 30))), "complement-sparse")
    for _ in range(900):
        n = rng.randint(10, 24)
        a = rng.randint(2, 8)
        cuts = sorted(rng.sample(range(1, n), a - 1))
        sizes = [y - x for x, y in zip([0] + cuts, cuts + [n])]
        G = nx.Graph()
        start, blocks = 0, []
        for s in sizes:
            block = list(range(start, start + s))
            G.add_nodes_from(block)
            G.add_edges_from((u, v) for i, u in enumerate(block) for v in block[i + 1:])
            blocks.append(block)
            start += s
        for _ in range(rng.randint(0, 3 * n)):
            b1, b2 = rng.sample(range(a), 2)
            G.add_edge(rng.choice(blocks[b1]), rng.choice(blocks[b2]))
        add(G, "clique-union")
    for _ in range(600):
        n = rng.randint(10, 24)
        add(nx.gnp_random_graph(n, rng.choice([0.2, 0.3, 0.4, 0.5, 0.6, 0.7]), seed=rng.randrange(1 << 30)), "gnp")
    for f in sorted((EXPS / "EXP-011-extremal-structure" / "artifacts" / "extremal").glob("*.g6")):
        for line in f.read_text(encoding="utf-8").split():
            out.append((line, "exp011-extremal"))
    return out


def gate_cases(a):
    graphs = constructed()
    with Pool(a.jobs) as p:
        tr = p.map(truth, [x for x, _ in graphs], chunksize=20)
    with open(ART / "cases.jsonl", "w", encoding="utf-8") as fh:
        for (line, fam), (al, ka) in zip(graphs, tr):
            n = nx.from_graph6_bytes(line.encode()).number_of_nodes()
            fh.write(json.dumps({"g6": line, "family": fam, "n": n, "alpha": al, "kappa": ka}) + "\n")
    fams = Counter(f for _, f in graphs)
    print(f"cases: {len(graphs)} graphs; families {dict(fams)}; alpha range {min(x[0] for x in tr)}..{max(x[0] for x in tr)};"
          f" kappa range {min(x[1] for x in tr)}..{max(x[1] for x in tr)}")
    return 0


def load_cases():
    return [json.loads(l) for l in (ART / "cases.jsonl").read_text(encoding="utf-8").splitlines()]


# ---------------------------------------------------------------- Gate A

def gate_a(a):
    cases = load_cases()
    groups = {}
    for c in cases:
        for al in (c["alpha"] - 1, c["alpha"], c["alpha"] + 1):
            for k in (c["kappa"] - 1, c["kappa"], c["kappa"] + 1):
                if al >= 1 and 1 <= k <= 9:
                    groups.setdefault((al, k), []).append(c)
    decisions = sum(len(v) for v in groups.values())
    bad, kept_total, rows = 0, 0, []
    for (al, k), cs in sorted(groups.items()):
        r = wsl(f"{a.filter} {al} {k} --print", stdin="".join(c["g6"] + "\n" for c in cs), timeout=3600)
        got = Counter(r.stdout.split())
        want = Counter(c["g6"] for c in cs if c["alpha"] == al and c["kappa"] >= k)
        diff = (got - want) + (want - got)
        bad += sum(diff.values())
        kept_total += sum(got.values())
        rows.append({"a": al, "k": k, "graphs": len(cs), "kept": sum(got.values()), "expected": sum(want.values()),
                     "disagreements": sum(diff.values()), "stderr": r.stderr.strip()})
    res = {"graphs": len(cases), "decisions": decisions, "kept": kept_total, "disagreements": bad,
           "max_k": max(k for _, k in groups), "groups": rows}
    (ART / "gate-a.json").write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    print(f"Gate A: {len(cases)} graphs, {decisions} decisions over {len(groups)} (a,k) groups, {kept_total} kept, "
          f"{bad} disagreements")
    return 1 if bad else 0


# ---------------------------------------------------------------- Gate B

B_TRIPLES = [(19, 3, 6), (20, 3, 6), (21, 3, 6), (22, 3, 6), (22, 3, 7), (23, 3, 6), (23, 3, 7), (22, 7, 3),
             (23, 7, 3), (24, 7, 3), (24, 3, 7)]


def recorded_counts():
    """(n, alpha, k, E) -> (graphs generated, CPU seconds) of the pruned-generator records (56 parts, 28 processes)."""
    rec = {}
    for f in EXPS.glob("EXP-0*/artifacts/enum.jsonl"):
        for l in f.read_text(encoding="utf-8").splitlines():
            r = json.loads(l)
            if r.get("mod") == 56:
                rec[(r["n"], r["alpha"], r["k"], r["E"])] = (r["generated"], r["seconds"] * 28)
    return rec


def b_truth(args):
    line, al, k = args
    G = nx.from_graph6_bytes(line.encode())
    x = alpha_of(G)
    if x != al:
        return x, None, False
    ka = nx.node_connectivity(G)
    return x, ka, ka >= k


def gate_b(a):
    """Slices are sized from the records: about 1,500 graphs and about 120 CPU seconds of generation each, extrapolated
    by a factor of 10 per edge above the last recorded count. Finished slices in artifacts/gate-b.json are kept."""
    rec = recorded_counts()
    old = json.loads((ART / "gate-b.json").read_text(encoding="utf-8")) if (ART / "gate-b.json").exists() else None
    rows = old["slices"] if old else []
    done = {(r["n"], r["alpha"], r["k"], r["E"]) for r in rows}
    bad = sum(r["disagreements"] + r["alpha_above_bound"] for r in rows)
    total = sum(r["graphs"] for r in rows)
    for n, al, k in B_TRIPLES:
        c = t(n, al) + ceil(k * al / 2)
        for E in (c - 1, c, c + 1):
            if (n, al, k, E) in done:
                continue
            known = sorted((e, g, cpu) for (n2, a2, k2, e), (g, cpu) in rec.items() if (n2, a2, k2) == (n, al, k)
                           and e <= E and g > 0)
            if known:
                e0, g0, cpu0 = known[-1]
                f = 10 ** max(0, E - e0)
                mod = max(1, ceil(g0 * f / 1500), ceil(cpu0 * f / 120))
            else:
                mod = 100000
            t0 = time.time()
            r = wsl(f"timeout 3600 {a.nauty}/geng_a{al} -q -d{k} {n} {E}:{E} 0/{mod} | head -n 3000", timeout=3700)
            lines = r.stdout.split()
            fr = wsl(f"{a.filter} {al} {k} --print", stdin="".join(x + "\n" for x in lines), timeout=3600)
            got = Counter(fr.stdout.split())
            with Pool(a.jobs) as p:
                tr = p.map(b_truth, [(x, al, k) for x in lines], chunksize=10)
            want = Counter(x for x, (_, _, q) in zip(lines, tr) if q)
            prune_fail = sum(1 for x, _, _ in tr if x > al)
            diff = (got - want) + (want - got)
            bad += sum(diff.values()) + prune_fail
            total += len(lines)
            row = {"n": n, "alpha": al, "k": k, "E": E, "c": c, "slice": f"0/{mod}", "graphs": len(lines),
                   "alpha_eq": sum(1 for x, _, _ in tr if x == al), "kept": sum(got.values()),
                   "expected": sum(want.values()), "disagreements": sum(diff.values()),
                   "alpha_above_bound": prune_fail, "seconds": round(time.time() - t0, 1)}
            rows.append(row)
            print(json.dumps(row), flush=True)
            (ART / "gate-b.json").write_text(json.dumps({"graphs": total, "disagreements": bad, "slices": rows},
                                                        indent=1) + "\n", encoding="utf-8")
    print(f"Gate B: {total} graphs in {len(rows)} slices, {bad} disagreements")
    return 1 if bad else 0


# ---------------------------------------------------------------- Gate C

def gate_c(a):
    cases = load_cases()
    rng = random.Random(20261112)
    extra = []
    for n in range(8, 25):
        for p in (0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8):
            for _ in range(3):
                extra.append(g6(nx.gnp_random_graph(n, p, seed=rng.randrange(1 << 30))))
    with Pool(a.jobs) as p:
        ex_alpha = p.map(alpha_of, [nx.from_graph6_bytes(x.encode()) for x in extra], chunksize=20)
    items = [(c["g6"], c["alpha"]) for c in cases] + list(zip(extra, ex_alpha))
    rows, bad = [], 0
    for A in range(2, 9):
        r = wsl(f"{a.build}/prune_test_{A}", stdin="".join(x + "\n" for x, _ in items), timeout=3600)
        got = [int(v) for v in r.stdout.split()]
        if len(got) != len(items):
            raise SystemExit(f"harness at A={A} returned {len(got)} answers for {len(items)} graphs: {r.stderr}")
        want = [int(al > A) for _, al in items]
        d = sum(1 for x, y in zip(got, want) if x != y)
        bad += d
        rows.append({"bound": A, "graphs": len(items), "prune_true": sum(got), "expected_true": sum(want),
                     "disagreements": d})
    res = {"graphs": len(items), "decisions": len(items) * 7, "disagreements": bad, "bounds": rows}
    (ART / "gate-c.json").write_text(json.dumps(res, indent=1) + "\n", encoding="utf-8")
    print(f"Gate C: {len(items)} graphs x 7 bounds, {bad} disagreements")
    return 1 if bad else 0


# ---------------------------------------------------------------- Gate D

D_CASES = [(17, 5, 3, 29), (19, 3, 6, 60), (20, 4, 4, 48)]


def gate_d(a):
    rows, bad = [], 0
    for n, al, k, E in D_CASES:
        geng = f"{a.nauty}/geng_a{al}"
        # each part writes its own file: parallel writers into one pipe can interleave lines (first run, 2026-11-14)
        tmp = f"/tmp/exp012-gate-d-{n}-{al}-{k}-{E}"
        one = wsl(f"{geng} -q -d{k} {n} {E}:{E} 0/1 | sort | tee >(wc -l >&2) | sha256sum", timeout=7200)
        parts = wsl(f"rm -rf {tmp} && mkdir -p {tmp} && seq 0 55 | xargs -P {a.jobs} -I R sh -c "
                    f"'{geng} -q -d{k} {n} {E}:{E} R/56 > {tmp}/part-R.txt' && cat {tmp}/part-*.txt | sort "
                    f"| tee >(wc -l >&2) | sha256sum; rm -rf {tmp}", timeout=7200)
        h1, h2 = one.stdout.split()[0], parts.stdout.split()[0]
        c1, c2 = int(one.stderr.split()[-1]), int(parts.stderr.split()[-1])
        ok = h1 == h2 and c1 == c2
        bad += not ok
        rows.append({"n": n, "alpha": al, "k": k, "E": E, "mod1_graphs": c1, "mod56_graphs": c2,
                     "mod1_sha256": h1, "mod56_sha256": h2, "equal": ok})
        print(json.dumps(rows[-1]), flush=True)
    (ART / "gate-d.json").write_text(json.dumps({"cases": rows, "disagreements": bad}, indent=1) + "\n",
                                     encoding="utf-8")
    print(f"Gate D: {len(rows)} cases, {bad} disagreements")
    return 1 if bad else 0


# ---------------------------------------------------------------- Gate E

def oeis(aid):
    req = urllib.request.Request(f"https://oeis.org/{aid}/b{aid[1:]}.txt", headers={"User-Agent": "caos-research-validation"})
    text = urllib.request.urlopen(req, timeout=60).read().decode()
    return {int(x): int(y) for x, y in (l.split()[:2] for l in text.splitlines() if l and not l.startswith("#"))}


E_CASES = [("A001349", "-c", 9, 9), ("A001349", "-c", 10, 10),
           ("A002851", "-c -d3 -D3", 16, 8), ("A002851", "-c -d3 -D3", 18, 9), ("A002851", "-c -d3 -D3", 20, 10),
           ("A002851", "-c -d3 -D3", 22, 11),
           ("A006820", "-c -d4 -D4", 12, 12), ("A006820", "-c -d4 -D4", 13, 13), ("A006820", "-c -d4 -D4", 14, 14),
           ("A006820", "-c -d4 -D4", 15, 15)]


def gate_e(a):
    seqs = {aid: oeis(aid) for aid in sorted({x[0] for x in E_CASES})}
    rows, bad = [], 0
    for aid, opts, n, idx in E_CASES:
        t0 = time.time()
        r = wsl(f"seq 0 55 | xargs -P {a.jobs} -I R {a.nauty}/geng -u {opts} {n} R/56 2>&1 | "
                f"grep -o '[0-9]* graphs generated' | awk '{{s+=$1}} END {{print s}}'", timeout=14400)
        got = int(r.stdout.strip() or -1)
        want = seqs[aid].get(idx)
        ok = got == want
        bad += not ok
        rows.append({"oeis": aid, "index": idx, "geng": f"geng -u {opts} {n}", "count": got, "oeis_value": want,
                     "equal": ok, "seconds": round(time.time() - t0, 1)})
        print(json.dumps(rows[-1]), flush=True)
        (ART / "gate-e.json").write_text(json.dumps({"cases": rows, "disagreements": bad}, indent=1) + "\n",
                                         encoding="utf-8")
    print(f"Gate E: {len(rows)} counts, {bad} disagreements")
    return 1 if bad else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("gate", choices=["cases", "a", "b", "c", "d", "e"])
    ap.add_argument("--build", default="/root/exp012-build")
    ap.add_argument("--nauty", default="/root/caos-nauty/nauty2_8_9")
    ap.add_argument("--filter", default="/root/caos-nauty/filter2")
    ap.add_argument("--jobs", type=int, default=4)
    a = ap.parse_args()
    ART.mkdir(exist_ok=True)
    return {"cases": gate_cases, "a": gate_a, "b": gate_b, "c": gate_c, "d": gate_d, "e": gate_e}[a.gate](a)


if __name__ == "__main__":
    sys.exit(main())
