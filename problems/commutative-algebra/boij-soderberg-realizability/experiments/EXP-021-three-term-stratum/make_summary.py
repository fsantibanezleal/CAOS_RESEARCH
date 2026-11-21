"""EXP-021: totals per case, the predictions P1 to P5 as counts, and results-summary.md, all computed from artifacts/results.json.

Every number of results-summary.md is computed from the stored cases, none is typed.  Counts and members only: no statement about
realizability is made here (the coordinating session draws the conclusions).  A case that is not started or not finished is shown as such
and the predictions that need it are 'not decided'.
"""
from pathlib import Path

SHOWN = 3  # pure members printed per case
P2_LOW, P2_HIGH = 200, 4000
P5_LOW, P5_HIGH = 0.1, 0.6


def _case(res, c):
    """The stored record of a case (finished), its view while not finished, or None."""
    return res["cases"].get(c["key"]) or res.get("cases_partial", {}).get(c["key"])


def compute_totals(res):
    out = {}
    for c in res["plan"]:
        s = _case(res, c)
        base = {"key": c["key"], "family": c["family"], "e": c["e"], "p": c["p"], "mode": c["mode"], "members": c["members"],
                "total_list": c["total"], "blocks": c["blocks"]}
        if s is None:
            out[c["key"]] = dict(base, status="not started", done=0, blocks_done=0, stages=[0] * 4, found_total=0, tables=0, pure=0,
                                 pure_delta0=0, pure_gamma_delta0=0, stage3_delta0=0, stage3_gamma_delta0=0, wall_seconds=0.0,
                                 worker_seconds=0.0, ms_per_member_per_worker=None, members_per_second=None)
            continue
        out[c["key"]] = dict(base, status=s["status"], done=s["done"], blocks_done=s["blocks"][1], stages=s["stages"],
                             found_total=s["found_total"], tables=s["tables"], pure=s["pure"], pure_delta0=s["pure_delta0"],
                             pure_gamma_delta0=s["pure_gamma_delta0"], stage3_delta0=s["stage3_delta0"],
                             stage3_gamma_delta0=s["stage3_gamma_delta0"], wall_seconds=s["wall_seconds"],
                             worker_seconds=s["worker_seconds"], ms_per_member_per_worker=s["ms_per_member_per_worker"],
                             members_per_second=int(s["done"] / max(s["wall_seconds"], 1e-9)))
    return out


def family_seconds(res):
    out = {}
    for r in res["runs"]:
        if r["command"] == "cases":
            out[r["family"]] = round(out.get(r["family"], 0.0) + r["seconds"], 1)
    return out


def _g2_rows(res, key):
    return [r for r in res["gates"].get("G2", {}).get("rows", []) if r["case"] == key]


def _tabled(s):
    return [m for m in s["members_stage3"] if "pure" in m]


def _covered(s, limit):
    """True when every member of stage 3 with index below `limit` was tabled (and the list was counted up to `limit`)."""
    if s["done"] < limit:
        return False
    below = [m for m in s["members_stage3"] if m["index"] < limit]
    return all("pure" in m for m in below)


