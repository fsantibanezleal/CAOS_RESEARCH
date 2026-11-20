"""EXP-005: the totals per family and per prediction from artifacts/results.json, and results-summary.md generated from them.

`python make_summary.py` rewrites results-summary.md from results.json (recomputing the totals); `run.py table` calls
compute_totals, stores the totals in results.json and then write_summary.  Nothing in the summary is typed by hand
except the fixed wording of the headings and of the reading notes.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import exp005_routine as R  # noqa: E402

FAMILY_ORDER = ["C1a", "C1b", "C1c", "C2a", "C2b", "C2c", "C2d", "C2e", "C2f", "C2g", "C3"]
FIELD_ORDER = ["GF(2)", "GF(2^2)", "GF(2^4)"]


def _done(records):
    return [r for r in records if r["status"] == "done"]


def compute_totals(res):
    cases = list(res["cases"].values())
    t = {"per_family_field": {}, "per_family": {}, "c3_per_shape": {}, "predictions": {}, "c4": {}}
    for fam in FAMILY_ORDER:
        recs = [r for r in cases if r["family"] == fam]
        if not recs:
            continue
        t["per_family"][fam] = R.family_counts(recs)
        for f in FIELD_ORDER:
            sub = [r for r in recs if r["field"] == f]
            if sub:
                t["per_family_field"]["%s|%s" % (fam, f)] = R.family_counts(sub)
    for shape in R.C3_SHAPES:
        sub = [r for r in cases if r["family"] == "C3" and tuple([r["a"], r["b"], r["e"]]) == shape]
        t["c3_per_shape"][str(shape)] = R.family_counts(sub)
    # P1
    c12 = [r for r in cases if r["family"].startswith(("C1", "C2"))]
    d12 = _done(c12)
    fin = [r["id"] for r in d12 if r["cls"] == R.FINITE]
    t["predictions"]["P1"] = {"cases_done": len(d12), "finite_length": len(fin), "finite_ids": fin, "holds": not fin and bool(d12)}
    # P2
    b1 = _done([r for r in c12 if r["b"] == r["a"] + 1])
    const = [r for r in b1 if r["cls"] == R.CONSTANT]
    right = [r for r in const if r["value"] == R.s2_value(r["a"], r["e"])]
    wrong = [[r["id"], r["value"], R.s2_value(r["a"], r["e"])] for r in const if r["value"] != R.s2_value(r["a"], r["e"])]
    uncl = [r["id"] for r in b1 if r["cls"] == R.UNCLASSIFIED]
    g16 = [r for r in b1 if r["family"].startswith("C2") and r["field"] == "GF(2^4)"]
    g16grow = [r for r in g16 if r["cls"] == R.GROWING]
    c1c = _done([r for r in cases if r["family"] == "C1c"])
    per_fam_growth = {}
    for fam in FAMILY_ORDER:
        sub = [r for r in g16 if r["family"] == fam]
        if sub:
            per_fam_growth[fam] = [sum(r["cls"] == R.GROWING for r in sub), len(sub)]
    t["predictions"]["P2"] = {
        "cases_b_eq_a_plus_1_done": len(b1), "eventually_constant": len(const), "constant_with_S2_value": len(right),
        "constant_with_other_value": wrong, "unclassified": len(uncl), "unclassified_ids": uncl,
        "gf16_cases": len(g16), "gf16_growing": len(g16grow), "gf16_growing_share": (len(g16grow) / len(g16)) if g16 else None,
        "gf16_growing_by_family": per_fam_growth,
        "growing_by_field": {f: [sum(r["cls"] == R.GROWING for r in b1 if r["field"] == f), sum(1 for r in b1 if r["field"] == f)]
                             for f in FIELD_ORDER},
        "c1c_cases_done": len(c1c), "c1c_growing": sum(r["cls"] == R.GROWING for r in c1c),
        "holds_value": not wrong and bool(const), "holds_no_unclassified": not uncl,
        "holds_gf16_share": (len(g16grow) <= 0.05 * len(g16)) if g16 else None,
        "holds_c1c_all_grow": bool(c1c) and all(r["cls"] == R.GROWING for r in c1c)}
    # P3
    p3 = {}
    for shape, c in t["c3_per_shape"].items():
        p3[shape] = {"cases": c["cases"], "finite_length": c["finite_length"], "unfinished": c["unfinished"], "holds": c["finite_length"] >= 8}
    t["predictions"]["P3"] = p3
    # P4
    p4, wrong4 = {}, []
    for key, r in sorted(res.get("c4", {}).items()):
        e, f = r["e"], r["field"]
        predicted_pure = f == "QQ" or (int(f[3:-1]) >= 2 * e)
        observed_pure = bool(r["pure_table_I1"]) and r.get("pure_table_I2") is True
        p4[key] = {"e": e, "field": f, "predicted_pure": predicted_pure, "pure_I1": r["pure_table_I1"], "pure_I2": r.get("pure_table_I2"),
                   "finite_length": r["finite_length"], "hilbert_equals_pure_prediction": r["hilbert_equals_pure_prediction"],
                   "tables_agree_I1_I2": r.get("tables_agree"), "matches_prediction": predicted_pure == observed_pure}
        if predicted_pure != observed_pure:
            wrong4.append(key)
    t["predictions"]["P4"] = {"modules": len(p4), "per_module": p4, "wrong_side": wrong4, "holds": bool(p4) and not wrong4}
    t["gates"] = {g: {"passed": v.get("passed")} for g, v in res.get("gates", {}).items()}
    return t


def totals_text(t):
    lines = ["family|field: cases, finite length, eventually constant (values), growing, unclassified, unfinished"]
    for key, c in t["per_family_field"].items():
        lines.append("%s: %d, %d, %d %s, %d, %d, %d" % (key, c["cases"], c["finite_length"], c["eventually_constant"],
                                                         json.dumps(c["constant_values"]), c["growing"], c["unclassified"], c["unfinished"]))
    for shape, c in t["c3_per_shape"].items():
        lines.append("C3 shape %s: %d, %d, %d, %d, %d, %d" % (shape, c["cases"], c["finite_length"], c["eventually_constant"],
                                                              c["growing"], c["unclassified"], c["unfinished"]))
    for p in ("P1", "P2", "P3", "P4"):
        pv = t["predictions"][p]
        if p == "P3":
            lines.append("P3: " + "; ".join("%s %d of %d finite" % (s, v["finite_length"], v["cases"]) for s, v in pv.items()))
        elif p == "P4":
            lines.append("P4: %d modules, %d on the wrong side" % (pv["modules"], len(pv["wrong_side"])))
        elif p == "P1":
            lines.append("P1: %d finite length of %d done cases of C1 and C2" % (pv["finite_length"], pv["cases_done"]))
        else:
            lines.append("P2: %d of %d (b = a + 1) constant, %d with the S2 value, %d other, %d unclassified; GF(16) growing %d of %d; C1c growing %d of %d"
                         % (pv["eventually_constant"], pv["cases_b_eq_a_plus_1_done"], pv["constant_with_S2_value"],
                            len(pv["constant_with_other_value"]), pv["unclassified"], pv["gf16_growing"], pv["gf16_cases"],
                            pv["c1c_growing"], pv["c1c_cases_done"]))
    return "\n".join(lines)


def _yn(v):
    return "holds" if v else "does not hold" if v is not None else "not applicable"


def write_summary(res, path):
    t = res.get("totals") or compute_totals(res)
    L = ["# EXP-005 results summary", "",
         "Generated from `artifacts/results.json` by `make_summary.py`; never edited by hand. The hypothesis is `hypothesis.md` (frozen). "
         "Counts only: the verdict is written by the coordinating session.", ""]
    L += ["## Gates", "", "| Gate | Outcome | Counts |", "|---|---|---|"]
    for g in ("G1", "G2", "G3", "G4"):
        v = res.get("gates", {}).get(g)
        if v is None:
            L.append("| %s | not run | |" % g)
            continue
        detail = {k: x for k, x in v.items() if k not in ("passed",)}
        L.append("| %s | %s | `%s` |" % (g, "PASSED" if v["passed"] else "FAILED", json.dumps(detail)))
    L += ["", "## Totals per family and field", "",
          "| Family | Field | Cases | Finite length | Eventually constant | By value | Growing | Unclassified | Unfinished |", "|---|---|---|---|---|---|---|---|---|"]
    for key, c in t["per_family_field"].items():
        fam, f = key.split("|")
        L.append("| %s | %s | %d | %d | %d | `%s` | %d | %d | %d |" % (fam, f, c["cases"], c["finite_length"], c["eventually_constant"],
                                                                      json.dumps(c["constant_values"]), c["growing"], c["unclassified"], c["unfinished"]))
    L += ["", "## C3 per shape (a, b, e)", "", "| Shape | Cases | Finite length | Eventually constant | Growing | Unclassified | Unfinished |", "|---|---|---|---|---|---|---|"]
    for shape, c in t["c3_per_shape"].items():
        L.append("| %s | %d | %d | %d | %d | %d | %d |" % (shape, c["cases"], c["finite_length"], c["eventually_constant"], c["growing"], c["unclassified"], c["unfinished"]))
    pr = t["predictions"]
    p1, p2, p3, p4 = pr["P1"], pr["P2"], pr["P3"], pr["P4"]
    L += ["", "## Predictions", "",
          "- P1 (no case of C1 or C2 has finite length): %s. %d finite length of %d done cases." % (_yn(p1["holds"]), p1["finite_length"], p1["cases_done"]),
          "- P2 (b = a + 1 cases): value clause %s: %d eventually constant, %d with the S2 value, %d with another value; no unclassified: %s (%d); "
          "GF(16) share growing: %s (%d of %d, share %s); C1c all grow: %s (%d of %d)."
          % (_yn(p2["holds_value"]), p2["eventually_constant"], p2["constant_with_S2_value"], len(p2["constant_with_other_value"]),
             _yn(p2["holds_no_unclassified"]), p2["unclassified"], _yn(p2["holds_gf16_share"]), p2["gf16_growing"], p2["gf16_cases"],
             p2["gf16_growing_share"], _yn(p2["holds_c1c_all_grow"]), p2["c1c_growing"], p2["c1c_cases_done"]),
          "  - growing by field over the b = a + 1 cases (growing, cases): `%s`" % json.dumps(p2["growing_by_field"]),
          "  - GF(16) growing by family (growing, cases): `%s`" % json.dumps(p2["gf16_growing_by_family"]),
          "- P3 (at least 8 of 10 finite length per shape): " + "; ".join("%s: %d of %d (%s)" % (s, v["finite_length"], v["cases"], _yn(v["holds"])) for s, v in p3.items()) + ".",
          "- P4 (the Betti table of U/U(x^e, y^e)): %s; %d modules, %d on the wrong side %s." % (_yn(p4["holds"]), p4["modules"], len(p4["wrong_side"]), json.dumps(p4["wrong_side"])), ""]
    if p2["constant_with_other_value"]:
        L += ["Eventually constant with another value than S2 (id, value, S2 value): `%s`" % json.dumps(p2["constant_with_other_value"]), ""]
    if p2["unclassified_ids"]:
        L += ["Unclassified cases: `%s`" % json.dumps(p2["unclassified_ids"]), ""]
    if p1["finite_ids"]:
        L += ["### Finite length cases of C1 and C2, as found", ""]
        for cid in p1["finite_ids"]:
            r = res["cases"][cid]
            L.append("- `%s` shape (%d, %d, %d) relations `%s` Hilbert function `%s`" % (cid, r["a"], r["b"], r["e"], json.dumps(r["relations"]), json.dumps(r["hilbert"])))
        L.append("")
    L += ["## P4 per module", "", "| Module | Predicted pure | Finite length | Pure table (first instrument) | Pure table (Singular) | Hilbert function is the pure one | Tables agree |", "|---|---|---|---|---|---|---|"]
    for key, v in p4["per_module"].items():
        L.append("| %s | %s | %s | %s | %s | %s | %s |" % (key, v["predicted_pure"], v["finite_length"], v["pure_I1"], v["pure_I2"], v["hilbert_equals_pure_prediction"], v["tables_agree_I1_I2"]))
    L += ["", "## Reading notes", "",
          "- The seed of a random case is 20261120 + its index within its (family, field) list (within C3: its index 0 to 39 in the order of the shapes).",
          "- For a module that is not of finite length at the degree bound, the first instrument has no Betti table by Tor; the table is then judged by the "
          "Hilbert function (a module with the pure table has the pure Hilbert function) and by Singular's table.",
          "- P2's 5 percent clause is evaluated over all GF(16) cases of C2 with b = a + 1 pooled; the per-family counts are listed above.",
          "- Wall time of the commands (seconds): `%s`; total %s." % (json.dumps(res.get("runs", [])), res.get("wall_seconds_total")), ""]
    Path(path).write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    res = json.loads((HERE / "artifacts" / "results.json").read_text(encoding="utf-8"))
    res["totals"] = compute_totals(res)
    write_summary(res, HERE / "results-summary.md")
    print(totals_text(res["totals"]))
