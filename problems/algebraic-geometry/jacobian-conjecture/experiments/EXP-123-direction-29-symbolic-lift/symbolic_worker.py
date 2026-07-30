"""Timeout-isolated exact determinant worker for EXP-123."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import time
from pathlib import Path

from sympy import Rational, eye, expand, symbols


HERE = Path(__file__).resolve().parent
RUN_PATH = HERE / "run.py"
ARTIFACT = HERE / "artifacts" / "symbolic-worker.json"

spec = importlib.util.spec_from_file_location("exp123", RUN_PATH)
exp123 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(exp123)


def main() -> None:
    started = time.time()
    (
        _,
        _,
        _,
        _,
        _,
        _,
        normalized,
        components,
    ) = exp123.build_selected_system()
    a, b, c = symbols("A B C")
    expression = Rational(1)
    blocks = []
    matrices = (
        normalized[(0, 1)],
        normalized[(0, 5)],
        normalized[exp123.TARGET],
    )
    for index, component in enumerate(components, start=1):
        block = (
            eye(len(component))
            + (a - 1) * matrices[0].extract(component, component)
            + b * matrices[1].extract(component, component)
            + c * matrices[2].extract(component, component)
        )
        block_determinant = block.det(method="domain-ge")
        expression = expand(expression * block_determinant)
        blocks.append(
            {
                "size": len(component),
                "vertices": component,
                "determinant": str(expand(block_determinant)),
            }
        )
        print(
            f"[INFO] exact block {index}/{len(components)} "
            f"size={len(component)}",
            flush=True,
        )
    expression = expand(expression)
    payload = {
        "determinant_ratio": str(expression),
        "block_records": blocks,
        "cyclic_component_sizes": [
            len(component) for component in components
        ],
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
