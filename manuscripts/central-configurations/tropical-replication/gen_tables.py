#!/usr/bin/env python3
"""Regenerate the tables and figure data of main.tex from the experiment artifacts.

Every number in the generated regions of main.tex is read from a stored artifact:

  EXP-004 artifacts/screening-table.txt   f-vectors and gfan wall times (fast path)
  EXP-004 artifacts/hashes.txt            SHA-256 of the gfan inputs and outputs
  EXP-007 artifacts/summary.json          comets, pointed, unpointed, decider seconds
  EXP-008 artifacts/out-n4-*.out          the twelve gfan outputs of the enrichment grid
  EXP-008 artifacts/table.json            gfan wall times of the eight cells it records

The twelve cells of the enrichment grid are decided again from the stored gfan outputs
with the same comet extraction (EXP-004 comet_analysis.py) and the same exact decider
(code/cclib/exact_lp.py); no gfan run is started. The eight cells in table.json are
compared with the recomputed values and the script stops on any difference.

Usage:
    python gen_tables.py            rewrite the generated regions of main.tex
    python gen_tables.py --check    exit 1 when main.tex differs from the regeneration
"""
import argparse
import glob
import importlib.util
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROB = HERE.parents[2] / "problems" / "dynamical-systems" / "central-configurations"
EXPS = PROB / "experiments"
TEX = HERE / "main.tex"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


LP = load("exact_lp", PROB / "code" / "cclib" / "exact_lp.py")
CA = load("comet_analysis", next(iter(glob.glob(str(EXPS / "EXP-004*" / "comet_analysis.py")))))

E4 = next(iter(glob.glob(str(EXPS / "EXP-004*"))))
E7 = next(iter(glob.glob(str(EXPS / "EXP-007*"))))
E8 = next(iter(glob.glob(str(EXPS / "EXP-008*"))))

VAL_N5 = {
    "V1pow3": ("$(1,3,9,27,81)$", "powers of 3"),
    "V2squares": ("$(1,4,9,16,25)$", "squares"),
    "V3pow2": ("$(1,2,4,8,16)$", "powers of 2"),
    "V4primes": ("$(2,3,5,7,11)$", "primes"),
    "V5arith": ("$(0,1,2,3,4)$", "arithmetic"),
    "V6repeat": ("$(1,1,9,27,81)$", "repeated"),
}
VAL_N4 = {
    "pow3": ("$(1,3,9,27)$", "powers of 3"),
    "pow2": ("$(1,2,4,8)$", "powers of 2"),
    "arith": ("$(0,1,2,3)$", "arithmetic"),
    "equal": ("$(0,0,0,0)$", "equal"),
}


def parse_screening():
    rows = {}
    for line in (Path(E4) / "artifacts" / "screening-table.txt").read_text().splitlines():
        parts = [p.strip() for p in line.split("|")]
        label = parts[0]
        fvec = parts[1].split(":", 1)[1].split()
        secs = int(parts[-1].rstrip("s"))
        rows[label] = {"fvec": fvec, "secs": secs}
    return rows


def parse_hashes():
    out = {}
    for line in (Path(E4) / "artifacts" / "hashes.txt").read_text().splitlines():
        h, name = line.split()
        out[name] = h
    return out


def decide_file(path):
    rays, cones = CA.parse_sections(str(path))
    comps = CA.components(rays, cones)
    pointed = unpointed = 0
    for comp in comps:
        gens = [[Fraction(x) for x in rays[i][1:]] for i in comp if rays[i][0] == 0]
        if not gens:
            pointed += 1
            continue
        if LP.decide_pointed(gens).pointed:
            pointed += 1
        else:
            unpointed += 1
    lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()
    fvec = next(lines[i + 1].split() for i, ln in enumerate(lines)
                if ln.strip() == "F_VECTOR")
    return fvec, len(comps), pointed, unpointed


