"""EXP-070 producer side: gluing cases with a counterexample factor, on the EXP-068 library.

Everything here uses `hwcert.gluing` (the producer route) and the EXP-068 `run.py` helpers (`PHAM`, `exp009_member`,
`factor`), imported by path and never copied. The independent route is `auditor.py`, which shares no code with
this file or with `hwcert`.
"""

from __future__ import annotations

import importlib.util
import sys
import time
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "code"))

from hwcert.gluing import (  # noqa: E402
    TensorTorsion, Window, dual, extension_generators, glue_generators, hilbert_identity_holds,
    ideal_from_generators, is_extension, is_huneke_wiegand, minimal_generators, predicted_length,
    semigroup_mask, tensor_torsion,
)

EXP068_RUN = HERE.parent / "EXP-068-gluing-tensor-factorization" / "run.py"


def load_exp068():
    if not EXP068_RUN.exists():
        raise FileNotFoundError(f"EXP-068 producer missing: {EXP068_RUN}")
    if "exp068_run_for_exp070" in sys.modules:
        return sys.modules["exp068_run_for_exp070"]
    spec = importlib.util.spec_from_file_location("exp068_run_for_exp070", EXP068_RUN)
    module = importlib.util.module_from_spec(spec)
    sys.modules["exp068_run_for_exp070"] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


_E68 = load_exp068()
PHAM = _E68.PHAM
_C4, _C4_FROB = _E68.exp009_member(4)
_C5, _C5_FROB = _E68.exp009_member(5)

BASES = {
    "B1": {"name": "Pham", "gens": PHAM, "ideal": (0, 14), "role": "counterexample"},
    "B2": {"name": "C_4", "gens": _C4, "ideal": (0, 24), "role": "counterexample"},
    "B3": {"name": "Pham control", "gens": PHAM, "ideal": (0, 1), "role": "Huneke-Wiegand"},
    "B4": {"name": "C_5", "gens": _C5, "ideal": (0, 30), "role": "counterexample"},
}
FROBENIUS_DECLARED = {"B1": 181, "B2": 311, "B3": 181, "B4": 389}
MULTIPLICITY_DECLARED = {"B1": 56, "B2": 96, "B3": 56, "B4": 120}
PARTNERS = {"<2,3>": (2, 3), "<2,5>": (2, 5), "<3,4>": (3, 4), "<3,5>": (3, 5), "<3,4,5>": (3, 4, 5),
            "<4,5,6,7>": (4, 5, 6, 7)}
PARTNER_IDEALS = ((0,), (0, 1))
PRODUCER_LIMIT_SECONDS = 1800
AUDITOR_LIMIT_SECONDS = 900


def in_semigroup(gens: tuple[int, ...], value: int) -> bool:
    reach = [False] * (value + 1)
    reach[0] = True
    for v in range(1, value + 1):
        reach[v] = any(v >= g and reach[v - g] for g in gens)
    return reach[value]


def gluing_parameters(gens_b: tuple[int, ...], gens_s: tuple[int, ...]) -> tuple[int, int]:
    """a1 = least nonzero element of S; a2 = least element of Gamma_B coprime to a1."""
    a1 = min(gens_s)
    a2 = next(v for v in range(1, 10_000) if gcd(v, a1) == 1 and in_semigroup(gens_b, v))
    return a1, a2


def pair_count(window: Window, sg: int, semigroup_gens: tuple[int, ...], ideal_gens: tuple[int, ...]) -> dict:
    """Pairs (x, z), x in A, z in A*, x + z <= top, that `tensor_torsion` enumerates, by the cost model."""
    ideal = ideal_from_generators(window, sg, ideal_gens)
    gens = minimal_generators(window, ideal, semigroup_gens)
    star = dual(window, sg, gens)
    top = max(gens) + window.tail_start(sg) + window.tail_start(star)
    a_min, s_min = window.first(ideal), window.first(star)
    prefix = {s_min - 1: 0}
    for t in range(s_min, top + 1):
        prefix[t] = prefix[t - 1] + (1 if window.contains(star, t) else 0)
    pairs = 0
    for x in range(a_min, top - s_min + 1):
        if window.contains(ideal, x):
            pairs += prefix[top - x]
    return {"pairs": pairs, "degrees": [a_min + s_min, top], "top": top}


def _serialize_factor(f: dict, gens: tuple[int, ...]) -> dict:
    window, sg = f["window"], f["semigroup"]
    return {
        "length": f["torsion"].length,
        "jordan": {str(k): v for k, v in f["torsion"].jordan_at_least.items()},
        "hw": f["hw"], "gens": list(f["gens"]),
        "frobenius": window.tail_start(sg) - 1, "multiplicity": min(gens),
        "window": [window.lo, window.hi],
    }


