"""Assemble main.tex of this manuscript from its parts (abstract.tex, body-sections-*.tex).

The parts are kept in separate files so that no LaTeX ever passes through a shell string. A line
%%PART:name.tex%% in a body part is replaced by the content of that file: the tables and figures
written by make_tables.py (run it first), and results-theorem.tex.
Usage: python assemble.py [--draft]   (writes main.tex, or draft.tex with --draft)
"""

import io
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BS = chr(92)
BODY_PARTS = ("body-sections-1-3.tex", "body-sections-4-6.tex", "body-sections-7-13.tex")


def main() -> None:
    skeleton = io.open(HERE / "skeleton.tex", encoding="utf-8").read()
    body = "\n".join(io.open(HERE / name, encoding="utf-8").read() for name in BODY_PARTS)
    abstract_path = HERE / "abstract.tex"
    if abstract_path.exists():
        abstract = io.open(abstract_path, encoding="utf-8").read()
    else:
        abstract = BS + "begin{abstract}\nDraft.\n" + BS + "end{abstract}\n"
    for _ in range(3):
        for name in sorted(set(re.findall(r"%%PART:([A-Za-z0-9_.-]+)%%", body))):
            body = body.replace("%%PART:" + name + "%%", io.open(HERE / name, encoding="utf-8").read())
    out = skeleton.replace("%%ABSTRACT%%", abstract).replace("%%BODY%%", body)
    if "%%" in out.replace(BS + "%", ""):
        left = [line for line in out.splitlines() if "%%" in line]
        print("placeholders left:", left)
    target = HERE / ("draft.tex" if "--draft" in sys.argv else "main.tex")
    io.open(target, "w", encoding="utf-8", newline="\n").write(out)
    print("wrote", target.name, len(out))


if __name__ == "__main__":
    main()
