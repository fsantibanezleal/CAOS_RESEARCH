"""EXP-006: totals per family and field, the four predictions as counts, and results-summary.md, all from results.json.

Nothing here is typed by hand: every number of results-summary.md is computed from the chunk records of
artifacts/results.json.  The predictions are reported as counts and comparisons with the interval or threshold the
hypothesis states; no statement about realizability is made here (the coordinating session draws the conclusions).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import exp006_routine as R  # noqa: E402

PRIME_OF = {"GF(3)": 3, "GF(5)": 5, "GF(7)": 7, "GF(9)": 3, "GF(11)": 11, "GF(13)": 13, "GF(25)": 5, "GF(27)": 3}


def _merge(dst, src):
    for k, v in src.items():
        dst[k] = dst.get(k, 0) + v


def compute_totals(res):
    """{family|field: {...}} from the chunk records."""
    out = {}
    for fam, (e, fields, kind, n_planned, mode, orbit) in R.FAMILIES.items():
        for fname in fields:
            recs = [c for c in res["chunks"].values() if c["family"] == fam and c["field"] == fname]
            q = int(fname[3:-1])
            tgt = R.target_rank(e)
            t = {"family": fam, "field": fname, "e": e, "q": q, "char": PRIME_OF[fname], "planned": n_planned,
                 "chunks": len(recs), "chunks_planned": len(range(0, n_planned, R.CHUNK)),
                 "spaces": sum(c["n"] for c in recs), "rank_hist": {}, "hilbert_computed": 0, "hilbert_other": {},
                 "pure_hilbert": sum(c["pure_hilbert"] for c in recs), "pure": sum(c["pure"] for c in recs),
                 "nonpure_tables": {}, "target_rank": tgt, "seconds_cpu": round(sum(c["seconds"] for c in recs), 1)}
            for c in recs:
                _merge(t["rank_hist"], c["rank_hist"])
                _merge(t["hilbert_other"], c["hilbert_other"])
                _merge(t["nonpure_tables"], c["nonpure_tables"])
                t["hilbert_computed"] += c["hilbert_computed"]
            t["rank_hist"] = {k: t["rank_hist"][k] for k in sorted(t["rank_hist"], key=int)}
            t["rank_le_target"] = sum(v for k, v in t["rank_hist"].items() if int(k) <= tgt)
            n = t["spaces"]
            t["share_rank_le_target"] = t["rank_le_target"] / n if n else None
            t["share_pure"] = t["pure"] / n if n else None
            t["share_pure_hilbert"] = t["pure_hilbert"] / n if n else None
            t["q_minus_2"] = 1.0 / (q * q)
            t["ratio_rank_to_q_minus_2"] = t["share_rank_le_target"] / t["q_minus_2"] if n else None
            t["ratio_pure_to_q_minus_2"] = t["share_pure"] / t["q_minus_2"] if n else None
            t["complete"] = n == n_planned
            if orbit:
                pure_sp = [sp for c in recs for sp in c["spaces"] if sp["pure"]]
                kinds = {}
                for sp in pure_sp:
                    kinds[sp["orbit"]["kind"]] = kinds.get(sp["orbit"]["kind"], 0) + 1
                t["orbit"] = {"pure_spaces_tested": len(pure_sp), "in_orbit": sum(sp["orbit"]["in_orbit"] for sp in pure_sp),
                              "outside_orbit": sum(not sp["orbit"]["in_orbit"] for sp in pure_sp), "kinds": kinds}
            out["%s|%s" % (fam, fname)] = t
    fam_tot = {}
    for t in out.values():
        f = fam_tot.setdefault(t["family"], {"spaces": 0, "pure_hilbert": 0, "pure": 0, "planned": 0})
        f["spaces"] += t["spaces"]
        f["pure_hilbert"] += t["pure_hilbert"]
        f["pure"] += t["pure"]
        f["planned"] += t["planned"]
    return {"per_field": out, "per_family": fam_tot}


def predictions(totals):
    """P1 to P4 as counts and comparisons with the hypothesis's statements (no verdict on realizability)."""
    pf = totals["per_field"]
    p1 = {"pure_pairs_over_GF(3)": pf["A1|GF(3)"]["pure"], "pure_pairs_over_GF(5)": pf["A2|GF(5)"]["pure"],
          "share_pure_GF(25)": pf["A2|GF(25)"]["share_pure"], "share_pure_GF(27)": pf["A2|GF(27)"]["share_pure"],
          "share_pure_GF(9)": pf["A2|GF(9)"]["share_pure"]}
    p1["holds"] = (p1["pure_pairs_over_GF(3)"] > 0 and p1["pure_pairs_over_GF(5)"] > 0
                   and (p1["share_pure_GF(25)"] or 0) >= 0.5 and (p1["share_pure_GF(27)"] or 0) >= 0.5)
    p2 = {}
    for key in ("B1|GF(3)", "B1|GF(5)", "B1|GF(7)", "B2|GF(11)", "B2|GF(13)", "B3|GF(9)"):
        t = pf[key]
        r = t["ratio_rank_to_q_minus_2"]
        p2[key] = {"spaces": t["spaces"], "rank_le_48": t["rank_le_target"], "share": t["share_rank_le_target"],
                   "q_minus_2": t["q_minus_2"], "ratio": r, "in_interval_0.3_to_3": r is not None and 0.3 <= r <= 3.0}
    p2["holds"] = all(v["in_interval_0.3_to_3"] for v in p2.values())
    p3 = {"pure_pairs": {k: pf[k]["pure"] for k in ("B1|GF(3)", "B1|GF(5)", "B1|GF(7)")}}
    p3["holds"] = all(v > 0 for v in p3["pure_pairs"].values())
    p4 = {}
    for key in ("B2|GF(11)", "B2|GF(13)"):
        o = pf[key].get("orbit", {})
        p4[key] = {"pure": pf[key]["pure"], "outside_orbit": o.get("outside_orbit"), "in_orbit": o.get("in_orbit")}
    p4["holds"] = all((v["outside_orbit"] or 0) > 0 for v in p4.values())
    return {"P1": p1, "P2": p2, "P3": p3, "P4": p4}


