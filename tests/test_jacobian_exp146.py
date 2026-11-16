"""Tests for EXP-146 (single-prime resultant-chain certificates with proven degree bounds, JCB-103).

Fast tests of the bound engine (M4), the degree-drop image formula (M5) and the tree on planted systems (G4 in
miniature). The production run and the real-system gates are in the experiment's run.py.
"""

import importlib
import itertools
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
EXP = (
    ROOT / "problems" / "algebraic-geometry" / "jacobian-conjecture" / "experiments"
    / "EXP-146-case1-chain-certificate"
)
sys.path.insert(0, str(EXP))
cc = importlib.import_module("chaincert")
gates = importlib.import_module("gates")

PRIME = cc.Prime(536870909, 505390653)


def test_hungarian_matches_bruteforce():
    rng = np.random.default_rng(1)
    for _ in range(300):
        n = int(rng.integers(1, 7))
        M = rng.integers(-5, 20, size=(n, n)).astype(np.int64)
        M[rng.random((n, n)) < 0.3] = cc.NEG
        best = max(sum(int(M[i, s[i]]) for i in range(n)) for s in itertools.permutations(range(n)))
        assert cc.max_assignment(M) == best


def test_bound_engine_random_pairs_never_under_bounds():
    st = gates.g2_random(300, seed=7)
    assert st["pass"], st
    assert st["weights_checked"] > 5000
    assert st["planted_cancel"] > 30 and st["planted_monomial"] > 30 and st["split_cases"] > 50
    assert st["formal_degree_above_actual"] > 0   # loose supports really occur


def test_negative_weight_gives_tight_order_bound_on_a_monomial_factor():
    """f = v^2 (x + 1), g = v (x - 2) with v the split variable: Res = (-3)... times v^3, so order 3."""
    from flint import fmpz_mpoly_ctx
    ctx = fmpz_mpoly_ctx.get(["x", "v"], "lex")
    x, v = ctx.gens()
    f, g = v**2 * (x + 1), v * (x - 2)
    split = 1
    Bf = cc.exact_bound(sorted(tuple(m) for m in f.monoms()), 2, split)
    Bg = cc.exact_bound(sorted(tuple(m) for m in g.monoms()), 2, split)
    assert Bf.low(split) == 2 and Bg.low(split) == 1
    mf, zf = cc.formal_degree(Bf, 0, split)
    ng, zg = cc.formal_degree(Bg, 0, split)
    Bh = cc.res_bound(Bf, mf, zf, Bg, ng, zg, 0, split, 2)
    h = f.resultant(g, "x")
    assert h != 0 and min(m[1] for m in h.monoms()) == 3
    assert Bh.low(split) == 3


def test_degree_drop_image_formula_one_planted_case():
    """phi of the exact formal resultant = M5 image formula, with the leading coefficient of f vanishing at r."""
    st = gates.g3_degree_drop(40, PRIME, seed=11)
    assert st["pass"], st
    assert any(k > 0 for k in st["drops"])


def test_planted_unit_system_is_certified_and_common_root_is_not():
    st = gates.g4_controls(PRIME)
    assert st["planted_unit_certified"] is True
    assert st["planted_common_root_certified"] is False
    assert st["pass"]


def test_exact_division_by_a_power_is_refused_when_not_exact():
    from flint import nmod_mpoly_ctx
    ctx = nmod_mpoly_ctx.get(["w"], modulus=PRIME.p)
    w = ctx.gen(0)
    assert cc.shift_down(w**3 + w**5, 0, 3) == 1 + w**2
    with pytest.raises(cc.BoundViolation):
        cc.shift_down(w**2 + w**5, 0, 3)


def test_constant_member_needs_proven_zero_degree_bounds_not_a_constant_image():
    """Coordinator reading of M6: a member is a constant only if B(e_x) = 0 for every variable; an image that
    happens to be constant (leading coefficients vanishing mod p) does not count."""
    from flint import nmod_mpoly_ctx
    ctx = nmod_mpoly_ctx.get(["a", "b"], modulus=PRIME.p)
    loose = cc.exact_bound([(2, 0), (0, 0)], 2, None)
    tight = cc.exact_bound([(0, 0)], 2, None)
    g_loose = cc.Mem("m", None, ctx.from_dict({(0, 0): 5}), loose, 1)
    g_tight = cc.Mem("m", None, ctx.from_dict({(0, 0): 5}), tight, 1)
    assert not cc.is_constant_member(g_loose, 2)
    assert cc.is_constant_member(g_tight, 2)


