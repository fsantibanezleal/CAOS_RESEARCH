"""Declared exact all-triangle source and relative-functional campaign, CPU only."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import importlib.util
import io
import json
import math
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
CAMPAIGN = tuple(range(8, 15)) + (16, 20, 25, 32, 50, 64, 100)
PREMISES = {
    "EXP-062-triangle-torsion-family/hypothesis.md":
        "56663e362e4e26d16d8db30f6000a1761f8e3e5b1e380fc67d9a441c6c8cbeeb",
    "EXP-060-uniform-endpoint-annihilator/run.py":
        "ad24a493584834217b760eb3d11b4bc49db3775aacd056e986ad3e7632b667eb",
    "EXP-061-uniform-parity-functional/run.py":
        "767b34ffe8dcd880ece54743bfff400a59f3c91471483afc5a76350d8de60968",
    "EXP-061-uniform-parity-functional/audit.py":
        "2808798097a4c257c640e864ad73ffc23981197d4f422ee3e8472c14f7ab3ab5",
    "EXP-061-uniform-parity-functional/artifacts/audit-results.json":
        "0d891037c2dd007d3f0cd2c971a4be7529d789c4317307355b711e1afc882b07",
    "EXP-054-full-source-boundary/run.py":
        "bb6c35f36da17d4e4045670348416a18d9cbb28bf5f5774fcf1deabf28ed951f",
    "EXP-054-full-source-boundary/audit.py":
        "9e21b8a03694938e04dc7aba3555944fa511e4d1ac0d4dfc92727288ed7a1b63",
    "EXP-036-factor-two-torsion-anatomy/run.py":
        "1c6923c7c6456673402b5bdd3dada137970f6d01985690f29c960af65a981d03",
    "EXP-057-four-row-kernel-normal-form/run.py":
        "e07ea055a55df8faa909653b763aa95cc07a42b40fde552fbc7043dc1299b05d",
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
    gate = json.loads((EXPERIMENTS / "EXP-061-uniform-parity-functional/artifacts/audit-results.json")
                      .read_text(encoding="utf-8"))
    if gate["status"] != "COMPLETE" or gate["totals"]["parameters"] != 5:
        raise AssertionError("EXP-061 complete original-sector execution gate is not passed")
    helpers = load("helpers060_for_062", "EXP-060-uniform-endpoint-annihilator/run.py")
    modules = helpers.dependencies()
    modules.update({"helpers": helpers,
                    "parity": load("parity061_for_062", "EXP-061-uniform-parity-functional/run.py"),
                    "offset_cache": {}})
    return modules


def validate_parameter(p):
    if not isinstance(p, int) or isinstance(p, bool) or p < 8:
        raise ValueError("triangle family requires integer p>=8")


def validate_triangle(p, triangle):
    validate_parameter(p)
    if (not isinstance(triangle, (tuple, list)) or len(triangle) != 3
            or any(not isinstance(v, int) or isinstance(v, bool) for v in triangle)):
        raise ValueError("triangle requires three integer indices")
    i, j, k = triangle
    if not (0 <= i < j < k and i + j + k == p - 2):
        raise ValueError("triangle must be increasing, nonnegative, and sum to p-2")
    return i, j, k


def triangles(p, budget_check=None):
    validate_parameter(p)
    check = budget_check or (lambda: None)
    n = p - 2
    result = []
    for i in range(n // 3 + 1):
        check()
        for j in range(i + 1, (n - i - 1) // 2 + 1):
            result.append((i, j, n - i - j))
    return result


def selected_triangles(p, budget_check=None):
    values = triangles(p, budget_check)
    if p <= 14:
        return values
    return [values[index] for index in sorted({0, (len(values) - 1) // 2, len(values) - 1})]


def triangle_potential(p, triangle):
    i, j, k = validate_triangle(p, triangle)
    fields = {}
    for u, a, b, weight in ((i, j, k, 1), (j, i, k, -1), (k, i, j, -1)):
        for r in range(u + a + 1, u + b + 1):
            fields[u, r] = weight
    return fields


def z_value(p, triangle, u, v):
    if not (0 <= u <= p - 2 and 0 <= v <= p - 2) or u == v:
        return 0
    return int(tuple(sorted((u, v, p - 2 - u - v))) == tuple(triangle))


def functional_records(p, triangle, parity):
    triangle = validate_triangle(p, triangle)
    i, j, k = triangle
    terms = [parity.e_row(p, u + v + shift, u, v)
             for u, v in ((i, j), (i, k), (j, k)) for shift in (0, 1)]
    for u in triangle:
        for r in range(p):
            s = p + u - 1 - r
            if r < s < p and (z_value(p, triangle, u, r - u)
                              ^ z_value(p, triangle, u, r - u - 1)):
                terms.append(parity.k_row(p, (p - r, p - s, 3 * p + u), 8 * p - 1))
    result = parity.parity_records(parity.parity_vector(terms))
    assert len(result) == 12 - int(j == i + 1) - int(k == j + 1)
    return result


def chosen_class(p, triangle, helpers, multiplier=1):
    i, j, _ = validate_triangle(p, triangle)
    return helpers.e_row(p, i + j, i, j, multiplier)


def pairing(functional, vector, parity):
    return len(parity.parity_vector(functional) & parity.parity_vector(vector)) % 2


def binary_rank(matrix):
    pivots = {}
    for row in matrix:
        value = sum((entry & 1) << index for index, entry in enumerate(row))
        while value:
            pivot = value.bit_length() - 1
            if pivot not in pivots:
                pivots[pivot] = value
                break
            value ^= pivots[pivot]
    return len(pivots)


def check_triangle(p, triangle, modules, budget_check=None):
    check = budget_check or (lambda: None)
    helpers, parity, primary = (modules[name] for name in ("helpers", "parity", "producer"))
    source = helpers.potential_source(p, triangle_potential(p, triangle), check)
    actual = helpers.multiply(p, source, modules, budget_check=check)
    independent = helpers.multiply(p, source, modules, independent=True, budget_check=check)
    expected = helpers.vector([chosen_class(p, triangle, helpers, 2)])
    assert actual == independent == expected, f"p={p},T={triangle}: M W != 2 x"
    functional = functional_records(p, triangle, parity)
    low, high, degree_two = parity.offsets(p, modules)
    for row in functional:
        _, exterior, coefficient = row["exact_label"]
        assert len(exterior) == 2 * p - 3 and set(exterior) <= low | high
        assert sum(exterior) + coefficient == 4 * p * p + 6 * p - 1
        assert coefficient in degree_two and sorted(set(exterior) - low) == [6 * p]
    x = chosen_class(p, triangle, helpers)
    assert pairing(functional, [x], parity) == 1

    # These are exact full mutation residuals by linearity, not projected faces.
    unit = {"coefficient": 1, "exact_label": source[0]["exact_label"]}
    unit_boundary = helpers.multiply(p, [unit], modules, independent=True, budget_check=check)
    assert unit_boundary, "selected source mutation has zero original boundary"
    sign_difference = {key: -2 * source[0]["coefficient"] * value
                       for key, value in unit_boundary.items()}
    i, j, _ = triangle
    low_set = parity.low_set(p)
    endpoint_source = [{"coefficient": 1,
                        "exact_label": ["K", sorted((low_set - {p - i - j, 3 * p + i})
                                                       | {6 * p}), 8 * p - 2 - j]}]
    endpoint_boundary = helpers.multiply(p, endpoint_source, modules, independent=True,
                                         budget_check=check)
    endpoint_records = helpers.records(endpoint_boundary)
    removed = [row for row in functional if row["exact_label"] != x["exact_label"]]
    assert len(removed) + 1 == len(functional) and pairing(removed, [x], parity) == 0
    assert pairing(functional, endpoint_records, parity) == 0
    assert pairing(removed, endpoint_records, parity) == 1
    return {
        "triangle": list(triangle), "chosen_edge": [i, j], "source_support": len(source),
        "source_hash": primary.digest(source), "full_source": source,
        "source_coefficient_height": max(abs(term["coefficient"]) for term in source),
        "functional_support": functional, "functional_hash": primary.digest(functional),
        "functional_rows": len(functional), "full_boundary": helpers.records(actual),
        "boundary_hash": primary.digest(helpers.records(actual)),
        "integer_boundary_equals_twice_class": True, "complete_D_zero": True, "own_pairing": 1,
        "controls": {
            "mutation_method": "exact original unit-column boundary and integral linearity",
            "mutated_source_label": unit["exact_label"],
            "original_source_coefficient": source[0]["coefficient"],
            "coefficient_mutation_rejected": True, "sign_mutation_rejected": True,
            "coefficient_mutation_difference": helpers.records(unit_boundary),
            "sign_mutation_difference": helpers.records(sign_difference),
            "removed_endpoint_rejected": True, "removed_row": x["exact_label"],
            "removed_endpoint_original_K_source": endpoint_source,
            "removed_endpoint_original_K_boundary": endpoint_records,
        },
    }


def eta_transfer(p, modules, budget_check=None):
    check = budget_check or (lambda: None)
    helpers, primary = modules["helpers"], modules["producer"]
    potential = helpers.combine_potentials((helpers.interval_potential(p, 1), 1),
                                           ({(0, 3): 1}, -2), ({(0, 2): 1}, -2))
    source = helpers.combine_sources((helpers.potential_source(p, potential, check), 1),
                                     (helpers.q_source(p, 3), 2), (helpers.q_source(p, 2), -2))
    expected = helpers.add_vectors((helpers.vector(modules["endpoint"].eta_formula(p)), 1),
                                   (helpers.vector([helpers.e_row(p, 2, 0, 2)]), -1))
    actual = helpers.multiply(p, source, modules, budget_check=check)
    assert actual == helpers.multiply(p, source, modules, independent=True, budget_check=check)
    assert actual == expected, f"p={p}: eta-x02 source identity fails"
    return {"identity": "M C = eta-x02", "verified": True,
            "source_support": len(source), "source_hash": primary.digest(source),
            "full_source": source, "full_boundary": helpers.records(actual),
            "boundary_hash": primary.digest(helpers.records(actual))}


def check_parameter(p, modules, budget_check=None):
    check = budget_check or (lambda: None)
    helpers, parity = modules["helpers"], modules["parity"]
    selected = selected_triangles(p, check)
    rows = []
    for triangle in selected:
        check()
        rows.append(check_triangle(p, triangle, modules, check))
    classes = [[chosen_class(p, triangle, helpers)] for triangle in selected]
    matrix = [[pairing(row["functional_support"], value, parity) for value in classes] for row in rows]
    identity = [[int(i == j) for j in range(len(rows))] for i in range(len(rows))]
    assert matrix == identity
    duplicate = [row.copy() for row in matrix]
    for row in duplicate:
        row[1] = row[0]
    i, _, k = selected[0]
    mirrored_class = [helpers.e_row(p, i + k, i, k)]
    mirrored = [row.copy() for row in matrix]
    for index, row in enumerate(rows):
        mirrored[index][1] = pairing(row["functional_support"], mirrored_class, parity)
    assert binary_rank(duplicate) == binary_rank(mirrored) == len(rows) - 1
    if p == 8:
        adjacent = next(row for row in rows if row["triangle"] == [1, 2, 3])
        assert adjacent["functional_rows"] == 10
    return {"p": p, "all_triangle_count": len(triangles(p, check)),
            "tested_triangles": [list(value) for value in selected], "triangles": rows,
            "full_small_pairing_matrix": p <= 14, "pairing_matrix": matrix, "pairing_identity": True,
            "singular_selection_controls": {
                "duplicate_column_matrix": duplicate, "duplicate_rank": binary_rank(duplicate),
                "mirrored_edge": [i, k], "mirrored_column_matrix": mirrored,
                "mirrored_rank": binary_rank(mirrored), "both_rejected": True},
            "eta_transfer": eta_transfer(p, modules, check) if p <= 12 else None}


def package_result(output, result, primary):
    output = Path(output)
    sources, transfers, compact_rows = [], [], []
    for row in result["rows"]:
        compact = {key: value for key, value in row.items() if key not in ("triangles", "eta_transfer")}
        compact["triangles"] = []
        for value in row["triangles"]:
            source = value["full_source"]
            assert primary.digest(source) == value["source_hash"]
            sources.append({"p": row["p"], "triangle": value["triangle"],
                            "source_hash": value["source_hash"], "source_support": len(source),
                            "full_source": source})
            compact["triangles"].append({key: item for key, item in value.items() if key != "full_source"})
        transfer = row["eta_transfer"]
        if transfer is not None:
            transfers.append({"p": row["p"], "source_hash": transfer["source_hash"],
                              "source_support": transfer["source_support"],
                              "full_source": transfer["full_source"]})
            compact["eta_transfer"] = {key: value for key, value in transfer.items() if key != "full_source"}
        else:
            compact["eta_transfer"] = None
        compact_rows.append(compact)
    payload = {"experiment": "EXP-062", "format": "full_triangle_sources_v1",
               "sources": sources, "transfers": transfers}
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    buffer = io.BytesIO()
    with gzip.GzipFile(filename="", fileobj=buffer, mode="wb", compresslevel=9, mtime=0) as archive:
        archive.write(raw)
    compressed = buffer.getvalue()
    source_path = output.with_name(output.stem + "-sources.json.gz")
    source_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = source_path.with_suffix(source_path.suffix + ".tmp")
    temporary.write_bytes(compressed)
    temporary.replace(source_path)
    compact = {key: value for key, value in result.items() if key not in ("rows", "artifact_hash")}
    compact["rows"] = compact_rows
    compact["full_source_archive"] = {
        "filename": source_path.name, "format": payload["format"],
        "sources": len(sources), "transfers": len(transfers),
        "raw_sha256": hashlib.sha256(raw).hexdigest(), "raw_bytes": len(raw),
        "gzip_sha256": hashlib.sha256(compressed).hexdigest(), "gzip_bytes": len(compressed),
        "gzip_mtime": 0, "gzip_filename": ""}
    compact["artifact_hash"] = primary.digest(compact)
    primary.write_json(output, compact)
    return compact


def run(output, smoke_only=False, budget=120):
    if not math.isfinite(budget) or not 0 < budget <= 120:
        raise ValueError("budget must be finite, positive, and at most 120 seconds")
    started = time.monotonic()
    modules = dependencies()
    primary = modules["producer"]
    result = {"experiment": "EXP-062", "status": "CHECKPOINT", "premises": PREMISES,
              "producer_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "execution_gate": "EXP-061 complete original-sector audit passed and hash pinned",
              "campaign": list((8,) if smoke_only else CAMPAIGN),
              "sampling": "all triangles p8..14; first/middle index floor((q-1)/2)/last thereafter",
              "old_p11_hnf_source_accessed": False, "rows": [], "count_checks": []}
    last_memory = [started - 1]

    def check():
        now = time.monotonic()
        if now - started > budget:
            raise RuntimeError("declared 120-second time budget exhausted")
        if now - last_memory[0] >= 0.1:
            last_memory[0] = now
            if modules["helpers"].private_memory_bytes() > 1024 ** 3:
                raise RuntimeError("declared 1-GiB private-memory budget exhausted")

    def checkpoint():
        return package_result(output, result, primary)

    checkpoint()
    current = None
    try:
        for p in range(8, 101):
            check()
            count = len(triangles(p, check))
            assert count == ((p - 2) ** 2 + 3) // 12
            result["count_checks"].append({"p": p, "count": count, "formula_matches": True})
        for p in result["campaign"]:
            current = p
            result["rows"].append(check_parameter(p, modules, check))
            checkpoint()
            print(f"p={p}: {len(result['rows'][-1]['triangles'])} integer sources and "
                  "relative pairings PASS", flush=True)
            check()
    except (AssertionError, RuntimeError) as error:
        result["status"] = "RESOURCE_STOP" if isinstance(error, RuntimeError) else "REFUTED"
        result["first_failure"] = {"p": current, "message": str(error)}
        checkpoint()
        raise
    result["status"] = "COMPLETE"
    result["tested_sources"] = sum(len(row["triangles"]) for row in result["rows"])
    result["claims"] = {
        "P1_integer_sources": "PASS_DECLARED_CAMPAIGN",
        "P2_complete_relative_annihilation": "REQUIRES_INDEPENDENT_FULL_SECTOR_AUDIT_AND_PROOF",
        "P3_pairing_and_count": "PASS_DECLARED_CAMPAIGN",
        "uniform_torsion_lower_bound": "REQUIRES_ALL_PARAMETER_PROOF_AND_INDEPENDENT_AUDIT",
        "complete_quotient_or_upper_bound": "NOT_ESTABLISHED"}
    return checkpoint()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=HERE / "artifacts/results.json")
    parser.add_argument("--smoke-only", action="store_true")
    parser.add_argument("--budget", type=float, default=120)
    args = parser.parse_args()
    run(args.output, args.smoke_only, args.budget)
