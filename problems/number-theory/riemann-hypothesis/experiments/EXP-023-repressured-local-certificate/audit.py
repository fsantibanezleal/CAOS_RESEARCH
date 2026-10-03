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


def nonnegative_integer(value):
    # bool is an int subclass, but is not a valid traversal count.
    return type(value) is int and value >= 0


def validate_counters(state, report):
    keys = ["nodes", "pruned", "splits", "initial_boxes", "maximum_depth",
            "pressure_pruned", "interval_pruned", "tangent_pruned"]
    require(all(nonnegative_integer(state[k]) for k in keys), "invalid tree counter")
    require(state["nodes"] == state["splits"]+state["pruned"] and
            state["pruned"] == sum(state[k] for k in keys[-3:]) and
            state["pruned"] == state["initial_boxes"]+state["splits"], "tree accounting")
    for key in keys[:5]:
        require(nonnegative_integer(report[key]) and report[key] == state[key],
                "report counter mismatch")
    for key in keys[-3:]:
        require(nonnegative_integer(report["details"][key]) and
                report["details"][key] == state[key], "pruning counter mismatch")


def audit(directory, experiment="EXP-023"):
    root = Path(__file__).resolve().parents[5]
    problem = Path(__file__).resolve().parents[2]
    raw = (problem/"experiments/EXP-018-nine-point-distinct-transfer/artifacts/input/nine-point-final.json").read_bytes()
    packet_sha = "9f113eb52fba9c3a1fd7d5f2714e925ef19d3104b8fdaa982661fa96794d0c0d"
    require(sha(raw) == packet_sha, "packet changed")
    packet = json.loads(raw)
    binding = json.loads((directory/"run-binding.json").read_bytes())
    require(binding["packet_sha256"] == packet_sha and binding["shard_count"] == 96,
            "run input mismatch")
    require(experiment == "EXP-023", "unknown target")
    stronger = True
    base = binding["baseline_source"] if stronger else binding
    pressure, target, grid = Fraction(1, 1250), Fraction(52231, 5000000), 4000
    require(binding["target"] == str(target) and binding["pressure"] == str(pressure)
            and binding["grid"] == grid and binding["precision"] == 128, "wrong target/parameters")
    require(base["packet_sha256"] == packet_sha and
            base["upstream_commit"] == "1610b97b7895ff34982260f8dcaf04a0f7b82cf7",
            "baseline identity mismatch")
    require({name.replace("\\", "/") for name in base["code"]} ==
            {"local_replay.py", "rh019_vendor/checkpoint_general.py",
             "rh019_vendor/kernel.py", "rh019_vendor/source-binding.json"},
            "missing or unexpected baseline source")
    for name, value in base["code"].items():
        require(sha((problem/"code"/name.replace("\\", "/")).read_bytes()) == value, "bound code mismatch")
    require(sha((problem/"experiments/EXP-019-nine-point-local-replay/run.py").read_bytes()) == base["runner_sha256"], "baseline runner changed")
    frozen = json.loads((problem/"code/rh019_vendor/source-binding.json").read_bytes())
    require(frozen["upstream_commit"] == "1610b97b7895ff34982260f8dcaf04a0f7b82cf7", "upstream mismatch")
    for name, value in frozen["files"].items():
        require(sha((problem/"code/rh019_vendor"/name).read_bytes()) == value, "frozen source mismatch")
    if stronger:
        require({name.replace("\\", "/") for name in binding["code"]} ==
                {"code/certified_quadratic.py", "code/pressure_replay.py",
                 "code/rh019_vendor/quadratic_general.py",
                 "experiments/EXP-023-repressured-local-certificate/run.py"},
                "missing or unexpected quadratic source")
        for name, value in binding["code"].items():
            require(sha((problem/name.replace("\\", "/")).read_bytes()) == value, "quadratic code mismatch")
    units = target*grid/pressure
    cutoff = -(-units.numerator//units.denominator)+1
    require(cutoff == 52232, "cutoff mismatch")
    cells = cutoff+8
    require(set(binding["tables"]) == {"w.bin", "w-second.bin"}, "missing or unexpected table")
    if stronger:
        require(binding["cells"] == cells, "binding cell count")
    tables = {}
    for name, value in binding["tables"].items():
        raw = (directory/"tables"/name).read_bytes()
        require(sha(raw) == value, "table changed")
        require(len(raw) == cells*8, "table count")
        tables[name] = list(struct.unpack(f">{cells}d", raw))
        require(all(math.isfinite(x) for x in tables[name]), "nonfinite table")
    require(min(tables["w.bin"]) >= 0, "negative w table")
    weights = {tuple(pair): Fraction(n, packet["pair_weight_denominator"])
               for pair, n in zip(packet["pair_order"], packet["pair_weight_numerators"])}
    require(min(weights.values()) >= 0 and
            all(sum(w for (i, j), w in weights.items() if j-i == r) == 2 for r in range(1, 9)),
            "capacity mismatch")
    p = math.nextafter(float(pressure), -math.inf)
    target_upper = math.nextafter(float(target), math.inf)
    require(Fraction(target_upper) >= target, "unsafe target enclosure")
    require(pressure*cutoff/grid > target, "outside-domain pressure margin")
    for n in range(8*(cutoff-1)+1):
        require(Fraction(math.nextafter(p*n/grid, -math.inf)) <= pressure*n/grid,
                "unsafe summed pressure rounding")
    for w in weights.values():
        require(Fraction(math.nextafter(float(w), -math.inf)) <= w <=
                Fraction(math.nextafter(float(w), math.inf)), "unsafe weight enclosure")
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
        require(obj["binding"] == binding and (stronger or obj["shard_count"] == 96), "report input mismatch")
        require(report["verified"] is True and report["target"] == f"F >= {target}"
                and report["grid"] == grid, "false result")
        raw = (directory/"checkpoints"/f"shard-{s:03d}.json").read_bytes()
        require(sha(raw) == obj["checkpoint_sha256"], "report/checkpoint mismatch")
        checkpoint = json.loads(raw)
        data = checkpoint["data"]
        require(sha(canonical(data)) == checkpoint["sha256"], "checkpoint corrupt")
        require(data["binding"] == binding and data["shard"] == s
                and (stronger or data["shard_count"] == 96),
                "checkpoint input mismatch")
        require(data["schema"] == ("exp023-checkpoint-v1" if stronger else "exp019-checkpoint-v1"), "checkpoint schema")
        state = data["state"]
        require(data["complete"] is True and state["stack"] == [], "unfinished branch")
        initial_digest = sha(json.dumps(expected[s], separators=(",", ":")).encode())
        require(state["initial_sha256"] == initial_digest and state["initial_boxes"] == len(expected[s]),
                "initial cover mismatch")
        validate_counters(state, report)
        require(report["details"]["w_table_sha256"] == binding["tables"]["w.bin"] and
                report["details"]["w_second_table_sha256"] == binding["tables"]["w-second.bin"], "table report mismatch")
        require(report["details"]["cutoff_cells"] == cutoff, "report cutoff mismatch")
        for key in totals:
            totals[key] += state[key]
        depth = max(depth, state["maximum_depth"])
        report_hashes[path.name] = sha(path.read_bytes())
    require(seen == set(range(96)) and totals["initial_boxes"] == len(initial), "missing cover")
    return {"schema": f"{experiment.lower().replace('-', '')}-independent-cover-audit-v1", "passed": True,
            "experiment": experiment,
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
    parser.add_argument("--experiment", choices=["EXP-023"], default="EXP-023")
    args = parser.parse_args()
    result = audit(args.output_dir, args.experiment)
    args.receipt.write_bytes((json.dumps(result, indent=2)+"\n").encode())
    print(json.dumps(result["totals"], indent=2), flush=True)
