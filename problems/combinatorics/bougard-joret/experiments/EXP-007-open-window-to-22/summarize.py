"""EXP-007 summary: per triple, the edge counts completed, the lower bound proved and whether the conjectured value
was attained in the enumeration. Reads triples.json and artifacts/enum.jsonl; writes artifacts/summary.md.
"""
import json
from math import ceil
from pathlib import Path

HERE = Path(__file__).resolve().parent
triples = json.loads((HERE / "triples.json").read_text())
recs = {}
for line in (HERE / "artifacts" / "enum.jsonl").read_text(encoding="utf-8").splitlines():
    r = json.loads(line)
    recs[(r["n"], r["alpha"], r["k"], r["E"])] = r
rows, confirmed, open_ = [], 0, 0
for n, a, k, t, c in triples:
    lo, conj = max(t, ceil(n * k / 2)), t + c
    done = [E for E in range(lo, conj) if (n, a, k, E) in recs]
    below_clear = all(recs[(n, a, k, E)]["kept"] == 0 for E in done)
    complete = len(done) == conj - lo
    att = recs.get((n, a, k, conj))
    graphs = sum(recs[(n, a, k, E)]["generated"] for E in done)
    if complete and below_clear:
        status, value = "CONFIRMED", str(conj)
        confirmed += 1
    elif not below_clear:
        first = min(E for E in done if recs[(n, a, k, E)]["kept"])
        status, value = "COUNTEREXAMPLE", str(first)
    else:
        status, value = "OPEN", f">= {max(done) + 1 if done else lo}"
        open_ += 1
    rows.append(f"| ({n},{a},{k}) | {conj} | {lo} to {conj - 1} | {graphs:,} | "
                f"{'yes (' + str(att['kept']) + ')' if att and att['kept'] else ('no' if att else 'not run')} | "
                f"{value} | {status} |")
text = ("| triple | conjectured | edge counts | graphs searched below | attained at conjectured value (graphs) | "
        "value | status |\n|---|---:|---|---:|---|---:|---|\n" + "\n".join(rows) +
        f"\n\nConfirmed {confirmed} of {len(triples)}; open {open_}.\n")
(HERE / "artifacts" / "summary.md").write_text(text, encoding="utf-8", newline="\n")
print(text)
