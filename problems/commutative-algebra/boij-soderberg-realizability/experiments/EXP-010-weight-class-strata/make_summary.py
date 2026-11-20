"""EXP-010: totals per pair, the predictions P1 to P5 as counts, and results-summary.md, all computed from artifacts/results.json.

Every number of results-summary.md is computed from the stored strata, none is typed.  Counts and members only: no statement about
realizability is made here (the coordinating session draws the conclusions).
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import exp010_routine as X  # noqa: E402

FAMILY_PAIRS = {"C": X.FAMILY_C_PAIRS, "Q": X.FAMILY_Q_PAIRS, "E": X.FAMILY_E_PAIRS}
FAMILY_TITLE = {"C": "Family C: controls on settled pairs", "Q": "Family Q: the five open pairs",
                "E": "Family E: e = 8, exploratory"}
P2_LOW, P2_HIGH = 0.1, 1.5


def pair_key(family, e, p):
    return "%s|%d|%d" % (family, e, p)


def _strata_of(res, family, e, p):
    return sorted((s for s in res["strata"].values() if s["family"] == family and s["e"] == e and s["p"] == p),
                  key=lambda s: (-s["m"], s["i"], s["j"]))


def compute_totals(res):
    out = {}
    for fam in X.FAMILIES:
        plans = {}
        for spec in X.plan_family(fam):
            plans.setdefault((spec["e"], spec["p"]), []).append(spec)
        for e, p in FAMILY_PAIRS[fam]:
            ss = _strata_of(res, fam, e, p)
            if not ss:
                continue
            planned = plans[(e, p)]
            h = X.h_e(e, 3 * e)
            s20 = next((s for s in ss if (s["m"], s["i"], s["j"]) == (2, 0, 1)), None)
            t = {"key": pair_key(fam, e, p), "family": fam, "e": e, "p": p, "r": X.target_rank(e), "h_3e": h,
                 "strata_planned": len(planned), "strata_stored": len(ss),
                 "strata_cut": [s for s in ss if s["stopped_by"]], "finished": len(ss) == len(planned) and not any(
                     s["stopped_by"] for s in ss),
                 "strata_with_members": sum(1 for s in ss if s["planned"] > 0),
                 "strata_with_rank_r": sum(1 for s in ss if s["rank_r"]),
                 "strata_with_pure_hilbert": sum(1 for s in ss if s["pure_hilbert"]),
                 "strata_with_pure": sum(1 for s in ss if s["pure"]), "members_examined": sum(s["examined"] for s in ss),
                 "rank_r": sum(s["rank_r"] for s in ss), "pure_hilbert": sum(s["pure_hilbert"] for s in ss),
                 "tables": sum(s["tables"] for s in ss), "pure": sum(s["pure"] for s in ss),
                 "rank_r_when_p_divides_m": sum(s["rank_r"] for s in ss if s["m"] % p == 0),
                 "examined_when_p_divides_m": sum(s["examined"] for s in ss if s["m"] % p == 0),
                 "worker_seconds": round(sum(s["worker_seconds"] for s in ss), 1),
                 "wall_seconds_sum": round(sum(s["wall_seconds"] for s in ss), 1)}
            if s20 and s20["examined"]:
                share = s20["pure_hilbert"] / s20["examined"]
                t["s20"] = {"examined": s20["examined"], "all_members": s20["all_members"] and s20["complete"], "pure_hilbert": s20["pure_hilbert"],
                            "pure": s20["pure"], "stopped_early": s20["stopped_early"], "share": share, "p_power": p ** -h,
                            "ratio": share * p ** h}
            else:
                t["s20"] = None
            out[t["key"]] = t
    return out


def predictions(res, totals):
    g2 = res["gates"].get("G2", {})
    g2_rows = g2.get("rows", [])

    def confirmed(fam, e, p):
        return sum(1 for r in g2_rows if r.get("agree") and r.get("pure_I2") and r["stratum"].startswith("%s|%d|%d|" % (fam, e, p)))

    p1, p2, p4, p5 = {}, {}, {}, {}
    for e, p in X.FAMILY_Q_PAIRS:
        t = totals.get(pair_key("Q", e, p))
        if t:
            p1["%d,%d" % (e, p)] = {"pure_members": t["pure"], "strata_with_pure": t["strata_with_pure"], "confirmed_by_second_instrument": confirmed(
                "Q", e, p), "strata_stored": t["strata_stored"], "strata_planned": t["strata_planned"], "pair_finished": t["finished"],
                "holds": t["pure"] > 0}
    for fam in ("Q", "C"):
        for e, p in FAMILY_PAIRS[fam]:
            t = totals.get(pair_key(fam, e, p))
            if not t:
                continue
            if t["s20"] and t["s20"]["pure_hilbert"] > 0:
                s = t["s20"]
                p2["%s %d,%d" % (fam, e, p)] = {"pure_hilbert": s["pure_hilbert"], "examined": s["examined"], "share": s["share"],
                                                "ratio_to_p_power": s["ratio"], "stopped_early": s["stopped_early"],
                                                "holds": P2_LOW <= s["ratio"] <= P2_HIGH}
            p4["%s %d,%d" % (fam, e, p)] = {"rank_r_in_strata_with_p_dividing_m": t["rank_r_when_p_divides_m"],
                                            "members_examined_there": t["examined_when_p_divides_m"], "holds": t["rank_r_when_p_divides_m"] == 0}
    p3 = {"G4": res["gates"].get("G4"), "holds": bool(res["gates"].get("G4", {}).get("passed"))}
    for e, p in X.FAMILY_E_PAIRS:
        t = totals.get(pair_key("E", e, p))
        if not t:
            continue
        s7 = next((s for s in _strata_of(res, "E", e, p) if (s["m"], s["i"], s["j"]) == (7, 0, 1)), None)
        row = {"pure_members": t["pure"], "strata_with_pure": t["strata_with_pure"], "strata_stored": t["strata_stored"],
               "strata_planned": t["strata_planned"], "pair_finished": t["finished"],
               "confirmed_by_second_instrument": confirmed("E", e, p)}
        if p in (11, 13):
            row["S(7; 0, 1)"] = None if s7 is None else {"pure": s7["pure"], "examined": s7["examined"], "complete": s7["complete"]}
            row["holds"] = bool(s7 and s7["pure"] > 0)
        else:
            row["holds"] = t["pure"] > 0
        p5["%d,%d" % (e, p)] = row
    return {"P1": p1, "P2": p2, "P3": p3, "P4": p4, "P5": p5}


def _share(s):
    return "-" if not s else "%.3g (%d of %d%s)" % (s["share"], s["pure_hilbert"], s["examined"], ", all members" if s["all_members"] else "")


def totals_text(totals):
    lines = ["%-4s %-8s %-9s %-9s %-8s %-9s %-7s %-6s %-26s %-8s" % (
        "fam", "(e, p)", "strata", "with rank", "with", "members", "pure", "pure", "share of pure Hilbert", "ratio")]
    lines.append("%-4s %-8s %-9s %-9s %-8s %-9s %-7s %-6s %-26s %-8s" % (
        "", "", "stored", "r", "pure", "examined", "Hilbert", "", "in S(2; 0, 1)", ""))
    for t in totals.values():
        s = t["s20"]
        lines.append("%-4s %-8s %-9s %-9d %-8d %-9d %-7d %-6d %-26s %-8s" % (
            t["family"], "(%d, %d)" % (t["e"], t["p"]), "%d/%d%s" % (t["strata_stored"], t["strata_planned"], "" if t["finished"] else "*"),
            t["strata_with_rank_r"], t["strata_with_pure"], t["members_examined"], t["pure_hilbert"], t["pure"], _share(s),
            "-" if not s else "%.3g" % s["ratio"]))
    lines.append("(* the pair did not finish: strata not run or cut by the time budget)")
    return "\n".join(lines)


def _rows(rows):
    return "none" if rows is None else "; ".join("b_%d,%d = %d" % tuple(r) for r in rows)


def _hist(h, limit=6):
    items = sorted(h.items(), key=lambda kv: -kv[1])
    s = ", ".join("%s: %d" % kv for kv in items[:limit])
    return s + (", ... (%d values)" % len(items) if len(items) > limit else "")


def _f(n):
    return "-" if n is None else "{:,}".format(n)


def write_summary(res, path):
    T, P = res["totals"], res["predictions"]
    L = ["# EXP-010 results summary", "",
         "Generated by make_summary.py from artifacts/results.json; every number below is computed, none is typed.",
         "Hypothesis: hypothesis.md (frozen). Counts and members only: no statement of realizability is made here.", "",
         "Notation: a stratum is S(m; i, j) with f on the monomials of weight class i and g on class j modulo m. r = 2 u(2e) - 2. "
         "'Examined' counts the members whose rank of mu_3e was computed (all members when 'all'; the first members of the enumeration when 'in order, stopped early', which the early stop cut; random members when 'sampled'); "
         "'rank r' those with that rank; 'pure Hilbert function' those that also pass the staged test; 'tables' the Betti tables "
         "computed by uhlib; 'pure' those whose table is (1, 2, 2, 1) on (0, e, 3e, 4e). A stratum stops once it has 5 pure members "
         "(chunks already started finish and are counted).", "", "## Gates", ""]
    for g in ("G1", "G2", "G3", "G4"):
        r = res["gates"].get(g)
        if r is None:
            L.append("- %s: not run" % g)
        elif r.get("blocked"):
            L.append("- %s: BLOCKED, %s" % (g, r["reason"]))
        elif g == "G1":
            d, c = r.get("direct"), r.get("after_c")
            L.append("- G1: %s (before the families: (a) %d cases, (b) %d cases, (c) %d cases, (d) %d values of e, %s; after family C: %s)" % (
                "PASSED" if r.get("direct", {}).get("passed") and (c or {}).get("passed") else "NOT YET PASSED" if not (c or {}).get(
                    "passed") and d and d["passed"] else "FAILED", len(d["a"]), len(d["b"]), d["c"]["cases"], len(d["d"]),
                "passed" if d["passed"] else "FAILED", "not checked" if c is None else ("passed" if c["passed"] else "FAILED")))
            if c:
                for row in c["rows"]:
                    L.append("    - (%d, %d) %s: expect %s; %s" % (row["pair"][0], row["pair"][1], row["stratum"], row["expect"], (
                        "pure %s" % row["pure"] if "pure" in row else "pure Hilbert function %s of %s examined" % (
                            row["pure_hilbert"], row["examined"])) + (" (ok)" if row["ok"] else " (NOT ok)")))
        elif g == "G2":
            L.append("- G2: %s (%s; %d pure members in the sample, %d with the same pure table from both instruments)" % (
                "PASSED" if r["passed"] else "FAILED", r["singular"], r["sample_members"], r["agree_and_pure_in_I2"]))
        elif g == "G3":
            L.append("- G3: %s (%s)" % ("PASSED" if r["passed"] else "FAILED", r["last_line"]))
        else:
            if r["passed"]:
                L.append("- G4: PASSED (%d strata that are not admissible, %d members examined, %d with the pure Hilbert function)" % (
                    r["strata_not_admissible"], r["members_examined"], r["with_pure_hilbert_function"]))
            else:
                L.append("- G4: FAILED: %s" % r)
    L += ["", "## Table of the pairs", "", "| Family | e | p | Strata stored of planned | Strata with rank r | Strata with pure members | Members "
          "examined | Rank r | Pure Hilbert function | Tables | Pure | Share with the pure Hilbert function in S(2; 0, 1) | Ratio to p^(-h_e(3e)) | "
          "Worker seconds |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for t in T.values():
        s = t["s20"]
        L.append("| %s | %d | %d | %d of %d%s | %d | %d | %s | %s | %s | %d | %d | %s | %s | %.0f |" % (
            t["family"], t["e"], t["p"], t["strata_stored"], t["strata_planned"], "" if t["finished"] else " (not finished)",
            t["strata_with_rank_r"], t["strata_with_pure"], _f(t["members_examined"]), _f(t["rank_r"]), _f(t["pure_hilbert"]), t["tables"],
            t["pure"], _share(s), "-" if not s else "%.3g (p^-%d = %.3g)" % (s["ratio"], t["h_3e"], s["p_power"]), t["worker_seconds"]))
    L += ["", "## Predictions as counts", ""]
    L.append("- P1 (an admissible stratum holds a pure member over GF(p) in each of the five pairs):")
    for k, v in P["P1"].items():
        L.append("    - (%s): %d pure members in %d strata (%d of %d strata stored%s); %d confirmed by Singular; %s" % (
            k, v["pure_members"], v["strata_with_pure"], v["strata_stored"], v["strata_planned"], "" if v["pair_finished"] else ", NOT FINISHED",
            v["confirmed_by_second_instrument"], "holds" if v["holds"] else "does not hold"))
    L.append("- P2 (the share of the pure Hilbert function in S(2; 0, 1) lies between %.1f and %.1f times p^(-h_e(3e)), in the pairs where "
             "it is positive):" % (P2_LOW, P2_HIGH))
    for k, v in P["P2"].items():
        L.append("    - %s: %d of %d examined%s, share %.3g, ratio %.3g; %s" % (
            k, v["pure_hilbert"], v["examined"], " (stopped early)" if v["stopped_early"] else "", v["share"], v["ratio_to_p_power"],
            "holds" if v["holds"] else "does not hold"))
    L.append("- P3 (gate G4): %s" % ("holds" if P["P3"]["holds"] else "does not hold"))
    L.append("- P4 (no member of a stratum with p dividing m has rank mu_3e exactly r; families C and Q):")
    for k, v in P["P4"].items():
        if k[0] in "CQ":
            L.append("    - %s: %d of %d members examined with p dividing m have rank r; %s" % (
                k, v["rank_r_in_strata_with_p_dividing_m"], v["members_examined_there"], "holds" if v["holds"] else "does not hold"))
    L.append("- P5 (e = 8, exploratory):")
    for k, v in P["P5"].items():
        extra = "" if "S(7; 0, 1)" not in v or v["S(7; 0, 1)"] is None else "; S(7; 0, 1): %d pure in %d examined%s" % (
            v["S(7; 0, 1)"]["pure"], v["S(7; 0, 1)"]["examined"], " (all members)" if v["S(7; 0, 1)"]["complete"] else "")
        L.append("    - (%s): %d pure members in %d strata (%d of %d strata stored%s); %d confirmed by Singular%s; %s" % (
            k, v["pure_members"], v["strata_with_pure"], v["strata_stored"], v["strata_planned"], "" if v["pair_finished"] else ", NOT FINISHED",
            v["confirmed_by_second_instrument"], extra, "holds" if v["holds"] else "does not hold"))
    if not P["P5"]:
        L.append("    - family E was not run")
    g2 = {(r["stratum"], r["index"]): r for r in res["gates"].get("G2", {}).get("rows", [])}
    for fam in X.FAMILIES:
        pairs = [t for t in T.values() if t["family"] == fam]
        if not pairs:
            continue
        L += ["", "## " + FAMILY_TITLE[fam], ""]
        for t in pairs:
            e, p = t["e"], t["p"]
            L += ["", "### (e, p) = (%d, %d)" % (e, p), "",
                  "r = %d; h_e(3e) = %d; p^(-h_e(3e)) = %.3g. Strata stored: %d of %d%s." % (
                      t["r"], t["h_3e"], p ** -t["h_3e"], t["strata_stored"], t["strata_planned"],
                      "" if t["finished"] else " (the pair did not finish: " + ("%d strata were cut by the time budget" % len(
                          t["strata_cut"]) if t["strata_cut"] else "strata not run") + ")"),
                  "Rows: the strata that have members of rank r or are admissible (the other strata of the pair, %d, have no member of "
                  "rank r and are not admissible)." % sum(1 for s in _strata_of(res, fam, e, p) if not s["rank_r"] and not s["admissible"]), "",
                  "| m | (i, j) | Admissible | d_i | d_j | N | Examined | Rank r | Pure Hilbert function | Tables | Pure | Stop | "
                  "Distribution of rank mu_3e |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
            shown = []
            for s in _strata_of(res, fam, e, p):
                if not (s["rank_r"] or s["admissible"]):
                    continue
                shown.append(s)
                mode = ("sampled" if not s["enumerated"] else "all" if s["N"] is not None and s["examined"] >= s["N"]
                        else "in order, stopped early")
                stop = "early stop" if s["stopped_early"] else ("cut: " + s["stopped_by"] if s["stopped_by"] else (
                    "tables cap" if s["tables_cap_reached"] else "budget done" if s["complete"] else "partial"))
                L.append("| %d | (%d, %d) | %s | %d | %d | %s | %s %s of %s | %s | %s | %d | %d | %s | %s |" % (
                    s["m"], s["i"], s["j"], "yes" if s["admissible"] else "no", s["d_i"], s["d_j"], _f(s["N"]), _f(s["examined"]), mode,
                    _f(s["planned"]), _f(s["rank_r"]), _f(s["pure_hilbert"]), s["tables"], s["pure"], stop, _hist(s["rank_hist"])))
            printed = False
            for s in shown:
                pure = [m for m in s["members"] if m["pure"]][:3]
                if not pure:
                    continue
                if not printed:
                    L += ["", "Pure members (PBW monomials x^a y^b z^c, y x = x y - z; coefficients as symmetric residues modulo p; the Betti "
                          "table of uhlib and, where G2 covers the member, of Singular):", ""]
                    printed = True
                key = "%s|%d|%d|%d|%d|%d" % (fam, e, p, s["m"], s["i"], s["j"])
                for m in pure:
                    r2 = g2.get((key, m["index"]))
                    L.append("- S(%d; %d, %d), member %d: f = %s ; g = %s ; uhlib: %s ; Singular: %s" % (
                        s["m"], s["i"], s["j"], m["index"], X.poly_text(e, p, m["f"]), X.poly_text(e, p, m["g"]), _rows(m["betti"]),
                        "not run on this member" if not r2 else (_rows(r2["betti_I2"]) if "betti_I2" in r2 else "error: %s" % r2.get("error"))))
            if not printed:
                L += ["", "No stratum of this pair has a member with the pure Betti table among the members examined."]
            others = [s for s in shown if s["pure_hilbert"] and s["nonpure_tables"]]
            for s in others:
                L.append("- S(%d; %d, %d): members with the pure Hilbert function and another Betti table: %s" % (
                    s["m"], s["i"], s["j"], "; ".join("%s x %d" % (k, v) for k, v in s["nonpure_tables"].items())))
    L += ["", "Time of the commands: " + ", ".join("%s%s %.0f s" % (r["command"], " " + r["family"] if r.get("family") else "", r["seconds"])
                                                      for r in res["runs"]) + "; total %.0f s." % res.get("wall_seconds_total", 0), ""]
    Path(path).write_text("\n".join(L), encoding="utf-8", newline="\n")