# ---------------------------------------------------------------------------------------------------------
# Fix pass 2026-11-16 (review findings F1 to F14)
# ---------------------------------------------------------------------------------------------------------

import subprocess  # noqa: E402

singular_eval = importlib.import_module("singular_eval")
PY = sys.executable


def _run_optimized(code):
    """Run `code` under python -O with the experiment on the path; returns the completed process."""
    prelude = f"import sys; sys.path.insert(0, {str(EXP)!r}); import chaincert as cc, numpy as np\n"
    return subprocess.run([PY, "-O", "-c", prelude + code], capture_output=True, text=True)


def test_f5_invariants_are_raises_that_survive_python_O():
    """The four invariants (Hungarian entry range, P(r) = 0, image degree <= formal degree, constant final
    resultant) raise BoundViolation, also under python -O (which removes asserts)."""
    code = (
        "import sys\n"
        "def t(f):\n"
        "    try:\n"
        "        f()\n"
        "    except cc.BoundViolation:\n"
        "        return 'raised'\n"
        "    return 'silent'\n"
        "from flint import nmod_mpoly_ctx\n"
        "ctx = nmod_mpoly_ctx.get(['x'], modulus=536870909)\n"
        "x = ctx.gen(0)\n"
        "out = [t(lambda: cc.max_assignment(np.array([[10**8]], dtype=np.int64))),\n"
        "       t(lambda: cc.Prime(536870909, 5)),\n"
        "       t(lambda: cc.res_image(x**3 + 1, x + 2, 0, 'x', 2, 536870909)),\n"
        "       t(lambda: cc.constant_value(x + 1, 1))]\n"
        "print(' '.join(out))\n"
    )
    r = _run_optimized(code)
    assert r.returncode == 0, r.stderr
    assert r.stdout.split() == ["raised"] * 4, r.stdout


def test_f11_hungarian_refuses_when_the_proven_zero_threshold_is_unsound():
    """The test val < DEAD_BELOW needs n * E < 4e8 (n the matrix size, E the largest finite entry)."""
    n = 50
    M = np.full((n, n), 9 * 10**6, dtype=np.int64)
    with pytest.raises(cc.BoundViolation):
        cc.max_assignment(M)
    small = np.full((30, 30), 10**6, dtype=np.int64)
    assert cc.max_assignment(small) == 30 * 10**6


def test_f7_pass_route_requires_an_image_free_of_x():
    from flint import nmod_mpoly_ctx
    ctx = nmod_mpoly_ctx.get(["x", "a"], modulus=PRIME.p)
    x, a = ctx.gens()
    # a bound that proves every coefficient of x^c, c >= 1, zero although B(e_x) = 1 (bogus on purpose)
    B = cc.Bd((0,), {(0,): 0, (1,): 1, (2,): 1, (3,): 1})
    m, z = cc.formal_degree(B, 0, None)
    assert B.deg(0) == 1 and m == 0
    good = cc.Mem("g", None, ctx.from_dict({(0, 1): 3}), B, 1)
    out = cc.pass_member(good, 0, None)
    assert out.id == "g"
    bad = cc.Mem("b", None, x + a, B, 1)
    with pytest.raises(cc.BoundViolation):
        cc.pass_member(bad, 0, None)


def test_f7_pass_route_checks_the_exact_support_too():
    ring = cc.NodeRing(["x", "a"])
    ex = ring.ex
    B = cc.Bd((0,), {(0,): 0, (1,): 1, (2,): 1, (3,): 1})
    img = cc.phi(ring, ex.from_dict({(0, 0, 1): 1}), PRIME)
    g = cc.Mem("g", ex.from_dict({(0, 1, 1): 1}), img, B, 1)   # exact polynomial contains x, image does not
    with pytest.raises(cc.BoundViolation):
        cc.pass_member(g, 0, None)


