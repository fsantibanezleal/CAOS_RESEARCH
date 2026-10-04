"""Corrupt actual proof, arithmetic and publication evidence, not synthetic proofs."""
import copy
import json
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "data-pipeline"))
from researchlab.stages import riemann_moment  # noqa: E402


@pytest.fixture(scope="module")
def inputs():
    return {role: subprocess.check_output(["git", "show", f"HEAD:{path}"], cwd=ROOT)
            for role, path in riemann_moment.INPUTS.items()}


def test_actual_reviewed_moment(inputs):
    data = riemann_moment.validate(inputs)
    assert data["onset"] == "0.527" and data["previous_onset"] == "0.5339"
    assert data["charged_exponents"] == ["-51/12500", "-6711/40000"]
    assert data["arithmetic_alone_proves_theorem"] is False
    assert data["external_peer_review"] is False


@pytest.mark.parametrize("role", list(riemann_moment.INPUTS))
def test_missing_real_source_rejected(inputs, role):
    raw = copy.copy(inputs)
    raw.pop(role)
    with pytest.raises(ValueError):
        riemann_moment.validate(raw)


@pytest.mark.parametrize("role", ["moment_mellin", "moment_review_text", "moment_detector", "moment_paper"])
def test_changed_real_source_rejected(inputs, role):
    raw = copy.copy(inputs)
    raw[role] += b"changed"
    with pytest.raises(ValueError, match="committed source bytes"):
        riemann_moment.validate(raw)


@pytest.mark.parametrize("key,value", [
    ("analytic_moment_reviewed", False), ("compact_window_loss_charged", False),
    ("external_peer_review", True), ("theta", "267/500"), ("eta", "0"),
    ("charged_exponents", ["0", "-6711/40000"]), ("simple_density_floor", "1"),
])
def test_false_analytic_or_arithmetic_review_rejected(inputs, key, value):
    raw = copy.copy(inputs)
    review = json.loads(raw["moment_review"])
    review[key] = value
    raw["moment_review"] = json.dumps(review).encode()
    import hashlib
    delivery = json.loads(raw["moment_delivery"])
    delivery["source_sha256"]["moment_review"] = hashlib.sha256(raw["moment_review"]).hexdigest()
    raw["moment_delivery"] = json.dumps(delivery).encode()
    with pytest.raises(ValueError):
        riemann_moment.validate(raw)


def test_unpublished_and_incomplete_receipts_rejected_even_when_rebound(inputs):
    import hashlib
    for role, key, value in [("moment_publication", "status", "draft"),
                             ("moment_archive", "members", 84),
                             ("moment_independent", "passed_conditional_controls", False),
                             ("moment_frequency", "analytic_moment_theorem_proved", True)]:
        raw = copy.copy(inputs)
        receipt = json.loads(raw[role])
        receipt[key] = value
        raw[role] = json.dumps(receipt).encode()
        delivery = json.loads(raw["moment_delivery"])
        delivery["source_sha256"][role] = hashlib.sha256(raw[role]).hexdigest()
        raw["moment_delivery"] = json.dumps(delivery).encode()
        with pytest.raises(ValueError):
            riemann_moment.validate(raw)


def test_omitted_collision_cost_rejected_even_when_both_reviews_rebound(inputs):
    import hashlib
    raw = copy.copy(inputs)
    receipt = json.loads(raw["moment_adversarial"])
    receipt["audit"]["negative_controls"]["omitted_collisions"]["true_normalized_mass"] = 6
    raw["moment_adversarial"] = json.dumps(receipt).encode()
    digest = hashlib.sha256(raw["moment_adversarial"]).hexdigest()
    review = json.loads(raw["moment_review"])
    key = riemann_moment.ANALYTIC_ROLES["moment_adversarial"]
    review["source_sha256"][key] = review["source_lf_sha256"][key] = digest
    raw["moment_review"] = json.dumps(review).encode()
    delivery = json.loads(raw["moment_delivery"])
    for role in ("moment_review", "moment_adversarial"):
        delivery["source_sha256"][role] = hashlib.sha256(raw[role]).hexdigest()
    raw["moment_delivery"] = json.dumps(delivery).encode()
    with pytest.raises(ValueError, match="adversarial negative controls"):
        riemann_moment.validate(raw)
