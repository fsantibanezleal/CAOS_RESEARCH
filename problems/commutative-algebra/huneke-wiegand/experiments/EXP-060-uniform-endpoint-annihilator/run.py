"""Exact original sources for uniform twice-endpoint annihilation, CPU only."""

from __future__ import annotations

import argparse
import ctypes
import gzip
import hashlib
import importlib.util
import io
import json
import math
import os
import time
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
CAMPAIGN = tuple(range(8, 21)) + (25, 32, 50, 64, 100)
PREMISES = {
    "EXP-060-uniform-endpoint-annihilator/hypothesis.md":
        "cd0e5715326570487cec4e79da27bbc79a14e9b3dbc1aa0787f86eebb42daf56",
    "EXP-036-factor-two-torsion-anatomy/run.py":
        "1c6923c7c6456673402b5bdd3dada137970f6d01985690f29c960af65a981d03",
    "EXP-054-full-source-boundary/run.py":
        "bb6c35f36da17d4e4045670348416a18d9cbb28bf5f5774fcf1deabf28ed951f",
    "EXP-054-full-source-boundary/audit.py":
        "9e21b8a03694938e04dc7aba3555944fa511e4d1ac0d4dfc92727288ed7a1b63",
    "EXP-057-four-row-kernel-normal-form/run.py":
        "e07ea055a55df8faa909653b763aa95cc07a42b40fde552fbc7043dc1299b05d",
    "EXP-059-potential-connecting-map/proof.md":
        "9c14bacae452614bb26cb39d5419bb89b40e43cf5de6c96fb0f2b43e5e7ec73c",
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
        "algebra": load("algebra036_for_060", "EXP-036-factor-two-torsion-anatomy/run.py"),
        "producer": load("producer054_for_060", "EXP-054-full-source-boundary/run.py"),
        "independent": load("independent054_for_060", "EXP-054-full-source-boundary/audit.py"),
        "endpoint": load("endpoint057_for_060", "EXP-057-four-row-kernel-normal-form/run.py"),
    }


def validate_parameter(p):
    if not isinstance(p, int) or isinstance(p, bool) or p < 8:
        raise ValueError("annihilator formula requires integer p>=8")


def label_key(label):
    return label[0], tuple(label[1]), *label[2:]


def records(vector):
    return [{"coefficient": value, "exact_label": [key[0], list(key[1]), *key[2:]]}
            for key, value in sorted(vector.items()) if value]


def combine_sources(*terms):
    result = Counter()
    for source, multiplier in terms:
        for term in source:
            result[label_key(term["exact_label"])] += multiplier * term["coefficient"]
    return records(result)


def vector(source):
    result = Counter()
    for term in source:
        result[label_key(term["exact_label"])] += term["coefficient"]
    return {key: value for key, value in result.items() if value}


def add_vectors(*terms):
    result = Counter()
    for value, multiplier in terms:
        for key, coefficient in value.items():
            result[key] += multiplier * coefficient
    return {key: coefficient for key, coefficient in result.items() if coefficient}


def interval_potential(p, j):
    validate_parameter(p)
    if j not in (1, 2):
        raise ValueError("interval potential requires j=1 or j=2")
    k = p - 2 - j
    result = {}
    for u, first, last, weight in ((0, j + 1, k, 1), (j, j + 1, p - 2, -1),
                                    (k, k + 1, p - 2, -1)):
        for r in range(first, last + 1):
            result[u, r] = weight
    return result


def combine_potentials(*terms):
    result = Counter()
    for potential, multiplier in terms:
        for key, value in potential.items():
            result[key] += multiplier * value
    return {key: value for key, value in result.items() if value}


def potential_source(p, potential, budget_check=None):
    """Direct sparse frozen d=2 alpha/beta operator, combined in original labels."""
    validate_parameter(p)
    for (u, r), weight in potential.items():
        if not (isinstance(u, int) and isinstance(r, int) and isinstance(weight, int)
                and 0 <= u <= p - 2 and 0 <= r <= p - 1 and (r > u or weight == 0)):
            raise ValueError("potentials must be integral and vanish for r<=u")
    check = budget_check or (lambda: None)
    active = sorted({u for (u, _), weight in potential.items() if weight})
    low = set(range(1, p + 1)) | set(range(3 * p, 4 * p - 1))
    high = {6 * p, 8 * p - 2}
    source = []

    def add(missing, coefficient, weight):
        if weight:
            source.append({"coefficient": weight,
                           "exact_label": ["S", sorted((low - set(missing)) | high), coefficient]})

    for u in active:
        for r in range(p):
            check()
            for s in range(r + 1, p):
                if u <= r + s <= p + u - 1:
                    value = potential.get((u, s), 0) - potential.get((u, r), 0)
                    add((p - r, p - s, 3 * p + u), p + u - r - s,
                        (-1) ** (p + r + s + u) * value)
    pairs = sorted({tuple(sorted((u, v))) for u in active for v in range(p - 1) if u != v})
    for u, v in pairs:
        total = u + v
        shift = (potential.get((u, total + 1), 0) - potential.get((v, total + 1), 0)
                 if total <= p - 2 else 0)
        for r in range(max(0, total - p + 2), min(p - 1, total) + 1):
            check()
            value = potential.get((u, r), 0) - potential.get((v, r), 0) - shift
            add((p - r, 3 * p + u, 3 * p + v), 3 * p + total - r,
                (-1) ** (p + r + u + v) * value)
    return combine_sources((source, 1))


