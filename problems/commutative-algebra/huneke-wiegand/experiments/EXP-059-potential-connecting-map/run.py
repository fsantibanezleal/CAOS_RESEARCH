"""Uniform fixed-high potential chains; exact integers, CPU only, no elimination."""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import importlib.util
import math
import os
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
PREMISES = {
    "EXP-059-potential-connecting-map/hypothesis.md":
        "c08a6104dafc057711d5ec42314ea4b762a5a9121a827bf1bf4f3ac459043ea2",
    "EXP-036-factor-two-torsion-anatomy/run.py":
        "1c6923c7c6456673402b5bdd3dada137970f6d01985690f29c960af65a981d03",
    "EXP-054-full-source-boundary/run.py":
        "bb6c35f36da17d4e4045670348416a18d9cbb28bf5f5774fcf1deabf28ed951f",
    "EXP-054-full-source-boundary/audit.py":
        "9e21b8a03694938e04dc7aba3555944fa511e4d1ac0d4dfc92727288ed7a1b63",
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
        "algebra": load("algebra036_for_059", "EXP-036-factor-two-torsion-anatomy/run.py"),
        "producer": load("producer054_for_059", "EXP-054-full-source-boundary/run.py"),
        "independent": load("independent054_for_059", "EXP-054-full-source-boundary/audit.py"),
    }


def validate_parameter(p):
    if not isinstance(p, int) or isinstance(p, bool) or p < 8:
        raise ValueError("potential formula requires integer p>=8")


def basis_pairs(p):
    validate_parameter(p)
    return [(u, r) for u in range(p - 2) for r in range(u + 2, p)]


def campaign_pairs(p):
    validate_parameter(p)
    if p <= 16:
        return basis_pairs(p)
    return [(0, 2), (0, p - 1), (1, 3), (p - 3, p - 1)]


def unit_chain(p, u0, r0, budget_check=None):
    """Sparse implementation of the frozen alpha/beta formulas for one potential."""
    validate_parameter(p)
    if not (isinstance(u0, int) and isinstance(r0, int) and 0 <= u0 <= p - 3
            and u0 + 2 <= r0 <= p - 1):
        raise ValueError("unit potential requires 0<=u<=p-3 and u+2<=r<=p-1")
    check = budget_check or (lambda: None)
    low = set(range(1, p + 1)) | set(range(3 * p, 4 * p - 1))
    high = {6 * p, 8 * p - 4}
    alpha, beta = [], []

    def term(missing, coefficient, weight):
        return {"coefficient": weight,
                "exact_label": ["S", sorted((low - set(missing)) | high), coefficient]}

    for other in range(p):
        check()
        if other == r0:
            continue
        r, s = sorted((r0, other))
        if u0 + 2 <= r + s <= p + u0 + 1:
            value = 1 if s == r0 else -1
            alpha.append(term((p - r, p - s, 3 * p + u0), p + 2 + u0 - r - s,
                              (-1) ** (p + r + s + u0) * value))
    for other in range(p - 1):
        check()
        if other == u0:
            continue
        u, v = sorted((u0, other))
        total = u + v
        first, last = max(0, total - p + 4), min(p - 1, total + 2)
        sign = 1 if u0 == u else -1
        if total <= p - 4 and r0 == total + 3:
            entries = ((r, -sign) for r in range(first, last + 1))
        elif first <= r0 <= last:
            entries = ((r0, sign),)
        else:
            entries = ()
        for r, value in entries:
            check()
            beta.append(term((p - r, 3 * p + u, 3 * p + v),
                             3 * p + 2 + u + v - r,
                             (-1) ** (p + r + u + v) * value))
    return alpha + beta, alpha, beta


def boundary_formula(p, source):
    """P3's complete retained high-face formula; no differential multiplication."""
    result = []
    for term in source:
        _, exterior, coefficient = term["exact_label"]
        if coefficient == 3 or 3 * p <= coefficient <= 3 * p + 2:
            result.append({"coefficient": -term["coefficient"],
                           "exact_label": ["K", [v for v in exterior if v != 8 * p - 4],
                                           coefficient + 8 * p - 4]})
    return result


def recovered_potential(p, u, r, source):
    low = set(range(1, p + 1)) | set(range(3 * p, 4 * p - 1))
    exterior = sorted((low - {p, p - r, 3 * p + u}) | {6 * p, 8 * p - 4})
    label = ["S", exterior, p + 2 + u - r]
    found = [term["coefficient"] for term in source if term["exact_label"] == label]
    return (found[0] if found else 0) * (-1) ** (p + r + u)


