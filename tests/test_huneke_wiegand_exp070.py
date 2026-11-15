"""EXP-070 tests: producer and auditor agree on a case with a counterexample factor; the auditor shares no code."""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXP070 = ROOT / "problems/commutative-algebra/huneke-wiegand/experiments/EXP-070-gluing-counterexample-factors"
CODE = ROOT / "problems/commutative-algebra/huneke-wiegand/code"
sys.path.insert(0, str(CODE))


def load(name: str, path: Path):
    sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def test_producer_and_auditor_agree_on_pham_ideal_times_principal_partner() -> None:
    cases = load("exp070_cases_t1", EXP070 / "gluing_cases.py")
    auditor = load("exp070_auditor_t1", EXP070 / "auditor.py")
    spec = cases.build_spec("B1", "<2,3>", (0,))
    assert (spec["a1"], spec["a2"]) == (2, 57)
    assert spec["factor_b"]["hw"] is False and spec["factor_b"]["length"] == 0
    produced = cases.case_job(spec)
    audited = auditor.audit_case(spec)
    assert produced["torsion_direct"] == produced["torsion_law"] == audited["torsion"] == 0
    assert produced["hw"] is False and audited["hw"] is False
    assert produced["mu"] == [2, 1, 2]
    assert produced["p1"] and produced["p2"] and produced["p4"]
    assert audited["frobenius"] == produced["frobenius_measured"]


def test_producer_and_auditor_agree_on_a_case_with_torsion_from_the_partner() -> None:
    cases = load("exp070_cases_t2", EXP070 / "gluing_cases.py")
    auditor = load("exp070_auditor_t2", EXP070 / "auditor.py")
    spec = cases.build_spec("B1", "<2,3>", (0, 1))
    produced = cases.case_job(spec)
    audited = auditor.audit_case(spec)
    assert produced["torsion_direct"] == produced["torsion_law"] == audited["torsion"]
    assert produced["torsion_law"] > 0
    assert produced["hw"] is True and audited["hw"] is True
    assert produced["p1"] and produced["p2"] and produced["p4"]


def test_auditor_files_share_no_code_with_the_producer_library() -> None:
    paths = [EXP070 / "auditor.py", EXP070.parent / "EXP-068-gluing-tensor-factorization" / "audit.py"]
    for path in paths:
        imports = [line for line in path.read_text(encoding="utf-8").splitlines()
                   if line.startswith(("import ", "from "))]
        assert imports, path
        assert not any("hwcert" in line or "gluing_cases" in line for line in imports), (path, imports)


def test_pair_count_equals_the_enumeration_of_tensor_torsion() -> None:
    cases = load("exp070_cases_t3", EXP070 / "gluing_cases.py")
    from hwcert.gluing import (Window, dual, ideal_from_generators, minimal_generators, semigroup_mask)

    gens, ideal_gens = (3, 5, 7), (0, 1)
    window = Window(-6, 120)
    sg = semigroup_mask(window, gens)
    ideal = ideal_from_generators(window, sg, ideal_gens)
    mingens = minimal_generators(window, ideal, gens)
    star = dual(window, sg, mingens)
    top = max(mingens) + window.tail_start(sg) + window.tail_start(star)
    a_min, s_min = window.first(ideal), window.first(star)
    brute = sum(1 for d in range(a_min + s_min, top + 1) for x in range(a_min, d - s_min + 1)
                if window.contains(ideal, x) and window.contains(star, d - x))
    assert cases.pair_count(window, sg, gens, ideal_gens)["pairs"] == brute > 0


def test_gluing_parameters_follow_the_hypothesis_rule() -> None:
    cases = load("exp070_cases_t4", EXP070 / "gluing_cases.py")
    pham = cases.BASES["B1"]["gens"]
    assert cases.gluing_parameters(pham, (3, 4)) == (3, 56)
    assert cases.gluing_parameters(pham, (4, 5, 6, 7)) == (4, 57)
    assert cases.gluing_parameters(pham, (2, 5)) == (2, 57)
