"""Replay the Riemann certificate and reject malformed coverage and arithmetic claims."""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from fractions import Fraction
from pathlib import Path

import pytest
from flint import arb, ctx

ROOT = Path(__file__).resolve().parents[1]
PROBLEM = ROOT / "problems/number-theory/riemann-hypothesis"
sys.path.insert(0, str(PROBLEM / "code"))
from riemann_certificates import (  # noqa: E402
    ball,
    certify_triangle,
    kernel,
    sinc_series,
    verify_triangle,
)


@pytest.fixture(autouse=True)
def high_precision():
    previous = ctx.prec
    ctx.prec = 256
    yield
    ctx.prec = previous


@pytest.fixture(scope="module")
def small_certificate():
    previous = ctx.prec
    try:
        ctx.prec = 160
        return certify_triangle(Fraction(3, 4), Fraction(1), Fraction(1, 10))
    finally:
        ctx.prec = previous


def _modified(certificate, **updates):
    candidate = copy.deepcopy(certificate)
    candidate.update(updates)
    candidate["tree_sha256"] = hashlib.sha256(candidate["tree"].encode()).hexdigest()
    return candidate


@pytest.mark.parametrize(
    "updates,reason",
    [
        ({"tree": "O", "nodes": 1, "energy_leaves": 0, "outside_leaves": 1}, "intersects"),
        ({"tree": "E", "nodes": 1, "energy_leaves": 1, "outside_leaves": 0}, "Uncertified"),
        ({"unresolved_boxes": 1}, "Incomplete"),
        ({"theta": "1"}, "parameters"),
        ({"theta": "0"}, "parameters"),
        ({"radius": "-1"}, "parameters"),
        ({"threshold": "0"}, "parameters"),
        ({"threshold": "2"}, "parameters"),
        ({"tree": "?"}, "Unknown"),
    ],
)
def test_rejects_false_domain_and_energy_claims(small_certificate, updates, reason):
    with pytest.raises(ValueError, match=reason):
        verify_triangle(_modified(small_certificate, **updates))


def test_rejects_missing_or_trailing_partition_nodes(small_certificate):
    tree = small_certificate["tree"]
    with pytest.raises(ValueError, match="Incomplete"):
        verify_triangle(_modified(small_certificate, tree=tree[:-1]))
    with pytest.raises(ValueError, match="Trailing"):
        verify_triangle(_modified(small_certificate, tree=tree + "E"))


def test_rejects_digest_and_count_corruption(small_certificate):
    damaged = copy.deepcopy(small_certificate)
    damaged["tree_sha256"] = "0" * 64
    with pytest.raises(ValueError, match="hash mismatch"):
        verify_triangle(damaged)
    for field in ("nodes", "energy_leaves", "outside_leaves"):
        with pytest.raises(ValueError, match="count mismatch"):
            verify_triangle(_modified(small_certificate, **{field: small_certificate[field] + 1}))


def test_rejects_inflated_arithmetic_threshold(small_certificate):
    with pytest.raises(ValueError, match="Uncertified"):
        verify_triangle(_modified(small_certificate, threshold="1"))


def test_checkpoint_resume_is_identical_and_fail_closed(tmp_path, capsys):
    checkpoint = tmp_path / "checkpoint.json"
    spec = (Fraction(3, 4), Fraction(1), Fraction(1, 10))
    with pytest.raises(TimeoutError, match="unresolved"):
        certify_triangle(*spec, max_nodes=1, checkpoint=checkpoint, progress_every=1)
    saved = json.loads(checkpoint.read_text())
    assert saved["pending"]
    assert saved["counts"]["nodes"] == 1
    assert saved["tree"] == "B"
    assert '"event": "progress"' in capsys.readouterr().out
    resumed = certify_triangle(*spec, checkpoint=checkpoint, resume=True)
    fresh = certify_triangle(*spec)
    assert resumed == fresh
    assert not json.loads(checkpoint.read_text())["pending"]
    assert verify_triangle(resumed, independent=False)["verified"]
    assert verify_triangle(resumed, independent=True)["verified"]
    with pytest.raises(ValueError, match="parameters differ"):
        certify_triangle(Fraction(3, 4), Fraction(2), Fraction(1, 10),
                         checkpoint=checkpoint, resume=True)


def test_sinc_zero_and_removable_cosine_kernel_points():
    theta = Fraction(3, 4)
    a = ball(theta) / arb(2).sqrt()
    assert sinc_series(arb(0)) == 1
    assert kernel(theta, Fraction(0)).contains(1)
    assert kernel(theta, Fraction(0), independent=True).contains(1)
    # X=a is the removable Fourier singularity, not a zero. Evaluate its
    # independent analytic limit rather than divide a zero-containing ball.
    expected = (a / a.sin() + a.cos()) / 2
    native = (arb(0).sinc() + (2 * a).sinc()) / (2 * a.sinc())
    taylor = (sinc_series(arb(0)) + sinc_series(2 * a)) / (2 * sinc_series(a))
    assert expected > 0
    assert expected.overlaps(native)
    assert expected.overlaps(taylor)


@pytest.mark.parametrize("point", [Fraction(1, 10), Fraction(1, 3), Fraction(7, 3), Fraction(21, 4)])
def test_sinc_kernel_matches_closed_formula_away_from_singularities(point):
    theta = Fraction(3, 4)
    a = ball(theta) / arb(2).sqrt()
    x = arb.pi() * ball(theta) * ball(point)
    denominator = 1 - x * x / (a * a)
    assert not denominator.contains(0)
    direct = (x.cos() - x * a.cos() * x.sin() / (a * a.sin())) / denominator
    assert direct.overlaps(kernel(theta, point))
    assert direct.overlaps(kernel(theta, point, independent=True))
    assert kernel(theta, -point).overlaps(kernel(theta, point))


def test_full_committed_certificate_replays_with_separate_sinc_evaluator():
    artifact = PROBLEM / "experiments/EXP-002-short-interval-stability/artifacts/triangle-certificate.json"
    certificate = json.loads(artifact.read_text())
    result = verify_triangle(certificate, independent=True)
    assert result["verified"]
    assert result["independent_sinc_taylor"]
    assert result["nodes"] == certificate["nodes"]

