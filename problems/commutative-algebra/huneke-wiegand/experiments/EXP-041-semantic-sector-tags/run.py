"""EXP-041 exact semantic profiles of the frozen parity-core components.

CPU only. This reconstructs the EXP-039 support and unit peeling, reproduces
the frozen component hashes for p=8,...,11, and profiles interval-labelled
rows and columns without performing new finite-field elimination.
"""

from __future__ import annotations

import argparse
import gc
import hashlib
import importlib.util
import json
from array import array
from collections import Counter
from pathlib import Path
from types import ModuleType


HERE = Path(__file__).resolve().parent
EXP037 = HERE.parent / "EXP-037-connecting-quasipolynomial"
EXP039 = HERE.parent / "EXP-039-core-component-stabilization"
EXP040 = HERE.parent / "EXP-040-merged-sector-relation"
DEFAULT_OUTPUT = HERE / "artifacts" / "results.json"
PREMISES = {
    "EXP-037 rank engine": (
        EXP037 / "run.py",
        "1abebc24c99398dded97aa08216211db089889e154736ed9eb5a7202de0b5df0",
    ),
    "EXP-039 component engine": (
        EXP039 / "run.py",
        "8ab5678829094a2b314a23889201b06f555aafc5af176500ef62a5eb30e4a352",
    ),
    "EXP-039 p8-p9 components": (
        EXP039 / "artifacts" / "results-p9.json",
        "831a4300cac10bf44753050a686a7993fabef09bf28b4332c6bb1fb9881c9e2c",
    ),
    "EXP-039 audit": (
        EXP039 / "artifacts" / "audit-certificate.json",
        "55e3159dd01f9c412ad56a5808eda1f428672341b57ce5dd6eb4e2f266051534",
    ),
    "EXP-040 p10-p11 components": (
        EXP040 / "artifacts" / "target-t2-p10-p11.json",
        "ad1fec04199ff94b803f95f98650c8c8ab386386240d584f447afbb9fe27668b",
    ),
    "EXP-040 audit": (
        EXP040 / "artifacts" / "audit-certificate.json",
        "625f9ac10b8aaaf1e2cf4f8ba0d2d12cf1fe3b68745d2c418707c1e8be501482",
    ),
}
EXPECTED_PARTITIONS = {8: [20, 4, 4, 3], 9: [45, 4], 10: [67, 5], 11: [95, 7]}
GENERATOR_TAGS = ("L0", "L1", "H0", "H1", "H2", "H3", "H4", "H5", "H6", "H7")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def write_json_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")
    temporary.replace(path)