def source_boundary_formula(p, source):
    result = []
    for term in source:
        kind, exterior, coefficient = term["exact_label"]
        assert kind == "S"
        if coefficient in (1, 3 * p):
            result.append({"coefficient": -term["coefficient"],
                           "exact_label": ["K", [v for v in exterior if v != 8 * p - 2],
                                           8 * p - 2 + coefficient]})
    return vector(result)


def e_row(p, r, u, v, weight=1):
    validate_parameter(p)
    if not (0 <= r <= p - 1 and 0 <= u < v <= p - 2):
        raise ValueError("invalid endpoint row indices")
    low = set(range(1, p + 1)) | set(range(3 * p, 4 * p - 1))
    return {"coefficient": (-1) ** (p + r + u + v) * weight,
            "exact_label": ["K", sorted((low - {p - r, 3 * p + u, 3 * p + v}) | {6 * p}),
                            11 * p - 2 + u + v - r]}


def q_source(p, a):
    validate_parameter(p)
    if a not in (2, 3):
        raise ValueError("Q source requires a=2 or a=3")
    low = set(range(1, p + 1)) | set(range(3 * p, 4 * p - 1))
    return [{"coefficient": 1,
             "exact_label": ["K", sorted((low - {p - a, 3 * p}) | {6 * p}), 8 * p - 2 - a]}]


def candidate_source(p, budget_check=None):
    f1, f2 = interval_potential(p, 1), interval_potential(p, 2)
    potential = combine_potentials((f2, 1), (f1, 2), ({(0, 3): 1}, -4), ({(0, 2): 1}, -4))
    source = potential_source(p, potential, budget_check)
    return combine_sources((source, 1), (q_source(p, 3), 4), (q_source(p, 2), -4))


def multiply(p, source, modules, independent=False, budget_check=None):
    check = budget_check or (lambda: None)
    total = Counter()
    for start in range(0, len(source), 8):
        check()
        part = source[start:start + 8]
        value = (modules["independent"].independent_boundary(p, part) if independent else
                 modules["producer"].multiply(p, part, modules["algebra"]))
        total.update(value)
    check()
    return {key: value for key, value in total.items() if value}


