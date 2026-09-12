"""Independent combinatorial checks and adversarial pressure-certificate replay."""

from __future__ import annotations

import copy
import hashlib
import itertools
import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

import pytest
from flint import ctx

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "problems/number-theory/riemann-hypothesis/code"))
from riemann_pressure import (  # noqa: E402
    SCHEMA, certify_pressure_triangle, digest, frame_coefficients, gain_comparison,
    parameters, pressure_frame_bound, verify_pressure_triangle,
)


@pytest.fixture(autouse=True)
def precision():
    previous = ctx.prec
    ctx.prec = 160
    yield
    ctx.prec = previous


@pytest.fixture(scope="module")
def easy_certificate():
    previous = ctx.prec
    ctx.prec = 160
    try:
        return certify_pressure_triangle("3/4", "1/20", "1/10")
    finally:
        ctx.prec = previous


def modified(certificate, **updates):
    value = copy.deepcopy(certificate)
    value.update(updates)
    value["tree_sha256"] = hashlib.sha256(value["tree"].encode()).hexdigest()
    return value


def test_frame_pairs_and_span_coefficients():
    for k in range(1, 9):
        size = 2 * k + 1
        triples = [tuple(range(start, start + 3)) for start in range(0, size - 2, 2)]
        pairs = Counter(pair for triple in triples for pair in itertools.combinations(triple, 2))
        assert len(pairs) == 3 * k
        assert set(pairs.values()) == {1}
        spans = Counter(gap for triple in triples for gap in range(triple[0], triple[-1]))
        assert spans == Counter(range(size - 1))
        # Overlapping triples really share vertices; they are not pinched separately.
        if k > 1:
            assert set(triples[0]) & set(triples[1]) == {2}


def test_frame_offset_coverage_including_short_sequences():
    for k in range(1, 9):
        size = 2 * k + 1
        for count in range(41):
            starts = []
            for offset in range(size):
                group = list(range(offset, count - size + 1, size))
                assert all(b - a == size for a, b in zip(group, group[1:]))
                starts.extend(group)
            assert sorted(starts) == list(range(max(0, count - size + 1)))
            gap_counts = Counter(gap for start in starts for gap in range(start, start + size - 1))
            assert max(gap_counts.values(), default=0) <= size - 1
            assert all(0 <= gap < count - 1 for gap in gap_counts)


def test_frame_exact_stage_a_coefficient_and_unit_cap():
    d, radius = Fraction(1, 7000), Fraction(21, 4)
    alpha, beta = frame_coefficients(d, d / radius, 7000)
    assert alpha == Fraction(1, 14001)
    assert beta == 2 * alpha / radius
    assert alpha / (1 - alpha) == d / 2
    assert (alpha / (1 - alpha)) > d / (3 - d)
    with pytest.raises(ValueError, match="unit cap"):
        frame_coefficients(d, d / radius, 7001)
    for k in (True, 0, Fraction(2)):
        with pytest.raises(ValueError):
            frame_coefficients(d, d / radius, k)


def test_gain_gate_rejects_stage_a_itself():
    assert gain_comparison("3/4", Fraction(1, 7000) / Fraction(21, 4), "1/7000", 7000) < 0
    # Doubling both p and epsilon preserves the cutoff and increases the conditional gain.
    assert gain_comparison("3/4", Fraction(2, 7000) / Fraction(21, 4), "1/3500", 3500) > 0
    assert pressure_frame_bound("3/4", "1/20", "1/10", 10).is_finite()


@pytest.mark.parametrize("theta,p,epsilon", [
    ("0", "1/20", "1/10"), ("1", "1/20", "1/10"),
    ("3/4", "0", "1/10"), ("3/4", "-1", "1/10"),
    ("3/4", "1/20", "0"), ("3/4", "1/20", "3/4"),
    ("3/4", "1/1000", "1/10"), (0.75, "1/20", "1/10"),
])
def test_invalid_exact_parameters(theta, p, epsilon):
    with pytest.raises(ValueError):
        parameters(theta, p, epsilon)


@pytest.mark.parametrize("updates,reason", [
    ({"schema": "riemann-triangle-v1"}, "schema"),
    ({"cutoff": "1"}, "cutoff"),
    ({"tree": "P"}, "pressure-only"),
    ({"tree": "V"}, "Uncertified"),
    ({"tree": "O"}, "Unknown"),
    ({"tree": "?"}, "Unknown"),
    ({"unresolved_boxes": 1}, "Incomplete"),
    ({"nodes": 1}, "count"),
    ({"validated_leaves": -1}, "count"),
    ({"pressure_leaves": -1}, "count"),
])
def test_tampered_certificate_fails(easy_certificate, updates, reason):
    with pytest.raises(ValueError, match=reason):
        verify_pressure_triangle(modified(easy_certificate, **updates), independent=False)


