"""EXP-015: totals per case, the predictions P1 and P2 as counts, and results-summary.md, all computed from artifacts/results.json.

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

TITLE = {"K": "Family K: controls on settled pairs", "L": "Family L: the stratum S(e - 1; 0, 1) at e = 10 to 13",
         "R": "Family R: the strata of e = 9 at (9, 5), (9, 11), (9, 13)"}
L_PURE = {(10, 17), (10, 19), (11, 19), (12, 23), (13, 23)}


def stratum_name(s):
    return "L-stratum" if (s["m"], s["i"], s["j"]) == (s["e"] - 1, 0, 1) else "stratum"


def _cases(res):
    return sorted(res["strata"].values(), key=lambda s: ("KLR".index(s["family"]), s["e"], s["p"], -s["m"], s["i"], s["j"]))


def compute_totals(res):
    out = {}
    for s in _cases(res):
        key = "%s|%d|%d|%d|%d|%d" % (s["family"], s["e"], s["p"], s["m"], s["i"], s["j"])
        out[key] = {"key": key, "family": s["family"], "e": s["e"], "p": s["p"], "stratum": [s["m"], s["i"], s["j"]],
                    "name": stratum_name(s), "r": X.target_rank(s["e"]), "N": s["N"], "planned": s["planned"], "examined": s["examined"],
                    "all_members": bool(s["all_members"] and s["complete"]), "complete": s["complete"], "rank_r": s["rank_r"],
                    "pure_hilbert": s["pure_hilbert"], "tables": s["tables"], "pure": s["pure"], "stopped_early": s["stopped_early"],
                    "stopped_by": s["stopped_by"], "wall_seconds": s["wall_seconds"], "worker_seconds": s["worker_seconds"]}
    return out


def _case(res, fam, e, p, name=None):
    for s in res["strata"].values():
        if (s["family"], s["e"], s["p"]) == (fam, e, p) and (name is None or stratum_name(s) == name):
            return s
    return None


def _confirmed(res, s):
    rows = res["gates"].get("G2", {}).get("rows", [])
    key = "%s|%d|%d|%d|%d|%d" % (s["family"], s["e"], s["p"], s["m"], s["i"], s["j"])
    return sum(1 for r in rows if r["stratum"] == key and r.get("agree") and r.get("pure_I2"))


def _row(res, s):
    return None if s is None else {"examined": s["examined"], "all_members": bool(s["all_members"] and s["complete"]), "rank_r": s["rank_r"],
                                   "pure_hilbert": s["pure_hilbert"], "pure": s["pure"], "confirmed_by_second_instrument": _confirmed(res, s)}


def predictions(res, totals):
    """P1 (twelve outcomes of family L) and P2 (family R, per pair and overall) as counts; a prediction that does not hold is a result."""
    P = {"P1": {}, "P2": {}}
    for s in res["strata"].values():
        pair = "%d,%d" % (s["e"], s["p"])
        if s["family"] == "L":
            row = _row(res, s)
            row["expect_pure"] = (s["e"], s["p"]) in L_PURE
            row["holds"] = (s["pure"] > 0) == row["expect_pure"]
            P["P1"][pair] = row
    byp = {}
    for s in res["strata"].values():
        if s["family"] == "R":
            d = byp.setdefault((s["e"], s["p"]), {"strata_done": 0, "pure": 0, "examined": 0, "rank_r": 0, "pure_hilbert": 0, "confirmed": 0})
            d["strata_done"] += 1
            d["pure"] += s["pure"]
            d["examined"] += s["examined"]
            d["rank_r"] += s["rank_r"]
            d["pure_hilbert"] += s["pure_hilbert"]
            d["confirmed"] += _confirmed(res, s)
    for (e, p), d in sorted(byp.items(), key=lambda kv: [(9, 5), (9, 11), (9, 13)].index(kv[0])):
        d["holds"] = d["pure"] > 0
        P["P2"]["%d,%d" % (e, p)] = d
    P["P1_counts"] = {"cases_done": len(P["P1"]), "holding": sum(1 for v in P["P1"].values() if v["holds"]), "planned": 12}
    P["P2_counts"] = {"pairs_with_a_pure_member": sum(1 for v in P["P2"].values() if v["holds"]), "pairs_started": len(P["P2"])}
    return P


def _share(n):
    return "{:,}".format(n) if isinstance(n, int) else "-"


def totals_text(totals):
    lines = ["%-3s %-8s %-12s %-10s %-9s %-14s %-7s %-8s %-6s %-6s" % ("fam", "(e, p)", "stratum", "N", "examined", "mode", "rank r", "pure HF",
                                                                      "tables", "pure")]
    for t in totals.values():
        lines.append("%-3s %-8s %-12s %-10s %-9s %-14s %-7s %-8s %-6s %-6s" % (
            t["family"], "(%d, %d)" % (t["e"], t["p"]), "S(%d;%d,%d)" % tuple(t["stratum"]), _share(t["N"]), _share(t["examined"]),
            "all members" if t["all_members"] else "sampled", _share(t["rank_r"]), _share(t["pure_hilbert"]), t["tables"], t["pure"]))
    return "\n".join(lines)


def _rows(rows):
    return "none" if rows is None else "; ".join("b_%d,%d = %d" % tuple(r) for r in rows)


def _hist(h, limit=6):
    items = sorted(h.items(), key=lambda kv: -kv[1])
    return ", ".join("%s: %d" % kv for kv in items[:limit]) + (", ... (%d values)" % len(items) if len(items) > limit else "")


def _gate_lines(res):
    L = []
    g = res["gates"]
    r = g.get("G1")
    if r is None:
        L.append("- G1: not run")
    else:
        fam = r.get("family")
        L.append("- G1: fixed member %s; family part %s" % ("passed" if r["fixed"]["ok"] else "FAILED", "not checked" if fam is None else (
            "passed" if fam["passed"] else "FAILED")))
        for row in (fam or {}).get("rows", []):
            L.append("    - (%d, %d): expect %s; %s%s" % (row["pair"][0], row["pair"][1], row["expect"], (
                "pure %s" % row["pure"] if "pure" in row else "%s with the pure Hilbert function among %s examined (all members: %s)" % (row["pure_hilbert"], row["examined"], row["all_members"])),
                " (ok)" if row["ok"] else " (NOT ok)"))
    r = g.get("G2")
    L.append("- G2: not run" if r is None else "- G2: BLOCKED, %s" % r["reason"] if r.get("blocked") else
             "- G2: %s (%s; %d pure members in the sample, %d with the same pure table from both instruments)" % (
                 "PASSED" if r["passed"] else "FAILED", r["singular"], r["sample_members"], r["agree_and_pure_in_I2"]))
    r = g.get("G3")
    L.append("- G3: not run" if r is None else "- G3: %s (exit code %d; %s)" % ("PASSED" if r["passed"] else "FAILED", r["exit_code"], r["last_line"]))
    return L


def write_summary(res, path):
    T, P = res["totals"], res["predictions"]
    L = ["# EXP-015 results summary", "",
         "Generated by make_summary.py from artifacts/results.json; every number below is computed, none is typed.",
         "Hypothesis: hypothesis.md (frozen). Counts and members only: no statement of realizability is made here.", "",
         "Notation: a case is one stratum S(m; i, j) at (e, p). r = 2 u(2e) - 2. 'Examined' counts the members whose rank of mu_3e was "
         "computed ('all members' or 'sampled'); 'rank r' those with that rank; 'pure Hilbert function' those that also pass the staged "
         "test; 'tables' the Betti tables computed by uhlib; 'pure' those whose table is (1, 2, 2, 1) on (0, e, 3e, 4e). A case stops "
         "once it has 5 pure members (chunks already started finish and are counted).", "", "## Gates", ""] + _gate_lines(res)
    L += ["", "## Table of the cases", "", "| Family | e | p | Stratum | d_i | d_j | N | Examined | Mode | r | Rank r | Pure Hilbert function | Tables "
          "| Pure | Stop | Wall seconds |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for s in _cases(res):
        t = T["%s|%d|%d|%d|%d|%d" % (s["family"], s["e"], s["p"], s["m"], s["i"], s["j"])]
        stop = "early stop" if s["stopped_early"] else "cut: " + s["stopped_by"] if s["stopped_by"] else (
            "tables cap" if s["tables_cap_reached"] else "budget done" if s["complete"] else "partial")
        L.append("| %s | %d | %d | %s S(%d; %d, %d) | %d | %d | %s | %s of %s | %s | %d | %s | %s | %d | %d | %s | %.0f |" % (
            s["family"], s["e"], s["p"], t["name"], s["m"], s["i"], s["j"], s["d_i"], s["d_j"], _share(s["N"]), _share(s["examined"]),
            _share(s["planned"]), "all members" if t["all_members"] else "sampled", t["r"], _share(s["rank_r"]), _share(s["pure_hilbert"]),
            s["tables"], s["pure"], stop, s["wall_seconds"]))
    L += ["", "## Predictions as counts", ""]
    L.append("- P1 (family L: a pure member in each pair with 2e - p <= 3, in none with 2e - p >= 5): %d of %d cases run, %d outcomes as stated:" % (
        P["P1_counts"]["cases_done"], P["P1_counts"]["planned"], P["P1_counts"]["holding"]))
    for pair, v in P["P1"].items():
        L.append("    - (%s): expected %s; %s examined%s, rank r %s, pure Hilbert function %s, pure %d, %d confirmed by Singular; outcome %s" % (
            pair, "pure members" if v["expect_pure"] else "none", _share(v["examined"]), " (all members)" if v["all_members"] else " (sampled)",
            _share(v["rank_r"]), _share(v["pure_hilbert"]), v["pure"], v["confirmed_by_second_instrument"],
            "as stated" if v["holds"] else "NOT as stated"))
    if not P["P1"]:
        L.append("    - not run")
    L.append("- P2 (family R: a pure member in at least one of (9, 5), (9, 11), (9, 13)): %d of %d pairs started hold a pure member:" % (
        P["P2_counts"]["pairs_with_a_pure_member"], P["P2_counts"]["pairs_started"]))
    for pair, v in P["P2"].items():
        L.append("    - (%s): %d of 12 strata stored; %s members examined in all, rank r %s, pure Hilbert function %s, pure %d, %d confirmed by "
                 "Singular; %s" % (pair, v["strata_done"], _share(v["examined"]), _share(v["rank_r"]), _share(v["pure_hilbert"]), v["pure"],
                                   v["confirmed"], "a pure member found" if v["holds"] else "no pure member found"))
    if not P["P2"]:
        L.append("    - not run")
    g2 = {(r["stratum"], r["index"]): r for r in res["gates"].get("G2", {}).get("rows", [])}
    for fam in ("K", "L", "R"):
        cs = [s for s in _cases(res) if s["family"] == fam]
        if not cs:
            continue
        L += ["", "## " + TITLE[fam], ""]
        for s in cs:
            e, p = s["e"], s["p"]
            key = "%s|%d|%d|%d|%d|%d" % (fam, e, p, s["m"], s["i"], s["j"])
            L += ["", "### (e, p) = (%d, %d), %s S(%d; %d, %d)" % (e, p, stratum_name(s), s["m"], s["i"], s["j"]), "",
                  "Distribution of rank mu_3e: %s. Seed: %s." % (_hist(s["rank_hist"]), s["seed"] if s["seed"] is not None else "none (enumerated)")]
            pure = [m for m in s["members"] if m["pure"]][:3]
            if not pure:
                L += ["", "No member with the pure Betti table among the %s members examined." % _share(s["examined"])]
            for m in pure:
                r2 = g2.get((key, m["index"]))
                L.append("- member %d: f = %s ; g = %s ; uhlib: %s ; Singular: %s" % (
                    m["index"], X.poly_text(e, p, m["f"]), X.poly_text(e, p, m["g"]), _rows(m["betti"]),
                    "not run on this member" if not r2 else (_rows(r2["betti_I2"]) if "betti_I2" in r2 else "error: %s" % r2.get("error"))))
            if s["nonpure_tables"]:
                L.append("- members with the pure Hilbert function and another Betti table: %s" % "; ".join(
                    "%s x %d" % kv for kv in s["nonpure_tables"].items()))
    runs = res["runs"]
    L += ["", "Time of the commands: " + ", ".join("%s%s%s %.0f s" % (r["command"], " " + r["family"] if r.get("family") else "",
                                                                       " (%s)" % r["only"] if r.get("only") else "", r["seconds"])
                                                    for r in runs) + "; total %.0f s." % res.get("wall_seconds_total", 0), ""]
    Path(path).write_text("\n".join(L), encoding="utf-8", newline="\n")
