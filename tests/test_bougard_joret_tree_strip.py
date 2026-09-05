"""Exact regression replay; all writes go to the pytest temporary directory."""

import json
import subprocess
import sys
from pathlib import Path


def test_tree_strip_certificate_replays(tmp_path):
    root = Path(__file__).resolve().parents[1]
    experiment = root / "problems/combinatorics/bougard-joret/experiments/EXP-001-tree-strip"
    output = tmp_path / "certificate.json"
    subprocess.run([sys.executable, str(experiment / "run.py"), "--output", str(output)],
                   cwd=root, check=True, timeout=60)
    assert json.loads(output.read_text()) == json.loads(
        (experiment / "artifacts/certificate.json").read_text()
    )
