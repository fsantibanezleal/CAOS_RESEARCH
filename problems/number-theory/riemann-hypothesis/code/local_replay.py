"""Packet-bound EXP-019 replay operations; heavy checkpoints live outside Git."""

from __future__ import annotations

import hashlib
import json
import math
import os
import platform
from fractions import Fraction
from pathlib import Path
import struct
import time

import flint
from flint import fmpq

from rh019_vendor.checkpoint_general import CertificateSpec, cutoff_cell_count, verify_general
from rh019_vendor.kernel import KernelSpec, build_w_lower_table, build_w_second_lower_table

PACKET_SHA = "9f113eb52fba9c3a1fd7d5f2714e925ef19d3104b8fdaa982661fa96794d0c0d"
CODE = Path(__file__).resolve().parent
PACKET = CODE.parent/"experiments/EXP-018-nine-point-distinct-transfer/artifacts/input/nine-point-final.json"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def atomic_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix+f".{os.getpid()}.tmp")
    with temporary.open("wb") as stream:
        stream.write(encoded(data)+b"\n")
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def spec_from_packet():
    raw = PACKET.read_bytes()
    if digest(raw) != PACKET_SHA:
        raise ValueError("packet hash mismatch")
    packet = json.loads(raw)
    pairs = [(i, j) for i in range(9) for j in range(i+1, 9)]
    if packet["s"] != 9 or packet["pair_order"] != [list(p) for p in pairs]:
        raise ValueError("packet pair cover mismatch")
    numerators = packet["pair_weight_numerators"]
    if len(numerators) != 36 or min(numerators) < 0:
        raise ValueError("invalid weights")
    den = packet["pair_weight_denominator"]
    weights = {ij: fmpq(n, den) for ij, n in zip(pairs, numerators) if n}
    if any(sum((w for (i, j), w in weights.items() if j-i == r), fmpq(0)) != 2
           for r in range(1, 9)):
        raise ValueError("capacity mismatch")
    if (packet["pressure"] != {"numerator": 1, "denominator": 2500}
            or packet["target_epsilon"] != {"numerator": 15211, "denominator": 2500000}):
        raise ValueError("pressure or target mismatch")
    kernel = KernelSpec(coeffs=tuple(fmpq(n, packet["window_coefficient_denominator"])
                                   for n in packet["window_coefficient_numerators"]),
                        omega_pi_multiples=(2, 4, 6, 8, 10, 12))
    return CertificateSpec(kernel=kernel, q=8, pressure=fmpq(1, 2500),
                           target=fmpq(15211, 2500000), weights=weights, grid=4000, precision=128)


def source_binding():
    vendor = CODE/"rh019_vendor"
    manifest = json.loads((vendor/"source-binding.json").read_bytes())
    for name, expected in manifest["files"].items():
        if digest((vendor/name).read_bytes()) != expected:
            raise ValueError(f"frozen source mismatch: {name}")
    paths = [Path(__file__), vendor/"kernel.py", vendor/"checkpoint_general.py", vendor/"source-binding.json"]
    runner = CODE.parent/"experiments/EXP-019-nine-point-local-replay/run.py"
    return {"packet_sha256": PACKET_SHA, "upstream_commit": manifest["upstream_commit"],
            "code": {str(p.relative_to(CODE)): digest(p.read_bytes()) for p in paths},
            "runner_sha256": digest(runner.read_bytes()),
            "runtime": {"python": platform.python_version(), "python_flint": flint.__version__,
                        "platform": platform.platform()}}


