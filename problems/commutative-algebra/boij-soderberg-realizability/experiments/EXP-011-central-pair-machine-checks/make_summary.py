"""EXP-011: results-summary.md generated from artifacts/results.json (every entry comes from the file; nothing is typed by hand)."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "artifacts" / "results.json"
SUMMARY = HERE / "results-summary.md"


def table_str(rows, e=None):
    if rows is None:
        return "-"
    pure = e is not None and [[0, 0, 1], [1, e, 2], [2, 3 * e, 2], [3, 4 * e, 1]] == [list(r) for r in rows]
    body = "; ".join("b%d,%d=%d" % (i, j, r) for i, j, r in rows)
    return body + (" (pure)" if pure else "")


def instrument_cell(b, e):
    if b.get("table") is not None:
        return table_str(b["table"], e) + " [%ss]" % b.get("seconds")
    status = b.get("status", "")
    if b.get("error"):
        status += ": " + b["error"]
    return status or "-"


def row(r):
    ident = r["identities"]
    ok = "all hold" if ident["all"] else "FAILED: " + ", ".join(k for k, v in ident.items() if v is False and k != "all")
    hf = "equals h_e" if r["hilbert_equals_h_e"] else "differs from h_e"
    if not r["finite_length"]:
        hf += "; dims %s" % r["dims_found"]
    length = "%s (e^3 = %d)" % (r["length"], r["e"] ** 3) if r["finite_length"] else "not finite within degree %d" % (
        len(r["hilbert"]) - 1)
    lam = "%s" % r["lambda"] if r["lambda"] is not None else "not a multiple of z^e"
    return "| %s | %s | (%d, %d) | `%s` ; `%s` | %s | %s | %s | %s | %s | %s | %s |" % (
        r["id"], r["family"], r["e"], r["p"], r["f_text"], r["g_text"], lam, ok, hf, length,
        instrument_cell(r["betti_uhlib"], r["e"]), instrument_cell(r["betti_singular"], r["e"]), "%.1f s" % r["seconds"])


HEADER = ("| Case | Family | (e, p) | f ; g | lambda | Identities | Hilbert function | Length | Betti (uhlib) | Betti (Singular) "
          "| Time (identities, Hilbert, uhlib Betti) |\n|---|---|---|---|---|---|---|---|---|---|---|")


def ordered(res):
    return sorted(res["cases"].values(), key=lambda r: ("TGN".index(r["family"]), int(r["id"][1:])))


def table_text(res):
    return HEADER + "\n" + "\n".join(row(r) for r in ordered(res))


def write_summary(res):
    out = ["# EXP-011 results summary (generated from artifacts/results.json by make_summary.py)", "",
           "Outcomes only: no statement about realizability or about the theorem. Betti entries b(i,j) = rank of the free module "
           "of homological degree i in degree j; pure means (1, 2, 2, 1) on (0, e, 3e, 4e).", "",
           "## Gates and predictions", ""]
    for k in ("G1", "G2", "G3"):
        gv = res["gates"].get(k)
        out.append("- %s: %s" % (k, "not run" if gv is None else ("passed" if gv["passed"] else "FAILED or incomplete")
                                  + " " + json.dumps({a: b for a, b in gv.items() if a != "cases"})))
    for k in ("P1", "P2"):
        pv = res["predictions"].get(k)
        out.append("- %s: %s" % (k, "not evaluated" if pv is None else json.dumps(pv)))
    out += ["", "## Cases", "", table_text(res), "",
            "Replacements of a non-coprime pair (G1, G3): " + (json.dumps({r["id"]: r["replacement"] for r in res["cases"].values()
                                                                          if r.get("replacement")}) or "none"), ""]
    SUMMARY.write_text("\n".join(out), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    write_summary(json.loads(RESULTS.read_text(encoding="utf-8")))
    print("wrote", SUMMARY, file=sys.stderr)
