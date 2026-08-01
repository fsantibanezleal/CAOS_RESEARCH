"""Timeout-isolated characteristic-zero determinant worker for EXP-134."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import time
from pathlib import Path

from sympy import Rational, eye, expand, symbols


HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
EXP124_RUN = EXPERIMENTS / "EXP-124-rational-graph-alternative-chart" / "run.py"
EXP124_RESULTS = (
    EXPERIMENTS
    / "EXP-124-rational-graph-alternative-chart"
    / "artifacts"
    / "results.json"
)
CHECKPOINT = HERE / "artifacts" / "worker-checkpoint.json"
ARTIFACT = HERE / "artifacts" / "symbolic-worker.json"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def persist(payload: dict[str, object], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> None:
    started = time.time()
    exp124 = load_module("exp124_for_134", EXP124_RUN)
    accepted = json.loads(EXP124_RESULTS.read_text(encoding="utf-8"))
    rows = list(accepted["selected_rows"])
    base, directions = exp124.build_full_system()

    forced = exp124.exp112.forced_polynomial()
    all_directions = sorted(exp124.exp112.exp071.LOWER)
    _, complete_rows = exp124.exp112.complete_row_labels(forced, all_directions)
    constant_column = exp124.exp112.exp071.NQ.index((0, 0))
    q_columns = [
        index
        for index in range(len(exp124.exp112.exp071.NQ))
        if index != constant_column
    ]
    directions[(2, 8)] = exp124.exp112.coefficient_matrix(
        {(2, 8): exp124.exp112.Fraction(1)},
        complete_rows,
        q_columns,
        include_rhs=False,
    )

    selected_base = base.extract(rows, range(125))
    selected_directions = {
        direction: matrix.extract(rows, range(125))
        for direction, matrix in directions.items()
    }
    anchor = selected_base + selected_directions[(0, 1)]
    anchor_determinant = anchor.det(method="domain-ge")
    if anchor_determinant == 0:
        raise AssertionError("accepted EXP-124 anchor became singular")
    inverse = anchor.inv()
    normalized = {
        direction: inverse * matrix
        for direction, matrix in selected_directions.items()
    }
    components = exp124.exp122.cyclic_components(list(normalized.values()))
    largest = max(len(component) for component in components)
    if largest > 45:
        raise AssertionError(f"joint SCC {largest} exceeds declared gate 45")

    a, b, c, t = symbols("A B C T")
    expression = Rational(1)
    blocks: list[dict[str, object]] = []
    checkpoint: dict[str, object] = {
        "anchor_determinant": str(anchor_determinant),
        "joint_component_sizes": [len(component) for component in components],
        "largest_joint_component": largest,
        "completed_blocks": blocks,
    }
    persist(checkpoint, CHECKPOINT)

    for index, component in enumerate(components, start=1):
        block = (
            eye(len(component))
            + (a - 1) * normalized[(0, 1)].extract(component, component)
            + b * normalized[(0, 5)].extract(component, component)
            + c * normalized[(2, 9)].extract(component, component)
            + t * normalized[(2, 8)].extract(component, component)
        )
        block_started = time.time()
        determinant = expand(block.det(method="domain-ge"))
        expression = expand(expression * determinant)
        blocks.append(
            {
                "index": index,
                "size": len(component),
                "vertices": component,
                "determinant": str(determinant),
                "elapsed_seconds": time.time() - block_started,
            }
        )
        checkpoint["partial_determinant_ratio"] = str(expression)
        checkpoint["elapsed_seconds"] = time.time() - started
        persist(checkpoint, CHECKPOINT)
        print(
            f"[INFO] exact block {index}/{len(components)} "
            f"size={len(component)} elapsed={blocks[-1]['elapsed_seconds']:.2f}s",
            flush=True,
        )

    payload = {
        "determinant_ratio": str(expression),
        "anchor_determinant": str(anchor_determinant),
        "joint_component_sizes": [len(component) for component in components],
        "largest_joint_component": largest,
        "block_records": blocks,
        "elapsed_seconds": time.time() - started,
    }
    persist(payload, ARTIFACT)
    digest = hashlib.sha256(ARTIFACT.read_bytes()).hexdigest().upper()
    print(f"[PASS] symbolic worker SHA256 {digest}", flush=True)


if __name__ == "__main__":
    main()