def predictions(res):
    tot = compute_totals(res)
    x = next((t for t in tot.values() if t["family"] == "X"), None)
    out = {}
    if x is None or x["status"] == "not started":
        for k in ("P1", "P2", "P3", "P4", "P5"):
            out[k] = {"outcome": "not decided", "why": "family X not started"}
        return out
    s = _case(res, {"key": x["key"]})
    complete = s["status"] == "complete"
    p, e = x["p"], x["e"]
    pure = [m for m in _tabled(s) if m["pure"]]
    conf = [r for r in _g2_rows(res, x["key"]) if r.get("agree") and r.get("pure_I2")]
    # P1
    if pure and conf:
        o1 = {"outcome": "holds", "why": "%d pure members, %d confirmed by both instruments" % (s["pure"], len(conf))}
    elif pure:
        o1 = {"outcome": "not decided", "why": "%d pure members found by the first instrument; second instrument not confirming (G2 %s)" % (
            s["pure"], "run" if res["gates"].get("G2") else "not run")}
    elif complete:
        o1 = {"outcome": "does not hold", "why": "complete list, %d members of stage 3, %d tables, no pure member" % (s["found_total"], s["tables"])}
    else:
        o1 = {"outcome": "not decided", "why": "case %s" % s["status"]}
    out["P1"] = dict(statement="a pure pair at (11, 3), confirmed by both instruments", **o1, pure=s["pure"], confirmed=len(conf))
    # P2
    if s["blocks"][1] < s["blocks"][0]:
        o2 = {"outcome": "not decided", "why": "%d of %d blocks counted" % (s["blocks"][1], s["blocks"][0])}
    else:
        o2 = {"outcome": "holds" if P2_LOW <= s["found_total"] <= P2_HIGH else "does not hold", "why": "%d members of stage 3" % s["found_total"]}
    out["P2"] = dict(statement="the number of members of stage 3 is between %d and %d" % (P2_LOW, P2_HIGH), **o2, count=s["found_total"])
    # P3 and P4
    for key, limit, name, st3 in (("P3", p ** (e + 3), "delta = 0", s["stage3_delta0"]), ("P4", p ** (e + 1), "gamma = delta = 0",
                                                                                      s["stage3_gamma_delta0"])):
        below = [m for m in pure if m["index"] < limit]
        cov = _covered(s, limit)
        if key == "P3":
            if below:
                o = {"outcome": "holds", "why": "%d pure members with %s (first index %d)" % (len(below), name, below[0]["index"])}
            elif cov:
                o = {"outcome": "does not hold", "why": "all %d members of stage 3 with %s tabled, none pure" % (st3, name)}
            else:
                o = {"outcome": "not decided", "why": "no pure member with %s yet; the tables do not cover its %s members of stage 3" % (name, st3)}
            stmt = "the members with delta = 0 (index below %d) hold a pure pair" % limit
        else:
            if below:
                o = {"outcome": "does not hold", "why": "%d pure members with %s (first index %d)" % (len(below), name, below[0]["index"])}
            elif cov:
                o = {"outcome": "holds", "why": "all %d members of stage 3 with %s tabled, none pure" % (st3, name)}
            else:
                o = {"outcome": "not decided", "why": "no pure member with %s yet; the tables do not cover its %s members of stage 3" % (name, st3)}
            stmt = "no pure pair among the members with gamma = delta = 0 (index below %d)" % limit
        out[key] = dict(statement=stmt, **o, stage3=st3, pure=len(below))
    # P5
    if s["tables"] == 0:
        o5 = {"outcome": "not decided", "why": "no table computed"}
    else:
        share = s["pure"] / s["tables"]
        in_band = P5_LOW <= share <= P5_HIGH
        o5 = {"outcome": ("holds" if in_band else "does not hold") if s["pure"] else "not decided (given P1)",
              "why": "%d of %d tables are pure (%.3f)" % (s["pure"], s["tables"], share)}
    out["P5"] = dict(statement="of the Betti tables computed, between one tenth and six tenths are pure (given P1)", **o5, tables=s["tables"],
                     pure=s["pure"])
    return out


# ------------------------------------------------------------------ text
def _table_text(rows):
    return " ".join("(%d,%d):%d" % tuple(r) for r in rows) if rows else "none"


def totals_text(tot):
    lines = ["| Case | Members done / planned | Stages 0, 1, 2, 3 | Stage 3 | Tables | Pure | Status |", "|---|---|---|---|---|---|---|"]
    for t in tot.values():
        lines.append("| (%d, %d) %s | %s / %s | %s | %s | %s | %s | %s |" % (
            t["e"], t["p"], t["mode"], "{:,}".format(t["done"]), "{:,}".format(t["members"]), "; ".join("{:,}".format(v) for v in t["stages"]),
            "{:,}".format(t["found_total"]), t["tables"], t["pure"], t["status"]))
    return "\n".join(lines)