def check_unit(p, u, r, modules, budget_check=None):
    check = budget_check or (lambda: None)
    source, alpha, beta = unit_chain(p, u, r, check)
    primary, independent = modules["producer"], modules["independent"]
    expected = independent.sparse(boundary_formula(p, source))
    actual = dict(primary.multiply(p, source, modules["algebra"]))
    check()
    secondary = independent.independent_boundary(p, source)
    assert actual == secondary == expected, f"p={p}, ({u},{r}): full boundary disagreement"
    assert all(index[0] == "K" for index in actual), "nonzero D residual"
    assert source and len(source) <= 3 * p - 5
    assert all(abs(term["coefficient"]) == 1 for term in source)
    c0 = sum(index[-1] == 8 * p - 1 for index in actual)
    c2 = sum(11 * p - 4 <= index[-1] <= 11 * p - 2 for index in actual)
    assert c0 <= 1 and c2 <= 6 and c0 + c2 == len(actual) <= 7
    assert recovered_potential(p, u, r, source) == 1

    # Flipping beta changes D by -2*d_D(beta). The independent map checks it is nonzero.
    beta_boundary = independent.independent_boundary(p, beta)
    wrong_sign_rejected = any(index[0] == "D" for index in beta_boundary)
    assert wrong_sign_rejected, "wrong beta sign not rejected"
    one_column = independent.independent_boundary(p, source[:1])
    coefficient_mutation_rejected = any(index[0] == "D" for index in one_column)
    assert coefficient_mutation_rejected, "single coefficient mutation not rejected"
    check()
    return {
        "potential": [u, r], "source_support": len(source), "alpha_support": len(alpha),
        "beta_support": len(beta), "coefficient_height": 1, "boundary_support": len(actual),
        "c0_rows": c0, "c2_rows": c2, "full_D_zero": True, "independent_agreement": True,
        "potential_recovered": True, "wrong_beta_sign_rejected": wrong_sign_rejected,
        "coefficient_mutation_rejected": coefficient_mutation_rejected,
        "source_hash": primary.digest(source),
        "boundary_hash": primary.digest(primary.records(actual)),
    }


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


def run(output, maximum=100, budget=60):
    if not isinstance(maximum, int) or isinstance(maximum, bool) or not 8 <= maximum <= 100:
        raise ValueError("maximum must be an integer in the declared range 8..100")
    if not math.isfinite(budget) or budget <= 0 or budget > 60:
        raise ValueError("budget must be finite, positive, and at most 60 seconds")
    started = time.monotonic()
    modules = dependencies()
    primary = modules["producer"]
    result = {"experiment": "EXP-059", "status": "CHECKPOINT", "premises": PREMISES,
              "p11_original_source_accessed": False, "parameters_requested": [8, maximum],
              "campaign": "all unit potentials p8..16; four frozen endpoint pairs p17..100",
              "rows": [], "completed_chains": 0}
    last_memory_check = [started - 1]

    def checkpoint():
        result["artifact_hash"] = primary.digest(
            {key: value for key, value in result.items() if key != "artifact_hash"})
        primary.write_json(output, result)

    def budget_check():
        now = time.monotonic()
        if now - started > budget:
            raise RuntimeError("declared 60-second time budget exhausted")
        if now - last_memory_check[0] >= 0.1:
            last_memory_check[0] = now
            if private_memory_bytes() > 1024 ** 3:
                raise RuntimeError("declared 1-GiB private-memory budget exhausted")

    checkpoint()
    current = None
    try:
        for p in range(8, maximum + 1):
            parameter = {"p": p, "basis_rank": math.comb(p - 1, 2),
                         "complete_basis_checked": p <= 16, "chains": []}
            result["rows"].append(parameter)
            for u, r in campaign_pairs(p):
                current = [p, u, r]
                checked = check_unit(p, u, r, modules, budget_check)
                parameter["chains"].append(checked)
                result["completed_chains"] += 1
            checkpoint()
            print(f"p={p}: {len(parameter['chains'])} potential chains PASS; "
                  f"cumulative {result['completed_chains']}", flush=True)
            budget_check()
    except (AssertionError, RuntimeError) as error:
        result["status"] = "RESOURCE_STOP" if isinstance(error, RuntimeError) else "REFUTED"
        result["first_failure"] = {"case": current, "message": str(error)}
        checkpoint()
        raise
    result["status"] = "COMPLETE"
    result["claims"] = {"P1": "UNIFORM_PROOF_WITH_INTEGRAL_RECONSTRUCTION",
                        "P2": "UNIFORM_PROOF_AND_FINITE_STRESS",
                        "P3": "UNIFORM_FACE_PROOF_AND_INDEPENDENT_EXACT_STRESS",
                        "uniform_eta_order_two_or_nonvanishing": "NOT_ESTABLISHED"}
    checkpoint()
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=HERE / "artifacts/results.json")
    parser.add_argument("--maximum", type=int, default=100)
    parser.add_argument("--budget", type=float, default=60)
    args = parser.parse_args()
    run(args.output, args.maximum, args.budget)
