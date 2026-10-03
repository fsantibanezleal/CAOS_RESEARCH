"""Independent stdlib audit of packet binding, deterministic cover and receipts."""

from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import itertools
import json
import math
from pathlib import Path
import struct


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def audit(directory):
    root = Path(__file__).resolve().parents[5]
    problem = Path(__file__).resolve().parents[2]
    raw = (problem/"experiments/EXP-018-nine-point-distinct-transfer/artifacts/input/nine-point-final.json").read_bytes()
    packet_sha = "9f113eb52fba9c3a1fd7d5f2714e925ef19d3104b8fdaa982661fa96794d0c0d"
    require(sha(raw) == packet_sha, "packet changed")
    packet = json.loads(raw)
    binding = json.loads((directory/"run-binding.json").read_bytes())
    require(binding["packet_sha256"] == packet_sha and binding["shard_count"] == 96,
            "run input mismatch")
    for name, value in binding["code"].items():
        require(sha((problem/"code"/name).read_bytes()) == value, "bound code mismatch")
    require(sha((Path(__file__).parent/"run.py").read_bytes()) == binding["runner_sha256"], "runner changed")
    tables = {}
    for name, value in binding["tables"].items():
        raw = (directory/"tables"/name).read_bytes()
        require(sha(raw) == value, "table changed")
        require(len(raw) == 60853*8, "table count")
        tables[name] = list(struct.unpack(">60853d", raw))
    weights = {tuple(pair): Fraction(n, packet["pair_weight_denominator"])
               for pair, n in zip(packet["pair_order"], packet["pair_weight_numerators"])}
    require(min(weights.values()) >= 0 and
            all(sum(w for (i, j), w in weights.items() if j-i == r) == 2 for r in range(1, 9)),
            "capacity mismatch")
    pressure, target, grid = Fraction(1, 2500), Fraction(15211, 2500000), 4000
    units = target*grid/pressure
    cutoff = -(-units.numerator//units.denominator)+1
    require(cutoff == 60845, "cutoff mismatch")
    p = math.nextafter(float(pressure), -math.inf)
    target_upper = math.nextafter(float(target), math.inf)
    components = []
    excluded = []
    for coordinate in range(8):
        weight = math.nextafter(float(weights[coordinate, coordinate+1]), -math.inf)
        ranges = []
        rejected = 0
        for i in range(cutoff):
            pressure_term = math.nextafter(p*i/grid, -math.inf)
            require(Fraction(pressure_term) <= pressure*i/grid, "unsafe pressure")
            lower = math.nextafter(pressure_term+math.nextafter(weight*tables["w.bin"][i], -math.inf), -math.inf)
            if lower >= target_upper:
                rejected += 1
            elif ranges and i == ranges[-1][1]+1:
                ranges[-1][1] = i
            else:
                ranges.append([i, i])
        components.append(ranges)
        excluded.append(rejected)
    initial = list(itertools.product(*components))
    # Rebuild the modulo partition without calling the verifier or its helpers.
    expected = {s: [(parts, 0) for index, parts in enumerate(initial) if index % 96 == s]
                for s in range(96)}
    require(sum(len(v) for v in expected.values()) == len(initial), "non-covering partition")
    reports = list((directory/"reports").glob("*.json"))
    require(len(reports) == 96, "incomplete coverage")
    seen = set()
    totals = {key: 0 for key in ["nodes", "pruned", "splits", "initial_boxes",
                               "pressure_pruned", "interval_pruned", "tangent_pruned"]}
    depth = 0
    report_hashes = {}
    for path in reports:
        obj = json.loads(path.read_bytes())
        s, report = obj["shard"], obj["report"]
        require(type(s) is int and 0 <= s < 96 and s not in seen, "duplicate or invalid shard")
        seen.add(s)
        require(obj["binding"] == binding and obj["shard_count"] == 96, "report input mismatch")
        require(report["verified"] is True and report["target"] == "F >= 15211/2500000"
                and report["grid"] == grid, "false result")
        raw = (directory/"checkpoints"/f"shard-{s:03d}.json").read_bytes()
        require(sha(raw) == obj["checkpoint_sha256"], "report/checkpoint mismatch")
        checkpoint = json.loads(raw)
        data = checkpoint["data"]
        require(sha(canonical(data)) == checkpoint["sha256"], "checkpoint corrupt")
        require(data["binding"] == binding and data["shard"] == s and data["shard_count"] == 96,
                "checkpoint input mismatch")
        state = data["state"]
        require(data["complete"] is True and state["stack"] == [], "unfinished branch")
        initial_digest = sha(json.dumps(expected[s], separators=(",", ":")).encode())
        require(state["initial_sha256"] == initial_digest and state["initial_boxes"] == len(expected[s]),
                "initial cover mismatch")
        require(state["nodes"] == state["splits"]+state["pruned"] and
                state["pruned"] == sum(state[k] for k in ["pressure_pruned", "interval_pruned", "tangent_pruned"])
                and state["pruned"] == state["initial_boxes"]+state["splits"], "tree accounting")
        for key in ["nodes", "pruned", "splits", "initial_boxes", "maximum_depth"]:
            require(report[key] == state[key], "report counter mismatch")
        for key in ["pressure_pruned", "interval_pruned", "tangent_pruned"]:
            require(report["details"][key] == state[key], "pruning counter mismatch")
        require(report["details"]["w_table_sha256"] == binding["tables"]["w.bin"] and
                report["details"]["w_second_table_sha256"] == binding["tables"]["w-second.bin"], "table report mismatch")
        require(report["details"]["cutoff_cells"] == cutoff, "report cutoff mismatch")
        for key in totals:
            totals[key] += state[key]
        depth = max(depth, state["maximum_depth"])
        report_hashes[path.name] = sha(path.read_bytes())
    require(seen == set(range(96)) and totals["initial_boxes"] == len(initial), "missing cover")
    return {"schema": "exp019-independent-cover-audit-v1", "passed": True,
            "binding": binding, "totals": totals, "maximum_depth": depth,
            "coordinate_components": components, "excluded_cells_per_coordinate": excluded,
            "initial_boxes": len(initial), "reports_sha256": report_hashes,
            "auditor_sha256": sha(Path(__file__).read_bytes()),
            "repository_relative_auditor": str(Path(__file__).relative_to(root)),
            "scope": "independent binding/initial-domain/coverage/accounting audit; interval execution remains in the stated trust base"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    result = audit(args.output_dir)
    args.receipt.write_bytes((json.dumps(result, indent=2)+"\n").encode())
    print(json.dumps(result["totals"], indent=2), flush=True)
