from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
RUN = (
    ROOT
    / "problems"
    / "commutative-algebra"
    / "huneke-wiegand"
    / "experiments"
    / "EXP-067-simple-gluing-rigidity-transfer"
    / "run.py"
)


def load_run() -> ModuleType:
    spec = importlib.util.spec_from_file_location("exp067_test_run", RUN)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_predicted_apery_matches_direct_gluing() -> None:
    run = load_run()
    _, _, generators = run.EXP009.formula_mask(4)
    multiplicity = 96
    base = run.apery_from_generators(multiplicity, tuple(generators))
    glued = (multiplicity,) + tuple(5 * value for value in generators if value != multiplicity)
    assert run.apery_from_generators(multiplicity, glued) == run.predicted_glued_apery(base, 5)


def test_caos_gluing_case_and_negative_control() -> None:
    run = load_run()
    case = run.case_record(4, 5)
    assert case["accepted"]
    assert case["frobenius"] == 1939
    assert case["embedding_dimension"] == 44
    assert case["ideal_exponents"] == [480, 600]
    assert run.negative_control(5)["accepted"]


def test_first_admissible_q_values_are_coprime() -> None:
    run = load_run()
    assert run.first_admissible_q(96) == (1, 5, 7, 11, 13, 17, 19, 23)
