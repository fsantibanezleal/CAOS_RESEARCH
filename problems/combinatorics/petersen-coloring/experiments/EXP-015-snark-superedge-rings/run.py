"""EXP-015: rings of superedges cut from the cyclically 5-edge-connected snarks of order at most 28 (hypothesis.md).

    .venv/Scripts/python.exe .../run.py gates          # G0 inputs, G1 block matrices, G2 = R4 (G52 control)
    .venv/Scripts/python.exe .../run.py blocks         # every block of F, process pool, resumable
    .venv/Scripts/python.exe .../run.py rings2         # R1: every pair of generators of F
    .venv/Scripts/python.exe .../run.py rings3         # R2: every cyclic triple of generators of F22
    .venv/Scripts/python.exe .../run.py crosscheck     # R3: 500 random rings against CaDiCaL on the explicit graph
    .venv/Scripts/python.exe .../run.py describe       # descriptive measurements
    .venv/Scripts/python.exe .../run.py zero           # solver checks of every zero-trace ring (and of G52, as a self-test)
    .venv/Scripts/python.exe .../run.py all            # gates, blocks, rings2, rings3, crosscheck, describe, zero

A block `B(G; u, w) = G - u - w` of a snark G with u, w at distance at least 2 has L = the dangling ends at the former
neighbors of u and R = those at the former neighbors of w (each ordered by the neighbor's index). It enters a ring in both
orientations, each followed by the six junction permutations (12 generators). A ring of generators g_1 ... g_t is Petersen
colorable if and only if some sector of g_1 ... g_t has a nonzero diagonal (code/pcclib/transfer.py, EXP-014).

Environment overrides (device-agnostic defaults): EXP015_SOURCES, EXP015_DATA.
"""

from __future__ import annotations

import os

for _v in ("OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "OMP_NUM_THREADS"):
    os.environ.setdefault(_v, "12")

import argparse
import base64
import hashlib
import importlib.util
import itertools
import json
import multiprocessing as mp
import queue
import random
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
PROBLEM = HERE.parents[1]
sys.path.insert(0, str(PROBLEM / "code"))

from pcclib import graphs, invariants, poles, solver, transfer  # noqa: E402

ARTIFACTS = HERE / "artifacts"
SOURCES = Path(os.environ.get("EXP015_SOURCES", "E:/_Datos/caos-research/petersen-coloring/sources/hog-snarks-cyc5"))
DATA = Path(os.environ.get("EXP015_DATA", "E:/_Datos/caos-research/petersen-coloring/EXP-015"))
SECTORS = transfer.SECTORS
PERMS = transfer.PERMS
ORDERS = (10, 20, 22, 24, 26, 28)
EXPECTED_COUNTS = {10: 1, 20: 1, 22: 2, 24: 2, 26: 10, 28: 75}
EXP014 = PROBLEM / "experiments" / "EXP-014-transfer-semigroups"
G52_CUT_EDGES = [8, 26, 39, 40, 48, 59]
SEED = 20261115
BLOCK_TIMEOUT_S = 600
SECOND_ENCODING_TIMEOUT_S = 7200
MAX_WORKERS = 12


def log(msg: str) -> None:
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    try:
        ARTIFACTS.mkdir(exist_ok=True)
        with open(ARTIFACTS / "run-log.txt", "a", encoding="utf-8", newline="\n") as fh:
            fh.write(line + "\n")
    except OSError:
        pass


def write_json(path: Path, obj) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(obj, indent=1, sort_keys=False) + "\n", encoding="utf-8", newline="\n")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def update_results(key: str, value) -> None:
    path = ARTIFACTS / "results.json"
    cur = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    cur[key] = value
    write_json(path, cur)


def read_results() -> dict:
    path = ARTIFACTS / "results.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


# ----------------------------------------------------------------------------------------------------------------------
# Inputs (G0)
# ----------------------------------------------------------------------------------------------------------------------

def source_file(n: int) -> Path:
    return SOURCES / f"Generated_graphs.{n}.05.sn.cyc5.g6"


def load_g6(path: Path) -> list[graphs.Graph]:
    import networkx as nx

    out = []
    for line in Path(path).read_bytes().split(b"\n"):
        line = line.strip()
        if not line:
            continue
        nxg = nx.from_graph6_bytes(line)
        g = graphs.Graph.from_edges(sorted((min(a, b), max(a, b)) for a, b in nxg.edges))
        if len(g.edges) != nxg.number_of_edges():
            raise ValueError("graph6 line with a repeated edge")
        out.append(g)
    return out


def three_edge_colorable(g: graphs.Graph) -> bool:
    from pysat.solvers import Solver

    m = len(g.edges)
    var = lambda e, c: 3 * e + c + 1  # noqa: E731
    clauses = []
    for e in range(m):
        clauses.append([var(e, c) for c in range(3)])
        clauses += [[-var(e, a), -var(e, b)] for a, b in itertools.combinations(range(3), 2)]
    for inc in g.incidence():
        for e1, e2 in itertools.combinations(inc, 2):
            clauses += [[-var(e1, c), -var(e2, c)] for c in range(3)]
    with Solver(name="cadical153", bootstrap_with=clauses) as s:
        return bool(s.solve())


def cyclic_connectivity(g: graphs.Graph) -> int:
    """Smallest size of a cycle-separating edge cut when it is at most 4 (exact search), else 5 (meaning at least 5)."""
    cut = invariants.cyclic_edge_cut_below(g, 5)
    return 5 if cut is None else len(cut)


def g0_graph(g: graphs.Graph) -> dict:
    return {"order": g.n, "edges": len(g.edges), "cubic": g.is_cubic(), "simple": len(set(g.edges)) == len(g.edges),
            "girth": invariants.girth(g), "cyclic_edge_connectivity_at_least_5_checked_exactly": True,
            "cyclically_5_edge_connected": invariants.cyclic_edge_cut_below(g, 5) is None,
            "three_edge_colorable": three_edge_colorable(g)}


def check_input_hashes() -> dict:
    sums = SOURCES / "SHA256SUMS"
    if not sums.exists():
        raise SystemExit(f"G0 FAILED: {sums} is missing")
    want = {}
    for line in sums.read_text(encoding="utf-8").splitlines():
        if line.strip():
            h, name = line.split(None, 1)
            want[name.strip().lstrip("*")] = h
    rec = {}
    for n in ORDERS:
        f = source_file(n)
        if not f.exists():
            raise SystemExit(f"G0 FAILED: input file {f} is missing (never download a replacement silently)")
        got = sha256_file(f)
        if want.get(f.name) != got:
            raise SystemExit(f"G0 FAILED: SHA-256 of {f.name} is {got}, SHA256SUMS says {want.get(f.name)}")
        rec[f.name] = got
    return rec


def _g0_job(arg):
    n, i = arg
    return n, i, g0_graph(load_g6(source_file(n))[i])


