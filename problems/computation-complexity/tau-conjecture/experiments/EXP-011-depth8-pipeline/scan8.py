"""EXP-011 stage scan8: multiprocess last-gate scan over a stored frontier.

Usage:
  python scan8.py --smoke     (build depth-6 frontier in RAM, write it in
                               the binary format, scan it with the pool:
                               MUST return z_max = 5 and zero z>=6
                               witnesses, matching EXP-004)
  python scan8.py             (scan SCRATCH/frontier7 -> exact z_max(8))

Resumable: per-partition result JSONs in artifacts/scan8_parts/; finished
partitions are skipped on relaunch. Histogram is per op-application (WITH
multiplicity); distinct-poly counting at depth 8 is out of scope (see the
hypothesis amendment). z_max and witness collection are exact.
"""

import argparse
import json
import os
import pickle
import sys
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "code"))

T0 = time.time()
ART = HERE / "artifacts"
SCRATCH = Path("E:/_Temp/tau_depth8")
ZMAX_PREV = {7: 5, 8: 6}  # z_max at the frontier's own depth (known)


def log(msg):
    print(f"[{time.time() - T0:9.1f}s] {msg}", flush=True)


def worker(task):
    """Scan one partition file. Returns (part, states, hist, witnesses)."""
    part, frontier_dir, polys_path, width, zrecord_threshold, ns = task
    sys.path.insert(0, str(Path(polys_path).parent.parent.parent / "code"))
    from tclib.enum import integer_roots, padd, pmul, psub
    with open(polys_path, "rb") as fh:
        data = pickle.load(fh)
    polys = data["polys"]
    f = Path(frontier_dir) / f"uniq{part:03d}.bin"
    out = ART / f"scan8_parts_{ns}" / f"part{part:03d}.json"
    if out.exists():
        return None
    if not f.exists():
        res = {"part": part, "states": 0, "hist": {}, "witnesses": []}
    else:
        arr = np.fromfile(f, dtype=np.int32).reshape(-1, width)
        opcache = {}
        rootmemo = {}
        hist = {}
        witnesses = []

        def zcount(t):
            z = rootmemo.get(t)
            if z is None:
                z = len(integer_roots(t))
                if len(rootmemo) < 2_000_000:
                    rootmemo[t] = z
            return z

        fns = (padd, pmul, psub)
        for row in arr:
            state = tuple(int(x) for x in row)
            operands = (0, 1, 2) + state
            opolys = [polys[i] for i in operands]
            n = len(operands)
            for i in range(n):
                for j in range(n):
                    for o in (0, 1, 2):
                        if o != 2 and j < i:
                            continue
                        if o == 2 and i == j:
                            continue
                        key = (o, operands[i], operands[j])
                        t = opcache.get(key)
                        if t is None:
                            t = fns[o](opolys[i], opolys[j])
                            if len(opcache) < 4_000_000:
                                opcache[key] = t
                        if not t:
                            continue
                        z = zcount(t)
                        hist[z] = hist.get(z, 0) + 1
                        if z >= zrecord_threshold:
                            witnesses.append({
                                "state": [int(x) for x in row],
                                "op": "+*-"[o],
                                "a": operands[i], "b": operands[j],
                                "poly": list(t),
                            })
        res = {"part": part, "states": int(arr.shape[0]),
               "hist": {str(k): v for k, v in hist.items()},
               "witnesses": witnesses[:100]}
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".tmp")
    tmp.write_text(json.dumps(res), "utf-8")
    tmp.replace(out)
    return part


def run_scan(frontier_dir, polys_path, width, zrecord_threshold, nproc, ns):
    parts = list(range(256))
    tasks = [(p, str(frontier_dir), str(polys_path), width,
              zrecord_threshold, ns) for p in parts]
    done = 0
    with Pool(processes=nproc) as pool:
        for r in pool.imap_unordered(worker, tasks):
            done += 1
            if done % 16 == 0:
                log(f"  partitions done: {done}/256")
    # merge
    hist = {}
    witnesses = []
    states = 0
    for p in parts:
        f = ART / f"scan8_parts_{ns}" / f"part{p:03d}.json"
        d = json.loads(f.read_text("utf-8"))
        states += d["states"]
        for k, v in d["hist"].items():
            hist[k] = hist.get(k, 0) + v
        witnesses.extend(d["witnesses"])
    zmax = max((int(k) for k, v in hist.items() if v > 0), default=0)
    return states, hist, witnesses, zmax


def write_frontier_from_ram(frontier, width, outdir):
    outdir.mkdir(parents=True, exist_ok=True)
    mult = np.random.default_rng(12345).integers(
        1, 2**31, size=width).astype(np.int64)
    bufs = [[] for _ in range(256)]
    for state in frontier:
        h = int(sum(c * m for c, m in zip(state, mult)) & 0xFF)
        bufs[h].append(state)
    for p in range(256):
        arr = (np.array(bufs[p], dtype=np.int32)
               if bufs[p] else np.empty((0, width), dtype=np.int32))
        arr.tofile(outdir / f"uniq{p:03d}.bin")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--nproc", type=int, default=20)
    args = ap.parse_args()

    if args.smoke:
        from pipeline import Engine, build_frontier_ram
        eng = Engine()
        first_seen = {}
        f5 = build_frontier_ram(eng, 5, first_seen)
        log("expanding to depth-6 frontier in RAM (gate-checked)")
        f6 = set()
        for state in f5:
            operands = (0, 1, 2) + state
            oset = set(operands)
            n = len(operands)
            for i in range(n):
                for j in range(i, n):
                    for o in (0, 1):
                        r = eng.op(o, operands[i], operands[j])
                        if r != eng.ZERO and r not in oset:
                            f6.add(tuple(sorted(state + (r,))))
            for ia in operands:
                for ib in operands:
                    if ia != ib:
                        r = eng.op(2, ia, ib)
                        if r != eng.ZERO and r not in oset:
                            f6.add(tuple(sorted(state + (r,))))
        assert len(f6) == 25_844_905, len(f6)
        outdir = SCRATCH / "smoke_frontier6"
        log(f"writing smoke frontier ({len(f6)} states)")
        write_frontier_from_ram(f6, 6, outdir)
        polys_path = ART / "polys_smoke.pkl"
        with open(polys_path, "wb") as fh:
            pickle.dump({"polys": eng.polys, "first_seen": first_seen}, fh)
        # clear any prior part results for the smoke namespace
        import shutil
        shutil.rmtree(ART / "scan8_parts_smoke", ignore_errors=True)
        states, hist, wits, zmax = run_scan(outdir, polys_path, 6, 6,
                                            args.nproc, "smoke")
        ok = (states == 25_844_905 and zmax == ZMAX_PREV[7]
              and not wits)
        log(f"SMOKE: states={states} zmax={zmax} z>=6 wits={len(wits)}: "
            f"{'PASS' if ok else 'FAIL'}")
        (ART / "scan8_smoke.json").write_text(json.dumps(
            {"states": states, "hist": hist, "zmax": zmax,
             "witnesses": len(wits), "pass": ok}), "utf-8")
        shutil.rmtree(outdir, ignore_errors=True)
        return 0 if ok else 1

    polys_path = ART / "polys.pkl"
    states, hist, wits, zmax = run_scan(SCRATCH / "frontier7", polys_path,
                                        7, 7, args.nproc, "final")
    log(f"SCAN8: states={states} zmax(8)={zmax} z>=7 wits={len(wits)}")
    (ART / "scan8_final.json").write_text(json.dumps(
        {"states": states, "hist": hist, "zmax": zmax,
         "witnesses": wits[:100]}), "utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
