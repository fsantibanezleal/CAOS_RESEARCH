#!/usr/bin/env python3
"""Regenerate the tables and figure data of main.tex from the experiment artifacts.

Every number in the generated regions of main.tex is read from a stored artifact:

  EXP-004 artifacts/screening-table.txt   f-vectors and gfan wall times (fast path)
  EXP-004 artifacts/hashes.txt            SHA-256 of the gfan inputs and outputs
  EXP-007 artifacts/summary.json          comets, pointed, unpointed, decider seconds
  EXP-008 artifacts/out-n4-*.out          the twelve gfan outputs of the enrichment grid
  EXP-008 artifacts/table.json            gfan wall times of the eight cells it records
  EXP-007 artifacts/*unpointed-certificates.json   generators of each unpointed comet
  EXP-004 artifacts/sys-n*-S*.txt         the polynomial systems (counted)
  EXP-012 artifacts/times.json            Singular job times of the partial Groebner spike
  EXP-020 artifacts/residual-count.json   residual sign assignments per orientation chamber
  EXP-021 artifacts/integrated-summary.json and EXP-022 artifacts/*-summary.json
                                          box outcomes of the covering runs that closed with zero failures

The script exits nonzero when any of these records is missing or violates an invariant it checks
(see the asserts in the figure and macro builders).

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
E12 = next(iter(glob.glob(str(EXPS / "EXP-012*"))))
E20 = next(iter(glob.glob(str(EXPS / "EXP-020*"))))
E21 = next(iter(glob.glob(str(EXPS / "EXP-021*"))))
E22 = next(iter(glob.glob(str(EXPS / "EXP-022*"))))

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


def fmt_int(n):
    return f"{n:,}".replace(",", "{,}")


def count_polys(path):
    """Number of polynomials of a gfan system file: top-level commas inside the braces plus one."""
    t = Path(path).read_text()
    body = t[t.index("{") + 1:t.rindex("}")]
    return body.count(",") + 1


def unpointed_generators():
    """Recession generators of the single unpointed comet of each of the nine failing cells (EXP-007)."""
    rows = []
    for f in sorted(glob.glob(str(Path(E7) / "artifacts" / "*unpointed-certificates.json"))):
        name = Path(f).name.replace("out-", "").replace("-unpointed-certificates.json", "")
        certs = json.loads(Path(f).read_text())
        assert len(certs) == 1 and certs[0]["comet"] == 0, name
        rows.append((name, certs[0]["n_generators"]))
    assert len(rows) == 9, len(rows)
    return rows


GEN_ORDER = ["n4-S1-equal", "n5-S1-V5arith", "n5-S1-V6repeat", "n5-S2-V1pow3", "n5-S2-V2squares",
             "n5-S2-V3pow2", "n5-S2-V4primes", "n5-S2-V5arith", "n5-S2-V6repeat"]
GEN_LABEL = {
    "n4-S1-equal": "S1 equal n4",
    "n5-S1-V5arith": "S1 arithmetic",
    "n5-S1-V6repeat": "S1 repeated",
    "n5-S2-V1pow3": "S2 powers of 3",
    "n5-S2-V2squares": "S2 squares",
    "n5-S2-V3pow2": "S2 powers of 2",
    "n5-S2-V4primes": "S2 primes",
    "n5-S2-V5arith": "S2 arithmetic",
    "n5-S2-V6repeat": "S2 repeated",
}


def cert_support():
    """Nonzero coefficients of the stored infeasibility combination of each unpointed comet."""
    out = []
    for f in sorted(glob.glob(str(Path(E7) / "artifacts" / "*unpointed-certificates.json"))):
        c = json.loads(Path(f).read_text())[0]
        assert len(c["lambda"]) == c["n_generators"]
        out.append(sum(1 for x in c["lambda"] if x != "0"))
    return out


def fig_gens(rows):
    d = dict(rows)
    assert set(d) == set(GEN_ORDER), sorted(d)
    names = ",".join(GEN_LABEL[k] for k in GEN_ORDER)
    s1 = " ".join(f"({GEN_LABEL[k]},{d[k]}) [{d[k]}]" for k in GEN_ORDER if "S1" in k)
    s2 = " ".join(f"({GEN_LABEL[k]},{d[k]}) [{d[k]}]" for k in GEN_ORDER if "S2" in k)
    return names, s1, s2


def fig_times(scr, summ):
    """gfan wall seconds against exact-decider seconds, the twelve n = 5 cells."""
    out = {"S1": [], "S2": []}
    ratios = []
    for sysname in ("S1", "S2"):
        for key in VAL_N5:
            label = f"n5-{sysname}-{key}"
            g = scr[label]["secs"]
            d = summ[f"out-{label}.out"]["seconds"]
            assert d > 0, label
            out[sysname].append(f"({g},{d})")
            ratios.append(100.0 * d / g)
    return " ".join(out["S1"]), " ".join(out["S2"]), min(ratios), max(ratios)


def singular_jobs():
    """EXP-012 times.json: jobs ab-0..ab-14 are the 15 archived subideals, v2-* the lighter menu of 16.
    A wall reading above 120 s is a job that reached the 120 s cap (the record: cap plus WSL overhead)."""
    t = json.loads((Path(E12) / "artifacts" / "times.json").read_text())
    ab_done, ab_capped, menu = [], [], []
    for i, (k, v) in enumerate(t.items()):
        if k.startswith("ab-"):
            assert int(k.split("-")[1]) == i, k
            (ab_capped if v > 120 else ab_done).append((i, v))
        else:
            assert k.startswith("v2-") and v <= 120, (k, v)
            menu.append((i, v))
    assert len(t) == 31 and len(ab_done) == 12 and len(ab_capped) == 3 and len(menu) == 16
    assert [i for i, _ in ab_capped] == [1, 4, 7]
    return ab_done, ab_capped, menu


def fig_singular():
    ab_done, ab_capped, menu = singular_jobs()
    done = ab_done + menu
    return (" ".join(f"({i},{v})" for i, v in ab_done), " ".join(f"({i},{v})" for i, v in ab_capped),
            " ".join(f"({i},{v})" for i, v in menu), min(v for _, v in done), max(v for _, v in done))


def chambers():
    r = json.loads((Path(E20) / "artifacts" / "residual-count.json").read_text())
    per = r["per_orientation_nonzero"]
    assert r["feasible_orientations"] == 24 and len(per) == 24
    assert sum(per.values()) == r["total_residual"]
    unit = min(per.values())
    assert all(v % unit == 0 for v in per.values())
    return sorted(per.values()), r["total_residual"], unit


def fig_chambers():
    vals, total, unit = chambers()
    return " ".join(f"({i},{v / 1e6:.6f})" for i, v in enumerate(vals, start=1))


ATLAS_RUNS = [
    ("core", "EXP-021", "integrated-summary.json"),
    ("tube-L", "EXP-022", "tube-L-summary.json"),
    ("tube-R", "EXP-022", "tube-R-summary.json"),
    ("tubeext-L", "EXP-022", "tubeext-L-summary.json"),
    ("tubeext-R", "EXP-022", "tubeext-R-summary.json"),
    ("ulow", "EXP-022", "ulow-summary.json"),
    ("fa1", "EXP-022", "fa1-summary.json"),
    ("bicorner-opp", "EXP-022", "bicorner-opp-summary.json"),
    ("fa2b-residue", "EXP-022", "fa2b-residue-summary.json"),
]


def atlas_runs():
    out = []
    for label, exp, fname in ATLAS_RUNS:
        base = E21 if exp == "EXP-021" else E22
        d = json.loads((Path(base) / "artifacts" / fname).read_text())
        c = d["counters"]
        assert d["ok"] is True and c["failed"] == 0, label
        leaves = {k: c.get(k, 0) for k in ("certified", "mv_certified", "trapped", "discarded", "ball_covered")}
        n = sum(leaves.values())
        seeds = 2 * n - c["processed"]
        # a binary bisection forest: processed = 2 * leaves - seeds; the residue re-run of fa2b starts from
        # the 200 residual boxes of the fa2b run, every other run from one seed box
        assert seeds == (200 if label == "fa2b-residue" else 1), (label, c["processed"], n, seeds)
        out.append((label, c["processed"], n, leaves))
    return out


def fig_atlas():
    runs = atlas_runs()
    names = ",".join(r[0] for r in runs)
    series = {}
    for key in ("certified", "mv_certified", "trapped", "discarded"):
        series[key] = " ".join(f"({r[0]},{100.0 * r[3][key] / r[2]:.3f})" for r in runs)
    total_leaves = sum(r[2] for r in runs)
    ball = sum(r[3]["ball_covered"] for r in runs)
    certified_share = 100.0 * sum(r[3]["certified"] for r in runs) / total_leaves
    return names, series, len(runs), total_leaves, ball, certified_share, runs


def macros(scr, summ):
    _, _, rmin, rmax = fig_times(scr, summ)
    _, _, _, smin, smax = fig_singular()
    vals, total, unit = chambers()
    _, _, nruns, leaves, ball, cshare, runs = fig_atlas()
    gens = unpointed_generators()
    g1 = [v for k, v in gens if "S1" in k]
    g2 = [v for k, v in gens if "S2" in k]
    n5s1 = count_polys(Path(E4) / "artifacts" / "sys-n5-S1.txt")
    n5s2 = count_polys(Path(E4) / "artifacts" / "sys-n5-S2.txt")
    n4s1 = count_polys(Path(E4) / "artifacts" / "sys-n4-S1.txt")
    assert (n5s1, n5s2, n4s1) == (35, 25, 19), (n5s1, n5s2, n4s1)
    share = lambda r, k: 100.0 * r[3][k] / r[2]
    tmax = max(runs, key=lambda r: share(r, "trapped"))
    cmin = min(runs, key=lambda r: share(r, "certified"))
    cmax = max(runs, key=lambda r: share(r, "certified"))
    items = [
        ("numAtlasTrapMax", f"{share(tmax, 'trapped'):.0f}"), ("numAtlasTrapRun", tmax[0]),
        ("numAtlasCertMin", f"{share(cmin, 'certified'):.0f}"), ("numAtlasCertMinRun", cmin[0]),
        ("numAtlasCertMax", f"{share(cmax, 'certified'):.0f}"), ("numAtlasCertMaxRun", cmax[0]),
        ("numCertNzMin", str(min(cert_support()))), ("numCertNzMax", str(max(cert_support()))),
        ("numRatioMin", f"{rmin:.1f}"), ("numRatioMax", f"{rmax:.1f}"),
        ("numSingMin", f"{smin:.1f}"), ("numSingMax", f"{smax:.1f}"),
        ("numChamberTotal", fmt_int(total)), ("numChamberUnit", fmt_int(unit)),
        ("numGenSoneMin", str(min(g1))), ("numGenSoneMax", str(max(g1))),
        ("numGenStwoMin", str(min(g2))), ("numGenStwoMax", str(max(g2))),
        ("numAtlasRuns", str(nruns)), ("numAtlasLeaves", fmt_int(leaves)),
        ("numAtlasBall", str(ball)), ("numAtlasCertShare", f"{cshare:.0f}"),
        ("numPolyFiveOne", str(n5s1)), ("numPolyFiveTwo", str(n5s2)), ("numPolyFourOne", str(n4s1)),
    ]
    return "\n".join("\\newcommand{\\" + k + "}{" + v + "}" for k, v in items)


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
        "fig-gens-names": fig_gens(unpointed_generators())[0],
        "fig-gens-s1": fig_gens(unpointed_generators())[1],
        "fig-gens-s2": fig_gens(unpointed_generators())[2],
        "fig-times-s1": fig_times(scr, summ)[0],
        "fig-times-s2": fig_times(scr, summ)[1],
        "fig-singular-done": fig_singular()[0],
        "fig-singular-capped": fig_singular()[1],
        "fig-singular-menu": fig_singular()[2],
        "fig-chambers": fig_chambers(),
        "fig-atlas-names": fig_atlas()[0],
        "fig-atlas-cert": fig_atlas()[1]["certified"],
        "fig-atlas-mv": fig_atlas()[1]["mv_certified"],
        "fig-atlas-trap": fig_atlas()[1]["trapped"],
        "fig-atlas-disc": fig_atlas()[1]["discarded"],
        "macros": macros(scr, summ),
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
