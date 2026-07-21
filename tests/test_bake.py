"""The export stage bakes valid CONTRACT-2 artifacts (writes to a tmp tree, never canonical)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "data-pipeline"))

from researchlab.stages import export_registry  # noqa: E402


def test_bake_writes_valid_registry(tmp_path, monkeypatch):
    monkeypatch.setattr(export_registry, "DERIVED", tmp_path / "derived")
    monkeypatch.setattr(export_registry, "MANIFESTS", tmp_path / "derived" / "manifests")
    written = export_registry.run()
    assert written, "bake wrote nothing"
    idx = json.loads((tmp_path / "derived" / "manifests" / "index.json").read_text())
    assert {c["case_id"] for c in idx["cases"]} == {"portfolio", "experiments", "jacobian"}
    for c in idx["cases"]:
        man = json.loads((tmp_path / "derived" / c["manifest_path"]).read_text())
        art = tmp_path / "derived" / man["artifact"]["path"]
        assert art.exists() and art.stat().st_size == man["artifact"]["bytes"]
        assert man["gate"]["lane"] == man["lane"] == "precompute"
    exps = json.loads((tmp_path / "derived" / "research" / "experiments.json").read_text())
    assert len(exps["experiments"]) >= 12
    jac = json.loads((tmp_path / "derived" / "research" / "jacobian.json").read_text())
    assert jac["map"]["det"] == -2 and len(jac["family"]) == 5
