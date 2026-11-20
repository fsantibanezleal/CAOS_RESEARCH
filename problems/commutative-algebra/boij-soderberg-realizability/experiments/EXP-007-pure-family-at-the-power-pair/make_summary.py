"""EXP-007: the statements T1 to T6 and the predictions P1 to P6 as counts, and results-summary.md, all from results.json.

Nothing here is typed by hand: every number of results-summary.md is computed from the case records of artifacts/results.json.
The outcomes are reported against the hypothesis; no statement about smoothness, irreducibility or novelty is made here (the
coordinating session writes the verdict).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import exp007_routine as R  # noqa: E402

BIG = "GF(32003)"
T2_KEYS = [(4, "GF(13)"), (4, "GF(17)"), (4, BIG), (5, "GF(13)"), (5, "GF(17)"), (5, BIG), (6, "GF(13)"), (6, "GF(17)"), (6, BIG),
           (7, "GF(17)"), (7, BIG)]
T3_NAMES = ("W0_e4", "W0_e5", "P1", "P2", "P3", "P4", "P5", "C1", "C2")


def _c(res, cid):
    return res["cases"].get(cid)


def _complete(rec):
    return rec is not None and not rec.get("unfinished")


def statements(res):
    out = {}
    # T1
    rows = []
    for e in (4, 5, 6, 7):
        r = _c(res, "T1|QQ|e%d" % e)
        if r is not None:
            rows.append({"e": e, "rank_A": r["rank_A"], "r": r["target_rank_r"], "dim_K": r["dim_K"], "coker_dim": r["coker_dim"],
                         "coker_expected": r["coker_expected_h_e_3e"], "rank_T": r["rank_T"], "tangent_dim": r["tangent_dim"],
                         "bound": r["tangent_bound_4e_minus_4"], "orbit_in_tangent": r["orbit_directions_in_tangent_space"],
                         "orbit_rank": r["orbit_directions_rank"], "matrix": [r["rows_A"], r["cols_A"]],
                         "coordinates": r["coordinates"], "holds": r["holds"]})
    out["T1"] = {"rows": rows, "complete": len(rows) == 4}
    # T2
    rows = []
    for e, f in T2_KEYS:
        r = _c(res, "T2|%s|e%d" % (f, e))
        if r is not None:
            rows.append({"e": e, "field": f, "rank_A": r["rank_A"], "r": r["target_rank_r"], "dim_K": r["dim_K"], "coker_dim": r["coker_dim"],
                         "rank_T": r["rank_T"], "tangent_dim": r["tangent_dim"], "expected": r["expected_tangent_dim"],
                         "orbit_in_tangent": r["orbit_directions_in_tangent_space"], "holds": r["holds"]})
    out["T2"] = {"rows": rows, "complete": len(rows) == len(T2_KEYS)}
    # T3
    rows = []
    g3 = {r["name"]: r for r in res["gates"].get("G3", {}).get("rows", [])}
    for n in T3_NAMES:
        r = _c(res, "T3|%s" % n)
        if r is not None:
            rows.append({"name": n, "e": r["e"], "text": r["text"], "rank_mu_3e": r["rank_mu_3e"], "r": r["target_rank_r"], "betti_I1": r["betti"],
                         "pure": r["pure"], "finite_length": r.get("finite_length"), "dim_S": r["orbit"]["dim_S"],
                         "dim_S_plus_W": r["orbit"]["dim_S_plus_W"], "outside_orbit": r["orbit"]["outside_orbit"],
                         "expected": r["expected"], "holds_first": r["holds_first_instrument"],
                         "nonzero_to_24": r.get("nonzero_in_every_degree_to_24"), "g3": g3.get(n)})
    out["T3"] = {"rows": rows, "complete": len(rows) == len(T3_NAMES)}
    # T4
    t4 = {}
    for e in (4, 5):
        q = _c(res, "T4|QQ|e%d" % e)
        chunks = [c for k, c in res["cases"].items() if k.startswith("T4|%s|e%d|" % (BIG, e))]
        ent = {"qq": None, "gf": None}
        if q is not None:
            ent["qq"] = {"members": q["members_done"], "planned": q["members_planned"], "rank_hist": q["rank_hist"], "rank_le_r": q["rank_le_r"],
                         "above_r": len(q["members_above_r"]), "failing": q["members_above_r"][:3], "unfinished": q["unfinished"]}
        if chunks:
            mem = sorted((m for c in chunks for m in c["members"]), key=lambda m: m["index"])
            r = R.target_rank(e)
            hist = {}
            for m in mem:
                hist[str(m["rank_mu_3e"])] = hist.get(str(m["rank_mu_3e"]), 0) + 1
            ent["gf"] = {"members": len(mem), "planned": 200, "rank_hist": {k: hist[k] for k in sorted(hist, key=int)},
                         "rank_le_r": sum(1 for m in mem if m["rank_mu_3e"] <= r), "pure": sum(1 for m in mem if m["pure"]),
                         "outside_orbit": sum(1 for m in mem if m["outside_orbit"]),
                         "pure_and_outside": sum(1 for m in mem if m["pure"] and m["outside_orbit"]),
                         "not_pure_and_outside": [m for m in mem if not (m["pure"] and m["outside_orbit"])][:3],
                         "unfinished": any(c.get("unfinished") for c in chunks) or len(chunks) < 4}
        t4[str(e)] = ent
    out["T4"] = t4
    # T5
    g = _c(res, "T5|grid")
    p = _c(res, "T5|pure")
    out["T5"] = {"grid": None if g is None else {k: g[k] for k in ("spaces_done", "spaces_planned", "plane_points", "rank_le_48", "rank_hist",
                                                                   "points_on_plane", "mismatches", "unfinished", "holds")},
                 "pure": None if p is None else [{"name": s["name"], "rank_mu_3e": s["rank_mu_3e"], "betti": s["betti"], "pure": s["pure"],
                                                  "equation_value": s["equation_value"], "text": s["text"]} for s in p["spaces"]]}
    # T6
    t6 = {}
    for e, d in ((4, 1), (5, 2), (6, 4)):
        r = _c(res, "T6|e%d|d%d" % (e, d))
        if r is not None:
            hist = {}
            for s in r["spaces"]:
                hist[str(s["rank_mu_3e"])] = hist.get(str(s["rank_mu_3e"]), 0) + 1
            t6[str(e)] = {"d": d, "spaces": r["spaces_done"], "planned": r["spaces_planned"], "r": r["target_rank_r"], "rank_le_r": r["rank_le_r"],
                          "rank_hist": {k: hist[k] for k in sorted(hist, key=int)}, "infinite_length": r["infinite_length_count"],
                          "failing": [s for s in r["spaces"] if not s["rank_le_r"] or (e == 4 and not s["nonzero_in_every_degree_to_24"])][:3],
                          "unfinished": r["unfinished"], "holds": r["holds"]}
    out["T6"] = t6
    return out


def predictions(res):
    S = res.get("statements") or statements(res)
    P = {}
    # P1
    t1 = S["T1"]
    P["P1"] = {"holds": all(r["holds"] for r in t1["rows"]) if t1["complete"] else None,
               "outcome": "; ".join("e=%d: rank A %d (r %d), dim K %d, coker %d (h_e(3e) %d), tangent dimension %d (4e-4 = %d), orbit directions inside %s"
                                    % (r["e"], r["rank_A"], r["r"], r["dim_K"], r["coker_dim"], r["coker_expected"], r["tangent_dim"], r["bound"],
                                       r["orbit_in_tangent"]) for r in t1["rows"]),
               "undecided": [] if t1["complete"] else ["T1 cases missing"]}
    # P2
    t2 = S["T2"]
    P["P2"] = {"holds": all(r["holds"] for r in t2["rows"]) if t2["complete"] else None,
               "outcome": "; ".join("e=%d %s: %d (hypothesis %d)" % (r["e"], r["field"], r["tangent_dim"], r["expected"]) for r in t2["rows"]),
               "failing": [r for r in t2["rows"] if not r["holds"]], "undecided": [] if t2["complete"] else ["T2 cases missing"]}
    # P3
    t3 = S["T3"]
    first = all(r["holds_first"] for r in t3["rows"]) if t3["complete"] else None
    g3 = res["gates"].get("G3")
    second = None
    if g3 is not None and not g3.get("blocked"):
        second = bool(g3["passed"])
    holds = None if first is None else (False if first is False else second)
    P["P3"] = {"holds": holds, "first_instrument": first, "second_instrument_G3": second,
               "outcome": "; ".join("%s: rank mu_3e %d, %s, orbit %d to %d%s" % (
                   r["name"], r["rank_mu_3e"], "pure" if r["pure"] else ("not pure" + ("" if r["finite_length"] else ", infinite length")),
                   r["dim_S"], r["dim_S_plus_W"], ", outside" if r["outside_orbit"] else ", inside") for r in t3["rows"]),
               "failing": [r for r in t3["rows"] if not r["holds_first"]],
               "undecided": [] if (t3["complete"] and second is not None) else ["second instrument not run or blocked" if second is None else "T3 cases missing"]}
    # P4
    t4 = S["T4"]
    ok, parts, und = [], [], []
    for e in ("4", "5"):
        ent = t4.get(e, {})
        qq, gf = ent.get("qq"), ent.get("gf")
        if qq is None or gf is None or qq["unfinished"] or gf["unfinished"]:
            und.append("T4 e=%s incomplete" % e)
            continue
        ok.append(qq["rank_le_r"] == 625 and gf["rank_le_r"] == 200 and gf["pure_and_outside"] >= 190)
        parts.append("e=%s: QQ rank <= r for %d of %d; GF(32003) rank <= r for %d of %d, pure and outside the orbit %d of %d (threshold 190)"
                     % (e, qq["rank_le_r"], qq["members"], gf["rank_le_r"], gf["members"], gf["pure_and_outside"], gf["members"]))
    P["P4"] = {"holds": (all(ok) if not und and len(ok) == 2 else None), "outcome": "; ".join(parts), "undecided": und}
    # P5
    g = S["T5"]["grid"]
    pu = S["T5"]["pure"]
    und = [] if (g is not None and not g["unfinished"] and pu is not None) else ["T5 incomplete"]
    holds5 = None if und else (g["holds"] and all(s["pure"] for s in pu))
    P["P5"] = {"holds": holds5,
               "outcome": "" if g is None else "grid: %d spaces, %d on the plane, %d with rank mu_12 <= 48, %d contradicting the equation; pure on the plane directions: %s" % (
                   g["spaces_done"], g["plane_points"], g["rank_le_48"], len(g["mismatches"]),
                   ", ".join("%s %s" % (s["name"], "pure" if s["pure"] else "NOT pure") for s in (pu or []))),
               "undecided": und}
    # P6
    t6 = S["T6"]
    und = [] if len(t6) == 3 and not any(v["unfinished"] for v in t6.values()) else ["T6 incomplete"]
    P["P6"] = {"holds": None if und else all(v["holds"] for v in t6.values()),
               "outcome": "; ".join("e=%s (common factor of degree %d): rank mu_3e <= %d for %d of %d spaces%s" % (
                   e, v["d"], v["r"], v["rank_le_r"], v["spaces"],
                   ("; nonzero in every degree up to 24 for %d" % v["infinite_length"]) if e == "4" else "") for e, v in t6.items()),
               "undecided": und}
    return P


def _tab(rows):
    return "none" if rows is None else "; ".join("b_%d,%d = %d" % tuple(r) for r in rows)


def table_text(res):
    P = res["predictions"]
    L = []
    for g in ("G1", "G2", "G3", "G4"):
        r = res["gates"].get(g)
        L.append("%s: %s" % (g, "not run" if r is None else ("BLOCKED" if r.get("blocked") else ("PASSED" if r["passed"] else "FAILED"))))
    for k, v in P.items():
        L.append("%s: holds=%s | %s%s" % (k, v["holds"], v["outcome"], ("  UNDECIDED: " + "; ".join(v["undecided"])) if v.get("undecided") else ""))
    return "\n".join(L)


def _yn(x):
    return "n/a" if x is None else ("yes" if x else "NO")


def write_summary(res, path):
    S, P = res["statements"], res["predictions"]
    L = ["# EXP-007 results summary", "",
         "Generated by make_summary.py from artifacts/results.json; every number below is computed, none is typed.",
         "Hypothesis: hypothesis.md (frozen). Outcomes against the hypothesis only: no statement about smoothness, irreducibility or novelty.", ""]
    L += ["## Gates", ""]
    for g in ("G1", "G2", "G3", "G4"):
        r = res["gates"].get(g)
        if r is None:
            L.append("- %s: not run" % g)
        elif r.get("blocked"):
            L.append("- %s: BLOCKED, %s" % (g, r["reason"]))
        else:
            extra = ""
            if g == "G1":
                extra = " (%s)" % "; ".join("e=%d %s, rank mu_3e %d, r %d" % (c["e"], "pure" if c["pure"] else "NOT pure", c["rank_mu_3e"], c["r"]) for c in r["cases"])
            if g == "G2":
                extra = " (%s)" % "; ".join("%s %dx%d rank %d: dimension %d (expected %d)" % (c["field"], c["shape"][0], c["shape"][1], c["rank"], c["tangent_dim"],
                                                                                          c["expected_dimension"]) for c in r["cases"])
            if g == "G3":
                extra = " (%s; %d spaces, %d agree: %s)" % (r["singular"], r["spaces"], r["agree"], "; ".join(
                    "%s %s" % (x["name"], "agree" if x.get("agree") else "DISAGREE/ERROR") for x in r["rows"]))
            if g == "G4":
                extra = " (%s)" % r["last_line"]
            L.append("- %s: %s%s" % (g, "PASSED" if r["passed"] else "FAILED", extra))
    L += ["", "## T1: tangent space of D_e at W_0 over the rationals", "",
          "| e | A (rows x cols) | rank A | r | dim K | coker | h_e(3e) | chart coordinates | rank T | tangent dim | 4e-4 | orbit directions in it (rank) | holds |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in S["T1"]["rows"]:
        L.append("| %d | %d x %d | %d | %d | %d | %d | %d | %d | %d | %d | %d | %s (%d) | %s |" % (
            r["e"], r["matrix"][0], r["matrix"][1], r["rank_A"], r["r"], r["dim_K"], r["coker_dim"], r["coker_expected"], r["coordinates"], r["rank_T"],
            r["tangent_dim"], r["bound"], _yn(r["orbit_in_tangent"]), r["orbit_rank"], _yn(r["holds"])))
    L += ["", "## T2: tangent space in positive characteristic", "",
          "| e | field | rank A | r | dim K | coker | rank T | tangent dim | hypothesis | holds |", "|---|---|---|---|---|---|---|---|---|---|"]
    for r in S["T2"]["rows"]:
        L.append("| %d | %s | %d | %d | %d | %d | %d | %d | %d | %s |" % (r["e"], r["field"], r["rank_A"], r["r"], r["dim_K"], r["coker_dim"], r["rank_T"],
                                                                         r["tangent_dim"], r["expected"], _yn(r["holds"])))
    L += ["", "## T3: explicit pairs over the rationals and controls (polynomials in PBW monomials x^i y^j z^k; yx = xy - z)", ""]
    for r in S["T3"]["rows"]:
        g3 = r["g3"]
        sec = "second instrument not run" if g3 is None else ("Singular: %s (%s)" % (
            _tab(g3.get("betti_I2")) if r["name"] != "C2" else "Hilbert function to degree 24 " + ("equal" if g3.get("agree") else "DIFFERENT"),
            "agrees" if g3.get("agree") else "DISAGREES"))
        L.append("- %s (e = %d): f = %s ; g = %s ; rank mu_3e = %d (r = %d); uhlib: %s%s; orbit: dim S_e = %d, dim (S_e + W) = %d, %s; %s; first-instrument hypothesis statement: %s (%s)" % (
            r["name"], r["e"], r["text"][0], r["text"][1], r["rank_mu_3e"], r["r"], _tab(r["betti_I1"]) if r["betti_I1"] is not None else "no finite Betti table (infinite length)",
            "" if r["nonzero_to_24"] is None else "; H nonzero in every degree to 24: " + _yn(r["nonzero_to_24"]), r["dim_S"], r["dim_S_plus_W"],
            "outside the orbit" if r["outside_orbit"] else "inside the orbit", sec, _yn(r["holds_first"]), r["expected"]))
    L += ["", "## T4: the linear family L_e(a, b, c, d)", ""]
    for e, ent in S["T4"].items():
        qq, gf = ent["qq"], ent["gf"]
        if qq:
            L.append("- e = %s, QQ, (a, b, c, d) in {-2..2}^4: %d of %d members done; rank mu_3e <= r: %d; rank histogram: %s; members above r: %d" % (
                e, qq["members"], qq["planned"], qq["rank_le_r"], ", ".join("%s: %d" % kv for kv in qq["rank_hist"].items()), qq["above_r"]))
        if gf:
            L.append("- e = %s, GF(32003), random (a, b, c, d) with seeds 20261120 + index (index 0..199): %d members; rank mu_3e <= r: %d; pure: %d; "
                     "outside the orbit: %d; pure and outside: %d (threshold 190); rank histogram: %s" % (
                         e, gf["members"], gf["rank_le_r"], gf["pure"], gf["outside_orbit"], gf["pure_and_outside"],
                         ", ".join("%s: %d" % kv for kv in gf["rank_hist"].items())))
            for m in gf["not_pure_and_outside"]:
                L.append("    - not pure or not outside: index %d, (a, b, c, d) = %s, rank %d, pure %s, outside %s, Betti %s ; f = %s ; g = %s" % (
                    m["index"], m["abcd"], m["rank_mu_3e"], m["pure"], m["outside_orbit"], _tab(m["betti"]), m["text"][0] if "text" in m else "", m["text"][1] if "text" in m else ""))
    L += ["", "## T5: the plane section at e = 4", ""]
    g = S["T5"]["grid"]
    if g:
        L.append("- grid alpha, beta, gamma in {-4..4}, QQ: %d of %d spaces; points on 8 alpha + 31 beta + 118 gamma = 0: %d (%s); with rank mu_12 <= 48: %d; "
                 "rank histogram: %s; contradicting the equation: %d" % (
                     g["spaces_done"], g["spaces_planned"], g["plane_points"], ", ".join("(%d,%d,%d)" % tuple(p) for p in g["points_on_plane"]), g["rank_le_48"],
                     ", ".join("%s: %d" % kv for kv in g["rank_hist"].items()), len(g["mismatches"])))
        for m in g["mismatches"][:5]:
            L.append("    - mismatch (alpha, beta, gamma) = (%d, %d, %d), rank mu_12 = %d" % tuple(m))
    for s in S["T5"]["pure"] or []:
        L.append("- %s: equation value %d; rank mu_12 = %d; Betti table %s; pure: %s; f = %s" % (s["name"], s["equation_value"], s["rank_mu_3e"], _tab(s["betti"]),
                                                                                                _yn(s["pure"]), s["text"][0]))
    L += ["", "## T6: the common-factor locus over GF(32003)", ""]
    for e, v in S["T6"].items():
        L.append("- e = %s, common factor of degree %d: %d of %d spaces; rank mu_3e <= %d for %d; rank histogram: %s%s" % (
            e, v["d"], v["spaces"], v["planned"], v["r"], v["rank_le_r"], ", ".join("%s: %d" % kv for kv in v["rank_hist"].items()),
            ("; nonzero in every degree up to 24: %d" % v["infinite_length"]) if e == "4" else ""))
    L += ["", "## Predictions as outcomes", ""]
    for k, v in P.items():
        L.append("- %s: holds = %s. %s%s" % (k, _yn(v["holds"]), v["outcome"], (" Undecided: " + "; ".join(v["undecided"]) + ".") if v.get("undecided") else ""))
    L += ["", "Wall time of the commands: " + ", ".join("%s %.0f s" % (r["command"], r["seconds"]) for r in res["runs"])
          + "; total %.0f s." % res.get("wall_seconds_total", 0), ""]
    Path(path).write_text("\n".join(L), encoding="utf-8", newline="\n")
