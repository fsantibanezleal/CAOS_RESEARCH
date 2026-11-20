"""EXP-019: totals per case, the predictions P1 to P5 as counts, and results-summary.md, all computed from artifacts/results.json.

Every number of results-summary.md is computed from the stored cases, none is typed.  Counts and members only: no statement about
realizability is made here (the coordinating session draws the conclusions).  A case that is not started or not finished is shown as such
and the predictions that need it are 'not decided'.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP10 = HERE.parent / "EXP-010-weight-class-strata"
if str(EXP10) not in sys.path:
    sys.path.append(str(EXP10))

import exp010_routine as X  # noqa: E402

P5_LOW, P5_HIGH, P5_MIN_PASSING = 0.1, 3.0, 10
SHOWN = 3  # pure members printed per case
FAMILY_TITLE = {"K": "family K (controls)", "X": "family X (open pairs with e <= 14)", "Y": "family Y (open pairs with e = 15, 16)"}


def _by_key(res):
    return {c["key"]: c for c in res["plan"]}


def _state(res, c):
    """The stored record of a case (finished), its partial state, or None."""
    if c["key"] in res["cases"]:
        return res["cases"][c["key"]]
    return res["partial"].get(c["key"])


def compute_totals(res):
    out = {}
    for c in res["plan"]:
        s = _state(res, c)
        e, p, t = c["e"], c["p"], c["t"]
        expected = float(p) ** -(e - t - 2)
        if s is None:
            out[c["key"]] = {"key": c["key"], "family": c["family"], "e": e, "p": p, "t": t, "d": c["d"], "stratum": c["stratum"],
                             "budget": c["budget"], "status": "not started", "examined": 0, "f0": 0, "f1": 0, "f2": 0, "f3": 0,
                             "pure_hilbert": 0, "tables": 0, "pure": 0, "share_f3": None, "expected_share": expected, "ratio": None,
                             "stored": 0, "filter_members_per_second_per_worker": None, "worker_seconds": 0.0, "wall_seconds": 0.0}
            continue
        n = s["counts"]
        examined = n["examined"]
        status = s["status"] if "status" in s else "not finished"
        fsec = s["filter_seconds"]
        share = (n["f3"] / examined) if examined else None
        out[c["key"]] = {"key": c["key"], "family": c["family"], "e": e, "p": p, "t": t, "d": c["d"], "stratum": c["stratum"],
                         "budget": c["budget"], "status": status, "examined": examined, "f0": n["f0"], "f1": n["f1"], "f2": n["f2"],
                         "f3": n["f3"], "pure_hilbert": n["pure_hilbert"], "tables": s["tables"], "pure": s["pure"], "share_f3": share,
                         "expected_share": expected, "ratio": None if share is None else share / expected,
                         "stored": len(s["members"]), "filter_members_per_second_per_worker": int(examined / max(fsec, 1e-9)),
                         "worker_seconds": round(s["worker_seconds"], 1), "wall_seconds": s["wall_seconds"]}
    return out


def _g2_rows(res, key):
    return [r for r in res["gates"].get("G2", {}).get("rows", []) if r["case"] == key]


def _g2_row(res, key, index):
    return next((r for r in _g2_rows(res, key) if r["index"] == index), None)


def _pair_outcome(res, t):
    """The outcome of a pair for P1 and P2: a pure pair confirmed by both instruments."""
    if t["status"] == "not started":
        return {"outcome": "not decided", "why": "case not started"}
    s = _state(res, {"key": t["key"]})
    pure = [m for m in s["members"] if m.get("pure")]
    if t["pure"] > 0:
        rows = [_g2_row(res, t["key"], m["index"]) for m in pure[:3]]
        rows = [r for r in rows if r]
        ok = [r for r in rows if r.get("agree") and r.get("pure_I2")]
        if not res["gates"].get("G2"):
            return {"outcome": "not decided", "why": "pure member found by the first instrument; second instrument not yet run",
                    "pure": t["pure"], "confirmed": 0}
        if ok:
            return {"outcome": "holds", "why": "pure pair confirmed by both instruments", "pure": t["pure"], "confirmed": len(ok),
                    "checked": len(rows)}
        return {"outcome": "not confirmed", "why": "pure member found, no confirmation by the second instrument (errors or "
                "disagreement)", "pure": t["pure"], "confirmed": 0, "checked": len(rows)}
    if t["status"] in ("complete",):
        return {"outcome": "does not hold", "why": "no pure member in the %s members of the budget (%s pass the filter)" % (
            "{:,}".format(t["examined"]), t["f3"]), "pure": 0}
    return {"outcome": "not decided", "why": "case %s after %s members, no pure member yet" % (t["status"], "{:,}".format(t["examined"])),
            "pure": 0}


def predictions(res):
    tot = compute_totals(res)
    out = {}
    for name, fam in (("P1", "X"), ("P2", "Y")):
        rows = []
        for t in tot.values():
            if t["family"] == fam:
                rows.append(dict(_pair_outcome(res, t), pair=[t["e"], t["p"]], key=t["key"], status=t["status"], examined=t["examined"],
                                 pass_filter=t["f3"]))
        out[name] = {"statement": "family %s: a pure pair at each pair, confirmed by both instruments" % fam, "rows": rows}
    rows = []
    for t in tot.values():
        if t["status"] == "not started":
            rows.append({"case": t["key"], "outcome": "not decided", "pass_filter": 0})
        elif t["f3"] > 0:
            rows.append({"case": t["key"], "pass_filter": t["f3"], "pure_hilbert": t["pure_hilbert"], "outcome":
                         "holds" if t["pure_hilbert"] == t["f3"] else "does not hold"})
        else:
            rows.append({"case": t["key"], "pass_filter": 0, "outcome": "not applicable (no member passes)"})
    out["P3"] = {"statement": "every member that passes the filter has the pure Hilbert function", "rows": rows,
                 "holds_on_cases_done": all(r["outcome"] in ("holds", "not decided", "not applicable (no member passes)") for r in rows)
                 and any(r["outcome"] == "holds" for r in rows)}
    rows = []
    for t in tot.values():
        if t["tables"] > 0:
            rows.append({"case": t["key"], "tables": t["tables"], "pure": t["pure"], "outcome": "holds" if t["tables"] == t["pure"]
                         else "does not hold"})
        else:
            rows.append({"case": t["key"], "tables": 0, "pure": 0, "outcome": "not decided" if t["status"] == "not started" else
                         "not applicable (no table computed)"})
    out["P4"] = {"statement": "every Betti table computed on a member that passes the filter is pure", "rows": rows,
                 "holds_on_cases_done": all(r["outcome"] != "does not hold" for r in rows) and any(r["outcome"] == "holds" for r in rows)}
    rows = []
    for t in tot.values():
        if t["status"] == "not started":
            rows.append({"case": t["key"], "outcome": "not decided"})
        elif t["f3"] >= P5_MIN_PASSING:
            ok = P5_LOW <= t["ratio"] <= P5_HIGH
            rows.append({"case": t["key"], "pass_filter": t["f3"], "examined": t["examined"], "share": t["share_f3"],
                         "expected_share": t["expected_share"], "ratio": t["ratio"], "outcome": "holds" if ok else "does not hold"})
        else:
            rows.append({"case": t["key"], "pass_filter": t["f3"], "outcome": "not applicable (fewer than %d members pass)" % P5_MIN_PASSING})
    out["P5"] = {"statement": "where at least 10 members pass, their share is between 0.1 and 3 times p^-(e-t-2)", "rows": rows,
                 "holds_on_cases_done": all(r["outcome"] != "does not hold" for r in rows) and any(r["outcome"] == "holds" for r in rows)}
    return out


def family_seconds(res):
    out = {}
    for r in res["runs"]:
        k = r.get("family") or r["command"]
        out[k] = round(out.get(k, 0.0) + r["seconds"], 1)
    return out


def totals_text(totals):
    head = "%-8s %-13s %3s %3s %15s %9s %9s %7s %7s %7s %6s %7s %5s %9s" % (
        "case", "status", "t", "d", "examined", "F0", "F1", "F2", "F3", "HF", "", "tables", "pure", "mem/s/w")
    lines = [head]
    for t in totals.values():
        lines.append("%-8s %-13s %3d %3d %15s %9s %9s %7s %7s %7s %6s %7s %5s %9s" % (
            t["key"], t["status"], t["t"], t["d"], "{:,}".format(t["examined"]), "{:,}".format(t["f0"]), "{:,}".format(t["f1"]),
            "{:,}".format(t["f2"]), "{:,}".format(t["f3"]), t["pure_hilbert"], "", t["tables"], t["pure"],
            "n/a" if t["filter_members_per_second_per_worker"] is None else "{:,}".format(t["filter_members_per_second_per_worker"])))
    return "\n".join(lines)


def _table_rows(rows):
    return "\n".join("| " + " | ".join(str(c) for c in r) + " |" for r in rows)


def _betti(rows):
    return "none" if not rows else "; ".join("(%d, %d): %d" % tuple(r) for r in rows)


def _fmt(x, nd=3):
    return "n/a" if x is None else ("%.*g" % (nd, x))


def write_summary(res, path):
    tot = compute_totals(res)
    pred = predictions(res)
    g = res["gates"]
    L = ["# EXP-019: results", "",
         "Generated by `make_summary.py` from `artifacts/results.json`; every count is read from there.  Counts and members only; the",
         "verdict is written by the coordinating session.  The hypothesis is `hypothesis.md` (frozen).", ""]
    L += ["## Gates", ""]
    st = g.get("G1", {}).get("stored")
    if st:
        L.append("- G1 (a), the stored members of EXP-010, EXP-014, EXP-015 and EXP-018 with a computed table in a stratum S((e + t)/2; 0, "
                 "(e - t)/2): %d pure members by stage of the filter (stage 0 to 4, 4 = passes (F0) to (F3)) %s; %d members with another "
                 "table by stage %s; %d not of the form of the stratum; counts of the probe %d and %d; %s." % (
                     st["pure"], st["pure_by_stage"], st["other"], st["other_by_stage"], st["not_of_the_form"], st["probe_counts"]["pure"],
                     st["probe_counts"]["other"], "passed" if st["ok"] else "FAILED"))
    fam = g.get("G1", {}).get("family")
    if fam:
        L.append("- G1 (b), the controls: " + "; ".join("(%d, %d) t = %d: %s members examined, %s pass (F0) to (F3), %s pure" % (
            r["pair"][0], r["pair"][1], r["t"], "{:,}".format(r["examined"] or 0), r["pass_filter"], r["pure"]) for r in fam["rows"]) +
            "; %s." % ("passed" if fam["passed"] else "FAILED"))
    g2 = g.get("G2")
    if g2:
        L.append("- G2, the second instrument (%s): %s of %s sampled pure members agree and are pure in Singular; failing %s; errors %s; %s." % (
            g2.get("singular", "n/a"), g2.get("agree_and_pure_in_I2", "n/a"), g2.get("sample_members", "n/a"), g2.get("failing_cases"),
            g2.get("singular_errors"), "passed" if g2.get("passed") else ("BLOCKED" if g2.get("blocked") else "FAILED")))
    g3 = g.get("G3")
    if g3:
        L.append("- G3, the unit tests: %s (%s)." % ("passed" if g3["passed"] else "FAILED", g3["last_line"]))
    L.append("")
    L += ["## Cases", "",
          "Columns: t = the exponent, d = (e - t)/2; examined of the budget; F0 to F3 = members passing (F0), (F1), (F2) and (F3) in turn; "
          "HF = with the pure Hilbert function (staged test of EXP-010, run on every member passing (F3)); tables = Betti tables computed "
          "(uhlib), on the members with the pure Hilbert function in the order of their index; pure = tables with the pure Betti table "
          "(1, 2, 2, 1) in degrees (0, e, 3e, 4e); the throughput is the filter alone (members per second on one worker process).", "",
          "| case | t | d | stratum | status | examined | budget | F0 | F1 | F2 | F3 | HF | tables | pure | filter members/s/worker | worker s | wall s |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    rows = [[t["key"], t["t"], t["d"], "S(%d; %d, %d)" % tuple(t["stratum"]), t["status"], "{:,}".format(t["examined"]), "{:,}".format(t["budget"]),
             "{:,}".format(t["f0"]), "{:,}".format(t["f1"]), "{:,}".format(t["f2"]), "{:,}".format(t["f3"]), t["pure_hilbert"], t["tables"],
             t["pure"], "n/a" if t["filter_members_per_second_per_worker"] is None else "{:,}".format(t["filter_members_per_second_per_worker"]),
             t["worker_seconds"], t["wall_seconds"]] for t in tot.values()]
    L += [_table_rows(rows), ""]
    L += ["## Share passing the filter", "",
          "| case | passing (F0) to (F3) | examined | share | p^-(e-t-2) | ratio |", "|---|---|---|---|---|---|"]
    for t in tot.values():
        if t["examined"]:
            L.append("| %s | %s | %s | %s | %s | %s |" % (t["key"], t["f3"], "{:,}".format(t["examined"]), _fmt(t["share_f3"]),
                                                          _fmt(t["expected_share"]), _fmt(t["ratio"])))
    L.append("")
    L += ["## Time per family", ""]
    fs = res.get("wall_seconds_by_family") or family_seconds(res)
    L += ["- %s: %s s" % (k, v) for k, v in sorted(fs.items())] + [""]
    L += ["## Pure members", ""]
    for c in res["plan"]:
        s = _state(res, c)
        if s is None:
            L += ["### %s (e = %d, p = %d, t = %d): not started" % (c["key"], c["e"], c["p"], c["t"]), ""]
            continue
        pure = [m for m in s["members"] if m.get("pure")]
        L.append("### %s (e = %d, p = %d, t = %d): %d pure of %d tables" % (c["key"], c["e"], c["p"], c["t"], s["pure"], s["tables"]))
        if s.get("nonpure_tables"):
            L += ["", "Tables that are not pure: " + "; ".join("%s x %d" % (k, v) for k, v in sorted(s["nonpure_tables"].items())) + "."]
        if not pure:
            L += ["", "No pure member (a result)." if s.get("status") == "complete" else "No pure member yet.", ""]
            continue
        for m in pure[:SHOWN]:
            r2 = _g2_row(res, c["key"], m["index"])
            L += ["", "- member %d: alpha = %s, beta = %s, c = %s, c' = %s" % (m["index"], m["alpha"], m["beta"], m["c"], m["cp"]),
                  "  - f = %s" % X.poly_text(c["e"], c["p"], m["f"]), "  - g = %s" % X.poly_text(c["e"], c["p"], m["g"]),
                  "  - Betti table, first instrument: %s" % _betti(m["betti"]),
                  "  - Betti table, second instrument: %s" % ("not computed" if r2 is None else (
                      _betti(r2["betti_I2"]) if "betti_I2" in r2 else "no result (%s)" % r2.get("error")))]
        L.append("")
    L += ["## Predictions", ""]
    for name in ("P1", "P2"):
        p = pred[name]
        L.append("- %s (%s): %s" % (name, p["statement"], "; ".join(
            "(%d, %d) %s (%s)" % (r["pair"][0], r["pair"][1], r["outcome"], r["why"]) for r in p["rows"])))
    for name in ("P3", "P4", "P5"):
        p = pred[name]
        L.append("- %s (%s): %s on the cases done; %s" % (name, p["statement"], "holds" if p["holds_on_cases_done"] else "does not hold",
                                                          "; ".join("%s %s" % (r["case"], r["outcome"] + (
                                                              " (%s of %s)" % (r["pure_hilbert"], r["pass_filter"]) if name == "P3" and "pure_hilbert" in r
                                                              else " (%s of %s)" % (r["pure"], r["tables"]) if name == "P4" and r["tables"]
                                                              else " (ratio %s, %s passing)" % (_fmt(r["ratio"]), r["pass_filter"])
                                                              if name == "P5" and "ratio" in r else "")) for r in p["rows"])))
    L.append("")
    Path(path).write_text("\n".join(L), encoding="utf-8", newline="\n")
