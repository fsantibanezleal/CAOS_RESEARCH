"""EXP-011: out-of-core depth-8 census pipeline. See hypothesis.md.

Stages:
  python pipeline.py --stage validate   (depth 5 -> 6 out-of-core; gates)
  python pipeline.py --stage build7     (depth 6 -> 7 shards + dedup)
  python pipeline.py --stage scan8      (multiprocess last-gate scan)

All arithmetic exact; states are sorted id-tuples packed as int32 rows.
Scratch: E:/_Temp/tau_depth8/ (deleted rows after use; disk guard).
"""

import argparse
import json
import os
import pickle
import shutil
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "code"))
from tclib.enum import integer_roots, padd, pmul, psub  # noqa: E402

T0 = time.time()
ART = HERE / "artifacts"
SCRATCH = Path("E:/_Temp/tau_depth8")
NPART = 256
EXPECTED6_STATES = 25_844_905
EXPECTED6_NEWPOLYS = 134_494
EXPECTED_STATES = {1: 9, 2: 98, 3: 1462, 4: 29506, 5: 778087}
DISK_GUARD_GB = 60


def log(msg):
    print(f"[{time.time() - T0:9.1f}s] {msg}", flush=True)


def checkpoint(name, payload):
    ART.mkdir(exist_ok=True)
    p = ART / "pipeline.json"
    data = json.loads(p.read_text("utf-8")) if p.exists() else {}
    data[name] = payload
    tmp = ART / "pipeline.json.tmp"
    tmp.write_text(json.dumps(data, indent=1, sort_keys=True), "utf-8")
    tmp.replace(p)


def disk_ok():
    return shutil.disk_usage("E:/").free / 2**30 > DISK_GUARD_GB


class Engine:
    def __init__(self):
        self.polys = [(-1,), (1,), (0, 1)]
        self.pid = {(-1,): 0, (1,): 1, (0, 1): 2}
        self.cache = {}
        self.ZERO = -1

    def intern(self, t):
        i = self.pid.get(t)
        if i is None:
            i = len(self.polys)
            self.polys.append(t)
            self.pid[t] = i
        return i

    def op(self, o, ia, ib):
        key = (o, ia, ib)
        r = self.cache.get(key)
        if r is not None:
            return r
        a, b = self.polys[ia], self.polys[ib]
        v = padd(a, b) if o == 0 else pmul(a, b) if o == 1 else psub(a, b)
        r = self.ZERO if not v else self.intern(v)
        if len(self.cache) < 60_000_000:
            self.cache[key] = r
        return r


def build_frontier_ram(eng, depth, first_seen):
    frontier = {()}
    for d in range(1, depth + 1):
        nf = set()
        for state in frontier:
            operands = (0, 1, 2) + state
            oset = set(operands)
            n = len(operands)
            for i in range(n):
                ia = operands[i]
                for j in range(i, n):
                    ib = operands[j]
                    for o in (0, 1):
                        r = eng.op(o, ia, ib)
                        if r != eng.ZERO and r not in oset:
                            nf.add(tuple(sorted(state + (r,))))
                            if r not in first_seen:
                                first_seen[r] = d
            for ia in operands:
                for ib in operands:
                    if ia != ib:
                        r = eng.op(2, ia, ib)
                        if r != eng.ZERO and r not in oset:
                            nf.add(tuple(sorted(state + (r,))))
                            if r not in first_seen:
                                first_seen[r] = d
        frontier = nf
        exp = EXPECTED_STATES.get(d)
        if exp is not None and len(frontier) != exp:
            raise SystemExit(f"GATE FAIL depth {d}: {len(frontier)}")
        log(f"  RAM frontier depth {d}: {len(frontier)}")
    return frontier


def expand_to_shards(eng, frontier, first_seen, next_depth, width, outdir):
    """Expand frontier one level; write successor rows hash-partitioned."""
    outdir.mkdir(parents=True, exist_ok=True)
    handles = [open(outdir / f"part{p:03d}.bin", "wb") for p in range(NPART)]
    bufs = [[] for _ in range(NPART)]
    BUF = 200_000
    rows = 0
    t_last = time.time()
    mult = np.random.default_rng(12345).integers(  # fixed seed: reproducible
        1, 2**31, size=width).astype(np.int64)

    def flush(p):
        if bufs[p]:
            arr = np.array(bufs[p], dtype=np.int32)
            handles[p].write(arr.tobytes())
            bufs[p].clear()

    for k, state in enumerate(frontier):
        operands = (0, 1, 2) + state
        oset = set(operands)
        n = len(operands)
        cand = set()
        for i in range(n):
            ia = operands[i]
            for j in range(i, n):
                ib = operands[j]
                for o in (0, 1):
                    r = eng.op(o, ia, ib)
                    if r != eng.ZERO and r not in oset:
                        cand.add(r)
        for ia in operands:
            for ib in operands:
                if ia != ib:
                    r = eng.op(2, ia, ib)
                    if r != eng.ZERO and r not in oset:
                        cand.add(r)
        for r in cand:
            if r not in first_seen:
                first_seen[r] = next_depth
            row = tuple(sorted(state + (r,)))
            h = int(sum(c * m for c, m in zip(row, mult)) & 0xFF)
            bufs[h].append(row)
            rows += 1
            if len(bufs[h]) >= BUF:
                flush(h)
        if (k + 1) % 500_000 == 0:
            log(f"  expanded {k+1}/{len(frontier)} states, {rows} rows")
            if not disk_ok():
                raise SystemExit("DISK GUARD tripped")
            checkpoint("expand_progress", {"states": k + 1, "rows": rows})
    for p in range(NPART):
        flush(p)
        handles[p].close()
    return rows


