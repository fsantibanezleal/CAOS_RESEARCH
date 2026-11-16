"""EXP-147: does GGHV 2022 Theorem 5.1 apply to the three polygon classes of their Proposition 4.2 (the (9,24) case)?

Exact integer geometry on Newton polygons, with the starting and end points of a face defined as in GGV1 (arXiv:1401.1784,
Notation at lines 368 to 372): the first and the last point of the face met when running counterclockwise along the boundary.
Each pair (st, en) is also checked against GGV1's cross-product rule (rho, sigma) x (en - st) > 0 for a non-monomial face.

    python run.py [--out artifacts/results.json]

Exit 0 when the claims A1 to A4 hold for every class and every control behaves as the hypothesis states; 1 otherwise.
"""
from __future__ import annotations

import argparse
import json
from math import gcd
from pathlib import Path

HERE = Path(__file__).resolve().parent

# GGHV 2022 Proposition 4.2 (arXiv:2204.14178v1, lines 668 to 680): [P, Q] = x and one of three classes.
CLASSES = {
    1: ([(0, 0), (1, 1), (6, 16), (6, 18), (0, 12)], [(0, 0), (1, 0), (9, 24), (9, 27), (0, 18)]),
    2: ([(0, 0), (1, 1), (6, 16), (6, 18), (0, 6)], [(0, 0), (1, 0), (9, 24), (9, 27), (0, 9)]),
    3: ([(0, 0), (1, 1), (6, 16), (6, 18)], [(0, 0), (1, 0), (9, 24), (9, 27)]),
}
# Theorem 5.1 (lines 1402 to 1409), hypotheses (2) and (3).
TARGET_P = {"en_3,-1": (6, 16), "st_1,0": (6, 16), "st_-1,1": (6, 18), "en_1,0": (6, 18)}
TARGET_Q = {"en_3,-1": (9, 24), "st_1,0": (9, 24), "st_-1,1": (9, 27), "en_1,0": (9, 27)}


