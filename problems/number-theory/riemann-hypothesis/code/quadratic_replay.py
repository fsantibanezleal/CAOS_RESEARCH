"""EXP-020 stronger target, with separately bound quadratic pruning code."""

from dataclasses import replace
from fractions import Fraction
import json
import math
from pathlib import Path
import struct
import time

from flint import fmpq

from local_replay import (CODE, PACKET_SHA, atomic_json, digest, encoded,
                          source_binding, spec_from_packet, validate_state)
from rh019_vendor.quadratic_general import cutoff_cell_count, verify_general
from rh019_vendor.kernel import build_w_lower_table, build_w_second_lower_table

TARGET = fmpq(3051, 500000)


def spec():
    return replace(spec_from_packet(), target=TARGET)


def binding():
    base = source_binding()
    additions = [CODE/"certified_quadratic.py", CODE/"quadratic_replay.py",
                 CODE/"rh019_vendor/quadratic_general.py",
                 CODE.parent/"experiments/EXP-020-quadratic-local-certificate/run.py"]
    return {"baseline_source": base, "packet_sha256": PACKET_SHA,
            "target": str(TARGET), "pressure": "1/2500", "grid": 4000, "precision": 128,
            "code": {str(p.relative_to(CODE.parent)): digest(p.read_bytes()) for p in additions}}


def prepare(directory, baseline_dir):
    directory = Path(directory)
    current = spec()
    cutoff = cutoff_cell_count(current)
    p = math.nextafter(float(Fraction(1, 2500)), -math.inf)
    for n in range(cutoff):
        if Fraction(math.nextafter(p*n/4000, -math.inf)) > Fraction(n, 10000000):
            raise ValueError("unsafe extended pressure index")
    atomic_json(directory/"pressure-audit.json", {"passed": True, "indices": cutoff,
                                                "target": str(TARGET), "binding": binding()})
    baseline_dir = Path(baseline_dir)
    baseline_meta = json.loads((baseline_dir/"tables/tables.json").read_bytes())
    if baseline_meta["binding"] != source_binding():
        raise ValueError("baseline table source mismatch")
    table_dir = directory/"tables"
    table_dir.mkdir(parents=True, exist_ok=True)
    cells = cutoff+current.extra_cells
    values = []
    for name, builder in [("w.bin", build_w_lower_table), ("w-second.bin", build_w_second_lower_table)]:
        raw = (baseline_dir/"tables"/name).read_bytes()
        if digest(raw) != baseline_meta["hashes"][name] or len(raw) != 8*baseline_meta["cells"]:
            raise ValueError("baseline table corruption")
        table = list(struct.unpack(f">{baseline_meta['cells']}d", raw))
        table.extend(builder(current.grid, cells, current.kernel, current.precision, baseline_meta["cells"]))
        if len(table) != cells or any(not math.isfinite(x) for x in table):
            raise ValueError("extended table malformed")
        values.append(table)
        (table_dir/name).write_bytes(struct.pack(f">{cells}d", *table))
    hashes = {name: digest((table_dir/name).read_bytes()) for name in ["w.bin", "w-second.bin"]}
    full_binding = {**binding(), "tables": hashes, "cells": cells, "shard_count": 96}
    atomic_json(directory/"run-binding.json", full_binding)
    atomic_json(table_dir/"tables.json", {"binding": full_binding,
                                        "reused_source_cells": baseline_meta["cells"],
                                        "fresh_tail_cells": cells-baseline_meta["cells"],
                                        "reuse_basis": "kernel/grid/precision independent of pressure cutoff and target"})
    return full_binding


def read_state(path, expected, shard):
    obj = json.loads(path.read_bytes())
    data = obj["data"]
    if (digest(encoded(data)) != obj["sha256"] or data["binding"] != expected
            or data["shard"] != shard or data["schema"] != "exp020-checkpoint-v1"):
        raise ValueError("quadratic checkpoint binding/checksum mismatch")
    validate_state(data["state"], spec())
    if data["complete"] != (not data["state"]["stack"]):
        raise ValueError("quadratic checkpoint completion mismatch")
    return data["state"]


def worker(task):
    shard, directory, expected = task
    directory = Path(directory)
    if {k: expected[k] for k in binding()} != binding():
        raise ValueError("quadratic live source mismatch")
    tables = []
    for name, hash_value in expected["tables"].items():
        raw = (directory/"tables"/name).read_bytes()
        if digest(raw) != hash_value or len(raw) != expected["cells"]*8:
            raise ValueError("quadratic table mismatch")
    for name in ["w.bin", "w-second.bin"]:
        tables.append(list(struct.unpack(f">{expected['cells']}d", (directory/"tables"/name).read_bytes())))
    path = directory/"checkpoints"/f"shard-{shard:03d}.json"
    previous = read_state(path, expected, shard) if path.exists() else None
    last_print = last_save = time.monotonic()

    def callback(state, force):
        nonlocal last_print, last_save
        now = time.monotonic()
        if force or now-last_print >= 30:
            print(f"quadratic shard={shard}/96 nodes={state['nodes']} pending={len(state['stack'])} depth={state['maximum_depth']}", flush=True)
            last_print = now
        if force or now-last_save >= 60:
            validate_state(state, spec())
            data = {"schema": "exp020-checkpoint-v1", "binding": expected, "shard": shard,
                    "state": state, "complete": not state["stack"]}
            atomic_json(path, {"data": data, "sha256": digest(encoded(data))})
            last_save = now

    report = verify_general(spec(), shard=shard, shard_count=96, tables=tuple(tables),
                            resume_state=previous, state_callback=callback)
    result = {"binding": expected, "shard": shard, "report": report.__dict__,
              "checkpoint_sha256": digest(path.read_bytes())}
    atomic_json(directory/"reports"/f"shard-{shard:03d}.json", result)
    return result
