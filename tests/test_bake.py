"""The export stage bakes valid CONTRACT-2 artifacts (writes to a tmp tree, never canonical)."""
import json
import hashlib
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "data-pipeline"))

from researchlab.stages import export_registry  # noqa: E402


def test_bake_writes_valid_registry(tmp_path, monkeypatch):
    monkeypatch.setattr(export_registry, "DERIVED", tmp_path / "derived")
    monkeypatch.setattr(export_registry, "MANIFESTS", tmp_path / "derived" / "manifests")
    written = export_registry.run()
    assert written, "bake wrote nothing"
    assert all(b"\r\n" not in path.read_bytes() for path in written)
    idx = json.loads((tmp_path / "derived" / "manifests" / "index.json").read_text())
    assert {c["case_id"] for c in idx["cases"]} == {
        "portfolio", "experiments", "jacobian", "riemann",
    }
    for c in idx["cases"]:
        man = json.loads((tmp_path / "derived" / c["manifest_path"]).read_text())
        art = tmp_path / "derived" / man["artifact"]["path"]
        assert art.exists() and art.stat().st_size == man["artifact"]["bytes"]
        assert hashlib.sha256(art.read_bytes()).hexdigest() == man["artifact"]["sha256"]
        assert man["gate"]["lane"] == man["lane"] == "precompute"
    exps = json.loads((tmp_path / "derived" / "research" / "experiments.json").read_text())
    assert len(exps["experiments"]) >= 12
    jac = json.loads((tmp_path / "derived" / "research" / "jacobian.json").read_text())
    assert jac["map"]["det"] == -2 and len(jac["family"]) == 5
    riemann = json.loads((tmp_path / "derived" / "research" / "riemann.json").read_text())
    manifest = json.loads((tmp_path / "derived" / "manifests" / "riemann.json").read_text())
    assert manifest["sources"] == riemann["provenance"]
    assert {p["source_exp"] for p in manifest["sources"]} == {
        "EXP-001-source-and-constant-audit", "EXP-002-short-interval-stability", "source-review",
        "EXP-003-odd-frame-pressure",
        "EXP-004-parity-density-transfer",
        "EXP-005-local-selberg-transfer",
        "EXP-006-hilbert-parity-compression",
        "EXP-007-spectral-defect-parity",
        "EXP-008-rank-six-local-transfer",
    }
    assert riemann["schema"] == "riemann-replay-v7"


