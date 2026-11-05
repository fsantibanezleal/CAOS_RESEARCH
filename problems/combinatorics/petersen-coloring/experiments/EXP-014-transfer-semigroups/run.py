"""EXP-014: transfer semigroups of 6-poles (hypothesis.md).

    .venv/Scripts/python.exe .../run.py blocks [--workers 8]
    .venv/Scripts/python.exe .../run.py closure --family F1 [--cap 200000]
    .venv/Scripts/python.exe .../run.py crosscheck [--words 200]

`blocks` computes the six sector matrices of every block (artifacts/blocks.json for the summary,
HEAVY/blocks.npz for the matrices). `closure` closes the semigroup of a family, words of length at
least 2, and writes the certificate (HEAVY/certificate-<family>.npz) and artifacts/closure-<family>.json.
`crosscheck` decides random rings both ways (sector traces against an external solver on the graph).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import random
import sys
import time
from functools import lru_cache
from multiprocessing import Pool
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
PROBLEM = HERE.parents[1]
sys.path.insert(0, str(PROBLEM / "code"))

from pcclib import graphs, poles, solver, transfer  # noqa: E402

ARTIFACTS = HERE / "artifacts"
HEAVY = Path("E:/_Datos/caos-research/petersen-coloring/EXP-014")
SECTORS = transfer.SECTORS


def log(msg: str) -> None:
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def exp013():
    spec = importlib.util.spec_from_file_location("exp013", PROBLEM / "experiments" / "EXP-013-six-pole-charges" / "run.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def claw() -> transfer.Block:
    """Block 1 of J5: hub a_1 = 4 and leaves b_1, c_1, d_1 = 5, 6, 7; L toward block 0, R toward block 2."""
    g = graphs.flower_snark(5)
    keep = {4, 5, 6, 7}
    pl = poles.pole(g, removed_vertices=[v for v in range(g.n) if v not in keep])
    left, right = {}, {}
    for j, (x, ei) in enumerate(pl.dangling):
        other = g.other_end(ei, x)
        (left if other < 4 else right)[x] = j
    return transfer.Block("Y", pl, tuple(left[x] for x in (5, 6, 7)), tuple(right[x] for x in (5, 6, 7)))


def superedge() -> transfer.Block:
    p = graphs.petersen()
    adj = p.adjacency()
    u = 0
    w = min(x for x in range(p.n) if x != u and x not in adj[u] and set(adj[x]) & set(adj[u]))
    pl = poles.pole(p, removed_vertices=(u, w))
    uend = tuple(j for j, (x, ei) in enumerate(pl.dangling) if u in p.edges[ei])
    wend = tuple(j for j, (x, ei) in enumerate(pl.dangling) if w in p.edges[ei])
    return transfer.Block("S", pl, uend, wend)


@lru_cache(maxsize=1)
def all_blocks() -> list[transfer.Block]:
    m = exp013()
    out = [claw(), superedge()]
    plist, _ = m.poles_for(graphs.petersen(), "b")
    for name, pl, splits in plist:
        for si, (c1, c2) in enumerate(splits):
            out.append(transfer.Block(f"Pb:{name}|s{si}", pl, tuple(c1), tuple(c2)))
    for src, tag in (("J5", "Ja5"), ("J7", "Ja7"), ("Dodeca", "Da")):
        plist, _ = m.poles_for(m.load(src), "a")
        for name, pl, splits in plist:
            (c1, c2), = splits
            out.append(transfer.Block(f"{tag}:{name}", pl, tuple(c1), tuple(c2)))
    return out


FAMILIES = {
    "F1": lambda b: b.name == "Y",
    "F2": lambda b: b.name == "S",
    "F3": lambda b: b.name in ("Y", "S"),
    "F4": lambda b: b.name.startswith("Pb:"),
    "F5": lambda b: True,
}


def _block_job(i: int):
    blk = all_blocks()[i]
    t0 = time.time()
    mats = transfer.sector_matrices(blk)
    return i, transfer.pack(mats), time.time() - t0


def cmd_blocks(args) -> None:
    blocks = all_blocks()
    log(f"{len(blocks)} blocks")
    with Pool(args.workers) as pool:
        res = sorted(pool.map(_block_job, range(len(blocks)), chunksize=1))
    HEAVY.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(HEAVY / "blocks.npz", names=np.array([b.name for b in blocks]),
                        packed=np.array([np.frombuffer(r[1], dtype=np.uint8) for r in res]))
    summary = []
    for (i, raw, sec), blk in zip(res, blocks):
        mats = transfer.unpack(raw)
        summary.append({"block": blk.name, "vertices": len(blk.pole.kept), "seconds": round(sec, 2),
                        "ones": {o: int(mats[o].sum()) for o in SECTORS},
                        "conducted": [o for o in SECTORS if mats[o].any()],
                        "self_ring_sectors": transfer.colorable_sectors(mats)})
    ARTIFACTS.mkdir(exist_ok=True)
    (ARTIFACTS / "blocks.json").write_text(json.dumps({"sector_sizes": {o: len(transfer.sector_states()[o]) for o in SECTORS},
                                                       "blocks": summary}, indent=1) + "\n", encoding="utf-8", newline="\n")
    log(f"blocks done; slowest {max(r[2] for r in res):.1f} s")


def load_blocks() -> tuple[list[transfer.Block], list[dict]]:
    blocks = all_blocks()
    z = np.load(HEAVY / "blocks.npz")
    assert list(z["names"]) == [b.name for b in blocks]
    return blocks, [transfer.unpack(row.tobytes()) for row in z["packed"]]


def generators(blocks, mats, family: str):
    gens, keys = [], {}
    for blk, m in zip(blocks, mats):
        if not FAMILIES[family](blk):
            continue
        for orient, mm in (("f", m), ("r", transfer.transpose(m))):
            for pi in transfer.PERMS:
                g = transfer.with_junction(mm, pi)
                k = transfer.pack(g)
                if k not in keys:
                    keys[k] = len(gens)
                    gens.append({"block": blk.name, "orient": orient, "pi": pi, "mats": g})
    return gens


class Closure:
    """Exact closure of {products of at least two generators} under right multiplication."""

    def __init__(self, gens):
        self.gens = gens
        self.sizes = [len(transfer.sector_states()[o]) for o in SECTORS]
        self.cat = {o: np.concatenate([g["mats"][o].astype(np.float32) for g in gens], axis=1) for o in SECTORS}
        self.ids: dict[bytes, int] = {}
        self.rows: list[bytes] = []
        self.parent: list[tuple[int, int]] = []
        self.length: list[int] = []
        self.zero: list[int] = []

    def right_products(self, mats):
        """All products mats * g, packed, and whether each has a nonzero diagonal."""
        k = len(self.gens)
        flat, diag = [], np.zeros(k, dtype=bool)
        for o, n in zip(SECTORS, self.sizes):
            prod = (mats[o].astype(np.float32) @ self.cat[o]).reshape(n, k, n).transpose(1, 0, 2) > 0.5
            diag |= np.any(np.diagonal(prod, axis1=1, axis2=2), axis=1)
            flat.append(prod.reshape(k, n * n))
        packed = np.packbits(np.concatenate(flat, axis=1), axis=1)
        return packed, diag

    def add(self, raw: bytes, parent: tuple[int, int], length: int, nonzero: bool):
        if raw in self.ids:
            return None
        i = len(self.rows)
        self.ids[raw] = i
        self.rows.append(raw)
        self.parent.append(parent)
        self.length.append(length)
        if not nonzero:
            self.zero.append(i)
        return i

    def run(self, cap: int) -> bool:
        queue = []
        for gi, g in enumerate(self.gens):
            packed, diag = self.right_products(g["mats"])
            for hj in range(len(self.gens)):
                i = self.add(packed[hj].tobytes(), (-1 - gi, hj), 2, bool(diag[hj]))
                if i is not None:
                    queue.append(i)
        head = 0
        while head < len(queue):
            if len(self.rows) > cap:
                return False
            x = queue[head]
            head += 1
            packed, diag = self.right_products(transfer.unpack(self.rows[x]))
            for hj in range(len(self.gens)):
                i = self.add(packed[hj].tobytes(), (x, hj), self.length[x] + 1, bool(diag[hj]))
                if i is not None:
                    queue.append(i)
            if head % 2000 == 0:
                log(f"  expanded {head}, stored {len(self.rows)}, queue {len(queue) - head}, longest word {max(self.length)}")
        return True

    def word(self, i: int) -> list[int]:
        out = []
        while True:
            p, g = self.parent[i]
            out.append(g)
            if p < 0:
                out.append(-1 - p)
                return out[::-1]
            i = p


class AntichainClosure(Closure):
    """The closure kept as an antichain under inclusion (hypothesis.md, "Soundness and certificate").

    A product containing an active element is dropped; a new element retires every active element
    that contains it (retired elements are not expanded: their products contain the new element's).
    At the end every product of at least two generators contains an active element, and every
    active element times every generator does too."""

    WORDS = 269  # 17,197 bits padded to 269 64-bit words

    def __init__(self, gens, cap: int):
        super().__init__(gens)
        self.cap = cap
        self.bits = np.zeros((cap + 1, self.WORDS), dtype=np.uint64)
        self.active = np.zeros(cap + 1, dtype=bool)
        self.retired = 0

    @classmethod
    def words(cls, packed: np.ndarray) -> np.ndarray:
        pad = np.zeros((packed.shape[0], cls.WORDS * 8), dtype=np.uint8)
        pad[:, :packed.shape[1]] = packed
        return pad.view(np.uint64)

    def offer(self, packed: np.ndarray, diag: np.ndarray, parents: list[tuple[int, int]], length: int) -> list[int]:
        packed, idx = np.unique(packed, axis=0, return_index=True)
        diag = diag[idx]
        parents = [parents[i] for i in idx]
        w = self.words(packed)
        n = len(self.rows)
        act = np.flatnonzero(self.active[:n])
        keep = np.ones(w.shape[0], dtype=bool)
        if act.size:
            abits = self.bits[act]
            step = max(1, int(1e7 // (act.size * self.WORDS)))
            for s in range(0, w.shape[0], step):
                x = w[s:s + step]
                keep[s:s + step] = ~np.any(np.all((abits[None, :, :] & ~x[:, None, :]) == 0, axis=2), axis=1)
        cand = np.flatnonzero(keep)
        pc = np.unpackbits(packed[cand], axis=1).sum(axis=1)
        cand = cand[np.argsort(pc, kind="stable")]
        new = []
        for k in cand:
            x = w[k]
            if new and np.any(np.all((self.bits[new] & ~x) == 0, axis=1)):
                continue
            raw = packed[k].tobytes()
            if raw in self.ids:
                continue
            if act.size:
                sup = act[np.all((x & ~self.bits[act]) == 0, axis=1)]
                if sup.size:
                    self.active[sup] = False
                    self.retired += int(sup.size)
                    act = np.setdiff1d(act, sup, assume_unique=True)
            i = self.add(raw, parents[k], length, bool(diag[k]))
            self.bits[i] = x
            self.active[i] = True
            new.append(i)
        return new

    def run(self, cap: int) -> bool:
        queue = []
        for gi, g in enumerate(self.gens):
            packed, diag = self.right_products(g["mats"])
            queue += self.offer(packed, diag, [(-1 - gi, hj) for hj in range(len(self.gens))], 2)
            if len(self.rows) >= cap - len(self.gens):
                return False
        head = 0
        while head < len(queue):
            x = queue[head]
            head += 1
            if not self.active[x]:
                continue
            packed, diag = self.right_products(transfer.unpack(self.rows[x]))
            queue += self.offer(packed, diag, [(x, hj) for hj in range(len(self.gens))], self.length[x] + 1)
            if len(self.rows) >= cap - len(self.gens):
                return False
            if head % 200 == 0:
                log(f"  expanded {head}, stored {len(self.rows)}, active {int(self.active[:len(self.rows)].sum())}, "
                    f"queue {len(queue) - head}, longest word {max(self.length)}")
        return True


def cmd_closure(args) -> None:
    blocks, mats = load_blocks()
    gens = generators(blocks, mats, args.family)
    log(f"family {args.family}: {len(gens)} distinct generators")
    if args.antichain:
        return cmd_antichain(args, gens)
    t0 = time.time()
    cl = Closure(gens)
    reached = cl.run(args.cap)
    sec = time.time() - t0
    log(f"family {args.family}: closure {'reached' if reached else 'STOPPED AT CAP'} with {len(cl.rows)} elements, "
        f"longest word {max(cl.length)}, zero-trace elements {len(cl.zero)}, {sec:.0f} s")
    sector_counts = {o: 0 for o in SECTORS}
    for raw in cl.rows:
        for o in transfer.colorable_sectors(transfer.unpack(raw)):
            sector_counts[o] += 1
    zero_words = []
    for i in cl.zero[:50]:
        w = cl.word(i)
        zero_words.append([{"block": gens[g]["block"], "orient": gens[g]["orient"], "pi": list(gens[g]["pi"])} for g in w])
    HEAVY.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(HEAVY / f"certificate-{args.family}.npz",
                        generators=np.array([np.frombuffer(transfer.pack(g["mats"]), dtype=np.uint8) for g in gens]),
                        elements=np.array([np.frombuffer(r, dtype=np.uint8) for r in cl.rows]))
    out = {"family": args.family, "generators": [{"block": g["block"], "orient": g["orient"], "pi": list(g["pi"])} for g in gens],
           "closure_reached": reached, "cap": args.cap, "elements": len(cl.rows), "longest_word": max(cl.length),
           "zero_trace_elements": len(cl.zero), "zero_trace_words": zero_words,
           "elements_with_sector_diagonal": sector_counts, "seconds": round(sec, 1)}
    ARTIFACTS.mkdir(exist_ok=True)
    (ARTIFACTS / f"closure-{args.family}.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8", newline="\n")


def cmd_antichain(args, gens) -> None:
    t0 = time.time()
    cl = AntichainClosure(gens, args.cap)
    reached = cl.run(args.cap)
    sec = time.time() - t0
    n = len(cl.rows)
    active = np.flatnonzero(cl.active[:n])
    log(f"family {args.family} (antichain): closure {'reached' if reached else 'STOPPED AT CAP'}; stored {n}, active {active.size}, "
        f"retired {cl.retired}, longest word {max(cl.length)}, zero-trace elements {len(cl.zero)}, {sec:.0f} s")
    zero_words = []
    for i in cl.zero[:50]:
        zero_words.append([{"block": gens[g]["block"], "orient": gens[g]["orient"], "pi": list(gens[g]["pi"])} for g in cl.word(i)])
    sector_counts = {o: 0 for o in SECTORS}
    for i in active:
        for o in transfer.colorable_sectors(transfer.unpack(cl.rows[i])):
            sector_counts[o] += 1
    HEAVY.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(HEAVY / f"certificate-{args.family}-antichain.npz",
                        generators=np.array([np.frombuffer(transfer.pack(g["mats"]), dtype=np.uint8) for g in gens]),
                        elements=np.array([np.frombuffer(cl.rows[i], dtype=np.uint8) for i in active]))
    out = {"family": args.family, "mode": "antichain", "generators": len(gens), "closure_reached": reached, "cap": args.cap,
           "stored": n, "active": int(active.size), "retired": cl.retired, "longest_word": max(cl.length),
           "zero_trace_elements": len(cl.zero), "zero_trace_words": zero_words,
           "active_with_sector_diagonal": sector_counts, "seconds": round(sec, 1)}
    (ARTIFACTS / f"closure-{args.family}-antichain.json").write_text(json.dumps(out, indent=1) + "\n", encoding="utf-8", newline="\n")


def ring_cnf_status(g: graphs.Graph, stem: str) -> dict:
    pl = poles.pole(g)
    f, _ = poles.pole_formula(pl)
    cnf = HEAVY / "crosscheck" / f"{stem}.cnf"
    cnf.parent.mkdir(parents=True, exist_ok=True)
    f.write(cnf, [f"EXP-014 {stem}"])
    return solver.solve(cnf, cnf.with_suffix(".drat"), 600)


def cmd_crosscheck(args) -> None:
    blocks, mats = load_blocks()
    rng = random.Random(20261006)
    rows, attempts = [], 0
    for k in (5, 7, 9):
        y = [b for b in blocks if b.name == "Y"][0]
        word = [(y, (0, 1, 2))] * (k - 1) + [(y, (0, 2, 1))]
        g = transfer.build_ring(word)
        import networkx as nx
        iso = nx.is_isomorphic(nx.Graph(list(g.edges)), nx.Graph(list(graphs.flower_snark(k).edges)))
        tr = transfer.colorable_sectors(transfer.product([transfer.with_junction(mats[blocks.index(y)], pi) for _, pi in word]))
        rec = ring_cnf_status(g, f"J{k}")
        rows.append({"word": f"J{k}", "isomorphic_to_flower_snark": iso, "trace_sectors": tr, "solver": rec["status"],
                     "verified": rec.get("drat_trim_verified"), "agree": (rec["status"] == "SAT") == bool(tr)})
        log(f"J{k}: iso {iso}, trace sectors {tr}, solver {rec['status']}")
    while len(rows) < args.words + 3:
        attempts += 1
        t = rng.randint(2, 6)
        word = []
        for _ in range(t):
            bi = rng.randrange(len(blocks))
            blk = blocks[bi] if rng.random() < 0.5 else blocks[bi].reversed()
            word.append((bi, blk, rng.choice(transfer.PERMS)))
        try:
            g = transfer.build_ring([(blk, pi) for _, blk, pi in word])
        except ValueError:
            continue
        elems = []
        for bi, blk, pi in word:
            m = mats[bi] if not blk.name.endswith("^r") else transfer.transpose(mats[bi])
            elems.append(transfer.with_junction(m, pi))
        tr = transfer.colorable_sectors(transfer.product(elems))
        stem = f"w{len(rows):03d}"
        rec = ring_cnf_status(g, stem)
        ok = (rec["status"] == "SAT") == bool(tr) and rec["status"] in ("SAT", "UNSAT")
        rows.append({"word": [[blk.name, list(pi)] for _, blk, pi in word], "order": g.n, "trace_sectors": tr,
                     "solver": rec["status"], "verified": rec.get("drat_trim_verified"), "agree": ok})
        if not ok:
            log(f"DISAGREEMENT {stem}: trace {tr}, solver {rec['status']}")
    ARTIFACTS.mkdir(exist_ok=True)
    (ARTIFACTS / "crosscheck.json").write_text(json.dumps({"attempts": attempts, "rows": rows,
                                                          "agree": sum(r["agree"] for r in rows), "total": len(rows)}, indent=1) + "\n",
                                               encoding="utf-8", newline="\n")
    log(f"crosscheck: {sum(r['agree'] for r in rows)} of {len(rows)} agree ({attempts} random words drawn)")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("blocks")
    b.add_argument("--workers", type=int, default=8)
    c = sub.add_parser("closure")
    c.add_argument("--family", required=True, choices=sorted(FAMILIES))
    c.add_argument("--cap", type=int, default=200000)
    c.add_argument("--antichain", action="store_true")
    x = sub.add_parser("crosscheck")
    x.add_argument("--words", type=int, default=200)
    args = ap.parse_args()
    {"blocks": cmd_blocks, "closure": cmd_closure, "crosscheck": cmd_crosscheck}[args.cmd](args)


if __name__ == "__main__":
    main()
