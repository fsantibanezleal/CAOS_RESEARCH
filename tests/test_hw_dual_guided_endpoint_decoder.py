from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN = (
    ROOT
    / "problems/commutative-algebra/huneke-wiegand/experiments"
    / "EXP-065-dual-guided-endpoint-decoder/run.py"
)


def load_run():
    spec = importlib.util.spec_from_file_location("exp065_test", RUN)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_dual_guided_escape_finds_integral_witness():
    module = load_run()
    columns = [[(0, 1), (1, 1)], [(1, 1)]]
    first = module.solve_qq(columns, {0}, 0)
    assert first["classification"] == "QQ_INCONSISTENT"
    escapes = module.escaping_columns(columns, {0}, first["dual"])
    assert escapes == [(1, first["dual"][1])]

    solved = module.solve_qq(columns, {0, 1}, 0)
    assert solved["classification"] == "INTEGRAL_SECTION"
    witness = {index: int(value) for index, value in solved["particular"].items()}
    assert module.multiply(columns, witness, 2) == [1, 0]


def test_reverse_order_and_hnf_controls():
    module = load_run()
    columns = [[(0, 1), (1, 1)], [(1, 1)]]
    assert module.solve_qq(columns, {0, 1}, 0, reverse=True)["classification"] == (
        "INTEGRAL_SECTION"
    )
    assert module.hnf_integer_solution([[(0, 2)]], {0}, 0, 1) is None


def test_endpoint_targets_are_distinct_and_training_only():
    module = load_run()
    assert module.target_triangles(8) == ((0, 1, 5), (0, 2, 4))
    assert module.target_triangles(10) == ((0, 1, 7), (0, 2, 6))

