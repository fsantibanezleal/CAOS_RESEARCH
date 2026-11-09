"""Summarise the completed parts of order-13 case A (EXP-004 + EXP-006): parts with a recorded .err only."""
import sys
from collections import Counter
from pathlib import Path

P = Path(sys.argv[1])
done = sorted(P.glob("p*.err"), key=lambda f: int(f.stem[1:]))
read = mnh = 0
graphs = []
summary = []
for f in done:
    a = f.read_text().split()
    read += int(a[1])
    mnh += int(a[5])
    summary.append(f"{f.stem} {' '.join(a)}")
    t = f.with_suffix(".txt").read_text().splitlines()
    graphs += [l for l in t if l.strip()]
missing = sorted(set(range(2000)) - {int(f.stem[1:]) for f in done})
print(f"parts complete {len(done)} of 2000; graphs read {read:,}; MNH {mnh}; graph lines {len(graphs)}")
print("hoa flags:", Counter(l.split()[3] for l in graphs), "circumference:", Counter(l.split()[1] for l in graphs))
print(f"missing parts: {len(missing)} (first {missing[:5]}, last {missing[-5:]})")
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
(out / "mnh-n13-caseA-partial.txt").write_text("\n".join(graphs) + "\n", encoding="utf-8", newline="\n")
(out / "parts-summary.txt").write_text("\n".join(summary) + "\n", encoding="utf-8", newline="\n")
(out / "missing-parts.txt").write_text(" ".join(map(str, missing)) + "\n", encoding="utf-8", newline="\n")
