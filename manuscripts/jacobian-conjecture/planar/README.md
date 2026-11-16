# manuscript-planar/ - the PLANAR PROGRAM paper (B of three)

`main.tex` / `main.pdf`: "Planar Keller Maps after the Counterexample: Weight-Class Exclusions, a Chart
Atlas for the (72,108) Reduction, and Independent Checks of Cases 1 and 2". The
ACTIVE paper: the JC(2) machine (uniform closure, forced tops, descent), the four
unconditional exclusion theorems (with complete proofs, and the scope of each stated) plus the
annihilation lemma, the diagonal corner and the staircase transport (with the fifth exclusion in window
form, at all partner degrees on its six certified grid shapes, and the half-plane certificates as window
results with propagation conjectured),
the matched-pair law and the x^m-anchored edge operator, and the source-audited frontier
(gcd coverage; Moh/GGHV floors; the B = 16 normal form and the (72, 108) pair as live
targets), including the EXP-095/096 original-pair gates (seven possible nonzero inner
vertices and exact resultant intersection number 21 with root partition 84+24) and the
EXP-097 transport audit (absolute degree is not typed after Laurent localization without
a boundary-divisor ledger), and the EXP-098--108 constructible-certificate
route, including the first complete exact augmented-minor chart cover on an
actual three-coefficient GGHV slice and its global lower-family mod-9 grading,
followed by the EXP-111 full-family rank correction, the EXP-112 exact
36-column cyclic-core compression, the EXP-114 weighted residual factors,
and the EXP-115--130 weighted-chart campaign: the complete quotient boundary
is closed, a first open chart makes all three selected component
intersections finite, a third chart closes the \(G\) component, and one
shared residual-selected basis closes both finite \(L/Q\) strata. The
complete three-parameter \(T_B\) restriction is therefore closed. The first
restored direction \((2,9)\) gives the exact higher-dimensional reduction
\(A^{87}(R(A^3,B)+A^2CS(A^3,B))\), with primitive coefficient gcd one.
An alternative minor covers a dense open of that graph and leaves three
factor curves. Exact recursion on the linear-in-\(X\) factor reduces its
principal-open residual to degree \(9+15=24\), or 72 lifted algebraic
points. The same exact minor reduces the quadratic-in-\(X\) \(F_6\) curve
through a degree-74 function-field norm. Exact boundary classification leaves
only irreducible factors of degrees 18 and 30 on \(AS\ne0\): 48 normalized
values, or 144 lifted algebraic points. A distinct \(F_7\) section has a
degree-58 norm; after exact boundary classification, irreducible degrees
3, 9, and 18 survive: 30 normalized values and 90 lifts. No
positive-dimensional factor curve remains on the graph chart. Exact CRT
analysis identifies two repeated geometric blocks, reducing the union from
102 factor appearances to 75 normalized points. The existing (h_7) section
covers the unique degree-15 and degree-30 blocks, and two newly reconstructed
maximal minors generate the unit ideal on the remaining (F_7) blocks of
degrees 3, 9, and 18. The complete (AS\ne0) rational graph is therefore
closed. EXP-130 decomposes the principal-open base locus into reduced field
blocks of degrees 3, 6, 12, and 69, total dimension 90, and certifies a
finite maximal-minor atlas uniformly in (Y=A^2C). The complete (A\ne0)
sector of the declared four-parameter restriction is closed. EXP-131 returns
to the original augmented matrix at (A=0) and gives two exact
(C)-independent minors whose (B)-divisors have unit gcd. Together with the
separate (d=0) cover, the declared four-coefficient restriction is closed.
EXP-132 then adds the transverse direction (2,8) and closes the complete
direct (A=0,d=1) boundary of the declared five-coefficient restriction with
three exact maximal minors generating the unit ideal in QQ[B,C,T]. The new
SCC-guided basis is essential because the inherited EXP-123/124 bases vanish
identically on this direct specialization. EXP-135 then proves the stronger
ambient identity `det(H+T K_(2,8))=det(H)` for the accepted EXP-124 section.
The exact certificate uses rank degrees (25,24,6,7), 136,500 complete grid
controls across 30 primes, and a CRT product above an explicit coefficient
bound. The old `F3*F6*F7` divisor is therefore retained for this section. The
other (A nonzero,d=1) sections and transverse (d=0) quotient remain open, so the
five-coefficient restriction, 24-parameter core, and full family remain open. Grows
per session; content moved here from `manuscript/` in the 2026-07-22 split
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

Manuscript version in preparation: **v0.38** (2026-11-16; its version DOI and checksum are set at release). Last published version: **v0.37**, published 2026-11-15 at version DOI `10.5281/zenodo.24240037`
(concept DOI `10.5281/zenodo.21503367`; 51 pages, 722,853 bytes, SHA-256
`f8fea6a7ba16ddf43e51133de4097416633e6a33d9b0c2785ca06313f06f3dd4`): the full revision (methods with six
algorithms, complete proofs, related work, the atlas, exclusion and frontier tables, six figures, and the
(72,108) part restructured around GGHV Proposition 4.3 with Cases 1 and 2). v0.36: `10.5281/zenodo.24226225`. Substantive revisions are published as new Zenodo
versions under the concept DOI.

Generated pieces: `make_tables.py` writes `tab_atlas.tex`, `tab_repro.tex` and `fig_times.tex` from the
experiment records (it refuses a cell whose quotation is absent from its record); run it before building.
Build with three `pdflatex` passes.