def factor_job(gens: tuple[int, ...], ideal_gens: tuple[int, ...], y_degree: int) -> dict:
    started = time.time()
    f = _E68.factor(tuple(gens), tuple(ideal_gens), y_degree)
    record = _serialize_factor(f, tuple(gens))
    record["pairs"] = pair_count(f["window"], f["semigroup"], tuple(gens), tuple(f["gens"]))
    record["seconds"] = round(time.time() - started, 2)
    return record


def torsion_of(record: dict) -> TensorTorsion:
    return TensorTorsion(length=record["length"], jordan_at_least={int(k): v for k, v in record["jordan"].items()})


def build_spec(base: str, partner: str, ideal_s: tuple[int, ...], factors: dict | None = None) -> dict:
    """The data of one case; the factor records are computed here unless `factors` supplies them."""
    gens_b, ideal_b = tuple(BASES[base]["gens"]), tuple(BASES[base]["ideal"])
    gens_s = PARTNERS[partner]
    a1, a2 = gluing_parameters(gens_b, gens_s)
    if factors is None:
        factors = {"b": factor_job(gens_b, ideal_b, a2), "s": factor_job(gens_s, tuple(ideal_s), a1)}
    return {
        "label": f"{base} x {partner} ideal {tuple(ideal_s)}", "base": base, "partner": partner,
        "gens_b": list(gens_b), "ideal_b_decl": list(ideal_b), "gens_s": list(gens_s),
        "ideal_s_decl": list(ideal_s), "a1": a1, "a2": a2,
        "factor_b": factors["b"], "factor_s": factors["s"],
    }


def glued_instance(spec: dict):
    """Window, semigroup, ideal of the extension, sized as EXP-068 `big_instance` sizes them."""
    a1, a2 = spec["a1"], spec["a2"]
    gens_b, gens_s = tuple(spec["gens_b"]), tuple(spec["gens_s"])
    glued = glue_generators(a1, gens_b, a2, gens_s)
    ext = extension_generators(a1, tuple(spec["factor_b"]["gens"]), a2, tuple(spec["factor_s"]["gens"]))
    frob = a1 * spec["factor_b"]["frobenius"] + a2 * spec["factor_s"]["frobenius"] + a1 * a2
    window = Window(-max(ext) - 8, frob + 3 * max(ext) + 4 * max(glued))
    sg = semigroup_mask(window, glued)
    ideal = ideal_from_generators(window, sg, ext)
    return window, sg, glued, ext, ideal, frob


def case_job(spec: dict) -> dict:
    """Producer route on one case: direct torsion, law, predicate, mu, Hilbert identity, window, pairs."""
    started = time.time()
    fb, fs = spec["factor_b"], spec["factor_s"]
    a1, a2 = spec["a1"], spec["a2"]
    window, sg, glued, ext, ideal, frob = glued_instance(spec)
    measured = window.tail_start(sg) - 1
    mingens = minimal_generators(window, ideal, glued)
    pairs = pair_count(window, sg, glued, mingens)
    t0 = time.time()
    direct = tensor_torsion(window, sg, glued, mingens)
    torsion_seconds = round(time.time() - t0, 2)
    law = predicted_length(a1, a2, torsion_of(fb), torsion_of(fs))
    hw = is_huneke_wiegand(window, sg, glued, mingens)
    hw_rule = None if (fb["hw"] is None and fs["hw"] is None) else (fb["hw"] is True or fs["hw"] is True)
    mu_factors = len(fb["gens"]) * len(fs["gens"])

    gens_b, gens_s = tuple(spec["gens_b"]), tuple(spec["gens_s"])
    span_b, span_s = max(fb["gens"]), max(fs["gens"])
    w1 = Window(-span_b - 4, fb["frobenius"] + 1 + max(gens_b) + span_b + 16)
    w2 = Window(-span_s - 4, fs["frobenius"] + 1 + max(gens_s) + span_s + 16)
    m1 = ideal_from_generators(w1, semigroup_mask(w1, gens_b), tuple(fb["gens"]))
    m2 = ideal_from_generators(w2, semigroup_mask(w2, gens_s), tuple(fs["gens"]))
    hilbert = hilbert_identity_holds(window, sg, a1, a2, m1, w1, m2, w2, ideal, upto=window.hi)

    p1 = direct.length == law
    p2 = hw == hw_rule and len(mingens) == mu_factors and (hw is None or (direct.length > 0) == hw)
    special = None
    if fb["hw"] is False and fs["hw"] is None:
        special = bool(hw is False and direct.length == 0 and len(mingens) >= 2)
    elif fs["hw"] is True or fb["hw"] is True:
        special = bool(hw is True)
    return {
        "label": spec["label"], "base": spec["base"], "partner": spec["partner"],
        "ideal_b": list(fb["gens"]), "ideal_s": list(fs["gens"]), "a1": a1, "a2": a2,
        "factor_hw": [fb["hw"], fs["hw"]], "factor_torsion": [fb["length"], fs["length"]],
        "factor_jordan": [fb["jordan"], fs["jordan"]],
        "torsion_law": law, "torsion_direct": direct.length,
        "hw": hw, "hw_rule": hw_rule, "mu": [len(fb["gens"]), len(fs["gens"]), len(mingens)],
        "ideal_generators": list(mingens), "hilbert_identity": hilbert,
        "frobenius_formula": frob, "frobenius_measured": measured, "frobenius_matches": measured == frob,
        "window": [window.lo, window.hi], "factor_windows": [[w1.lo, w1.hi], [w2.lo, w2.hi]],
        "pairs_scanned": pairs["pairs"], "degree_range": pairs["degrees"],
        "torsion_seconds": torsion_seconds, "seconds": round(time.time() - started, 2),
        "p1": p1, "p2": p2, "p2_special_rule": special, "p4": bool(hilbert),
    }