@pytest.fixture
def committed_riemann(tmp_path, monkeypatch):
    """An isolated Git source demonstrates that dirty files never become public evidence."""
    monkeypatch.setattr(export_registry, "RIEMANN_EXPERIMENT_MAX", 6)
    def git(*args):
        return subprocess.run(
            ["git", *args], cwd=tmp_path, check=True, capture_output=True,
        ).stdout

    git("init", "--quiet")
    problem = tmp_path / "problems/number-theory/riemann-hypothesis"
    exp_one = problem / "experiments/EXP-001-source-and-constant-audit"
    exp_two = problem / "experiments/EXP-002-short-interval-stability"
    exp_three = problem / "experiments/EXP-003-odd-frame-pressure"
    exp_four = problem / "experiments/EXP-004-parity-density-transfer"
    exp_five = problem / "experiments/EXP-005-local-selberg-transfer"
    exp_six = problem / "experiments/EXP-006-hilbert-parity-compression"
    files = {
        exp_one / "artifacts/result.json": {"status": "PASS"},
        exp_two / "artifacts/result.json": {
            "audit": {"verified": True, "independent_sinc_taylor": True},
        },
        exp_two / "artifacts/triangle-certificate.json": {"tree": "E"},
        exp_two / "artifacts/exploration.json": {"rows": []},
        exp_two / "mathematical-proof.md": "# A committed proof\n",
        exp_two / "verdict.md": "# A committed verdict\n",
        problem / "context/source-manifest.json": {"reviewed_on": "2026-09-12"},
        exp_three / "mathematical-proof.md": "# The committed odd-frame proof\n",
        exp_three / "verdict.md": "# EXP-003 verdict: confirmed\n",
        exp_three / "adversarial-audit.md": "# The committed adversarial audit\n",
        exp_three / "hypothesis.md": "# The declaration\n",
        exp_three / "artifacts/candidates.json": {"candidates": []},
        exp_three / "run.py": "# The declared runner\n",
        exp_three / "explore.py": "# The bounded design pass\n",
        problem / "code/riemann_pressure.py": "# Pressure checker\n",
        problem / "code/riemann_certificates.py": "# Legacy checker\n",
        exp_four / "hypothesis.md": "# Frozen parity declaration\n",
        exp_four / "run.py": "# Parity runner fixture, not a research calculation\n",
        exp_four / "mathematical-proof.md": "# Reviewed parity proof fixture\n",
        exp_four / "adversarial-audit.md": "# Reviewed parity audit fixture\n",
        exp_four / "verdict.md": "# EXP-004 verdict: confirmed\n",
        exp_four / "artifacts/symbolic.json": {"fixture": "symbolic"},
        exp_four / "artifacts/census.jsonl": "[0,0]\n",
        exp_four / "artifacts/relaxation.json": {"fixture": "relaxation"},
        exp_four / "artifacts/sharpness.json": {"fixture": "sharpness"},
        problem / "context/2026-09-12-critical-mass-and-multiplicity-route.md": "# Classical seed fixture\n",
        problem / "context/2026-09-12-parity-transfer-adversarial-audit.md": "# Independent preflight fixture\n",
        problem / "context/2026-09-12-wang-transfer-audit.md": "# Arithmetic transfer fixture\n",
        exp_five / "hypothesis.md": "# Frozen local Selberg declaration\n",
        exp_five / "run.py": "# Local Selberg exact runner fixture\n",
        exp_five / "mathematical-proof.md": "# Reviewed localization proof fixture\n",
        exp_five / "adversarial-audit.md": "# Reviewed localization audit fixture\n",
        exp_five / "verdict.md": "# EXP-005 verdict: confirmed\n",
        exp_six / "hypothesis.md": "# Frozen Hilbert declaration\nQ(N-O)\n0.5458<theta<0.5459\n",
        exp_six / "run.py": "# Hilbert parity exact runner fixture\n",
        exp_six / "mathematical-proof.md": "# Reviewed Hilbert parity proof fixture\n",
        exp_six / "adversarial-audit.md": "# Reviewed Hilbert parity audit fixture\n",
        exp_six / "verdict.md": "# EXP-006 verdict: confirmed\n",
        tmp_path / "tests/test_riemann_hilbert_parity.py": "# Focused Hilbert parity tests\n",
    }
    for path, content in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content if isinstance(content, str) else json.dumps(content),
                        encoding="utf-8", newline="\n")

    def checksum(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    (exp_three / "artifacts/candidates.json").write_text(json.dumps({"candidates": [],
        "exploration_source_sha256": checksum(exp_three / "explore.py"),
        "prior_exploration_sha256": checksum(exp_two / "artifacts/exploration.json")}), encoding="utf-8")

    source_identity = {
        "hypothesis": {"sha256": checksum(exp_three / "hypothesis.md")},
        "certificate_code": {name: checksum(problem / "code" / name)
                             for name in ("riemann_pressure.py", "riemann_certificates.py")},
        "runner_sha256": checksum(exp_three / "run.py"),
        "reused_certificate": {"sha256": checksum(exp_two / "artifacts/triangle-certificate.json")},
    }
    (exp_three / "artifacts/result.json").write_text(json.dumps({
        "schema": "riemann-exp003-results-v1",
        "stage_a": {"arithmetic_status": "verified", "provenance": source_identity,
                    "replay": {"verified": True, "independent_sinc_taylor": True}},
        "stage_b": {"arithmetic_status": "not_confirmed", "outcomes": [],
                    "candidate_list_sha256": checksum(exp_three / "artifacts/candidates.json")},
    }), encoding="utf-8")

    def commit():
        git("add", ".")
        git("-c", "user.name=Replay test", "-c", "user.email=replay@example.invalid",
            "commit", "--quiet", "-m", "Fixture source")

    commit()
    declaration = git("rev-parse", "HEAD").decode().strip()
    monkeypatch.setattr(export_registry, "EXP004_DECLARATION", declaration)
    monkeypatch.setattr(export_registry, "EXP005_DECLARATION", declaration)
    monkeypatch.setattr(export_registry, "EXP005_CANONICAL", "fixture-canonical")
    monkeypatch.setattr(export_registry, "EXP006_DECLARATION", declaration)
    monkeypatch.setattr(export_registry, "EXP006_CANONICAL", "fixture-hilbert-canonical")
    premise_names = (
        "context/2026-09-12-critical-mass-and-multiplicity-route.md",
        "context/2026-09-12-parity-transfer-adversarial-audit.md",
        "context/2026-09-12-wang-transfer-audit.md",
        "experiments/EXP-003-odd-frame-pressure/mathematical-proof.md",
    )

    def source(path):
        return {"path": path.relative_to(tmp_path).as_posix(), "sha256": checksum(path),
                "source_commit": declaration}

    parity = {
        "schema": "riemann-exp004-results-v1", "experiment": exp_four.name,
        "arithmetic_status": "verified",
        "provenance": {
            "declaration_commit": declaration, "hypothesis": source(exp_four / "hypothesis.md"),
            "runner": source(exp_four / "run.py"),
            "inputs": [source(problem / name) for name in premise_names],
        },
        "symbolic": {"residual_identities": 2, "multiplicity_regression_cases": 24},
        "census": {"vectors": 19683, "sigma_evaluations": 59049, "sigma_values": [0, 1, 2]},
        "relaxation": {"cases": 42}, "sharpness": {"cases": 36},
        "threshold": {
            "alpha": "51/100", "derivative_cap": "10000/2601", "c_alpha_upper": "-1801/20400",
            "derivative_formula_verified": True, "c_alpha_upper_negative": True,
            "classical_a": None, "kappa": None, "theta0_numeric": None, "theta1_decimal": None,
        },
        "proof_status": {"all_height_theorem": "Not proved by this computational runner"},
    }
    for section in ("symbolic", "census", "relaxation", "sharpness"):
        filename = f"{section}.jsonl" if section == "census" else f"{section}.json"
        parity[section].update(raw_artifact=filename, sha256=checksum(exp_four / "artifacts" / filename))
    _write_json(exp_four / "artifacts/result.json", parity)
    role_paths = {
        "parity_result": exp_four / "artifacts/result.json",
        "parity_hypothesis": exp_four / "hypothesis.md",
        "parity_proof": exp_four / "mathematical-proof.md",
        "parity_audit": exp_four / "adversarial-audit.md",
        "parity_verdict": exp_four / "verdict.md",
    }
    _write_json(exp_four / "proof-review.json", {
        "schema": "riemann-exp004-proof-review-v1", "declaration_commit": declaration,
        "scientific_verdict": "confirmed", "universal_finite_proof_reviewed": True,
        "asymptotic_transfer_reviewed": True, "numerical_exponent_claimed": False,
        "source_sha256": {role: checksum(path) for role, path in role_paths.items()},
    })
    def exact(numerator, denominator=1):
        return {
            "numerator": str(numerator), "denominator": str(denominator),
            "decimal": str(Decimal(numerator) / Decimal(denominator)),
        }
    checks = {
        name: True for name in (
            "baseline_negative", "boundary_rejected", "c3_interval_ordered",
            "curve_simple_positive", "e_interval", "fixed_u_simple_positive",
            "interval_contains_c", "interval_contains_curve", "interval_contains_fixed",
            "mollifier_below_quarter", "negative_theta_control", "source_hashes",
            "sqrt2_interval", "strict_localization_margin",
        )
    }
    local_result = {
        "schema": "riemann-exp005-results-v1", "status": "pass", "passed": True,
        "checks": checks,
        "claim_boundary": {"rh_solved": False},
        "boundary_control": {"accepted": False, "margin": exact(0), "u": exact(23, 1000)},
        "parameters": {
            "theta": exact(273, 500), "negative_control_theta": exact(5459, 10000),
            "mollifier_exponent_u": exact(2299, 100000), "simple_gate": exact(9, 100000),
        },
        "positive_point": {
            "fixed_u_simple_lower": exact(98, 1000000),
            "simple_curve_lower": exact(99, 1000000),
            "localization_exponent_margin": exact(2, 100000),
        },
        "negative_control": {"simple_curve_upper": exact(-1, 100000)},
        "source_constant": {"name": "C[q3]", "center": exact(656775, 1000000)},
        "execution_identity": {
            "head": "fixture-canonical", "tracked_clean_at_start": True,
            "hypothesis_sha256": checksum(exp_five / "hypothesis.md"),
            "run_py_sha256": checksum(exp_five / "run.py"),
        },
    }
    local_result_path = exp_five / "artifacts/canonical/result.json"
    local_result_path.parent.mkdir(parents=True, exist_ok=True)
    _write_json(local_result_path, local_result)
    local_result_sha = checksum(local_result_path)
    _write_json(exp_five / "artifacts/canonical/execution-receipt.json", {
        "schema": "riemann-exp005-execution-receipt-v1", "status": "pass",
        "result_sha256": local_result_sha,
        "git": {"head": "fixture-canonical", "tracked_clean_at_start": True},
    })
    local_roles = {
        "hypothesis": exp_five / "hypothesis.md",
        "mathematical_proof": exp_five / "mathematical-proof.md",
        "adversarial_audit": exp_five / "adversarial-audit.md",
        "result": local_result_path,
        "verdict": exp_five / "verdict.md",
    }
    _write_json(exp_five / "proof-review.json", {
        "schema": "riemann-exp005-proof-review-v1", "declaration_commit": declaration,
        "canonical_commit": "fixture-canonical", "scientific_verdict": "confirmed",
        "analytic_localization_reviewed": True, "exact_certificate_reviewed": True,
        "source_sha256": {role: checksum(path) for role, path in local_roles.items()},
    })
    # The real EXP-006 declaration was later amended after a consistency audit.
    # Keep that two-commit history in the fixture as well.
    (exp_six / "hypothesis.md").write_text(
        "# Frozen Hilbert declaration\nQ(N-O)\n0.5458<theta<0.5459\n"
        "## Audit strengthening after the declared prediction\n(Q-S)(N-O)\n",
        encoding="utf-8", newline="\n",
    )
    hilbert_checks = {name: True for name in (
        "c3_interval_ordered", "c6_interval_ordered", "e_interval",
        "finite_census", "finite_census_has_all_regimes",
        "independent_interval_contained", "old_linear_negative",
        "rank_six_sensitivity_stronger", "root_lower_negative",
        "root_monotone_conditions", "root_upper_positive",
        "scalar_headlines_allow_zero", "source_hashes", "sqrt2_interval",
        "strong_bound_improves_weak", "strong_bound_positive",
        "target_below_wang_root", "weak_bound_positive",
    )}
    hilbert_result = {
        "schema": "riemann-exp006-results-v2", "status": "pass", "passed": True,
        "checks": hilbert_checks,
        "claim_boundary": {"rh_solved": False},
        "parameters": {
            "theta": exact(5459, 10000), "root_lower_theta": exact(136471, 250000),
            "root_upper_theta": exact(109177, 200000), "simple_gate": exact(1, 100000),
        },
        "target": {
            "c_upper": exact(-1, 100), "old_linear_upper": exact(-1, 100000),
            "weak_simple_upper": exact(13, 1000000),
            "strong_simple_lower": exact(17, 1000000),
        },
        "root_bracket": {
            "lower": {"root_function_upper": exact(-1, 1000000)},
            "upper": {"root_function_lower": exact(1, 1000000)},
        },
        "finite_census": {
            "cases": 18479, "equality_cases": 135, "strict_cases": 18340,
            "empty_dimension_cases": 4,
        },
        "scalar_headline_barrier": {"passed": True, "checks": {"witness": True}},
        "execution_identity": {
            "head": "fixture-hilbert-canonical", "tracked_clean_at_start": True,
            "hypothesis_sha256": checksum(exp_six / "hypothesis.md"),
            "run_py_sha256": checksum(exp_six / "run.py"),
        },
    }
    hilbert_result_path = exp_six / "artifacts/canonical/result.json"
    hilbert_result_path.parent.mkdir(parents=True, exist_ok=True)
    _write_json(hilbert_result_path, hilbert_result)
    hilbert_result_sha = checksum(hilbert_result_path)
    _write_json(exp_six / "artifacts/canonical/execution-receipt.json", {
        "schema": "riemann-exp006-execution-receipt-v1", "status": "pass",
        "result_sha256": hilbert_result_sha,
        "git": {"head": "fixture-hilbert-canonical", "tracked_clean_at_start": True},
    })
    hilbert_roles = {
        "hypothesis": exp_six / "hypothesis.md",
        "mathematical_proof": exp_six / "mathematical-proof.md",
        "adversarial_audit": exp_six / "adversarial-audit.md",
        "result": hilbert_result_path,
        "verdict": exp_six / "verdict.md",
        "runner": exp_six / "run.py",
        "focused_test": tmp_path / "tests/test_riemann_hilbert_parity.py",
    }
    _write_json(exp_six / "proof-review.json", {
        "schema": "riemann-exp006-proof-review-v1", "declaration_commit": declaration,
        "canonical_commit": "fixture-hilbert-canonical", "scientific_verdict": "confirmed",
        "analytic_transfer_reviewed": True, "exact_certificate_reviewed": True,
        "source_sha256": {role: checksum(path) for role, path in hilbert_roles.items()},
    })
    commit()
    monkeypatch.setattr(export_registry, "ROOT", tmp_path)
    return tmp_path, exp_two, git, commit


def _write_json(path, value):
    path.write_text(json.dumps(value, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def _rewrite_parity_result(exp_four, mutate, *, rebind_review=True):
    path = exp_four / "artifacts/result.json"
    value = json.loads(path.read_text(encoding="utf-8"))
    mutate(value)
    _write_json(path, value)
    if rebind_review:
        review_path = exp_four / "proof-review.json"
        review = json.loads(review_path.read_text(encoding="utf-8"))
        review["source_sha256"]["parity_result"] = hashlib.sha256(path.read_bytes()).hexdigest()
        _write_json(review_path, review)


def test_riemann_export_ignores_uncommitted_source_bytes(committed_riemann):
    root, exp_two, git, _ = committed_riemann
    result_file = exp_two / "artifacts/result.json"
    committed = result_file.read_bytes()
    source_commit = git("log", "-1", "--format=%H", "HEAD", "--",
                        result_file.relative_to(root).as_posix()).decode().strip()
    result_file.write_text('{"audit":{"verified":false}}', encoding="utf-8")
    (exp_two / "mathematical-proof.md").write_text("Unreviewed replacement", encoding="utf-8")
    payload = export_registry._riemann_payload()
    assert payload["result"]["audit"]["verified"] is True
    source = next(p for p in payload["provenance"] if p["role"] == "result")
    assert source["sha256"] == hashlib.sha256(committed).hexdigest()
    assert source["bytes"] == len(committed)
    assert source["source_commit"] == source_commit
    assert source["path"] == result_file.relative_to(root).as_posix()


def test_riemann_export_rejects_untracked_certificate(committed_riemann):
    root, exp_two, git, _ = committed_riemann
    certificate = exp_two / "artifacts/triangle-certificate.json"
    git("rm", "--cached", certificate.relative_to(root).as_posix())
    git("-c", "user.name=Replay test", "-c", "user.email=replay@example.invalid",
        "commit", "--quiet", "-m", "Remove certificate from committed evidence")
    assert certificate.is_file()
    with pytest.raises(subprocess.CalledProcessError):
        export_registry._riemann_payload()


def test_riemann_export_rejects_failed_recorded_crosscheck(committed_riemann):
    _, exp_two, _, commit = committed_riemann
    (exp_two / "artifacts/result.json").write_text(json.dumps({
        "audit": {"verified": True, "independent_sinc_taylor": False},
    }), encoding="utf-8")
    commit()
    with pytest.raises(ValueError, match="both recorded arithmetic checks"):
        export_registry._riemann_payload()


def test_pressure_export_ignores_worktree_replacement_and_binds_committed_code(committed_riemann):
    _, exp_two, _, commit = committed_riemann
    code = exp_two.parent.parent / "code/riemann_pressure.py"
    expected = export_registry._riemann_payload()["pressure_result"]
    code.write_text("# Unreviewed checker replacement\n", encoding="utf-8", newline="\n")
    assert export_registry._riemann_payload()["pressure_result"] == expected
    commit()
    with pytest.raises(ValueError, match="committed input differs: pressure_code"):
        export_registry._riemann_payload()


def test_pressure_export_rejects_a_verified_stage_without_a_winning_certificate(committed_riemann):
    _, exp_two, _, commit = committed_riemann
    result_file = exp_two.parent / "EXP-003-odd-frame-pressure/artifacts/result.json"
    value = json.loads(result_file.read_text(encoding="utf-8"))
    value["stage_b"]["arithmetic_status"] = "verified"
    result_file.write_text(json.dumps(value), encoding="utf-8")
    commit()
    with pytest.raises(ValueError, match="no complete certificate"):
        export_registry._riemann_payload()


def test_pressure_export_binds_frozen_candidates(committed_riemann):
    _, exp_two, _, commit = committed_riemann
    candidates = exp_two.parent / "EXP-003-odd-frame-pressure/artifacts/candidates.json"
    candidates.write_text('{"candidates":[{"pressure":"1/2","epsilon":"1/4"}]}', encoding="utf-8")
    commit()
    with pytest.raises(ValueError, match="candidate list differs"):
        export_registry._riemann_payload()


@pytest.mark.parametrize("tamper", ["none", "certificate", "audit", "strict_gain", "frozen_parameters"])
def test_pressure_export_requires_matching_complete_certificate(committed_riemann, tamper):
    _, exp_two, _, commit = committed_riemann
    exp_three = exp_two.parent / "EXP-003-odd-frame-pressure"
    result_file = exp_three / "artifacts/result.json"
    value = json.loads(result_file.read_text(encoding="utf-8"))
    certificate = {"theta": "3/4", "pressure": "1/100", "epsilon": "1/10", "cutoff": "10",
                   "tree": "V", "unresolved_boxes": 0}
    cert_file = exp_three / "artifacts/stage-b/candidate-1/pressure-certificate.json"
    cert_file.parent.mkdir(parents=True)
    cert_file.write_text(json.dumps(certificate), encoding="utf-8")
    identity = hashlib.sha256((json.dumps(certificate, sort_keys=True, separators=(",", ":")) + "\n").encode()).hexdigest()
    candidates = exp_three / "artifacts/candidates.json"
    candidate_record = json.loads(candidates.read_text(encoding="utf-8"))
    candidate_record["candidates"] = [{"pressure": "1/100", "epsilon": "1/10"}]
    candidates.write_text(json.dumps(candidate_record), encoding="utf-8")
    candidates_hash = hashlib.sha256(candidates.read_bytes()).hexdigest()
    winner = {"candidate": 1, "status": "arithmetic_verified", **certificate,
        "certificate_sha256": identity, "strict_gain_gate": {"lower": "1/100000"},
        "audit": {"verified": True, "independent_sinc_taylor": True, "certificate_sha256": identity},
        "provenance": {**value["stage_a"]["provenance"], "candidate_list_sha256": candidates_hash}}
    if tamper == "certificate":
        cert_file.write_text(json.dumps({**certificate, "unresolved_boxes": 1}), encoding="utf-8")
    elif tamper == "audit":
        winner["audit"]["independent_sinc_taylor"] = False
    elif tamper == "strict_gain":
        winner["strict_gain_gate"]["lower"] = "0"
    elif tamper == "frozen_parameters":
        winner["pressure"] = "1/99"
    value["stage_b"] = {"arithmetic_status": "verified", "outcomes": [winner],
                        "candidate_list_sha256": candidates_hash}
    result_file.write_text(json.dumps(value), encoding="utf-8")
    commit()
    if tamper == "none":
        payload = export_registry._riemann_payload()
        assert any(p["role"] == "pressure_certificate_1" for p in payload["provenance"])
    else:
        with pytest.raises(ValueError):
            export_registry._riemann_payload()


def test_riemann_modal_records_ignore_dirty_and_staged_only_files(committed_riemann):
    root, exp_two, git, _ = committed_riemann
    verdict = exp_two / "verdict.md"
    original = git("show", f"HEAD:{verdict.relative_to(root).as_posix()}").decode()
    artifact = exp_two / "artifacts/result.json"
    committed_size = len(git("show", f"HEAD:{artifact.relative_to(root).as_posix()}"))
    verdict.write_text("# An unreviewed claim", encoding="utf-8")
    artifact.write_text("{}", encoding="utf-8")
    extra = exp_two / "hypothesis.md"
    extra.write_text("# An uncommitted hypothesis", encoding="utf-8")
    git("add", extra.relative_to(root).as_posix())
    record, = [item for item in export_registry._read_experiments()
               if item["slug"] == exp_two.name]
    assert record["verdict_md"] == original
    assert record["hypothesis_md"] == ""
    assert next(a for a in record["artifacts"] if a["name"] == "result.json")["bytes"] == committed_size


@pytest.mark.parametrize("missing_directory", ["experiments", "problem"])
def test_riemann_modal_records_survive_deleted_worktree_directories(
    committed_riemann, missing_directory,
):
    root, exp_two, _, _ = committed_riemann
    original = export_registry._read_experiments()
    original_payload = export_registry._riemann_payload()
    source = exp_two.parent if missing_directory == "experiments" else exp_two.parent.parent
    destination = root / "removed-working-files"
    assert source.resolve().is_relative_to(root.resolve())
    assert destination.resolve().is_relative_to(root.resolve())
    source.rename(destination)
    assert export_registry._read_experiments() == original
    assert export_registry._riemann_payload() == original_payload


def test_parity_export_binds_all_evidence_without_promoting_runner_to_proof(committed_riemann):
    _, exp_two, _, _ = committed_riemann
    payload = export_registry._riemann_payload()
    assert payload["schema"] == "riemann-replay-v5"
    assert payload["parity_result"]["proof_status"]["all_height_theorem"].startswith("Not proved")
    assert payload["parity_review"]["scientific_verdict"] == "confirmed"
    assert payload["local_review"]["scientific_verdict"] == "confirmed"
    assert payload["local_result"]["positive_point"]["fixed_u_simple_lower"]["numerator"] == "98"
    sources = {item["role"]: item for item in payload["provenance"]}
    for section in ("symbolic", "census", "relaxation", "sharpness"):
        record = payload["parity_result"][section]
        assert sources[f"parity_{section}_raw"]["sha256"] == record["sha256"]
        assert sources[f"parity_{section}_raw"]["source_exp"] == "EXP-004-parity-density-transfer"
    assert len([role for role in sources if role.startswith("parity_premise_")]) == 4
    # Fixtures exercise binding only; these placeholder raw records are never
    # portrayed as a second execution or independent proof of the census.
    assert (exp_two.parent / "EXP-004-parity-density-transfer/artifacts/census.jsonl").read_text() == "[0,0]\n"


def test_parity_export_ignores_dirty_and_staged_result_review_and_runner(committed_riemann):
    root, exp_two, git, _ = committed_riemann
    exp_four = exp_two.parent / "EXP-004-parity-density-transfer"
    expected = export_registry._riemann_payload()
    for filename in ("artifacts/result.json", "proof-review.json", "run.py"):
        path = exp_four / filename
        path.write_text("Unreviewed working bytes", encoding="utf-8")
        git("add", path.relative_to(root).as_posix())
    assert export_registry._riemann_payload() == expected


@pytest.mark.parametrize("section", ["symbolic", "census", "relaxation", "sharpness"])
def test_parity_export_rejects_changed_raw_evidence(committed_riemann, section):
    _, exp_two, _, commit = committed_riemann
    exp_four = exp_two.parent / "EXP-004-parity-density-transfer"
    suffix = "jsonl" if section == "census" else "json"
    path = exp_four / f"artifacts/{section}.{suffix}"
    path.write_bytes(path.read_bytes() + b"\n")
    commit()
    with pytest.raises(ValueError, match=f"raw evidence differs: {section}"):
        export_registry._riemann_payload()


def test_parity_export_rejects_missing_census_evidence(committed_riemann):
    root, exp_two, git, _ = committed_riemann
    path = exp_two.parent / "EXP-004-parity-density-transfer/artifacts/census.jsonl"
    git("rm", "--cached", path.relative_to(root).as_posix())
    git("-c", "user.name=Replay test", "-c", "user.email=replay@example.invalid",
        "commit", "--quiet", "-m", "Remove census evidence")
    assert path.is_file()
    with pytest.raises(subprocess.CalledProcessError):
        export_registry._riemann_payload()


def test_parity_export_rejects_truncated_census_evidence(committed_riemann):
    _, exp_two, _, commit = committed_riemann
    path = exp_two.parent / "EXP-004-parity-density-transfer/artifacts/census.jsonl"
    path.write_bytes(b"".join(path.read_bytes().splitlines(keepends=True)[:-1]))
    commit()
    with pytest.raises(ValueError, match="raw evidence differs: census"):
        export_registry._riemann_payload()


@pytest.mark.parametrize("filename,role", [("run.py", "parity_runner"), ("hypothesis.md", "parity_hypothesis")])
def test_parity_export_rejects_changed_bound_runner_or_hypothesis(committed_riemann, filename, role):
    _, exp_two, _, commit = committed_riemann
    path = exp_two.parent / "EXP-004-parity-density-transfer" / filename
    path.write_text("Changed source without a new run", encoding="utf-8")
    commit()
    with pytest.raises(ValueError, match=f"committed input differs: {role}"):
        export_registry._riemann_payload()


@pytest.mark.parametrize("premise", [
    "context/2026-09-12-critical-mass-and-multiplicity-route.md",
    "experiments/EXP-003-odd-frame-pressure/mathematical-proof.md",
])
def test_parity_export_rejects_changed_imported_premise(committed_riemann, premise):
    _, exp_two, _, commit = committed_riemann
    path = exp_two.parent.parent / premise
    path.write_text("Changed imported premise", encoding="utf-8")
    commit()
    with pytest.raises(ValueError, match="declared premise differs"):
        export_registry._riemann_payload()


@pytest.mark.parametrize("filename,role", [
    ("mathematical-proof.md", "parity_proof"),
    ("adversarial-audit.md", "parity_audit"),
    ("verdict.md", "parity_verdict"),
])
def test_parity_export_rejects_stale_scientific_review(committed_riemann, filename, role):
    _, exp_two, _, commit = committed_riemann
    path = exp_two.parent / "EXP-004-parity-density-transfer" / filename
    path.write_text("Changed scientific conclusion", encoding="utf-8")
    commit()
    with pytest.raises(ValueError, match=f"proof review no longer matches: {role}"):
        export_registry._riemann_payload()


def test_parity_export_rejects_an_untracked_proof_review_even_if_file_exists(committed_riemann):
    root, exp_two, git, _ = committed_riemann
    path = exp_two.parent / "EXP-004-parity-density-transfer/proof-review.json"
    git("rm", "--cached", path.relative_to(root).as_posix())
    git("-c", "user.name=Replay test", "-c", "user.email=replay@example.invalid",
        "commit", "--quiet", "-m", "Remove reviewed theorem gate")
    assert path.exists()
    with pytest.raises(subprocess.CalledProcessError):
        export_registry._riemann_payload()


@pytest.mark.parametrize("field,value", [
    ("scientific_verdict", "paper_only"),
    ("universal_finite_proof_reviewed", False),
    ("asymptotic_transfer_reviewed", False),
    ("numerical_exponent_claimed", True),
    ("declaration_commit", "0" * 40),
])
def test_parity_export_requires_separate_full_review(committed_riemann, field, value):
    _, exp_two, _, commit = committed_riemann
    path = exp_two.parent / "EXP-004-parity-density-transfer/proof-review.json"
    review = json.loads(path.read_text(encoding="utf-8"))
    review[field] = value
    _write_json(path, review)
    commit()
    with pytest.raises(ValueError, match="separate finite-proof and asymptotic review"):
        export_registry._riemann_payload()


@pytest.mark.parametrize("field", ["classical_a", "kappa", "theta0_numeric", "theta1_decimal"])
def test_parity_export_rejects_made_up_numeric_constants_even_with_rebound_review(committed_riemann, field):
    _, exp_two, _, commit = committed_riemann
    exp_four = exp_two.parent / "EXP-004-parity-density-transfer"
    _rewrite_parity_result(exp_four, lambda result: result["threshold"].update({field: "1/1000000"}))
    commit()
    with pytest.raises(ValueError, match="does not certify numerical seed constants"):
        export_registry._riemann_payload()


def test_parity_export_rejects_promoted_all_height_claim_even_with_rebound_review(committed_riemann):
    _, exp_two, _, commit = committed_riemann
    exp_four = exp_two.parent / "EXP-004-parity-density-transfer"
    _rewrite_parity_result(
        exp_four,
        lambda result: result["proof_status"].update(
            all_height_theorem="The Riemann hypothesis is proved",
        ),
    )
    commit()
    with pytest.raises(ValueError, match="cannot claim an all-height theorem"):
        export_registry._riemann_payload()


@pytest.mark.parametrize("section,field,value", [
    ("symbolic", "residual_identities", 1),
    ("symbolic", "multiplicity_regression_cases", 23),
    ("census", "vectors", 19682),
    ("census", "sigma_evaluations", 59048),
    ("relaxation", "cases", 41),
    ("sharpness", "cases", 35),
    ("census", "vectors", 19683.0),
    ("symbolic", "residual_identities", "2"),
])
def test_parity_export_rejects_changed_counts_with_rebound_review(committed_riemann, section, field, value):
    _, exp_two, _, commit = committed_riemann
    exp_four = exp_two.parent / "EXP-004-parity-density-transfer"
    _rewrite_parity_result(exp_four, lambda result: result[section].update({field: value}))
    commit()
    with pytest.raises(ValueError, match="do not cover the declared scope"):
        export_registry._riemann_payload()


@pytest.mark.parametrize("values", [[0, 1, 3], [False, True, 2], [0, 1]])
def test_parity_export_rejects_changed_slack_grid(committed_riemann, values):
    _, exp_two, _, commit = committed_riemann
    exp_four = exp_two.parent / "EXP-004-parity-density-transfer"
    _rewrite_parity_result(exp_four, lambda result: result["census"].update(sigma_values=values))
    commit()
    with pytest.raises(ValueError, match="slack values differ"):
        export_registry._riemann_payload()


@pytest.mark.parametrize("target", ["hypothesis", "premise"])
def test_parity_export_checks_actual_declaration_bytes_after_hash_rebinding(committed_riemann, target):
    root, exp_two, _, commit = committed_riemann
    exp_four = exp_two.parent / "EXP-004-parity-density-transfer"
    if target == "hypothesis":
        path = exp_four / "hypothesis.md"
    else:
        path = exp_two.parent.parent / "context/2026-09-12-critical-mass-and-multiplicity-route.md"
    path.write_text("Post-declaration source change", encoding="utf-8")
    checksum = hashlib.sha256(path.read_bytes()).hexdigest()

    def rebind(result):
        if target == "hypothesis":
            result["provenance"]["hypothesis"]["sha256"] = checksum
        else:
            record, = [entry for entry in result["provenance"]["inputs"]
                       if entry["path"] == path.relative_to(root).as_posix()]
            record["sha256"] = checksum

    _rewrite_parity_result(exp_four, rebind)
    if target == "hypothesis":
        review_path = exp_four / "proof-review.json"
        review = json.loads(review_path.read_text(encoding="utf-8"))
        review["source_sha256"]["parity_hypothesis"] = checksum
        _write_json(review_path, review)
    commit()
    with pytest.raises(ValueError, match="differs from its declaration revision"):
        export_registry._riemann_payload()


def test_parity_export_rejects_missing_premise_and_arithmetic_only_status(committed_riemann):
    _, exp_two, _, commit = committed_riemann
    exp_four = exp_two.parent / "EXP-004-parity-density-transfer"
    _rewrite_parity_result(exp_four, lambda result: result["provenance"]["inputs"].pop())
    commit()
    with pytest.raises(ValueError, match="complete declared premise set"):
        export_registry._riemann_payload()
    _rewrite_parity_result(exp_four, lambda result: result.update(arithmetic_status="not_confirmed"))
    commit()
    with pytest.raises(ValueError, match="verified declared result"):
        export_registry._riemann_payload()


@pytest.mark.parametrize("verdict", ["confirmed", "PASS"])
def test_registry_reads_lowercase_verdict_headers_and_body_dates(tmp_path, monkeypatch, verdict):
    relative = "problems/number-theory/parser-fixture/experiments/EXP-002-test/verdict.md"
    path = tmp_path / relative
    path.parent.mkdir(parents=True)
    path.write_text(f"# EXP-002 verdict: {verdict} for a bounded claim\n\nDate: 2026-09-12.\n")
    monkeypatch.setattr(export_registry, "ROOT", tmp_path)
    monkeypatch.setattr(export_registry, "_tracked_problem_paths", lambda: {relative})
    monkeypatch.setattr(export_registry, "_committed_riemann_paths", set)
    record, = export_registry._read_experiments()
    assert record["verdict"] == verdict.lower()
    assert record["date"] == "2026-09-12"