def load_module(name: str, path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify_premises() -> dict[str, str]:
    actual = {name: sha256(path) for name, (path, _) in PREMISES.items()}
    expected = {name: expected_hash for name, (_, expected_hash) in PREMISES.items()}
    if actual != expected:
        raise AssertionError({"premise_hash_mismatch": {"actual": actual, "expected": expected}})
    return actual


def frozen_rows() -> dict[int, dict[str, object]]:
    exp039 = json.loads((EXP039 / "artifacts" / "results-p9.json").read_text(encoding="utf-8"))
    exp040 = json.loads(
        (EXP040 / "artifacts" / "target-t2-p10-p11.json").read_text(encoding="utf-8")
    )
    rows = {int(row["p"]): row for row in exp039["rows"] if int(row["p"]) in (8, 9)}
    rows.update({int(row["p"]): row for row in exp040["rows"]})
    if set(rows) != {8, 9, 10, 11}:
        raise AssertionError({"frozen_parameters": sorted(rows)})
    for p, row in rows.items():
        partition = sorted(
            (
                int(component["odd_minus_two_rank_defect"])
                for component in row["components"]
                if component["odd_minus_two_rank_defect"]
            ),
            reverse=True,
        )
        if partition != EXPECTED_PARTITIONS[p]:
            raise AssertionError({"p": p, "frozen_partition": partition})
    return rows


def generator_intervals(p: int) -> list[tuple[str, int, int]]:
    return [
        ("L0", 1, p),
        ("L1", 3 * p, 4 * p - 2),
        ("H0", 6 * p, 8 * p - 2),
        ("H1", 8 * p, 10 * p - 2),
        ("H2", 10 * p, 10 * p),
        ("H3", 11 * p - 1, 12 * p - 1),
        ("H4", 13 * p + 1, 14 * p - 2),
        ("H5", 14 * p, 15 * p - 1),
        ("H6", 16 * p, 16 * p),
        ("H7", 17 * p - 1, 18 * p - 1),
    ]


def degree_two_intervals(p: int) -> list[tuple[str, int, int]]:
    return [
        ("C0", 8 * p - 1, 8 * p - 1),
        ("C1", 10 * p - 1, 10 * p - 1),
        ("C2", 10 * p + 1, 11 * p - 2),
        ("C3", 12 * p, 13 * p),
        ("C4", 14 * p - 1, 14 * p - 1),
        ("C5", 15 * p, 16 * p - 1),
        ("C6", 16 * p + 1, 17 * p - 2),
        ("C7", 18 * p, 24 * p - 1),
    ]


def interval_tag(value: int, intervals: list[tuple[str, int, int]], reverse: bool) -> str:
    candidates = list(reversed(intervals)) if reverse else intervals
    matches = [tag for tag, first, last in candidates if first <= value <= last]
    if len(matches) != 1:
        raise AssertionError({"value": value, "interval_matches": matches})
    return matches[0]


def exterior_counts(exterior: tuple[int, ...], p: int, reverse: bool) -> tuple[int, ...]:
    counts = Counter(
        interval_tag(variable, generator_intervals(p), reverse) for variable in exterior
    )
    if sum(counts.values()) != len(exterior):
        raise AssertionError("exterior tag coverage mismatch")
    return tuple(counts[tag] for tag in GENERATOR_TAGS)


def semantic_atom(
    *, side: str, kind: str, coefficient_tag: str, exterior: tuple[int, ...], p: int, reverse: bool
) -> str:
    return json.dumps(
        [side, kind, coefficient_tag, list(exterior_counts(exterior, p, reverse))],
        separators=(",", ":"),
    )


def support_only_profile(
    *,
    exp037: ModuleType,
    exp036: ModuleType,
    basis: dict[str, object],
    d_rows: list[object],
    frozen: dict[str, object],
    budget: object,
    reverse_tags: bool,
) -> dict[str, object]:
    """Repeat EXP-039 support decomposition and add exact semantic histograms."""

    p = int(basis["p"])
    low = basis["low"]
    degree_two = basis["degree_two"]
    codomain = basis["codomain"]
    kernel_domain = basis["kernel_domain"]
    source = basis["source"]
    k_index = {row: index for index, row in enumerate(codomain)}
    d_index = {row: index for index, row in enumerate(d_rows)}
    k_base = len(d_rows)
    row_count = len(d_rows) + len(codomain)
    column_count = len(source) + len(kernel_domain)

    def kernel_entries(column: int) -> list[tuple[int, int]]:
        exterior, coefficient = kernel_domain[column]
        entries: list[tuple[int, int]] = []
        for variable, sign, face in exp037.signed_faces(exterior):
            product_offset = coefficient + variable
            if product_offset in degree_two:
                entries.append((k_base + k_index[(face, product_offset)], sign))
        return entries

    def source_entries(column: int) -> list[tuple[int, int]]:
        exterior, coefficient = source[column]
        entries: list[tuple[int, int]] = []
        for variable, sign, face in exp037.signed_faces(exterior):
            if variable in low:
                product = exp036.low_product(p, variable, coefficient)
                if product is not None:
                    entries.append((d_index[(face, product[0], product[1])], sign))
            else:
                product_offset = variable + coefficient
                if product_offset in degree_two:
                    entries.append((k_base + k_index[(face, product_offset)], sign))
        return entries

    def combined_entries(column: int) -> list[tuple[int, int]]:
        if column < len(source):
            return source_entries(column)
        return kernel_entries(column - len(source))

    def row_atom(row: int) -> tuple[str, bool]:
        if row < k_base:
            exterior, product_kind, _ = d_rows[row]
            return (
                semantic_atom(
                    side="row",
                    kind="D",
                    coefficient_tag=product_kind,
                    exterior=exterior,
                    p=p,
                    reverse=reverse_tags,
                ),
                False,
            )
        exterior, coefficient = codomain[row - k_base]
        return (
            semantic_atom(
                side="row",
                kind="K",
                coefficient_tag=interval_tag(
                    coefficient, degree_two_intervals(p), reverse_tags
                ),
                exterior=exterior,
                p=p,
                reverse=reverse_tags,
            ),
            (exterior, coefficient) == basis["selected_row"],
        )

    def column_atom(column: int) -> str:
        if column < len(source):
            exterior, coefficient = source[column]
            tag = interval_tag(coefficient, generator_intervals(p), reverse_tags)
            kind = "S"
        else:
            exterior, coefficient = kernel_domain[column - len(source)]
            tag = interval_tag(coefficient, generator_intervals(p), reverse_tags)
            kind = "K"
        return semantic_atom(
            side="column",
            kind=kind,
            coefficient_tag=tag,
            exterior=exterior,
            p=p,
            reverse=reverse_tags,
        )

    counts = array("I", [0]) * row_count
    incident_xor = array("I", [0]) * row_count
    column_sizes = array("I", [0]) * column_count
    initial_nonzeros = 0
    for column in range(column_count):
        entries = combined_entries(column)
        column_sizes[column] = len(entries)
        initial_nonzeros += len(entries)
        for row, value in entries:
            if value:
                counts[row] += 1
                incident_xor[row] ^= column
        if column and column % 50_000 == 0:
            budget.check(f"p={p} incidence scan")
            print(f"p={p} incidence {column}/{column_count}", flush=True)

    active = bytearray(1 if size else 0 for size in column_sizes)
    del column_sizes
    leaf_rows = array("I", (row for row, count in enumerate(counts) if count == 1))
    initial_leaf_rows = len(leaf_rows)
    row_leaf_pivots = 0
    while leaf_rows:
        row = leaf_rows.pop()
        if counts[row] != 1:
            continue
        column = incident_xor[row]
        if not active[column]:
            raise AssertionError("stale unique-column sketch")
        active[column] = 0
        row_leaf_pivots += 1
        for adjacent_row, value in combined_entries(column):
            if value:
                counts[adjacent_row] -= 1
                incident_xor[adjacent_row] ^= column
                if counts[adjacent_row] == 1:
                    leaf_rows.append(adjacent_row)
    del incident_xor, leaf_rows

    row_only_rows = sum(count > 0 for count in counts)
    row_only_columns = sum(active)
    row_only_nonzeros = sum(counts)
    first_row_map = array("i", [-1]) * row_count
    core_global_rows = array("I")
    for row, count in enumerate(counts):
        if count:
            first_row_map[row] = len(core_global_rows)
            core_global_rows.append(row)

    core_original_columns = array("I")
    column_offsets = array("Q", [0])
    edge_rows = array("I")
    column_degrees = array("I")
    for original_column, is_active in enumerate(active):
        if not is_active:
            continue
        mapped = [
            first_row_map[row]
            for row, value in combined_entries(original_column)
            if value and first_row_map[row] >= 0
        ]
        if mapped:
            core_original_columns.append(original_column)
            edge_rows.extend(mapped)
            column_degrees.append(len(mapped))
            column_offsets.append(len(edge_rows))
    del active, first_row_map, counts
    gc.collect()
    if len(edge_rows) != row_only_nonzeros:
        raise AssertionError("CSR nonzero mismatch")

    row_degrees = array("I", [0]) * row_only_rows
    for row in edge_rows:
        row_degrees[row] += 1
    row_offsets = array("Q", [0])
    for degree in row_degrees:
        row_offsets.append(row_offsets[-1] + degree)
    row_edges = array("I", [0]) * len(edge_rows)
    row_positions = array("Q", row_offsets[:-1])
    for column in range(len(core_original_columns)):
        for edge in range(column_offsets[column], column_offsets[column + 1]):
            row = edge_rows[edge]
            row_edges[row_positions[row]] = column
            row_positions[row] += 1
    del row_positions

    active_rows = bytearray([1]) * row_only_rows
    active_columns = bytearray([1]) * len(core_original_columns)
    row_queue = array("I", (row for row, degree in enumerate(row_degrees) if degree == 1))
    column_queue = array(
        "I", (column for column, degree in enumerate(column_degrees) if degree == 1)
    )
    initial_leaf_columns = len(column_queue)
    two_sided_pivots = 0

    def cancel_pair(row: int, column: int) -> None:
        nonlocal two_sided_pivots
        active_rows[row] = 0
        active_columns[column] = 0
        two_sided_pivots += 1
        for edge in range(column_offsets[column], column_offsets[column + 1]):
            adjacent_row = edge_rows[edge]
            if active_rows[adjacent_row]:
                row_degrees[adjacent_row] -= 1
                if row_degrees[adjacent_row] == 1:
                    row_queue.append(adjacent_row)
        for edge in range(row_offsets[row], row_offsets[row + 1]):
            adjacent_column = row_edges[edge]
            if active_columns[adjacent_column]:
                column_degrees[adjacent_column] -= 1
                if column_degrees[adjacent_column] == 1:
                    column_queue.append(adjacent_column)
        row_degrees[row] = 0
        column_degrees[column] = 0

    while row_queue or column_queue:
        if row_queue:
            row = row_queue.pop()
            if not active_rows[row] or row_degrees[row] != 1:
                continue
            neighbors = [
                row_edges[edge]
                for edge in range(row_offsets[row], row_offsets[row + 1])
                if active_columns[row_edges[edge]]
            ]
            if len(neighbors) != 1:
                raise AssertionError("row leaf degree mismatch")
            cancel_pair(row, neighbors[0])
        else:
            column = column_queue.pop()
            if not active_columns[column] or column_degrees[column] != 1:
                continue
            neighbors = [
                edge_rows[edge]
                for edge in range(column_offsets[column], column_offsets[column + 1])
                if active_rows[edge_rows[edge]]
            ]
            if len(neighbors) != 1:
                raise AssertionError("column leaf degree mismatch")
            cancel_pair(neighbors[0], column)

    component_rows: list[array[int]] = []
    component_columns: list[array[int]] = []
    row_components = array("i", [-1]) * row_only_rows
    column_components = array("i", [-1]) * len(core_original_columns)
    for seed in range(len(core_original_columns)):
        if (
            not active_columns[seed]
            or column_degrees[seed] == 0
            or column_components[seed] >= 0
        ):
            continue
        component = len(component_columns)
        rows_here = array("I")
        columns_here = array("I")
        column_components[seed] = component
        column_stack = [seed]
        row_stack: list[int] = []
        while column_stack or row_stack:
            while column_stack:
                column = column_stack.pop()
                columns_here.append(column)
                for edge in range(column_offsets[column], column_offsets[column + 1]):
                    row = edge_rows[edge]
                    if active_rows[row] and row_components[row] < 0:
                        row_components[row] = component
                        row_stack.append(row)
            while row_stack:
                row = row_stack.pop()
                rows_here.append(row)
                for edge in range(row_offsets[row], row_offsets[row + 1]):
                    column = row_edges[edge]
                    if active_columns[column] and column_components[column] < 0:
                        column_components[column] = component
                        column_stack.append(column)
        component_rows.append(rows_here)
        component_columns.append(columns_here)

    frozen_components = frozen["components"]
    observed_hashes: Counter[str] = Counter()
    profiles: list[dict[str, object]] = []
    all_component_summaries: list[dict[str, object]] = []
    for component, (local_rows, local_columns) in enumerate(
        zip(component_rows, component_columns, strict=True)
    ):
        global_rows = sorted(core_global_rows[row] for row in local_rows)
        row_map = {row: index for index, row in enumerate(global_rows)}
        original_columns = sorted(core_original_columns[column] for column in local_columns)
        support_hasher = hashlib.sha256()
        nonzeros = 0
        for original_column in original_columns:
            entries = [
                (row_map[row], value)
                for row, value in combined_entries(original_column)
                if row in row_map and value
            ]
            entries.sort()
            nonzeros += len(entries)
            support_hasher.update(json.dumps([row for row, _ in entries]).encode())
        support_hash = support_hasher.hexdigest()
        observed_hashes[support_hash] += 1
        frozen_component = frozen_components[component]
        if (
            int(frozen_component["component"]) != component
            or frozen_component["support_hash"] != support_hash
            or int(frozen_component["rows"]) != len(global_rows)
            or int(frozen_component["columns"]) != len(original_columns)
            or int(frozen_component["nonzeros"]) != nonzeros
        ):
            raise AssertionError(
                {
                    "p": p,
                    "component_regression": component,
                    "observed": {
                        "support_hash": support_hash,
                        "rows": len(global_rows),
                        "columns": len(original_columns),
                        "nonzeros": nonzeros,
                    },
                    "frozen": {
                        "support_hash": frozen_component["support_hash"],
                        "rows": frozen_component["rows"],
                        "columns": frozen_component["columns"],
                        "nonzeros": frozen_component["nonzeros"],
                    },
                }
            )
        defect = int(frozen_component["odd_minus_two_rank_defect"] or 0)
        all_component_summaries.append(
            {
                "component": component,
                "support_hash": support_hash,
                "rows": len(global_rows),
                "columns": len(original_columns),
                "defect": defect,
            }
        )
        if defect:
            histogram: Counter[str] = Counter()
            selected_row_present = False
            for row in global_rows:
                atom, selected = row_atom(row)
                histogram[atom] += 1
                selected_row_present = selected_row_present or selected
            for original_column in original_columns:
                histogram[column_atom(original_column)] += 1
            row_total = sum(
                count for atom, count in histogram.items() if json.loads(atom)[0] == "row"
            )
            column_total = sum(
                count for atom, count in histogram.items() if json.loads(atom)[0] == "column"
            )
            if row_total != len(global_rows) or column_total != len(original_columns):
                raise AssertionError({"p": p, "semantic_histogram_sum": component})
            coefficient_support = sorted(
                {":".join(json.loads(atom)[:3]) for atom in histogram}
            )
            profiles.append(
                {
                    "component": component,
                    "support_hash": support_hash,
                    "rows": len(global_rows),
                    "columns": len(original_columns),
                    "vertices": len(global_rows) + len(original_columns),
                    "defect": defect,
                    "selected_row_present": selected_row_present,
                    "coefficient_tag_support": coefficient_support,
                    "coefficient_tag_support_hash": digest(coefficient_support),
                    "semantic_atom_count": len(histogram),
                    "semantic_histogram": dict(sorted(histogram.items())),
                    "semantic_histogram_hash": digest(dict(sorted(histogram.items()))),
                }
            )
        budget.check(f"p={p} component profile {component}")

    expected_hashes = Counter(component["support_hash"] for component in frozen_components)
    if observed_hashes != expected_hashes:
        raise AssertionError(
            {
                "p": p,
                "component_hash_multiset_regression": {
                    "observed": dict(observed_hashes),
                    "expected": dict(expected_hashes),
                },
            }
        )
    partition = sorted((profile["defect"] for profile in profiles), reverse=True)
    if partition != EXPECTED_PARTITIONS[p]:
        raise AssertionError({"p": p, "profile_partition": partition})
    selected_profiles = [profile for profile in profiles if profile["selected_row_present"]]
    print(
        f"p={p}: components={len(component_rows)}, defective={len(profiles)}, "
        f"partition={partition}, selected-defective={len(selected_profiles)}",
        flush=True,
    )
    return {
        "p": p,
        "tag_order": "reverse" if reverse_tags else "forward",
        "basis_hashes": basis["hashes"],
        "matrix": {
            "rows": row_count,
            "columns": column_count,
            "initial_nonzeros": initial_nonzeros,
            "initial_leaf_rows": initial_leaf_rows,
            "initial_leaf_columns_after_row_peel": initial_leaf_columns,
            "row_leaf_pivots": row_leaf_pivots,
            "two_sided_leaf_pivots": two_sided_pivots,
            "row_only_residual_rows": row_only_rows,
            "row_only_residual_columns": row_only_columns,
            "row_only_residual_nonzeros": row_only_nonzeros,
            "component_count": len(component_rows),
        },
        "component_regression_hash": digest(all_component_summaries),
        "defect_partition": partition,
        "defective_profiles": profiles,
    }


def evaluate_predictions(rows: list[dict[str, object]]) -> dict[str, object]:
    by_p = {int(row["p"]): row for row in rows}
    if set(by_p) != {8, 9, 10, 11}:
        return {"p1_status": "NOT_EVALUATED", "p2_status": "NOT_EVALUATED", "p3_status": "NOT_EVALUATED"}

    p8 = by_p[8]["defective_profiles"]
    r_anchors = [profile for profile in p8 if profile["defect"] == 3]
    l_anchors = [profile for profile in p8 if profile["defect"] == 4]
    if len(r_anchors) != 1 or len(l_anchors) != 2:
        raise AssertionError("p=8 anchors are not unique")
    r_anchor = r_anchors[0]
    fingerprints_distinct = len(
        {profile["semantic_histogram_hash"] for profile in p8}
    ) == 4
    r_support = r_anchor["coefficient_tag_support_hash"]
    r_support_unique = sum(
        profile["coefficient_tag_support_hash"] == r_support for profile in p8
    ) == 1
    p1_pass = fingerprints_distinct and r_support_unique

    small: dict[int, dict[str, object]] = {}
    for p in (9, 10, 11):
        profiles = by_p[p]["defective_profiles"]
        small[p] = min(profiles, key=lambda profile: int(profile["vertices"]))
    l_supports = {profile["coefficient_tag_support_hash"] for profile in l_anchors}
    p2_checks = {
        "p9_matches_r_support": small[9]["coefficient_tag_support_hash"] == r_support,
        "p10_matches_r_support": small[10]["coefficient_tag_support_hash"] == r_support,
        "p11_loses_r_support": small[11]["coefficient_tag_support_hash"] != r_support,
        "p11_matches_exactly_one_l_support": (
            small[11]["coefficient_tag_support_hash"] in l_supports and len(l_supports) == 2
        ),
    }
    p2_pass = p1_pass and all(p2_checks.values())

    selected = {
        p: [
            profile
            for profile in by_p[p]["defective_profiles"]
            if profile["selected_row_present"]
        ]
        for p in by_p
    }
    p3_pass = p1_pass and all(len(profiles) == 1 for profiles in selected.values())
    return {
        "p1_status": "PASS_FINITE" if p1_pass else "REFUTED",
        "p1_checks": {
            "p8_full_fingerprints_distinct": fingerprints_distinct,
            "p8_r_coefficient_support_unique": r_support_unique,
        },
        "p2_status": "PASS_FINITE" if p2_pass else "REFUTED",
        "p2_checks": p2_checks,
        "p3_status": "PASS_FINITE" if p3_pass else "REFUTED",
        "selected_components": {
            str(p): [
                {
                    "component": profile["component"],
                    "defect": profile["defect"],
                    "support_hash": profile["support_hash"],
                }
                for profile in profiles
            ]
            for p, profiles in selected.items()
        },
        "anchor_hashes": {
            "R": r_anchor["support_hash"],
            "L": sorted(profile["support_hash"] for profile in l_anchors),
        },
        "isolated_hashes": {str(p): profile["support_hash"] for p, profile in small.items()},
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--p-min", type=int, default=8)
    parser.add_argument("--p-max", type=int, default=11)
    parser.add_argument("--budget-seconds", type=float, default=2400.0)
    parser.add_argument("--memory-gib", type=float, default=36.0)
    parser.add_argument("--tag-order", choices=("forward", "reverse"), default="forward")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if args.p_min < 8 or args.p_max > 11 or args.p_min > args.p_max:
        raise ValueError("declared range is 8<=p_min<=p_max<=11")

    premise_hashes = verify_premises()
    frozen = frozen_rows()
    exp037 = load_module("exp037_frozen_for_exp041", EXP037 / "run.py")
    exp036 = exp037.load_exp036()
    budget = exp037.Budget(args.budget_seconds, args.memory_gib)
    result: dict[str, object] = {
        "experiment": "EXP-041",
        "route": "exact semantic interval profiles of frozen parity-core components",
        "status": "RUNNING",
        "parameters": {
            "p_min": args.p_min,
            "p_max": args.p_max,
            "t": 2,
            "budget_seconds": args.budget_seconds,
            "memory_gib": args.memory_gib,
            "tag_order": args.tag_order,
        },
        "premise_hashes": premise_hashes,
        "rows": [],
    }
    write_json_atomic(args.output, result)
    try:
        for p in range(args.p_min, args.p_max + 1):
            print(f"building complete basis for p={p}", flush=True)
            basis = exp037.build_basis(exp036, p, 2)
            d_rows = exp037.d_rows_for_basis(exp036, basis, budget)
            row = support_only_profile(
                exp037=exp037,
                exp036=exp036,
                basis=basis,
                d_rows=d_rows,
                frozen=frozen[p],
                budget=budget,
                reverse_tags=args.tag_order == "reverse",
            )
            result["rows"].append(row)
            result["status"] = "CHECKPOINT"
            result["elapsed_seconds"] = budget.elapsed
            write_json_atomic(args.output, result)
            del basis, d_rows
            gc.collect()
    except exp037.BudgetStop as error:
        result["status"] = "INCONCLUSIVE_RESOURCE_BUDGET"
        result["resource_stop"] = str(error)
        result["elapsed_seconds"] = budget.elapsed
        result["artifact_hash"] = digest(result)
        write_json_atomic(args.output, result)
        print(json.dumps({"status": result["status"], "error": str(error)}, indent=2), flush=True)
        return 2

    result.update(evaluate_predictions(result["rows"]))
    result["status"] = "COMPLETE"
    result["elapsed_seconds"] = budget.elapsed
    result["artifact_hash"] = digest(result)
    write_json_atomic(args.output, result)
    print(
        json.dumps(
            {
                "experiment": result["experiment"],
                "status": result["status"],
                "completed_parameters": [row["p"] for row in result["rows"]],
                "p1_status": result["p1_status"],
                "p2_status": result["p2_status"],
                "p3_status": result["p3_status"],
                "elapsed_seconds": result["elapsed_seconds"],
                "artifact_hash": result["artifact_hash"],
            },
            indent=2,
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
