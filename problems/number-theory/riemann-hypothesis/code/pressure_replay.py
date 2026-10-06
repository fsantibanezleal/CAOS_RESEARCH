"""EXP-023 pressure override; immutable interval core, prefix-only table reuse."""

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

TARGET = fmpq(52231, 5000000)
PRESSURE = fmpq(1, 1250)
EXPERIMENT = CODE.parent/"experiments/EXP-023-repressured-local-certificate"


def spec():
    return replace(spec_from_packet(), target=TARGET, pressure=PRESSURE)


def binding():
    additions = [CODE/"certified_quadratic.py", CODE/"pressure_replay.py",
                 CODE/"rh019_vendor/quadratic_general.py", EXPERIMENT/"run.py"]
    return {"baseline_source": source_binding(), "packet_sha256": PACKET_SHA,
            "target": str(TARGET), "pressure": str(PRESSURE), "grid": 4000,
            "precision": 128,
            "code": {str(p.relative_to(CODE.parent)): digest(p.read_bytes()) for p in additions}}


def pressure_audit():
    current = spec()
    pressure, target = Fraction(1, 1250), Fraction(52231, 5000000)
    cutoff = cutoff_cell_count(current)
    lower = math.nextafter(float(pressure), -math.inf)
    maximum_sum = current.q*(cutoff-1)
    for n in range(maximum_sum+1):
        if Fraction(math.nextafter(lower*n/current.grid, -math.inf)) > pressure*n/current.grid:
            raise ValueError("unsafe compound pressure rounding")
    for value in current.weights.values():
        exact = Fraction(int(value.p), int(value.q))
        if not (Fraction(math.nextafter(float(exact), -math.inf)) <= exact <=
                Fraction(math.nextafter(float(exact), math.inf))):
            raise ValueError("weight rounding failed")
    if Fraction(math.nextafter(float(target), math.inf)) < target:
        raise ValueError("unsafe target rounding")
    assert cutoff == 52232
    return {"schema": "exp023-pressure-audit-v1", "passed": True,
            "checked_indices": maximum_sum+1, "cutoff_indices": cutoff,
            "index_range": [0, maximum_sum],
            "target": str(TARGET), "pressure": str(PRESSURE), "binding": binding()}


def prepare(directory, baseline_dir):
    directory, baseline_dir = Path(directory), Path(baseline_dir)
    audited = pressure_audit()
    baseline_meta = json.loads((baseline_dir/"tables/tables.json").read_bytes())
    if baseline_meta["binding"] != source_binding():
        raise ValueError("baseline table source mismatch")
    cells = cutoff_cell_count(spec())+spec().extra_cells
    if baseline_meta["cells"] < cells:
        raise ValueError("prefix cache too short")
    prefixes, hashes = {}, {}
    for name in ["w.bin", "w-second.bin"]:
        raw = (baseline_dir/"tables"/name).read_bytes()
        if digest(raw) != baseline_meta["hashes"][name] or len(raw) != 8*baseline_meta["cells"]:
            raise ValueError("baseline table corruption")
        prefix = raw[:cells*8]
        values = struct.unpack(f">{cells}d", prefix)
        if any(not math.isfinite(x) for x in values) or (name == "w.bin" and min(values) < 0):
            raise ValueError("malformed prefix table")
        prefixes[name], hashes[name] = prefix, digest(prefix)
    full = {**binding(), "tables": hashes, "cells": cells, "shard_count": 96,
            "prefix_source": {"cells": baseline_meta["cells"], "hashes": baseline_meta["hashes"]}}
    if (directory/"run-binding.json").exists():
        if json.loads((directory/"run-binding.json").read_bytes()) != full:
            raise ValueError("existing run binding changed")
        for name, value in prefixes.items():
            if (directory/"tables"/name).read_bytes() != value:
                raise ValueError("existing prefix table changed")
        if json.loads((directory/"pressure-audit.json").read_bytes()) != audited:
            raise ValueError("existing rounding audit changed")
        return full
    table_dir = directory/"tables"
    table_dir.mkdir(parents=True, exist_ok=True)
    for name, value in prefixes.items():
        (table_dir/name).write_bytes(value)
    atomic_json(directory/"pressure-audit.json", audited)
    atomic_json(table_dir/"tables.json", {"binding": full, "reused_source_cells": cells,
                                        "fresh_tail_cells": 0, "byte_order": "big-endian"})
    atomic_json(directory/"run-binding.json", full)
    return full


def read_state(path, expected, shard):
    obj = json.loads(path.read_bytes())
    data = obj["data"]
    if (digest(encoded(data)) != obj["sha256"] or data["binding"] != expected
            or data["shard"] != shard or data["schema"] != "exp023-checkpoint-v1"):
        raise ValueError("pressure checkpoint binding/checksum mismatch")
    validate_state(data["state"], spec())
    if type(data["complete"]) is not bool or data["complete"] != (not data["state"]["stack"]):
        raise ValueError("checkpoint completion mismatch")
    return data["state"]


def worker(task):
    shard, directory, expected = task
    directory = Path(directory)
    live = binding()
    if {k: expected[k] for k in live} != live:
        raise ValueError("changed-pressure live source mismatch")
    tables = []
    for name in ["w.bin", "w-second.bin"]:
        raw = (directory/"tables"/name).read_bytes()
        if digest(raw) != expected["tables"][name] or len(raw) != expected["cells"]*8:
            raise ValueError("pressure table mismatch")
        tables.append(list(struct.unpack(f">{expected['cells']}d", raw)))
    path = directory/"checkpoints"/f"shard-{shard:03d}.json"
    previous = read_state(path, expected, shard) if path.exists() else None
    last_print = last_save = time.monotonic()

    def callback(state, force):
        nonlocal last_print, last_save
        now = time.monotonic()
        if force or now-last_print >= 30:
            print(f"pressure shard={shard}/96 nodes={state['nodes']} pending={len(state['stack'])} depth={state['maximum_depth']}", flush=True)
            last_print = now
        if force or now-last_save >= 60:
            validate_state(state, spec())
            data = {"schema": "exp023-checkpoint-v1", "binding": expected,
                    "shard": shard, "state": state, "complete": not state["stack"]}
            atomic_json(path, {"data": data, "sha256": digest(encoded(data))})
            last_save = now

    report = verify_general(spec(), shard=shard, shard_count=96, tables=tuple(tables),
                            resume_state=previous, state_callback=callback)
    result = {"binding": expected, "shard": shard, "report": report.__dict__,
              "checkpoint_sha256": digest(path.read_bytes())}
    atomic_json(directory/"reports"/f"shard-{shard:03d}.json", result)
    return result
