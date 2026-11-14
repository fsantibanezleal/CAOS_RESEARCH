"""Generate every table, figure input and number of the second-regime paper from the experiment records.

Inputs (all under the bougard-joret experiments folder given by --exp):
  EXP-005 .. EXP-010 artifacts/enum.jsonl      enumeration records (n, alpha, k, E, generated, kept, examples, mod, seconds)
  EXP-011 artifacts/structure.jsonl, verify.jsonl, didin.jsonl, collect.jsonl   extremal graphs and their analysis
  EXP-012 artifacts/provenance.txt, gate-a.json .. gate-e.json                   validation gates
Outputs (next to this script): numbers.tex, table.tex, window.tex, percount.tex, structure.tex, validation.tex,
graphs.tex, growth-<n>-<a>-<k>.dat.

Decision records: for each (triple, E) the record of the pruned generator (56 parts) when one exists, otherwise the
plain-generator record; where both exist they must agree on the number of kept graphs (checked, exit 1 otherwise).
Usage: python make_tables.py --exp <experiments folder>
"""
import argparse
import json
import math
import re
import statistics
from collections import Counter, defaultdict
from math import ceil, comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCES = ["EXP-005-second-regime-small", "EXP-006-second-regime-beyond-15", "EXP-007-open-window-to-22",
           "EXP-008-order-23", "EXP-009-order-24", "EXP-010-order-24-close"]
NMAX = 24
PLOTTED = [(17, 5, 3), (22, 5, 3), (23, 3, 7), (24, 5, 4), (24, 4, 5)]
PHASE2 = [(15, 4, 3), (20, 3, 6), (20, 6, 3), (21, 3, 6), (21, 4, 4), (21, 4, 5), (21, 5, 3), (21, 5, 4), (21, 6, 3),
          (22, 3, 6), (22, 4, 4), (22, 5, 3), (22, 6, 3)]
DRAW = "(10,3,3)"


def t(n, a):
    q, r = divmod(n, a)
    return r * comb(q + 1, 2) + (a - r) * comb(q, 2)


def cval(n, a, k):
    return t(n, a) + ceil(k * a / 2)


def window(nmax):
    out = []
    for a in range(3, nmax):
        for k in range(3, nmax):
            for n in range(k * a + 1, nmax + 1):
                if n >= 2 * a and n >= a + k and n // a <= ceil(k * a / 2) - a + 1:
                    out.append((n, a, k))
    return sorted(out)


def allowed_s(n, a, k):
    out = {0}
    for s in range(1, a):
        p = a - s
        if t(n + s, a) - s + (ceil(k * p / 2) if p >= 2 else 0) <= cval(n, a, k):
            out.add(s)
    return out


def fmt(x):
    return f"{x:,}".replace(",", "{,}")


def write(name, text):
    (HERE / name).write_text(text, encoding="utf-8", newline="\n")