def gate_g0(workers: int) -> dict:
    hashes = check_input_hashes()
    counts = {n: len(load_g6(source_file(n))) for n in ORDERS}
    ok_counts = counts == EXPECTED_COUNTS
    tasks = [(n, i) for n in ORDERS for i in range(counts[n])]
    with mp.get_context("spawn").Pool(workers) as pool:
        rows = pool.map(_g0_job, tasks, chunksize=1)
    bad = [(n, i, r) for n, i, r in rows if not (r["cubic"] and r["simple"] and r["girth"] >= 5 and r["cyclically_5_edge_connected"]
                                                   and not r["three_edge_colorable"] and r["order"] == n)]
    return {"sha256": hashes, "counts": counts, "counts_as_listed": ok_counts, "graphs_checked": len(rows), "failures": bad,
            "passed": ok_counts and not bad}


# ----------------------------------------------------------------------------------------------------------------------
# Blocks
# ----------------------------------------------------------------------------------------------------------------------

def orbit_pairs(g: graphs.Graph) -> tuple[list[tuple[int, int, int]], int]:
    """One representative (u, w, distance) per Aut(G)-orbit of unordered vertex pairs at distance at least 2, and |Aut(G)|."""
    import networkx as nx
    from networkx.algorithms.isomorphism import GraphMatcher

    nxg = nx.Graph(list(g.edges))
    auts = list(GraphMatcher(nxg, nxg).isomorphisms_iter())
    dist = dict(nx.all_pairs_shortest_path_length(nxg))
    seen, reps = set(), []
    for u, w in itertools.combinations(range(g.n), 2):
        if dist[u][w] < 2 or (u, w) in seen:
            continue
        reps.append((u, w, dist[u][w]))
        for a in auts:
            x, y = a[u], a[w]
            seen.add((min(x, y), max(x, y)))
    return reps, len(auts)


def superedge_block(g: graphs.Graph, u: int, w: int, name: str) -> transfer.Block:
    pl = poles.pole(g, removed_vertices=(u, w))
    left = sorted((x, j) for j, (x, ei) in enumerate(pl.dangling) if u in g.edges[ei])
    right = sorted((x, j) for j, (x, ei) in enumerate(pl.dangling) if w in g.edges[ei])
    assert len(left) == 3 and len(right) == 3
    return transfer.Block(name, pl, tuple(j for _, j in left), tuple(j for _, j in right))


def double_ends(blk: transfer.Block):
    """(position in L, position in R) of the vertex adjacent to both u and w (distance 2), else None."""
    lv = [blk.pole.dangling[j][0] for j in blk.left]
    rv = [blk.pole.dangling[j][0] for j in blk.right]
    common = set(lv) & set(rv)
    if not common:
        return None
    assert len(common) == 1, "girth at least 5 allows one common neighbor"
    x = next(iter(common))
    return lv.index(x), rv.index(x)


def triple_frame(blk: transfer.Block, orient: str, pi_index: int):
    """What decides whether two blocks in a ring of two share a parallel edge, in the frame of the generator."""
    d = double_ends(blk)
    if d is None:
        return None
    a, b = d if orient == "f" else (d[1], d[0])
    return (a, b, PERMS[pi_index])


def ring2_is_simple(f1, f2) -> bool:
    """A ring of two blocks has parallel edges only through the vertex adjacent to both u and w of each block:
    R_1's end at x_1 joins L_2's end at x_2 and R_2's end at x_2 joins L_1's end at x_1."""
    if f1 is None or f2 is None:
        return True
    a1, b1, p1 = f1
    a2, b2, p2 = f2
    return not (p1[b1] == a2 and p2[b2] == a1)


def count_nonsimple_pairs(frames: list) -> int:
    """Unordered pairs of generator triples (a triple with itself included) whose ring of two is not simple."""
    cls = Counter(f for f in frames if f is not None)
    ordered = sum(c1 * c2 for f1, c1 in cls.items() for f2, c2 in cls.items() if not ring2_is_simple(f1, f2))
    diag = sum(c for f, c in cls.items() if not ring2_is_simple(f, f))
    assert (ordered + diag) % 2 == 0
    return (ordered + diag) // 2


def block_generators(mats: dict[str, np.ndarray]) -> list[tuple[str, int, dict[str, np.ndarray]]]:
    """The twelve generators of a block: both orientations, each followed by each junction permutation."""
    out = []
    for orient, mm in (("f", mats), ("r", transfer.transpose(mats))):
        for pi_index, pi in enumerate(PERMS):
            out.append((orient, pi_index, transfer.with_junction(mm, pi)))
    return out


def graph_id(n: int, i: int) -> str:
    return f"S{n}-{i:03d}"


def build_block_table() -> dict:
    path = DATA / "blocktable.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    per_graph, blocks = {}, []
    for n in ORDERS:
        for i, g in enumerate(load_g6(source_file(n))):
            reps, naut = orbit_pairs(g)
            by_dist = Counter(d for _, _, d in reps)
            gid = graph_id(n, i)
            per_graph[gid] = {"order": n, "aut": naut, "orbits_by_distance": {str(d): c for d, c in sorted(by_dist.items())}}
            for u, w, d in reps:
                if n <= 26 or d == 5:
                    blocks.append({"id": f"{gid}:{u}-{w}", "gid": gid, "n": n, "gi": i, "u": u, "w": w, "dist": d,
                                   "F22": n <= 22, "family": "F26" if n <= 26 else "F28d5"})
        log(f"order {n}: {EXPECTED_COUNTS[n]} graphs, block table now {len(blocks)}")
    table = {"graphs": per_graph, "blocks": blocks}
    write_json(path, table)
    return table


_GRAPHS: dict = {}


def graph_of(n: int, i: int) -> graphs.Graph:
    if n not in _GRAPHS:
        _GRAPHS[n] = load_g6(source_file(n))
    return _GRAPHS[n][i]


def block_of(rec: dict) -> transfer.Block:
    return superedge_block(graph_of(rec["n"], rec["gi"]), rec["u"], rec["w"], rec["id"])


def block_job(rec: dict):
    mats = transfer.sector_matrices(block_of(rec))
    return transfer.pack(mats)


# A pool of workers that can be killed one by one (the 10 minute kill criterion of the hypothesis).

def _worker_loop(wid, func, tq, rq):
    while True:
        item = tq.get()
        if item is None:
            return
        key, arg = item
        rq.put(("start", wid, key, time.time()))
        t0 = time.time()
        try:
            res = func(arg)
            rq.put(("ok", wid, key, res, time.time() - t0))
        except BaseException as e:  # noqa: BLE001
            rq.put(("error", wid, key, repr(e), time.time() - t0))