def enrichment_grid():
    stored = json.loads((Path(E8) / "artifacts" / "table.json").read_text())
    rows = []
    for vkey in ("equal", "pow2", "arith"):
        for sysname in ("A1", "A2", "A3", "A4"):
            label = f"n4-{sysname}-{vkey}"
            fvec, ncom, npt, nun = decide_file(Path(E8) / "artifacts" / f"out-{label}.out")
            secs = None
            if label in stored:
                st = stored[label]
                assert st["f_vector"].split() == fvec, label
                assert (st["comets"], st["pointed"], st["unpointed"]) == (ncom, npt, nun), label
                secs = st["seconds"]
            rows.append((vkey, sysname, fvec, ncom, npt, nun, secs))
    return rows


def table_n5(scr, summ):
    out = []
    out.append(r"\begin{tabular}{@{}llrrrrr@{}}")
    out.append(r"\toprule")
    out.append(r"System & Valuations & comets & pointed & unpointed & gfan (s) & decider (s) \\")
    out.append(r"\midrule")
    for sysname in ("S1", "S2"):
        for key, (vals, name) in VAL_N5.items():
            label = f"n5-{sysname}-{key}"
            s = summ[f"out-{label}.out"]
            out.append(
                f"{sysname} & {vals} {name} & {s['comets']} & {s['pointed']} & {s['unpointed']} "
                f"& {scr[label]['secs']} & {s['seconds']:.1f} \\\\")
        if sysname == "S1":
            out.append(r"\midrule")
    out.append(r"\bottomrule")
    out.append(r"\end{tabular}")
    return "\n".join(out)


def table_f5(scr):
    out = []
    out.append(r"\begin{tabular}{@{}lll@{}}")
    out.append(r"\toprule")
    out.append(r"System & Valuations & $f$-vector \\")
    out.append(r"\midrule")
    for sysname in ("S1", "S2"):
        for key, (vals, name) in VAL_N5.items():
            fv = scr[f"n5-{sysname}-{key}"]["fvec"]
            out.append(f"{sysname} & {vals} {name} & " + r"\texttt{" + " ".join(fv) + r"} \\")
        if sysname == "S1":
            out.append(r"\midrule")
    out.append(r"\bottomrule")
    out.append(r"\end{tabular}")
    return "\n".join(out)


def table_n4(scr, summ):
    out = []
    out.append(r"\begin{tabular}{@{}lrrrrrl@{}}")
    out.append(r"\toprule")
    out.append(r"Valuations & comets & pointed & unpointed & gfan (s) & decider (s) & $f$-vector \\")
    out.append(r"\midrule")
    for key, (vals, name) in VAL_N4.items():
        label = f"n4-S1-{key}"
        s = summ[f"out-{label}.out"]
        fv = scr[label]["fvec"]
        out.append(
            f"{vals} {name} & {s['comets']} & {s['pointed']} & {s['unpointed']} & "
            f"{scr[label]['secs']} & {s['seconds']:.1f} & "
            r"\texttt{" + " ".join(fv) + r"} \\")
    out.append(r"\bottomrule")
    out.append(r"\end{tabular}")
    return "\n".join(out)


def table_enrich(rows):
    names = {"equal": "$(0,0,0,0)$ equal", "pow2": "$(1,2,4,8)$ powers of 2",
             "arith": "$(0,1,2,3)$ arithmetic"}
    adds = {"A1": "baseline", "A2": "$+\\,e_{IU}$", "A3": "$+$ Dziobek",
            "A4": "$+$ both"}
    out = []
    out.append(r"\begin{tabular}{@{}llrrrrl@{}}")
    out.append(r"\toprule")
    out.append(r"Valuations & System & comets & pointed & unpointed & gfan (s) & $f$-vector \\")
    out.append(r"\midrule")
    prev = None
    for vkey, sysname, fvec, ncom, npt, nun, secs in rows:
        if prev is not None and vkey != prev:
            out.append(r"\midrule")
        prev = vkey
        t = "--" if secs is None else f"{secs:.1f}"
        out.append(f"{names[vkey]} & {sysname}, {adds[sysname]} & {ncom} & {npt} & {nun} & {t} & "
                   r"\texttt{" + " ".join(fvec) + r"} \\")
    out.append(r"\bottomrule")
    out.append(r"\end{tabular}")
    return "\n".join(out)


