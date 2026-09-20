from __future__ import annotations

import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = (
    ROOT
    / "problems"
    / "commutative-algebra"
    / "huneke-wiegand"
    / "experiments"
    / "EXP-063-triangle-isolated-comparison"
)
SPEC = importlib.util.spec_from_file_location("hw_exp063", EXPERIMENT / "run.py")
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def payload() -> dict[str, object]:
    return json.loads((EXPERIMENT / "artifacts" / "results.json").read_text(encoding="utf-8"))


def test_triangle_enumeration_and_exact_labels() -> None:
    expected = {8: 3, 9: 4, 10: 5, 11: 7}
    for p, count in expected.items():
        values = MODULE.triangles(p)
        assert len(values) == count
        assert values[0] == (0, 1, p - 3)
        assert values[1] == (0, 2, p - 4)
        assert len({json.dumps(MODULE.triangle_label(p, value)) for value in values}) == count


def test_frozen_relation_spaces_have_the_declared_shape() -> None:
    result = payload()
    unsigned = dict(result)
    artifact_hash = unsigned.pop("artifact_hash")
    assert MODULE.digest(unsigned) == artifact_hash
    assert result["claims"] == {"P1": True, "P2": True, "P3": True}
    for row in result["rows"]:
        p = row["p"]
        q = row["triangle_count"]
        masks = {item["mask"]: item for item in row["masks"]}
        assert masks[59]["triangle_span_rank"] == q
        assert masks[62]["triangle_span_rank"] == q
        assert masks[59]["relations"] == []
        assert masks[62]["relations"] == []
        assert [item["bits_hex"] for item in masks[58]["relations"]] == ["0x1", "0x2"]
        expected_56 = q if p < 11 else q - 1
        assert masks[56]["relation_dimension"] == expected_56


def test_dependency_space_agrees_across_pivot_orders() -> None:
    columns = [0b0011, 0b1100]
    triangles = [0b0001, 0b0010, 0b0100]
    low = MODULE.dependency_space(columns, triangles, high=False)
    high = MODULE.dependency_space(columns, triangles, high=True)
    assert low == high == (2, [0b0011])