def check_parameter(p, modules, budget_check=None):
    check = budget_check or (lambda: None)
    primary = modules["producer"]
    potentials = {"F1": interval_potential(p, 1), "F2": interval_potential(p, 2),
                  "delta03": {(0, 3): 1}, "delta02": {(0, 2): 1}}
    sources, boundaries, summaries = {}, {}, {}
    for name, potential in potentials.items():
        source = potential_source(p, potential, check)
        expected = source_boundary_formula(p, source)
        actual = multiply(p, source, modules, budget_check=check)
        secondary = multiply(p, source, modules, independent=True, budget_check=check)
        assert actual == secondary == expected, f"p={p}, {name}: P1 full boundary disagreement"
        assert all(key[0] == "K" for key in actual)
        sources[name], boundaries[name] = source, actual
        summaries[name] = {"source_support": len(source), "source_hash": primary.digest(source),
                           "full_boundary": records(actual), "boundary_hash": primary.digest(records(actual)),
                           "P1_full_boundary_verified": True}
    for j in (1, 2):
        assert boundaries[f"F{j}"] == vector([e_row(p, j, 0, j, 2)]), f"p={p}: P2 fails j={j}"
    for a in (2, 3):
        name = f"Q{a}"
        source = q_source(p, a)
        actual = multiply(p, source, modules, budget_check=check)
        assert actual == multiply(p, source, modules, independent=True, budget_check=check)
        assert all(key[0] == "K" and 6 * p in key[1] for key in actual), "unaccounted Q high face"
        sources[name], boundaries[name] = source, actual

    b = add_vectors((boundaries["delta03"], 1), (boundaries["Q3"], -1))
    d = add_vectors((boundaries["delta02"], 1), (boundaries["Q2"], 1))
    b_expected = vector([e_row(p, 3, 0, 1), e_row(p, 2, 0, 2), e_row(p, 3, 0, 2)])
    d_expected = vector([e_row(p, 1, 0, 1), e_row(p, 2, 0, 1)])
    assert b == b_expected and d == d_expected, f"p={p}: P3 B/D identities fail"
    eta = vector(modules["endpoint"].eta_formula(p))
    eta_reconstruction = add_vectors((vector([e_row(p, 2, 0, 2), e_row(p, 1, 0, 1, 2)]), 1),
                                     (b, -2), (d, -2))
    assert eta == eta_reconstruction, f"p={p}: exact eta reconstruction fails"

    source = candidate_source(p, check)
    expanded = combine_sources((sources["F2"], 1), (sources["F1"], 2),
                               (sources["delta03"], -4), (sources["delta02"], -4),
                               (sources["Q3"], 4), (sources["Q2"], -4))
    assert source == expanded, "direct potential operator violates integral linearity"
    expected = {key: 2 * coefficient for key, coefficient in eta.items()}
    actual = multiply(p, source, modules, budget_check=check)
    secondary = multiply(p, source, modules, independent=True, budget_check=check)
    assert actual == secondary == expected, f"p={p}: M V = 2 eta fails"

    rejected = combine_sources((source, 1), (sources["delta02"], 4), (sources["Q2"], 4))
    rejected_boundary = multiply(p, rejected, modules, independent=True, budget_check=check)
    rejected_difference = add_vectors((rejected_boundary, 1), (expected, -1))
    assert rejected_difference == {key: 4 * value for key, value in d.items()} and rejected_difference
    literal_earliest = combine_sources((rejected, 1), (sources["F1"], -4))
    literal_boundary = multiply(p, literal_earliest, modules, independent=True, budget_check=check)
    literal_difference = add_vectors((literal_boundary, 1), (expected, -1))
    assert literal_difference == vector([e_row(p, 2, 0, 1, 4), e_row(p, 1, 0, 1, -4)])
    single = multiply(p, source[:1], modules, independent=True, budget_check=check)
    assert single, "first-column mutation not detected"
    sign_difference = {key: -2 * value for key, value in single.items()}
    coefficient_difference = {key: value // source[0]["coefficient"] for key, value in single.items()}
    assert sign_difference and coefficient_difference
    return {"p": p, "P1": True, "P2": True, "P3": True, "M_V_equals_twice_eta": True,
            "full_original_independent_agreement": True, "source_support": len(source),
            "source_coefficient_height": max(abs(term["coefficient"]) for term in source),
            "full_source": source, "source_hash": primary.digest(source),
            "full_boundary": records(actual), "boundary_hash": primary.digest(records(actual)),
            "components": summaries, "B_boundary": records(b), "D_boundary": records(d),
            "rejected_missing_delta02_formula_fails": True,
            "rejected_difference": records(rejected_difference),
            "rejected_difference_hash": primary.digest(records(rejected_difference)),
            "literal_earliest_wrong_F1_sign_and_missing_delta02_fails": True,
            "literal_earliest_formula": "P(F2-2F1-4delta03)+4Q3",
            "literal_earliest_difference": records(literal_difference),
            "literal_earliest_difference_hash": primary.digest(records(literal_difference)),
            "sign_mutation_rejected": True, "coefficient_mutation_rejected": True,
            "sign_mutation_difference_hash": primary.digest(records(sign_difference)),
            "coefficient_mutation_difference_hash": primary.digest(records(coefficient_difference))}


def private_memory_bytes():
    if os.name == "nt":
        class Counters(ctypes.Structure):
            _fields_ = [("cb", ctypes.c_ulong), ("PageFaultCount", ctypes.c_ulong)] + [
                (name, ctypes.c_size_t) for name in (
                    "PeakWorkingSetSize", "WorkingSetSize", "QuotaPeakPagedPoolUsage",
                    "QuotaPagedPoolUsage", "QuotaPeakNonPagedPoolUsage", "QuotaNonPagedPoolUsage",
                    "PagefileUsage", "PeakPagefileUsage", "PrivateUsage")]
        counters = Counters()
        counters.cb = ctypes.sizeof(counters)
        handle = ctypes.windll.kernel32.GetCurrentProcess
        handle.restype = ctypes.c_void_p
        function = ctypes.windll.psapi.GetProcessMemoryInfo
        function.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong]
        if not function(handle(), ctypes.byref(counters), counters.cb):
            raise OSError("cannot verify the declared private-memory budget")
        return counters.PrivateUsage
    import resource
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1024


