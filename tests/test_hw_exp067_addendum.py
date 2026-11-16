"""Tests of EXP-067 addendum 1 (audit_v2.py): the routines against brute force."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]
AUDIT = (
    ROOT
    / "problems"
    / "commutative-algebra"
    / "huneke-wiegand"
    / "experiments"
    / "EXP-067-simple-gluing-rigidity-transfer"
    / "audit_v2.py"
)


def load_audit() -> ModuleType:
    spec = importlib.util.spec_from_file_location("exp067_audit_v2_test", AUDIT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def bits_to_set(bits: int, limit: int) -> set[int]:
    return {value for value in range(limit + 1) if bits >> value & 1}


def brute_semigroup(generators: tuple[int, ...], limit: int) -> set[int]:
    """Closure of {0} under adding generators, by plain search."""
    found = {0}
    frontier = [0]
    while frontier:
        value = frontier.pop()
        for generator in generators:
            total = value + generator
            if total <= limit and total not in found:
                found.add(total)
                frontier.append(total)
    return found


def test_gluing_bitset_matches_brute_force() -> None:
    audit = load_audit()
    base = brute_semigroup((4, 5), 200)
    base_bits = sum(1 << value for value in base)
    limit = 120
    got = bits_to_set(audit.glued_bitset(4, 3, base_bits, limit), limit)
    expected = {
        4 * k + 3 * g for k in range(limit) for g in base if 4 * k + 3 * g <= limit
    }
    assert got == expected
    assert got == brute_semigroup((4, 12, 15), limit)


def test_minimal_generators_of_glued_45_with_q3() -> None:
    audit = load_audit()
    base_bits = sum(1 << value for value in brute_semigroup((4, 5), 200))
    limit = 150
    bits = audit.glued_bitset(4, 3, base_bits, limit)
    assert audit.minimal_generators(bits, limit) == [4, 15]  # 12 = 3*4 is a multiple of 4


def test_exponent_and_sumset_routines_match_brute_force() -> None:
    audit = load_audit()
    limit = 80
    gamma = brute_semigroup((4, 5), 200)
    bits = sum(1 << value for value in gamma)
    shift = 1
    e_expected = {a for a in range(limit + 1) if a in gamma and a + shift in gamma}
    d_expected = {
        a
        for a in range(limit + 1)
        if a in gamma and a + shift in gamma and a + 2 * shift in gamma
    }
    e_bits, d_bits = audit.exponent_sets(bits, shift, limit)
    assert bits_to_set(e_bits, limit) == e_expected
    assert bits_to_set(d_bits, limit) == d_expected
    sums = {x + y for x in e_expected for y in e_expected if x + y <= limit}
    assert bits_to_set(audit.sumset(e_bits, limit), limit) == sums
    # <4,5> with s = 1 is nonrigid: D differs from E + E
    assert sums != d_expected


def test_transfer_set_matches_brute_force() -> None:
    audit = load_audit()
    limit = 100
    e_base = {4, 8, 9, 12, 13, 14, 15, 16}
    e_bits = sum(1 << value for value in e_base)
    got = bits_to_set(audit.transfer_bits(4, 3, e_bits, limit), limit)
    expected = {4 * k + 3 * e for k in range(limit) for e in e_base if 4 * k + 3 * e <= limit}
    assert got == expected


def test_noncoprime_pair_is_rejected_and_producer_refuses() -> None:
    audit = load_audit()
    record = audit.noncoprime_record(4, 2)
    assert record["generator_gcd"] == 2
    assert record["gcd_exceeds_one"] is True
    assert record["witness_not_in_semigroup"] is True
    assert record["witness"] % 2 == 1
    assert record["producer_refused"] is True
    assert record["producer_error"]
