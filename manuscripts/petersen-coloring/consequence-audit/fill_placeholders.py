"""Fill the two EXP-010 placeholders of main.tex (file to file, no shell strings)."""

import io
from pathlib import Path

HERE = Path(__file__).resolve().parent
BS = chr(92)
s = io.open(HERE / "main.tex", encoding="utf-8").read()
graphs = "$" + BS + "Gfty$, $" + BS + "Gftyb$ and $" + BS + "Gsix$"
counts = "482, 482 and 4{,}947"
assert s.count("%%POLE_GRAPHS%%") == 1 and s.count("%%POLE_COUNTS%%") == 1
s = s.replace("%%POLE_GRAPHS%%", graphs).replace("%%POLE_COUNTS%%", counts)
old = "pairs, or the four edges adjacent to one edge of $" + BS + "PG$."
assert s.count(old) == 1
new = (old + " Adjacent labels are always available at the two ends of a deleted edge (all 73 4-poles of $"
       + BS + "Gfty$ containing a fixed deleted edge), so such 4-poles can be chained around a ring. Ten dot products of $"
       + BS + "Gfty$ with itself, cubic graphs on 102 vertices, have no Petersen coloring (checked proofs) and defect exactly~2.")
s = s.replace(old, new)
io.open(HERE / "main.tex", "w", encoding="utf-8", newline="\n").write(s)
print("filled")
