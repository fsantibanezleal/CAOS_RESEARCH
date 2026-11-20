"""EXP-012: the gates G2, the predictions P1 to P3 and the totals into results.json, and results-summary.md, all from results.json.

Every entry of results-summary.md is computed from the records of artifacts/results.json.  Outcomes only: no statement about
realizability or about the theorem is made here (the coordinating session draws the conclusions).
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "artifacts" / "results.json"
X_ORDER = ["B1", "B2", "B3", "B4", "B5", "C1", "C2", "C3", "D1", "D2", "D3"]
N_ORDER = ["N1", "N2", "N3"]
R_ORDER = ["4,3", "6,3", "6,5", "7,3", "7,7", "8,7", "9,3", "10,3"]
IDS = ("commutator", "s1", "s2", "g_s1_plus_f_s2")


def table_text(rows):
    if rows is None:
        return "not computed"
    return ", ".join("b(%d,%d)=%d" % (i, j, r) for i, j, r in rows)


def poly_text(lst, names):
    if not lst:
        return "0"
    out = []
    for *ex, c in lst:
        mon = " ".join(n if k == 1 else "%s^%d" % (n, k) for n, k in zip(names, ex) if k)
        out.append((str(c) + " " + mon).strip() if (c != 1 or not mon) else mon)
    return " + ".join(out)


def x_outcome(r):
    s = r.get("singular")
    return {"identities": all(r["identities"][k] for k in IDS), "criterion": r["criterion"]["holds"],
            "hilbert": r["hilbert_is_h_e"], "length": r["length_is_e_cubed"], "betti_uhlib": r["betti_uhlib_pure"],
            "betti_singular": None if not s or s["betti"] is None else s["same_as_uhlib"] and r["betti_uhlib_pure"]}


def r_totals(rec):
    pairs = rec["pairs"]
    both = [p for p in pairs if p["criterion"] and p["pure_hilbert"]]
    only_crit = [p for p in pairs if p["criterion"] and not p["pure_hilbert"]]
    only_hf = [p for p in pairs if p["pure_hilbert"] and not p["criterion"]]
    bt = rec.get("betti", {})
    return {"e": rec["e"], "p": rec["p"], "seed": rec["seed"], "n_pairs": len(pairs),
            "identity": sum(p["identity"] for p in pairs), "criterion": sum(p["criterion"] for p in pairs),
            "pure_hilbert": sum(p["pure_hilbert"] for p in pairs), "both": len(both),
            "exactly_one": len(only_crit) + len(only_hf), "criterion_only": [p["i"] for p in only_crit],
            "pure_hilbert_only": [p["i"] for p in only_hf],
            "disagreements": [{"i": p["i"], **p.get("intermediate", {})} for p in only_crit + only_hf],
            "betti_computed": len(bt), "betti_pure": sum(1 for b in bt.values() if b["pure"]),
            "betti_not_pure": [b["i"] for b in bt.values() if not b["pure"]], "seconds": rec["seconds"]}


def build(res):
    """Fill res['totals'], res['gates']['G2'], res['predictions']."""
    xs = {k: res["X"][k] for k in X_ORDER if k in res["X"]}
    rs = {k: r_totals(res["R"][k]) for k in R_ORDER if k in res["R"]}
    ns = {k: res["N"][k] for k in N_ORDER if k in res["N"]}
    res["totals"] = {"R": rs}
    # G2
    have = {k: x["singular"] for k, x in xs.items() if "singular" in x}
    errors = {k: s["error"] for k, s in have.items() if s["error"]}
    differs = [k for k, s in have.items() if s["betti"] is not None and not s["same_as_uhlib"]]
    missing = [k for k in X_ORDER if k not in have]
    res["gates"]["G2"] = {"passed": not errors and not differs and not missing and len(have) == len(X_ORDER),
                          "cases_with_singular": sorted(have), "missing": missing, "errors": errors, "differs": differs,
                          "single_instrument_cases": sorted(set(errors) | set(missing))}
    # P1
    p1 = {k: x_outcome(x) for k, x in xs.items()}
    p1_fail = {k: [a for a, v in o.items() if v is False] for k, o in p1.items() if any(v is False for v in o.values())}
    p1_pending = [k for k in X_ORDER if k not in xs] + [k for k, o in p1.items() if o["betti_singular"] is None]
    res["predictions"] = {
        "P1": {"cases": p1, "failing": p1_fail, "not_computed": p1_pending,
               "holds": not p1_fail and not p1_pending and len(xs) == len(X_ORDER)},
    }
    # P2
    bad_id = {k: t["n_pairs"] - t["identity"] for k, t in rs.items() if t["identity"] != t["n_pairs"]}
    bad_agree = {k: t["exactly_one"] for k, t in rs.items() if t["exactly_one"]}
    bad_betti = {k: t["betti_not_pure"] for k, t in rs.items() if t["betti_not_pure"]}
    res["predictions"]["P2"] = {"failing_identity": bad_id, "disagreements": bad_agree, "non_pure_tables": bad_betti,
                                "not_computed": [k for k in R_ORDER if k not in rs],
                                "holds": not bad_id and not bad_agree and not bad_betti and len(rs) == len(R_ORDER)}
    # P3
    p3 = {k: {"criterion_fails": not n["criterion"]["holds"], "not_finite_within_5e": not n["finite_length_within_5e"]}
          for k, n in ns.items()}
    res["predictions"]["P3"] = {"cases": p3, "not_computed": [k for k in N_ORDER if k not in ns],
                                "holds": all(all(v.values()) for v in p3.values()) and len(ns) == len(N_ORDER)}


def yn(v):
    return "n/a" if v is None else ("yes" if v else "NO")


def render_table(res):
    lines = ["| Case | (e, p) | identities (4) | criterion | Hilbert = h_e | length | Betti uhlib | Betti Singular | seconds |",
             "|---|---|---|---|---|---|---|---|---|"]
    for k in X_ORDER:
        r = res["X"].get(k)
        if not r:
            lines.append("| %s | not run | | | | | | | |" % k)
            continue
        s = r.get("singular")
        sing = "not run" if not s else (s["error"] or table_text(s["betti"]) + (" (same)" if s["same_as_uhlib"] else " (DIFFERENT)"))
        lines.append("| %s | (%d, %d) | %s | %s | %s | %d | %s | %s | %.1f |" % (
            k, r["e"], r["p"], yn(all(r["identities"][i] for i in IDS)), yn(r["criterion"]["holds"]), yn(r["hilbert_is_h_e"]),
            r["length"], table_text(r["betti_uhlib"]), sing, r["seconds"]))
    return "\n".join(lines)


def render(res):
    if "predictions" not in res:
        build(res)
    L = ["# EXP-012 results summary", "",
         "Generated by `make_summary.py` from `artifacts/results.json`; every entry below is computed from it. Outcomes only.", ""]
    L += ["## Gates", ""]
    for g in ("G1", "G2", "G3"):
        r = res["gates"].get(g)
        if r is None:
            L.append("- %s: not run" % g)
        elif g == "G1":
            L.append("- G1: %s. %s" % ("passed" if r["passed"] else "FAILED", "; ".join(
                "%s: pure %s (expected %s), Betti %s" % (c["case"], c["pure"], c["expected_pure"], table_text(c["betti"]))
                for c in r["pairs"]) + "; " + "; ".join("%s: criterion %s (expected %s)" % (c["ideal"], c["criterion"], c["expected"])
                                                        for c in r["ideals"])))
        elif g == "G2":
            L.append("- G2: %s. Singular and uhlib tables compared in %d of %d cases; missing %s; errors %s; differing %s." % (
                "passed" if r["passed"] else "NOT passed", len(r["cases_with_singular"]), len(X_ORDER), r["missing"] or "none",
                r["errors"] or "none", r["differs"] or "none"))
        else:
            L.append("- G3: %s (pytest exit code %d): %s" % ("passed" if r["passed"] else "FAILED", r["exit_code"], r["last_line"]))
    L += ["", "## Family X (the explicit pairs of the corollary)", "", render_table(res), ""]
    for k in X_ORDER:
        r = res["X"].get(k)
        if not r:
            continue
        L += ["### %s, (e, p) = (%d, %d)" % (k, r["e"], r["p"]), "",
              "- f = %s; g = %s" % (r["f_text"], r["g_text"]),
              "- PBW f = %s; g = %s" % (poly_text(r["f"], "xyz"), poly_text(r["g"], "xyz")),
              "- coefficient vectors on the basis of V_e: f = %s; g = %s" % (r["vec_f"], r["vec_g"]),
              "- data (A; beta_1; beta_2) = (%s; %s; %s) and (B; delta_1; delta_2) = (%s; %s; %s) in X, Y, z" % (
                  poly_text(r["data_f"]["A"], "XYz"), poly_text(r["data_f"]["beta1"], "XYz"), poly_text(r["data_f"]["beta2"], "XYz"),
                  poly_text(r["data_g"]["B"], "XYz"), poly_text(r["data_g"]["delta1"], "XYz"), poly_text(r["data_g"]["delta2"], "XYz")),
              "- D = %s; n(f) = %s; n(g) = %s" % (poly_text(r["D"], "XYz"), poly_text(r["nf"], "XYz"), poly_text(r["ng"], "XYz")),
              "- identities: g f - f g = - D z: %s; v f + w g = 0 for s_1: %s, for s_2: %s; g s_1 + f s_2 = 0: %s" % (
                  yn(r["identities"]["commutator"]), yn(r["identities"]["s1"]), yn(r["identities"]["s2"]),
                  yn(r["identities"]["g_s1_plus_f_s2"])),
              "- criterion (%s): %s; Groebner basis of %d elements, pure powers %s" % (
                  r["criterion"]["method"], yn(r["criterion"]["holds"]), r["criterion"]["basis_size"], r["criterion"]["pure_powers"]),
              "- Hilbert function (degrees 0 to %d): %s; equals h_e: %s; length %d (e^3 = %d)" % (
                  4 * r["e"] + 3, r["hilbert"], yn(r["hilbert_is_h_e"]), r["length"], r["e"] ** 3),
              "- Betti table by uhlib: %s; uhlib dimensions equal the ranks: %s" % (table_text(r["betti_uhlib"]),
                                                                                  yn(r["uhlib_dims_equal_ranks"]))]
        s = r.get("singular")
        L.append("- Betti table by Singular: " + ("not run" if not s else "%s (%.1f s%s)" % (
            table_text(s["betti"]), s["seconds"], "; error: " + s["error"] if s["error"] else "")))
        L += ["- seconds: identities %.2f, criterion %.2f, Hilbert %.2f, uhlib Betti %.2f, total %.1f" % (
            r["seconds_identities"], r["seconds_criterion"], r["seconds_hilbert"], r["seconds_betti_uhlib"], r["seconds"]), ""]
    L += ["## Family R (200 random pairs of V_e per (e, p))", "",
          "| (e, p) | seed | pairs | identity | criterion true | pure Hilbert | both | exactly one | Betti computed | Betti pure | seconds |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    tot = res.get("totals", {}).get("R", {})
    for k in R_ORDER:
        t = tot.get(k)
        if t:
            L.append("| (%d, %d) | %d | %d | %d | %d | %d | %d | %d | %d | %d | %.1f |" % (
                t["e"], t["p"], t["seed"], t["n_pairs"], t["identity"], t["criterion"], t["pure_hilbert"], t["both"],
                t["exactly_one"], t["betti_computed"], t["betti_pure"], t["seconds"]))
        else:
            L.append("| %s | not run | | | | | | | | | |" % k)
    L.append("")
    for k in R_ORDER:
        t = tot.get(k)
        if t:
            L.append("- (%s): pairs with exactly one of the two: %s" % (k, json.dumps(t["disagreements"]) if t["disagreements"] else "none"))
    L += ["", "## Family N (the criterion should fail)", ""]
    for k in N_ORDER:
        n = res["N"].get(k)
        if not n:
            L.append("- %s: not run" % k)
            continue
        L += ["### %s, (e, p) = (%d, %d)" % (k, n["e"], n["p"]), "",
              "- f = %s; g = %s" % (n["f_text"], n["g_text"]),
              "- D = %s; n(f) = %s; n(g) = %s" % (poly_text(n["D"], "XYz"), poly_text(n["nf"], "XYz"), poly_text(n["ng"], "XYz")),
              "- identities: %s" % ", ".join("%s %s" % (i, yn(n["identities"][i])) for i in IDS),
              "- criterion: %s; Groebner basis of %d elements, pure powers %s" % (
                  yn(n["criterion"]["holds"]), n["criterion"]["basis_size"], n["criterion"]["pure_powers"]),
              "- Hilbert function (degrees 0 to %d): %s; finite length within degree %d: %s%s" % (
                  5 * n["e"], n["hilbert_to_5e"], 5 * n["e"], yn(n["finite_length_within_5e"]),
                  "" if not n["finite_length_within_5e"] else "; length %d" % n["length"]), ""]
    L += ["## Predictions", ""]
    pr = res["predictions"]
    L.append("- P1 (family X): %s; failing %s; not computed or without a second table %s" % (
        "holds on every case" if pr["P1"]["holds"] else "does not hold as stated", pr["P1"]["failing"] or "none",
        pr["P1"]["not_computed"] or "none"))
    L.append("- P2 (family R): %s; pairs with a failing identity %s; (e, p) with a disagreement of criterion and pure Hilbert "
             "function %s; non-pure tables %s; not computed %s" % (
                 "holds" if pr["P2"]["holds"] else "does not hold as stated", pr["P2"]["failing_identity"] or "none",
                 pr["P2"]["disagreements"] or "none", pr["P2"]["non_pure_tables"] or "none", pr["P2"]["not_computed"] or "none"))
    L.append("- P3 (family N): %s; per case %s; not computed %s" % (
        "holds" if pr["P3"]["holds"] else "does not hold as stated", json.dumps(pr["P3"]["cases"]), pr["P3"]["not_computed"] or "none"))
    L += ["", "## Runs", ""]
    for r in res["runs"]:
        L.append("- %s: %.1f s" % (r["command"], r["seconds"]))
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    res = json.loads(RESULTS.read_text(encoding="utf-8"))
    build(res)
    (HERE / "results-summary.md").write_text(render(res), encoding="utf-8", newline="\n")
    sys.exit(0)
