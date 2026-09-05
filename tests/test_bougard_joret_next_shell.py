"""Replay the full exact finite certificate; no writes to historical artifacts."""

import json
import subprocess
import sys
from pathlib import Path


def test_next_shell_certificate_replays(tmp_path):
    root = Path(__file__).resolve().parents[1]
    experiment = root / "problems/combinatorics/bougard-joret/experiments/EXP-002-next-shell"
    output = tmp_path / "certificate.json"
    subprocess.run([sys.executable, str(experiment / "run.py"), "--output", str(output)],
                   cwd=root, check=True, timeout=300)
    assert json.loads(output.read_text()) == json.loads(
        (experiment / "artifacts/certificate.json").read_text()
    )