def _planted_rec(last, members):
    return {"id": "t", "last": last, "members": members, "steps": [], "inputs": [], "order": ["q"], "kind": "root",
            "parent": None}


def _dig(terms, degs, evals):
    return {"terms": terms, "degrees": degs, "eval": evals}


def test_f8_constant_member_line_is_compared():
    p = PRIME.p
    mem = {"E1": {"digest": _dig(1, [0], [77, 5])}}
    last = {"x": "q", "members": [], "pivot": None, "n": None, "pairs": [], "constant_member": "E1"}
    rec = _planted_rec(last, mem)
    ok_out = "DIG t E1 1 0 77 5\nCONST t E1 77\n"
    st = singular_eval.compare([rec], ok_out, PRIME)
    assert st["pass"] and st["constants_compared"] == 1
    st = singular_eval.compare([rec], "DIG t E1 1 0 77 5\n", PRIME)           # the CONST line is missing
    assert not st["pass"] and ["t", "E1"] in st["missing"]
    st = singular_eval.compare([rec], "DIG t E1 1 0 77 5\nCONST t E1 78\n", PRIME)   # a wrong value
    assert not st["pass"] and ["t", "E1"] in st["constant_mismatches"]
    st = singular_eval.compare([rec], "DIG t E1 1 0 77 5\nCONST t E1 0\n", PRIME)    # zero
    assert not st["pass"]
    neg = f"DIG t E1 1 0 {p - 77} {p - 5}\nCONST t E1 {p - 77}\n"                    # up to sign
    assert singular_eval.compare([rec], neg, PRIME)["pass"]


def test_f9_univariate_digests_and_the_final_pivot_degree_are_compared():
    mem = {"U": {"digest": _dig(2, [3], [11, 12])}}
    last = {"x": "q", "members": [{"id": "U", "L": 0, "d": 3, "img_deg": 3, "img_order": 0,
                                   "digest": _dig(2, [3], [21, 22])}],
            "pivot": "U", "n": 3, "pairs": [], "constant_member": None}
    rec = _planted_rec(last, mem)
    base = "DIG t U 2 3 11 12\nDIG t V_U 2 3 21 22\n"
    assert singular_eval.compare([rec], base, PRIME)["pass"]
    assert not singular_eval.compare([rec], "DIG t U 2 3 11 12\n", PRIME)["pass"]            # V digest missing
    st = singular_eval.compare([rec], "DIG t U 2 3 11 12\nDIG t V_U 2 3 21 23\n", PRIME)    # V digest perturbed
    assert not st["pass"] and ["t", "V_U"] in st["digest_mismatches"]
    st = singular_eval.compare([rec], base + "BAD_PIVOT_DEGREE t V_U\n", PRIME)             # flagged line
    assert not st["pass"]


def test_f9_script_prints_the_final_pivot_degree_check():
    rec = {"id": "t", "parent": None, "kind": "root", "order": ["q"], "inputs": ["E1"], "steps": [],
           "last": {"x": "q", "members": [{"id": "E1", "L": 0, "d": 2, "img_deg": 2, "img_order": 0}],
                    "pivot": "E1", "n": 2, "pairs": [], "constant_member": None},
           "members": {}, "transform": None}
    terms = {"E1": [([2], [1, 0, 0, 0, 0])]}
    txt = singular_eval.build_script([rec], terms, ["q"], PRIME)
    assert "BAD_PIVOT_DEGREE t V_E1" in txt


def test_f10_from_vectors_rejects_non_integers_and_repeated_monomials():
    ring = cc.NodeRing(["a", "b"])
    with pytest.raises(ValueError):
        ring.from_vectors([([1, 0], [2.7, 0, 0, 0, 0])])
    with pytest.raises(ValueError):
        ring.from_vectors([([1, 0], [True, 0, 0, 0, 0])])
    with pytest.raises(ValueError):
        ring.from_vectors([([1, 0], [1, 0, 0, 0, 0]), ([1, 0], [2, 0, 0, 0, 0])])
    with pytest.raises(ValueError):
        ring.from_vectors([([1, 0], [1, 0, 0])])
    assert ring.from_vectors([([1, 0], [1, 2, 0, 0, 0])]) != 0