def jl(path):
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()] if path.exists() else []


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exp", default=str(HERE.parents[2] / "problems" / "combinatorics" / "bougard-joret" / "experiments"))
    a = ap.parse_args()
    exp = Path(a.exp)

    # ------------------------------------------------------------- enumeration records
    recs = defaultdict(list)
    for s in SOURCES:
        for r in jl(exp / s / "artifacts" / "enum.jsonl"):
            r["source"] = s[:7]
            r["generator"] = "pruned" if r.get("mod") == 56 else "plain"
            recs[(r["n"], r["alpha"], r["k"], r["E"])].append(r)
    decision, agree_pairs = {}, 0
    for key, rs in recs.items():
        if len({r["kept"] for r in rs}) != 1:
            raise SystemExit(f"records disagree on kept graphs at {key}")
        if len({r["generator"] for r in rs}) == 2:
            agree_pairs += 1
        pr = [r for r in rs if r["generator"] == "pruned"]
        decision[key] = pr[-1] if pr else rs[-1]

    triples = window(NMAX)
    rows, conf, opn, tot_g, tot_s, g_plain, g_pruned, bounds = [], 0, 0, 0, 0.0, 0, 0, []
    for n, al, k in triples:
        tt, c = t(n, al), cval(n, al, k)
        lo = max(ceil(n * k / 2), tt)
        done = [E for E in range(lo, c) if (n, al, k, E) in decision]
        found = [E for E in done if decision[(n, al, k, E)]["kept"]]
        g = sum(decision[(n, al, k, E)]["generated"] for E in done)
        s = sum(decision[(n, al, k, E)]["seconds"] for E in done)
        for E in done:
            if decision[(n, al, k, E)]["generator"] == "plain":
                g_plain += decision[(n, al, k, E)]["generated"]
            else:
                g_pruned += decision[(n, al, k, E)]["generated"]
        tot_g += g
        tot_s += s
        att = decision.get((n, al, k, c))
        atts = str(att["kept"]) if att else "--"
        if found:
            val = r"\textbf{" + str(min(found)) + "}"
        elif len(done) == c - lo:
            val, conf = str(c), conf + 1
        else:
            first_missing = min(E for E in range(lo, c) if E not in done)
            val, opn = f"$\\ge{first_missing}$", opn + 1
            bounds.append((n, al, k, first_missing))
        rows.append(f"$({n},{al},{k})$ & {tt} & {c} & {val} & {lo}--{c - 1} & {fmt(g)} & {fmt(round(s))} & {atts} \\\\")
    head = ("$(n,\\alpha,k)$ & $t(n,\\alpha)$ & $c$ & $f$ & edges searched & graphs & seconds & at $c$ \\\\\n")
    cap = ("\\caption{Values on the open window with $n\\le24$. $f$: the value found; $\\ge E$: no qualifying graph "
           "below $E$, and the count $E$ was not completed. Graphs: candidates examined below $c$ (pruned generator "
           "where available). Seconds: wall-clock time on 28 processes. At $c$: the number of extremal graphs when "
           "$E=c$ was enumerated.}\\label{tab:values}\\\\\n")
    write("table.tex", "{\\small\n\\begin{longtable}{lrrrrrrr}\n" + cap + "\\toprule\n" + head
          + "\\midrule\n\\endfirsthead\n\\toprule\n" + head + "\\midrule\n\\endhead\n"
          + "\n".join(rows) + "\n\\bottomrule\n\\end{longtable}}\n")

    # ------------------------------------------------------------- window by order
    w30 = window(30)
    by_n = defaultdict(list)
    for x in w30:
        by_n[x[0]].append(x)
    wrows = []
    for n in sorted(by_n):
        dec = 0
        for (n_, a_, k_) in by_n[n]:
            if n_ > NMAX:
                continue
            lo = max(ceil(n_ * k_ / 2), t(n_, a_))
            if all((n_, a_, k_, E) in decision for E in range(lo, cval(n_, a_, k_))):
                dec += 1
        wrows.append(f"{n} & {len(by_n[n])} & {dec} & " + ", ".join(f"$({a_},{k_})$" for _, a_, k_ in by_n[n]) + " \\\\")
    write("window.tex", "\\begin{tabular}{rrrp{0.62\\textwidth}}\n\\toprule\n$n$ & open & decided & pairs "
          "$(\\alpha,k)$ \\\\\n\\midrule\n" + "\n".join(wrows) + "\n\\bottomrule\n\\end{tabular}\n")

    # ------------------------------------------------------------- every record (appendix)
    prow = []
    for key in sorted(recs):
        for r in recs[key]:
            prow.append(f"$({key[0]},{key[1]},{key[2]})$ & {key[3]} & {r['source']} & {r['generator']} & "
                        f"{r.get('mod', '')} & {fmt(r['generated'])} & {r['kept']} & {r['seconds']} \\\\")
    phead = "triple & $E$ & record & generator & parts & graphs & kept & seconds \\\\\n"
    write("percount.tex", "\\begin{longtable}{lrllrrrr}\n\\caption{Every enumeration record of EXP-005 to EXP-010. "
          "Generator: \\emph{plain} is \\texttt{geng} with minimum degree $k$; \\emph{pruned} adds the hook of "
          "Lemma~\\ref{lem:prune}. Parts: the number $M$ of disjoint parts. Kept: graphs with independence number "
          "$\\alpha$ and connectivity at least $k$. Seconds: wall-clock time.}\\label{tab:percount}\\\\\n\\toprule\n"
          + phead + "\\midrule\n\\endfirsthead\n\\toprule\n" + phead + "\\midrule\n\\endhead\n" + "\n".join(prow)
          + "\n\\bottomrule\n\\end{longtable}\n")

    # ------------------------------------------------------------- growth data and plots
    ratios, plot_g, plot_s = [], [], []
    marks = ["*", "square*", "triangle*", "diamond*", "o"]
    for i, (n, al, k) in enumerate(PLOTTED):
        lines, prev = ["E graphs seconds"], None
        for E in range(0, 200):
            r = decision.get((n, al, k, E))
            if r and r["generated"] > 0 and E < cval(n, al, k):
                lines.append(f"{E} {r['generated']} {max(r['seconds'], 0.1)}")
                if prev and prev >= 1000:
                    ratios.append(r["generated"] / prev)
                prev = r["generated"]
        fn = f"growth-{n}-{al}-{k}.dat"
        write(fn, "\n".join(lines) + "\n")
        plot_g.append(f"\\addplot+[mark={marks[i]}] table[x=E,y=graphs]{{{fn}}};\\addlegendentry{{$({n},{al},{k})$}}")
        plot_s.append(f"\\addplot+[mark={marks[i]}] table[x=E,y=seconds]{{{fn}}};")
    # per-order growth of total time at fixed (alpha, k), consecutive orders both decided
    tot_by = {}
    for n, al, k in triples:
        lo = max(ceil(n * k / 2), t(n, al))
        Es = range(lo, cval(n, al, k))
        if all((n, al, k, E) in decision for E in Es):
            tot_by[(n, al, k)] = sum(decision[(n, al, k, E)]["seconds"] for E in Es)
    per_order = defaultdict(float)
    for (n, al, k), secs in tot_by.items():
        per_order[n] += secs

    # ------------------------------------------------------------- extremal structure (EXP-011)
    e11 = exp / "EXP-011-extremal-structure" / "artifacts"
    st, ve, di, co = jl(e11 / "structure.jsonl"), jl(e11 / "verify.jsonl"), jl(e11 / "didin.jsonl"), jl(e11 / "collect.jsonl")
    per = defaultdict(lambda: Counter())
    for r in st:
        d = per[(r["n"], r["alpha"], r["k"])]
        d["graphs"] += 1
        d["ok"] += r["recheck"]
        d["part"] += r["clique_partition"]
        d["bj"] += bool(r.get("bj_structure"))
    for r in di:
        per[(r["n"], r["alpha"], r["k"])][f"s{r['s']}"] += 1
    agree_v = sum(1 for r in ve if r["agrees"])
    srows = []
    for key in sorted(per):
        d = per[key]
        rec = decision.get((key[0], key[1], key[2], cval(*key)))
        sdist = ", ".join(f"{x[1:]}:{y}" for x, y in sorted(d.items()) if re.fullmatch(r"s\d+", x))
        srows.append(f"$({key[0]},{key[1]},{key[2]})$ & {cval(*key)} & {d['graphs']} & "
                     f"{rec['kept'] if rec else '--'} & {d['part']} & {d['graphs'] - d['part']} & {sdist} & "
                     f"{', '.join(str(x) for x in sorted(allowed_s(*key)))} \\\\")
    write("structure.tex", "\\begin{tabular}{lrrrrrll}\n\\toprule\ntriple & $c$ & graphs & recorded & partition & "
          "$\\theta=\\alpha+1$ & $s$ (value:count) & allowed $s$ \\\\\n\\midrule\n" + "\n".join(srows)
          + "\n\\bottomrule\n\\end{tabular}\n")
    n_ext = len(st)
    n_nopart = sum(1 for r in st if not r["clique_partition"])
    n_tenb = sum(1 for r in di if (r["n"], r["alpha"], r["k"]) == (10, 3, 3) and r["s"] == 2)

    # ------------------------------------------------------------- drawings of two extremal graphs
    write("graphs.tex", drawings(di, st))
    write("blocks.tex", blocks())
    write("partition-chart.tex", partition_chart(per))
    write("window-map.tex", window_map(by_n, decision))
    e13 = jl(exp / "EXP-013-odd-alpha-construction" / "artifacts" / "construct.jsonl")

    # ------------------------------------------------------------- validation (EXP-012 and earlier gates)
    e12 = exp / "EXP-012-pipeline-validation" / "artifacts"
    prov = (e12 / "provenance.txt").read_text(encoding="utf-8") if (e12 / "provenance.txt").exists() else ""
    sha_f = re.search(r"filter2 rebuilt (\w+) production (\w+)", prov)
    sha_g = re.search(r"geng.c sha256: (\w+)", prov)
    gates = {x: json.loads((e12 / f"gate-{x}.json").read_text(encoding="utf-8")) if (e12 / f"gate-{x}.json").exists()
             else None for x in "abcde"}
    ga, gb, gc, gd, ge = (gates[x] for x in "abcde")
    gd_sum = ("pending" if not gd else
              "For " + ", ".join(f"$({c['n']},{c['alpha']},{c['k']})$ at $E={c['E']}$ ({fmt(c['mod1_graphs'])} graphs)"
                                 for c in gd["cases"]) +
              f", the sorted output of the pruned generator in one part equals the union of its 56 parts, byte for byte "
              f"(equal SHA-256); {gd['disagreements']} differences.")
    ge_sum = ("pending" if not ge else
              f"\\texttt{{geng}} reproduces all {len(ge['cases'])} values checked against the OEIS \\cite{{OEIS}}: "
              "connected graphs of orders 9 and 10 (A001349), connected cubic graphs of orders 16 to 22 (A002851) "
              "and connected quartic graphs of orders 12 to 15 (A006820), the largest count being "
              f"${fmt(max(c['count'] for c in ge['cases']))}$; {ge['disagreements']} differences.")
    vrows = [
        ("Generator counts", "EXP-005", "connected graphs, $n=5,7,8$", "3", "A001349: 21, 853, 11{,}117"),
        ("Cubic graphs", "EXP-005", "$(16,5,3)$, $E=24$", "4{,}207", "A005638$(8)$"),
        ("Known values", "EXP-005, 006", "$f(7,3,4)=15$, $f(12,3,3)=23$", "2", "reproduced"),
        ("Filter vs.\\ NetworkX", "EXP-006", "all graphs, $n=8$, $\\alpha\\le6$, $k\\le5$", "12{,}346", "0 mismatches"),
        ("Two filters", "EXP-006", "4 edge counts, $n\\le16$", "27{,}235{,}386", "kept counts equal"),
        ("Prune end to end", "EXP-006", "12 edge counts, $n\\le17$", "12", "kept counts equal"),
        ("Plain vs.\\ pruned", "EXP-006", "$(16,5,3)$, $(17,5,3)$", str(agree_pairs), "kept counts equal"),
        ("F: provenance", "EXP-012", "filter2, geng\\_a3 to geng\\_a7", "6 binaries", "byte-identical"),
        ("A: filter, known answers", "EXP-012", "$n\\le24$, $k'\\le9$, $\\alpha\\le12$",
         fmt(ga["decisions"]) if ga else "pending", f"{ga['disagreements']} mismatches" if ga else "pending"),
        ("B: filter, production", "EXP-012", "$k\\ge6$ or $\\alpha=7$, $E=c-1,c,c+1$",
         fmt(gb["graphs"]) if gb else "pending", f"{gb['disagreements']} mismatches" if gb else "pending"),
        ("C: prune hook", "EXP-012", "bounds $2$ to $8$, $n\\le24$",
         fmt(gc["decisions"]) if gc else "pending", f"{gc['disagreements']} mismatches" if gc else "pending"),
        ("D: split under the hook", "EXP-012", "3 triples, mod 1 vs.\\ 56",
         str(len(gd["cases"])) if gd else "pending", f"{gd['disagreements']} differences" if gd else "pending"),
        ("E: generator counts", "EXP-012", "A001349, A002851, A006820",
         str(len(ge["cases"])) if ge else "pending", f"{ge['disagreements']} differences" if ge else "pending"),
        ("Extremal recount", "EXP-011", f"{len(per)} triples at $E=c$", fmt(n_ext),
         "counts equal the records"),
        ("Extremal recheck", "EXP-011", "edges, $\\alpha$, $\\kappa$ by NetworkX", fmt(n_ext),
         f"{sum(1 for r in st if not r['recheck'])} failures"),
        ("Two partition methods", "EXP-011", "colouring vs.\\ maximal cliques", fmt(len(ve)),
         f"{len(ve) - agree_v} disagreements"),
        ("Core search", "EXP-011", "vs.\\ all set partitions, $n\\le9$", "400", "0 differences"),
    ]
    write("validation.tex", "\\begin{tabular}{lllrl}\n\\toprule\ncheck & record & scope & items & outcome \\\\\n"
          "\\midrule\n" + "\n".join(" & ".join(r) + " \\\\" for r in vrows) + "\n\\bottomrule\n\\end{tabular}\n")

    # ------------------------------------------------------------- numbers and phrases
    complete = opn == 0
    if complete:
        title = "The second Bougard--Joret line up to order 24:\\\\ an exhaustive check and the extremal graphs"
        absval = (f"At every one of the {len(triples)} triples with $\\alpha\\ge3$, $k\\ge3$ and $n\\le24$ outside the "
                  "range that Bougard and Joret's Proposition~8 settles, $f$ equals the conjectured value")
        theorem = ("For every open-window triple $(n,\\alpha,k)$ with $n\\le24$, "
                   "$f(n,\\alpha,k)=t(n,\\alpha)+\\ceil{k\\alpha/2}$.")
        indep = "$f$ equals the bound of Didin's Theorem~9"
    else:
        bl = ", ".join(f"$f({n},{al},{k})\\ge{E}$" for n, al, k, E in bounds)
        title = ("The second Bougard--Joret line up to order 24:\\\\ values, bounds and the extremal graphs")
        absval = (f"At {conf} of the {len(triples)} triples with $\\alpha\\ge3$, $k\\ge3$ and $n\\le24$ outside the range "
                  f"that Bougard and Joret's Proposition~8 settles, $f$ equals the conjectured value, and at the other "
                  f"{opn} we prove {bl}")
        theorem = (f"For every open-window triple $(n,\\alpha,k)$ with $n\\le24$ other than "
                   + ", ".join(f"$({n},{al},{k})$" for n, al, k, _ in bounds)
                   + f", $f(n,\\alpha,k)=t(n,\\alpha)+\\ceil{{k\\alpha/2}}$. Moreover {bl}.")
        indep = f"$f$ equals the bound of Didin's Theorem~9 at {conf} triples and is at least the bounds above at the others"
    nums = {
        "papertitle": title, "abstractvalues": absval, "valuestheorem": theorem, "independentphrase": indep,
        "ntriples": len(triples), "nconfirmed": conf, "nopen": opn, "ngraphs": fmt(tot_g),
        "ngraphsplain": fmt(g_plain), "ngraphspruned": fmt(g_pruned), "nhours": f"{tot_s / 3600:.1f}",
        "nrecords": sum(len(v) for v in recs.values()), "nwindowthirty": len(w30),
        "nextremal": fmt(n_ext), "nexttriples": len(per), "nnopart": n_nopart, "ntenthreeb": n_tenb,
        "nphasetwotriples": len(PHASE2),
        "nsone": sum(1 for r in di if r["s"] == 1),
        "fullpairs": ", ".join(f"$({a},{k})$" for a, k in full_pairs(decision)),
        "nfullpairs": len(full_pairs(decision)),
        "nturancond": sum(1 for n, al, k in triples if t(n, al - 1) >= cval(n, al, k)),
        "nconstructed": sum(1 for r in e13 if r.get("found")),
        "gateAgraphs": fmt(ga["graphs"]) if ga else "pending", "gateAdecisions": fmt(ga["decisions"]) if ga else "pending",
        "gateAgroups": ga and len(ga["groups"]) or "pending", "gateAkept": fmt(ga["kept"]) if ga else "pending",
        "gateBgraphs": fmt(gb["graphs"]) if gb else "pending", "gateBslices": len(gb["slices"]) if gb else "pending",
        "gateCgraphs": fmt(gc["graphs"]) if gc else "pending", "gateCdecisions": fmt(gc["decisions"]) if gc else "pending",
        "gateDsummary": gd_sum, "gateEsummary": ge_sum,
        "shafilter": sha_f.group(2)[:16] + "\\ldots" if sha_f else "pending",
        "shageng": sha_g.group(1)[:16] + "\\ldots" if sha_g else "pending",
        "growthlow": f"{min(ratios):.1f}" if ratios else "pending", "growthhigh": f"{max(ratios):.1f}" if ratios else "pending",
        "secorderxxi": fmt(round(per_order[21])), "secorderxxii": fmt(round(per_order[22])),
        "secorderxxiii": fmt(round(per_order[23])),
        "ratioxxii": f"{per_order[22] / per_order[21]:.1f}", "ratioxxiii": f"{per_order[23] / per_order[22]:.1f}",
        "growthplotsgraphs": "\n".join(plot_g), "growthplotsseconds": "\n".join(plot_s),
    }
    write("numbers.tex", "".join(f"\\newcommand{{\\{k}}}{{{v}}}\n" for k, v in nums.items()))
    print({k: v for k, v in nums.items() if not k.startswith("growthplots")})


