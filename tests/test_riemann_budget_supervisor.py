"""Real Windows process ownership checks for the separate cost supervisor."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

SOURCE = (Path(__file__).resolve().parents[1]
          / "problems/number-theory/riemann-hypothesis/experiments"
          / "EXP-023-repressured-local-certificate/budget_supervisor.py")
SPEC = importlib.util.spec_from_file_location("rh_budget_supervisor", SOURCE)
SUPERVISOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SUPERVISOR)


def test_snapshot_rejects_corrupt_atomic_state(tmp_path):
    output = tmp_path / "state"
    output.mkdir()
    (output / "checkpoint.json").write_text('{"incomplete":', encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        SUPERVISOR.archive(output, tmp_path / "snapshot.zip")


@pytest.mark.skipif(os.name != "nt", reason="Windows process ownership control")
def test_fast_runner_exit_is_not_a_certificate(tmp_path):
    record = SUPERVISOR.supervise(
        [sys.executable, "-c", "pass", str(tmp_path)], tmp_path, 8,
        tmp_path / "receipt.json", tmp_path / "runner.log")
    assert record["exit_code"] == 0
    assert record["state"] == "runner exited; coverage not assessed"
    assert "owned_stop" not in record
    assert record["mathematical_verdict"] == "not assessed"


@pytest.mark.skipif(os.name != "nt", reason="Windows process ownership control")
def test_real_budget_stop_preserves_unrelated_process(tmp_path):
    sentinel = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(90)"])
    output = tmp_path / "owned-output"
    child_code = (
        "import subprocess,sys,time,json; from pathlib import Path; "
        "p=subprocess.Popen([sys.executable,'-c','import time; time.sleep(90)']); "
        "Path(sys.argv[-1],'child.json').write_text(json.dumps({'pid':p.pid})); "
        "time.sleep(90)"
    )
    try:
        record = SUPERVISOR.supervise(
            [sys.executable, "-c", child_code, str(output)], output, 8,
            tmp_path / "receipt.json", tmp_path / "runner.log")
        child_pid = json.loads((output / "child.json").read_text())["pid"]
        ended = record["owned_stop"]["stopped"] + record["owned_stop"]["already_exited"]
        assert child_pid in ended
        assert record["root_pid"] in ended
        assert sentinel.poll() is None
        assert sentinel.pid not in record["owned_stop"]["stopped"]
        assert record["snapshot_before_stop"]["files_sha256"]["child.json"]
        assert record["mathematical_verdict"] == "not assessed"
        assert record["elapsed_seconds"] < 30
    finally:
        sentinel.terminate()
        sentinel.wait(timeout=15)