def _branch_dict(names=("q5", "q3", "q4", "q2", "q0")):
    return {"names": list(names), "from": [3], "eqs": [[[[1] + [0] * (len(names) - 1), [1, 0, 0, 0, 0]]]]}


def test_f10_branch_input_checks():
    order = list(gates.ORDER)
    assert gates.check_branch_inputs(_branch_dict(), order)["pass"]
    d = _branch_dict()
    d["eqs"][0][0][1] = [2.0, 0, 0, 0, 0]
    assert not gates.check_branch_inputs(d, order)["pass"]
    d = _branch_dict()
    d["eqs"][0][0][1] = [True, 0, 0, 0, 0]
    assert not gates.check_branch_inputs(d, order)["pass"]
    d = _branch_dict()
    d["eqs"][0].append(list(d["eqs"][0][0]))                     # a repeated monomial
    assert not gates.check_branch_inputs(d, order)["pass"]
    d = _branch_dict(("q5", "q3", "q4", "q2", "q0", "zz"))      # an extra variable
    assert not gates.check_branch_inputs(d, order)["pass"]
    with pytest.raises(ValueError):
        gates.branch_inputs(d, cc.NodeRing(order))


def test_f10_g1_covers_both_branch_files():
    g1 = gates.g1_ring_maps(gates.second_prime())
    assert set(g1["inputs"]) == {"plus", "minus"}
    assert all(v["pass"] for v in g1["inputs"].values()) and g1["pass"]


# ---- F2: a crashing control can never pass G4 ----

def test_f2_crashing_control_is_recorded_as_crashed_and_fails_g4():
    crash = [PY, "-c", "import sys; sys.stderr.write('planted bug'); sys.exit(3)"]
    entry = gates.run_branch_control(0, 5, 20, argv=crash)
    assert entry["certified"] is None and entry["outcome"].startswith("crashed (returncode 3)")
    assert "planted bug" in entry["error"]
    assert gates.control_blocks_g4(entry)
    raising = [PY, "-c", "raise RuntimeError('boom')"]
    assert gates.control_blocks_g4(gates.run_branch_control(1, 5, 20, argv=raising))


def test_f2_a_finished_uncertified_control_and_a_timeout_do_not_block():
    line = 'print("NEGRESULT " + __import__("json").dumps({"removed": "E3", "certified": False, "nodes": []}))'
    ok = gates.run_branch_control(0, 5, 20, argv=[PY, "-c", line])
    assert ok["outcome"] == "finished" and ok["certified"] is False and not gates.control_blocks_g4(ok)
    slow = gates.run_branch_control(0, 5, 1, argv=[PY, "-c", "import time; time.sleep(30)"])
    assert slow["certified"] is None and slow["outcome"].startswith("inconclusive (killed at the")
    assert not gates.control_blocks_g4(slow)
    cert = {"removed": "E3", "certified": True, "outcome": "finished"}
    assert gates.control_blocks_g4(cert)
    silent = gates.run_branch_control(0, 5, 20, argv=[PY, "-c", "pass"])   # exit 0 but no NEGRESULT line
    assert gates.control_blocks_g4(silent) and silent["outcome"].startswith("crashed")


def test_f2_g4_fails_end_to_end_with_a_raising_child():
    st = gates.g4_controls(PRIME, branch_plus_path=gates.BRANCH["plus"], removal_cases=(0,), hard_seconds=20,
                           neg_argv=[PY, "-c", "raise RuntimeError('planted bug')"], extended_cases=(), nonempty=False)
    assert st["pass"] is False
    assert st["branch_minus_one_equation"][0]["outcome"].startswith("crashed")


# ---- F4: composition family and the planted split ----

def test_f4_composition_family_holds_and_its_mutant_fails():
    st = gates.g2_composition(150, seed=3)
    assert st["pass"], st
    assert st["composition_cases"] >= 20 and st["composition_weights"] > 500
    assert st["composition_violations"] == 0
    assert st["composition_mutant_violations"] > 0


