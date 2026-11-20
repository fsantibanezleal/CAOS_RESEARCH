"""EXP-018: totals per case, the predictions P1 to P3 as counts, and results-summary.md, all computed from artifacts/results.json.

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

FAMS = "KZT"
TITLE = {"K": "Family K: controls with known answers", "Z": "Family Z: the stratum with t + 2",
         "T": "Family T: the largest exponent t the characteristic allows"}
T_PAIRS = [(11, 17), (13, 19), (14, 23), (11, 13), (13, 17)]
P1_PRIOR = {(11, 17): 0.8, (13, 19): 0.8, (14, 23): 0.75, (11, 13): 0.5, (13, 17): 0.45}
P3_LOW, P3_HIGH, P3_MIN = 0.03, 3.0, 10


def tt(s):
    return 2 * s["m"] - s["e"]


def conditions(s):
    return s["e"] - tt(s) - 2


def _key(s):
    return "%s|%d|%d|%d|%d|%d" % (s["family"], s["e"], s["p"], s["m"], s["i"], s["j"])


def _cases(res):
    return sorted(res["strata"].values(), key=lambda s: (FAMS.index(s["family"]), s["e"], s["p"], -s["m"], s["i"], s["j"]))


def compute_totals(res):
    out = {}
    for s in _cases(res):
        key = _key(s)
        out[key] = {"key": key, "family": s["family"], "e": s["e"], "p": s["p"], "stratum": [s["m"], s["i"], s["j"]], "t": tt(s),
                    "r": X.target_rank(s["e"]), "d_i": s["d_i"], "d_j": s["d_j"], "N": s["N"], "planned": s["planned"],
                    "examined": s["examined"], "all_members": bool(s["all_members"] and s["complete"]), "complete": s["complete"],
                    "rank_r": s["rank_r"], "pure_hilbert": s["pure_hilbert"], "tables": s["tables"], "pure": s["pure"],
                    "stopped_early": s["stopped_early"], "stopped_by": s["stopped_by"], "seed": s["seed"],
                    "wall_seconds": s["wall_seconds"], "worker_seconds": s["worker_seconds"]}
    return out


def _confirmed(res, s):
    rows = res["gates"].get("G2", {}).get("rows", [])
    key = _key(s)
    return sum(1 for r in rows if r["stratum"] == key and r.get("agree") and r.get("pure_I2"))


def _row(res, s):
    return {"examined": s["examined"], "planned": s["planned"], "all_members": bool(s["all_members"] and s["complete"]),
            "complete": s["complete"], "rank_r": s["rank_r"], "pure_hilbert": s["pure_hilbert"], "tables": s["tables"], "pure": s["pure"],
            "confirmed_by_second_instrument": _confirmed(res, s)}


def predictions(res, totals):
    """P1 per pair of family T, P2 per stratum of family Z, P3 over the cases of families T and K; a prediction that does not hold is a
    result."""
    P = {"P1": {}, "P2": {}, "P3": {}}
    for s in res["strata"].values():
        pair = "%d,%d" % (s["e"], s["p"])
        if s["family"] == "T":
            row = _row(res, s)
            row["prior"] = P1_PRIOR[(s["e"], s["p"])]
            row["holds"] = s["pure"] > 0
            P["P1"][pair] = row
        elif s["family"] == "Z":
            row = _row(res, s)
            row["stratum"] = [s["m"], s["i"], s["j"]]
            row["holds"] = s["pure_hilbert"] == 0 and s["pure"] == 0
            P["P2"][pair] = row
        if s["family"] in ("T", "K"):
            c = conditions(s)
            base = float(s["p"]) ** (-c)
            row = {"pair": [s["e"], s["p"]], "stratum": [s["m"], s["i"], s["j"]], "conditions": c, "examined": s["examined"],
                   "pure_hilbert": s["pure_hilbert"], "reference": base, "applies": s["pure_hilbert"] >= P3_MIN}
            row["share"] = s["pure_hilbert"] / s["examined"] if s["examined"] else None
            row["ratio"] = row["share"] / base if row["share"] is not None else None
            row["holds"] = bool(row["applies"] and P3_LOW <= row["ratio"] <= P3_HIGH) if row["applies"] else None
            P["P3"]["%s|%s" % (s["family"], pair)] = row
    P["P1"] = {k: P["P1"][k] for k in ["%d,%d" % q for q in T_PAIRS] if k in P["P1"]}
    P["P1_counts"] = {"cases_done": len(P["P1"]), "with_a_pure_member": sum(1 for v in P["P1"].values() if v["holds"]), "planned": 5}
    P["P2_counts"] = {"cases_done": len(P["P2"]), "holding": sum(1 for v in P["P2"].values() if v["holds"]), "planned": 5,
                      "pure_hilbert_members_in_family_Z": sum(v["pure_hilbert"] for v in P["P2"].values())}
    ap = [v for v in P["P3"].values() if v["applies"]]
    P["P3_counts"] = {"cases_with_at_least_10_pure_hilbert": len(ap), "holding": sum(1 for v in ap if v["holds"]), "cases_considered": len(P["P3"])}
    return P


def _share(n):
    return "{:,}".format(n) if isinstance(n, int) else "-"


def totals_text(totals):
    lines = ["%-3s %-8s %-12s %-14s %-9s %-14s %-7s %-8s %-6s %-6s" % ("fam", "(e, p)", "stratum", "N", "examined", "mode", "rank r",
                                                                       "pure HF", "tables", "pure")]
    for t in totals.values():
        lines.append("%-3s %-8s %-12s %-14s %-9s %-14s %-7s %-8s %-6s %-6s" % (
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
            L.append("    - (%d, %d): expect %s; pure %s%s" % (row["pair"][0], row["pair"][1], row["expect"], row["pure"],
                                                              " (ok)" if row["ok"] else " (NOT ok)"))
    r = g.get("G2")
    L.append("- G2: not run" if r is None else "- G2: BLOCKED, %s" % r["reason"] if r.get("blocked") else
             "- G2: %s (%s; %d pure members in the sample, %d with the same pure table from both instruments)" % (
                 "PASSED" if r["passed"] else "FAILED", r["singular"], r["sample_members"], r["agree_and_pure_in_I2"]))
    r = g.get("G3")
    L.append("- G3: not run" if r is None else "- G3: %s (exit code %d; %s)" % ("PASSED" if r["passed"] else "FAILED", r["exit_code"], r["last_line"]))
    return L


def _outcome(v):
    return "as stated" if v["holds"] else "NOT as stated"


def write_summary(res, path):
    T, P = res["totals"], res["predictions"]
    L = ["# EXP-018 results summary", "",
         "Generated by make_summary.py from artifacts/results.json; every number below is computed, none is typed.",
         "Hypothesis: hypothesis.md (frozen). Counts and members only: no statement of realizability is made here.", "",
         "Notation: a case is one stratum S(m; i, j) at (e, p) with t = 2m - e. r = 2 u(2e) - 2. 'Examined' counts the members whose rank "
         "of mu_3e was computed ('all members' or 'sampled'); 'rank r' those with that rank; 'pure Hilbert function' those that also pass "
         "the staged test; 'tables' the Betti tables computed by uhlib; 'pure' those whose table is (1, 2, 2, 1) on (0, e, 3e, 4e). A case "
         "stops once it has 5 pure members (chunks already started finish and are counted).", "", "## Gates", ""] + _gate_lines(res)
    L += ["", "## Table of the cases", "", "| Family | e | p | t | Stratum | d_i | d_j | N | Examined | Mode | r | Rank r | Pure Hilbert function | "
          "Tables | Pure | Stop | Wall seconds |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for s in _cases(res):
        t = T[_key(s)]
        stop = "early stop" if s["stopped_early"] else "cut: " + s["stopped_by"] if s["stopped_by"] else (
            "tables cap" if s["tables_cap_reached"] else "budget done" if s["complete"] else "partial")
        L.append("| %s | %d | %d | %d | S(%d; %d, %d) | %d | %d | %s | %s of %s | %s | %d | %s | %s | %d | %d | %s | %.0f |" % (
            s["family"], s["e"], s["p"], t["t"], s["m"], s["i"], s["j"], s["d_i"], s["d_j"], _share(s["N"]), _share(s["examined"]),
            _share(s["planned"]), "all members" if t["all_members"] else "sampled", t["r"], _share(s["rank_r"]), _share(s["pure_hilbert"]),
            s["tables"], s["pure"], stop, s["wall_seconds"]))
    L += ["", "## Predictions as counts", ""]
    L.append("- P1 (family T: a pure pair at the largest t): %d of %d cases run, %d with a pure member:" % (
        P["P1_counts"]["cases_done"], P["P1_counts"]["planned"], P["P1_counts"]["with_a_pure_member"]))
    for pair, v in P["P1"].items():
        L.append("    - (%s): prior %.2f; %s examined of %s planned%s, rank r %s, pure Hilbert function %s, tables %d, pure %d, %d confirmed by "
                 "Singular; %s" % (pair, v["prior"], _share(v["examined"]), _share(v["planned"]), " (all members)" if v["all_members"] else
                                   " (sampled)", _share(v["rank_r"]), _share(v["pure_hilbert"]), v["tables"], v["pure"],
                                   v["confirmed_by_second_instrument"], "a pure member found" if v["holds"] else "no pure member found"))
    if not P["P1"]:
        L.append("    - not run")
    L.append("- P2 (family Z: no member with the pure Hilbert function): %d of %d cases run, %d members with the pure Hilbert function in all; "
             "%d cases as stated:" % (P["P2_counts"]["cases_done"], P["P2_counts"]["planned"],
                                      P["P2_counts"]["pure_hilbert_members_in_family_Z"], P["P2_counts"]["holding"]))
    for pair, v in P["P2"].items():
        L.append("    - (%s) S(%d; %d, %d): %s examined of %s planned%s, rank r %s, pure Hilbert function %s, pure %d; %s" % (
            pair, v["stratum"][0], v["stratum"][1], v["stratum"][2], _share(v["examined"]), _share(v["planned"]),
            " (all members)" if v["all_members"] else " (sampled)", _share(v["rank_r"]), _share(v["pure_hilbert"]), v["pure"], _outcome(v)))
    if not P["P2"]:
        L.append("    - not run")
    L.append("- P3 (density, cases of families T and K with at least 10 members with the pure Hilbert function; share within 0.03 to 3 times "
             "p^-(e-t-2)): %d cases apply, %d as stated:" % (P["P3_counts"]["cases_with_at_least_10_pure_hilbert"], P["P3_counts"]["holding"]))
    for k, v in P["P3"].items():
        L.append("    - %s (%d, %d) S(%d; %d, %d): pure Hilbert function %s of %s examined, share %s, reference p^-%d = %.3e, ratio %s; %s" % (
            k.split("|")[0], v["pair"][0], v["pair"][1], v["stratum"][0], v["stratum"][1], v["stratum"][2], _share(v["pure_hilbert"]),
            _share(v["examined"]), "%.3e" % v["share"] if v["share"] is not None else "-", v["conditions"], v["reference"],
            "%.3f" % v["ratio"] if v["ratio"] is not None else "-", "does not apply (fewer than 10)" if not v["applies"] else _outcome(v)))
    if not P["P3"]:
        L.append("    - not run")
    g2 = {(r["stratum"], r["index"]): r for r in res["gates"].get("G2", {}).get("rows", [])}
    for fam in FAMS:
        cs = [s for s in _cases(res) if s["family"] == fam]
        if not cs:
            continue
        L += ["", "## " + TITLE[fam], ""]
        for s in cs:
            e, p = s["e"], s["p"]
            key = _key(s)
            L += ["", "### (e, p) = (%d, %d), t = %d, S(%d; %d, %d)" % (e, p, tt(s), s["m"], s["i"], s["j"]), "",
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
