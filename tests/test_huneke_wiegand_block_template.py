from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "problems"
    / "commutative-algebra"
    / "huneke-wiegand"
    / "experiments"
    / "EXP-006-block-family"
    / "run_template.py"
)
SPEC = importlib.util.spec_from_file_location("hw_block_template", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_seed_template_reconstructs_displayed_generators() -> None:
    assert MODULE.template_generators(14) == MODULE.SEED_GENERATORS


def test_template_requires_declared_parameter_domain() -> None:
    for invalid in (1, 13, 15):
        try:
            MODULE.template_generators(invalid)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid template parameter was accepted")


def test_template_generation_is_deterministic() -> None:
    generators = MODULE.template_generators(16)
    assert generators == MODULE.template_generators(16)
    assert len(generators) == len(set(generators))
