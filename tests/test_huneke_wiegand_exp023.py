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
    / "EXP-023-one-cubic-defining-ideal"
)


def load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, EXP / filename)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


RUN = load_module("hw_exp023_run", "run.py")
AUDIT = load_module("hw_exp023_audit", "audit.py")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_cumulative_offset_bases() -> None:
    for p in (4, 7):
        expected_dimensions = (1, 10 * p, 22 * p, 24 * p - 1, 24 * p, 24 * p)
        assert tuple(len(RUN.basis(p, degree)) for degree in range(6)) == expected_dimensions
        assert RUN.basis(p, 2) == (
            set(range(0, 2 * p + 1))
            | set(range(3 * p, 5 * p - 1))
            | set(range(6 * p, 24 * p))
        )
        assert RUN.basis(p, 3) == set(range(24 * p)) - {6 * p - 1}
        assert RUN.basis(p, 4) == set(range(24 * p))


def test_parameter_four_has_exact_one_cubic_profile() -> None:
    row = RUN.analyze_parameter(4)
    assert row["first_betti_row_degrees_2_to_5"] == {
        "2": 732,
        "3": 1,
        "4": 0,
        "5": 0,
    }
    assert row["minimal_equation_count"] == 733
    assert row["degree_rows"][0]["first_obstruction"]["total"] == 12
    assert all(row["predictions"].values())
    assert all(row["controls"].values())


def test_independent_total_graph_agrees_at_parameter_four() -> None:
    rebuilt = AUDIT.rebuild(4)
    assert rebuilt["first_betti_row_degrees_2_to_5"] == {
        "2": 732,
        "3": 1,
        "4": 0,
        "5": 0,
    }
    assert rebuilt["exceptional_cubic_total"] == 12
    assert rebuilt["degree_rows"][0]["exceptional_nonzero_totals"] == {"12": 2}
    assert all(row["first_invalid_component"] is None for row in rebuilt["degree_rows"])


def test_persisted_campaign_and_symbolic_certificate_are_internally_complete() -> None:
    campaign_path = EXP / "artifacts" / "results.json"
    audit_path = EXP / "artifacts" / "audit.json"
    certificate_path = EXP / "artifacts" / "symbolic-certificate.json"
    campaign = json.loads(campaign_path.read_text(encoding="utf-8"))
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    certificate = json.loads(certificate_path.read_text(encoding="utf-8"))

    hashes, parameters = AUDIT.verify_campaign(campaign)
    assert len(hashes) == 20
    assert sorted(parameters) == list(range(4, 24))
    assert campaign["campaign_aggregate"] == (
        "d23792c47a2e07785a27ebc71e99619705f7aa53a38ebe7f66ffa03b0518ce83"
    )
    assert audit["status"] == "INDEPENDENT_AUDIT_PASS"
    assert audit["campaign_file_sha256"] == sha256(campaign_path)
    assert certificate["status"] == "SYMBOLIC_CERTIFICATE_PASS"
    assert certificate["leaf_query_count"] == 133
    assert certificate["all_leaf_results"] == "unsat"
    assert all(leaf["result"] == "unsat" for leaf in certificate["leaves"])
    assert certificate["query_aggregate"] == (
        "832c8421fe66359b8c246e3465e27de6ea7829215f892ab815e72b1f44787194"
    )


def test_canonical_artifact_hashes() -> None:
    expected = {
        "results.json": "e91a4e6acd9bbc243642c028eaba755b3cebf1a647f162634e579e6598944f44",
        "audit.json": "30deabe2aceb1791f2fe8458c7c78ffa2db6da3c87586cf1932545d7cae62180",
        "symbolic-certificate.json": (
            "c2dd364126eb059f22c9356d4b99d0b4ae8a2c54db5e1dbff1d0ebfc43a48a6d"
        ),
        "attempt-1-budget-checkpoint.json": (
            "94010d659afebdff99cd66e337d36d28bedbbca9e6b467f837ac1c6d19fca486"
        ),
    }
    for filename, expected_hash in expected.items():
        assert sha256(EXP / "artifacts" / filename) == expected_hash
