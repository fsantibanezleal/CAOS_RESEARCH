import hashlib
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXP = (
    ROOT
    / "problems"
    / "commutative-algebra"
    / "huneke-wiegand"
    / "experiments"
    / "EXP-024-extremal-betti-data"
)


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, EXP / filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


RUN = load_module("hw_exp024_run", "run.py")
AUDIT = load_module("hw_exp024_audit", "audit.py")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_parameter_four_exact_edge_data() -> None:
    row = RUN.analyze_parameter(4)
    assert row["variable_count"] == 40
    assert row["codimension"] == 39
    assert row["projective_dimension"] == 39
    assert row["regularity"] == 4
    assert row["first_betti"] == {"beta_1_2": 732, "beta_1_3": 1}
    assert set(row["linear_first_syzygies"].values()) == {17896}
    assert row["last_betti_row_nonzero_entries"] == [
        {"homological_degree": 39, "internal_degree": 41, "rank": 40, "socle_degree": 2},
        {"homological_degree": 39, "internal_degree": 43, "rank": 1, "socle_degree": 4},
    ]
    assert row["penultimate_extremal"] == {
        "homological_degree": 38,
        "internal_degree": 42,
        "rank": 32,
    }
    assert row["canonical_module_minimal_generator_degrees"] == {"-3": 1, "-1": 40}
    assert all(row["comparisons"].values())
    assert all(row["controls"].values())
    assert row["interior_betti_table_determined"] is False


def test_closed_linear_syzygy_formula_is_integral() -> None:
    for p in range(4, 301):
        value = RUN.beta_2_3_closed(p)
        assert value == AUDIT.rebuild(p)["beta_2_3"]


def test_persisted_campaign_and_audit() -> None:
    campaign_path = EXP / "artifacts" / "results.json"
    audit_path = EXP / "artifacts" / "audit.json"
    checkpoint_path = EXP / "artifacts" / "checkpoint.json"
    campaign = json.loads(campaign_path.read_text(encoding="utf-8"))
    audit = json.loads(audit_path.read_text(encoding="utf-8"))

    rows = AUDIT.verify_campaign(campaign)
    assert sorted(rows) == list(range(4, 301))
    assert audit["status"] == "INDEPENDENT_AUDIT_PASS"
    assert audit["campaign_file_sha256"] == sha256(campaign_path)
    assert audit["checkpoint_file_sha256"] == sha256(checkpoint_path)
    assert audit["selected_parameters"] == [4, 5, 17, 73, 151, 300]
    assert all(audit["controls"].values())
    assert audit["premise_sha256"] == RUN.PREMISE_SHA256


def test_smoke_and_checkpoint_are_complete() -> None:
    smoke = json.loads((EXP / "artifacts" / "smoke-p4.json").read_text(encoding="utf-8"))
    checkpoint = json.loads((EXP / "artifacts" / "checkpoint.json").read_text(encoding="utf-8"))
    assert smoke["range"] == {"first": 4, "last": 4, "count": 1}
    assert smoke["rows"][0]["linear_first_syzygies"]["closed_formula"] == 17896
    assert checkpoint["status"] == "COMPLETE"
    assert checkpoint["range"] == {"first": 4, "last": 300}
    assert checkpoint["completed_through"] == 300
    assert len(checkpoint["row_hashes"]) == 297


def test_canonical_artifact_hashes() -> None:
    expected = {
        "smoke-p4.json": "492f6f8171412efa040e77d887168a098b634d7d4e083052d0a98a41e91563d0",
        "smoke-p4-checkpoint.json": (
            "a4dee7cbf8cf8556e7377727fe15efcad71b5401dacbc197970666023807ff06"
        ),
        "results.json": "30cefcb20edaeca931f471a781db9f7fb2da5796ed77dce61f6a8dfb609807e9",
        "checkpoint.json": "fb7e7dab64f47832f8d065469e9dba815c4439d18b2b05ec68b1be45549ffd3f",
        "audit.json": "4f39aa61b11c05c3ab73e58265f988196ffefa602b1512d5d9aefa76aacb20a9",
    }
    for filename, expected_hash in expected.items():
        assert sha256(EXP / "artifacts" / filename) == expected_hash
