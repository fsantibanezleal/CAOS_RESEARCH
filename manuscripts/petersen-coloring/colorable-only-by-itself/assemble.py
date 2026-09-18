"""Assemble main.tex of this manuscript from its parts (abstract.tex, body-sections-*.tex).

The parts are kept in separate files so that no LaTeX ever passes through a shell string.
Usage: python assemble.py [--draft]   (writes main.tex, or draft.tex with --draft)
"""

import io
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BS = chr(92)


def main() -> None:
    skeleton = io.open(HERE / "skeleton.tex", encoding="utf-8").read()
    body = io.open(HERE / "body-sections-1-3.tex", encoding="utf-8").read() + "\n" + io.open(HERE / "body-sections-4-6.tex", encoding="utf-8").read()
    abstract_path = HERE / "abstract.tex"
    if abstract_path.exists():
        abstract = io.open(abstract_path, encoding="utf-8").read()
    else:
        abstract = BS + "begin{abstract}\nDraft.\n" + BS + "end{abstract}\n"
    for name, tag in (("results-theorem.tex", "%%RESULTS_THEOREM%%"), ("results-table.tex", "%%RESULTS_TABLE%%")):
        part = HERE / name
        if part.exists():
            body = body.replace(tag, io.open(part, encoding="utf-8").read())
    out = skeleton.replace("%%ABSTRACT%%", abstract).replace("%%BODY%%", body)
    if "%%" in out.replace(BS + "%", ""):
        left = [line for line in out.splitlines() if "%%" in line]
        print("placeholders left:", left)
    target = HERE / ("draft.tex" if "--draft" in sys.argv else "main.tex")
    io.open(target, "w", encoding="utf-8", newline="\n").write(out)
    print("wrote", target.name, len(out))


if __name__ == "__main__":
    main()
