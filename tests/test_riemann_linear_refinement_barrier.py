from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path

import pytest

pytest.importorskip("flint")

ROOT = Path(__file__).resolve().parents[1]
EXPERIMENT = ROOT / "problems/number-theory/riemann-hypothesis/experiments" / "EXP-011-linear-refinement-barrier"


def _load(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, EXPERIMENT / filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


RUN = _load("riemann_exp011_run", "run.py")


def _frozen() -> dict:
    return json.loads(RUN.FROZEN.read_text(encoding="utf-8"))


def test_kernel_is_normalized_and_even() -> None:
    RUN.ctx.prec = RUN.PREC_BITS
    kernel = RUN.Kernel()
    assert abs(kernel(RUN.acb(0)).real - 1) < RUN.arb("1e-30")
    z = RUN.acb(RUN.ball("0.7"), RUN.ball("0.2"))
    assert (kernel(z) - kernel(-z)).abs_upper() < RUN.arb("1e-30")


def test_c1_violates_the_linear_candidate_with_certified_margin() -> None:
    RUN.ctx.prec = RUN.PREC_BITS
    pts, mult = RUN.c1_points(_frozen())
    q = RUN.q_direct(pts, mult, RUN.Kernel())
    slack = q - 58
    assert RUN.upper(slack) < Fraction(-5, 100)
    product = q * 14 - 2 * 20**2
    assert RUN.lower(product) > 0


def test_lattice_formula_matches_the_direct_sum() -> None:
    RUN.ctx.prec = RUN.PREC_BITS
    kernel = RUN.Kernel()
    s, cell, mult, _ = RUN.c2_cell(_frozen())
    formula = RUN.q_lattice(s, cell, mult, 4, kernel)
    pts, mm = RUN.lattice_points(s, cell, mult, 4)
    assert formula.overlaps(RUN.q_direct(pts, mm, kernel))


def test_canonical_result_is_bound_and_accepted() -> None:
    out = EXPERIMENT / "artifacts" / "canonical"
    result = json.loads((out / "result.json").read_text(encoding="utf-8"))
    receipt = json.loads((out / "execution-receipt.json").read_text(encoding="utf-8"))
    assert result["accepted"] is True and all(result["checks"].values())
    assert receipt["result_sha256"] == hashlib.sha256((out / "result.json").read_bytes()).hexdigest()
    assert result["C2"]["O"] == 10001 and result["C2"]["N"] == 130013
    audit = json.loads((EXPERIMENT / "artifacts" / "audit" / "audit.json").read_text(encoding="utf-8"))
    assert audit["accepted"] is True