def pressure_audit():
    spec = spec_from_packet()
    cutoff = cutoff_cell_count(spec)
    pressure = Fraction(1, 2500)
    lower = math.nextafter(float(pressure), -math.inf)
    failures = []
    for n in range(cutoff):
        # Exact comparison of the complete compound expression actually used.
        result = math.nextafter(lower*n/spec.grid, -math.inf)
        if Fraction(result) > pressure*n/spec.grid:
            failures.append(n)
    for w in spec.weights.values():
        exact = Fraction(int(w.p), int(w.q))
        if not Fraction(math.nextafter(float(exact), -math.inf)) <= exact <= Fraction(math.nextafter(float(exact), math.inf)):
            raise ValueError("weight enclosure failed")
    target = Fraction(int(spec.target.p), int(spec.target.q))
    if Fraction(math.nextafter(float(target), math.inf)) < target:
        raise ValueError("target enclosure failed")
    result = {"schema": "exp019-pressure-audit-v1", "binding": source_binding(),
              "index_range": [0, cutoff-1], "checked_indices": cutoff,
              "invalid_indices": failures, "passed": not failures,
              "scope": "the exact pinned pressure/grid/target only; no generic compound-rounding theorem"}
    if failures:
        raise ValueError(result)
    return result


def table_chunk(task):
    start, stop, directory, binding = task
    path = Path(directory)/f"chunk-{start:06d}-{stop:06d}.json"
    if path.exists():
        chunk = json.loads(path.read_bytes())
        if chunk["binding"] != binding or digest(encoded(chunk["values"])) != chunk["values_sha256"]:
            raise ValueError("cached table chunk mismatch")
        if chunk["start"] != start or chunk["stop"] != stop:
            raise ValueError("cached table chunk coverage mismatch")
        return str(path)
    spec = spec_from_packet()
    a = build_w_lower_table(spec.grid, stop, spec.kernel, spec.precision, start)
    b = build_w_second_lower_table(spec.grid, stop, spec.kernel, spec.precision, start)
    values = [[x.hex() for x in a], [x.hex() for x in b]]
    chunk = {"binding": binding, "start": start, "stop": stop, "values": values,
             "values_sha256": digest(encoded(values))}
    atomic_json(path, chunk)
    print(f"table cells [{start},{stop}) saved", flush=True)
    return str(path)


def load_tables(directory, expected_binding):
    directory = Path(directory)
    meta = json.loads((directory/"tables.json").read_bytes())
    if meta["binding"] != expected_binding:
        raise ValueError("table code/packet binding mismatch")
    tables = []
    for name in ["w.bin", "w-second.bin"]:
        raw = (directory/name).read_bytes()
        if digest(raw) != meta["hashes"][name] or len(raw) != 8*meta["cells"]:
            raise ValueError("table byte/count mismatch")
        values = list(struct.unpack(f">{meta['cells']}d", raw))
        if any(not math.isfinite(x) for x in values):
            raise ValueError("nonfinite table")
        tables.append(values)
    if any(x < 0 for x in tables[0]):
        raise ValueError("negative squared-kernel table")
    spec = spec_from_packet()
    if meta["cells"] != cutoff_cell_count(spec)+spec.extra_cells:
        raise ValueError("incorrect table cover")
    return tuple(tables), meta


def validate_state(state, spec):
    count_keys = ["nodes", "pruned", "splits", "maximum_depth", "pressure_pruned",
                  "interval_pruned", "tangent_pruned", "initial_boxes"]
    if any(type(state[k]) is not int or state[k] < 0 for k in count_keys):
        raise ValueError("invalid state counter")
    if (state["nodes"] != state["splits"]+state["pruned"]
            or state["pruned"] != sum(state[k] for k in count_keys[4:7])
            or len(state["stack"]) != state["initial_boxes"]+state["splits"]-state["pruned"]):
        raise ValueError("checkpoint tree accounting mismatch")
    cutoff = cutoff_cell_count(spec)
    for box, depth in state["stack"]:
        if len(box) != spec.q or type(depth) is not int or not 0 <= depth <= state["maximum_depth"]+1:
            raise ValueError("invalid pending box")
        for lo, hi in box:
            if type(lo) is not int or type(hi) is not int or not 0 <= lo <= hi < cutoff:
                raise ValueError("invalid pending cell bounds")


