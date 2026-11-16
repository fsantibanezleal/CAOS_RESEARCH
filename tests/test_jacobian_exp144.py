"""Fast tests for EXP-144 (exact in-house check of Long's rank-two Poisson counterexample)."""

import importlib.util
import sys
from pathlib import Path

import pytest
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
EXP = (
    ROOT / "problems" / "algebraic-geometry" / "jacobian-conjecture" / "experiments"
    / "EXP-144-long-poisson-exact-check"
)


def load(name):
    if str(EXP) not in sys.path:
        sys.path.insert(0, str(EXP))
    spec = importlib.util.spec_from_file_location(name, EXP / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def lg():
    return load("exp144_long")


def test_R_expands_to_lemma_3_1(lg):
    x, q = lg.x, lg.q
    assert sp.expand(lg.R - x * (2 - 3 * x * q)) == 0


def test_checker_reports_control_C1_as_failure(lg):
    ok, _ = lg.poisson_symbolic(lg.R, lg.T, lg.D0_poly_as_D(), lg.S)
    assert ok is False
    # {D0, R} = 1 still holds (the paper's (44))
    assert sp.expand(lg.bracket(lg.D0, lg.R) - 1) == 0


def test_printed_fiber_point_satisfies_four_equations(lg):
    pt = {lg.x: 1, lg.q: sp.Rational(2, 3), lg.p: sp.Rational(247, 96), lg.z: -sp.Rational(89, 64)}
    vals = [lg.R.subs(pt), (lg.T - sp.Rational(1, 8)).subs(pt), lg.D.subs(pt), lg.S.subs(pt)]
    assert vals == [0, 0, 0, 0]


def test_P2_symbolic_bracket_matrix_of_RTDS_equals_canonical(lg):
    got = lg.bracket_matrix((lg.R, lg.T, lg.D, lg.S))
    want = lg.target_matrix()
    # the canonical matrix pinned explicitly over (x, q, p, z): {x,p} = -1, {q,z} = -1 and their transposes (F4)
    assert [[sp.expand(v) for v in row] for row in want] == [[0, 0, -1, 0], [0, 0, 0, -1], [1, 0, 0, 0], [0, 1, 0, 0]]
    assert all(sp.expand(got[i][j] - want[i][j]) == 0 for i in range(4) for j in range(4))
    ok, bad = lg.poisson_symbolic(lg.R, lg.T, lg.D, lg.S)
    assert ok is True and bad == []


def test_control_C2_constant_126_makes_P2_checker_fail(lg):
    assert lg.D_C2 != lg.D
    assert sp.expand(lg.D_C2 - lg.D - lg.y ** 4 / 20) == 0  # exactly the 125 to 126 change of H (F4)
    ok, bad = lg.poisson_symbolic(lg.R, lg.T, lg.D_C2, lg.S)
    assert ok is False and len(bad) > 0


# ---- fix pass (verification findings F1 to F4) ------------------------------------------------------
import hashlib
import json
import os
import shutil
import subprocess

RUN_PY = "run.py"
ARTIFACT_FILES = ("results.json", "run-log.txt", "addendum-1.json", "polynomials.txt")


def _copy_experiment(tmp_path):
    dst = tmp_path / "exp"
    shutil.copytree(EXP, dst, ignore=shutil.ignore_patterns("__pycache__"))
    return dst


def _run(exp, *args, timeout=900):
    return subprocess.run([sys.executable, str(exp / RUN_PY), *args], capture_output=True, text=True,
                          timeout=timeout, env={k: v for k, v in os.environ.items()
                                                if k != "CAOS_RESEARCH_DATA_ROOT"})


def _digest(exp):
    art = exp / "artifacts"
    return {f.name: hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(art.iterdir()) if f.is_file()}


def test_F2_wrong_data_root_exits_2_and_writes_nothing(tmp_path):
    exp = _copy_experiment(tmp_path)
    before = _digest(exp)
    r = _run(exp, "--data-root", str(tmp_path / "nonexistent"))
    assert r.returncode == 2
    assert "MISSING source PDF" in r.stdout
    assert _digest(exp) == before  # no file under artifacts/ created, changed or removed


def test_F5_no_data_root_exits_2_with_a_message_and_writes_nothing(tmp_path):
    exp = _copy_experiment(tmp_path)
    before = _digest(exp)
    r = _run(exp)  # no --data-root and CAOS_RESEARCH_DATA_ROOT removed from the environment
    assert r.returncode == 2
    assert "no data root" in r.stdout
    assert _digest(exp) == before


def test_F1_missing_pinned_baseline_exits_2_and_writes_nothing(tmp_path):
    exp = _copy_experiment(tmp_path)
    (exp / "artifacts" / "results-pre-addendum-1.json").unlink()
    before = _digest(exp)
    r = _run(exp, "--data-root", str(tmp_path / "nonexistent"))
    assert r.returncode == 2
    assert "baseline" in r.stdout
    assert _digest(exp) == before


def test_F1_changed_pinned_baseline_exits_2_and_writes_nothing(tmp_path):
    exp = _copy_experiment(tmp_path)
    base = exp / "artifacts" / "results-pre-addendum-1.json"
    data = json.loads(base.read_text(encoding="utf-8"))
    data["P4_quotient_dimension"] = 4
    base.write_text(json.dumps(data, indent=2), encoding="utf-8")
    before = _digest(exp)
    r = _run(exp, "--data-root", str(tmp_path / "nonexistent"))
    assert r.returncode == 2
    assert "baseline" in r.stdout and "differs" in r.stdout
    assert _digest(exp) == before


def test_F1_baseline_is_the_pre_addendum_record_with_its_hash_pinned():
    base = EXP / "artifacts" / "results-pre-addendum-1.json"
    src = (EXP / RUN_PY).read_text(encoding="utf-8")
    sha = hashlib.sha256(base.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
    assert sha in src
    keys = set(json.loads(base.read_text(encoding="utf-8")))
    assert len(keys) == 23 and "P4_quotient_dimension" in keys and "python_version" not in keys


@pytest.mark.skipif(not os.environ.get("CAOS_RESEARCH_DATA_ROOT"),
                    reason="needs the data root with the source PDF (slow full run, about 80 s)")
def test_F3_forced_comparison_failure_makes_the_result_FAIL(tmp_path):
    # Alter one recorded value in the baseline and re-pin its hash in the copy: the predictions all pass, the
    # comparison fails; the log, the exit code and results.json must agree on FAIL.
    exp = _copy_experiment(tmp_path)
    base = exp / "artifacts" / "results-pre-addendum-1.json"
    old_sha = hashlib.sha256(base.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
    data = json.loads(base.read_text(encoding="utf-8"))
    data["P4_quotient_dimension"] = 4
    base.write_bytes(json.dumps(data, indent=2).encode("utf-8"))
    new_sha = hashlib.sha256(base.read_bytes()).hexdigest()
    run_py = exp / RUN_PY
    run_py.write_text(run_py.read_text(encoding="utf-8").replace(old_sha, new_sha), encoding="utf-8")
    r = _run(exp, "--data-root", os.environ["CAOS_RESEARCH_DATA_ROOT"])
    log = (exp / "artifacts" / "run-log.txt").read_text(encoding="utf-8")
    res = json.loads((exp / "artifacts" / "results.json").read_text(encoding="utf-8"))
    assert r.returncode == 1
    assert "RESULT: FAIL" in log and "RESULT: PASS" not in log
    assert "addendum 1: recorded values not reproduced" in res["failures"]
    assert log.index("addendum 1 comparison") < log.index("RESULT:")

