# manuscript/ - findings and approaches, LaTeX + PDF

`main.tex` is the working manuscript mapping all validated findings and approaches of the
program; `main.pdf` is the built copy committed per release.

Build (MiKTeX or any TeX distribution):

```powershell
pdflatex -interaction=nonstopmode main.tex; pdflatex -interaction=nonstopmode main.tex
```

Rules (methodology/05): findings enter only after adversarial validation; every claim is labeled
[MV] machine-verified, [D] derived (instance-certified), or [C] conjecture.