def read_checkpoint(path, binding, shard, shard_count, spec):
    obj = json.loads(Path(path).read_bytes())
    data = obj["data"]
    if digest(encoded(data)) != obj["sha256"]:
        raise ValueError("checkpoint checksum mismatch")
    if (data["binding"] != binding or data["shard"] != shard
            or data["shard_count"] != shard_count or data["schema"] != "exp019-checkpoint-v1"):
        raise ValueError("checkpoint binding mismatch")
    validate_state(data["state"], spec)
    if data["complete"] != (not data["state"]["stack"]):
        raise ValueError("checkpoint completion mismatch")
    return data


def shard_worker(task):
    shard, shard_count, directory, binding = task
    directory = Path(directory)
    spec = spec_from_packet()
    tables, _ = load_tables(directory/"tables", source_binding())
    path = directory/"checkpoints"/f"shard-{shard:03d}.json"
    previous = read_checkpoint(path, binding, shard, shard_count, spec) if path.exists() else None
    # A completed shard is still passed through verify_general's deterministic
    # initial-cover binding check; it has no pending nodes to recompute.
    last_print = last_save = time.monotonic()

    def callback(state, force):
        nonlocal last_print, last_save
        now = time.monotonic()
        if force or now-last_print >= 30:
            print(f"shard={shard}/{shard_count} nodes={state['nodes']} pending={len(state['stack'])} depth={state['maximum_depth']}", flush=True)
            last_print = now
        if force or now-last_save >= 60:
            validate_state(state, spec)
            data = {"schema": "exp019-checkpoint-v1", "binding": binding,
                    "shard": shard, "shard_count": shard_count, "state": state,
                    "complete": not state["stack"]}
            atomic_json(path, {"data": data, "sha256": digest(encoded(data))})
            last_save = now

    report = verify_general(spec, shard=shard, shard_count=shard_count, tables=tables,
                            resume_state=previous["state"] if previous else None,
                            state_callback=callback)
    result = {"binding": binding, "shard": shard, "shard_count": shard_count,
              "report": report.__dict__, "checkpoint_sha256": digest(path.read_bytes())}
    atomic_json(directory/"reports"/f"shard-{shard:03d}.json", result)
    return result


def aggregate(directory, binding, shard_count=96):
    directory = Path(directory)
    files = sorted((directory/"reports").glob("shard-*.json"))
    if len(files) != shard_count:
        raise ValueError("incomplete shard coverage")
    seen, nodes, boxes = set(), 0, 0
    for path in files:
        obj = json.loads(path.read_bytes())
        s, report = obj["shard"], obj["report"]
        if type(s) is not int or not 0 <= s < shard_count or s in seen:
            raise ValueError("duplicate/invalid shard")
        if (obj["binding"] != binding or obj["shard_count"] != shard_count
                or report["verified"] is not True or report["target"] != "F >= 15211/2500000"
                or report["grid"] != 4000):
            raise ValueError("report binding/target mismatch")
        checkpoint = directory/"checkpoints"/f"shard-{s:03d}.json"
        data = read_checkpoint(checkpoint, binding, s, shard_count, spec_from_packet())
        if not data["complete"] or digest(checkpoint.read_bytes()) != obj["checkpoint_sha256"]:
            raise ValueError("report/checkpoint mismatch")
        for k in ["nodes", "pruned", "splits", "maximum_depth", "initial_boxes"]:
            if report[k] != data["state"][k]:
                raise ValueError("report/state accounting mismatch")
        if (report["details"]["w_table_sha256"] != binding["tables"]["w.bin"]
                or report["details"]["w_second_table_sha256"] != binding["tables"]["w-second.bin"]):
            raise ValueError("report table mismatch")
        seen.add(s)
        nodes += report["nodes"]
        boxes += report["initial_boxes"]
    if seen != set(range(shard_count)):
        raise ValueError("missing shard")
    return {"schema": "exp019-full-cover-v1", "binding": binding,
            "verified": True, "shards": shard_count, "nodes": nodes, "initial_boxes": boxes,
            "reports_sha256": {p.name: digest(p.read_bytes()) for p in files}}