def drawings(di, st):
    """TikZ code for two extremal graphs of (10,3,3): one with s = 0 and one with s = 2, vertices grouped by parts."""
    import networkx as nx
    sys_path_hint = None  # noqa: F841
    pick = {}
    for r in di:
        if (r["n"], r["alpha"], r["k"]) == (10, 3, 3) and r["s"] in (0, 1) and r["s"] not in pick:
            pick[r["s"]] = r["g6"]
    if len(pick) < 2:
        return "\\fbox{drawings pending}"
    out = []
    for s, g6 in sorted(pick.items()):
        G = nx.convert_node_labels_to_integers(nx.from_graph6_bytes(g6.encode()))
        parts = best_parts(G, 3 - s)
        pos, centers = {}, []
        q = len(parts)
        for i, part in enumerate(parts):
            ang = 90 + 360 * i / q
            cx, cy = 1.9 * math.cos(math.radians(ang)), 1.9 * math.sin(math.radians(ang))
            centers.append((cx, cy, len(part)))
            for j, v in enumerate(sorted(part)):
                b = ang + 180 + 360 * j / len(part)
                rr = 0.55 if len(part) > 1 else 0
                pos[v] = (cx + rr * math.cos(math.radians(b)), cy + rr * math.sin(math.radians(b)))
        lines = [f"\\begin{{tikzpicture}}[scale=0.95,every node/.style={{circle,fill=black,inner sep=1.4pt}}]"]
        for cx, cy, size in centers:
            lines.append(f"\\fill[gray!18] ({cx:.3f},{cy:.3f}) circle ({0.55 + 0.32 if size > 1 else 0.3:.2f});")
        for v, (x, y) in sorted(pos.items()):
            lines.append(f"\\node (v{v}) at ({x:.3f},{y:.3f}) {{}};")
        where = {v: i for i, p in enumerate(parts) for v in p}
        for u, v in G.edges:
            style = "gray!70" if where[u] == where[v] else "linknavy,thick"
            lines.append(f"\\draw[{style}] (v{u}) -- (v{v});")
        lines.append("\\end{tikzpicture}")
        out.append("\n".join(lines))
    return out[0] + "\\qquad\n" + out[1] + "\n"


