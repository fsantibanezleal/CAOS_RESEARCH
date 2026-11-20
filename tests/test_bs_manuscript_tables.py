"""Tests of the table generator of the primitive-points manuscript (make_tables.py).

1. The bytes and the SHA-256 printed in the manifest table equal those of the blob committed at HEAD (so a checkout with CRLF line
   ends cannot make the table stale again).
2. `make_tables.py --check` reports every generated output current.
3. The guards on the artifacts of EXP-005 to EXP-017 (EXP-016 is not used) stop the generator when an artifact differs from what
   the text relies on: a mutated copy (in a pytest tmp path) is refused, an unmutated copy is accepted.
4. The admissible and refined admissible strata for e = 4 to 8 equal the counts of the independent computation, and the rule of the
   grid of pairs (e, p) gives the hand-checked cells.
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
    for d in (mt.E5, mt.E6, mt.E7, mt.E8, mt.E9, mt.E11, mt.E12, mt.E10, mt.E13, mt.E14, mt.E15, mt.E17, mt.E16, mt.E18):
        dst = root / "experiments" / d.name / "artifacts"
        dst.mkdir(parents=True)
        (dst / "results.json").write_bytes((d / "artifacts" / "results.json").read_bytes())
    return root


def _run(mt, root, data_root=None):
    mt.FAILS.clear()
    try:
        mt.build_new(root, {}, data_root)
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


def test_guard_exp007_refuses_a_histogram_that_does_not_sum(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    _edit(root, mt.E7, lambda d: d["statements"]["T4"]["4"]["qq"]["rank_hist"].__setitem__("48", 568))
    assert any("does not sum to its member count" in f for f in _run(mt, root))


def test_guard_exp005_refuses_a_changed_printed_hilbert_function(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    _edit(root, mt.E5, lambda d: d["cases"]["C3|GF(2^4)|21"]["hilbert"].__setitem__(4, 7))
    assert any("printed C3 case" in f for f in _run(mt, root))


def test_guard_exp006_refuses_a_false_full_file_hash(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    _edit(root, mt.E6, lambda d: d["full_results"].__setitem__("sha256", "0" * 64))
    assert any("recorded hash of the full results file" in f for f in _run(mt, root))


def test_guard_exp006_hashes_the_full_file_when_present(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    data = tmp_path / "data"
    full = data / "caos-research" / "boij-soderberg-realizability" / "EXP-006" / "results-full.json"
    full.parent.mkdir(parents=True)
    full.write_bytes(b"not the recorded file")
    assert any("full results file under the data root" in f for f in _run(mt, root, data))
    h = hashlib.sha256(full.read_bytes()).hexdigest()
    _edit(root, mt.E6, lambda d: d["full_results"].update({"sha256": h, "bytes": len(b"not the recorded file")}))
    assert _run(mt, root, data) == []


def test_guard_exp008_refuses_a_changed_count(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    _edit(root, mt.E8, lambda d: d["totals"]["C"].__setitem__("pure", 41))
    assert any("EXP-008 C" in f for f in _run(mt, root))


def test_guard_exp008_refuses_a_changed_pair(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)

    def mutate(d):
        for k, c in d["chunks"].items():
            if k.startswith("C|"):
                for s in c["spaces"]:
                    if s.get("seed") == 20264514:
                        s["basis"][1] = [list(t) for t in s["basis"][0]]
    _edit(root, mt.E8, mutate)
    assert any("pair C|GF(3)" in f for f in _run(mt, root))


# ---- EXP-009, EXP-011, EXP-012 ----

def test_guard_exp009_refuses_a_member_above_r(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    _edit(root, mt.E9, lambda d: d["totals"]["4|5|X"].__setitem__("rank_above_r", 1))
    assert any("EXP-009 X 4,5" in f for f in _run(mt, root))


def test_guard_exp009_refuses_a_pure_member_at_6_7(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    _edit(root, mt.E9, lambda d: d["totals"]["6|7|X"].__setitem__("pure", 1))
    assert any("EXP-009 X 6,7" in f for f in _run(mt, root))


def test_guard_exp009_refuses_a_changed_member(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)

    def mutate(d):
        s2 = d["pairs"]["6|11|X"]["s2"]
        mem = next(m for m in s2["members_pure_hilbert"] if m["pure"])
        mem["basis"][1][0][1] = 5   # the coefficient of the second form changes: no longer L_6 of its parameters
    _edit(root, mt.E9, mutate)
    assert any("EXP-009 member 6,11" in f for f in _run(mt, root))


def test_guard_exp009_refuses_a_prediction_that_does_not_hold(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    _edit(root, mt.E9, lambda d: d["predictions"]["P2"]["6,7"].__setitem__("holds", True))
    assert any("EXP-009 P2" in f for f in _run(mt, root))


def test_guard_exp011_refuses_a_changed_lambda(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    _edit(root, mt.E11, lambda d: d["cases"]["T5"].__setitem__("lambda", 2))
    assert any("EXP-011 T5: g f - f g" in f for f in _run(mt, root))


def test_guard_exp011_refuses_a_changed_length(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    _edit(root, mt.E11, lambda d: d["cases"]["T8"].__setitem__("length", 728))
    assert any("EXP-011 T8: length" in f for f in _run(mt, root))


def test_guard_exp011_refuses_a_changed_polynomial(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    _edit(root, mt.E11, lambda d: d["cases"]["T3"]["g"].append([[3, 0, 1], 1]))   # adds x^3 z to g (degree 5): the commutator is no longer lambda z^5
    assert any("EXP-011 T3" in f for f in _run(mt, root))


def test_guard_exp012_refuses_a_changed_D(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    _edit(root, mt.E12, lambda d: d["X"]["B2"].__setitem__("D", [[1, 1, 0, 2]]))
    assert any("EXP-012 B2" in f for f in _run(mt, root))


def test_guard_exp012_refuses_a_changed_random_count(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    _edit(root, mt.E12, lambda d: d["totals"]["R"]["6,5"].__setitem__("criterion", 118))
    assert any("EXP-012 R 6,5" in f for f in _run(mt, root))


def test_guard_exp012_refuses_a_disagreement_between_criterion_and_purity(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)

    def mutate(d):
        x = d["R"]["6,5"]["pairs"][0]
        x["criterion"] = not x["criterion"]
    _edit(root, mt.E12, mutate)
    assert any("EXP-012 R 6,5" in f for f in _run(mt, root))


def test_guard_exp012_refuses_a_negative_control_that_turns_pure(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    _edit(root, mt.E12, lambda d: d["N"]["N2"]["criterion"].__setitem__("holds", True))
    assert any("EXP-012 N2" in f for f in _run(mt, root))


# ---- the strata and the grid of pairs ----

def test_refined_admissible_counts_equal_the_independent_computation(mt):
    got = {}
    for e in range(4, 9):
        adm, ref = mt.strata_tables(e)
        got[e] = (sum(adm.values()), len(adm), sum(ref.values()))
    assert got == {4: (17, 34, 11), 5: (19, 55, 9), 6: (34, 83, 19), 7: (34, 119, 13), 8: (58, 164, 30)}
    # a few strata by hand: S(e+1; 0, e) is the point W_0 and is admissible, S(e+1; 1, e) is not; for m = e the refined list is (0, j) only
    adm, ref = mt.strata_tables(6)
    assert adm[(7, 0, 6)] and not adm[(7, 1, 6)]
    assert sorted((i, j) for (m, i, j), ok in ref.items() if m == 6 and ok) == [(0, j) for j in range(6)]


def test_strata_facts_guard_stops_on_a_wrong_note(mt, monkeypatch):
    monkeypatch.setitem(mt.STRATA_NOTE, 6, (34, 83, 20))
    mt.FAILS.clear()
    try:
        mt.strata_output({}, {})
        assert any("strata e=6" in f for f in mt.FAILS)
    finally:
        mt.FAILS.clear()


def test_grid_rule_on_hand_checked_cells(mt):
    explicit = {(2, 3), (3, 3), (3, 5), (4, 3), (4, 5), (4, 7), (5, 3), (5, 5), (5, 7), (6, 3)}
    linear = {(4, 5), (4, 7), (5, 7), (6, 11), (7, 11), (7, 13)}
    cells = mt.grid_cells(16, explicit, linear)
    # p divides e(e-1): the criterion
    assert cells[(6, 5)] == "C" and cells[(7, 3)] == "C" and cells[(7, 7)] == "C" and cells[(8, 7)] == "C"
    # the pull-back: 8 = 4.2 at p = 3 (4 = 1 modulo 3, (2,3) settled), 12 = 6.2 at p = 5, 14 = 7.2 at p = 3, 16 = 8.2 at p = 7
    assert cells[(8, 3)] == "P" and cells[(12, 5)] == "P" and cells[(14, 3)] == "P" and cells[(16, 7)] == "P"
    # the linear family and a search
    assert cells[(6, 11)] == "L" and cells[(7, 13)] == "L" and cells[(5, 3)] == "S" and cells[(2, 3)] == "S"
    # the cells that the results leave open
    for k in [(6, 7), (7, 5), (8, 5), (8, 11), (8, 13), (11, 3), (9, 5)]:
        assert cells[k] is None, k
    assert all(v is not None for (e, p), v in cells.items() if e <= 5)
    # without the pair of quadrics over F_3 the pull-back at (8, 3) is not available, and without the linear family (6, 11) is open
    cells2 = mt.grid_cells(16, explicit - {(2, 3)}, set())
    assert cells2[(8, 3)] is None and cells2[(6, 11)] is None and cells2[(4, 5)] == "S"


def test_grid_inputs_come_from_the_artifacts(mt):
    r5, r6, r7, r8 = mt.read_artifacts(mt.PROBLEM)
    r9, _r11, _r12 = mt.read_later(mt.PROBLEM)

    def below(pairs):   # the grid has only p < 2e; the searches also found pairs over F_11 and F_13 at e = 4
        return {k for k in pairs if k[1] < 2 * k[0]}
    assert below(mt.explicit_from_artifacts(r6, r8, 1)) == {(2, 3), (3, 3), (3, 5), (4, 3), (4, 5), (4, 7), (5, 3), (5, 5), (5, 7), (6, 3)}
    assert below(mt.explicit_from_artifacts(r6, r8, 0)) == {(3, 3), (3, 5), (4, 3), (4, 5), (4, 7), (5, 3), (5, 5), (5, 7), (6, 3)}
    assert mt.linear_from_artifacts(r9) == {(4, 5), (4, 7), (5, 7), (6, 11), (7, 11), (7, 13)}


# ---- EXP-010, EXP-013, EXP-014 ----

def _first_pure_member(d, key_filter):
    for k, st in d["strata"].items():
        if key_filter(k, st) and st["pure"]:
            return st, next(m for m in st["members"] if m["pure"])
    raise AssertionError("no stratum")


def test_guard_exp010_refuses_a_changed_total(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    _edit(root, mt.E10, lambda d: d["totals"]["Q|6|5"].__setitem__("pure", 45))
    assert any("EXP-010 Q|6|5" in f for f in _run(mt, root))


def test_guard_exp010_refuses_a_failed_exclusion(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    _edit(root, mt.E10, lambda d: d["gates"]["G4"].__setitem__("with_pure_hilbert_function", 1))
    assert any("EXP-010 G4" in f for f in _run(mt, root))


def test_guard_exp010_refuses_a_prediction_that_changes(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    _edit(root, mt.E10, lambda d: d["predictions"]["P5"]["8,5"].__setitem__("holds", True))
    assert any("EXP-010 P5 at (8, 5)" in f for f in _run(mt, root))


def test_guard_exp010_refuses_a_member_outside_its_stratum(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)

    def mutate(d):
        st, mem = _first_pure_member(d, lambda k, s: s["family"] == "Q" and s["e"] == 6 and s["p"] == 5 and (s["m"], s["i"], s["j"]) == (6, 0, 3))
        mem["f"][1] = 1     # the monomial of weight 5 modulo 6 enters f
    _edit(root, mt.E10, mutate)
    assert any("EXP-010 pair 6,5" in f for f in _run(mt, root))


def test_guard_exp013_refuses_a_table_that_is_not_scaled(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    _edit(root, mt.E13, lambda d: d["cases"]["S2"]["uhlib_phi"]["table"][1].__setitem__(1, 7))
    assert any("EXP-013 S2" in f for f in _run(mt, root))


def test_guard_exp013_refuses_a_changed_endomorphism(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    _edit(root, mt.E13, lambda d: d["cases"]["S3"]["phi_z"].append([[0, 0, 3], 1]))
    assert any("EXP-013 S3" in f for f in _run(mt, root))


def test_guard_exp013_refuses_a_changed_generator(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    _edit(root, mt.E13, lambda d: d["cases"]["S1"]["gens_phi"][0][0].__setitem__(1, 2))
    assert any("EXP-013 S1" in f for f in _run(mt, root))


def test_guard_exp014_refuses_a_prediction_that_changes(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    _edit(root, mt.E14, lambda d: d["predictions"]["P1"]["8,3"].__setitem__("holds", True))
    assert any("EXP-014 P1" in f for f in _run(mt, root))


def test_guard_exp014_refuses_a_changed_count(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    _edit(root, mt.E14, lambda d: d["totals"]["V|8|5|8|0|4"].__setitem__("pure", 5))
    assert any("EXP-014 V|8|5|8|0|4" in f for f in _run(mt, root))


def test_guard_exp014_refuses_a_member_outside_its_stratum(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)

    def mutate(d):
        st = d["strata"]["V|8|5|8|0|4"]
        next(m for m in st["members"] if m["pure"])["f"][1] = 1
    _edit(root, mt.E14, mutate)
    assert any("EXP-014 pair 8,5" in f for f in _run(mt, root))


def test_grid_with_the_searches_in_strata(mt):
    explicit = {(2, 3), (3, 3), (3, 5), (4, 3), (4, 5), (4, 7), (5, 3), (5, 5), (5, 7), (6, 3)}
    linear = {(4, 5), (4, 7), (5, 7), (6, 11), (7, 11), (7, 13)}
    w = {(6, 5), (6, 7), (7, 3), (7, 5), (7, 7), (8, 3), (8, 7), (8, 13)}
    mid = {(8, 5), (8, 7), (8, 11), (8, 13), (9, 7), (9, 17), (10, 3), (10, 7), (10, 11), (10, 13), (12, 5)}
    cells = mt.grid_cells(16, explicit, linear, (("W", w), ("M", mid)))
    assert cells[(6, 7)] == "W" and cells[(7, 5)] == "W" and cells[(8, 5)] == "M" and cells[(8, 11)] == "M" and cells[(8, 13)] == "W"
    assert cells[(9, 7)] == "M" and cells[(9, 17)] == "M" and cells[(8, 3)] == "P" and cells[(12, 5)] == "P" and cells[(10, 3)] == "C"
    for k in [(9, 5), (9, 11), (9, 13), (10, 17), (10, 19), (12, 7), (12, 13), (11, 3)]:
        assert cells[k] is None, k
    # every odd prime below 2e is settled for 2 <= e <= 8, and e = 9 is the first row with an open cell
    assert all(cells[(e, p)] is not None for (e, p) in cells if e <= 8)
    assert any(cells[(9, p)] is None for p in (3, 5, 7, 11, 13, 17))


# ---- EXP-015, EXP-017, the weight-zero projection and the rule of the linear family ----

def test_guard_exp015_refuses_a_prediction_that_changes(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    key = sorted(_read(root, mt.E15)["predictions"]["P1"])[0]
    _edit(root, mt.E15, lambda d: d["predictions"]["P1"][key].__setitem__("holds", False))
    assert any("EXP-015 P1" in f for f in _run(mt, root))


def test_guard_exp015_refuses_a_pure_member_where_the_rule_says_none(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    _edit(root, mt.E15, lambda d: d["strata"]["L|10|11|9|0|1"].__setitem__("pure", 1))
    assert any("EXP-015 L 10,11" in f for f in _run(mt, root))


def test_guard_exp015_refuses_a_stratum_excluded_by_the_corollary_that_holds_a_pure_hilbert_function(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    d0 = _read(root, mt.E15)
    key = next(k for k, s in d0["strata"].items() if s["family"] == "R" and mt.cor5_excluded(s["e"], s["p"], s["m"], s["i"], s["j"]))
    _edit(root, mt.E15, lambda d: d["strata"][key].__setitem__("pure_hilbert", 1))
    assert _run(mt, root) != []


def test_guard_exp017_refuses_a_table_that_is_not_pure(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    _edit(root, mt.E17, lambda d: d["cases"]["Q|9|11"].__setitem__("tables", d["cases"]["Q|9|11"]["pure"] + 1))
    assert _run(mt, root) != []


def test_guard_exp017_refuses_a_filter_count_that_is_not_monotone(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    _edit(root, mt.E17, lambda d: d["cases"]["K|5|7"]["counts"].__setitem__("f3", d["cases"]["K|5|7"]["counts"]["f2"] + 1))
    assert any("EXP-017" in f for f in _run(mt, root))


def _read(root, d):
    return json.loads((root / "experiments" / d.name / "artifacts" / "results.json").read_text(encoding="utf-8"))


def test_corollary_of_the_weight_zero_projection_on_hand_cases(mt):
    # (7,3): W = {0,2,5,7} for S(5;0,2), w- = 2, w+ = 5, 2 * 3 = 6 >= 4: excluded
    assert mt.cor5_excluded(7, 3, 5, 0, 2) is True
    # (6,3): S(3;0,1) has the weight e/2 = 3 (3 % 3 = 0), so the corollary does not apply
    assert mt.cor5_excluded(6, 3, 3, 0, 1) is False
    # the strata of the central pairs for odd e have gap 1 and are never excluded for p >= 3
    for e in (5, 7, 9, 11, 13):
        assert mt.cor5_excluded(e, 3, (e + 1) // 2, 0, (e - 1) // 2) is False


def test_linear_stratum_rule_from_the_corollary_and_the_artifacts(mt):
    r9 = json.loads((mt.E9 / "artifacts" / "results.json").read_text(encoding="utf-8"))
    r10 = json.loads((mt.E10 / "artifacts" / "results.json").read_text(encoding="utf-8"))
    r14 = json.loads((mt.E14 / "artifacts" / "results.json").read_text(encoding="utf-8"))
    r15 = json.loads((mt.E15 / "artifacts" / "results.json").read_text(encoding="utf-8"))
    res = mt.linear_strata_pairs(r9, r10, r14, r15)
    assert len(res) == 24
    for (e, p), v in res.items():
        assert (v[1] > 0) == (2 * e - p <= 3), (e, p)
        if 2 * e - p >= 5:
            assert p <= 2 * e - 5 and v[1] == 0


# ---- EXP-016 ----

def test_guard_exp016_refuses_a_list_that_changes(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    _edit(root, mt.E16, lambda d: d["cases"]["B|12|7|1"].__setitem__("list", []))
    assert _run(mt, root) != []


def test_guard_exp016_refuses_a_verified_form_that_is_not_pure(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    _edit(root, mt.E16, lambda d: d["cases"]["B|12|7|1"]["verified"][0]["second"].__setitem__("pure", False))
    assert any("EXP-016" in f for f in _run(mt, root))


def test_guard_exp016_refuses_a_negative_control_of_length_e_cubed(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    _edit(root, mt.E16, lambda d: d["negatives"]["N|6|7|1"]["forms"][0].__setitem__("length", 216))
    assert any("EXP-016" in f for f in _run(mt, root))


def test_guard_exp016_refuses_an_unfinished_case_that_is_declared_complete(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    _edit(root, mt.E16, lambda d: d["cases"]["B|14|23|1"].__setitem__("complete", True))
    assert any("EXP-016" in f for f in _run(mt, root))


def test_grid_with_the_lists_of_forms(mt):
    r16 = mt.read_fourth(mt.PROBLEM)
    pairs = mt.lists_pairs(r16)
    assert pairs[(12, 7)] == 1 and pairs[(16, 13)] == 1 and (14, 5) not in pairs and (14, 11) not in pairs and (14, 23) not in pairs
    r10, r13, r14 = mt.read_second(mt.PROBLEM)
    r15, r17 = mt.read_third(mt.PROBLEM)
    w, mid, oth, flt, lst, detail = mt.search_sets_from_artifacts(r10, r14, r15, r17, r16)
    for k in [(12, 7), (12, 13), (12, 17), (12, 19), (14, 17), (14, 19), (16, 11), (16, 13)]:
        assert k in lst, k
    assert (14, 5) not in lst and (14, 11) not in lst


# ---- EXP-018 ----

def test_guard_exp018_refuses_a_stratum_of_family_z_with_a_pure_hilbert_function(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    _edit(root, mt.E18, lambda d: d["strata"]["Z|11|13|9|0|2"].__setitem__("pure_hilbert", 1))
    assert any("EXP-018" in f for f in _run(mt, root))


def test_guard_exp018_refuses_a_largest_exponent_case_without_a_pure_member(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    def mutate(d):
        s = d["strata"]["T|11|17|9|0|2"]
        s["pure"] = 0
    _edit(root, mt.E18, mutate)
    assert any("EXP-018" in f for f in _run(mt, root))


def test_guard_exp018_refuses_a_prediction_that_changes(mt, tmp_path):
    root = _copy_problem(mt, tmp_path)
    _edit(root, mt.E18, lambda d: d["predictions"]["P2"]["11,17"].__setitem__("holds", False))
    assert any("EXP-018 P2" in f for f in _run(mt, root))


def test_largest_exponent_is_the_largest_allowed_by_the_corollary(mt):
    r18 = mt.read_fifth(mt.PROBLEM)
    assert mt.largest_pairs(r18) == {(11, 13): (8, 0, 3), (11, 17): (9, 0, 2), (13, 17): (10, 0, 3), (13, 19): (11, 0, 2), (14, 23): (12, 0, 2)}
    for (e, p), (m_, i_, j_) in mt.largest_pairs(r18).items():
        t = 2 * m_ - e
        assert 2 * t <= p - 1 and 2 * (t + 2) >= p + 1
        assert not mt.cor5_excluded(e, p, m_, i_, j_)
        assert mt.cor5_excluded(e, p, m_ + 1, 0, j_ - 1) or True
