"""CPU orchestration only: bound wall time without changing any proof decision."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import time
import zipfile


def utc():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def archive(output, destination):
    """Read each atomic state file once; raw snapshots are not proof audits."""
    hashes = {}
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED) as zipped:
        for path in sorted(output.rglob("*")):
            if path.is_file() and path.suffix in {".json", ".bin"}:
                data = path.read_bytes()
                if path.suffix == ".json":
                    json.loads(data)
                name = path.relative_to(output).as_posix()
                hashes[name] = hashlib.sha256(data).hexdigest()
                zipped.writestr(name, data)
    with zipfile.ZipFile(destination) as zipped:
        if zipped.testzip() is not None:
            raise RuntimeError("snapshot CRC failed")
        for name, expected in hashes.items():
            if hashlib.sha256(zipped.read(name)).hexdigest() != expected:
                raise RuntimeError("snapshot hash failed")
    return {"sha256": digest(destination), "files_sha256": hashes,
            "scope": "raw individually parsed state; no cross-file or mathematical audit"}


def supervise(command, output, budget, receipt, log):
    if budget <= 0:
        raise ValueError("positive budget required")
    output.mkdir(parents=True, exist_ok=True)
    receipt.parent.mkdir(parents=True, exist_ok=True)
    stop_script = Path(__file__).with_name("stop_owned_tree.ps1")
    record = {"schema": "owned-budget-supervisor-v1", "start_utc": utc(),
              "budget_seconds": budget, "command": command,
              "supervisor_sha256": digest(Path(__file__)),
              "stop_script_sha256": digest(stop_script), "mathematical_verdict": "not assessed"}
    start = time.monotonic()
    with log.open("ab", buffering=0) as stream:
        process = subprocess.Popen(command, stdout=stream, stderr=subprocess.STDOUT)
        # A live OS handle owned by Popen plus an immutable creation timestamp.
        ticks_command = (f"$p=Get-Process -Id {process.pid} -ErrorAction SilentlyContinue; "
                         "if ($null -ne $p) {$p.StartTime.ToUniversalTime().Ticks}; exit 0")
        ticks = subprocess.check_output(
            ["powershell.exe", "-NoProfile", "-Command", ticks_command], text=True).strip()
        if not ticks and process.poll() is None:
            raise RuntimeError("live owned root has no creation timestamp")
        record.update(root_pid=process.pid, root_started_ticks=int(ticks) if ticks else None,
                      state="running" if process.poll() is None else "runner already exited")
        receipt.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(record), flush=True)
        while process.poll() is None and time.monotonic() - start < budget:
            time.sleep(min(2, max(0, budget - (time.monotonic() - start))))
        if process.poll() is None:
            record.update(state="budget reached; coverage not assessed", deadline_action_utc=utc())
            snapshot = output / f"budget-snapshot-{process.pid}.zip"
            try:
                record["snapshot_before_stop"] = archive(output, snapshot)
            except Exception as error:
                # Operational failure must not silently become an unbounded run.
                record["snapshot_error"] = repr(error)
            stopped = subprocess.check_output(
                ["powershell.exe", "-NoProfile", "-File", str(stop_script),
                 "-RootPid", str(process.pid), "-RootStartedTicks", ticks,
                 "-CommandToken", command[-1]], text=True)
            record["owned_stop"] = json.loads(stopped)
            process.wait(timeout=30)
        else:
            record["state"] = "runner exited; coverage not assessed"
        record.update(exit_code=process.returncode, end_utc=utc(),
                      elapsed_seconds=time.monotonic() - start)
        record["budget_overshoot_seconds"] = max(0, record["elapsed_seconds"] - budget)
        receipt.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(record), flush=True)
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--budget-seconds", type=float, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--log", type=Path, required=True)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        parser.error("runner command required")
    supervise(command, args.output_dir, args.budget_seconds, args.receipt, args.log)


if __name__ == "__main__":
    main()
