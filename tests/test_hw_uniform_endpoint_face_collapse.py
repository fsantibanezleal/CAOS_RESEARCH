from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUN = (
    ROOT
    / "problems/commutative-algebra/huneke-wiegand/experiments"
    / "EXP-066-uniform-endpoint-face-collapse/run.py"
)


def load_run():
    spec = importlib.util.spec_from_file_location("exp066_test", RUN)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_modules(module):
    return {
        "exp036": module.load_module("test_exp036", module.EXP036 / "run.py"),
        "exp037": module.load_module("test_exp037", module.EXP037 / "run.py"),
        "exp042": module.load_module("test_exp042", module.EXP042 / "run.py"),
        "exp048": module.load_module("test_exp048", module.EXP048 / "run.py"),
        "exp063": module.load_module("test_exp063", module.EXP063 / "run.py"),
    }


def test_uniform_face_counts_and_endpoint_projection():
    module = load_run()
    modules = load_modules(module)
    for p in (8, 11, 37):
        for r in (1, 2):
            record = module.check_formula(p, r, modules)
            assert record["counts"] == {"R0": p - 3, "R2": p - 3, "R5": 1}
            assert record["projected_sign"] == -1
            assert record["projected_row_hash"] == module.digest(module.target_label(p, r))


def test_negative_controls_are_rejected():
    module = load_run()
    modules = load_modules(module)
    assert module.check_mutations(11, 1, modules) == 5
    assert module.check_mutations(11, 2, modules) == 5


def test_sparse_locked_holdout_matches_unique_frozen_columns():
    module = load_run()
    modules = load_modules(module)
    result = module.holdout(modules)
    assert result["status"] == "HOLDOUT_PASS"
    assert [record["component_column"] for record in result["records"]] == [210, 308]
    assert [record["component_row"] for record in result["records"]] == [12559, 12560]
