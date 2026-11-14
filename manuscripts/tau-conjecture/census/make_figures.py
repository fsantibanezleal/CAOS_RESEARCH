"""Regenerate the data files of the census manuscript figures from the repository records.

Reads the experiment artifacts of problems/computation-complexity/tau-conjecture and writes
pgfplots tables to manuscripts/tau-conjecture/census/figures/. main.tex draws the axes and reads
these files; no figure value is typed by hand. The script exits with status 1 when an input record
is missing or fails a consistency assertion, and it is deterministic (the files are committed and
a rerun reproduces them byte for byte).

Usage (from anywhere):  python manuscripts/tau-conjecture/census/make_figures.py
Needs sympy (exact Sturm counting for the doubling and Chebyshev series) and the repository tclib.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
PROB = os.path.join(REPO, "problems", "computation-complexity", "tau-conjecture")
EXP = os.path.join(PROB, "experiments")
OUT = os.path.join(HERE, "figures")
sys.path.insert(0, os.path.join(PROB, "code"))


def fail(msg):
    print(f"make_figures: FAILED: {msg}", file=sys.stderr)
    sys.exit(1)


def load(*parts):
    path = os.path.join(EXP, *parts)
    if not os.path.isfile(path):
        fail(f"missing input record {os.path.relpath(path, REPO)}")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def expect(cond, msg):
    if not cond:
        fail(msg)


def write(name, header, rows):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, name), "w", encoding="utf-8", newline="\n") as fh:
        fh.write(" ".join(header) + "\n")
        for r in rows:
            fh.write(" ".join(str(v) for v in r) + "\n")
    print(f"wrote figures/{name} ({len(rows)} rows)")


def fig_counts():
    """States and new polynomials per depth: EXP-002 (1-5), EXP-003 (6), EXP-004 (6 states, 7), EXP-011 (7 states)."""
    c5 = load("EXP-002-census-depth5", "artifacts", "census5.json")
    s6 = load("EXP-003-last-gate-depth6", "artifacts", "scan6.json")
    s7 = load("EXP-004-depth7", "artifacts", "scan7.json")
    pl = load("EXP-011-depth8-pipeline", "artifacts", "pipeline.json")
    rows = []
    for d in range(1, 6):
        pd = c5["per_depth"][str(d)]
        expect(pd["complete"], f"depth {d} not complete")
        rows.append((d, pd["states"], pd["new_polynomials"]))
    expect(s6["base_depth"] == 5 and s6["states_scanned"] == rows[-1][1], "EXP-003 base frontier mismatch")
    expect(s7["base_depth"] == 6 and s7["scan_complete"], "EXP-004 not complete")
    expect(pl["build7"]["new7"] == s7["new_polynomials"], "EXP-011 new7 differs from EXP-004")
    expect(pl["validate"]["new6"] == s6["new_polynomials"], "EXP-011 validate new6 differs from EXP-003")
    expect(pl["validate"]["frontier6"] == s7["stage1_states"], "depth-6 state count differs between EXP-011 and EXP-004")
    rows.append((6, s7["stage1_states"], s6["new_polynomials"]))
    rows.append((7, pl["build7"]["frontier7"], s7["new_polynomials"]))
    write("fig-counts.dat", ["depth", "states", "newpolys"], rows)


def fig_zhist():
    """Distinct integer roots: new polynomials at tau 6 and 7, last-gate applications at depth 8."""
    s6 = load("EXP-003-last-gate-depth6", "artifacts", "scan6.json")["z_histogram_new"]
    s7r = load("EXP-004-depth7", "artifacts", "scan7.json")
    s7 = s7r["z_histogram_new"]
    s8r = load("EXP-011-depth8-pipeline", "artifacts", "scan8_final.json")
    s8 = s8r["hist"]
    expect(sum(s6.values()) == 134494, "tau 6 histogram does not sum to 134,494")
    expect(sum(s7.values()) == s7r["new_polynomials"], "tau 7 histogram does not sum to its polynomial count")
    expect(sum(s8.values()) == 208411120719, "depth-8 histogram does not sum to 208,411,120,719")
    expect(s8r["zmax"] == 6 and max(int(k) for k in s8) == 6, "depth-8 zmax is not 6")
    rows = []
    t6, t7, t8 = sum(s6.values()), sum(s7.values()), sum(s8.values())
    for z in range(0, 7):
        a, b, c = s6.get(str(z), 0), s7.get(str(z), 0), s8.get(str(z), 0)
        # share = percentage of the histogram total; a zero count is written as nan (not plotted)
        sh = [f"{100.0 * v / t:.8g}" if v else "nan" for v, t in ((a, t6), (b, t7), (c, t8))]
        rows.append((z, a, b, c, *sh))
    write("fig-zhist.dat", ["z", "n6", "n7", "n8", "p6", "p7", "p8"], rows)


def fig_funnel():
    """Window-free additive scan, stage counters of EXP-015 final.json."""
    t = load("EXP-015-unwindowed-additive", "artifacts", "final.json")["totals"]
    expect(t["candidates"] == 4000 * t["states"], "candidates != 4000 x states")
    expect(t["pass3"] == t["zero_suspect"] + t["zero_exact"] + t["exact"], "pass3 identity fails")
    expect(t["hits"] == 0, "EXP-015 reports hits")
    stages = [
        ("candidates", t["candidates"]),
        ("degree_survivors", t["candidates"] - t["deg_drop"]),
        ("pass2", t["pass2"]),
        ("pass3", t["pass3"]),
        ("exact", t["exact"]),
        ("zero_exact", t["zero_exact"]),
        ("zero_suspect", t["zero_suspect"]),
    ]
    write("fig-funnel.dat", ["idx", "stage", "count"], [(i, n, v) for i, (n, v) in enumerate(stages)])


def fig_partitions():
    """Per-partition distinct states (EXP-011) and wall-clock seconds of the window-free scan (EXP-015)."""
    s8 = load("EXP-011-depth8-pipeline", "artifacts", "scan8_final.json")
    p15 = load("EXP-015-unwindowed-additive", "artifacts", "final.json")["totals"]
    import math
    import statistics
    rows = []
    exact = []
    tot_states, tot_cand, tot_sec = 0, 0, 0.0
    for h in range(256):
        a = load("EXP-011-depth8-pipeline", "artifacts", "scan8_parts_final", f"part{h:03d}.json")
        b = load("EXP-015-unwindowed-additive", "artifacts", "parts", f"part{h:03d}.json")
        expect(a["part"] == h and b["part"] == h, f"partition index mismatch at {h}")
        expect(a["states"] == b["stats"]["states"], f"states differ between EXP-011 and EXP-015 at partition {h}")
        rows.append((h, a["states"], b["seconds"]))
        exact.append(b["stats"]["exact"])
        tot_states += a["states"]
        tot_cand += b["stats"]["candidates"]
        tot_sec += b["seconds"]
    expect(tot_states == s8["states"] == 1048460912, "partition states do not sum to 1,048,460,912")
    expect(tot_cand == p15["candidates"], "partition candidates do not sum to final.json")
    write("fig-partitions.dat", ["part", "states", "seconds"], rows)
    st = [r[1] for r in rows]
    sec = [r[2] for r in rows]
    mean_x, mean_s = statistics.mean(exact), statistics.mean(sec)
    corr = sum((a - mean_x) * (b - mean_s) for a, b in zip(exact, sec)) / math.sqrt(
        sum((a - mean_x) ** 2 for a in exact) * sum((b - mean_s) ** 2 for b in sec))

    def thou(n):
        return f"{int(round(n)):,}".replace(",", "{,}")

    macros = {
        "PartStatesMin": thou(min(st)),
        "PartStatesMax": thou(max(st)),
        "PartStatesSpread": f"{100.0 * (max(st) - min(st)) / statistics.mean(st):.2f}",
        "PartSecMin": thou(min(sec)),
        "PartSecMax": thou(max(sec)),
        "PartSecMedian": thou(statistics.median(sec)),
        "PartSecOver": str(sum(1 for v in sec if v > 10000)),
        "PartSecHours": f"{tot_sec / 3600.0:.0f}",
        "PartExactMin": thou(min(exact)),
        "PartExactMax": thou(max(exact)),
        "PartExactSpread": f"{100.0 * (max(exact) - min(exact)) / mean_x:.1f}",
        "PartCorr": f"{corr:.2f}",
    }
    with open(os.path.join(OUT, "partition-stats.tex"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("% generated by make_figures.py from the per-partition records; do not edit\n")
        for k, v in macros.items():
            fh.write(f"\\newcommand{{\\{k}}}{{{v}}}\n")
    print("wrote figures/partition-stats.tex", macros)


def fig_family():
    """Quadratic family h_c = x^2 - c, EXP-005: tower yield and exact cost of the constant c, per c with nonzero yield."""
    d = load("EXP-005-family-towers", "artifacts", "family.json")
    pc = d["per_c_nonzero"]
    expect(d["family_zmax"] == 5 and d["family_argmax"] == 2 and d["cmax"] == 200, "family summary differs from the paper")
    rows = [(int(c), v["z_max_shapes"], v["tau_c"]) for c, v in pc.items()]
    rows.sort()
    expect(max(r[1] for r in rows) == 5 and [r[0] for r in rows if r[1] == 5] == [2], "yield 5 is not attained only at c = 2")
    write("fig-family.dat", ["c", "yield", "tauc"], rows)


def count_real_roots(coeffs):
    import sympy as sp
    x = sp.Symbol("x")
    p = sp.Poly(list(reversed(coeffs)), x, domain="ZZ")
    if p.degree() < 1:
        return 0
    p = p.quo(sp.Poly(sp.gcd(p, p.diff(x)), x, domain="ZZ"))
    return int(p.count_roots()) if p.degree() >= 1 else 0


def fig_doubling():
    """The real doubling step g -> g (g - x^2) from the tau = 4 record, and the Chebyshev tower, exact Sturm counts."""
    from tclib.enum import pmul, padd, psub
    a = pmul((0, 1), (0, 1))
    g = psub(pmul(psub(a, (1,)), psub(a, (1,))), a)
    gates = 4
    rows = [(gates, len(g) - 1, count_real_roots(g))]
    for _ in range(4):
        h = psub(g, a)
        g = pmul(g, h)
        gates += 2
        rows.append((gates, len(g) - 1, count_real_roots(g)))
    expect([r[2] for r in rows][:3] == [4, 8, 16], "doubling family does not start 4, 8, 16")
    write("fig-doubling.dat", ["gates", "degree", "real"], rows)
    # Chebyshev tower T_(2^k): T_2 = 2x^2 - 1 costs three gates, each composition adds three
    T = psub(padd(a, a), (1,))
    cheb = [(3, count_real_roots(T))]
    gates = 3
    for _ in range(3):
        d = pmul(T, T)
        T = psub(padd(d, d), (1,))
        gates += 3
        cheb.append((gates, count_real_roots(T)))
    expect(cheb == [(3, 2), (6, 4), (9, 8), (12, 16)], "Chebyshev tower counts differ from 2^k at 3k gates")
    write("fig-chebyshev.dat", ["gates", "real"], cheb)


def main():
    for f in (fig_counts, fig_zhist, fig_funnel, fig_partitions, fig_family, fig_doubling):
        f()
    print("make_figures: ok")


if __name__ == "__main__":
    main()
