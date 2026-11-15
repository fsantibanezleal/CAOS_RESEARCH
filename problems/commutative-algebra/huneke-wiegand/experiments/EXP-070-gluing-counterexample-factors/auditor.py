"""EXP-070 independent route: EXP-068 `audit.py` (plain integer sets, breadth-first search) on one case.

This file imports nothing but the standard library and EXP-068 `audit.py`, loaded by path; the glued semigroup,
the extension generators and every statistic are rebuilt here from the declared inputs (generators of both
factors, their declared ideals and the two gluing multipliers), not read from the producer.
"""

from __future__ import annotations

import importlib.util
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
AUDIT_PATH = HERE.parent / "EXP-068-gluing-tensor-factorization" / "audit.py"


def load_audit():
    if not AUDIT_PATH.exists():
        raise FileNotFoundError(f"EXP-068 auditor missing: {AUDIT_PATH}")
    if "exp068_audit_for_exp070" in sys.modules:
        return sys.modules["exp068_audit_for_exp070"]
    spec = importlib.util.spec_from_file_location("exp068_audit_for_exp070", AUDIT_PATH)
    module = importlib.util.module_from_spec(spec)
    sys.modules["exp068_audit_for_exp070"] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def factor_status(gens: tuple[int, ...], ideal_decl: tuple[int, ...]) -> dict:
    """Minimal generators, Frobenius number and partition-criterion status of one factor ideal."""
    audit = load_audit()
    sg = audit.Semigroup(tuple(gens), 8 * max(gens))
    ideal = audit.minimal_gens(sg, tuple(ideal_decl))
    hi = sg.frobenius + 3 * max(ideal) + max(gens) + 8
    return {"frobenius": sg.frobenius, "minimal_generators": list(ideal),
            "hw": audit.huneke_wiegand(sg, ideal, -max(ideal) - 4, hi)}


def audit_case(spec: dict) -> dict:
    """Direct torsion length and Huneke-Wiegand predicate of the glued extension ideal, from plain sets."""
    started = time.time()
    audit = load_audit()
    a1, a2 = spec["a1"], spec["a2"]
    gens_b, gens_s = tuple(spec["gens_b"]), tuple(spec["gens_s"])
    fb = factor_status(gens_b, tuple(spec["ideal_b_decl"]))
    fs = factor_status(gens_s, tuple(spec["ideal_s_decl"]))
    glued = tuple(sorted({a1 * g for g in gens_b} | {a2 * g for g in gens_s}))
    ext = sorted({a1 * x + a2 * z for x in fb["minimal_generators"] for z in fs["minimal_generators"]})
    frob_formula = a1 * fb["frobenius"] + a2 * fs["frobenius"] + a1 * a2
    sg = audit.Semigroup(glued, frob_formula + 4 * max(glued) + 2 * max(ext) + 64)
    mingens = audit.minimal_gens(sg, ext)
    hw = audit.huneke_wiegand(sg, ext, -max(ext) - 4, sg.frobenius + 3 * max(ext) + max(glued))
    torsion = audit.direct_torsion(sg, ext)
    return {"label": spec["label"], "torsion": torsion, "hw": hw, "mu": len(mingens),
            "minimal_generators": list(mingens), "frobenius": sg.frobenius,
            "factor_hw": [fb["hw"], fs["hw"]], "factor_minimal_generators": [fb["minimal_generators"],
                                                                              fs["minimal_generators"]],
            "seconds": round(time.time() - started, 2)}
