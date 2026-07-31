"""Timeout-isolated exact determinant worker for EXP-124."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import time
from pathlib import Path

from sympy import Rational, eye, expand, symbols


HERE = Path(__file__).resolve().parent
RUN_PATH = HERE / "run.py"
CHECKPOINT = HERE / "artifacts" / "checkpoint.json"
ARTIFACT = HERE / "artifacts" / "symbolic-worker.json"

spec = importlib.util.spec_from_file_location("exp124", RUN_PATH)
exp124 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(exp124)


def main() -> None:
    started = time.time()
    checkpoint = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
    rows = checkpoint["selected_rows"]
    anchor_point = checkpoint["anchor"]["point"]
    base, directions = exp124.build_full_system()
    selected_base = base.extract(rows, range(125))
    selected_directions = {
        direction: matrix.extract(rows, range(125))
        for direction, matrix in directions.items()
    }
    anchor = (
        selected_base
        + anchor_point[0] * selected_directions[(0, 1)]
        + anchor_point[1] * selected_directions[(0, 5)]
        + anchor_point[2] * selected_directions[exp124.TARGET]
    )
    inverse = anchor.inv()
    normalized = {
        direction: inverse * matrix
        for direction, matrix in selected_directions.items()
    }
    components = exp124.exp122.cyclic_components(list(normalized.values()))
    a, b, c = symbols("A B C")
    expression = Rational(1)
    blocks = []
    for index, component in enumerate(components, start=1):
        block = (
            eye(len(component))
            + (a - anchor_point[0])
            * normalized[(0, 1)].extract(component, component)
            + (b - anchor_point[1])
            * normalized[(0, 5)].extract(component, component)
            + (c - anchor_point[2])
            * normalized[exp124.TARGET].extract(component, component)
        )
        determinant = block.det(method="domain-ge")
        expression = expand(expression * determinant)
        blocks.append(
            {
                "size": len(component),
                "vertices": component,
                "determinant": str(expand(determinant)),
            }
        )
        print(
            f"[INFO] exact block {index}/{len(components)} "
            f"size={len(component)}",
            flush=True,
        )
    payload = {
        "determinant_ratio": str(expand(expression)),
        "block_records": blocks,
        "elapsed_seconds": time.time() - started,
    }
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    digest = hashlib.sha256(ARTIFACT.read_bytes()).hexdigest().upper()
    print(f"[PASS] symbolic worker SHA256 {digest}", flush=True)


if __name__ == "__main__":
    main()