def test_f13_g2_random_records_the_weight_checked_pairs():
    st = gates.g2_random(80, seed=5)
    assert st["pass"]
    assert st["weight_checked_pairs"] == st["cases"] - st["resultant_zero"]


def _split_system():
    """f1 = w x - 1 with w = a + b v: x eliminated against f1 gives multiples of w^2, so the root splits on w."""
    ring = cc.NodeRing(["x", "v"])
    ex = ring.ex
    y, x, v = ex.gens()
    w = (3 + y) + (2 - y**2) * v
    f1 = ring.reduce(w * x - 1)
    f2 = ring.reduce(w**2 * x**2 + 3)
    f3 = ring.reduce(w**2 * x**2 + w * x + 1)
    return ring, [("f1", f1), ("f2", f2), ("f3", f3)]


def test_f4_planted_split_exact_transform_project_and_replay():
    ring, ins = _split_system()
    ok, st = cc.solve_tree(ring.order, ins, PRIME, max_depth=2, node_seconds=60, log=lambda *_: None, tag="s")
    assert ok and st.counter == 1
    status = {r["id"]: r["status"] for r in st.records}
    assert status == {"s": "split", "s.nz": "certified", "s.z": "certified"}
    sp = st.records[0]["split"]
    y = ring.ex.gen(0)
    a = sum(c * y**i for i, c in enumerate(sp["a"]))
    b = sum(c * y**i for i, c in enumerate(sp["b"]))
    # exact_transform against substitution: w := a + b v in the transformed polynomial gives b^deg_v(f) f(v)
    for mid, f in ins:
        f2 = st.nodes["s.nz"]["inputs"][mid]
        sub = ring.ex.from_dict({})
        for mono, c in f2.to_dict().items():
            term = ring.ex.from_dict({(mono[0], mono[1], 0): int(c)})
            for _ in range(mono[2]):
                term = ring.reduce(term * (a + b * ring.ex.gen(2)))
            sub = sub + term
        sub = ring.reduce(sub)
        dv = max(m[2] for m in f.monoms())
        want = ring.reduce(b**dv * f)
        assert ring.reduce(sub - want) == 0, mid
    # project_w0 against w = 0 (setting the last variable of the transformed polynomial to 0)
    for mid, f in ins:
        f2 = st.nodes["s.nz"]["inputs"][mid]
        at0 = {k[:-1]: int(c) for k, c in f2.to_dict().items() if k[-1] == 0}
        proj = st.nodes["s.z"]["inputs"].get(mid)
        got = {k: int(c) for k, c in proj.to_dict().items()} if proj is not None else {}
        assert got == at0, mid
    # replay of every certified leaf at a second prime
    p2 = gates.second_prime()
    for r in st.records:
        if r["status"] == "certified":
            rp = cc.replay_leaf(st, r, p2)
            assert rp["certified"] and not rp["problems"], (r["id"], rp)


# ---- F1: controls with final pairs on nonempty nodes ----

def test_f1_node_stats_count_final_pairs_and_constant_checks():
    recs = [
        {"id": "n", "status": "split", "last": {"pairs": [{"c": 0}, {"c": 0}], "constant_member": None}},
        {"id": "n.nz", "status": "unknown", "last": {"pairs": [], "constant_member": None}},
        {"id": "n.z", "status": "certified", "last": {"pairs": [{"c": 5}], "constant_member": None}},
        {"id": "n.q", "status": "unknown", "last": None},
    ]
    stats = gates.node_pair_stats(recs)
    assert stats["n"]["final_pairs"] == 2 and stats["n"]["nonzero_pairs"] == 0
    assert stats["n.z"]["nonzero_pairs"] == 1 and "n.q" not in stats
    assert stats["n"]["constant_member"] is None