def table_hashes(hashes):
    out = []
    out.append(r"\begin{tabular}{@{}lll@{}}")
    out.append(r"\toprule")
    out.append(r"Cell (system S1, $n=5$) & gfan input, SHA-256 prefix & gfan output, SHA-256 prefix \\")
    out.append(r"\midrule")
    for key, (_, name) in VAL_N5.items():
        i = hashes[f"in-n5-S1-{key}.txt"][:16]
        o = hashes[f"out-n5-S1-{key}.out"][:16]
        out.append(f"{name} & \\texttt{{{i}}} & \\texttt{{{o}}} \\\\")
    out.append(r"\bottomrule")
    out.append(r"\end{tabular}")
    return "\n".join(out)


def fig_fvec(scr):
    """pgfplots data: f-vector profiles of the six S1 cells at n = 5 (log scale)."""
    lines = []
    for key, (_, name) in VAL_N5.items():
        coords = " ".join(f"({i},{v})" for i, v in enumerate(scr[f"n5-S1-{key}"]["fvec"]))
        lines.append(f"\\addplot coordinates {{{coords}}};")
        lines.append(f"\\addlegendentry{{{name}}}")
    return "\n".join(lines)


def fig_comets(summ):
    """pgfplots data: comet counts of S1 and S2 at n = 5, one point per valuation family."""
    keys = list(VAL_N5)
    names = ",".join(VAL_N5[k][1] for k in keys)
    s1 = " ".join(f"({VAL_N5[k][1]},{summ[f'out-n5-S1-{k}.out']['comets']})" for k in keys)
    s2 = " ".join(f"({VAL_N5[k][1]},{summ[f'out-n5-S2-{k}.out']['comets']})" for k in keys)
    return names, s1, s2


def fig_enrich(rows):
    series = {}
    for vkey, sysname, fvec, ncom, npt, nun, secs in rows:
        series.setdefault(vkey, []).append((sysname, ncom))
    lines = []
    legend = {"equal": "equal", "pow2": "powers of 2", "arith": "arithmetic"}
    for vkey in ("equal", "pow2", "arith"):
        coords = " ".join(f"({s},{c})" for s, c in series[vkey])
        lines.append(f"\\addplot coordinates {{{coords}}};")
        lines.append(f"\\addlegendentry{{{legend[vkey]}}}")
    return "\n".join(lines)


def build_regions():
    scr = parse_screening()
    summ = json.loads((Path(E7) / "artifacts" / "summary.json").read_text())
    hashes = parse_hashes()
    rows = enrichment_grid()
    names, s1, s2 = fig_comets(summ)
    return {
        "table-n5": table_n5(scr, summ),
        "table-f5": table_f5(scr),
        "table-n4": table_n4(scr, summ),
        "table-enrich": table_enrich(rows),
        "table-hashes": table_hashes(hashes),
        "fig-fvec": fig_fvec(scr),
        "fig-comets-names": names,
        "fig-comets-s1": s1,
        "fig-comets-s2": s2,
        "fig-enrich": fig_enrich(rows),
    }


def apply(text, regions):
    for name, body in regions.items():
        pat = re.compile(
            rf"(% BEGIN GENERATED {re.escape(name)}\n).*?(\n% END GENERATED {re.escape(name)})",
            re.S)
        if not pat.search(text):
            sys.exit(f"missing marker pair for {name}")
        text = pat.sub(lambda m: m.group(1) + body + m.group(2), text)
    return text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    old = TEX.read_text(encoding="utf-8")
    new = apply(old, build_regions())
    if args.check:
        if new != old:
            print("main.tex differs from the regeneration")
            return 1
        print("main.tex matches the artifacts")
        return 0
    TEX.write_text(new, encoding="utf-8", newline="\n")
    print("regions rewritten:", ", ".join(build_regions()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
