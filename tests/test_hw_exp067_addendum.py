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


# ---------------------------------------------------------------- fix pass (HWB-095 verification F1, F2, F3, F5)

EXP009 = AUDIT.parent.parent / "EXP-009-growing-interval-family" / "audit.py"
REFUSALS = (
    "generators do not define a numerical semigroup",
    "q must be coprime to the multiplicity",
)


class FakeProducer:
    """A producer whose entry point raises the given exception (or returns)."""

    def __init__(self, error: Exception | None) -> None:
        self.error = error

    def case_record(self, p: int, q: int) -> dict[str, object]:
        if self.error is not None:
            raise self.error
        return {"accepted": False}


def base_data(audit: ModuleType, p: int) -> tuple[tuple[int, ...], int, ModuleType]:
    exp009 = audit.load_module(EXP009, "exp009_for_tests")
    _, frobenius, generators = exp009.independent_mask(p)
    return tuple(generators), frobenius, exp009


def brute_case(p: int, q: int, gens: tuple[int, ...], upto: int) -> dict[str, object]:
    """Delta = 24p*N + q*Gamma_p by plain closure, with its Frobenius, E and D."""
    multiplicity = 24 * p
    delta_gens = (multiplicity,) + tuple(q * g for g in gens if g != multiplicity)
    delta = brute_semigroup(delta_gens, upto)
    gaps = [v for v in range(upto + 1) if v not in delta]
    shift = q * 6 * p
    e_set = {a for a in range(upto + 1) if a in delta and a + shift in delta}
    d_set = {a for a in e_set if a + 2 * shift in delta}
    return {"delta": delta, "frobenius": max(gaps), "E": e_set, "D": d_set, "shift": shift}


def brute_minimal_generator_count(delta: set[int], upto: int) -> int:
    nonzero = sorted(v for v in delta if 0 < v <= upto)
    sums = {x + y for x in nonzero for y in nonzero if x + y <= upto}
    return sum(1 for v in nonzero if v not in sums)


def test_noncoprime_unrelated_exception_is_not_a_refusal() -> None:
    """F1: only run.py's own ValueError messages count as a refusal."""
    audit = load_audit()
    record = audit.noncoprime_record(4, 2, producer=FakeProducer(KeyError("unrelated crash")))
    assert record["producer_refused"] is False
    assert record["producer_unexpected_error"]
    wrong_text = audit.noncoprime_record(4, 2, producer=FakeProducer(ValueError("something else")))
    assert wrong_text["producer_refused"] is False
    for message in REFUSALS:
        good = audit.noncoprime_record(4, 2, producer=FakeProducer(ValueError(message)))
        assert good["producer_refused"] is True
        assert good["producer_error"] == message
        assert not good["producer_unexpected_error"]
    no_raise = audit.noncoprime_record(4, 2, producer=FakeProducer(None))
    assert no_raise["producer_refused"] is False


def test_real_producer_refusal_is_the_exact_value_error() -> None:
    audit = load_audit()
    record = audit.noncoprime_record(4, 2)
    assert record["producer_error_type"] == "ValueError"
    assert record["producer_error"] in REFUSALS
    assert not record["producer_unexpected_error"]


def test_coprime_probe_reads_no_producer_result() -> None:
    """F3: the probe is whether the producer raises, never its `accepted` value."""
    audit = load_audit()
    assert audit.producer_does_not_refuse_coprime(FakeProducer(None)) is True
    assert audit.producer_does_not_refuse_coprime(FakeProducer(ValueError(REFUSALS[0]))) is False
    assert audit.producer_does_not_refuse_coprime(FakeProducer(KeyError("x"))) is False
    assert audit.producer_does_not_refuse_coprime() is True


