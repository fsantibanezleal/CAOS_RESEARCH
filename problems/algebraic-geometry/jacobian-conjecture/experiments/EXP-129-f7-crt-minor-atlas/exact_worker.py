"""EXP-129 exact block-determinant reconstruction for the selected atlas."""

from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

from sympy import Rational, expand, eye, symbols


HERE = Path(__file__).resolve().parent
E125_PATH = HERE.parent / "EXP-125-factor-curve-recursion" / "run.py"
SELECTION = HERE / "artifacts" / "selection.json"
ARTIFACT = HERE / "artifacts" / "exact-worker.json"
EXPECTED_SELECTION = "B43053AEEE214A77E79AEE00FBE6B66EFB3A5C2F2DF410A650B8EFA43982CEC3"

spec = importlib.util.spec_from_file_location("exp125_exp129_worker", E125_PATH)
exp125 = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(exp125)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def main() -> None:
    if sha256(SELECTION) != EXPECTED_SELECTION:
        raise AssertionError("selection artifact hash mismatch")
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
        checked_components = exp125.exp124.exp122.cyclic_components(list(normalized.values()))
        if checked_components != components:
            raise AssertionError("SCC profile changed after exact normalization")
        expression = Rational(1)
        blocks = []
        for block_index, component in enumerate(components, start=1):
            block = (
                eye(len(component))
                + (a - anchor_point[0]) * normalized[(0, 1)].extract(component, component)
                + (b - anchor_point[1]) * normalized[(0, 5)].extract(component, component)
                + (c - anchor_point[2]) * normalized[exp125.exp124.TARGET].extract(component, component)
            )
            determinant = expand(block.det(method="domain-ge"))
            expression = expand(expression * determinant)
            blocks.append({"size": len(component), "vertices": component, "determinant": str(determinant)})
            print(
                f"[INFO] atlas {atlas_index}/{len(selection['selected_atlas'])} "
                f"block {block_index}/{len(components)} size={len(component)}",
                flush=True,
            )
        records.append({
            "atlas_index": atlas_index,
            "source_degree": selected["source_degree"],
            "rows": rows,
            "anchor": {"point": list(anchor_point), "determinant": str(anchor_det), "attempts": anchor_attempts},
            "cyclic_component_sizes": [len(component) for component in components],
            "determinant_ratio": str(expression),
            "block_records": blocks,
        })
    payload = {"experiment": "EXP-129-exact-worker", "selection_sha256": EXPECTED_SELECTION, "atlas_records": records}
    ARTIFACT.parent.mkdir(parents=True, exist_ok=True)
    ARTIFACT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(f"[PASS] wrote {ARTIFACT.relative_to(HERE)}", flush=True)
    print(f"SHA256 {sha256(ARTIFACT)}", flush=True)


if __name__ == "__main__":
    main()
