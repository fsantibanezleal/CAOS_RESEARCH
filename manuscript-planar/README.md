# manuscript-planar/ - the PLANAR PROGRAM paper (B of three)

`main.tex` / `main.pdf`: "Planar Keller Maps after the Counterexample: Machine-Certified
Newton-Polygon Exclusions, the Staircase Transport, and the Recalibrated Frontier". The
ACTIVE paper: the JC(2) machine (uniform closure, forced tops, descent), the four
unconditional exclusion theorems plus the annihilation lemma, the diagonal corner and the
staircase transport (with the fifth exclusion in window form and its cleared certificates),
the matched-pair law and the x^m-anchored edge operator, and the source-audited frontier
(gcd coverage; Moh/GGHV floors; the B = 16 normal form and the (72, 108) pair as live
targets). Grows per session; content moved here from `manuscript/` in the 2026-07-22 split
(see `manuscript/README.md` for the three-paper structure).

Positioning discipline: novelty claims follow the adversarial literature pass
(`problems/algebraic-geometry/jacobian-conjecture/context/2026-07-22-literature-pass-dossier.md`);
replication-status labels are mandatory for literature-covered certificates; Felipe
validates the novelty phrasing before any submission.

Build:

```powershell
pdflatex -interaction=nonstopmode main.tex; pdflatex -interaction=nonstopmode main.tex
```

Rules (methodology/05): [MV] / [D] / [C] labels on every claim; findings enter only after
adversarial validation.
