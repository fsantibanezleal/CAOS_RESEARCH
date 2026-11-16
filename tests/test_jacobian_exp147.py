"""EXP-147: GGHV Theorem 5.1 against the polygon classes of Proposition 4.2 (the (9,24) case)."""
import importlib.util
import json
from pathlib import Path

EXP = Path(__file__).resolve().parents[1] / "problems/algebraic-geometry/jacobian-conjecture/experiments/EXP-147-gghv-924-bridge"


def load():
    spec = importlib.util.spec_from_file_location("exp147_run", EXP / "run.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_hull_is_counterclockwise_and_faces_of_a_square():
    r = load()
    h = r.hull_ccw([(0, 0), (2, 0), (2, 2), (0, 2), (1, 1)])
    assert h == [(0, 0), (2, 0), (2, 2), (0, 2)]
    assert r.st_en(h, (1, 0)) == ((2, 0), (2, 2))  # counterclockwise: up the right side
    assert r.st_en(h, (0, 1)) == ((2, 2), (0, 2))  # leftwards along the top
    assert r.st_en(h, (1, 1)) == ((2, 2), (2, 2))  # a vertex
    assert r.st_en(h, (1, 0), clockwise=True) == ((2, 2), (2, 0))


def test_cross_rule_matches_the_walk_on_every_edge_of_a_polygon():
    r = load()
    h = r.hull_ccw([(0, 0), (1, 1), (6, 16), (6, 18), (0, 12)])
    for d in ((3, -1), (1, 0), (-1, 1), (0, 1), (-1, 0), (1, -1)):
        st, en = r.st_en(h, d)
        assert r.cross_rule(d, st, en)


def test_every_class_satisfies_theorem_5_1(tmp_path):
    r = load()
    assert r.main(["--out", str(tmp_path / "res.json")]) == 0
    res = json.loads((tmp_path / "res.json").read_text(encoding="utf-8"))
    assert res["verdict"] == "CONFIRMED"
    for k in ("1", "2", "3"):
        assert res["classes"][k]["theorem_5_1_applies"] is True


def test_successor_directions_after_the_vertex_6_18():
    r = load()
    expected = {1: (-1, 1), 2: (-2, 1), 3: (-3, 1)}
    for k, (np_, nq) in r.CLASSES.items():
        assert r.successor_of(r.hull_ccw(np_), (1, 0)) == expected[k]
        assert r.successor_of(r.hull_ccw(nq), (1, 0)) == expected[k]


def test_controls_fail_or_hold_as_declared():
    r = load()
    k1 = r.conditions(r.measure([(0, 0), (1, 1), (6, 16), (6, 18), (0, 18)]), r.TARGET_P)
    assert not r.all_hold(k1) and k1["st_-1,1"]["value"] == [0, 18]
    m2 = r.measure([(0, 0), (1, 0), (8, 28), (8, 32), (0, 8)])
    assert m2["faces"]["1,0"]["st"] == (8, 28)
    for np_, nq in r.CLASSES.values():
        assert not r.all_hold(r.conditions(r.measure(np_, clockwise=True), r.TARGET_P))
        assert not r.all_hold(r.conditions(r.measure(nq, clockwise=True), r.TARGET_Q))
    k4 = r.conditions(r.measure([(0, 0), (1, 1), (6, 16), (6, 18), (2, 18)]), r.TARGET_P)
    assert not r.all_hold(k4)
