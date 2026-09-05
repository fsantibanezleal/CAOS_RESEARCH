"""Exact finite certificate replay, with all writes in the temporary directory."""

import json
import subprocess
import sys
from pathlib import Path


def test_next_matching_certificate(tmp_path):
    root = Path(__file__).resolve().parents[1]
    exp = root / "problems/combinatorics/bougard-joret/experiments/EXP-003-triangle-free-next-matching"
    output = tmp_path / "certificate.json"
    subprocess.run([sys.executable, str(exp / "run.py"), "--output", str(output)],
                   cwd=root, check=True, timeout=300)
    assert json.loads(output.read_text()) == json.loads((exp / "artifacts/certificate.json").read_text())
