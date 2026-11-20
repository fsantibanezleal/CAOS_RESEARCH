"""EXP-013: results-summary.md generated from artifacts/results.json (every entry comes from the file; nothing is typed by hand)."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "artifacts" / "results.json"
SUMMARY = HERE / "results-summary.md"
ORDER = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "T1", "T2", "T3", "N1", "N2"]


def table_str(rows):
    if rows is None:
        return "-"
    return "; ".join("b%d,%d=%d" % (i, j, r) for i, j, r in rows)


def instrument(b):
    """One cell: the table, the length and the time of one instrument on one module."""
    if b is None or b.get("status") == "not attempted":
        return "not run"
    if b.get("table") is None:
        why = b.get("error") or b.get("status", "")
        extra = " (dimensions found: %s)" % b["dims"] if b.get("dims") else ""
        return "no table: %s%s [%ss]" % (why, extra, b.get("seconds"))
    return "%s; length %s [%ss]" % (table_str(b["table"]), b.get("length"), b.get("seconds"))


def comp(c):
    if c is None:
        return "not run"
    return "table %s, length %s" % (
        {True: "is the scaled table", False: "is NOT the scaled table", None: "not decided"}[c["table_is_scaled_table"]],
        {True: "is d^3 times", False: "is NOT d^3 times", None: "not decided"}[c["length_is_d3_times"]])


def poly_block(texts):
    return " ; ".join("`%s`" % t for t in texts)


def ordered(res):
    return [res["cases"][c] for c in ORDER if c in res["cases"]]


def table_text(res):
    head = ("| Case | p | d | Module | Table of M' (uhlib) | Table of M' (Singular) | Scaled table of M' | "
            "Table of phi^*M' (uhlib) | Table of phi^*M' (Singular) | Comparison (uhlib) | Comparison (Singular) | Time |\n"
            "|---|---|---|---|---|---|---|---|---|---|---|---|")
    rows = []
    for r in ordered(res):
        rows.append("| %s | %d | %d | %s | %s | %s | %s | %s | %s | %s | %s | %.1f s |" % (
            r["id"], r["p"], r["d"], r["module_text"], instrument(r["uhlib_base"]), instrument(r["singular_base"]),
            table_str(r["scaled_table_base"]), instrument(r["uhlib_phi"]), instrument(r["singular_phi"]),
            comp(r["compare_uhlib"]), comp(r.get("compare_singular")), r["seconds"]))
    return head + "\n" + "\n".join(rows)


def write_summary(res):
    out = ["# EXP-013 results summary (generated from artifacts/results.json by make_summary.py)", "",
           "Outcomes only: no statement about realizability or about the theorem. Betti entries b(i,j) = rank of the free module "
           "of homological degree i in degree j. d is the degree of the endomorphism; the scaled table sends b(i, j) to b(i, d j).",
           "", "## Gates and predictions", ""]
    for k in ("G1", "G2", "G3"):
        gv = res["gates"].get(k)
        out.append("- %s: %s" % (k, "not run" if gv is None else ("passed" if gv["passed"] else "FAILED or incomplete")
                                  + " " + json.dumps({a: b for a, b in gv.items() if a not in ("cases",)})))
    for k in ("P1", "P2"):
        pv = res["predictions"].get(k)
        out.append("- %s: %s" % (k, "not evaluated" if pv is None else json.dumps(pv)))
    out += ["", "## Cases", "", table_text(res), "", "## Per case: endomorphism and generators", ""]
    for r in ordered(res):
        out += ["### %s (%s)" % (r["id"], r["what"]), "",
                "- phi(x) = `%s`; phi(y) = `%s`; phi(z) = `%s` (computed as phi(x) phi(y) - phi(y) phi(x))" % (
                    r["phi_x_text"], r["phi_y_text"], r["phi_z_text"]),
                "- generators of the ideal of M' (PBW): %s" % poly_block(r["gens_base_text"]),
                "- generators of the ideal of phi^*M' (the images of those generators): %s" % poly_block(r["gens_phi_text"]),
                "- expected length of phi^*M' by the hypothesis (d^3 times the length of M'): %s" % r.get("expected_length_phi"), ""]
    SUMMARY.write_text("\n".join(out), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    write_summary(json.loads(RESULTS.read_text(encoding="utf-8")))
    print("wrote", SUMMARY, file=sys.stderr)
