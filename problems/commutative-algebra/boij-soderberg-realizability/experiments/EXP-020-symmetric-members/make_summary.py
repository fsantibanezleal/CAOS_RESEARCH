"""EXP-020: totals per case, the predictions P1 to P4 as counts, and results-summary.md, all computed from artifacts/results.json.

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

P4_LOW, P4_HIGH = 0.1, 1.0
SHOWN = 3  # pure members printed per case
FAMILY_TITLE = {"K": "family K (controls)", "X": "family X (open pairs)"}


def _state(res, c):
    """The stored record of a case (finished), its partial state, or None."""
    if c["key"] in res["cases"]:
        return res["cases"][c["key"]]
    return res["partial"].get(c["key"])


def _members(s):
    return s.get("passing", [])


def compute_totals(res):
    out = {}
    for c in res["plan"]:
        s = _state(res, c)
        e, p, t = c["e"], c["p"], c["t"]
        base = {"key": c["key"], "family": c["family"], "e": e, "p": p, "t": t, "d": c["d"], "stratum": c["stratum"], "nu": c["nu"],
                "members": c["members"], "two_p2": 2 * p * p}
        if s is None:
            out[c["key"]] = dict(base, status="not started", examined=0, stage_counts=[0] * 5, f0=0, f1=0, f2=0, f3=0, differ=0, c1=0,
                                 pure_hilbert=0, tables=0, pure=0, ratio=None, filter_members_per_second_per_worker=None, worker_seconds=0.0,
                                 wall_seconds=0.0)
            continue
        n = s["counts"]
        status = s.get("status") or ("filter done" if s.get("filter_done") else "not finished")
        fsec = s["filter_seconds"]
        out[c["key"]] = dict(base, status=status, examined=n["examined"], stage_counts=s["stage_counts"], f0=n["f0"], f1=n["f1"], f2=n["f2"],
                             f3=n["f3"], differ=n["differ"], c1=n["c1"], pure_hilbert=n["pure_hilbert"], tables=s["tables"], pure=s["pure"],
                             ratio=n["f3"] / (2 * p * p), filter_members_per_second_per_worker=int(n["examined"] / max(fsec, 1e-9)),
                             worker_seconds=round(s["worker_seconds"], 1), wall_seconds=s["wall_seconds"])
    return out


def _g2_row(res, key, index):
    return next((r for r in res["gates"].get("G2", {}).get("rows", []) if r["case"] == key and r["index"] == index), None)


def _pair_outcome(res, t):
    """The outcome of a pair for P1: a pure pair confirmed by both instruments."""
    if t["status"] != "complete":
        return {"outcome": "not decided", "why": "case %s" % t["status"], "pure": t["pure"], "confirmed": 0}
    s = _state(res, t)
    pure = [m for m in _members(s) if m.get("pure")]
    if t["pure"] > 0:
        if not res["gates"].get("G2"):
            return {"outcome": "not decided", "why": "pure member found by the first instrument; second instrument not yet run",
                    "pure": t["pure"], "confirmed": 0}
        rows = [r for r in (_g2_row(res, t["key"], m["index"]) for m in pure[:3]) if r]
        ok = [r for r in rows if r.get("agree") and r.get("pure_I2")]
        if ok:
            return {"outcome": "holds", "why": "pure pair confirmed by both instruments (%d of %d checked)" % (len(ok), len(rows)),
                    "pure": t["pure"], "confirmed": len(ok)}
        return {"outcome": "not confirmed", "why": "pure member found, no confirmation by the second instrument", "pure": t["pure"],
                "confirmed": 0}
    return {"outcome": "does not hold", "why": "no pure member among the %s members (%s pass the filter, %s tables computed)" % (
        "{:,}".format(t["examined"]), t["f3"], t["tables"]), "pure": 0, "confirmed": 0}


def predictions(res):
    tot = compute_totals(res)
    out = {}
    rows = []
    for t in tot.values():
        if t["family"] == "X":
            rows.append(dict(_pair_outcome(res, t), pair=[t["e"], t["p"]], key=t["key"], status=t["status"], examined=t["examined"],
                             pass_filter=t["f3"]))
    out["P1"] = {"statement": "family X: a pure pair at each open pair, confirmed by both instruments", "rows": rows}
    rows = []
    for t in tot.values():
        if t["status"] == "not started":
            rows.append({"case": t["key"], "outcome": "not decided"})
        else:
            rows.append({"case": t["key"], "with_f0": t["f0"], "differ": t["differ"],
                         "outcome": "holds" if t["differ"] == 0 else "does not hold"})
    out["P2"] = {"statement": "in every case no member with (F0) satisfies exactly one of (F1), (F2)", "rows": rows,
                 "holds_on_cases_done": all(r["outcome"] != "does not hold" for r in rows) and any(r["outcome"] == "holds" for r in rows)}
    rows = []
    for t in tot.values():
        if t["status"] == "not started":
            rows.append({"case": t["key"], "outcome": "not decided"})
            continue
        s = _state(res, t)
        mem = _members(s)
        tab = [m for m in mem if m.get("betti") is not None]
        c1y = [m for m in tab if m["c1"]]
        c1n = [m for m in tab if not m["c1"]]
        hf_ok = t["pure_hilbert"] == t["f3"] if s.get("staged_done", t["status"] == "complete") else None
        rows.append({"case": t["key"], "pass_filter": t["f3"], "pure_hilbert": t["pure_hilbert"], "hilbert_holds": hf_ok,
                     "tables_c1": len(c1y), "pure_c1": sum(1 for m in c1y if m["pure"]), "tables_no_c1": len(c1n),
                     "pure_no_c1": sum(1 for m in c1n if m["pure"]),
                     "outcome": "not decided" if hf_ok is None else ("holds" if hf_ok and all(m["pure"] for m in tab) else "does not hold")})
    out["P3"] = {"statement": "every passing member has the pure Hilbert function; every Betti table computed on a passing member (with or "
                              "without (C1)) is pure", "rows": rows,
                 "holds_on_cases_done": all(r["outcome"] != "does not hold" for r in rows) and any(r["outcome"] == "holds" for r in rows)}
    rows = []
    for t in tot.values():
        if t["family"] != "X":
            continue
        if t["status"] != "complete":
            rows.append({"case": t["key"], "outcome": "not decided"})
            continue
        ok = P4_LOW <= t["ratio"] <= P4_HIGH
        rows.append({"case": t["key"], "pass_filter": t["f3"], "two_p2": t["two_p2"], "ratio": t["ratio"],
                     "outcome": "holds" if ok else "does not hold"})
    out["P4"] = {"statement": "in every case of family X the number of passing members is between 0.1 and 1 times 2 p^2", "rows": rows,
                 "holds_on_cases_done": all(r["outcome"] != "does not hold" for r in rows) and any(r["outcome"] == "holds" for r in rows)}
    return out


def family_seconds(res):
    out = {}
    for r in res["runs"]:
        k = r.get("family") or r["command"]
        out[k] = round(out.get(k, 0.0) + r["seconds"], 1)
    return out


def totals_text(totals):
    head = "%-8s %-12s %3s %3s %11s %9s %9s %7s %7s %6s %5s %6s %7s %5s %9s" % (
        "case", "status", "t", "d", "examined", "F0", "F1", "F2", "F3", "differ", "C1", "HF", "tables", "pure", "mem/s/w")
    lines = [head]
    for t in totals.values():
        lines.append("%-8s %-12s %3d %3d %11s %9s %9s %7s %7s %6s %5s %6s %7s %5s %9s" % (
            t["key"], t["status"], t["t"], t["d"], "{:,}".format(t["examined"]), "{:,}".format(t["f0"]), "{:,}".format(t["f1"]),
            "{:,}".format(t["f2"]), "{:,}".format(t["f3"]), t["differ"], t["c1"], t["pure_hilbert"], t["tables"], t["pure"],
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
    L = ["# EXP-020: results", "",
         "Generated by `make_summary.py` from `artifacts/results.json`; every count is read from there.  Counts and members only; the",
         "verdict is written by the coordinating session.  The hypothesis is `hypothesis.md` (frozen).", ""]
    L += ["## Gates", ""]
    g1 = g.get("G1")
    if g1:
        L.append("- G1, the controls against the table of the probe: " + "; ".join(
            "(%d, %d) t = %d: %s members, %s with (F0) where (F1) and (F2) differ, %s pass, %s with (C1) (probe: %s, %s, %s, %s; stage vector %s "
            "the probe's); %s pure" % (r["pair"][0], r["pair"][1], r["t"], "{:,}".format(r["got"]["members"]), r["got"]["differ"],
                                       r["got"]["passing"], r["got"]["c1"], "{:,}".format(r["want"]["members"]), r["want"]["differ"],
                                       r["want"]["passing"], r["want"]["c1"], "equal to" if r["stages_equal"] else "different from",
                                       r["pure"]) if not r.get("missing") else "(%d, %d): not run" % tuple(r["pair"]) for r in g1["rows"]) +
                 "; %s." % ("passed" if g1["passed"] else "FAILED"))
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
          "Columns: t = the exponent, d = (e - t)/2, nu = the least non-residue; members = 2 (p^(d+1) - 1), all enumerated; stages: members "
          "passing (F0), (F1), (F2), (F3) in turn (F3 = passing the whole filter); differ = members with (F0) where (F1) and (F2) differ; C1 = "
          "passing members with Delta coprime to A_(e-t); HF = passing members with the pure Hilbert function (staged test of EXP-010, run on "
          "every passing member); tables = Betti tables computed (uhlib) on the passing members in the order of their index (stop at 5 pure or "
          "40 tables); pure = tables with the Betti table (1, 2, 2, 1) in degrees (0, e, 3e, 4e); the throughput is the filter alone "
          "(members per second on one worker process).", "",
          "| case | t | d | stratum | nu | status | members | examined | F0 | F1 | F2 | F3 | differ | C1 | HF | tables | pure | filter members/s/worker "
          "| worker s | wall s |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    rows = [[t["key"], t["t"], t["d"], "S(%d; %d, %d)" % tuple(t["stratum"]), t["nu"], t["status"], "{:,}".format(t["members"]),
             "{:,}".format(t["examined"]), "{:,}".format(t["f0"]), "{:,}".format(t["f1"]), "{:,}".format(t["f2"]), "{:,}".format(t["f3"]),
             t["differ"], t["c1"], t["pure_hilbert"], t["tables"], t["pure"],
             "n/a" if t["filter_members_per_second_per_worker"] is None else "{:,}".format(t["filter_members_per_second_per_worker"]),
             t["worker_seconds"], t["wall_seconds"]] for t in tot.values()]
    L += [_table_rows(rows), ""]
    L += ["## Members stopped at each stage", "", "| case | stopped at (F0) | stopped at (F1) | stopped at (F2) | stopped at (F3) | passing |",
          "|---|---|---|---|---|---|"]
    for t in tot.values():
        if t["examined"]:
            L.append("| %s | %s |" % (t["key"], " | ".join("{:,}".format(v) for v in t["stage_counts"])))
    L.append("")
    L += ["## Share passing the filter", "", "| case | passing | 2 p^2 | passing / (2 p^2) |", "|---|---|---|---|"]
    for t in tot.values():
        if t["examined"]:
            L.append("| %s | %s | %s | %s |" % (t["key"], t["f3"], t["two_p2"], _fmt(t["ratio"])))
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
        pure = [m for m in _members(s) if m.get("pure")]
        L.append("### %s (e = %d, p = %d, t = %d): %d pure of %d tables, %d passing members" % (
            c["key"], c["e"], c["p"], c["t"], s["pure"], s["tables"], s["counts"]["f3"]))
        if s.get("nonpure_tables"):
            L += ["", "Tables that are not pure: " + "; ".join("%s x %d" % (k, v) for k, v in sorted(s["nonpure_tables"].items())) + "."]
        if not pure:
            L += ["", ("No pure member among the %d passing members (the list is complete, a result)." % s["counts"]["f3"]
                       if s.get("status") == "complete" else "No pure member yet."), ""]
            continue
        for m in pure[:SHOWN]:
            r2 = _g2_row(res, c["key"], m["index"])
            L += ["", "- member %d: alpha = %s, c = %s, beta = %s, form c = %s, form c' = %s, (C1) %s" % (
                m["index"], m["alpha"], m["scalar"], m["beta"], m["form_c"], m["form_cp"], m["c1"]),
                  "  - f = %s" % X.poly_text(c["e"], c["p"], m["f"]), "  - g = %s" % X.poly_text(c["e"], c["p"], m["g"]),
                  "  - Betti table, first instrument: %s; length %s (e^3 = %d)" % (_betti(m["betti"]), m.get("length"), c["e"] ** 3),
                  "  - Betti table, second instrument: %s" % ("not computed" if r2 is None else (
                      _betti(r2["betti_I2"]) if "betti_I2" in r2 else "no result (%s)" % r2.get("error")))]
        L.append("")
    L += ["## Predictions", ""]
    p1 = pred["P1"]
    L.append("- P1 (%s): %s" % (p1["statement"], "; ".join("(%d, %d) %s (%s)" % (r["pair"][0], r["pair"][1], r["outcome"], r["why"])
                                                         for r in p1["rows"])))
    p2 = pred["P2"]
    L.append("- P2 (%s): %s on the cases done; %s" % (p2["statement"], "holds" if p2["holds_on_cases_done"] else "does not hold", "; ".join(
        "%s %s (%s of %s)" % (r["case"], r["outcome"], r.get("differ", "n/a"), r.get("with_f0", "n/a")) for r in p2["rows"])))
    p3 = pred["P3"]
    L.append("- P3 (%s): %s on the cases done; %s" % (p3["statement"], "holds" if p3["holds_on_cases_done"] else "does not hold", "; ".join(
        "%s %s (pure Hilbert function %s of %s; tables with (C1) %s, pure %s; tables without (C1) %s, pure %s)" % (
            r["case"], r["outcome"], r["pure_hilbert"], r["pass_filter"], r["tables_c1"], r["pure_c1"], r["tables_no_c1"], r["pure_no_c1"])
        if "tables_c1" in r else "%s %s" % (r["case"], r["outcome"]) for r in p3["rows"])))
    p4 = pred["P4"]
    L.append("- P4 (%s): %s on the cases done; %s" % (p4["statement"], "holds" if p4["holds_on_cases_done"] else "does not hold", "; ".join(
        "%s %s (%s passing, ratio %s)" % (r["case"], r["outcome"], r["pass_filter"], _fmt(r["ratio"])) if "ratio" in r
        else "%s %s" % (r["case"], r["outcome"]) for r in p4["rows"])))
    L.append("")
    Path(path).write_text("\n".join(L), encoding="utf-8", newline="\n")