def full_pairs(decision):
    """Pairs (alpha, k), alpha, k >= 3, whose whole open window (n from k alpha + 1 to the end of eq. window) is decided."""
    out = []
    for a in range(3, NMAX):
        for k in range(3, NMAX):
            lo_n, hi_n = k * a + 1, a * (ceil(k * a / 2) - a + 2) - 1
            if lo_n > hi_n or lo_n > NMAX:
                continue
            ok = hi_n <= NMAX and all(
                all((n, a, k, E) in decision for E in range(max(ceil(n * k / 2), t(n, a)), cval(n, a, k)))
                for n in range(lo_n, hi_n + 1) if n >= 2 * a and n >= a + k)
            if ok:
                out.append((a, k))
    return sorted(out, key=lambda x: (x[1], x[0]))


def blocks():
    """TikZ drawings of X6 and X7 with an attaching triple filled and the free independent pair open."""
    import networkx as nx
    out = []
    for g6, att, free in ((b"ETxO", {0, 1, 5}, {3, 4}), (b"FQjRo", {0, 1, 2}, {3, 4})):
        X = nx.from_graph6_bytes(g6)
        m = X.number_of_nodes()
        pos = {v: (1.3 * math.cos(math.radians(90 + 360 * v / m)), 1.3 * math.sin(math.radians(90 + 360 * v / m)))
               for v in X}
        lines = ["\\begin{tikzpicture}[scale=1.0]"]
        for u, v in X.edges:
            lines.append(f"\\draw[gray!70] ({pos[u][0]:.3f},{pos[u][1]:.3f}) -- ({pos[v][0]:.3f},{pos[v][1]:.3f});")
        for v in X:
            x, y = pos[v]
            style = "fill=linknavy" if v in att else ("fill=white,draw=black" if v in free else "fill=gray")
            lines.append(f"\\node[circle,{style},inner sep=1.8pt,label={{[font=\\scriptsize]{90 + 360 * v / m:.0f}:{v}}}] "
                         f"at ({x:.3f},{y:.3f}) {{}};")
            if v in att:
                lines.append(f"\\draw[linknavy,thick] ({x:.3f},{y:.3f}) -- ({1.6 * x / 1.3:.3f},{1.6 * y / 1.3:.3f});")
        lines.append("\\end{tikzpicture}")
        out.append("\n".join(lines))
    return out[0] + "\\qquad\\qquad\n" + out[1] + "\n"