def prune_bases(res, keep):
    """Per (family, field): the bases of the first `keep` pure spaces stay; later pure spaces keep their seed or index only."""
    groups = {}
    for c in res["chunks"].values():
        groups.setdefault((c["family"], c["field"]), []).append(c)
    pruned = {}
    for (fam, fname), recs in groups.items():
        seen = 0
        for c in sorted(recs, key=lambda c: c["start"]):
            for sp in sorted(c["spaces"], key=lambda s: s["index"]):
                if sp["pure"]:
                    seen += 1
                    if seen > keep and "basis" in sp:
                        del sp["basis"]
                        pruned["%s|%s" % (fam, fname)] = pruned.get("%s|%s" % (fam, fname), 0) + 1
    res["bases_dropped_beyond_first_%d_pure" % keep] = pruned


def totals_text(totals):
    lines = ["%-4s %-8s %7s %7s %9s %8s %8s %9s" % ("fam", "field", "spaces", "planned", "rank<=tgt", "pureHF", "pure", "complete")]
    for t in totals["per_field"].values():
        lines.append("%-4s %-8s %7d %7d %9d %8d %8d %9s" % (t["family"], t["field"], t["spaces"], t["planned"],
                                                           t["rank_le_target"], t["pure_hilbert"], t["pure"], t["complete"]))
    lines.append("")
    for fam, f in totals["per_family"].items():
        lines.append("family %-3s spaces %7d of %7d   pure Hilbert function %7d   pure %7d" % (fam, f["spaces"], f["planned"],
                                                                                            f["pure_hilbert"], f["pure"]))
    return "\n".join(lines)


# ------------------------------------------------------------------ results-summary.md
def _pct(x, d=2):
    return "n/a" if x is None else "%.*f%%" % (d, 100 * x)


def _table_text(rows):
    if rows is None:
        return "none"
    return "; ".join("b_%d,%d = %d" % tuple(r) for r in rows)


