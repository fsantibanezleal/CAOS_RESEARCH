"""Generate every table and data-driven figure of main.tex from the archived computations.

Usage (from any directory):
    python make_tables.py            # writes tables/*.tex next to this file
    python make_tables.py --check    # also asserts every encoding-size formula against pcclib

Inputs (read only): problems/combinatorics/petersen-coloring/experiments/EXP-*/artifacts/*.json and
the encoders of problems/combinatorics/petersen-coloring/code/pcclib. Nothing is solved here: the
encoders only build formulas (to count variables and clauses) and the stored witnesses are only
classified. A later version regenerates the tables by running this script again.
"""

from __future__ import annotations

import argparse
import collections
import glob
import json
import math
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PC = ROOT / "problems/combinatorics/petersen-coloring"
EXPS = PC / "experiments"
sys.path.insert(0, str(PC / "code"))

from pcclib import charges, encoders, graphs, invariants, relaxed  # noqa: E402

OUT = HERE / "tables"
BSL = chr(92)
G5 = ["G112", "H112", "G52", "G52b", "G68"]
FILES = {
    "G112": "putman-112-main.edgelist",
    "H112": "putman-112-d3.edgelist",
    "G52": "gjmmm-52.edgelist",
    "G52b": "gjmmmu-52-b.edgelist",
    "G68": "hog-57280-68.edgelist",
}
MACRO = {"G112": r"$\Gmain$", "H112": r"$\Gsym$", "G52": r"$\Gfty$", "G52b": r"$\Gftyb$", "G68": r"$\Gsix$"}