def test_partition_digest_and_completeness(easy_certificate):
    damaged = copy.deepcopy(easy_certificate)
    damaged["tree_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="hash"):
        verify_pressure_triangle(damaged)
    with pytest.raises(ValueError, match="Incomplete"):
        verify_pressure_triangle(modified(easy_certificate, tree=easy_certificate["tree"][:-1]))
    with pytest.raises(ValueError, match="Trailing"):
        verify_pressure_triangle(modified(easy_certificate, tree=easy_certificate["tree"] + "P"))


def test_cutoff_boundary_pressure_is_exact(easy_certificate):
    # Reconstruct the cover independently: equality at the cutoff is valid pressure,
    # but a cell whose lower corner lies below it must never be a pressure-only leaf.
    cutoff = Fraction(easy_certificate["cutoff"])
    stack = [(Fraction(0), cutoff, Fraction(0), cutoff)]
    equal = 0
    for token in easy_certificate["tree"]:
        u0, u1, v0, v1 = stack.pop()
        if token == "B":
            if u1 - u0 >= v1 - v0:
                mid = (u0 + u1) / 2
                children = [(u0, mid, v0, v1), (mid, u1, v0, v1)]
            else:
                mid = (v0 + v1) / 2
                children = [(u0, u1, v0, mid), (u0, u1, mid, v1)]
            stack.extend(reversed(children))
        elif token == "P":
            assert u0 + v0 >= cutoff
            equal += u0 + v0 == cutoff
    assert not stack
    assert equal > 0


def test_construction_checkpoint_resume_and_metadata(tmp_path, easy_certificate, capsys):
    path = tmp_path / "construction.json"
    with pytest.raises(TimeoutError, match="unresolved"):
        certify_pressure_triangle("3/4", "1/20", "1/10", max_nodes=10,
                                  checkpoint=path, progress_every=1)
    saved = json.loads(path.read_text())
    assert saved["counts"]["nodes"] == 10
    assert saved["pending"] and saved["source_identity"]
    assert saved["precision_bits"] == 160
    assert b"\r\n" not in path.read_bytes()
    assert '"event": "progress"' in capsys.readouterr().out
    resumed = certify_pressure_triangle("3/4", "1/20", "1/10", checkpoint=path, resume=True)
    assert resumed == easy_certificate
    with pytest.raises(ValueError, match="parameters"):
        certify_pressure_triangle("3/4", "1/30", "1/10", checkpoint=path, resume=True)
    saved["pending"] = []
    path.write_text(json.dumps(saved))
    with pytest.raises(ValueError, match="coverage"):
        certify_pressure_triangle("3/4", "1/20", "1/10", checkpoint=path, resume=True)


def test_replay_budget_checkpoint_and_untrusted_prefix(tmp_path, easy_certificate):
    path = tmp_path / "replay.json"
    ctx.prec = 256
    with pytest.raises(TimeoutError, match="unchecked"):
        verify_pressure_triangle(easy_certificate, budget=0, checkpoint=path)
    saved = json.loads(path.read_text())
    assert saved["phase"] == "replay" and saved["pending"]
    assert saved["evaluator"] == "sinc-taylor-96"
    resumed = verify_pressure_triangle(easy_certificate, checkpoint=path, resume=True)
    assert resumed["verified"]
    assert resumed == verify_pressure_triangle(easy_certificate)
    assert verify_pressure_triangle(easy_certificate, independent=False)["verified"]
    changed = copy.deepcopy(saved)
    changed["certificate_sha256"] = "0" * 64
    path.write_text(json.dumps(changed))
    with pytest.raises(ValueError, match="certificate differs"):
        verify_pressure_triangle(easy_certificate, checkpoint=path, resume=True)


def test_new_schema_does_not_reinterpret_legacy_artifact():
    old = ROOT / "problems/number-theory/riemann-hypothesis/experiments/EXP-002-short-interval-stability/artifacts/triangle-certificate.json"
    with pytest.raises(ValueError, match="schema"):
        verify_pressure_triangle(json.loads(old.read_text()))
    assert SCHEMA != "riemann-triangle-v1"


def test_fully_forged_completed_replay_prefix_cannot_bypass_arithmetic(tmp_path, easy_certificate):
    path = tmp_path / "forged.json"
    ctx.prec = 256
    false = modified(easy_certificate, tree="V", nodes=1, validated_leaves=1, pressure_leaves=0)
    with pytest.raises(TimeoutError):
        verify_pressure_triangle(false, checkpoint=path, budget=0)
    saved = json.loads(path.read_text())
    saved.update(tree="V", pending=[], counts={"nodes": 1, "validated_leaves": 1, "pressure_leaves": 0},
                 tree_sha256=hashlib.sha256(b"V").hexdigest(), certificate_sha256=digest(false))
    path.write_text(json.dumps(saved))
    with pytest.raises(ValueError, match="Uncertified"):
        verify_pressure_triangle(false, checkpoint=path, resume=True)


def test_restoration_work_is_inside_replay_budget(tmp_path, easy_certificate):
    path = tmp_path / "done.json"
    verify_pressure_triangle(easy_certificate, independent=False, checkpoint=path)
    with pytest.raises(TimeoutError, match="restoration"):
        verify_pressure_triangle(easy_certificate, independent=False, checkpoint=path, resume=True, budget=0)
