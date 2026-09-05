"""Twelve-row relative parity functional and complete-sector potential checks over F2."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import math
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
CAMPAIGN = tuple(range(8, 17)) + (25, 32, 50, 64, 100)
PREMISES = {
    "EXP-061-uniform-parity-functional/hypothesis.md":
        "ff85801daf2facc0df6399c3d128636c17ec575e35c8fadd8166eb6532d98d97",
    "EXP-036-factor-two-torsion-anatomy/run.py":
        "1c6923c7c6456673402b5bdd3dada137970f6d01985690f29c960af65a981d03",
    "EXP-054-full-source-boundary/run.py":
        "bb6c35f36da17d4e4045670348416a18d9cbb28bf5f5774fcf1deabf28ed951f",
    "EXP-054-full-source-boundary/audit.py":
        "9e21b8a03694938e04dc7aba3555944fa511e4d1ac0d4dfc92727288ed7a1b63",
    "EXP-057-four-row-kernel-normal-form/run.py":
        "e07ea055a55df8faa909653b763aa95cc07a42b40fde552fbc7043dc1299b05d",
    "EXP-060-uniform-endpoint-annihilator/run.py":
        "ad24a493584834217b760eb3d11b4bc49db3775aacd056e986ad3e7632b667eb",
    "EXP-060-uniform-endpoint-annihilator/proof.md":
        "47393d1ce2370ac7268b758bf784973a2ce0f4b3c72c8e282d3012f29d1fd37a",
}


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, EXPERIMENTS / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def dependencies():
    for relative, expected in PREMISES.items():
        if hashlib.sha256((EXPERIMENTS / relative).read_bytes()).hexdigest() != expected:
            raise AssertionError(f"premise hash mismatch: {relative}")
    return {
        "algebra": load("algebra036_for_061", "EXP-036-factor-two-torsion-anatomy/run.py"),
        "producer": load("producer054_for_061", "EXP-054-full-source-boundary/run.py"),
        "independent": load("independent054_for_061", "EXP-054-full-source-boundary/audit.py"),
        "endpoint": load("endpoint057_for_061", "EXP-057-four-row-kernel-normal-form/run.py"),
        "helpers": load("helpers060_for_061", "EXP-060-uniform-endpoint-annihilator/run.py"),
        "offset_cache": {},
    }


def validate_parameter(p):
    if not isinstance(p, int) or isinstance(p, bool) or p < 8:
        raise ValueError("parity formula requires integer p>=8")


def low_set(p):
    return set(range(1, p + 1)) | set(range(3 * p, 4 * p - 1))


def mask(values):
    result = 0
    for value in values:
        result |= 1 << value
    return result


def unmask(value):
    result = []
    while value:
        low = value & -value
        result.append(low.bit_length() - 1)
        value ^= low
    return result


def row_key(label):
    return label[0], mask(label[1]), *label[2:]


def parity_records(rows):
    return [{"coefficient": 1, "exact_label": [key[0], unmask(key[1]), *key[2:]]}
            for key in sorted(rows)]


def parity_vector(records):
    result = set()
    for term in records:
        if term["coefficient"] % 2:
            key = row_key(term["exact_label"])
            result.symmetric_difference_update((key,))
    return result


def k_row(p, missing, offset):
    return {"coefficient": 1,
            "exact_label": ["K", sorted((low_set(p) - set(missing)) | {6 * p}), offset]}


def e_row(p, r, u, v):
    return k_row(p, (p - r, 3 * p + u, 3 * p + v), 11 * p - 2 + u + v - r)


def functional_records(p):
    validate_parameter(p)
    k = p - 4
    result = [e_row(p, u + v + shift, u, v)
              for u, v in ((0, 2), (0, k), (2, k)) for shift in (0, 1)]
    for r, s, u in ((2, p - 3, 0), (3, p - 4, 0), (2, p - 1, 2),
                    (3, p - 2, 2), (p - 4, p - 1, k), (p - 3, p - 2, k)):
        result.append(k_row(p, (p - r, p - s, 3 * p + u), 8 * p - 1))
    assert len(parity_vector(result)) == 12
    return parity_records(parity_vector(result))


def z_value(p, u, v):
    if not (0 <= u <= p - 2 and 0 <= v <= p - 2) or u == v:
        return 0
    third = p - 2 - u - v
    if not 0 <= third <= p - 2:
        return 0
    return int(sorted((u, v, third)) == [0, 2, p - 4])


def basis_pairs(p, d):
    validate_parameter(p)
    if not isinstance(d, int) or not 2 <= d <= p + 1:
        raise ValueError("sector requires integer 2<=d<=p+1")
    return [(u, r) for u in range(p - 1) for r in range(max(1, u + d - 2), p)]


def sampled_pairs(p, d):
    """Frozen before the run: all small bases, then lexicographic endpoints/middle."""
    pairs = basis_pairs(p, d)
    if p <= 12:
        return pairs
    selected = {pairs[index] for index in (0, (len(pairs) - 1) // 2, len(pairs) - 1)}
    if d == 2:
        selected.add((1, 1))  # This free diagonal was absent from EXP-060's restricted family.
    return sorted(selected)


def unit_potential_source(p, d, u0, r0, budget_check=None):
    if (u0, r0) not in basis_pairs(p, d):
        raise ValueError("invalid complete-sector unit potential")
    check = budget_check or (lambda: None)
    low = low_set(p)
    high = {6 * p, 8 * p - d}
    source = []

    def add(missing, coefficient):
        source.append({"coefficient": 1,
                       "exact_label": ["S", sorted((low - set(missing)) | high), coefficient]})

    for other in range(p):
        check()
        if other == r0:
            continue
        r, s = sorted((r0, other))
        if u0 + d - 2 <= r + s <= p + u0 + d - 3:
            add((p - r, p - s, 3 * p + u0), p + u0 + d - 2 - r - s)
    for other in range(p - 1):
        check()
        if other == u0:
            continue
        u, v = sorted((u0, other))
        total = u + v
        first, last = max(0, total + d - p), min(p - 1, total + d - 2)
        if total <= p - d and r0 == total + d - 1:
            indices = range(first, last + 1)
        elif first <= r0 <= last:
            indices = (r0,)
        else:
            indices = ()
        for r in indices:
            check()
            add((p - r, 3 * p + u, 3 * p + v), 3 * p + total + d - 2 - r)
    return parity_records(parity_vector(source))


def offsets(p, modules):
    if p not in modules["offset_cache"]:
        algebra = modules["algebra"]
        modules["offset_cache"][p] = (algebra.low_offsets(p), algebra.high_offsets(p),
                                      algebra.degree_two_offsets(p))
    return modules["offset_cache"][p]


def full_boundary(p, source, modules, budget_check=None):
    """All original rows, using exact F2 toggles and integer-bitset exterior faces."""
    check = budget_check or (lambda: None)
    low, high, degree_two = offsets(p, modules)
    generators = low | high
    result = set()
    labels = set()
    for term in source:
        check()
        kind, exterior, coefficient = term["exact_label"]
        key = row_key(term["exact_label"])
        assert key not in labels and term["coefficient"] % 2
        labels.add(key)
        assert exterior == sorted(set(exterior)) and len(exterior) == 2 * p - 2
        assert set(exterior) <= generators and sum(exterior) + coefficient == 4 * p * p + 6 * p - 1
        assert coefficient in (low if kind == "S" else high)
        exterior_mask = mask(exterior)
        for variable in exterior:
            face = exterior_mask ^ (1 << variable)
            total = variable + coefficient
            row = None
            if kind == "S" and variable in low:
                product = modules["algebra"].low_product(p, variable, coefficient)
                if product is not None:
                    row = ("D", face, *product)
            elif total in degree_two:
                row = ("K", face, total)
            if row is not None:
                result.symmetric_difference_update((row,))
    return result


def literal_boundary(p, source, modules):
    value = modules["independent"].independent_boundary(p, source)
    return {row_key([key[0], list(key[1]), *key[2:]])
            for key, coefficient in value.items() if coefficient % 2}


def inverse_incidence(p, target_records, kind, modules, budget_check=None):
    check = budget_check or (lambda: None)
    low, high, _ = offsets(p, modules)
    generators = sorted(high if kind == "S" else low | high)
    labels = set()
    for term in target_records:
        _, exterior, offset = term["exact_label"]
        exterior_mask = mask(exterior)
        for added in generators:
            check()
            if exterior_mask & (1 << added):
                continue
            coefficient = offset - added
            if coefficient in (low if kind == "S" else high):
                labels.add((kind, exterior_mask | (1 << added), coefficient))
    return parity_records(labels)


def pairing(rows, functional):
    return len(rows & functional) % 2


def check_incidence(p, functional, modules, budget_check=None):
    check = budget_check or (lambda: None)
    primary = modules["producer"]
    targets = parity_records(functional)
    k_sources = inverse_incidence(p, targets, "K", modules, check)
    k_boundaries = []
    for source in k_sources:
        actual = full_boundary(p, [source], modules, check)
        assert actual == literal_boundary(p, [source], modules)
        assert pairing(actual, functional) == 0, f"p={p}: P1 original K source not annihilated"
        k_boundaries.append(actual)
    s_sources = inverse_incidence(p, targets, "S", modules, check)
    low, _, _ = offsets(p, modules)
    reached = sorted({next(value for value in source["exact_label"][1]
                           if value not in low and value != 6 * p) for source in s_sources})
    expected = list(range(7 * p - 1, 8 * p - 1)) + [10 * p - 3, 10 * p - 2, 10 * p]
    assert reached == expected, f"p={p}: visible high-sector list mismatch"
    eta = parity_vector(modules["endpoint"].eta_formula(p))
    assert len(eta) == 1 and pairing(eta, functional) == 1
    removed = functional - eta
    assert pairing(eta, removed) == 0
    assert any(pairing(boundary, removed) for boundary in k_boundaries)

    mutated = (functional - parity_vector([e_row(p, 2, 0, 2)])) | parity_vector([e_row(p, 4, 0, 2)])
    mutated_sources = inverse_incidence(p, parity_records(mutated), "K", modules, check)
    index_counterexample = next((source for source in mutated_sources
                                 if pairing(full_boundary(p, [source], modules, check), mutated)), None)
    assert index_counterexample is not None, "support-index mutation not rejected"
    omitted = [source for source in s_sources if 10 * p - 3 in source["exact_label"][1]]
    omitted_witness = next((source for source in omitted
                            if pairing(full_boundary(p, [source], modules, check), functional)), None)
    assert omitted_witness is not None, "omitted reachable sector diagnostic has no witness"
    omitted_boundary = full_boundary(p, [omitted_witness], modules, check)
    assert any(key[0] == "D" for key in omitted_boundary)

    proper_subset = [source for source, boundary in zip(k_sources, k_boundaries, strict=True)
                     if pairing(boundary, eta) == 0]
    added_source = next((source for source, boundary in zip(k_sources, k_boundaries, strict=True)
                         if pairing(boundary, eta)), None)
    assert proper_subset and added_source is not None
    return {
        "all_incident_K_sources": k_sources, "K_source_count": len(k_sources),
        "K_source_hash": primary.digest(k_sources), "P1_complete_inverse_incidence_pass": True,
        "K_full_boundary_hash": primary.digest([parity_records(value) for value in k_boundaries]),
        "all_incident_S_sources": s_sources, "S_source_count": len(s_sources),
        "S_source_hash": primary.digest(s_sources), "reachable_high_sectors": reached,
        "removed_eta_pairing_row_rejected": True, "support_index_mutation_rejected": True,
        "support_index_mutation_counterexample": index_counterexample,
        "omitted_sector_diagnostic": {"high": 10 * p - 3, "witness": omitted_witness,
                                      "K_pairing": 1, "D_boundary_nonzero": True},
        "proper_local_subset_control": {"candidate": parity_records(eta),
                                         "passing_K_columns": len(proper_subset),
                                         "added_source": added_source, "added_pairing": 1},
    }


def check_unit(p, d, u, r, functional, modules, budget_check=None, literal=False):
    check = budget_check or (lambda: None)
    primary = modules["producer"]
    source = unit_potential_source(p, d, u, r, check)
    actual = full_boundary(p, source, modules, check)
    assert all(key[0] == "K" for key in actual), f"p={p},d={d},({u},{r}): D kernel formula fails"
    _, _, degree_two = offsets(p, modules)
    h = 8 * p - d
    expected = set()
    for term in source:
        _, exterior, coefficient = term["exact_label"]
        assert 6 * p + coefficient not in degree_two
        if h + coefficient in degree_two:
            expected.symmetric_difference_update((("K", mask(exterior) ^ (1 << h), h + coefficient),))
    assert actual == expected, "complete high-face formula disagreement"
    if literal:
        assert actual == literal_boundary(p, source, modules)
    c0 = {key for key in functional if key[-1] == 8 * p - 1}
    c2 = functional - c0
    predicted = 0
    for a, b in ((0, 2), (0, p - 4), (2, p - 4)):
        for position in (a + b, a + b + 1):
            predicted ^= int(u in (a, b) and r == position)
    assert pairing(actual, c0) == pairing(actual, c2) == predicted, "C0/C2 pairing identity fails"
    assert pairing(actual, functional) == 0
    return {"potential": [u, r], "source_support": len(source),
            "source_hash": primary.digest(source), "full_D_zero": True,
            "complete_high_face_identity": True, "C0_pairing": predicted, "C2_pairing": predicted,
            "total_pairing": 0, "full_K_boundary_support": len(actual),
            "boundary_hash": primary.digest(parity_records(actual)), "literal_crosscheck": literal}


def check_parameter(p, modules, budget_check=None):
    check = budget_check or (lambda: None)
    primary = modules["producer"]
    functional = parity_vector(functional_records(p))
    low, high, degree_two = offsets(p, modules)
    for term in parity_records(functional):
        _, exterior, offset = term["exact_label"]
        assert len(exterior) == 2 * p - 3 and set(exterior) <= low | high
        assert sum(exterior) + offset == 4 * p * p + 6 * p - 1 and offset in degree_two
        assert [value for value in exterior if value not in low] == [6 * p]
    eta = parity_vector(modules["endpoint"].eta_formula(p))
    assert pairing(eta, functional) == 1
    k = p - 4
    for u, v in ((0, 2), (0, k), (2, k)):
        assert z_value(p, u, v) == z_value(p, u, p - 2 - u - v) == 1
    result = {"p": p, "functional_support": parity_records(functional),
              "functional_hash": primary.digest(parity_records(functional)),
              "eta_pairing": 1, "valid_distinct_functional_rows": 12,
              "incidence": check_incidence(p, functional, modules, check) if p <= 12 else None,
              "sectors": []}
    for d in range(2, p + 2):
        pairs = sampled_pairs(p, d)
        sector = {"d": d, "high": 8 * p - d, "complete_potential_basis_rank": len(basis_pairs(p, d)),
                  "all_basis_elements_tested": p <= 12, "chains": []}
        for u, r in pairs:
            check()
            literal = (p <= 12 and d == 2 and (u, r) in ((0, 1), (1, 1))) or (
                p == 8 and (u, r) == pairs[0])
            sector["chains"].append(check_unit(p, d, u, r, functional, modules, check, literal))
        result["sectors"].append(sector)
    return result


def run(output, smoke_only=False, budget=120):
    if not math.isfinite(budget) or not 0 < budget <= 120:
        raise ValueError("budget must be finite, positive, and at most 120 seconds")
    started = time.monotonic()
    modules = dependencies()
    primary = modules["producer"]
    parameters = (8,) if smoke_only else CAMPAIGN
    result = {"experiment": "EXP-061", "status": "CHECKPOINT", "premises": PREMISES,
              "arithmetic": "F2 original signed differential reduced modulo two",
              "campaign": list(parameters), "old_p11_hnf_source_accessed": False,
              "sampling": "all p8..12 bases; first/middle/last lexicographic pairs thereafter, plus d2(1,1)",
              "rows": []}
    last_memory = [started - 1]

    def checkpoint():
        result["artifact_hash"] = primary.digest(
            {key: value for key, value in result.items() if key != "artifact_hash"})
        primary.write_json(output, result)

    def check():
        now = time.monotonic()
        if now - started > budget:
            raise RuntimeError("declared 120-second time budget exhausted")
        if now - last_memory[0] >= 0.1:
            last_memory[0] = now
            if modules["helpers"].private_memory_bytes() > 1024 ** 3:
                raise RuntimeError("declared 1-GiB private-memory budget exhausted")

    checkpoint()
    current = None
    try:
        for p in parameters:
            current = p
            row = check_parameter(p, modules, check)
            result["rows"].append(row)
            checkpoint()
            count = sum(len(sector["chains"]) for sector in row["sectors"])
            incidence_label = "complete K incidence and " if p <= 12 else ""
            print(f"p={p}: eta pairing1, {incidence_label}{count} potential chains PASS", flush=True)
            check()
    except (AssertionError, RuntimeError) as error:
        result["status"] = "RESOURCE_STOP" if isinstance(error, RuntimeError) else "REFUTED"
        result["first_failure"] = {"p": current, "message": str(error)}
        checkpoint()
        raise
    result["status"] = "COMPLETE"
    result["total_potential_chains"] = sum(len(sector["chains"])
                                           for row in result["rows"] for sector in row["sectors"])
    result["claims"] = {"functional_and_potential_campaign": "PASS",
                        "complete_original_S_kernel_annihilation": "SEPARATE_INDEPENDENT_AUDIT_AND_PROOF",
                        "uniform_exact_order_two": "REQUIRES_COMPLETE_P1_P2_PROOF_AND_INDEPENDENT_AUDIT"}
    checkpoint()
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=HERE / "artifacts/results.json")
    parser.add_argument("--smoke-only", action="store_true")
    parser.add_argument("--budget", type=float, default=120)
    args = parser.parse_args()
    run(args.output, args.smoke_only, args.budget)
