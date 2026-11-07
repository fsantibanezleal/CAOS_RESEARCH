"""Build table.tex for the second-regime note from the EXP-005, EXP-006 and EXP-007 enumeration records.

For every open second-regime triple with n <= 22 (the EXP-005/006/007 lists), the conjectured value, the edge
counts searched below it, the number of candidate graphs searched there, and the number of qualifying graphs found
at the conjectured value (or the attaining construction when that count was not enumerated).
"""
import json
from math import ceil, comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXP = HERE.parents[2] / "problems" / "combinatorics" / "bougard-joret" / "experiments"
SOURCES = ["EXP-005-second-regime-small", "EXP-006-second-regime-beyond-15", "EXP-007-open-window-to-22"]


def t(n, a):
    q, r = divmod(n, a)
    return r * comb(q + 1, 2) + (a - r) * comb(q, 2)


recs = {}
for s in SOURCES:
    for line in (EXP / s / "artifacts" / "enum.jsonl").read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        key = (r["n"], r["alpha"], r["k"], r["E"])
        # keep the record with the most graphs read per key is not needed; kept counts agree across methods
        recs.setdefault(key, (r, s))
triples = []
for a in range(3, 12):
    for k in range(3, 12):
        for n in range(k * a + 1, 23):
            if n >= 2 * a and n >= a + k and n // a <= ceil(k * a / 2) - a + 1:
                triples.append((n, a, k))
triples.sort(key=lambda x: (x[0], x[1], x[2]))
rows, ok = [], 0
total_graphs = 0
for n, a, k in triples:
    conj = t(n, a) + ceil(k * a / 2)
    lo = max(ceil(n * k / 2), t(n, a))
    below = [recs.get((n, a, k, E)) for E in range(lo, conj)]
    missing = [E for E, r in zip(range(lo, conj), below) if r is None]
    # EXP-005 searched from ceil(nk/2), possibly below t(n, a); count every searched record below conj
    searched = [r for (nn, aa, kk, E), r in recs.items() if (nn, aa, kk) == (n, a, k) and E < conj]
    found_below = sum(r[0]["kept"] for r in searched)
    graphs = sum(r[0]["generated"] for r in searched)
    total_graphs += graphs
    att = recs.get((n, a, k, conj))
    att_s = str(att[0]["kept"]) if att and att[0]["kept"] else "construction"
    status = "yes" if not missing and found_below == 0 else ("COUNTEREXAMPLE" if found_below else "OPEN")
    ok += status == "yes"
    gstr = f"{graphs:,}".replace(",", "{,}")
    if status == "yes":
        fstr = str(conj)
    elif found_below:
        fstr = "\\textbf{" + str(min(E for (nn, aa, kk, E), r in recs.items()
                                     if (nn, aa, kk) == (n, a, k) and r[0]["kept"])) + "}"
    else:
        fstr = "$\\ge" + str(min(missing)) + "$"
    rows.append(f"$({n},{a},{k})$ & {t(n, a)} & {fstr} & {lo}--{conj - 1} & {gstr} & {att_s} \\\\")
body = ("\\begin{tabular}{lrrrrr}\n\\toprule\n$(n,\\alpha,k)$ & $t(n,\\alpha)$ & $f$ & edges searched & graphs below & "
        "extremal graphs \\\\\n\\midrule\n" + "\n".join(rows) + "\n\\bottomrule\n\\end{tabular}\n")
(HERE / "table.tex").write_text(body, encoding="utf-8", newline="\n")
nums = (f"\\newcommand{{\\ntriples}}{{{len(triples)}}}\n\\newcommand{{\\nconfirmed}}{{{ok}}}\n"
        f"\\newcommand{{\\ngraphs}}{{{total_graphs:,}}}\n".replace(",", "{,}", 0))
nums = nums.replace(f"{total_graphs:,}", f"{total_graphs:,}".replace(",", "{,}"))
(HERE / "numbers.tex").write_text(nums, encoding="utf-8", newline="\n")
print(f"{len(triples)} triples; equal to the formula with complete search: {ok}; graphs searched below: {total_graphs:,}")