def cross(o, a, b):
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def hull_ccw(points):
    """Convex hull vertices in counterclockwise order (Andrew's monotone chain), collinear points dropped."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts
    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def face(hull, d):
    """Indices of the hull vertices that maximize v_d (one vertex, or the two endpoints of an edge)."""
    vals = [d[0] * p[0] + d[1] * p[1] for p in hull]
    top = max(vals)
    return [i for i, v in enumerate(vals) if v == top]


def st_en(hull, d, clockwise=False):
    """Start and end of the d-face met along the boundary walk (counterclockwise, as GGV1 defines them)."""
    idx = face(hull, d)
    if len(idx) == 1:
        return hull[idx[0]], hull[idx[0]]
    n = len(hull)
    i, j = idx
    # the two endpoints of an edge are consecutive on the hull; the counterclockwise walk meets first the one whose
    # successor is the other
    if (i + 1) % n == j:
        first, last = hull[i], hull[j]
    elif (j + 1) % n == i:
        first, last = hull[j], hull[i]
    else:
        raise ValueError("face endpoints are not consecutive")
    return (last, first) if clockwise else (first, last)


def cross_rule(d, st, en):
    """GGV1 Remark: for a non-monomial face, d x (en - st) > 0."""
    if st == en:
        return True
    dx, dy = en[0] - st[0], en[1] - st[1]
    return d[0] * dy - d[1] * dx > 0


def successor_of(hull, d):
    """The outward normal (coprime integers) of the edge that follows the d-face counterclockwise."""
    idx = face(hull, d)
    n = len(hull)
    if len(idx) == 1:
        k = idx[0]
    else:
        i, j = idx
        k = j if (i + 1) % n == j else i
    a, b = hull[k], hull[(k + 1) % n]
    ex, ey = b[0] - a[0], b[1] - a[1]
    nx, ny = ey, -ex  # outward normal of a counterclockwise edge
    g = gcd(abs(nx), abs(ny)) or 1
    return (nx // g, ny // g)


def measure(polygon, clockwise=False):
    hull = hull_ccw(polygon)
    out = {"hull_ccw": hull, "faces": {}, "cross_rule_ok": True}
    for name, d in (("3,-1", (3, -1)), ("1,0", (1, 0)), ("-1,1", (-1, 1))):
        st, en = st_en(hull, d, clockwise)
        out["faces"][name] = {"face": [hull[i] for i in face(hull, d)], "st": st, "en": en}
        if not clockwise and not cross_rule(d, st, en):
            out["cross_rule_ok"] = False
    out["successor_of_1,0"] = successor_of(hull, (1, 0))
    return out


def conditions(m, target):
    f = m["faces"]
    got = {"en_3,-1": f["3,-1"]["en"], "st_1,0": f["1,0"]["st"], "st_-1,1": f["-1,1"]["st"], "en_1,0": f["1,0"]["en"]}
    return {k: {"value": list(v), "target": list(target[k]), "holds": tuple(v) == target[k]} for k, v in got.items()}


def all_hold(c):
    return all(x["holds"] for x in c.values())


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(HERE / "artifacts" / "results.json"))
    a = ap.parse_args(argv)
    res = {"experiment": "EXP-147", "classes": {}, "controls": {}}
    ok = True
    for k, (np_, nq) in CLASSES.items():
        mp, mq = measure(np_), measure(nq)
        cp, cq = conditions(mp, TARGET_P), conditions(mq, TARGET_Q)
        a1 = all(x >= 0 and y >= 0 for x, y in np_ + nq)
        row = {"A1_first_quadrant": a1, "A2_g_zero": True,  # [P, Q] = x is the statement of Proposition 4.2
               "A3_P": cp, "A4_Q": cq, "A3": all_hold(cp), "A4": all_hold(cq),
               "cross_rule_ok": mp["cross_rule_ok"] and mq["cross_rule_ok"],
               "P": mp, "Q": mq}
        row["theorem_5_1_applies"] = a1 and row["A3"] and row["A4"] and row["cross_rule_ok"]
        ok &= row["theorem_5_1_applies"]
        res["classes"][str(k)] = row
    # K1: Corollary 5.7's polygon before the shift fails A3 with st_{-1,1}(P) = (0,18).
    k1 = conditions(measure([(0, 0), (1, 1), (6, 16), (6, 18), (0, 18)]), TARGET_P)
    res["controls"]["K1_cor57_unshifted"] = {"conditions": k1, "fails": not all_hold(k1),
                                             "st_-1,1": k1["st_-1,1"]["value"], "expected_st_-1,1": [0, 18]}
    k1_ok = (not all_hold(k1)) and k1["st_-1,1"]["value"] == [0, 18]
    # K2: the paper's usage at line 380: the (1,0)-face from (8,28) to (8,32) starts at (8,28).
    m2 = measure([(0, 0), (1, 0), (8, 28), (8, 32), (0, 8)])
    k2_ok = m2["faces"]["1,0"]["st"] == (8, 28) and m2["faces"]["1,0"]["en"] == (8, 32)
    res["controls"]["K2_line380_st"] = {"st_1,0": list(m2["faces"]["1,0"]["st"]), "en_1,0": list(m2["faces"]["1,0"]["en"]),
                                        "ok": k2_ok}
    # K3: the clockwise walk (the orientation mutant) fails A3 and A4 in every class.
    k3 = {}
    for k, (np_, nq) in CLASSES.items():
        cp = conditions(measure(np_, clockwise=True), TARGET_P)
        cq = conditions(measure(nq, clockwise=True), TARGET_Q)
        k3[str(k)] = {"A3_fails": not all_hold(cp), "A4_fails": not all_hold(cq)}
    k3_ok = all(v["A3_fails"] and v["A4_fails"] for v in k3.values())
    res["controls"]["K3_clockwise_mutant"] = {"per_class": k3, "ok": k3_ok}
    # K4: a planted violation: the (-1,1)-face is the vertex (2,18), so A3 fails.
    k4 = conditions(measure([(0, 0), (1, 1), (6, 16), (6, 18), (2, 18)]), TARGET_P)
    k4_ok = (not all_hold(k4)) and k4["st_-1,1"]["value"] == [2, 18]
    res["controls"]["K4_planted"] = {"conditions": k4, "ok": k4_ok}
    controls_ok = k1_ok and k2_ok and k3_ok and k4_ok
    res["controls_ok"] = controls_ok
    res["claims_hold"] = ok
    res["verdict"] = "CONFIRMED" if (ok and controls_ok) else ("NO VERDICT (controls failed)" if not controls_ok else "REFUTED")
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, indent=1, default=list) + "\n", encoding="utf-8")
    for k, row in res["classes"].items():
        print(f"class {k}: A1 {row['A1_first_quadrant']} A3 {row['A3']} A4 {row['A4']} cross-rule {row['cross_rule_ok']} "
              f"successor of (1,0): P {row['P']['successor_of_1,0']} Q {row['Q']['successor_of_1,0']}")
    print("controls:", {k: v.get("ok", v.get("fails")) for k, v in res["controls"].items()})
    print("VERDICT", res["verdict"])
    return 0 if res["verdict"] == "CONFIRMED" else 1


if __name__ == "__main__":
    raise SystemExit(main())