def test_f1_extended_control_verdict_needs_a_nonempty_node_with_two_zero_pairs():
    stats = {"a": {"final_pairs": 2, "nonzero_pairs": 0, "constant_member": None, "certified": False, "nonempty": True},
             "b": {"final_pairs": 3, "nonzero_pairs": 0, "constant_member": None, "certified": False, "nonempty": False}}
    assert gates.extended_control_ok(stats)
    stats["a"]["final_pairs"] = 1
    assert not gates.extended_control_ok(stats)                      # only one pair on the nonempty node
    stats["a"]["final_pairs"] = 2
    stats["a"]["certified"] = True
    assert not gates.extended_control_ok(stats)                      # a certificate on a nonempty node
    stats["a"]["certified"] = False
    stats["a"]["nonzero_pairs"] = 1
    assert not gates.extended_control_ok(stats)
    stats["a"]["nonzero_pairs"] = 0
    stats["a"]["constant_member"] = "X"
    assert not gates.extended_control_ok(stats)


requires_wsl = pytest.mark.skipif(subprocess.run(["wsl", "-e", "bash", "-lc", "command -v Singular"],
                                                 capture_output=True, text=True).returncode != 0,
                                  reason="Singular is not available under WSL")


@requires_wsl
def test_f1_singular_nonemptiness_distinguishes_a_point_from_the_unit_ideal():
    ring = cc.NodeRing(["x1", "x2"])
    y, x1, x2 = ring.ex.gens()
    d_point = gates.singular_dims({"p": (ring, [x1 - 1, x2 - 2], None)}, PRIME)
    d_unit = gates.singular_dims({"u": (ring, [x1 - 1, x1 - 2], None)}, PRIME)
    assert d_point["p"]["dim"] == 0 and d_unit["u"]["dim"] == -1
    d_nz = gates.singular_dims({"z": (ring, [x1 - 1, x2 - 2], x1 - 1)}, PRIME)   # I + (w s - 1), w = x1 - 1
    assert d_nz["z"]["dim"] == -1


# ---- F1 item 3, F3: planted_split_common end to end, per-node generator counts, a unit drop-one ideal fails G4 ----

@requires_wsl
def test_f1_planted_split_common_end_to_end_with_nonemptiness_and_generator_counts():
    res = gates.g4_controls(PRIME, branch_plus_path=None, nonempty=True)
    psc = res["planted_split_common"]
    assert psc["generators"] >= psc["variables"] + 2 and psc["certified"] is False
    assert psc["extended_ok"] is True and res["pass"] is True
    nodes = psc["nodes"]
    qualifying = gates.extended_control_qualifying(nodes)
    assert "psc" in qualifying and "psc.nz" in qualifying       # nonempty nodes with two zero final pairs
    for nid in qualifying:
        s = nodes[nid]
        assert s["nonempty"] is True and s["dim"] >= 0 and s["final_pairs"] >= 2 and s["nonzero_pairs"] == 0
        # F1 item 3: the generator count is recorded at every node, with n + 2 generators on the qualifying ones
        assert s["generators"] >= s["variables"] + 2, (nid, s)
    assert nodes["psc.z"]["nonempty"] is False and nodes["psc.z"]["dim"] == -1
    assert res["final_pair_summary"]["nonempty_nodes_with_two_zero_pairs"] >= 2


@requires_wsl
def test_f3_a_unit_drop_one_ideal_fails_the_nonemptiness_check_and_g4(monkeypatch, tmp_path):
    # planted defect: E9 added to the subset, so dropping E9 leaves the (unit) minimal subset
    monkeypatch.setattr(gates, "SUBSET", list(gates.SUBSET) + [9])
    ne = gates.branch_subset_nonemptiness({"p1": PRIME}, workdir=tmp_path)
    assert ne["pass"] is False and ne["p1"]["full"]["dim"] == -1
    assert ne["p1"]["drop9"]["dim"] == -1
    fake = [sys.executable, "-c", 'print("NEGRESULT " + \'{"removed": "E3", "certified": false, "nodes": []}\')']
    res = gates.g4_controls(PRIME, branch_plus_path=gates.BRANCH["plus"], removal_cases=(0,), neg_argv=fake,
                            extended_cases=[], nonempty=True, hard_seconds=60)
    assert res["branch_subset_nonemptiness"]["pass"] is False
    assert res["pass"] is False
