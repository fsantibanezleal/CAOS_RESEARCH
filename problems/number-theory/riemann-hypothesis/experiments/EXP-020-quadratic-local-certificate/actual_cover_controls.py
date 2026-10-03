"""Reject corrupted copies of a real completed cover; never alter live output."""

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile

AUDITOR_PATH = Path(__file__).resolve().parent.parent/"EXP-019-nine-point-local-replay/audit.py"
SPEC = importlib.util.spec_from_file_location("exp020_cover_audit", AUDITOR_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
canonical, require = MODULE.canonical, MODULE.require


def audit(directory):
    return MODULE.audit(directory, "EXP-020")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def write(path, obj):
    path.write_bytes((json.dumps(obj, indent=2)+"\n").encode())


def change_report(directory, key, value):
    path = directory/"reports/shard-001.json"
    obj = json.loads(path.read_bytes())
    obj["report"][key] = value
    write(path, obj)


def change_checkpoint(directory, change):
    # Recompute both transport hashes to test semantic gates, rather than
    # merely demonstrating that a checksum mismatch is noticed.
    path = directory/"checkpoints/shard-001.json"
    obj = json.loads(path.read_bytes())
    change(obj["data"])
    obj["sha256"] = sha(canonical(obj["data"]))
    write(path, obj)
    report_path = directory/"reports/shard-001.json"
    report = json.loads(report_path.read_bytes())
    report["checkpoint_sha256"] = sha(path.read_bytes())
    write(report_path, report)


def changed_binding(directory):
    path = directory/"run-binding.json"
    obj = json.loads(path.read_bytes())
    key = next(iter(obj["code"]))
    obj["code"][key] = "0"*64
    write(path, obj)


def changed_table(directory):
    path = directory/"tables/w.bin"
    raw = bytearray(path.read_bytes())
    raw[17] ^= 1
    path.write_bytes(raw)


def changed_checksum(directory):
    path = directory/"checkpoints/shard-001.json"
    obj = json.loads(path.read_bytes())
    obj["sha256"] = "0"*64
    write(path, obj)
    report_path = directory/"reports/shard-001.json"
    report = json.loads(report_path.read_bytes())
    report["checkpoint_sha256"] = sha(path.read_bytes())
    write(report_path, report)


def controls(directory, scratch_root):
    # This admission gate explicitly prevents synthetic or partial input
    # from being described as a test of the actual completed certificate.
    baseline = audit(directory)
    cases = [
        ("missing-report", lambda d: (d/"reports/shard-001.json").unlink(), "incomplete coverage"),
        ("duplicate-shard", lambda d: shutil.copyfile(d/"reports/shard-002.json", d/"reports/shard-001.json"), "duplicate or invalid shard"),
        ("false-verdict", lambda d: change_report(d, "verified", False), "false result"),
        ("wrong-target", lambda d: change_report(d, "target", "F >= 1"), "false result"),
        ("source-binding", changed_binding, "quadratic code mismatch"),
        ("table-byte", changed_table, "table changed"),
        ("checkpoint-checksum", changed_checksum, "checkpoint corrupt"),
        ("unfinished-checkpoint", lambda d: change_checkpoint(d, lambda x: x.update(complete=False)), "unfinished branch"),
        ("pending-stack", lambda d: change_checkpoint(d, lambda x: x["state"].update(stack=[[[[0, 0]]*8, 0]])), "unfinished branch"),
        ("initial-domain", lambda d: change_checkpoint(d, lambda x: x["state"].update(initial_sha256="0"*64)), "initial cover mismatch"),
        ("tree-accounting", lambda d: change_checkpoint(d, lambda x: x["state"].update(nodes=x["state"]["nodes"]+1)), "tree accounting"),
        ("boolean-counter", lambda d: change_report(d, "nodes", True), "report counter mismatch"),
    ]
    results = []
    scratch_root.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="exp020-corruption-", dir=scratch_root) as temporary:
        copy = Path(temporary)/"cover"
        for name, change, reason in cases:
            # Copies, never hard links: intentional mutations cannot reach
            # the original mathematical worker output.
            shutil.copytree(directory/"tables", copy/"tables", dirs_exist_ok=True)
            shutil.copytree(directory/"reports", copy/"reports", dirs_exist_ok=True)
            shutil.copytree(directory/"checkpoints", copy/"checkpoints", dirs_exist_ok=True)
            shutil.copyfile(directory/"run-binding.json", copy/"run-binding.json")
            change(copy)
            try:
                audit(copy)
            except ValueError as error:
                require(str(error) == reason, f"unexpected rejection for {name}: {error}")
                results.append({"case": name, "rejected": True, "reason": str(error)})
                print(f"REJECTED {name}: {error}", flush=True)
            else:
                raise ValueError(f"corruption accepted: {name}")
            shutil.rmtree(copy)
    # Detect any unexpected change to the real completed input during tests.
    after = audit(directory)
    require(after == baseline, "original cover changed during controls")
    return {"schema": "exp020-actual-cover-corruption-controls-v1", "passed": True,
            "actual_cover_reports_sha256": baseline["reports_sha256"],
            "auditor_sha256": baseline["auditor_sha256"],
            "control_source_sha256": sha(Path(__file__).read_bytes()), "cases": results,
            "scope": "corruption rejection on copies of real complete output; no independent replay of interval leaves or formal proof"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--scratch-root", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args()
    result = controls(args.output_dir.resolve(), args.scratch_root.resolve())
    write(args.receipt, result)