def control_c1(base: str) -> dict:
    """Replace a1 by a gap of <2,3> coprime to a2: the Hilbert identity must break or the build be refused."""
    spec = build_spec(base, "<2,3>", (0,))
    gens_b, gens_s = tuple(spec["gens_b"]), PARTNERS["<2,3>"]
    a2 = spec["a2"]
    gap = next(g for g in range(1, 3) if not in_semigroup(gens_s, g) and gcd(g, a2) == 1)
    record = {"base": base, "a1_true": spec["a1"], "a1_gap": gap, "a2": a2}
    try:
        glued_bad = glue_generators(gap, gens_b, a2, gens_s)
        ext = extension_generators(gap, tuple(spec["factor_b"]["gens"]), a2, (0,))
        bound = gap * max(gens_b) ** 2 + a2 * max(gens_s) ** 2 + gap * a2
        window = Window(-max(ext) - 8, 4 * (bound + max(ext)) + 64)
        sg = semigroup_mask(window, glued_bad)
        ideal = ideal_from_generators(window, sg, ext)
        w1 = Window(-max(ext) - 4, 6 * max(gens_b) ** 2 + 64)
        w2 = Window(-4, 6 * max(gens_s) ** 2 + 64)
        m1 = ideal_from_generators(w1, semigroup_mask(w1, gens_b), tuple(spec["factor_b"]["gens"]))
        m2 = ideal_from_generators(w2, semigroup_mask(w2, gens_s), (0,))
        holds = hilbert_identity_holds(window, sg, gap, a2, m1, w1, m2, w2, ideal, upto=3 * bound)
        record.update({"refused": False, "hilbert_identity_holds": holds, "broken": not holds})
    except ValueError as error:
        record.update({"refused": True, "error": str(error), "broken": True})
    return record


def control_c2() -> dict:
    """B1 x <2,3> with the principal partner ideal: bump the largest minimal generator; not an extension."""
    spec = build_spec("B1", "<2,3>", (0,))
    a1, a2 = spec["a1"], spec["a2"]
    window, sg, glued, ext, ideal, _ = glued_instance(spec)
    gens_b, gens_s = tuple(spec["gens_b"]), tuple(spec["gens_s"])
    mingens = minimal_generators(window, ideal, glued)
    bumped = tuple(sorted(set(mingens[:-1]) | {mingens[-1] + 1}))
    perturbed = ideal_from_generators(window, sg, bumped)
    w1 = Window(-40, max(window.hi // a1 + 2, spec["factor_b"]["frobenius"] + max(gens_b) + 30))
    w2 = Window(-40, max(window.hi // a2 + 2, spec["factor_s"]["frobenius"] + max(gens_s) + 30))
    s1, s2 = semigroup_mask(w1, gens_b), semigroup_mask(w2, gens_s)
    true_ok = is_extension(window, sg, glued, ideal, a1, a2, s1, w1, gens_b, s2, w2, gens_s)
    bumped_ok = is_extension(window, sg, glued, perturbed, a1, a2, s1, w1, gens_b, s2, w2, gens_s)
    perturbed_mu = len(minimal_generators(window, perturbed, glued))
    return {"minimal_generators": list(mingens), "perturbed_generators": list(bumped),
            "true_ideal_is_extension": true_ok, "perturbed_is_extension": bumped_ok,
            "perturbed_mu": perturbed_mu, "perturbed_hw": is_huneke_wiegand(window, sg, glued, bumped)}