def run_killable(tasks: list, func, workers: int, timeout_s: float, on_result, label: str) -> None:
    """Run func(arg) for every (key, arg) in tasks on separate processes. A task running longer than timeout_s is killed
    (only the process this function started, by handle) and reported as status "timeout"."""
    if not tasks:
        return
    ctx = mp.get_context("spawn")
    tq, rq = ctx.Queue(), ctx.Queue()
    for t in tasks:
        tq.put(t)
    nw = min(workers, len(tasks))
    for _ in range(nw):
        tq.put(None)
    procs: dict = {}
    current: dict = {}
    counter = [0]

    def spawn():
        wid = counter[0]
        counter[0] += 1
        p = ctx.Process(target=_worker_loop, args=(wid, func, tq, rq), daemon=True)
        p.start()
        procs[wid] = p

    for _ in range(nw):
        spawn()
    started, finished, t_begin = set(), 0, time.time()
    while finished < len(tasks):
        try:
            msg = rq.get(timeout=2)
        except queue.Empty:
            msg = None
        if msg is not None:
            kind, wid, key = msg[0], msg[1], msg[2]
            if kind == "start":
                current[wid] = (key, msg[3])
                started.add(key)
            else:
                if current.get(wid, (None,))[0] == key:
                    del current[wid]
                finished += 1
                on_result(key, kind, msg[3], msg[4])
                if finished % 100 == 0 or finished == len(tasks):
                    el = time.time() - t_begin
                    log(f"{label}: {finished}/{len(tasks)} done in {el:.0f} s (eta {el / finished * (len(tasks) - finished):.0f} s)")
        now = time.time()
        for wid, (key, t0) in list(current.items()):
            p = procs[wid]
            if now - t0 > timeout_s:
                p.terminate()
                p.join(10)
                del current[wid]
                finished += 1
                on_result(key, "timeout", None, now - t0)
                if len(started) < len(tasks):
                    spawn()
            elif p.exitcode is not None:
                del current[wid]
                finished += 1
                on_result(key, "error", f"worker exited with code {p.exitcode}", now - t0)
                if len(started) < len(tasks):
                    spawn()
    for p in procs.values():
        p.join(15)
        if p.is_alive():
            p.terminate()
            p.join(10)


def read_block_records() -> dict:
    path = DATA / "blocks.jsonl"
    out = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                out[r["id"]] = r
    return out


def cmd_blocks(args) -> int:
    table = build_block_table()
    blocks = table["blocks"]
    done = read_block_records()
    keep = {"ok", "timeout"} if not args.retry_timeouts else {"ok"}
    todo = [(b["id"], b) for b in blocks if not (b["id"] in done and done[b["id"]]["status"] in keep)]
    log(f"blocks: {len(blocks)} in F, {len(blocks) - len(todo)} already recorded, {len(todo)} to compute")
    os.environ["OPENBLAS_NUM_THREADS"] = "1"
    os.environ["OMP_NUM_THREADS"] = "1"
    DATA.mkdir(parents=True, exist_ok=True)
    out = open(DATA / "blocks.jsonl", "a", encoding="utf-8", newline="\n")
    meta = {b["id"]: b for b in blocks}

    def on_result(key, status, payload, seconds):
        rec = {"id": key, "status": status, "seconds": round(seconds, 2), "n": meta[key]["n"], "dist": meta[key]["dist"]}
        if status == "ok":
            rec["packed"] = base64.b64encode(payload).decode("ascii")
        elif status == "error":
            rec["error"] = payload
        out.write(json.dumps(rec) + "\n")
        out.flush()
        if status != "ok":
            log(f"block {key}: {status} after {seconds:.0f} s {payload if status == 'error' else ''}")

    try:
        run_killable(todo, block_job, min(args.workers, MAX_WORKERS), BLOCK_TIMEOUT_S, on_result, "blocks")
    finally:
        out.close()
    summarize_blocks(table)
    write_manifest()
    recs = read_block_records()
    bad = [k for k in meta if recs.get(k, {}).get("status") != "ok"]
    log(f"blocks done: {len(meta) - len(bad)} computed, {len(bad)} not computed")
    return 0


def summarize_blocks(table: dict) -> dict:
    recs = read_block_records()
    rows, secs_by_n = [], {}
    for b in table["blocks"]:
        r = recs.get(b["id"])
        if r is None:
            rows.append({"id": b["id"], "status": "missing"})
            continue
        row = {"id": b["id"], "n": b["n"], "dist": b["dist"], "status": r["status"], "seconds": r["seconds"]}
        if r["status"] == "ok":
            mats = transfer.unpack(base64.b64decode(r["packed"]))
            row["conducted"] = [o for o in SECTORS if mats[o].any()]
            row["ones"] = {o: int(mats[o].sum()) for o in SECTORS}
            secs_by_n.setdefault(b["n"], []).append(r["seconds"])
        rows.append(row)
    summary = {"blocks_in_F": len(rows), "computed": sum(r["status"] == "ok" for r in rows),
               "not_computed": [r["id"] for r in rows if r["status"] != "ok"],
               "seconds_by_order": {str(n): {"count": len(v), "mean": round(float(np.mean(v)), 2), "max": round(float(np.max(v)), 2)}
                                    for n, v in sorted(secs_by_n.items())},
               "conducted_sector_sets": dict(Counter(",".join(r["conducted"]) for r in rows if r["status"] == "ok")),
               "rows": rows}
    update_results("blocks", {k: v for k, v in summary.items() if k != "rows"})
    write_json(ARTIFACTS / "blocks.json", summary)
    return summary


def load_computed_blocks(table: dict, pred) -> list[tuple[dict, dict]]:
    """[(block record, sector matrices)] of the computed blocks of the table satisfying pred, in table order."""
    recs = read_block_records()
    out = []
    for b in table["blocks"]:
        if pred(b) and recs.get(b["id"], {}).get("status") == "ok":
            out.append((b, transfer.unpack(base64.b64decode(recs[b["id"]]["packed"]))))
    return out


def write_manifest() -> None:
    files = {}
    for p in sorted(DATA.glob("*")):
        if p.is_file():
            files[p.name] = {"bytes": p.stat().st_size, "sha256": sha256_file(p)}
    per_block = {}
    for k, r in read_block_records().items():
        if r["status"] == "ok":
            per_block[k] = hashlib.sha256(base64.b64decode(r["packed"])).hexdigest()
    write_json(ARTIFACTS / "data-manifest.json", {"data_root_role": "EXP-015 data root (E:/_Datos/caos-research/petersen-coloring/EXP-015 on the default device)",
                                                  "files": files, "packed_matrix_sha256_by_block": per_block})


# ----------------------------------------------------------------------------------------------------------------------
# Generators and the trace test
# ----------------------------------------------------------------------------------------------------------------------

def pack_transpose(raw: bytes) -> bytes:
    return transfer.pack(transfer.transpose(transfer.unpack(raw)))


