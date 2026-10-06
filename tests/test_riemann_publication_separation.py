"""Reject misplaced files and broken links using actual publication receipts."""
import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "data-pipeline"))
from researchlab.stages.riemann_publication import admit  # noqa: E402


@pytest.fixture(params=["short-interval-levinson/versions/v0.02", "distinct-zero-gram"])
def published(request):
    folder = "manuscripts/riemann-hypothesis/" + request.param

    def read(name):
        return subprocess.check_output(["git", "show", f"HEAD:{folder}/{name}"], cwd=ROOT)

    return (json.loads(read("publication-receipt.json")), json.loads(read("current-publication.json")),
            json.loads(read("evidence-companion.json")), read("main.pdf"))


def check(history, manuscript, companion, pdf):
    return admit(history, json.dumps(manuscript).encode(), json.dumps(companion).encode(), pdf)


def test_real_publications_preserve_pdf_and_separate_all_archives(published):
    current, companion = check(*published)
    assert len(current["files"]) == 1
    assert companion["record_id"] != current["record_id"]
    assert all(f["name"].endswith(".zip") for f in companion["files"])


@pytest.mark.parametrize("case", ["mixed", "no-pdf", "wrong-doi", "changed-pdf", "wrong-pdf-url",
                                     "same-record", "wrong-link", "wrong-version", "wrong-type",
                                     "no-relation", "missing-zip", "changed-zip", "old-zip-url",
                                     "unverified-zip", "pdf-in-companion", "draft"])
def test_packaging_or_preservation_corruption_rejected(published, case):
    history, p, c, pdf = copy.deepcopy(published)
    if case == "mixed":
        p["files"].append(c["files"][0])
    elif case == "no-pdf":
        p["files"] = []
    elif case == "wrong-doi":
        p["version_doi"] = c["doi"]
    elif case == "changed-pdf":
        pdf += b"changed"
    elif case == "wrong-pdf-url":
        p["files"][0]["url"] = c["files"][0]["url"]
    elif case == "same-record":
        c["record_id"] = p["record_id"]
    elif case == "wrong-link":
        c["manuscript_record"] = "22940291"
    elif case == "wrong-version":
        c["version"] = "9.99"
    elif case == "wrong-type":
        c["resource_type"] = "publication-preprint"
    elif case == "no-relation":
        p["metadata"]["related_identifiers"] = []
    elif case == "missing-zip":
        c["files"].pop()
    elif case == "changed-zip":
        c["files"][0]["sha256"] = "0" * 64
    elif case == "old-zip-url":
        c["files"][0]["url"] = c["files"][0]["url"].replace(c["record_id"], p["record_id"])
    elif case == "unverified-zip":
        c["files"][0]["live_bytes_verified"] = False
    elif case == "pdf-in-companion":
        c["files"].append(p["files"][0])
    elif case == "draft":
        c["status"] = "draft"
    with pytest.raises(ValueError):
        check(history, p, c, pdf)