def package_result(output, result, primary):
    """Persist every full labelled witness in a deterministic, lossless gzip sidecar."""
    output = Path(output)
    source_path = output.with_name(output.stem + "-sources.json.gz")
    witnesses = []
    compact_rows = []
    for row in result["rows"]:
        source = row["full_source"]
        assert len(source) == row["source_support"] and primary.digest(source) == row["source_hash"]
        witnesses.append({"p": row["p"], "source_hash": row["source_hash"],
                          "source_support": len(source), "full_source": source})
        compact_rows.append({key: value for key, value in row.items() if key != "full_source"})
    payload = {"experiment": "EXP-060", "format": "full_original_V_source_records_v1",
               "sources": witnesses}
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    buffer = io.BytesIO()
    with gzip.GzipFile(filename="", fileobj=buffer, mode="wb", compresslevel=9, mtime=0) as archive:
        archive.write(raw)
    compressed = buffer.getvalue()
    source_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = source_path.with_suffix(source_path.suffix + ".tmp")
    temporary.write_bytes(compressed)
    temporary.replace(source_path)
    compact = {key: value for key, value in result.items() if key not in ("rows", "artifact_hash")}
    compact["rows"] = compact_rows
    compact["full_source_archive"] = {
        "filename": source_path.name, "format": payload["format"], "parameters": len(witnesses),
        "raw_sha256": hashlib.sha256(raw).hexdigest(), "raw_bytes": len(raw),
        "gzip_sha256": hashlib.sha256(compressed).hexdigest(), "gzip_bytes": len(compressed),
        "gzip_mtime": 0, "gzip_filename": "",
    }
    compact["artifact_hash"] = primary.digest(compact)
    primary.write_json(output, compact)
    return compact


def repackage_existing(output):
    """Mechanical encoding only: validate old full records, then losslessly package them."""
    modules = dependencies()
    result = json.loads(Path(output).read_text(encoding="utf-8"))
    expected = result["artifact_hash"]
    assert modules["producer"].digest({key: value for key, value in result.items()
                                       if key != "artifact_hash"}) == expected
    if not all("full_source" in row for row in result["rows"]):
        raise ValueError("repackaging requires the original full-record JSON")
    return package_result(output, result, modules["producer"])


def run(output, smoke_only=False, budget=60):
    if not math.isfinite(budget) or not 0 < budget <= 60:
        raise ValueError("budget must be finite, positive, and at most 60 seconds")
    started = time.monotonic()
    modules = dependencies()
    primary = modules["producer"]
    parameters = (8,) if smoke_only else CAMPAIGN
    result = {"experiment": "EXP-060", "status": "CHECKPOINT", "premises": PREMISES,
              "campaign": list(parameters), "p11_original_source_accessed": False,
              "old_hnf_source_accessed": False, "rows": []}
    last_memory = [started - 1]
    latest_checkpoint = [None]

    def checkpoint():
        latest_checkpoint[0] = package_result(output, result, primary)

    def check():
        now = time.monotonic()
        if now - started > budget:
            raise RuntimeError("declared time budget exhausted")
        if now - last_memory[0] >= 0.1:
            last_memory[0] = now
            if private_memory_bytes() > 1024 ** 3:
                raise RuntimeError("declared 1-GiB private-memory budget exhausted")

    checkpoint()
    current = None
    try:
        for p in parameters:
            current = p
            row = check_parameter(p, modules, check)
            result["rows"].append(row)
            checkpoint()
            print(f"p={p}: M V=2 eta PASS, source={row['source_support']}, "
                  f"height={row['source_coefficient_height']}; all P1/P2/P3 and controls PASS", flush=True)
            check()
    except (AssertionError, RuntimeError) as error:
        result["status"] = "RESOURCE_STOP" if isinstance(error, RuntimeError) else "REFUTED"
        result["first_failure"] = {"p": current, "message": str(error)}
        checkpoint()
        raise
    result["status"] = "COMPLETE"
    result["claims"] = {"P1": "PASS_DECLARED_CAMPAIGN", "P2": "PASS_DECLARED_CAMPAIGN",
                        "P3": "PASS_DECLARED_CAMPAIGN", "uniform_2_annihilation": "REQUIRES_SIGNED_PROOF_AUDIT",
                        "uniform_nonvanishing_second_class_upper_bound": "NOT_ESTABLISHED"}
    checkpoint()
    return latest_checkpoint[0]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=HERE / "artifacts/results.json")
    parser.add_argument("--smoke-only", action="store_true")
    parser.add_argument("--budget", type=float, default=60)
    parser.add_argument("--repackage-existing", action="store_true")
    args = parser.parse_args()
    if args.repackage_existing:
        repackage_existing(args.output)
    else:
        run(args.output, args.smoke_only, args.budget)