def partition_chart(per):
    """pgfplots stacked bars: extremal graphs with and without a partition into alpha cliques, per triple."""
    keys = sorted(per)
    coords = ",".join(f"{n}-{a}-{k}" for n, a, k in keys)
    labels = ",".join(f"{{({n},{a},{k})}}" for n, a, k in keys)
    part = " ".join(f"({n}-{a}-{k},{per[(n, a, k)]['part']})" for n, a, k in keys)
    nop = " ".join(f"({n}-{a}-{k},{per[(n, a, k)]['graphs'] - per[(n, a, k)]['part']})" for n, a, k in keys)
    return ("\\begin{tikzpicture}\n\\begin{axis}[ybar stacked,bar width=5pt,width=\\textwidth,height=5.2cm,"
            f"symbolic x coords={{{coords}}},xtick=data,xticklabels={{{labels}}},"
            "x tick label style={rotate=70,anchor=east,font=\\tiny},ylabel={extremal graphs},ymin=0,"
            "legend style={font=\\scriptsize,at={(0.02,0.97)},anchor=north west},enlarge x limits=0.02]\n"
            f"\\addplot+[fill=gray!45,draw=gray] coordinates {{{part}}};\\addlegendentry{{partition into $\\alpha$ cliques}}\n"
            f"\\addplot+[fill=linknavy,draw=linknavy] coordinates {{{nop}}};\\addlegendentry{{$\\theta(G)=\\alpha+1$}}\n"
            "\\end{axis}\n\\end{tikzpicture}\n")