def packed_pair_trace(pa: bytes, pb: bytes) -> bool:
    """trace(a b) != 0 in some sector, from the packed forms: some bit set in a AND b^T (uint64 words)."""
    bt = pack_transpose(pb)
    n = max(len(pa), len(bt))
    n += (-n) % 8
    wa = np.zeros(n, dtype=np.uint8)
    wb = np.zeros(n, dtype=np.uint8)
    wa[:len(pa)] = np.frombuffer(pa, dtype=np.uint8)
    wb[:len(bt)] = np.frombuffer(bt, dtype=np.uint8)
    return bool(np.any(wa.view(np.uint64) & wb.view(np.uint64)))


def _sector_offsets() -> dict[str, tuple[int, int]]:
    out, k = {}, 0
    for o in SECTORS:
        n = len(transfer.sector_states()[o])
        out[o] = (k, n)
        k += n * n
    return out


def _sector_rows(packed: np.ndarray, o: str, transposed: bool) -> np.ndarray:
    """float32 (N, n*n): the sector o of every packed generator, flattened (transposed when asked)."""
    off, n = _sector_offsets()[o]
    out = np.empty((packed.shape[0], n * n), dtype=np.float32)
    for s in range(0, packed.shape[0], 1024):
        bits = np.unpackbits(packed[s:s + 1024], axis=1)[:, off:off + n * n].reshape(-1, n, n)
        if transposed:
            bits = bits.transpose(0, 2, 1)
        out[s:s + bits.shape[0]] = bits.reshape(bits.shape[0], -1)
    return out


