"""Adversarial replay gates against the actual completed evidence."""
import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "data-pipeline"))
from researchlab.stages import riemann_distinct  # noqa: E402


@pytest.fixture
def committed_inputs():
    return {role: subprocess.run(["git", "show", f"HEAD:{path}"], cwd=ROOT,
                                check=True, capture_output=True).stdout
            for role, (_, path) in riemann_distinct.INPUTS.items()}


def test_actual_completed_evidence(committed_inputs):
    result = riemann_distinct.validate(committed_inputs)
    assert result["local"]["fraction"] == "3997934614153/4775507750000"
    assert result["vector"]["fraction"] == "30945470743359/36955122080000"
    assert result["vector"]["external_local_formalization_rebuilt_here"] is False
    assert result["incomplete_experiments"] == ["019", "023"]


@pytest.mark.parametrize("role,key,value", [
    ("distinct_cover", "passed", False),
    ("distinct_transfer", "liminf_fraction", "1"),
    ("distinct_native", "completed_closed_cells", 61028),
    ("distinct_native", "budget_expired", True),
    ("distinct_archive", "extracted_stdlib_cover_audit", False),
    ("distinct_vector", "pressure_total", "6/1000"),
    ("distinct_vector", "external_local_formalization_rebuilt_here", True),
    ("distinct_publication", "passed", False),
])
def test_actual_receipt_corruption(committed_inputs, role, key, value):
    changed = copy.copy(committed_inputs)
    data = json.loads(changed[role])
    data[key] = value
    changed[role] = json.dumps(data).encode()
    with pytest.raises(ValueError):
        riemann_distinct.validate(changed)


def test_missing_shard_and_changed_external_source(committed_inputs):
    changed = copy.copy(committed_inputs)
    transfer = json.loads(changed["distinct_transfer"])
    transfer["reports_sha256"].pop("shard-095.json")
    changed["distinct_transfer"] = json.dumps(transfer).encode()
    with pytest.raises(ValueError, match="incomplete local cover"):
        riemann_distinct.validate(changed)
    changed = copy.copy(committed_inputs)
    changed["distinct_external_source"] += b"changed"
    with pytest.raises(ValueError, match="external source bytes"):
        riemann_distinct.validate(changed)


def test_unpublished_or_changed_pdf_rejected(committed_inputs):
    changed = copy.copy(committed_inputs)
    publication = json.loads(changed["distinct_publication"])
    publication["files"][1]["live_download_exact_match"] = False
    changed["distinct_publication"] = json.dumps(publication).encode()
    with pytest.raises(ValueError, match="published byte checks"):
        riemann_distinct.validate(changed)
    changed = copy.copy(committed_inputs)
    changed["distinct_paper"] += b"changed"
    with pytest.raises(ValueError, match="published PDF bytes"):
        riemann_distinct.validate(changed)
