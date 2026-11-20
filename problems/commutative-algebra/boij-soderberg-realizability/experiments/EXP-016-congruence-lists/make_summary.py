"""EXP-016: totals, the predictions P1 to P5 and results-summary.md, all generated from artifacts/results.json (no number is typed here)."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import exp016_routine as R  # noqa: E402
from uhlib import algebra as A  # noqa: E402

EXP14 = HERE.parent / "EXP-014-middle-strata" / "artifacts" / "results.json"
P1_PAIRS = [(10, 17), (10, 19), (12, 13), (12, 17), (12, 19), (12, 23), (14, 5), (14, 11), (14, 17), (14, 19), (14, 23), (16, 11), (16, 13)]
P1_EXTRA = (12, 7)
P2_A = [(10, 3), (10, 7), (10, 11), (10, 13), (12, 5)]
P2_B = [(12, 11), (14, 3), (14, 13), (16, 3), (16, 5), (16, 7)]
P4 = [(8, 3), (6, 13), (14, 3)]
FAM_ORDER = {"A": 0, "B": 1, "X": 2, "O": 3}


def case_order(item):
    key, c = item
    return (FAM_ORDER[c["family"]], c["e"], c["p"])


def cases_sorted(res):
    return sorted(res["cases"].items(), key=case_order)


def get(res, family, e, p, k=1):
    return res["cases"].get("%s|%d|%d|%d" % (family, e, p, k))


def poly_of(c, f):
    F = R.Field(c["p"], c["degree"])
    return R.poly_text(F, [x if c["degree"] == 1 else tuple(x) for x in f["coeffs"]])


def lam_text(c, f):
    return str(f["lam"]) if c["degree"] == 1 else "(%d + %d t)" % tuple(f["lam"])


def status(c):
    return "complete" if c["complete"] else "partial: indices 0 to %d of %d (list is a lower bound)" % (c["done_upto"], c["n_forms"])


def compute_totals(res):
    out = {}
    for fam in ("A", "B", "X", "O"):
        cs = [c for _, c in res["cases"].items() if c["family"] == fam]
        out[fam] = {"cases": len(cs), "complete": sum(c["complete"] for c in cs), "forms": sum(c["done_upto"] for c in cs),
                    "nonempty_lists": sum(1 for c in cs if c["list"]), "list_forms": sum(len(c["list"]) for c in cs),
                    "verified_forms": sum(len(c["verified"]) for c in cs), "seconds": round(sum(c["seconds"] for c in cs), 1),
                    "worker_seconds": round(sum(c["worker_seconds"] for c in cs), 1)}
    return out


# ------------------------------------------------------------------ the pure members of EXP-014, rewritten in h
def exp14_members(e, p):
    """For the E-stratum of (e, p) in EXP-014: [(b, monic coefficient list or None, gamma_m)] of the stored pure members."""
    if not EXP14.exists():
        return None
    r = json.loads(EXP14.read_text(encoding="utf-8"))
    key = "V|%d|%d|%d|0|%d" % (e, p, e, e // 2)
    s = r["strata"].get(key)
    if s is None:
        return None
    m = e // 2
    monos = A.monos(e)
    pos = {mo: i for i, mo in enumerate(monos)}
    out = []
    for mem in s["members"]:
        if not mem["pure"]:
            continue
        f, g = mem["f"], mem["g"]
        b = (f[pos[(0, e, 0)]] * pow(f[pos[(e, 0, 0)]], -1, p)) % p
        gam = [g[pos[(a, a, m - a)]] % p for a in range(m + 1)]
        if gam[m] == 0:
            out.append({"b": b, "G": None, "gamma_m": 0, "index": mem["index"]})
            continue
        inv = pow(gam[m], -1, p)
        coeffs = [0] * (m + 1)
        for a in range(m + 1):
            for i, v in enumerate(R._A_int(a)):
                coeffs[i] = (coeffs[i] + gam[a] * v) % p
        out.append({"b": b, "G": [(c * inv) % p for c in coeffs[:m]], "gamma_m": gam[m], "index": mem["index"]})
    return out


def predictions(res):
    out = {}
    # P1
    rows, nonempty, all_complete = [], 0, True
    for e, p in P1_PAIRS + [P1_EXTRA]:
        c = get(res, "B", e, p)
        row = {"pair": [e, p], "case_run": c is not None, "complete": bool(c and c["complete"]), "size": None if c is None else len(c["list"]),
               "nonempty": bool(c and c["list"])}
        rows.append(row)
        if (e, p) != P1_EXTRA:
            nonempty += row["nonempty"]
            all_complete = all_complete and row["complete"]
    out["P1"] = {"claim": "L(e, p) not empty at the 13 pairs (0.75 each), at (12, 7) (0.4); at least 9 of these 14 not empty (0.7)", "rows": rows,
                 "nonempty_of_the_13": nonempty, "nonempty_of_the_14": nonempty + rows[-1]["nonempty"],
                 "at_least_9_of_14_nonempty": nonempty + rows[-1]["nonempty"] >= 9, "all_complete": all_complete and rows[-1]["complete"]}
    # P2
    rows = []
    for e, p in P2_A:
        c = get(res, "B", e, p)
        mem = exp14_members(e, p)
        row = {"pair": [e, p], "size": None if c is None else len(c["list"]), "complete": bool(c and c["complete"])}
        if mem is not None and c is not None:
            lst = [tuple(f["coeffs"]) for f in c["list"]]
            comp = [x for x in mem if x["G"] is not None]
            row.update({"exp014_pure_members": len(mem), "monic_g": len(comp), "g_not_of_degree_m": len(mem) - len(comp),
                        "in_list": sum(1 for x in comp if tuple(x["G"]) in lst),
                        "not_in_list": [{"G": x["G"], "b": x["b"]} for x in comp if tuple(x["G"]) not in lst],
                        "b_not_1": sum(1 for x in comp if x["b"] != 1)})
        rows.append(row)
    rows_b = [{"pair": [e, p], "size": None if get(res, "B", e, p) is None else len(get(res, "B", e, p)["list"]),
               "complete": bool(get(res, "B", e, p) and get(res, "B", e, p)["complete"])} for e, p in P2_B]
    out["P2"] = {"claim": "L(e, p) not empty at the five settled pairs and contains the G of every pure EXP-014 member (0.85); not empty at six more (0.7 each)",
                 "settled_rows": rows, "other_rows": rows_b,
                 "settled_nonempty": sum(1 for r in rows if r["size"]), "other_nonempty": sum(1 for r in rows_b if r["size"]),
                 "every_exp014_g_in_list": all(r.get("in_list") == r.get("monic_g") for r in rows if "in_list" in r)}
    # P3
    g4 = res["gates"].get("G4")
    out["P3"] = {"claim": "G4 passes (0.95)", "passed": None if g4 is None else g4["passed"],
                 "verified_forms": sum(len(c["verified"]) for c in res["cases"].values())}
    # P4
    rows = []
    for e, p in P4:
        c = get(res, "X", e, p, 2)
        rows.append({"case": "L(%d, %d)" % (e, p * p), "size": None if c is None else len(c["list"]), "complete": bool(c and c["complete"])})
    out["P4"] = {"claim": "L(8, 9), L(6, 169), L(14, 9) not empty (0.6, 0.85, 0.6)", "rows": rows}
    # P5
    rows, worst = [], None
    for key, c in cases_sorted(res):
        if c["family"] != "B":
            continue
        r = {"pair": [c["e"], c["p"]], "size": len(c["list"]), "three_p": 3 * c["p"], "more_than_3p": len(c["list"]) > 3 * c["p"],
             "complete": c["complete"]}
        rows.append(r)
        worst = r if worst is None or r["size"] / r["three_p"] > worst["size"] / worst["three_p"] else worst
    out["P5"] = {"claim": "no list over a prime field in family B has more than 3 p forms (0.7)", "rows": rows,
                 "lists_with_more_than_3p": [r["pair"] for r in rows if r["more_than_3p"]], "largest_relative_to_p": worst}
    return out


# ------------------------------------------------------------------ the text
def table_text(res):
    head = "%-6s %3s %4s %2s %16s %9s %12s %8s %8s %9s %5s %9s" % ("family", "e", "p", "k", "forms", "complete", "fast pass", "(b)", "(b)noC",
                                                                  "list", "verif", "seconds")
    lines = [head]
    for key, c in cases_sorted(res):
        lines.append("%-6s %3d %4d %2d %16d %9s %12d %8d %8d %9d %5d %9.1f" % (
            c["family"], c["e"], c["p"], c["degree"], c["n_forms"], "yes" if c["complete"] else "partial", c["n_fast"], c["n_b"], c["n_b_noC"],
            len(c["list"]), len(c["verified"]), c["seconds"]))
    return "\n".join(lines)


def tbl(rows):
    return "\n".join("    " + ln for ln in rows)


def betti_text(b):
    return "none" if b is None else " ".join("(%d,%d):%d" % tuple(x) for x in b)


def write_summary(res, path):
    L = ["# EXP-016 results summary", "",
         "Generated by make_summary.py from artifacts/results.json; every number below is computed, none is typed.",
         "Hypothesis: hypothesis.md (frozen). Lists, tables and counts only: no statement of realizability is made here.", "",
         "Notation: a case is (e, field); 'forms' is q^(e/2); 'fast pass' the forms that pass the fast test of (b); '(b)' those with (b) by the exact test; "
         "'(b)noC' those with (b) and without (C); 'list' those with (b) and (C). A partial case is marked with the index range done and its list is a "
         "lower bound. 'pure' means the table (1, 2, 2, 1) on (0, e, 3e, 4e) and length e^3 from uhlib.", "", "## Gates", ""]
    g = res["gates"]
    L.append("- G1 (sizes of family A): " + ("not evaluated" if "G1" not in g else "PASSED" if g["G1"]["passed"] else "FAILED"))
    if "G1" in g:
        for r in g["G1"]["rows"]:
            L.append("    - (%d, %d): expected %s, size %s%s" % (r["pair"][0], r["pair"][1], r["expected"], r["size"],
                                                               "" if "list_ok" not in r else ", named list %s" % ("matches" if r["list_ok"] else "DIFFERS")))
    if "G2" in g:
        L.append("- G2 (second instrument): %s; %s; %d verified forms, %d with the same table from both instruments; failing: %s" % (
            "PASSED" if g["G2"]["passed"] else "FAILED" if not g["G2"].get("blocked") else "BLOCKED", g["G2"].get("singular", g["G2"].get("reason")),
            g["G2"].get("forms", 0), g["G2"].get("agree", 0), g["G2"].get("failing", [])))
    else:
        L.append("- G2: not evaluated")
    if "G3" in g:
        L.append("- G3 (unit tests): %s; %s" % ("PASSED" if g["G3"]["passed"] else "FAILED", g["G3"]["last_line"]))
    if "G4" in g:
        L.append("- G4 (every verified form pure in the first instrument): %s; %d cases with verified forms, %d forms, %d not pure" % (
            "PASSED" if g["G4"]["passed"] else "FAILED", len(g["G4"]["rows"]), sum(r["verified"] for r in g["G4"]["rows"]),
            sum(len(r["not_pure"]) for r in g["G4"]["rows"])))
    if "G5" in g:
        L.append("- G5 (negative controls): %s" % ("PASSED" if g["G5"]["passed"] else "FAILED"))
        for r in g["G5"]["rows"]:
            L.append("    - (%d, %d): %d forms, %s" % (r["pair"][0], r["pair"][1], r["forms"], "all with a length different from e^3" if r["ok"] else "NOT ok"))
    th = res.get("throughput")
    if th:
        L += ["", "## Throughput", "",
              "One process on the first %d forms of (%d, %d): fast test %d forms/s (%.2f s); fast test plus exact tests %d forms/s (%.2f s); "
              "%d forms passed the fast test." % (th["forms"], th["e"], th["p"], th["forms_per_second_fast"], th["fast_test_seconds"],
                                                  th["forms_per_second_with_exact"], th["with_exact_seconds"], th["passing_fast"])]
    L += ["", "## Cases", "", table_text(res).replace("\n", "\n").join(["```\n", "\n```"]), "", "## Totals per family", ""]
    for fam, t in res.get("totals", compute_totals(res)).items():
        if t["cases"]:
            L.append("- family %s: %d cases (%d complete), %d forms scanned, %d lists not empty, %d forms in lists, %d verified forms, %.0f s wall, "
                     "%.0f s of worker time" % (fam, t["cases"], t["complete"], t["forms"], t["nonempty_lists"], t["list_forms"], t["verified_forms"],
                                               t["seconds"], t["worker_seconds"]))
    L += ["", "## Lists (forms as polynomials in h, with lambda; lists longer than 20 forms: the first 20 and the count)", ""]
    for key, c in cases_sorted(res):
        L.append("### %s, e = %d, %s: %d forms, %s, list size %d" % (c["family"], c["e"], c["field"], c["n_forms"], status(c), len(c["list"])))
        L.append("")
        for f in c["list"][:20]:
            L.append("- %s  (index %d, lambda = %s)" % (poly_of(c, f), f["index"], lam_text(c, f)))
        if len(c["list"]) > 20:
            L.append("- ... %d more forms (the list has %d forms)" % (len(c["list"]) - 20, len(c["list"])))
        if not c["list"]:
            L.append("- the list is empty")
        L.append("")
    L += ["## Verified forms (first instrument: uhlib; second instrument: Singular)", ""]
    for key, c in cases_sorted(res):
        for v in c["verified"]:
            fi, se = v["first"], v.get("second")
            L.append("- %s e = %d, %s, index %d: G = %s; g = %s; first instrument: length %s, table %s, pure %s (%.1f s)%s" % (
                c["family"], c["e"], c["field"], v["index"], v["poly"], " + ".join("%s*x^%d y^%d z^%d" % ((str(cf),) + tuple(mo)) for mo, cf in v["g"]),
                fi.get("length"), betti_text(fi.get("betti")), fi.get("pure"), fi.get("seconds", 0),
                "" if fi.get("betti") is not None or "timeout" not in fi else "; no result: " + fi["note"]) + (
                "; second instrument: table %s, pure %s (%.1f s)" % (betti_text(se.get("betti")), se.get("pure"), se["seconds"]) if se and "betti" in se else
                "; second instrument: " + (se.get("error", "") if se else "not run")))
    L += ["", "## Negative controls (family N: forms with (C) and without (b))", ""]
    for key, n in sorted(res["negatives"].items()):
        L.append("### (%d, %d): e^3 = %d" % (n["e"], n["p"], n["e_cubed"]))
        L.append("")
        for f in n["forms"]:
            L.append("- index %d, G = %s: length %s%s" % (f["index"], f["poly"], f["length"], "" if f["length"] is not None else " (%s)" % f["length_note"]))
        L.append("")
    L += ["## Predictions", ""]
    for name, pr in res.get("predictions", predictions(res)).items():
        L.append("### %s: %s" % (name, pr["claim"]))
        L.append("")
        L.append("```")
        L.append(json.dumps({k: v for k, v in pr.items() if k != "claim"}, indent=1))
        L.append("```")
        L.append("")
    L += ["## Time", "", "Wall seconds of the recorded commands: %s; budget used %.0f of %d s." % (
        res.get("wall_seconds_total", sum(r["seconds"] for r in res["runs"])), res["budget"]["used_seconds"], res["budget"]["limit_seconds"]), ""]
    for r in res["runs"]:
        L.append("- %s%s: %.0f s" % (r["command"], " " + r["family"] if r.get("family") else "", r["seconds"]))
    Path(path).write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
