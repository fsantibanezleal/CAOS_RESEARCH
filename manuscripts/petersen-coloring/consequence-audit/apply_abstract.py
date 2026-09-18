"""Replace the abstract of main.tex by abstract-v003.tex (file to file, no shell strings)."""

import io
from pathlib import Path

HERE = Path(__file__).resolve().parent
BS = chr(92)
s = io.open(HERE / "main.tex", encoding="utf-8").read()
new = io.open(HERE / "abstract-v003.tex", encoding="utf-8").read().rstrip("\n")
a = s.index(BS + "begin{abstract}")
b = s.index(BS + "end{abstract}") + len(BS + "end{abstract}")
s = s[:a] + new + s[b:]
io.open(HERE / "main.tex", "w", encoding="utf-8", newline="\n").write(s)
print("abstract replaced")