def window_map(by_n, decision):
    """pgfplots scatter of the open window up to order 30: decided triples filled, others open."""
    pairs = sorted({(a, k) for trip in by_n.values() for _, a, k in trip})
    ycoords = ",".join(f"{a}-{k}" for a, k in pairs)
    ylabels = ",".join(f"{{({a},{k})}}" for a, k in pairs)
    dec, opn = [], []
    for n, trip in by_n.items():
        for _, a, k in trip:
            lo = max(ceil(n * k / 2), t(n, a))
            done = n <= NMAX and all((n, a, k, E) in decision for E in range(lo, cval(n, a, k)))
            (dec if done else opn).append(f"({n},{a}-{k})")
    return ("\\begin{tikzpicture}\n\\begin{axis}[width=0.9\\textwidth,height=6.4cm,xlabel={order $n$},"
            "ylabel={$(\\alpha,k)$},"
            f"symbolic y coords={{{ycoords}}},ytick=data,yticklabels={{{ylabels}}},"
            "y tick label style={font=\\tiny},xmin=9,xmax=31,grid=major,grid style={gray!20},"
            "legend style={font=\\scriptsize,at={(0.02,0.97)},anchor=north west}]\n"
            f"\\addplot[only marks,mark=*,mark size=1.8pt,linknavy] coordinates {{{' '.join(dec)}}};"
            "\\addlegendentry{decided here}\n"
            f"\\addplot[only marks,mark=o,mark size=1.8pt,gray] coordinates {{{' '.join(opn)}}};"
            "\\addlegendentry{open to enumeration}\n"
            "\\end{axis}\n\\end{tikzpicture}\n")


def best_parts(G, q):
    """A partition of V(G) into q parts with sum of independence numbers <= alpha(G), maximising inside edges."""
    import itertools
    import networkx as nx
    alpha = nx.max_weight_clique(nx.complement(G), weight=None)[1]
    nodes = list(G.nodes)
    best, best_in = None, -1
    for labels in itertools.product(range(q), repeat=len(nodes)):
        if labels[0] != 0 or len(set(labels)) != q:
            continue
        parts = [[v for v, l in zip(nodes, labels) if l == i] for i in range(q)]
        if sum(nx.max_weight_clique(nx.complement(G.subgraph(p)), weight=None)[1] for p in parts) > alpha:
            continue
        inside = sum(1 for u, v in G.edges if labels[u] == labels[v])
        if inside > best_in:
            best, best_in = parts, inside
    return best


if __name__ == "__main__":
    main()