def test_audit_case_matches_brute_force() -> None:
    """F5: audit_case against brute force at q = 1 and q = 5 (p = 4)."""
    audit = load_audit()
    gens, base_frob, _ = base_data(audit, 4)
    for q in (1, 5):
        case = audit.audit_case(4, q, gens, base_frob)
        bound = case["comparison_bound"]
        assert bound >= 2 * case["conductor"]
        brute = brute_case(4, q, gens, bound + 2 * (q * 24 + 1))
        assert case["frobenius"] == brute["frobenius"]
        assert case["conductor"] == brute["frobenius"] + 1
        assert case["scaled_shift"] == brute["shift"] == q * 24
        e_set = {a for a in brute["E"] if a <= bound}
        d_set = {a for a in brute["D"] if a <= bound}
        assert case["h1_e_size"] == len(e_set)
        assert case["h1_d_size"] == len(d_set)
        sums = {x + y for x in e_set for y in e_set if x + y <= bound}
        assert sums == d_set
        assert case["h1_e_equal"] and case["h1_d_equal"] and case["h1_tails_full"]
        assert case["h2_rigid"] is True
        assert case["h5_shift_is_gap"] is (brute["shift"] not in brute["delta"])
        assert case["h4_embedding_dimension"] == 44
        assert case["h4_embedding_dimension"] == brute_minimal_generator_count(
            brute["delta"], brute["frobenius"] + 96
        )
        assert case["window_covers_2T"] is True
        assert case["tail_bound"] == max(case["conductor"], q * (case["base_conductor"] + 96))
        assert case["base_conductor"] == base_frob + 1
        assert bound == 2 * case["tail_bound"] + 2
        assert case["accepted"] is True and case["failures"] == []


def test_short_window_fails_h1() -> None:
    """F2: a window that does not cover 2T fails H1 and never passes vacuously."""
    audit = load_audit()
    gens, base_frob, _ = base_data(audit, 4)
    full = audit.audit_case(4, 5, gens, base_frob)
    short = audit.audit_case(4, 5, gens, base_frob, bound=full["conductor"])
    assert short["window_covers_2T"] is False
    assert short["h1_tails_full"] is False
    assert short["accepted"] is False
    assert "H1 E/D transfer" in short["failures"]
    assert short["tail_bound"] == full["tail_bound"]


def test_empty_tail_range_is_not_full() -> None:
    audit = load_audit()
    assert audit.range_full(0b1111, 2, 3) is True
    assert audit.range_full(0b1011, 2, 3) is False
    assert audit.range_full(0b1111, 5, 4) is False  # an empty range is not full


def test_frobenius_of_matches_formula() -> None:
    """F5: Frobenius of <4,5q> is 15q - 4 for odd q; None when the window is short."""
    audit = load_audit()
    for q in (1, 3, 5, 7):
        limit = 15 * q + 40
        bits = sum(1 << v for v in brute_semigroup((4, 5 * q), limit))
        assert audit.frobenius_of(bits, limit, 4) == 15 * q - 4
        assert audit.frobenius_of(bits, 15 * q - 4 + 2, 4) is None


def test_control_45_matches_brute_force() -> None:
    """F5: the <4,5> control, glued with odd q, is nonrigid with a gap at the shift."""
    audit = load_audit()
    for q in (1, 3, 5, 7):
        record = audit.control_45(q)
        limit = 40 * q + 200
        delta = brute_semigroup((4, 5 * q), limit)
        e_set = {a for a in range(limit + 1) if a in delta and a + q in delta}
        d_set = {a for a in e_set if a + 2 * q in delta}
        sums = {x + y for x in e_set for y in e_set if x + y <= limit}
        first = min(sums ^ d_set)
        assert record["nonrigid"] is True
        assert record["shift_is_gap"] is (q not in delta)
        assert record["first_sumset_difference"] == first == 14 * q
        assert record["frobenius"] == 15 * q - 4


def test_base_record_matches_brute_force() -> None:
    """F5: H3 for p = 4 and p = 5 against a plain closure of EXP-009's generators."""
    audit = load_audit()
    for p in (4, 5):
        gens, frob, exp009 = base_data(audit, p)
        record = audit.base_record(p, exp009)
        extent = frob + 2 * 24 * p
        brute = brute_semigroup(gens, extent)
        gaps = [v for v in range(extent + 1) if v not in brute]
        assert record["mask_equal"] is True
        assert record["first_difference"] is None
        assert record["frobenius"] == max(gaps) == frob
        assert record["generator_count"] == 11 * p
        assert record["frobenius_is_gap"] is True


def test_h4_gate_fails_when_the_generator_count_is_wrong(monkeypatch) -> None:
    """F5: a wrong embedding dimension is a recorded failure."""
    audit = load_audit()
    gens, base_frob, _ = base_data(audit, 4)
    monkeypatch.setattr(audit, "minimal_generators", lambda bits, limit: [4])
    case = audit.audit_case(4, 1, gens, base_frob)
    assert case["accepted"] is False
    assert "H4 embedding dimension" in case["failures"]
