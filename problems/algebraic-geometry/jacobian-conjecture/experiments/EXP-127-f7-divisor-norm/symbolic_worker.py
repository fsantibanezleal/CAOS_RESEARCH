"""Timeout-isolated exact determinant worker for the EXP-127 F7 basis."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from sympy import Rational, expand, eye, symbols


HERE = Path(__file__).resolve().parent
E125_DIR = HERE.parent / "EXP-125-factor-curve-recursion"
E125_PATH = E125_DIR / "run.py"
E125_ARTIFACT = E125_DIR / "artifacts" / "results.json"
CHECKPOINT = HERE / "artifacts" / "checkpoint.json"
ARTIFACT = HERE / "artifacts" / "symbolic-worker.json"

spec = importlib.util.spec_from_file_location("exp125_f7_worker", E125_PATH)
exp125 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(exp125)


def main() -> None:
    checkpoint = json.loads(CHECKPOINT.read_text(encoding="utf-8"))
    accepted = json.loads(E125_ARTIFACT.read_text(encoding="utf-8"))
    rows = checkpoint["selected_rows"]
    if rows != accepted["selected_rows"]["F7"]:
        raise AssertionError("checkpoint F7 rows differ from accepted EXP-125")
    anchor_point = checkpoint["anchor"]["point"]
    base, directions = exp125.exp124.build_full_system()
    selected_base = base.extract(rows, range(125))
    selected_directions = {
        direction: matrix.extract(rows, range(125))
        for direction, matrix in directions.items()
    }
    anchor = (
        selected_base
        + anchor_point[0] * selected_directions[(0, 1)]
        + anchor_point[1] * selected_directions[(0, 5)]
        + anchor_point[2] * selected_directions[exp125.exp124.TARGET]
    )
    inverse = anchor.inv()
    normalized = {
        direction: inverse * matrix
        for direction, matrix in selected_directions.items()
    }
    components = exp125.exp124.exp122.cyclic_components(list(normalized.values()))
    if [len(item) for item in components] != checkpoint["cyclic_component_sizes"]:
        raise AssertionError("worker SCC profile differs from checkpoint")

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
            * normalized[exp125.exp124.TARGET].extract(component, component)
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
    }
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"[PASS] wrote {ARTIFACT.relative_to(HERE)}", flush=True)


if __name__ == "__main__":
    main()
