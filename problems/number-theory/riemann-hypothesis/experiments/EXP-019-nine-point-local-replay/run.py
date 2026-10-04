"""CPU interval-cover runner; never equates partial progress with proof."""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor, wait, FIRST_COMPLETED
import json
import multiprocessing
from pathlib import Path
import struct
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[2]/"code"))
from local_replay import (aggregate, atomic_json, cutoff_cell_count, digest, load_tables,
                          pressure_audit, shard_worker, source_binding, spec_from_packet, table_chunk)


def stage_jobs(executor, function, tasks, label, directory):
    pending = {executor.submit(function, t) for t in tasks}
    total = len(pending)
    done = 0
    while pending:
        completed, pending = wait(pending, timeout=30, return_when=FIRST_COMPLETED)
        for future in completed:
            future.result()  # exceptions fail the parent; no success receipt
            done += 1
        print(f"{label}: completed={done}/{total} pending={len(pending)}", flush=True)
        atomic_json(directory/"progress.json", {"stage": label, "completed": done,
                                               "total": total, "time_unix": time.time()})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=24)
    parser.add_argument("--stage", choices=["audit", "tables", "full"], required=True)
    args = parser.parse_args()
    if not 1 <= args.workers <= 24:
        parser.error("worker count must be between 1 and 24")
    directory = args.output_dir.resolve()
    directory.mkdir(parents=True, exist_ok=True)
    audit = pressure_audit()
    atomic_json(directory/"pressure-audit.json", audit)
    print(f"pressure audit: {audit['checked_indices']} exact comparisons, passed", flush=True)
    if args.stage == "audit":
        return
    base = source_binding()
    table_dir = directory/"tables"
    table_dir.mkdir(exist_ok=True)
    spec = spec_from_packet()
    cells = cutoff_cell_count(spec)+spec.extra_cells
    chunk_size = 512
    chunks = [(start, min(start+chunk_size, cells), str(table_dir/"chunks"), base)
              for start in range(0, cells, chunk_size)]
    with ProcessPoolExecutor(max_workers=args.workers, mp_context=multiprocessing.get_context("spawn")) as pool:
        stage_jobs(pool, table_chunk, chunks, "tables", directory)
        tables = [[], []]
        for start, stop, _, _ in chunks:
            obj = json.loads((table_dir/"chunks"/f"chunk-{start:06d}-{stop:06d}.json").read_bytes())
            if any(len(v) != stop-start for v in obj["values"]):
                raise ValueError("chunk cell count mismatch")
            for index in range(2):
                tables[index].extend(float.fromhex(x) for x in obj["values"][index])
        hashes = {}
        for name, values in zip(["w.bin", "w-second.bin"], tables):
            raw = struct.pack(f">{len(values)}d", *values)
            (table_dir/name).write_bytes(raw)
            hashes[name] = digest(raw)
        atomic_json(table_dir/"tables.json", {"binding": base, "cells": cells, "hashes": hashes})
        load_tables(table_dir, base)
        print(f"tables bound: {hashes}", flush=True)
        if args.stage == "tables":
            return
        binding = {**base, "tables": hashes, "shard_count": 96,
                   "grid": 4000, "precision": 128, "target": "15211/2500000", "pressure": "1/2500"}
        atomic_json(directory/"run-binding.json", binding)
        stage_jobs(pool, shard_worker, [(s, 96, str(directory), binding) for s in range(96)],
                   "full-cover", directory)
    result = aggregate(directory, binding)
    atomic_json(directory/"full-cover.json", result)
    print(f"COMPLETE: all 96 shards verified, nodes={result['nodes']}", flush=True)


if __name__ == "__main__":
    main()
