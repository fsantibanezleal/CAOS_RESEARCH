"""Independent original-presentation triangle certificates; never rewrite artifacts."""

import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "problems/commutative-algebra/huneke-wiegand/experiments/EXP-062-triangle-torsion-family"
SPEC = importlib.util.spec_from_file_location("hw_triangle_independent_audit", HERE / "audit.py")
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


@pytest.fixture(scope="module")
def machinery():
    parity, signed = AUDIT.machinery()
    bitsets = signed.load_bitsets()
    literal = bitsets.arithmetic()
    return parity, signed, bitsets, literal


def test_all_triangle_counts_and_selection():
    assert [len(AUDIT.triangles(p)) for p in range(8, 13)] == [3, 4, 5, 7, 8]
    for p in range(8, 101):
        available = AUDIT.triangles(p)
        assert len(available) == ((p - 2) ** 2 + 3) // 12
        assert len(available) == len(set(available))
        assert all(0 <= i < j < k and i + j + k == p - 2 for i, j, k in available)
        expected = available if p <= 14 else [available[0], available[(len(available) - 1) // 2], available[-1]]
        assert AUDIT.selected_triangles(p) == expected


def test_generic_support_includes_adjacent_cancellation(machinery):
    parity, _, _, _ = machinery
    special = AUDIT.triangle_functional(8, (0, 2, 4), parity)
    assert special == parity.functional_rows(8)
    adjacent = AUDIT.triangle_functional(8, (0, 1, 5), parity)
    assert len(adjacent) < 12
    assert len(AUDIT.triangle_functional(8, (1, 2, 3), parity)) < 12


def test_complete_original_p8_rowspace_and_adversarial_controls(machinery, tmp_path):
    parity, signed, _, _ = machinery
    budget = parity.Budget(seconds=30, memory_mib=1024)
    result = AUDIT.parity_parameter(8, parity, signed, budget.check)
    output = tmp_path / "p8-independent.json"
    parity.save_checkpoint(output, result)
    saved = json.loads(output.read_text())
    assert saved["status"] == "COMPLETE"
    assert saved["pairing_matrix"] == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    assert saved["duplicate_mirrored_edge_control"]["rank"] == 2
    for triangle in saved["triangles"]:
        assert triangle["removed_endpoint_control"]["mutated_diagonal"] == 0
        assert triangle["incidence"]["all_original_K_pairings_zero"]
        assert 77 in triangle["incidence"]["actual_reachable_sectors"]
        assert all(sector["status"] == "ROW_SPAN_CERTIFIED" for sector in triangle["sectors"])


@pytest.mark.parametrize("triangle", [(0, 1, 5), (0, 2, 4), (1, 2, 3)])
def test_independent_complete_integer_source_and_mutations(machinery, triangle):
    _, signed, bitsets, literal = machinery
    source, certificate = AUDIT.signed_source_check(8, triangle, signed, bitsets, literal, lambda: None)
    assert source
    assert certificate["full_integer_boundary_equals_twice_x"]
    assert certificate["literal_054_crosscheck"]
    assert certificate["coefficient_mutation"]["rejected"] and certificate["sign_mutation"]["rejected"]


def test_eta_transfer_is_quotient_identity_not_equal_vectors(machinery):
    _, signed, bitsets, literal = machinery
    source, certificate = AUDIT.eta_transfer_check(8, signed, bitsets, literal, lambda: None)
    assert source and certificate["M_source_equals_eta_minus_x02"]
    assert certificate["full_boundary"]


def test_frozen_061_full_kernel_and_dual_smoke(machinery):
    parity, _, _, _ = machinery
    result = parity.sector_certificate(8, 62, parity.functional_rows(8), lambda: None)
    assert result["status"] == "ROW_SPAN_CERTIFIED"
    assert result["full_D_kernel_dimension"] == 34
    assert len(result["complete_kernel_basis_hex"]) == 34
    assert result["D_row_dual"]


@pytest.mark.parametrize("seconds", [0, -1, float("nan"), float("inf"), 121])
def test_audit_cannot_expand_declared_time_cap(machinery, seconds):
    parity, _, _, _ = machinery
    with pytest.raises(AssertionError):
        parity.Budget(seconds=seconds)


def test_canonical_audit_integrity_counts_and_portable_newlines():
    path = HERE / "artifacts/audit-results.json"
    payload = path.read_bytes()
    result = json.loads(payload)
    assert b"\r\n" not in payload
    assert result["status"] == "COMPLETE"
    assert result["auditor_sha256"] == AUDIT.file_hash(HERE / "audit.py")
    assert result["artifact_hash"] == AUDIT.digest({key: value for key, value in result.items() if key != "artifact_hash"})
    assert result["totals"]["full_signed_W_sources"] == 70
    assert result["totals"]["complete_parity_triangles"] == 27
    assert result["totals"]["complete_original_sectors"] == 364
    assert result["totals"]["distinct_parameter_high_sectors"] == 65
    assert result["totals"]["distinct_original_S_sources"] == 23695
    assert result["totals"]["eta_transfer_identities"] == 5
    assert not result["producer_math_imported"] and not result["old_HNF_source_accessed"]


def test_temporary_rowspace_replay_is_deterministic(machinery, tmp_path):
    parity, signed, _, _ = machinery
    first = AUDIT.parity_parameter(8, parity, signed, lambda: None)
    second = AUDIT.parity_parameter(8, parity, signed, lambda: None)
    output = tmp_path / "first.json"
    replay = tmp_path / "replay.json"
    AUDIT.save_checkpoint(output, first)
    AUDIT.save_checkpoint(replay, second)
    assert output.read_bytes() == replay.read_bytes()
