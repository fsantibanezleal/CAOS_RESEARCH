"""Tests of the table generator of the primitive-points manuscript (make_tables.py).

1. The bytes and the SHA-256 printed in the manifest table equal those of the blob committed at HEAD (so a checkout with CRLF line
   ends cannot make the table stale again).
2. `make_tables.py --check` reports every generated output current.
3. The guards on the artifacts of EXP-005, EXP-006 and EXP-007 stop the generator when an artifact differs from what the text
   relies on: a mutated copy (in a pytest tmp path) is refused, an unmutated copy is accepted.
"""
import importlib.util
import json
import re
import subprocess
import sys
import hashlib
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
MS = REPO / "manuscripts" / "boij-soderberg-realizability" / "primitive-points-realizability"


@pytest.fixture(scope="module")
def mt():
    spec = importlib.util.spec_from_file_location("bs_make_tables", MS / "make_tables.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["bs_make_tables"] = mod
    spec.loader.exec_module(mod)
    return mod


def _blob(rel):
    return subprocess.run(["git", "-C", str(REPO), "cat-file", "-p", f"HEAD:{rel}"], capture_output=True, check=True).stdout


def test_manifest_table_matches_committed_blobs(mt):
    text = (MS / "tab_manifests.tex").read_text(encoding="utf-8")
    rows = re.findall(r"\\texttt\{([^}]+)\}\s*&\s*(\d+)\s*&\s*\\texttt\{\\scriptsize ([0-9a-f]{32})\\allowbreak ([0-9a-f]{32})\}", text)
    assert [r[0] for r in rows] == [lab for lab, _ in mt.MANIFEST]
    for (label, size, h1, h2), (lab, rel) in zip(rows, mt.MANIFEST):
        blob = _blob(f"{mt.PROBLEM_REL}/{rel}")
        assert int(size) == len(blob), f"{label}: printed {size} bytes, committed blob {len(blob)}"
        assert h1 + h2 == hashlib.sha256(blob).hexdigest(), f"{label}: printed hash differs from the committed blob"


def test_hash_ignores_crlf(mt, tmp_path):
    p = tmp_path / "a.json"
    p.write_bytes(b'{"a": 1}\r\n{"b": 2}\r\n')
    q = tmp_path / "b.json"
    q.write_bytes(b'{"a": 1}\n{"b": 2}\n')
    assert mt.sha(p) == mt.sha(q) and len(mt.norm_bytes(p)) == len(q.read_bytes())
    r = tmp_path / "c.pdf"
    r.write_bytes(b"x\r\ny")
    assert mt.norm_bytes(r) == b"x\r\ny"


def test_check_reports_outputs_current():
    res = subprocess.run([sys.executable, str(MS / "make_tables.py"), "--check"], capture_output=True, text=True)
    assert res.returncode == 0, res.stderr
    assert "outputs current" in res.stdout


def _copy_problem(mt, tmp_path):
    root = tmp_path / "problem"
    for d in (mt.E5, mt.E6, mt.E7):
        dst = root / "experiments" / d.name / "artifacts"
        dst.mkdir(parents=True)
        (dst / "results.json").write_bytes((d / "artifacts" / "results.json").read_bytes())
    return root


def _run(mt, root):
    mt.FAILS.clear()
    try:
        mt.build_new(root, {})
        return list(mt.FAILS)
    finally:
        mt.FAILS.clear()


def _edit(root, d, fn):
    p = root / "experiments" / d.name / "artifacts" / "results.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    fn(data)
    p.write_text(json.dumps(data), encoding="utf-8", newline="\n")


def test_guards_accept_the_unmutated_artifacts(mt, tmp_path):
    assert _run(mt, _copy_problem(mt, tmp_path)) == []


def test_guard_exp006_refuses_a_changed_count(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    _edit(root, mt.E6, lambda d: d["totals"]["per_field"]["A1|GF(3)"].__setitem__("pure", 1945))
    assert any("A1|GF(3)" in f for f in _run(mt, root))


def test_guard_exp006_refuses_a_changed_pair(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)

    def mutate(d):
        for k, c in d["chunks"].items():
            if k.startswith("A1|GF(3)|"):
                for s in c["spaces"]:
                    if s.get("index") == 91:
                        s["basis"][1] = [list(t) for t in s["basis"][0]]  # g := f, so W has dimension 1
    _edit(root, mt.E6, mutate)
    fails = _run(mt, root)
    assert any("pair A1|GF(3)" in f for f in fails), fails


def test_guard_exp007_refuses_a_changed_tangent_dimension(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)

    def mutate(d):
        for row in d["statements"]["T1"]["rows"]:
            if row["e"] == 4:
                row["tangent_dim"] = 13
    _edit(root, mt.E7, mutate)
    assert any("EXP-007 T1 e=4" in f for f in _run(mt, root))


def test_guard_exp005_refuses_a_finite_length_case(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    _edit(root, mt.E5, lambda d: d["totals"]["per_family_field"]["C1b|GF(2)"].__setitem__("finite_length", 1))
    assert any("C1b|GF(2)" in f for f in _run(mt, root))
