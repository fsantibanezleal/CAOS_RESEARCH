"""Permanent declared EXP-062 checks; canonical artifacts are never test outputs."""

import gzip
import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "problems/commutative-algebra/huneke-wiegand/experiments/EXP-062-triangle-torsion-family"
SPEC = importlib.util.spec_from_file_location("triangle062_tests", HERE / "run.py")
MODEL = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODEL)


@pytest.fixture(scope="module")
def modules():
    return MODEL.dependencies()


@pytest.mark.parametrize("p", [8, 9, 10, 11, 12, 14, 25, 100])
def test_triangle_count_and_order(p):
    values = MODEL.triangles(p)
    assert values == sorted(set(values))
    assert len(values) == ((p - 2) ** 2 + 3) // 12
    assert all(0 <= i < j < k and i + j + k == p - 2 for i, j, k in values)


@pytest.mark.parametrize("triangle,rows", [((0, 1, 5), 11), ((0, 2, 4), 12), ((1, 2, 3), 10)])
def test_adjacency_and_exact_integer_sources(modules, triangle, rows):
    result = MODEL.check_triangle(8, triangle, modules)
    assert result["functional_rows"] == rows
    assert result["integer_boundary_equals_twice_class"]
    assert result["controls"]["removed_endpoint_rejected"]


def test_actual_integer_mutations(modules):
    helpers = modules["helpers"]
    result = MODEL.check_triangle(8, (1, 2, 3), modules)
    source = result["full_source"]
    for delta in (1, -2 * source[0]["coefficient"]):
        changed = [{**term, "exact_label": term["exact_label"].copy()} for term in source]
        changed[0]["coefficient"] += delta
        changed = [term for term in changed if term["coefficient"]]
        boundary = helpers.multiply(8, changed, modules, independent=True)
        assert boundary != helpers.vector(result["full_boundary"])


def test_full_small_pairing_and_selection_controls(modules):
    result = MODEL.check_parameter(8, modules)
    assert result["pairing_matrix"] == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    assert result["singular_selection_controls"]["duplicate_rank"] == 2
    assert result["singular_selection_controls"]["mirrored_rank"] == 2
    assert result["eta_transfer"]["verified"]


def test_sampling_frozen():
    assert MODEL.selected_triangles(14) == MODEL.triangles(14)
    values = MODEL.triangles(100)
    assert MODEL.selected_triangles(100) == [values[0], values[(len(values) - 1) // 2], values[-1]]


@pytest.mark.parametrize("triangle", [(0, 2, 3), (1, 1, 4), (2, 0, 4), (False, 2, 4)])
def test_invalid_triangles(triangle):
    with pytest.raises(ValueError):
        MODEL.triangle_potential(8, triangle)


def test_temporary_smoke_and_lossless_sources(tmp_path):
    output = tmp_path / "smoke.json"
    result = MODEL.run(output, smoke_only=True)
    assert result["status"] == "COMPLETE" and result["tested_sources"] == 3
    archive = result["full_source_archive"]
    payload = json.loads(gzip.decompress((tmp_path / archive["filename"]).read_bytes()))
    assert len(payload["sources"]) == 3 and len(payload["transfers"]) == 1
    assert len(result["count_checks"]) == 93


def test_budget_stop_preserves_partial_output(tmp_path):
    output = tmp_path / "capped.json"
    with pytest.raises(RuntimeError, match="time budget"):
        MODEL.run(output, smoke_only=True, budget=1e-12)
    result = json.loads(output.read_text())
    assert result["status"] == "RESOURCE_STOP" and result["rows"] == []


@pytest.mark.parametrize("budget", [0, -1, 121, float("nan")])
def test_invalid_budget(tmp_path, budget):
    with pytest.raises(ValueError):
        MODEL.run(tmp_path / "not-written.json", budget=budget)
