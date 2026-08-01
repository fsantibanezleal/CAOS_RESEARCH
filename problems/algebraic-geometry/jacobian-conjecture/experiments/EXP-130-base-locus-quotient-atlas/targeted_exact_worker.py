"""Exact reconstruction for the EXP-130 common-quadratic targeted basis."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

from sympy import Rational, expand, eye, symbols


HERE = Path(__file__).resolve().parent
E125_PATH = HERE.parent / "EXP-125-factor-curve-recursion" / "run.py"
SELECTION = HERE / "artifacts" / "targeted-selection.json"
ARTIFACT = HERE / "artifacts" / "targeted-exact-worker.json"
EXPECTED_SELECTION = "605B8E29E9694D7249C69E5E1C92680D349E503D37725F105A6F3EDF95AD129C"

spec = importlib.util.spec_from_file_location("exp125_exp130_target_worker", E125_PATH)
exp125 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(exp125)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main() -> None:
    if sha256(SELECTION) != EXPECTED_SELECTION:
        raise AssertionError("targeted selection artifact hash mismatch")
    selection = json.loads(SELECTION.read_text(encoding="utf-8"))
    base, directions = exp125.exp124.build_full_system()
    a, b, c = symbols("A B C")
    records = []
    for atlas_index, selected in enumerate(selection["selected_atlas"], start=1):
        rows = selected["rows"]
        (
            selected_base,
            selected_directions,
            _,
            anchor_det,
            _,
            components,
            anchor_point,
            anchor_attempts,
        ) = exp125.exact_profile(base, directions, rows)
        if len(components[0]) > 60:
            raise AssertionError("largest SCC exceeds the declared size-60 gate")
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
        checked = exp125.exp124.exp122.cyclic_components(list(normalized.values()))
        if checked != components:
            raise AssertionError("SCC profile changed after exact normalization")
        expression = Rational(1)
        blocks = []
        for block_index, component in enumerate(components, start=1):
            block = (
                eye(len(component))
                + (a - anchor_point[0])
                * normalized[(0, 1)].extract(component, component)
                + (b - anchor_point[1])
                * normalized[(0, 5)].extract(component, component)
                + (c - anchor_point[2])
                * normalized[exp125.exp124.TARGET].extract(component, component)
            )
            determinant = expand(block.det(method="domain-ge"))
            expression = expand(expression * determinant)
            blocks.append(
                {
                    "size": len(component),
                    "vertices": component,
                    "determinant": str(determinant),
                }
            )
            print(
                f"[INFO] targeted atlas {atlas_index}/{len(selection['selected_atlas'])} "
                f"block {block_index}/{len(components)} size={len(component)}",
                flush=True,
            )
        records.append(
            {
                "atlas_index": atlas_index,
                "source_degree": selected["source_degree"],
                "rows": rows,
                "anchor": {
                    "point": list(anchor_point),
                    "determinant": str(anchor_det),
                    "attempts": anchor_attempts,
                },
                "cyclic_component_sizes": [len(item) for item in components],
                "determinant_ratio": str(expression),
                "block_records": blocks,
            }
        )
    payload = {
        "experiment": "EXP-130-targeted-exact-worker",
        "selection_sha256": EXPECTED_SELECTION,
        "atlas_records": records,
    }
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"[PASS] targeted exact worker SHA256 {sha256(ARTIFACT)}", flush=True)


if __name__ == "__main__":
    main()