def _space(res, fam, fname, index):
    for c in res["chunks"].values():
        if c["family"] == fam and c["field"] == fname and c["start"] <= index < c["end"]:
            for sp in c["spaces"]:
                if sp["index"] == index:
                    return sp
    return None


def write_summary(res, path):
    T = res["totals"]
    P = res["predictions"]
    L = ["# EXP-006 results summary", "",
         "Generated by make_summary.py from artifacts/results.json; every number below is computed, none is typed.",
         "Hypothesis: hypothesis.md (frozen). Counts and pairs only: no statement of realizability is made here.", ""]
    L += ["## Gates", ""]
    for g in ("G1", "G2", "G3", "G4"):
        r = res["gates"].get(g)
        if r is None:
            L.append("- %s: not run" % g)
        elif r.get("blocked"):
            L.append("- %s: BLOCKED, %s" % (g, r["reason"]))
        else:
            extra = ""
            if g == "G3":
                extra = " (%s; %d pure spaces in the sample, %d with the same table from both instruments)" % (
                    r["singular"], r["sample_spaces"], r["agree_and_pure_in_I2"])
            if g == "G4":
                extra = " (%s)" % r["last_line"]
            L.append("- %s: %s%s" % (g, "PASSED" if r["passed"] else "FAILED", extra))
    L += ["", "## Totals per family and field", "",
          "| Family | e | Field | Spaces done / planned | rank mu_3e <= %s | Pure Hilbert function | Pure (Betti table) | Share pure | q^-2 | CPU s |"
          % "target", "|---|---|---|---|---|---|---|---|---|---|"]
    for t in T["per_field"].values():
        L.append("| %s | %d | %s | %d / %d | %d (%s) | %d | %d | %s | %s | %s |" % (
            t["family"], t["e"], t["field"], t["spaces"], t["planned"], t["rank_le_target"], _pct(t["share_rank_le_target"]),
            t["pure_hilbert"], t["pure"], _pct(t["share_pure"]), _pct(t["q_minus_2"]), t["seconds_cpu"]))
    L += ["", "The target is the rank of mu_3e(W) of the pure Hilbert function: 30 (e = 3), 48 (e = 4), 70 (e = 5).", ""]
    L += ["## Distribution of rank mu_3e per family and field", ""]
    for t in T["per_field"].values():
        L.append("- %s %s: %s" % (t["family"], t["field"], ", ".join("%s: %d" % kv for kv in t["rank_hist"].items())))
    L += ["", "## Spaces with the pure Hilbert function but another Betti table", ""]
    any_np = False
    for t in T["per_field"].values():
        if t["nonpure_tables"]:
            any_np = True
            L.append("- %s %s: %d spaces with the pure Hilbert function and another table; %d distinct tables" % (
                t["family"], t["field"], sum(t["nonpure_tables"].values()), len(t["nonpure_tables"])))
            for k, v in sorted(t["nonpure_tables"].items(), key=lambda kv: -kv[1])[:3]:
                L.append("    - %d x %s" % (v, k))
    if not any_np:
        L.append("- none")
    L += ["", "## Other Hilbert functions among the spaces whose Hilbert function was computed", ""]
    for t in T["per_field"].values():
        if t["hilbert_computed"]:
            L.append("- %s %s: Hilbert function computed for %d spaces; %d of them with a function other than h_e (%d distinct)"
                     % (t["family"], t["field"], t["hilbert_computed"], sum(t["hilbert_other"].values()), len(t["hilbert_other"])))
    L += ["", "## Orbit test of family B2", ""]
    for key in ("B2|GF(11)", "B2|GF(13)"):
        t = T["per_field"].get(key)
        if t and "orbit" in t:
            o = t["orbit"]
            L.append("- %s: %d pure spaces tested; in the orbit of <x^4, y^4>: %d; outside: %d; kinds: %s" % (
                t["field"], o["pure_spaces_tested"], o["in_orbit"], o["outside_orbit"],
                ", ".join("%s: %d" % kv for kv in sorted(o["kinds"].items())) or "none"))
    L += ["", "## Predictions as counts", ""]
    p = P["P1"]
    L.append("- P1 (e = 3): pure spaces over GF(3): %d (of %d, all subspaces); over GF(5): %d; share pure over GF(9): %s, GF(25): %s, GF(27): %s. "
             "Hypothesis statements hold: %s." % (p["pure_pairs_over_GF(3)"], T["per_field"]["A1|GF(3)"]["spaces"],
                                                  p["pure_pairs_over_GF(5)"], _pct(p["share_pure_GF(9)"]),
                                                  _pct(p["share_pure_GF(25)"]), _pct(p["share_pure_GF(27)"]), p["holds"]))
    L.append("- P2 (e = 4, share with rank mu_12 <= 48 between 0.3 q^-2 and 3 q^-2):")
    for key, v in P["P2"].items():
        if key != "holds":
            L.append("    - %s: %d of %d = %s; q^-2 = %s; ratio %.2f; inside the interval: %s" % (
                key, v["rank_le_48"], v["spaces"], _pct(v["share"]), _pct(v["q_minus_2"]), v["ratio"], v["in_interval_0.3_to_3"]))
    L.append("    - all six inside the interval: %s" % P["P2"]["holds"])
    L.append("- P3 (e = 4): pure spaces over GF(3), GF(5), GF(7): %s. Statement holds: %s." % (
        ", ".join("%s %d" % (k.split("|")[1], v) for k, v in P["P3"]["pure_pairs"].items()), P["P3"]["holds"]))
    L.append("- P4 (control): " + "; ".join("%s: %s pure, %s outside the orbit, %s in it" % (
        k.split("|")[1], v["pure"], v["outside_orbit"], v["in_orbit"]) for k, v in P["P4"].items() if k != "holds")
        + ". Statement holds: %s." % P["P4"]["holds"])
    L += ["", "## Explicit pure pairs (basis of W, PBW monomials x^i y^j z^k; yx = xy - z)", ""]
    g3 = res["gates"].get("G3", {}).get("rows", [])
    shown = {}
    for r in g3:
        key = (r["family"], r["field"])
        if shown.get(key, 0) >= 3 or not r.get("agree"):
            continue
        sp = _space(res, r["family"], r["field"], r["index"])
        if sp is None or "basis" not in sp:
            continue
        shown[key] = shown.get(key, 0) + 1
        F = R.make_field(r["field"])
        seed = sp["seed"]
        L.append("- %s over %s, %s %s: f = %s ; g = %s ; Betti table, uhlib: %s ; Singular: %s" % (
            r["family"], r["field"], "seed" if seed is not None else "enumeration index", seed if seed is not None else sp["index"],
            R.poly_text(F, sp["basis"][0]), R.poly_text(F, sp["basis"][1]), _table_text(r["betti_I1"]), _table_text(r["betti_I2"])))
    if not g3:
        L.append("- G3 has not been run")
    for key, t in T["per_field"].items():
        if t["pure"] == 0:
            L.append("- %s %s: no pure space among %d" % (t["family"], t["field"], t["spaces"]))
    ext = [t for t in T["per_field"].values() if t["field"] in ("GF(9)", "GF(25)", "GF(27)")]
    if ext:
        L += ["", "Extension fields: uhlib's moduli, passed to Singular unchanged: " + "; ".join(
            "%s = GF(%d)[a]/(%s)" % (R.field_record(R.make_field(t["field"]))["name"], t["char"], " + ".join(
                "%sa^%d" % ("" if c == 1 else str(c) + "*", i) if i else str(c)
                for i, c in enumerate(R.field_record(R.make_field(t["field"]))["modulus"]) if c))
            for t in {x["field"]: x for x in ext}.values())]
    L += ["", "Wall time of the commands: " + ", ".join("%s %.0f s" % (r["command"], r["seconds"]) for r in res["runs"])
          + "; total %.0f s." % res.get("wall_seconds_total", 0), ""]
    Path(path).write_text("\n".join(L), encoding="utf-8")