def write_summary(res, path):
    tot = res["totals"]
    L = ["# EXP-021 results summary (generated from artifacts/results.json by make_summary.py; do not edit)", "",
         "Counts and members only. No statement about realizability is made here.", ""]
    L += ["## Gates", ""]
    g = res["gates"]
    L.append("- G3 (unit tests): %s (%s)" % ("passed" if g.get("G3", {}).get("passed") else "not passed", g.get("G3", {}).get("last_line", "")))
    g1 = g.get("G1")
    L.append("- G1 (controls): %s" % ("not run" if g1 is None else "passed" if g1["passed"] else "FAILED"))
    g2 = g.get("G2")
    if g2 is None:
        L.append("- G2 (second instrument): not run")
    elif g2.get("blocked"):
        L.append("- G2 (second instrument): BLOCKED, %s" % g2["reason"])
    else:
        L.append("- G2 (second instrument, %s): %s; %d members, %d agree and are pure in both instruments; errors %s; failing %s" % (
            g2["singular"], "passed" if g2["passed"] else "not passed", g2["sample_members"], g2["agree_and_pure_in_I2"],
            g2["singular_errors"] or "none", g2["failing_cases"] or "none"))
    L.append("")
    if g1:
        L += ["### G1, every control count against the hypothesis", "", "| Case | Item | Got | Hypothesis | Equal |", "|---|---|---|---|---|"]
        for r in g1["rows"]:
            if r.get("missing"):
                L.append("| %s | missing | | | no |" % r["case"])
                continue
            for k, v in r["got"].items():
                L.append("| %s | %s | %s | %s | %s |" % (r["case"], k, v, r["want"].get(k, ""), "yes" if r["equal"].get(k, True) else "NO"))
        L.append("")
    L += ["## Cases", "", totals_text(tot), ""]
    for key, t in tot.items():
        s = res["cases"].get(key) or res.get("cases_partial", {}).get(key)
        L += ["### Case %s: (e, p) = (%d, %d), %s" % (key, t["e"], t["p"], t["mode"]), ""]
        if s is None:
            L += ["Not started.", ""]
            continue
        L.append("- Members done: %s of %s planned (list of %s); blocks %d of %d of %d members; status %s." % (
            "{:,}".format(s["done"]), "{:,}".format(s["members"]), "{:,}".format(s["total_list"]), s["blocks"][1], s["blocks"][0],
            s["block_size"], s["status"]))
        L.append("- Syzygy classes (s1, s2) = %s, block order %s." % (tuple(s["syzygy_classes"]), s["block_order"]))
        L.append("- Counts by stage 0, 1, 2, 3: %s." % ", ".join("{:,}".format(v) for v in s["stages"]))
        if s["mode"] == "complete":
            L.append("- Members with delta = 0 (index below %d), stages 0 to 3: %s; with gamma = delta = 0 (index below %d): %s." % (
                s["p"] ** (s["e"] + 3), s["stages_delta0"], s["p"] ** (s["e"] + 1), s["stages_gamma_delta0"]))
        if s["plain"]:
            L.append("- Members with the pure Hilbert function by the plain staged test (no pattern): %d." % s["plain"])
        L.append("- Members of stage 3: %d (%d kept with their data%s)." % (s["found_total"], s["found_kept"],
                                                                         "" if s["found_kept_all"] else ", the first in index order"))
        L.append("- Betti tables computed: %d (rule: %s%s); pure: %d; pure with delta = 0: %d; with gamma = delta = 0: %d." % (
            s["tables"], s["table_rule"], ", extended to every member of stage 3" if s["tables_extended"] else "", s["pure"],
            s["pure_delta0"], s["pure_gamma_delta0"]))
        if s["nonpure_tables"]:
            top = sorted(s["nonpure_tables"].items(), key=lambda kv: (-kv[1], kv[0]))[:3]
            L.append("- Tables that are not pure: %d members in %d distinct tables; the most frequent: %s." % (
                sum(s["nonpure_tables"].values()), len(s["nonpure_tables"]), "; ".join("%s x %d" % (k, v) for k, v in top)))
        L.append("- First pure indices: %s." % (s["pure_indices"][:8] or "none"))
        L.append("- Throughput: %s ms per member per worker (counting only); %s members per second of wall time (with the tables); "
                 "%.1f s of workers, %.1f s of wall time; block seconds min and max %s." % (
                     s["ms_per_member_per_worker"], t["members_per_second"], s["worker_seconds"], s["wall_seconds"],
                     s["blocks_seconds_min_max"]))
        pures = [m for m in s["members_stage3"] if m.get("pure")][:SHOWN]
        for m in pures:
            row = next((r for r in res["gates"].get("G2", {}).get("rows", []) if r["case"] == key and r["index"] == m["index"]), None)
            L += ["", "Pure member, index %d, digits %s:" % (m["index"], m["digits"]), "", "    f = %s" % m["f_text"], "    g = %s" % m["g_text"], "",
                  "Betti table by uhlib (degree-wise rank): %s; length %s." % (_table_text(m["betti"]), m["length"])]
            if row and row.get("betti_I2"):
                L.append("Betti table by Singular: %s; agree: %s." % (_table_text(row["betti_I2"]), row.get("agree")))
            elif row:
                L.append("Singular: no table (%s); checked by one instrument only." % row.get("error"))
            else:
                L.append("Singular: not run on this member.")
        L.append("")
    nm = res.get("nonmonic")
    if nm:
        L += ["### Non-monic members at (5, 3)", "",
              "Of the %s normalized members of S(2; 0, 1), %s have both leading coefficients nonzero and %s do not; stages of the latter 0 to 3: "
              "%s; with the pure Hilbert function by the plain staged test: %s." % (
                  "{:,}".format(nm["members"]), "{:,}".format(nm["monic_seen"]), "{:,}".format(nm["non_monic"]), nm["stages"], nm["plain"]), ""]
    L += ["## Predictions", ""]
    for k, v in res["predictions"].items():
        L.append("- %s (%s): %s, %s." % (k, v.get("statement", ""), v["outcome"], v["why"]))
    L += ["", "## Time", ""]
    L.append("- Wall time by family: %s; total %s s." % (res["wall_seconds_by_family"], res["wall_seconds_total"]))
    L.append("")
    Path(path).write_text("\n".join(L), encoding="utf-8", newline="\n")