def dedup_partitions(outdir, width):
    total = 0
    for p in range(NPART):
        f = outdir / f"part{p:03d}.bin"
        raw = np.fromfile(f, dtype=np.int32)
        if raw.size == 0:
            uniq_count = 0
        else:
            arr = raw.reshape(-1, width)
            v = np.ascontiguousarray(arr).view(
                np.dtype((np.void, arr.dtype.itemsize * width)))
            uniq = np.unique(v)
            uniq_count = uniq.shape[0]
            uniq.view(np.int32).tofile(outdir / f"uniq{p:03d}.bin")
        f.unlink()
        total += uniq_count
        if p % 32 == 0:
            log(f"  dedup part {p}: cumulative {total}")
    return total


def stage_validate():
    eng = Engine()
    first_seen = {}
    frontier5 = build_frontier_ram(eng, 5, first_seen)
    outdir = SCRATCH / "validate6"
    if outdir.exists():
        shutil.rmtree(outdir)
    rows = expand_to_shards(eng, frontier5, first_seen, 6, 6, outdir)
    log(f"raw successor rows: {rows}")
    total = dedup_partitions(outdir, 6)
    new6 = sum(1 for d in first_seen.values() if d == 6)
    ok = (total == EXPECTED6_STATES and new6 == EXPECTED6_NEWPOLYS)
    log(f"VALIDATE: frontier6={total} (expect {EXPECTED6_STATES}), "
        f"new6={new6} (expect {EXPECTED6_NEWPOLYS}): "
        f"{'PASS' if ok else 'FAIL'}")
    checkpoint("validate", {"frontier6": total, "new6": new6,
                            "raw_rows": rows, "pass": ok,
                            "elapsed_s": round(time.time() - T0, 1)})
    shutil.rmtree(outdir, ignore_errors=True)
    return 0 if ok else 1


def stage_build7():
    eng = Engine()
    first_seen = {}
    frontier5 = build_frontier_ram(eng, 5, first_seen)
    log("rebuilding depth-6 frontier in RAM")
    frontier6 = set()
    for state in frontier5:
        operands = (0, 1, 2) + state
        oset = set(operands)
        n = len(operands)
        for i in range(n):
            ia = operands[i]
            for j in range(i, n):
                ib = operands[j]
                for o in (0, 1):
                    r = eng.op(o, ia, ib)
                    if r != eng.ZERO and r not in oset:
                        frontier6.add(tuple(sorted(state + (r,))))
                        if r not in first_seen:
                            first_seen[r] = 6
        for ia in operands:
            for ib in operands:
                if ia != ib:
                    r = eng.op(2, ia, ib)
                    if r != eng.ZERO and r not in oset:
                        frontier6.add(tuple(sorted(state + (r,))))
                        if r not in first_seen:
                            first_seen[r] = 6
    if len(frontier6) != EXPECTED6_STATES:
        raise SystemExit(f"GATE FAIL frontier6: {len(frontier6)}")
    log(f"frontier6 OK: {len(frontier6)}")
    outdir = SCRATCH / "frontier7"
    if outdir.exists():
        shutil.rmtree(outdir)
    rows = expand_to_shards(eng, frontier6, first_seen, 7, 7, outdir)
    log(f"raw successor rows: {rows}; dedup...")
    total = dedup_partitions(outdir, 7)
    new7 = sum(1 for d in first_seen.values() if d == 7)
    log(f"BUILD7: |frontier7| = {total}, new depth-7 polys = {new7}")
    with open(ART / "polys.pkl", "wb") as fh:
        pickle.dump({"polys": eng.polys,
                     "first_seen": first_seen}, fh)
    checkpoint("build7", {"frontier7": total, "new7": new7,
                          "raw_rows": rows,
                          "elapsed_s": round(time.time() - T0, 1)})
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True)
    args = ap.parse_args()
    if args.stage == "validate":
        return stage_validate()
    if args.stage == "build7":
        return stage_build7()
    raise SystemExit("scan8 is implemented in scan8.py (separate, "
                     "multiprocess)")


if __name__ == "__main__":
    sys.exit(main())