def bulk_pair_hits(packed: np.ndarray, chunk: int = 512) -> tuple[np.ndarray, dict]:
    """For every pair i <= j of the N packed generators, whether trace(g_i g_j) is nonzero in some sector.

    Returns hits (N, ceil(N/8)) uint8, bit j of row i (big-endian bit order of numpy.packbits) set when the pair has a
    nonzero diagonal (valid for j >= i), and the number of pairs j >= i with a nonzero diagonal per sector. The product
    is the integer inner product of g_i with the transpose of g_j (float32 holds the counts exactly)."""
    n_gen = packed.shape[0]
    hits = np.zeros((n_gen, (n_gen + 7) // 8), dtype=np.uint8)
    per_sector = {}
    for o in SECTORS:
        a = _sector_rows(packed, o, False)
        bt = _sector_rows(packed, o, True)
        cnt = 0
        for i0 in range(0, n_gen, chunk):
            i1 = min(i0 + chunk, n_gen)
            j0 = (i0 // 8) * 8
            blk = (a[i0:i1] @ bt[j0:].T) > 0.5
            mask = (j0 + np.arange(blk.shape[1]))[None, :] >= (i0 + np.arange(i1 - i0))[:, None]
            cnt += int((blk & mask).sum())
            pb = np.packbits(blk, axis=1)
            hits[i0:i1, j0 // 8:j0 // 8 + pb.shape[1]] |= pb
        per_sector[o] = cnt
        del a, bt
    return hits, per_sector


def zero_pairs(hits: np.ndarray, n_gen: int, chunk: int = 2048) -> list[tuple[int, int]]:
    out = []
    for i0 in range(0, n_gen, chunk):
        i1 = min(i0 + chunk, n_gen)
        bits = np.unpackbits(hits[i0:i1], axis=1)[:, :n_gen]
        zero = bits == 0
        zero &= (np.arange(n_gen)[None, :] >= (i0 + np.arange(i1 - i0))[:, None])
        for r, c in zip(*np.nonzero(zero)):
            out.append((i0 + int(r), int(c)))
    return out


def hit_bit(hits: np.ndarray, i: int, j: int) -> bool:
    if j < i:
        i, j = j, i
    return bool(hits[i, j // 8] >> (7 - j % 8) & 1)


class Generators:
    """Distinct generator matrices of a family, with every (block, orientation, junction) that realizes each."""

    def __init__(self, entries: list[tuple[dict, dict]]):
        self.entries = entries
        self.index: dict[bytes, int] = {}
        self.packed: list[bytes] = []
        self.prov: list[list[tuple[int, str, int]]] = []
        self.triples = 0
        for bi, (_, mats) in enumerate(entries):
            for orient, pi_index, g in block_generators(mats):
                self.triples += 1
                k = transfer.pack(g)
                if k not in self.index:
                    self.index[k] = len(self.packed)
                    self.packed.append(k)
                    self.prov.append([])
                self.prov[self.index[k]].append((bi, orient, pi_index))

    def array(self) -> np.ndarray:
        return np.array([np.frombuffer(p, dtype=np.uint8) for p in self.packed])

    def mats(self, i: int) -> dict[str, np.ndarray]:
        return transfer.unpack(self.packed[i])

    def word(self, i: int) -> list[dict]:
        return [{"block": self.entries[bi][0]["id"], "orient": o, "pi": list(PERMS[p])} for bi, o, p in self.prov[i]]


def sorted_orders_pairs(counts: Counter) -> dict[int, int]:
    """Unordered pairs of generator triples by ring order, from the number of triples per block order n (block has n - 2 vertices)."""
    out: Counter = Counter()
    keys = sorted(counts)
    for a, x in enumerate(keys):
        for y in keys[a:]:
            c = counts[x] * (counts[x] + 1) // 2 if x == y else counts[x] * counts[y]
            out[(x - 2) + (y - 2)] += c
    return dict(sorted(out.items()))


def cyclic_triples_by_order(counts: Counter) -> dict[int, int]:
    ordered: Counter = Counter()
    fixed: Counter = Counter()
    for x, cx in counts.items():
        fixed[3 * (x - 2)] += cx
        for y, cy in counts.items():
            for z, cz in counts.items():
                ordered[(x - 2) + (y - 2) + (z - 2)] += cx * cy * cz
    out = {}
    for s, c in ordered.items():
        assert (c + 2 * fixed.get(s, 0)) % 3 == 0
        out[s] = (c + 2 * fixed.get(s, 0)) // 3
    return dict(sorted(out.items()))


# ----------------------------------------------------------------------------------------------------------------------
# R1, R2
# ----------------------------------------------------------------------------------------------------------------------

def imul_diag(mats_a: dict, mats_b: dict) -> list[str]:
    """Independent recheck of a pair: integer matrix product, sectors with a nonzero diagonal."""
    return [o for o in SECTORS if bool(np.any(np.diagonal((mats_a[o].astype(np.int32) @ mats_b[o].astype(np.int32)) > 0)))]


def family_entries(table: dict, name: str):
    pred = {"F": lambda b: True, "F22": lambda b: b["F22"]}[name]
    return load_computed_blocks(table, pred)


def cmd_rings2(args) -> int:
    table = build_block_table()
    t0 = time.time()
    entries = family_entries(table, "F")
    n_in_table = len(table["blocks"])
    gens = Generators(entries)
    n = len(gens.packed)
    log(f"R1: {len(entries)} of {n_in_table} blocks computed, {gens.triples} generator triples, {n} distinct generators, {n * (n + 1) // 2} unordered pairs")
    arr = gens.array()
    hits, per_sector = bulk_pair_hits(arr, chunk=args.chunk)
    log(f"R1: bulk trace test done in {time.time() - t0:.0f} s")
    zeros = zero_pairs(hits, n)
    np.save(DATA / "hits-F.npy", hits)
    # recheck by the independent packed-bit path on a random sample and on every zero pair
    rng = random.Random(SEED)
    sample = [(rng.randrange(n), rng.randrange(n)) for _ in range(args.sample)]
    mism = sum(1 for i, j in sample if packed_pair_trace(gens.packed[i], gens.packed[j]) != hit_bit(hits, i, j))
    zero_rechecked = all(not packed_pair_trace(gens.packed[i], gens.packed[j]) and not imul_diag(gens.mats(i), gens.mats(j)) for i, j in zeros)
    # simplicity
    frames_of_block = {}
    for bi, (rec, _) in enumerate(entries):
        frames_of_block[bi] = double_ends(block_of(rec)) if rec["dist"] == 2 else None
    def frame(t):
        bi, o, p = t
        d = frames_of_block[bi]
        if d is None:
            return None
        return (d[0], d[1], PERMS[p]) if o == "f" else (d[1], d[0], PERMS[p])
    all_frames = [frame((bi, o, p)) for bi in range(len(entries)) for o in "fr" for p in range(6)]
    nonsimple_triple_pairs = count_nonsimple_pairs(all_frames)
    zero_rows, zero_simple = [], 0
    for i, j in zeros:
        real = [(t1, t2) for t1 in gens.prov[i] for t2 in gens.prov[j]]
        simple = [(t1, t2) for t1, t2 in real if ring2_is_simple(frame(t1), frame(t2))]
        zero_simple += bool(simple)
        zero_rows.append({"g1": i, "g2": j, "word_1": gens.word(i), "word_2": gens.word(j), "simple_realizations": len(simple),
                          "realizations": len(real)})
    counts_by_order = Counter(entries[bi][0]["n"] for bi in range(len(entries)) for _ in range(12))
    total_triple_pairs = gens.triples * (gens.triples + 1) // 2
    res = {"blocks_in_F": n_in_table, "blocks_computed": len(entries), "blocks_not_computed": n_in_table - len(entries),
           "generator_triples": gens.triples, "distinct_generators": n, "unordered_pairs_tested": n * (n + 1) // 2,
           "pairs_with_nonzero_diagonal_by_sector": per_sector, "pairs_with_zero_trace": len(zeros),
           "zero_trace_pairs_with_a_simple_realization": zero_simple,
           "zero_trace_pairs": zero_rows,
           "unordered_pairs_of_generator_triples": total_triple_pairs, "nonsimple_pairs_of_generator_triples": nonsimple_triple_pairs,
           "rings_of_two_by_order_over_triples": sorted_orders_pairs(counts_by_order),
           "packed_vs_bulk_sample": args.sample, "packed_vs_bulk_mismatches": mism, "zero_pairs_rechecked_independently": zero_rechecked,
           "seconds": round(time.time() - t0, 1)}
    res["R1_holds_for_computed_blocks"] = zero_simple == 0
    res["R1_complete"] = res["blocks_not_computed"] == 0
    update_results("R1", res)
    write_manifest()
    log(f"R1: zero-trace pairs {len(zeros)} (simple realization: {zero_simple}); non-simple pairs of triples {nonsimple_triple_pairs}; "
        f"mismatches {mism}; seconds {res['seconds']}")
    return 0


def cmd_rings3(args) -> int:
    table = build_block_table()
    t0 = time.time()
    entries = family_entries(table, "F22")
    n_in_table = sum(1 for b in table["blocks"] if b["F22"])
    gens = Generators(entries)
    n = len(gens.packed)
    mats = [gens.mats(i) for i in range(n)]
    log(f"R2: {len(entries)} of {n_in_table} blocks of F22, {n} distinct generators, {n ** 3} ordered triples")
    sizes = {o: len(transfer.sector_states()[o]) for o in SECTORS}
    cat = {o: np.concatenate([m[o].astype(np.float32) for m in mats], axis=1) for o in SECTORS}  # (n_o, N n_o)
    bt = {o: np.stack([m[o].T.astype(np.float32).ravel() for m in mats]) for o in SECTORS}  # (N, n_o^2)
    zeros = []
    for i in range(n):
        hit = np.zeros((n, n), dtype=bool)
        for o in SECTORS:
            s = sizes[o]
            prod = (mats[i][o].astype(np.float32) @ cat[o]).reshape(s, n, s).transpose(1, 0, 2) > 0.5  # g_i g_j, all j
            flat = prod.reshape(n, s * s).astype(np.float32)
            hit |= (flat @ bt[o].T) > 0.5
        for j, k in zip(*np.nonzero(~hit)):
            t = (i, int(j), int(k))
            rots = [t, (t[1], t[2], t[0]), (t[2], t[0], t[1])]
            if t == min(rots):
                zeros.append(t)
        if (i + 1) % 100 == 0:
            log(f"R2: row {i + 1}/{n}, zero cyclic triples so far {len(zeros)}")
    # recheck every zero triple through the library product
    rechecked = all(not transfer.colorable_sectors(transfer.product([mats[a], mats[b], mats[c]])) for a, b, c in zeros)
    # independent spot check of colorable triples: random ordered triples against the library
    rng = random.Random(SEED + 3)
    mism = 0
    for _ in range(args.sample):
        a, b, c = rng.randrange(n), rng.randrange(n), rng.randrange(n)
        lib = bool(transfer.colorable_sectors(transfer.product([mats[a], mats[b], mats[c]])))
        is_zero = (a, b, c) in set(zeros) or (b, c, a) in set(zeros) or (c, a, b) in set(zeros)
        if lib == is_zero:
            mism += 1
    counts_by_order = Counter(entries[bi][0]["n"] for bi in range(len(entries)) for _ in range(12))
    res = {"blocks_in_F22": n_in_table, "blocks_computed": len(entries), "blocks_not_computed": n_in_table - len(entries),
           "generator_triples": gens.triples, "distinct_generators": n, "ordered_triples_tested": n ** 3,
           "cyclic_triples_of_distinct_generators": (n ** 3 + 2 * n) // 3, "zero_trace_cyclic_triples": len(zeros),
           "zero_trace_triples": [{"g": list(t), "words": [gens.word(x) for x in t]} for t in zeros],
           "all_rings_of_three_are_simple": True, "zero_triples_rechecked_by_library_product": rechecked,
           "spot_check_sample": args.sample, "spot_check_mismatches": mism,
           "rings_of_three_by_order_over_triples": cyclic_triples_by_order(counts_by_order), "seconds": round(time.time() - t0, 1)}
    res["R2_holds_for_computed_blocks"] = len(zeros) == 0
    res["R2_complete"] = res["blocks_not_computed"] == 0
    update_results("R2", res)
    log(f"R2: zero-trace cyclic triples {len(zeros)}; mismatches {mism}; seconds {res['seconds']}")
    return 0


# ----------------------------------------------------------------------------------------------------------------------
# Solver checks on explicit graphs (R3 and the zero-trace procedure)
# ----------------------------------------------------------------------------------------------------------------------

def colorable_by_cadical(g: graphs.Graph) -> bool:
    """Petersen colorability of the explicit graph by CaDiCaL (python-sat), a SAT answer decoded and checked."""
    from pysat.solvers import Solver

    pl = poles.pole(g)
    f, y = poles.pole_formula(pl)
    with Solver(name="cadical153", bootstrap_with=f.clauses) as s:
        if not s.solve():
            return False
        pos = {lit for lit in s.get_model() if lit > 0}
        lab = {key: t for (key, t), var in y.items() if var in pos}
        if not poles.check_pole(pl, lab):
            raise AssertionError("model of the explicit formula failed the check")
        return True


def second_encoding(pl: poles.Pole):
    """Second encoding: one variable per (vertex, image vertex of P, bijection of its three items onto the image's star)."""
    from pysat.card import CardEnc, EncType
    from pysat.formula import IDPool

    stars = [sorted(s) for s in graphs.petersen().incidence()]
    pool = IDPool()
    clauses = []
    lab = lambda it, t: pool.id(("l", it, t))  # noqa: E731
    items = sorted({it for v in pl.kept for it in pl.items[v]})
    for it in items:
        clauses += CardEnc.equals([lab(it, t) for t in range(15)], 1, vpool=pool, encoding=EncType.pairwise).clauses
    for v in pl.kept:
        opts = []
        for x, star in enumerate(stars):
            for perm in PERMS:
                o = pool.id(("o", v, x, perm))
                opts.append(o)
                for it, pi in zip(pl.items[v], perm):
                    clauses.append([-o, lab(it, star[pi])])
        clauses.append(opts)
    return clauses, pool, lab


def second_encoding_matrices(block: transfer.Block) -> dict[str, np.ndarray]:
    """Sector matrices by the second encoding and MiniSat 2.2 (EXP-014 check_certificate.py, same encoding). `solve_limited`
    replaces `solve`: in python-sat 1.9.dev22 on Windows `Solver(name="minisat22").solve` raises an access violation after
    some UNSAT answers under assumptions, `solve_limited` does not."""
    from pysat.solvers import Solver

    clauses, pool, lab = second_encoding(block.pole)
    states = transfer.sector_states()
    out = {}
    with Solver(name="minisat22", bootstrap_with=clauses) as s:
        for o in SECTORS:
            st = states[o]
            idx = {t: i for i, t in enumerate(st)}
            m = np.zeros((len(st), len(st)), dtype=bool)
            for i, a in enumerate(st):
                assume = [lab(("d", block.left[k]), a[k]) for k in range(3)]
                sel = pool.id(("sel", o, i))
                while s.solve_limited(assumptions=assume + [sel]):
                    model = {lit for lit in s.get_model() if lit > 0}
                    b = tuple(next(t for t in range(15) if lab(("d", block.right[k]), t) in model) for k in range(3))
                    m[i, idx[b]] = True
                    s.add_clause([-sel] + [-lab(("d", block.right[k]), b[k]) for k in range(3)])
                s.add_clause([-sel])
            out[o] = m
    return out


def colorable_by_minisat(g: graphs.Graph, limit_s: float) -> bool | None:
    """Second solver, second encoding, on the explicit graph. None when the limit is reached."""
    import threading

    from pysat.solvers import Solver

    clauses, _, _ = second_encoding(poles.pole(g))
    with Solver(name="minisat22", bootstrap_with=clauses) as s:
        timer = threading.Timer(limit_s, s.interrupt)
        timer.start()
        try:
            r = s.solve_limited(expect_interrupt=True)
        finally:
            timer.cancel()
        return r


def _g1_job(rec: dict):
    blk = block_of(rec)
    t0 = time.time()
    first = transfer.sector_matrices(blk)
    t1 = time.time()
    second = second_encoding_matrices(blk)
    t2 = time.time()
    same = all(np.array_equal(first[o], second[o]) for o in SECTORS)
    return {"same": same, "cadical_seconds": round(t1 - t0, 1), "minisat_seconds": round(t2 - t1, 1),
            "ones": {o: int(first[o].sum()) for o in SECTORS}}


def gate_g1(table: dict, workers: int) -> dict:
    p = graph_of(10, 0)
    reps, _ = orbit_pairs(p)
    mats = transfer.sector_matrices(superedge_block(p, reps[0][0], reps[0][1], "P"))
    ones = {o: int(m.sum()) for o, m in mats.items()}
    p_ok = ones == {"0": 120, "E": 296, "D3": 0, "D2": 8, "T1": 0, "T2": 0}
    rng = random.Random(SEED)
    sample = rng.sample(table["blocks"], 30)
    rows = {}

    def on_result(key, status, payload, seconds):
        rows[key] = {"status": status, **(payload if status == "ok" else {"detail": str(payload)}), "wall_seconds": round(seconds, 1)}

    run_killable([(b["id"], b) for b in sample], _g1_job, workers, SECOND_ENCODING_TIMEOUT_S, on_result, "G1")
    equal = sum(1 for r in rows.values() if r["status"] == "ok" and r["same"])
    return {"P_block_entries": ones, "P_block_equals_EXP014_S": p_ok, "sampled_blocks": [b["id"] for b in sample],
            "second_encoding_equal": equal, "second_encoding_total": len(sample), "rows": rows,
            "passed": p_ok and equal == len(sample)}


def _exp014_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, EXP014 / filename)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _g52_job(arg):
    return _exp014_module("exp014_g52", "run_g52_control.py").job(arg)


def gate_g2(workers: int) -> dict:
    """R4: the G52 split of EXP-014 addendum 1, recomputed: a zero diagonal in all six sectors for all ten splits."""
    ctl = _exp014_module("exp014_g52", "run_g52_control.py")
    g = graphs.load_edgelist(ctl.G52)
    x = ctl.find_cut(g)
    xs = set(x)
    cut_edges = [i for i, (u, v) in enumerate(g.edges) if (u in xs) != (v in xs)]
    splits = [(c1, tuple(e for e in cut_edges if e not in c1)) for c1 in itertools.combinations(cut_edges, 3) if cut_edges[0] in c1]
    rows = {}

    def on_result(key, status, payload, seconds):
        rows[key] = payload if status == "ok" else {"split": key, "status": status, "detail": str(payload)}

    run_killable([(i, (i, x, c1, c2)) for i, (c1, c2) in enumerate(splits)], _g52_job, min(workers, len(splits)), 7200, on_result, "G2/R4")
    rows_l = [rows[i] for i in sorted(rows)]
    decided = all("ring_diagonal_sectors" in r for r in rows_l) and len(rows_l) == 10
    all_zero = decided and all(not r["ring_diagonal_sectors"] for r in rows_l)
    sides = decided and all(r["X_conducted"] and r["Y_conducted"] for r in rows_l)
    return {"graph": "G52", "cut_edges": cut_edges, "cut_edges_as_in_EXP014": cut_edges == G52_CUT_EDGES, "X_size": len(x),
            "splits": rows_l, "decided": decided, "all_ten_splits_zero_in_all_six_sectors": all_zero, "sides_colorable": sides,
            "passed": bool(all_zero and sides and cut_edges == G52_CUT_EDGES)}


def cmd_gates(args) -> int:
    t0 = time.time()
    table = build_block_table()
    g0 = gate_g0(min(args.workers, MAX_WORKERS))
    log(f"G0: {'PASS' if g0['passed'] else 'FAIL'} ({g0['graphs_checked']} graphs)")
    update_results("G0", g0)
    if not g0["passed"]:
        return 4
    g2 = gate_g2(min(args.workers, MAX_WORKERS))
    log(f"G2 (R4): {'PASS' if g2['passed'] else 'FAIL'}")
    update_results("G2", g2)
    update_results("R4", {"holds": g2["passed"], "decided": g2["decided"], "all_zero": g2["all_ten_splits_zero_in_all_six_sectors"]})
    g1 = gate_g1(table, min(args.workers, MAX_WORKERS))
    log(f"G1: {'PASS' if g1['passed'] else 'FAIL'} ({g1['second_encoding_equal']} of {g1['second_encoding_total']} blocks equal under the second encoding)")
    update_results("G1", g1)
    update_results("gates_seconds", round(time.time() - t0, 1))
    return 0 if (g0["passed"] and g1["passed"] and g2["passed"]) else 4


# ----------------------------------------------------------------------------------------------------------------------
# R3 and descriptive measurements
# ----------------------------------------------------------------------------------------------------------------------

def block_table_entries(table, pred):
    recs = read_block_records()
    return [b for b in table["blocks"] if pred(b) and recs.get(b["id"], {}).get("status") == "ok"]


def cmd_crosscheck(args) -> int:
    table = build_block_table()
    t0 = time.time()
    entries = family_entries(table, "F")
    gens = Generators(entries)
    hits = np.load(DATA / "hits-F.npy")
    f22 = [bi for bi, (rec, _) in enumerate(entries) if rec["F22"]]
    rng = random.Random(SEED)
    blocks_cache = {}

    def blk_of(bi):
        if bi not in blocks_cache:
            blocks_cache[bi] = block_of(entries[bi][0])
        return blocks_cache[bi]

    rows, skipped = [], 0
    plan = [2] * args.len2 + [3] * args.len3
    for length in plan:
        while True:
            pool_idx = list(range(len(entries))) if length == 2 else f22
            word = [(rng.choice(pool_idx), rng.choice("fr"), rng.randrange(6)) for _ in range(length)]
            blocks = [(blk_of(bi) if o == "f" else blk_of(bi).reversed(), PERMS[p]) for bi, o, p in word]
            try:
                ring = transfer.build_ring(blocks)
            except ValueError:
                skipped += 1
                continue
            break
        gmats = []
        for bi, o, p in word:
            m = entries[bi][1] if o == "f" else transfer.transpose(entries[bi][1])
            gmats.append(transfer.with_junction(m, PERMS[p]))
        lib = bool(transfer.colorable_sectors(transfer.product(gmats)))
        row = {"length": length, "order": ring.n, "word": [[entries[bi][0]["id"], o, list(PERMS[p])] for bi, o, p in word],
               "trace_nonzero_library": lib}
        if length == 2:
            ids = [gens.index[transfer.pack(g)] for g in gmats]
            row["trace_nonzero_packed"] = packed_pair_trace(gens.packed[ids[0]], gens.packed[ids[1]])
            row["trace_nonzero_bulk"] = hit_bit(hits, ids[0], ids[1])
        row["cadical_colorable"] = colorable_by_cadical(ring)
        row["agree"] = lib == row["cadical_colorable"] and (length == 3 or (row["trace_nonzero_packed"] == lib == row["trace_nonzero_bulk"]))
        rows.append(row)
        if len(rows) % 50 == 0:
            log(f"R3: {len(rows)} rings, agreements {sum(r['agree'] for r in rows)}")
    res = {"seed": SEED, "rings": len(rows), "length_2": args.len2, "length_3": args.len3, "nonsimple_draws_skipped": skipped,
           "agree": sum(r["agree"] for r in rows), "colorable": sum(r["cadical_colorable"] for r in rows),
           "noncolorable": sum(not r["cadical_colorable"] for r in rows), "rows": rows, "seconds": round(time.time() - t0, 1)}
    res["holds"] = res["agree"] == res["rings"]
    update_results("R3", res)
    log(f"R3: {res['agree']} of {res['rings']} agree; colorable {res['colorable']}")
    return 0


def _ring_measure_job(arg):
    edges, = arg
    g = graphs.Graph.from_edges(edges)
    return {"order": g.n, "girth": invariants.girth(g), "cyclic_edge_connectivity": cyclic_connectivity(g)}


def cmd_describe(args) -> int:
    table = build_block_table()
    t0 = time.time()
    entries = family_entries(table, "F")
    blocks_summary = read_results().get("blocks", {})
    rng = random.Random(SEED + 11)
    jobs, meta = [], []
    while len(jobs) < args.rings:
        b1, b2 = rng.randrange(len(entries)), rng.randrange(len(entries))
        w = [(b1, rng.choice("fr"), rng.randrange(6)), (b2, rng.choice("fr"), rng.randrange(6))]
        try:
            ring = transfer.build_ring([(block_of(entries[bi][0]) if o == "f" else block_of(entries[bi][0]).reversed(), PERMS[p]) for bi, o, p in w])
        except ValueError:
            continue
        jobs.append((list(ring.edges),))
        meta.append([[entries[bi][0]["id"], o, p] for bi, o, p in w])
    with mp.get_context("spawn").Pool(min(args.workers, MAX_WORKERS)) as pool:
        out = pool.map(_ring_measure_job, jobs, chunksize=1)
    girths = Counter(r["girth"] for r in out)
    cyc = Counter(r["cyclic_edge_connectivity"] for r in out)
    res = {"sample": len(out), "seed": SEED + 11, "girth_counts": {str(k): v for k, v in sorted(girths.items())},
           "cyclic_edge_connectivity_counts": {("at least 5" if k == 5 else str(k)): v for k, v in sorted(cyc.items())},
           "orders": {"min": min(r["order"] for r in out), "max": max(r["order"] for r in out)},
           "rows": [{"word": m, **r} for m, r in zip(meta, out)],
           "graphs": read_results().get("blocks_graph_orbits") or build_block_table()["graphs"],
           "conducted_sector_sets": blocks_summary.get("conducted_sector_sets"), "seconds": round(time.time() - t0, 1)}
    update_results("describe", res)
    log(f"describe: girth {res['girth_counts']}, cyclic edge connectivity {res['cyclic_edge_connectivity_counts']}")
    return 0


# ----------------------------------------------------------------------------------------------------------------------
# The zero-trace procedure
# ----------------------------------------------------------------------------------------------------------------------

def ensure_drat_trim() -> dict:
    import subprocess

    def wsl(cmd: str, timeout: int = 900):
        return subprocess.run(["wsl.exe", "-e", "bash", "-c", cmd], capture_output=True, text=True, timeout=timeout)

    home = wsl("echo $HOME").stdout.strip()
    path = f"{home}/drat-trim/drat-trim"
    if wsl(f"test -x {path} && echo yes").stdout.strip() != "yes":
        r = wsl(f"cd {home} && rm -rf drat-trim && git clone https://github.com/marijnheule/drat-trim && cd drat-trim && make", 1200)
        if wsl(f"test -x {path} && echo yes").stdout.strip() != "yes":
            raise RuntimeError(f"drat-trim build failed: {r.stderr[-400:]}")
    commit = wsl(f"cd {home}/drat-trim && git rev-parse HEAD").stdout.strip()
    solver.DRAT_TRIM = path
    return {"path": path, "commit": commit, "source": "https://github.com/marijnheule/drat-trim"}


def decide_noncolorable(g: graphs.Graph, stem: str, limit_s: int = 7200) -> dict:
    """Non-colorability by CaDiCaL (DRAT proof checked by drat-trim) and by MiniSat 2.2 on the second encoding;
    then the structure (simple, cubic, girth, exact cyclic edge connectivity, order)."""
    tool = ensure_drat_trim()
    pl = poles.pole(g)
    f, _ = poles.pole_formula(pl)
    cnf = DATA / "zero" / f"{stem}.cnf"
    cnf.parent.mkdir(parents=True, exist_ok=True)
    f.write(cnf, [f"EXP-015 {stem}"])
    rec = solver.solve(cnf, cnf.with_suffix(".drat"), limit_s)
    mini = colorable_by_minisat(g, limit_s)
    out = {"stem": stem, "order": g.n, "simple_cubic": g.is_cubic() and len(set(g.edges)) == len(g.edges), "girth": invariants.girth(g),
           "cyclic_edge_connectivity": cyclic_connectivity(g), "cadical_status": rec["status"],
           "drat_trim_verified": rec.get("drat_trim_verified"), "cnf_sha256": rec["cnf_sha256"], "proof_sha256": rec.get("proof_sha256"),
           "proof_bytes": rec.get("proof_bytes"), "second_solver_colorable": mini, "drat_trim": tool, "cadical_seconds": rec["seconds"]}
    out["confirmed_noncolorable"] = rec["status"] == "UNSAT" and bool(rec.get("drat_trim_verified")) and mini is False
    return out


def cmd_zero(args) -> int:
    res = read_results()
    rings = []
    r1 = res.get("R1", {})
    table = build_block_table()
    entries = family_entries(table, "F")
    for k, row in enumerate(r1.get("zero_trace_pairs", [])):
        if row["simple_realizations"] == 0:
            continue
        for t1 in row["word_1"]:
            for t2 in row["word_2"]:
                rings.append((f"r1-{k}", [t1, t2]))
    for k, row in enumerate(res.get("R2", {}).get("zero_trace_triples", [])):
        # rings of three are always simple; every realization is rebuilt
        for w in itertools.product(*row["words"]):
            rings.append((f"r2-{k}", list(w)))
    by_id = {rec["id"]: rec for rec, _ in entries}
    out = []
    for stem, word in rings:
        blocks = []
        for t in word:
            b = block_of(by_id[t["block"]])
            blocks.append((b if t["orient"] == "f" else b.reversed(), tuple(t["pi"])))
        try:
            g = transfer.build_ring(blocks)
        except ValueError:
            continue
        out.append({"ring": stem, "word": word, **decide_noncolorable(g, f"{stem}-{len(out)}")})
        log(f"zero {stem}: {out[-1]['confirmed_noncolorable']}")
    # self-test of the procedure on the known non-colorable graph G52
    g52 = graphs.load_edgelist(PROBLEM / "data" / "gjmmm-52.edgelist")
    selftest = decide_noncolorable(g52, "g52-selftest") if args.selftest else None
    update_results("zero", {"rings_checked": len(out), "rows": out, "selftest_on_G52": selftest})
    log(f"zero: {len(out)} zero-trace rings checked; G52 self-test {selftest and selftest['confirmed_noncolorable']}")
    return 0


# ----------------------------------------------------------------------------------------------------------------------

def cmd_all(args) -> int:
    for name, fn in (("gates", cmd_gates), ("blocks", cmd_blocks), ("rings2", cmd_rings2), ("rings3", cmd_rings3),
                     ("crosscheck", cmd_crosscheck), ("describe", cmd_describe), ("zero", cmd_zero)):
        log(f"== {name}")
        rc = fn(args)
        if rc:
            update_results("status", {"stopped_at": name, "exit_code": rc})
            return rc
    res = read_results()
    undecided = res["R1"]["blocks_not_computed"] + res["R2"]["blocks_not_computed"]
    status = {"R1": res["R1"]["R1_holds_for_computed_blocks"], "R2": res["R2"]["R2_holds_for_computed_blocks"], "R3": res["R3"]["holds"],
              "R4": res["R4"]["holds"], "blocks_not_computed": undecided, "decided": undecided == 0}
    update_results("status", status)
    log(f"all done: {status}")
    return 0 if undecided == 0 else 3


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["gates", "blocks", "rings2", "rings3", "crosscheck", "describe", "zero", "all"])
    ap.add_argument("--workers", type=int, default=MAX_WORKERS)
    ap.add_argument("--retry-timeouts", action="store_true")
    ap.add_argument("--chunk", type=int, default=512)
    ap.add_argument("--sample", type=int, default=200000)
    ap.add_argument("--len2", type=int, default=300)
    ap.add_argument("--len3", type=int, default=200)
    ap.add_argument("--rings", type=int, default=200)
    ap.add_argument("--selftest", action="store_true", default=True)
    args = ap.parse_args()
    if args.workers > MAX_WORKERS:
        raise SystemExit("at most 12 workers (hypothesis budget)")
    fn = {"gates": cmd_gates, "blocks": cmd_blocks, "rings2": cmd_rings2, "rings3": cmd_rings3, "crosscheck": cmd_crosscheck,
          "describe": cmd_describe, "zero": cmd_zero, "all": cmd_all}[args.cmd]
    sys.exit(fn(args))


if __name__ == "__main__":
    main()
