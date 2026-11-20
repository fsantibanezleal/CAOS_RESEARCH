"""EXP-017: totals per case, the predictions P1 to P4 as counts, and results-summary.md, all computed from artifacts/results.json.

Every number of results-summary.md is computed from the stored cases, none is typed.  Counts and members only: no statement about
realizability is made here (the coordinating session draws the conclusions).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP10 = HERE.parent / "EXP-010-weight-class-strata"
if str(EXP10) not in sys.path:
    sys.path.append(str(EXP10))

import exp010_routine as X  # noqa: E402

TITLE = {"K": "Family K: controls on settled pairs", "Q": "Family Q: the question", "X": "Family X: exploratory"}
P1_LOW, P1_HIGH = 0.05, 2.0
SHOWN = 3  # pure members printed per case


def _key_parts(key):
    fam, e, p = key.split("|")
    return fam, int(e), int(p)


def _order(key):
    fam, e, p = _key_parts(key)
    return ("KQX".index(fam), {"K": [(5, 7), (7, 5), (7, 11), (9, 7)], "Q": [(9, 11), (9, 13)], "X": [(11, 7), (13, 5)]}[fam].index((e, p)))


def _all_cases(res):
    """Finished cases (records) and unfinished ones (partial states, with the number of members done), in the order of the plan."""
    out = {}
    for key, s in res["partial"].items():
        fam, e, p = _key_parts(key)
        out[key] = {"family": fam, "e": e, "p": p, "budget": None, "examined": s["counts"]["examined"], "complete": False,
                    "stopped_early": False, "counts": s["counts"], "tables": s["tables"], "pure": s["pure"],
                    "members": s["members"], "worker_seconds": round(s["worker_seconds"], 1), "wall_seconds": s["wall_seconds"],
                    "status": "partial", "nonpure_tables": s["nonpure_tables"]}
    for key, s in res["cases"].items():
        out[key] = dict(s, status="complete" if s["complete"] else ("early stop" if s["stopped_early"] else "cut"))
    return [dict(out[k], key=k) for k in sorted(out, key=_order)]


PLAN_BUDGET = {(5, 7): 200_000, (7, 5): 2_000_000, (7, 11): 20_000_000, (9, 7): 60_000_000, (9, 11): 200_000_000, (9, 13): 400_000_000,
               (11, 7): 300_000_000, (13, 5): 200_000_000}


def compute_totals(res):
    out = {}
    for c in _all_cases(res):
        n = c["counts"]
        examined = n["examined"]
        e, p = c["e"], c["p"]
        out[c["key"]] = {
            "key": c["key"], "family": c["family"], "e": e, "p": p, "budget": c["budget"] or PLAN_BUDGET[(e, p)], "status": c["status"],
            "examined": examined, "block_f1": n["block_f1"], "f0": n["f0"], "f1": n["f1"], "f2": n["f2"], "f3": n["f3"],
            "pure_hilbert": n["pure_hilbert"], "tables": c["tables"], "pure": c["pure"],
            "share_f3": (n["f3"] / examined) if examined else None, "expected_share": float(p) ** -(e - 3),
            "stored": len(c["members"]), "worker_seconds": c["worker_seconds"], "wall_seconds": c["wall_seconds"],
            "members_per_second_per_worker": int(examined / max(c["worker_seconds"], 1e-9))}
    return out


def _g2_confirmed(res, key, index):
    for r in res["gates"].get("G2", {}).get("rows", []):
        if r["case"] == key and r["index"] == index:
            return bool(r.get("agree") and r.get("pure_I2"))
    return None


def predictions(res):
    tot = compute_totals(res)
    out = {}
    rows = []
    for t in tot.values():
        if t["examined"] == 0:
            continue
        ratio = None if t["share_f3"] is None else t["share_f3"] / t["expected_share"]
        rows.append({"case": t["key"], "examined": t["examined"], "pass_filter": t["f3"], "share": t["share_f3"],
                     "expected_share": t["expected_share"], "ratio": ratio, "holds": ratio is not None and P1_LOW <= ratio <= P1_HIGH})
    out["P1"] = {"statement": "the share of members that pass (F0) to (F3) is between 0.05 and 2 times p^-(e-3) in every case", "rows": rows,
                 "holds": bool(rows) and all(r["holds"] for r in rows)}

    def pure_at(e, p):
        for t in tot.values():
            if (t["e"], t["p"]) == (e, p) and t["family"] in ("Q", "X"):
                confirmed = sum(1 for c in _all_cases(res) if c["key"] == t["key"] for m in c["members"] if m.get("pure")
                                and _g2_confirmed(res, t["key"], m["index"]))
                return {"pair": [e, p], "status": t["status"], "examined": t["examined"], "pass_filter": t["f3"], "pure": t["pure"],
                        "confirmed_by_second_instrument": confirmed, "found": t["pure"] > 0}
        return {"pair": [e, p], "status": "not run", "found": None}

    a, b = pure_at(9, 11), pure_at(9, 13)
    out["P2"] = {"statement": "a pure member is found at (9, 11); at (9, 13); at one of the two", "pairs": [a, b],
                 "either": None if a["found"] is None and b["found"] is None else bool(a["found"] or b["found"])}
    out["P3"] = {"statement": "a pure member is found at (11, 7); at (13, 5)", "pairs": [pure_at(11, 7), pure_at(13, 5)]}
    rows = []
    for t in tot.values():
        if t["f3"] > 0:
            rows.append({"case": t["key"], "pass_filter": t["f3"], "pure_hilbert": t["pure_hilbert"], "share": t["pure_hilbert"] / t["f3"],
                         "holds": 2 * t["pure_hilbert"] >= t["f3"]})
    out["P4"] = {"statement": "in every case at least half of the members that pass the filter have the pure Hilbert function", "rows": rows,
                 "holds": bool(rows) and all(r["holds"] for r in rows)}
    return out


def totals_text(totals):
    head = "%-8s %-9s %15s %11s %9s %7s %7s %7s %6s %7s %5s %9s" % ("case", "status", "examined", "block F1", "F0", "F1", "F2", "F3",
                                                                    "HF", "tables", "pure", "mem/s/w")
    lines = [head]
    for t in totals.values():
        lines.append("%-8s %-9s %15s %11s %9s %7s %7s %7s %6s %7s %5s %9s" % (
            t["key"], t["status"], "{:,}".format(t["examined"]), "{:,}".format(t["block_f1"]), "{:,}".format(t["f0"]), t["f1"], t["f2"],
            t["f3"], t["pure_hilbert"], t["tables"], t["pure"], "{:,}".format(t["members_per_second_per_worker"])))
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
    L = ["# EXP-017: results", "",
         "Generated by `make_summary.py` from `artifacts/results.json`; every count is read from there.  Counts and members only; the",
         "verdict is written by the coordinating session.  The hypothesis is `hypothesis.md` (frozen).", ""]
    g = res["gates"]
    L += ["## Gates", ""]
    fx = g.get("G1", {}).get("fixed")
    if fx:
        L.append("- G1, the fixed member (the pure pair of EXP-014 at (9, 7), rescaled): filter stage %s of 4 (4 = passes (F0) to (F3)), "
                 "pure Hilbert function %s, Betti table %s; %s." % (fx["filter_stage"], fx["pure_hilbert"], _betti(fx.get("betti")),
                                                                    "passed" if fx["ok"] else "FAILED"))
    fam = g.get("G1", {}).get("family")
    if fam:
        L.append("- G1, the controls: " + "; ".join("(%d, %d): %s members examined, %s pass (F0) to (F3), %s pure" % (
            r["pair"][0], r["pair"][1], "{:,}".format(r["examined"] or 0), r["pass_filter"], r["pure"]) for r in fam["rows"]) +
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
    if res.get("throughput"):
        L += ["## Throughput", ""]
        for k, t in sorted(res["throughput"].items()):
            L.append("- (%s): %s members in %s s on one worker, %s members per second per worker (sampling %s s, block test of (F1) %s s, "
                     "exact filter and staged test %s s); the block test accepted %s members, %s passed all four tests." % (
                         k.replace(",", ", "), "{:,}".format(t["members"]), t["seconds"], "{:,}".format(t["members_per_second_per_worker"]),
                         t["sample_seconds"], t["block_f1_seconds"], t["exact_and_hilbert_seconds"], t["block_f1_accepted"],
                         t["pass_all_four"]))
        L.append("")
    L += ["## Cases", "",
          "Columns: members examined of the budget; block F1 = accepted by the block test of (F1) (degree of Delta, independent columns, "
          "solvable); F0 to F3 = passing (F0), (F1), (F2) and (F3) in turn, among the members the block test accepted (the exact test of "
          "(F0) includes the coprimality; a member that passes (F0) and the block test passes (F1)); HF = with the pure Hilbert function "
          "among those passing (F3); tables = Betti tables computed; pure = pure (first instrument).", "",
          "| case | status | examined | budget | block F1 | F0 | F1 | F2 | F3 | HF | tables | pure | members/s/worker | worker s | wall s |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    rows = [[t["key"], t["status"], "{:,}".format(t["examined"]), "{:,}".format(t["budget"]), "{:,}".format(t["block_f1"]),
             "{:,}".format(t["f0"]), t["f1"], t["f2"], t["f3"], t["pure_hilbert"], t["tables"], t["pure"],
             "{:,}".format(t["members_per_second_per_worker"]), t["worker_seconds"], t["wall_seconds"]] for t in tot.values()]
    L += [_table_rows(rows), ""]
    L += ["## Share passing the filter", "",
          "| case | passing (F0) to (F3) | share | p^-(e-3) | ratio |", "|---|---|---|---|---|"]
    for t in tot.values():
        if t["examined"]:
            L.append("| %s | %s | %s | %s | %s |" % (t["key"], t["f3"], _fmt(t["share_f3"]), _fmt(t["expected_share"]),
                                                    _fmt(t["share_f3"] / t["expected_share"] if t["share_f3"] is not None else None)))
    L.append("")
    L += ["## Pure members", ""]
    for c in _all_cases(res):
        pure = [m for m in c["members"] if m.get("pure")]
        L.append("### %s (e = %d, p = %d): %d pure of %d tables" % (c["key"], c["e"], c["p"], c["pure"], c["tables"]))
        if c.get("nonpure_tables"):
            L.append("")
            L.append("Tables that are not pure: " + "; ".join("%s x %d" % (k, v) for k, v in sorted(c["nonpure_tables"].items())) + ".")
        if not pure:
            L += ["", "No pure member (a result).", ""]
            continue
        for m in pure[:SHOWN]:
            conf = _g2_confirmed(res, c["key"], m["index"])
            L += ["", "- member %d: alpha = %s, beta = %s, c = %s, c' = %s" % (m["index"], m["alpha"], m["beta"], m["c"], m["cp"]),
                  "  - f = %s" % X.poly_text(c["e"], c["p"], m["f"]), "  - g = %s" % X.poly_text(c["e"], c["p"], m["g"]),
                  "  - Betti table, first instrument: %s" % _betti(m["betti"]),
                  "  - Betti table, second instrument: %s" % (
                      "not computed" if conf is None else _betti(next(r["betti_I2"] for r in g["G2"]["rows"] if r["case"] == c["key"] and
                                                                      r["index"] == m["index"])))]
        L.append("")
    L += ["## Predictions", ""]
    p1 = pred["P1"]
    L.append("- P1 (share between %s and %s times p^-(e-3) in every case): %s.  %s" % (
        P1_LOW, P1_HIGH, "holds" if p1["holds"] else "does not hold",
        "; ".join("%s ratio %s (%s of %s)" % (r["case"], _fmt(r["ratio"]), r["pass_filter"], "{:,}".format(r["examined"])) for r in p1["rows"])))
    p2 = pred["P2"]
    L.append("- P2 (a pure member at (9, 11), at (9, 13), at one of them): %s; either: %s." % (
        "; ".join("(%d, %d): %s" % (x["pair"][0], x["pair"][1], ("%d pure of %s members passing, %s confirmed by Singular" % (
            x["pure"], x["pass_filter"], x["confirmed_by_second_instrument"])) if x["found"] is not None else "not run") for x in p2["pairs"]),
        p2["either"]))
    p3 = pred["P3"]
    L.append("- P3 (a pure member at (11, 7), at (13, 5)): %s." % "; ".join(
        "(%d, %d): %s" % (x["pair"][0], x["pair"][1], ("%d pure of %s members passing (%s)" % (x["pure"], x["pass_filter"], x["status"]))
                          if x["found"] is not None else "not run") for x in p3["pairs"]))
    p4 = pred["P4"]
    L.append("- P4 (at least half of the members passing the filter have the pure Hilbert function in every case): %s.  %s" % (
        "holds" if p4["holds"] else "does not hold", "; ".join("%s %s of %s" % (r["case"], r["pure_hilbert"], r["pass_filter"]) for r in p4["rows"])))
    L.append("")
    Path(path).write_text("\n".join(L), encoding="utf-8", newline="\n")