def J(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def A(exp, name):
    return J(next(iter(glob.glob(str(EXPS / f"{exp}-*/artifacts/{name}")))))


def n_(x: int) -> str:
    return f"{int(x):,}".replace(",", "{,}")


def f1(x: float) -> str:
    s = f"{x:,.1f}"
    return s.replace(",", "{,}")


def write(name: str, text: str) -> None:
    OUT.mkdir(exist_ok=True)
    (OUT / name).write_text(text, encoding="utf-8", newline="\n")


GR = {k: graphs.load_edgelist(PC / "data" / v) for k, v in FILES.items()}

# ---------------------------------------------------------------- encoding sizes ----------


def sinz(n_lits: int, k: int) -> tuple[int, int]:
    """(auxiliary variables, clauses) of the sequential counter of cnf.at_most_k."""
    if k >= n_lits:
        return 0, 0
    if k == 0:
        return 0, n_lits
    return n_lits * k, k + (n_lits - 1) * (2 * k + 1)


def formulas(n: int, ker: dict) -> dict:
    """Variable and clause counts as functions of n (cubic graph, m = 3n/2 edges)."""
    m = 3 * n // 2
    out = {}
    out["petersen"] = (15 * m, 106 * m + 495 * n + 2)
    out["petersen-nosym"] = (15 * m, 106 * m + 495 * n)
    out["relax1"] = (15 * m, 106 * m + 495 * (n - 1) + 2)
    out["relax2"] = (15 * m, 106 * m + 495 * (n - 2) + 2)
    out["normal5"] = (16 * m, 56 * m + 15 * n)
    out["normal5-relaxed-edge"] = (16 * m - 11, 11 * m + 15 * n + 45 * (m - 1))
    out["normal6"] = (19 * m, 70 * m + 18 * n)
    out["strong6"] = (19 * m, 70 * m + 18 * n + m)
    out["bf"] = (6 * m, 24 * n + 26 * m + 2)
    out["fr"] = (3 * m, 12 * n + m + 1)
    for k in (3, 4, 5):
        out[f"berge{k}"] = (k * m, 4 * k * n + m + 1)
    out["cdc5"] = (5 * m, 20 * n + 15 * m + 2)
    for k in (4, 5):
        out[f"flow{k}"] = (
            (k - 1) * m,
            (1 + (k - 1) * (k - 2) // 2) * m + ker["flow"][k] * n,
        )
    for b in (1, 2, 3, 4):
        av, ac = sinz(m, b)
        out[f"odd{b}"] = (2 * m + n + av, 4 * n + 2 * m + ac + 1)
    for b in (1, 2, 3):
        av, ac = sinz(m, b)
        out[f"res{b}"] = (4 * m + av, 7 * m + 9 * n + ac)
    for d in (0, 1, 2):
        av, ac = sinz(n, d)
        out[f"pdef{d}"] = (15 * m + n + av, 106 * m + 495 * n + ac)
    for d in (0, 1):
        av, ac = sinz(m, d)
        out[f"ndef{d}"] = (16 * m + m + av, 56 * m + 15 * n + ac)
    return out


def flow_kernel(k: int) -> int:
    """Violating value triples at a vertex of a nowhere-zero Z_k flow formula."""
    import itertools

    bad = sum(1 for v in itertools.product(range(1, k), repeat=3) if (v[0] + v[1] - v[2]) % k)
    return bad


def built_counts(g, key: str) -> tuple[int, int]:
    fk = {
        "petersen": lambda: encoders.petersen_coloring(g),
        "petersen-nosym": lambda: encoders.petersen_coloring(g, symmetry=False),
        "relax1": lambda: relaxed.petersen_relaxed_vertex(g, 0),
        "relax2": lambda: relaxed.petersen_relaxed_vertices(g, {0, 1}),
        "normal5": lambda: encoders.normal_coloring(g, 5),
        "normal5-relaxed-edge": lambda: relaxed.normal5_relaxed_edge(g, 0),
        "normal6": lambda: encoders.normal_coloring(g, 6),
        "strong6": lambda: encoders.normal_coloring(g, 6, strong=True),
        "bf": lambda: encoders.berge_fulkerson(g),
        "fr": lambda: encoders.fan_raspaud(g),
        "cdc5": lambda: encoders.cycle_double_cover(g, 5),
    }
    if key in fk:
        f = fk[key]()
    elif key.startswith("berge"):
        f = encoders.berge_cover(g, int(key[5:]))
    elif key.startswith("flow"):
        f = encoders.nowhere_zero_flow(g, int(key[4:]))
    elif key.startswith("odd"):
        f = encoders.oddness(g, int(key[3:]))
    elif key.startswith("res"):
        f = encoders.resistance(g, int(key[3:]))
    elif key.startswith("pdef"):
        f = encoders.petersen_coloring(g, defect_bound=int(key[4:]))
    elif key.startswith("ndef"):
        f = encoders.normal_coloring(g, 5, defect_bound=int(key[4:]))
    else:
        raise KeyError(key)
    return f.nvars, len(f.clauses)


KER = {"flow": {4: flow_kernel(4), 5: flow_kernel(5)}}
ORDER = [
    ("petersen", "Petersen edge-image, two symmetry units"),
    ("petersen-nosym", "Petersen edge-image, no symmetry units"),
    ("normal5", "normal 5-edge-coloring"),
    ("relax1", "Petersen, relaxed at one vertex"),
    ("relax2", "Petersen, relaxed at a pair"),
    ("normal5-relaxed-edge", "normal 5, relaxed at one edge"),
    ("pdef0", "Petersen defect bound 0"),
    ("pdef1", "Petersen defect bound 1"),
    ("pdef2", "Petersen defect bound 2"),
    ("ndef0", "normal-5 defect bound 0"),
    ("ndef1", "normal-5 defect bound 1"),
    ("normal6", "normal 6-edge-coloring"),
    ("strong6", "strong normal 6-edge-coloring"),
    ("bf", "Berge--Fulkerson cover"),
    ("berge3", "cover by 3 perfect matchings"),
    ("berge4", "cover by 4 perfect matchings"),
    ("berge5", "cover by 5 perfect matchings"),
    ("fr", "Fan--Raspaud triple"),
    ("cdc5", "5-cycle double cover"),
    ("flow4", "nowhere-zero $\\mathbb Z_4$-flow"),
    ("flow5", "nowhere-zero $\\mathbb Z_5$-flow"),
    ("odd1", "oddness bound 1"),
    ("odd2", "oddness bound 2"),
    ("odd3", "oddness bound 3"),
    ("odd4", "oddness bound 4"),
    ("res1", "resistance bound 1"),
    ("res2", "resistance bound 2"),
    ("res3", "resistance bound 3"),
]
FORM = {  # printed formulas, asserted against the builders by --check
    "petersen": ("22.5n", "654n+2"),
    "petersen-nosym": ("22.5n", "654n"),
    "normal5": ("24n", "99n"),
    "relax1": ("22.5n", "654n-493"),
    "relax2": ("22.5n", "654n-988"),
    "normal5-relaxed-edge": ("24n-11", "99n-45"),
    "pdef0": ("23.5n", "655n"),
    "pdef1": ("24.5n", "657n-2"),
    "pdef2": ("25.5n", "659n-3"),
    "ndef0": ("25.5n", "99n+1.5n"),
    "ndef1": ("27n", "99n+4.5n-2"),
    "normal6": ("28.5n", "123n"),
    "strong6": ("28.5n", "124.5n"),
    "bf": ("9n", "63n+2"),
    "berge3": ("4.5n", "13.5n+1"),
    "berge4": ("6n", "17.5n+1"),
    "berge5": ("7.5n", "21.5n+1"),
    "fr": ("4.5n", "13.5n+1"),
    "cdc5": ("7.5n", "42.5n+2"),
    "flow4": ("4.5n", "27n"),
    "flow5": ("6n", "62.5n"),
}


def encoding_tables(check: bool) -> None:
    vals: dict[str, dict[str, tuple[int, int]]] = {}
    for gk in G5:
        g = GR[gk]
        fm = formulas(g.n, KER)
        vals[gk] = {}
        for key, _ in ORDER:
            vv, cc = fm[key]
            if check:
                bv, bc = built_counts(g, key)
                assert (vv, cc) == (bv, bc), (gk, key, (vv, cc), (bv, bc))
            vals[gk][key] = (vv, cc)
    import re as _re

    for key, (fv, fc) in FORM.items():
        for gk in G5:
            nn = GR[gk].n
            ev = lambda t, nn=nn: eval(_re.sub(r"(\d(?:\.\d+)?)n", lambda mo: mo.group(1) + "*nn", t), {}, {"nn": nn})  # noqa: E731
            assert (ev(fv), ev(fc)) == vals[gk][key], (key, gk, ev(fv), ev(fc), vals[gk][key])
    # cross-check against the archived manifests
    chk = []
    m2 = A("EXP-002", "manifest.json")["targets"]
    m3 = A("EXP-003", "manifest.json")["instances"]
    m4 = A("EXP-004", "manifest.json")["instances"]
    m1 = A("EXP-001", "manifest.json")["targets"]
    for gk in ("G112", "H112", "G52"):
        for key, mm, nm in [("bf", m2, "bf"), ("berge4", m2, "berge4"), ("berge5", m2, "berge5"), ("fr", m2, "fr"),
                            ("cdc5", m3, "cdc5"), ("flow4", m3, "flow4"), ("flow5", m3, "flow5"),
                            ("odd1", m3, "odd_1"), ("odd2", m3, "odd_2"), ("res1", m3, "res_1"), ("res2", m3, "res_2"),
                            ("pdef0", m4, "pdef_0"), ("pdef1", m4, "pdef_1"), ("ndef0", m4, "ndef_0"),
                            ("ndef1", m4, "ndef_1"), ("normal6", m4, "normal6"), ("strong6", m4, "strong6"),
                            ("petersen", m1, "petersen"), ("normal5", m1, "normal5"), ("petersen-nosym", m1, "petersen_nosym")]:
            rec = mm.get(f"{gk}_{nm}")
            if rec is None or "variables" not in rec:
                continue
            assert (rec["variables"], rec["clauses"]) == vals[gk][key], (gk, key, rec["variables"], rec["clauses"], vals[gk][key])
            chk.append((gk, key))
    for gk, p in (("G52b", "battery-G52b.json"), ("G68", "battery-G68.json")):
        inst = A("EXP-008", p)["instances"]
        for key, nm in [("bf", "bf"), ("berge4", "berge4"), ("berge5", "berge5"), ("berge3", "berge3"), ("fr", "fr"),
                        ("cdc5", "cdc5"), ("flow4", "flow4"), ("flow5", "flow5"), ("odd1", "odd_1"), ("odd2", "odd_2"),
                        ("res1", "res_1"), ("res2", "res_2"), ("normal6", "normal6"), ("strong6", "normal6_strong")]:
            rec = inst.get(f"{gk}_{nm}")
            if rec is None:
                continue
            assert (rec["variables"], rec["clauses"]) == vals[gk][key], (gk, key)
            chk.append((gk, key))
    print(f"encoding sizes: {len(chk)} archived instance sizes equal the computed ones" + (" (builders also asserted)" if check else ""))

    # table of formulas
    rows = []
    for key, label in ORDER:
        if key in FORM:
            v, c = FORM[key]
            rows.append(f"{label} & ${v}$ & ${c}$\\\\")
    # oddness, resistance, in terms of the counter size
    rows.append("oddness bound $b$ & $4n+1.5nb$ & $4n+3n+b+(1.5n-1)(2b+1)+1$\\\\")
    rows.append("resistance bound $b$ & $6n+1.5nb$ & $10.5n+9n+b+(1.5n-1)(2b+1)$\\\\")
    write(
        "tab-enc-formulas.tex",
        "\\begin{tabular}{lll}\n\\toprule\nformula & variables & clauses\\\\\n\\midrule\n" + "\n".join(rows) + "\n\\bottomrule\n\\end{tabular}\n",
    )
    # table of values
    rows = []
    for key, label in ORDER:
        cells = []
        for gk in ("G52", "G68", "G112"):
            vv, cc = vals[gk][key]
            cells.append(f"{n_(vv)} / {n_(cc)}")
        rows.append(f"{label} & " + " & ".join(cells) + "\\\\")
    write(
        "tab-enc-values.tex",
        "\\begin{tabular}{llll}\n\\toprule\nformula (variables / clauses) & $n=52$ & $n=68$ & $n=112$\\\\\n\\midrule\n"
        + "\n".join(rows)
        + "\n\\bottomrule\n\\end{tabular}\n",
    )


# ---------------------------------------------------------------- certification -----------


def certification():
    m1 = A("EXP-001", "manifest.json")["targets"]
    rows = []
    figrows = []
    fm = {gk: formulas(GR[gk].n, KER) for gk in G5}
    for gk in G5:
        for kind, key in (("Petersen", "petersen"), ("normal-5", "normal5")):
            if gk in ("G112", "H112", "G52"):
                r = m1[f"{gk}_{key}"]
                v, c, s, pb, ck = r["variables"], r["clauses"], r["seconds"], r["proof_bytes"], r["drat_trim_seconds"]
                ok = r["drat_trim_verified"]
            else:
                p = A("EXP-007", f"p0-{gk}.json")
                r = p["petersen" if key == "petersen" else "normal5"]
                v, c = fm[gk][key]
                s, pb, ck, ok = r["seconds"], r["proof_bytes"], r["drat_trim_seconds"], r["drat_trim_verified"]
            assert ok
            rows.append(f"{MACRO[gk]} {kind} & {n_(v)} & {n_(c)} & {f1(s)} & {n_(pb)} & {f1(ck)}\\\\")
            figrows.append((gk, kind, GR[gk].n, s, pb, ck))
    for gk in ("G112", "H112", "G52"):
        r = m1[f"{gk}_petersen_nosym"]
        assert r["drat_trim_verified"]
        rows.append(
            f"{MACRO[gk]} Petersen, no symmetry units & {n_(r['variables'])} & {n_(r['clauses'])} & {f1(r['seconds'])} & {n_(r['proof_bytes'])} & {f1(r['drat_trim_seconds'])}\\\\"
        )
    write(
        "tab-certify.tex",
        "\\begin{tabular}{lrrrrr}\n\\toprule\ninstance & variables & clauses & solve (s) & proof (bytes) & check (s)\\\\\n\\midrule\n"
        + "\n".join(rows)
        + "\n\\bottomrule\n\\end{tabular}\n",
    )
    # figure: solve time and proof size per instance, log scale
    pts_p = " ".join(f"({gk.replace('G52b','G52p').replace('G112','G112').replace('H112','H112')},{s})" for gk, k, n, s, pb, ck in figrows if k == "Petersen")
    pts_n = " ".join(f"({gk.replace('G52b','G52p')},{s})" for gk, k, n, s, pb, ck in figrows if k == "normal-5")
    sym = ",".join(gk.replace("G52b", "G52p") for gk in G5)
    write(
        "fig-certify-times.tex",
        "\\begin{tikzpicture}\n\\begin{axis}[ybar, bar width=7pt, width=0.92\\textwidth, height=5.4cm, ymode=log, log origin=infty,\n"
        f" symbolic x coords={{{sym}}}, xtick=data, xticklabels={{$\\Gmain$,$\\Gsym$,$\\Gfty$,$\\Gftyb$,$\\Gsix$}}, x tick label style={{font=\\footnotesize}}, ylabel={{solve time (s)}}, ymin=1, ymax=8000,\n"
        " legend style={at={(0.02,0.98)},anchor=north west,font=\\footnotesize}, enlarge x limits=0.15, ymajorgrids]\n"
        f"\\addplot coordinates {{{pts_p}}};\n\\addplot coordinates {{{pts_n}}};\n"
        "\\legend{Petersen encoding, normal-5 encoding}\n\\end{axis}\n\\end{tikzpicture}\n",
    )
    # figure: DRAT proof bytes vs n? keep sizes in the table; second figure from the pair sweeps below
    return figrows


# ---------------------------------------------------------------- invariants table ---------


def invariants_table():
    m2 = A("EXP-002", "manifest.json")["targets"]
    m3 = A("EXP-003", "manifest.json")["instances"]
    b = {"G52b": A("EXP-008", "battery-G52b.json")["instances"], "G68": A("EXP-008", "battery-G68.json")["instances"]}

    def st(gk, exp, name):
        if gk in ("G112", "H112", "G52"):
            r = (m2 if exp == 2 else m3).get(f"{gk}_{name}")
        else:
            r = b[gk].get(f"{gk}_{name}")
        return r["status"] if r else None

    def yn(s):
        return "yes (S)" if s == "SAT" else ("no (U)" if s == "UNSAT" else "--")

    rows = []
    rows.append("order $n$ / edges & " + " & ".join(f"{GR[g].n} / {len(GR[g].edges)}" for g in G5) + " & EXP-001, EXP-007, EXP-008\\\\")
    sym = A("EXP-006", "normal-defect.json")["symmetry"]
    aut = {"G112": len(sym["G112"]["automorphisms"]), "H112": len(sym["H112"]["automorphisms"]), "G52": len(sym["G52"]["automorphisms"]),
           "G52b": len(A("EXP-008", "edges-G52b.json")["automorphisms"]), "G68": len(A("EXP-008", "edges-G68.json")["automorphisms"])}
    assert aut == {"G112": 1, "H112": 6, "G52": 6, "G52b": 6, "G68": 1}, aut
    rows.append("automorphism group order & " + " & ".join(str(aut[g]) for g in G5) + " & EXP-006, EXP-008\\\\")
    st1 = A("EXP-001", "manifest.json")["structure"]
    cuts = {g: st1[g]["cycle_separating_4_cut"] for g in ("G112", "H112", "G52")}
    cuts.update({"G52b": [0, 11, 70, 71], "G68": [2, 11, 90, 97]})
    assert cuts["G112"] == cuts["H112"]
    for g in ("G52b", "G68"):
        assert invariants.is_cycle_separating(GR[g], tuple(cuts[g]))
        assert A("EXP-007", f"p0-{g}.json")["cyclic_cut_below_4"] is None
    cs = lambda c: "$" + BSL + "{" + ",".join(map(str, c)) + BSL + "}$"  # noqa: E731
    rows.append("cycle-separating 4-cut (edge indices) & " + BSL + "multicolumn{2}{c}{" + cs(cuts["G112"]) + "} & " + cs(cuts["G52"]) + " & " + cs(cuts["G52b"]) + " & " + cs(cuts["G68"]) + " & EXP-001, EXP-007, EXP-008 (re-checked here)\\\\")
    rows.append("Petersen coloring / normal 5 & " + " & ".join(["no (U) / no (U)"] * 5) + " & EXP-001, EXP-007\\\\")
    rows.append("Berge--Fulkerson cover & " + " & ".join(yn(st(g, 2, "bf")) for g in G5) + " & EXP-002, EXP-008\\\\")
    rows.append("cover by 5 / by 4 perfect matchings & " + " & ".join(f"{yn(st(g,2,'berge5'))[:3]} / {yn(st(g,2,'berge4'))[:3]} (S)" for g in G5) + " & EXP-002, EXP-008\\\\")
    for g in ("G52b", "G68"):
        assert st(g, 2, "berge3") == "UNSAT"
    rows.append("cover by 3 perfect matchings & not computed$^{a}$ & not computed$^{a}$ & not computed$^{a}$ & " + yn(st("G52b", 2, "berge3")) + " & " + yn(st("G68", 2, "berge3")) + " & EXP-008\\\\")
    for g in G5:
        assert st(g, 2, "berge4") == "SAT" and st(g, 2, "berge5") == "SAT"
    rows.append("perfect matching index & " + " & ".join("4" for g in G5) + " & EXP-002, EXP-008\\\\")
    rows.append("Fan--Raspaud triple & " + " & ".join(yn(st(g, 2, "fr")) for g in G5) + " & EXP-002, EXP-008\\\\")
    rows.append("5-cycle double cover & " + " & ".join(yn(st(g, 3, "cdc5") if g in ("G112", "H112", "G52") else st(g, 3, "cdc5")) for g in G5) + " & EXP-003, EXP-008\\\\")
    rows.append("nowhere-zero $\\mathbb Z_5$-flow & " + " & ".join(yn(st(g, 3, "flow5")) for g in G5) + " & EXP-003, EXP-008\\\\")
    rows.append("nowhere-zero $\\mathbb Z_4$-flow & " + " & ".join(yn(st(g, 3, "flow4")) for g in G5) + " & EXP-003, EXP-008\\\\")
    odd = {"G112": 4, "H112": 4, "G52": 2, "G52b": 2, "G68": 2}
    res = {"G112": 3, "H112": 3, "G52": 2, "G52b": 2, "G68": 2}
    # verify the values against the archived ladders
    for g in G5:
        for bnd in range(1, odd[g]):
            assert st(g, 3, f"odd_{bnd}") == "UNSAT", (g, "odd", bnd)
        assert st(g, 3, f"odd_{odd[g]}") == "SAT"
        for bnd in range(1, res[g]):
            assert st(g, 3, f"res_{bnd}") == "UNSAT", (g, "res", bnd)
        assert st(g, 3, f"res_{res[g]}") == "SAT"
    rows.append("oddness (bounds refuted U / witness S) & " + " & ".join(f"{odd[g]} (1..{odd[g]-1} U, {odd[g]} S)" for g in G5) + " & EXP-003, EXP-008\\\\")
    rows.append("resistance (bounds refuted U / witness S) & " + " & ".join(f"{res[g]} (1..{res[g]-1} U, {res[g]} S)" for g in G5) + " & EXP-003, EXP-008\\\\")
    m4 = A("EXP-004", "manifest.json")["instances"]
    for g in ("G112", "H112", "G52"):
        assert m4[f"{g}_normal6"]["status"] == "SAT" and m4[f"{g}_strong6"]["status"] == "SAT"
    for g, kk in (("G52b", "G52b"), ("G68", "G68")):
        assert b[g][f"{kk}_normal6"]["status"] == "SAT" and b[g][f"{kk}_normal6_strong"]["status"] == "SAT"
    rows.append("normal 6 / strong normal 6 & " + " & ".join(["yes / yes (S)"] * 5) + " & EXP-004, EXP-008\\\\")
    m1t = A("EXP-001", "manifest.json")["targets"]
    for g in ("G112", "H112", "G52"):
        assert m1t[f"{g}_normal5"]["status"] == "UNSAT"
    for g in ("G52b", "G68"):
        assert A("EXP-007", f"p0-{g}.json")["normal5"]["status"] == "UNSAT"
    rows.append("normal chromatic index & " + " & ".join("6" for g in G5) + " & EXP-001, EXP-004, EXP-007, EXP-008\\\\")
    for g in ("G112", "H112", "G52"):
        d0 = A("EXP-006", f"pairs-{g}.json")["pairs"]
        assert all(v["status"] == "SAT" and v["defect"] == 2 for v in d0.values())
    for g in ("G52b", "G68"):
        d0 = A("EXP-008", f"pairs-{g}.json")
        assert d0["summary"]["critical_with_exactly_two_bad"] == d0["summary"]["pairs"]
    rows.append("Petersen defect pd & " + " & ".join("2" for g in G5) + " & EXP-006, EXP-008\\\\")
    nd = A("EXP-006", "normal-defect.json")["upper_bound"]
    t52b = b["G52b"]["G52b_normal5_defect_le2"]["seconds"] if "G52b_normal5_defect_le2" in b["G52b"] else None
    t68 = b["G68"]["G68_normal5_defect_le2"]["seconds"]
    secs = {"G112": nd["G112"]["seconds"], "H112": nd["H112"]["seconds"], "G52": nd["G52"]["seconds"], "G52b": t52b, "G68": t68}
    assert all(nd[g]["checker_defect"] == 2 for g in nd)
    rows.append("abnormal edges: coloring with $\\ab=2$ (S, seconds) & " + " & ".join(f"{f1(secs[g])}" if secs[g] else "--" for g in G5) + " & EXP-006, EXP-008\\\\")
    rows.append("$\\ab$ lower bound 2 (no coloring with 1) & theorem & theorem & orbit sweep (U) & theorem & theorem & EXP-006\\\\")
    pr = {g: A("EXP-006", f"pairs-{g}.json") for g in ("G112", "H112", "G52")}
    pr.update({g: A("EXP-008", f"pairs-{g}.json") for g in ("G52b", "G68")})
    sl = {}
    cnt = {}
    for g, d in pr.items():
        ps = d["pairs"]
        assert all(v["status"] == "SAT" for v in ps.values())
        sl[g] = max(v["seconds"] for v in ps.values())
        cnt[g] = len(ps)
    rows.append("critical vertex pairs, all SAT (S) & " + " & ".join(n_(cnt[g]) for g in G5) + " & EXP-006, EXP-008\\\\")
    rows.append("slowest pair instance (s) & " + " & ".join(f1(sl[g]) if sl[g] >= 1 else f"{sl[g]:.2f}" for g in G5) + " & EXP-006, EXP-008\\\\")
    assert sum(cnt.values()) == 17362
    write(
        "tab-invariants.tex",
        "\\begin{tabular}{>{\\raggedright\\arraybackslash}p{2.85cm}*{5}{>{\\raggedright\\arraybackslash}p{1.95cm}}>{\\raggedright\\arraybackslash}p{1.8cm}}\n\\toprule\n"
        "invariant & $\\Gmain$ & $\\Gsym$ & $\\Gfty$ & $\\Gftyb$ & $\\Gsix$ & computation\\\\\n\\midrule\n" + "\n".join(rows) + "\n\\bottomrule\n\\end{tabular}\n",
    )


# ---------------------------------------------------------------- pair sweeps -------------


def pair_tables():
    mm = A("EXP-006", "manifest.json")
    pr = {g: A("EXP-006", f"pairs-{g}.json") for g in ("G112", "H112", "G52")}
    pr.update({g: A("EXP-008", f"pairs-{g}.json") for g in ("G52b", "G68")})
    sing = {}
    for g in ("G52", "G112"):
        sing[g] = mm["vertices"][g]
    rows = []
    allsec = {}
    for g in G5:
        ps = pr[g]["pairs"]
        n = GR[g].n
        assert len(ps) == n * (n - 1) // 2
        secs = [v["seconds"] for v in ps.values()]
        allsec[g] = secs
        sec_all = sorted(secs)
        med = sec_all[len(sec_all) // 2]
        if g in sing:
            s = sing[g]
            assert all(v["status"] == "UNSAT" and v["verified"] for v in s.values())
            ss = [v["seconds"] for v in s.values()]
            single = f"{len(s)} U ({min(ss):.2f} to {max(ss):.2f} s)"
        else:
            single = "none run; parity theorem"
        exact = sum(1 for v in ps.values() if v.get("defect", 2) == 2) if g in ("G112", "H112", "G52") else len(ps)
        rows.append(
            f"{MACRO[g]} & {n} & {single} & {n_(len(ps))} & {n_(len(ps))} / 0 & {f1(max(secs)) if max(secs)>=1 else f'{max(secs):.2f}'} & {sum(secs)/len(secs):.2f} $\\pm$ {statistics.stdev(secs):.2f} & {med:.2f}\\\\"
        )
    tot = sum(len(pr[g]["pairs"]) for g in G5)
    assert tot == 17362
    rows.append(f"total & & & {n_(tot)} & {n_(tot)} / 0 & & &\\\\")
    write(
        "tab-pairs.tex",
        "\\begin{tabular}{llllllll}\n\\toprule\ngraph & $n$ & single vertices & pairs & SAT / UNSAT & slowest (s) & mean $\\pm$ sd (s) & median (s)\\\\\n\\midrule\n"
        + "\n".join(rows)
        + "\n\\bottomrule\n\\end{tabular}\n",
    )
    # histogram of the G112 pair solve times (log-spaced bins)
    secs = allsec["G112"]
    edges = [0.1 * 10 ** (i / 4) for i in range(0, 11)]  # 0.1 .. 31.6
    counts = [0] * (len(edges) - 1)
    under = 0
    for s in secs:
        if s < edges[0]:
            under += 1
            continue
        for i in range(len(edges) - 1):
            if edges[i] <= s < edges[i + 1]:
                counts[i] += 1
                break
        else:
            counts[-1] += 1
    counts[0] += under
    coords = " ".join(f"({edges[i]*10**(1/8):.3f},{counts[i]})" for i in range(len(counts)))
    write(
        "fig-pair-times.tex",
        "\\begin{tikzpicture}\n\\begin{axis}[ybar interval, width=0.92\\textwidth, height=5.2cm, xmode=log, xlabel={solve time of a pair relaxation (s)},"
        " ylabel={instances}, ymin=0, ymajorgrids, xmin=0.1, xmax=31.6]\n"
        f"\\addplot+[fill opacity=0.7] coordinates {{{' '.join(f'({edges[i]:.4f},{counts[i]})' for i in range(len(counts)))} ({edges[-1]:.4f},0)}};\n"
        "\\end{axis}\n\\end{tikzpicture}\n",
    )
    assert sum(counts) == 6216, sum(counts)
    # charge classes
    name_of, _ = charges.orbit_table()
    cls = {}
    for g in G5:
        gg = GR[g]
        inc = gg.incidence()
        c = collections.Counter()
        for k, v in pr[g]["pairs"].items():
            u, w = (int(x) for x in k.split("-"))
            lab = v["witness"]
            su = charges.signature(charges.vec(lab[e] for e in inc[u]))
            sw = charges.signature(charges.vec(lab[e] for e in inc[w]))
            assert su == sw
            c[name_of[su]] += 1
        cls[g] = c
    assert dict(cls["G52"]) == {"E": 1279, "D2": 37, "D3": 8, "T2": 2}
    orb = charges.ORBITS
    rows = []
    for o in orb:
        rows.append(f"{o} & " + " & ".join(n_(cls[g].get(o, 0)) for g in G5) + "\\\\")
    rows.append("all & " + " & ".join(n_(sum(cls[g].values())) for g in G5) + "\\\\")
    write(
        "tab-classes.tex",
        "\\begin{tabular}{lrrrrr}\n\\toprule\nclass & $\\Gmain$ & $\\Gsym$ & $\\Gfty$ & $\\Gftyb$ & $\\Gsix$\\\\\n\\midrule\n"
        + "\n".join(rows)
        + "\n\\bottomrule\n\\end{tabular}\n",
    )
    order = ["E", "D2", "D3", "T2"]
    sym = ",".join(order)
    coords = " ".join(f"({o},{cls['G52'].get(o,0)})" for o in order)
    write(
        "fig-classes.tex",
        "\\begin{tikzpicture}\n\\begin{axis}[ybar, bar width=18pt, width=0.8\\textwidth, height=5.2cm, ymode=log, log origin=infty, ymin=0.5, ymax=3000,\n"
        f" symbolic x coords={{{sym}}}, xtick=data, xlabel={{charge class of the two bad vertices}}, ylabel={{witnesses of $\\Gfty$}},\n"
        " nodes near coords, nodes near coords align={vertical}, enlarge x limits=0.12, ymajorgrids]\n"
        f"\\addplot coordinates {{{coords}}};\n\\end{{axis}}\n\\end{{tikzpicture}}\n",
    )
    return cls


# ---------------------------------------------------------------- rings and frames --------


def ring_table():
    rows = []
    objs = [("R2", "$C_2$", 2), ("R3", "$C_3$", 3), ("R4", "$C_4$", 4), ("K4G52", "$K_4[\\Gfty]$", 4)]
    for o, name, t in objs:
        pdj = A("EXP-009", f"pd-{o}.json")
        abj = A("EXP-009", f"ab-{o}.json")
        st = pdj["structure"]
        # pd witness
        wit = {b: v for b, v in pdj["bounds"].items() if v["status"] == "SAT"}
        if o == "R4":
            d = A("EXP-009", "r4-designated.json")["R4_relax_18_46_20_18"]
            assert d["checker_defect"] == 4 and d["status"] == "SAT"
            wtxt = f"designated, {d['seconds']:.1f} s"
            pdv = 4
        else:
            (b, v), = wit.items()
            assert v["checker_defect"] == t
            wtxt = f"bound {b}, {v['seconds']:.1f} s"
            pdv = t
        ab = {int(b): v for b, v in abj["bounds"].items()}
        sat = [b for b, v in ab.items() if v["status"] == "SAT"]
        if sat:
            ub = min(sat)
            abtxt = f"$2\\le\\ab\\le{ub}$ (bound {ub} SAT, {ab[ub]['seconds']:.0f} s)"
            assert o == "R2"
        else:
            abtxt = f"$\\ge{t}$; bounds " + ", ".join(str(b) for b in sorted(ab)) + " open at the cap"
        rows.append(
            f"{name} & {st['n']} & {st['edge_connectivity']} & {st['girth']} & {t} & {wtxt} & {pdv} & {abtxt}\\\\"
        )
    p5 = A("EXP-009", "p5-R2.json")["pairs"]
    assert len(p5) == 20 and all(v["status"] == "UNSAT" and v["verified"] for v in p5.values())
    mean = sum(v["seconds"] for v in p5.values()) / 20
    assert round(mean) == 128
    write(
        "tab-rings.tex",
        "\\begin{tabular}{llllllll}\n\\toprule\nobject & order & $\\kappa'$ & girth & $\\mathrm{pd}\\ge$ & witness for $\\mathrm{pd}$ & $\\mathrm{pd}$ & $\\mathrm{ab}$\\\\\n\\midrule\n"
        + "\n".join(rows)
        + "\n\\bottomrule\n\\end{tabular}\n",
    )
    return mean


# ---------------------------------------------------------------- 4-poles -----------------


def pole_tables():
    rows = []
    totals = {}
    for g, fam in (("G52", "G52"), ("G52b", "G52b"), ("G68", "G68"), ("H112", "H112"), ("J5", "J5")):
        reps = 0
        pats = collections.Counter()
        statuses = collections.Counter()
        expected = None
        for f in sorted(glob.glob(str(EXPS / f"EXP-010-*/artifacts/poles-{fam}-w*.json"))):
            d = J(f)
            expected = d.get("representatives", expected)
            for k, v in d["pairs"].items():
                reps += 1
                statuses[v["status"]] += 1
                if v["status"] == "SAT":
                    assert v["checker_ok"]
                    pats[v.get("pattern")] += 1
        totals[g] = (reps, pats, statuses, expected)
    for g in ("G52", "G52b", "G68", "H112", "J5"):
        reps, pats, statuses, expected = totals[g]
        name = MACRO.get(g, "$J_5$")
        assert statuses.get("SAT", 0) == reps
        other = reps - pats.get("crossed", 0) - pats.get("four-distinct", 0) - pats.get("restorable", 0)
        rows.append(
            f"{name} & {n_(reps)} / {n_(expected) if expected else '--'} & {n_(reps)} & {n_(pats.get('crossed',0))} & {n_(pats.get('four-distinct',0))} & {n_(pats.get('restorable',0))} & {other}\\\\"
        )
    write(
        "tab-poles.tex",
        "\\begin{tabular}{lllllll}\n\\toprule\ngraph & pairs run / of the total & colorable & crossed & four-distinct & restorable & other\\\\\n\\midrule\n"
        + "\n".join(rows)
        + "\n\\bottomrule\n\\end{tabular}\n",
    )
    # J5 control from the verdict: 28 representatives
    # distance sets
    ds = collections.Counter()
    decided = 0
    for f in sorted(glob.glob(str(EXPS / "EXP-010-*/artifacts/dist-G52-e*.json"))):
        d = J(f)
        for e, v in d["edges"].items():
            if "dist_set" in v and v["dist_set"] is not None:
                decided += 1
                ds[tuple(v["dist_set"])] += 1
    assert decided == 546 and sum(ds.values()) == 546, decided
    # EXP-011
    rows = []
    for f in sorted(glob.glob(str(EXPS / "EXP-011-*/artifacts/adjacent-pairs-*.json"))):
        d = J(f)
        ps = d["pairs"]
        secs = [v["seconds"] for v in ps.values()]
        s = d["summary"]
        assert s["adjacent_pairs"] == s["critical"] == len(ps)
        rows.append((d["object"], d["n"], len(ps), s["critical"], max(secs), sum(secs) / len(secs)))
    dp = [r for r in rows if r[0].startswith("D_")]
    assert len(dp) == 10 and sum(r[2] for r in dp) == 1530
    erows = []
    for r in rows:
        nm = "$G_{52}$ (control)" if r[0] == "G52" else "\\texttt{" + r[0].replace("_", "\\_") + "}"
        erows.append(f"{nm} & {r[1]} & {r[2]} & {r[3]} & {f1(r[4])} & {f1(r[5])}\\\\")
    write(
        "tab-adjacent.tex",
        "\\begin{tabular}{lrrrrr}\n\\toprule\nobject & order & adjacent pairs & critical & slowest (s) & mean (s)\\\\\n\\midrule\n"
        + "\n".join(erows)
        + "\n\\bottomrule\n\\end{tabular}\n",
    )
    # dot products: bound0 UNSAT verified, bound2 SAT
    dpj = A("EXP-010", "dot-products.json")
    for k, v in dpj.items():
        assert v["bound0"]["status"] == "UNSAT" and v["bound0"].get("verified", v["bound0"].get("drat_trim_verified", True))
        assert v["bound2"]["status"] == "SAT"
    dsrows = []
    for key in sorted(ds, key=lambda k: (len(k), k)):
        dsrows.append(f"$\\{{{','.join(map(str, key))}\\}}$ & {ds[key]}\\\\")
    write(
        "tab-distance.tex",
        "\\begin{tabular}{lr}\n\\toprule\ndistance set $\\mathrm{Dist}(e_0,e)$ & edges $e$ of $\\Gfty$\\\\\n\\midrule\n"
        + "\n".join(dsrows)
        + f"\n\\midrule\ndecided (of 949) & {decided}\\\\\n\\bottomrule\n\\end{{tabular}}\n",
    )
    return totals, ds, rows


# ---------------------------------------------------------------- validation --------------


def validation_tables():
    m1 = A("EXP-001", "manifest.json")
    rows = []
    ctrl = m1["controls"]
    names = {"petersen": "Petersen graph", "K4": "$K_4$", "prism": "prism", "J5": "flower snark $J_5$", "J7": "flower snark $J_7$"}
    for key in ("petersen", "K4", "prism", "J5", "J7"):
        p = ctrl[f"{key}_petersen"]
        q = ctrl[f"{key}_normal5"]
        assert p["status"] == q["status"] == "SAT" and p["checker_defect"] == q["checker_defect"] == 0
        rows.append(f"{names[key]} & {n_(p['variables'])} / {n_(p['clauses'])} & {p['seconds']:.2f} & {n_(q['variables'])} / {n_(q['clauses'])} & {q['seconds']:.2f} & 0 / 0\\\\")
    write(
        "tab-controls.tex",
        "\\begin{tabular}{lllllr}\n\\toprule\ncontrol graph & Petersen vars / clauses & s & normal-5 vars / clauses & s & checker defects\\\\\n\\midrule\n"
        + "\n".join(rows)
        + "\n\\bottomrule\n\\end{tabular}\n",
    )
    # known-value controls of the invariants
    m3 = A("EXP-003", "manifest.json")
    cv = m3["control_values"]
    assert cv["petersen"] == {"oddness": 2, "resistance": 2} and cv["K4"] == {"oddness": 0, "resistance": 0}
    m2 = A("EXP-002", "manifest.json")["controls"]
    assert m2["petersen_berge4"]["status"] == "UNSAT" and m2["petersen_berge4"]["drat_trim_verified"]
    assert m2["petersen_berge5"]["status"] == "SAT" and m2["K4_berge3"]["status"] == "SAT" and m2["prism_berge3"]["status"] == "SAT"
    mi = A("EXP-003", "manifest.json")["instances"]
    assert mi["petersen_flow4"]["status"] == "UNSAT" and mi["J5_flow4"]["status"] == "UNSAT"
    assert mi["K4_flow4"]["status"] == "SAT" and mi["prism_flow4"]["status"] == "SAT"
    rows = [
        "Petersen graph & 5 (4 matchings UNSAT, proof 452 bytes) & 2 & 2 & no (U) & yes\\\\",
        "$J_5$ & $\\le4$ (4 matchings SAT) & 2 & 2 & no (U) & yes\\\\",
        "$K_4$ & 3 (3 matchings SAT) & 0 & 0 & yes & yes\\\\",
        "prism & 3 (3 matchings SAT) & 0 & 0 & yes & yes\\\\",
    ]
    assert m2["petersen_berge4"]["proof_bytes"] == 452
    write(
        "tab-control-values.tex",
        "\\begin{tabular}{llllll}\n\\toprule\ncontrol graph & perfect matching index & oddness & resistance & $\\mathbb Z_4$-flow & $\\mathbb Z_5$-flow\\\\\n\\midrule\n"
        + "\n".join(rows)
        + "\n\\bottomrule\n\\end{tabular}\n",
    )
    pub = m1["public_proofs"]["checks"]
    names = {"main_petersen": "main, Petersen", "main_normal5": "main, normal-5", "d3_petersen": "$D_3$, Petersen", "d3_normal5": "$D_3$, normal-5"}
    rows = []
    for k in ("main_petersen", "main_normal5", "d3_petersen", "d3_normal5"):
        v = pub[k]
        assert v["verified"]
        rows.append(f"{names[k]} & {n_(v['proof_bytes'])} & {f1(v['seconds'])}\\\\")
    write(
        "tab-public.tex",
        "\\begin{tabular}{lrr}\n\\toprule\narchived instance & proof (bytes) & check (s)\\\\\n\\midrule\n" + "\n".join(rows) + "\n\\bottomrule\n\\end{tabular}\n",
    )
    # two-route agreement on G52
    m4 = A("EXP-004", "manifest.json")["instances"]
    c1, c2 = m4["G52_pdef_1"], m4["G52_pdef_2"]
    assert c1["status"] == "UNSAT" and c1["drat_trim_verified"] and c2["status"] == "SAT"
    return c1["seconds"], c1["proof_bytes"], c2["seconds"]


# ---------------------------------------------------------------- figure of the pole F ----


def f_pole_figure():
    """Petersen graph minus the two ends of an edge: the 4-pole F with its four semi-edges."""
    R_out, R_in = 2.0, 1.0
    coords = {}
    for k in range(5):
        a = 90 + 72 * k
        coords[f"o{k}"] = (R_out * math.cos(math.radians(a)), R_out * math.sin(math.radians(a)))
        coords[f"i{k}"] = (R_in * math.cos(math.radians(a)), R_in * math.sin(math.radians(a)))
    edges = [(f"o{k}", f"o{(k+1)%5}") for k in range(5)] + [(f"o{k}", f"i{k}") for k in range(5)] + [(f"i{k}", f"i{(k+2)%5}") for k in range(5)]
    assert len(edges) == 15
    drop = {"o0", "i0"}
    keep = [e for e in edges if not (set(e) & drop)]
    semi = [e for e in edges if len(set(e) & drop) == 1]
    assert len(keep) == 10 and len(semi) == 4
    lines = ["\\begin{tikzpicture}[x=1cm,y=1cm,v/.style={circle,fill=black,inner sep=1.4pt},s/.style={dashed,gray}]"]
    for name in coords:
        if name in drop:
            continue
        x, y = coords[name]
        lines.append(f"\\node[v] ({name}) at ({x:.3f},{y:.3f}) {{}};")
    for a, b in keep:
        lines.append(f"\\draw ({a}) -- ({b});")
    for a, b in semi:
        keepv = a if b in drop else b
        x, y = coords[keepv]
        dx, dy = x / math.hypot(x, y), y / math.hypot(x, y)
        if keepv.startswith("i"):
            dx, dy = (coords["i0"][0] - x), (coords["i0"][1] - y)
            norm = math.hypot(dx, dy)
            dx, dy = dx / norm, dy / norm
        else:
            dx, dy = (coords["o0"][0] - x), (coords["o0"][1] - y)
            norm = math.hypot(dx, dy)
            dx, dy = dx / norm, dy / norm
        lines.append(f"\\draw[s] ({keepv}) -- ++({0.9*dx:.3f},{0.9*dy:.3f});")
    lines.append("\\end{tikzpicture}")
    write("fig-f-pole.tex", "\n".join(lines) + "\n")
    # packing schematic of G52 (six copies of F and the four free vertices of EXP-006)
    free = A("EXP-006", "manifest.json")["free_vertices"]
    assert free["G52"] == [1, 18, 35, 51] and len(free["G112"]) == 16 and len(free["H112"]) == 16
    return free


def extras() -> None:
    """Digest table, oddness and resistance ladders, and the numbers quoted in the prose."""
    m1 = A("EXP-001", "manifest.json")["targets"]
    rows = []
    for gk in G5:
        for kind, key in (("Petersen", "petersen"), ("normal-5", "normal5")):
            if gk in ("G112", "H112", "G52"):
                r = m1[f"{gk}_{key}"]
            else:
                r = A("EXP-007", f"p0-{gk}.json")[key]
            rows.append(f"{MACRO[gk]} {kind} & \\texttt{{{r['cnf_sha256'][:16]}}} & \\texttt{{{r['proof_sha256'][:16]}}}\\\\")
    write(
        "tab-digests.tex",
        "\\begin{tabular}{lll}\n\\toprule\ninstance & formula SHA-256 (first 16 hex digits) & proof SHA-256 (first 16)\\\\\n\\midrule\n"
        + "\n".join(rows)
        + "\n\\bottomrule\n\\end{tabular}\n",
    )
    m3 = A("EXP-003", "manifest.json")["instances"]
    b = {"G52b": A("EXP-008", "battery-G52b.json")["instances"], "G68": A("EXP-008", "battery-G68.json")["instances"]}

    def rec(g, kind, bnd):
        tag = "odd" if kind == "odd" else "res"
        if g in ("G112", "H112", "G52"):
            return m3[f"{g}_{tag}_{bnd}"]
        return b[g][f"{g}_{tag}_{bnd}"]

    odd = {"G112": 4, "H112": 4, "G52": 2, "G52b": 2, "G68": 2}
    res = {"G112": 3, "H112": 3, "G52": 2, "G52b": 2, "G68": 2}
    rows = []
    for g in G5:
        cells = []
        for kind, top in (("odd", odd[g]), ("res", res[g])):
            parts = []
            for bnd in range(1, top + 1):
                r = rec(g, kind, bnd)
                if r["status"] == "UNSAT":
                    assert r["drat_trim_verified"]
                    parts.append(f"{bnd}: U, {n_(r['proof_bytes'])}~B")
                else:
                    parts.append(f"{bnd}: S")
            cells.append("; ".join(parts))
        rows.append(f"{MACRO[g]} & {cells[0]} & {cells[1]}\\\\")
    write(
        "tab-ladders.tex",
        "\\begin{tabular}{lp{5.6cm}p{5.0cm}}\\toprule\ngraph & oddness bounds (status, proof size) & resistance bounds\\\\\n\\midrule\n"
        + "\n".join(rows)
        + "\n\\bottomrule\n\\end{tabular}\n",
    )
    m2 = A("EXP-002", "manifest.json")["targets"]
    m4 = A("EXP-004", "manifest.json")["instances"]
    n6a = max(m4[f"{g}_{k}"]["seconds"] for g in ("G112", "H112", "G52") for k in ("normal6", "strong6"))
    n6b = max(b[g][f"{g}_{k}"]["seconds"] for g in ("G52b", "G68") for k in ("normal6", "normal6_strong"))
    bfa = max(v["seconds"] for v in m2.values())
    bfb = max(r["seconds"] for g in b for k, r in b[g].items() if any(t in k for t in ("_bf", "_berge", "_fr")))
    cdca = max(r["seconds"] for k, r in m3.items() if k.split("_")[0] in ("G112", "H112", "G52"))
    maxproof = max(r["proof_bytes"] for r in m1.values() if "proof_bytes" in r)
    g112 = [v["seconds"] for v in A("EXP-006", "pairs-G112.json")["pairs"].values()]
    vals = {
        "PairUnderOne": n_(sum(1 for x in g112 if x < 1)), "PairOverTen": str(sum(1 for x in g112 if x >= 10)),
        "NsixMaxA": f"{n6a:.2f}", "NsixMaxB": f"{n6b:.2f}", "CoverMaxA": f"{bfa:.2f}", "CoverMaxB": f"{bfb:.1f}",
        "CdcMaxA": f"{cdca:.2f}", "MaxProofGB": f"{maxproof / 1e9:.2f}",
    }
    out = "".join("\\newcommand{\\" + k + "}{" + v + "}\n" for k, v in vals.items())
    write("numbers.tex", out)
    print("numbers:", vals)




def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="assert the printed encoding formulas against the pcclib builders")
    a = ap.parse_args()
    encoding_tables(a.check)
    certification()
    invariants_table()
    pair_tables()
    ring_table()
    pole_tables()
    c1 = validation_tables()
    f_pole_figure()
    extras()
    print("two-route agreement on G52:", c1)
    print("tables written to", OUT)


if __name__ == "__main__":
    main()
