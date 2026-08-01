# 02 - The known-results ladder (state of the art, verified 2026-07-23)

Transcribed from `../context/2026-07-23-deep-research-dossier.md` (per-claim verification
tags there; [U] items may not carry conclusions).

## Finiteness results

| Case | Status | Who / how |
|---|---|---|
| $n = 3$ | 5 CCs, all masses (closed since 1772) | Euler + Lagrange; Moulton for the collinear count |
| collinear, any $n$ | exactly $n!/2$ classes | Moulton 1910 |
| $n = 4$ planar | FINITE for ALL positive masses; count in $[32, 8472]$ | Hampton-Moeckel, Invent. Math. 163 (2006) 289-312: Albouy-Chenciner equations + BKK theory + exact computer computation (THE machine-assisted precedent). Reproved without computer by Albouy-Kaloshin 2012 |
| $n = 5$ planar | FINITE except perhaps for masses in an explicit codimension-2 subvariety | Albouy-Kaloshin, Ann. of Math. 176 (2012) 535-588 (abstract fetched verbatim). Equal masses LIE IN the exceptional subvariety; settled separately by Moczurad-Zgliczynski 2019; further exceptional cases closed by Moczurad-Zgliczynski, arXiv:2601.01165 (2026) |
| $n = 5$ spatial | generic finiteness (Dziobek): Moeckel, Trans. AMS 353 (2001); explicit exceptional mass conditions: Hampton-Jensen, CMDA 109 (2011), tropical geometry (Gfan + Singular/Sage) | machine-assisted, exact |
| $n = 6$ planar | OPEN. The programme preprint states verbatim: 117 candidate zw-diagrams from the first algorithm, 31 eliminated by the second, mass relations found for 62 by the third (one impossible for positive masses), "leaving 24 cases unsolved" | Chang-Chen, J. Symbolic Comput. 123 (2024) 102277 (part I); programme preprint arXiv:2303.02853, pages 1-6 read directly 2026-08-01 (PDF archived with SHA-256) |
| $n = 6$ planar, CROSS symmetric stratum (four bodies on the symmetry axis, mirror pair off it; the symmetry forces $m_5 = m_6$) | generically FINITE: off a proper closed mass subset (their theorem statement misprints "open"; the proof constructs a closed set); same result for the six-vortex analogue | Dias-Pan, arXiv:1811.08681 (2018), read in full 2026-08-01: Laura-Andoyer equations (linear in masses), block-triangular Jacobian, fiber-dimension theorem, partial-Groebner dimension bounds, explicit witness configuration |
| $n \ge 7$ planar | FULLY OPEN, even generic finiteness | Moeckel, Lectures (Sect. 14-15) |
| Dziobek CCs, homogeneous potentials | generic finiteness + uniform bound $2^{O(n^2)}$; 8192 for $n = 4$ | T. Dias, arXiv:2601.07962 (2026) |
| negative masses | FALSE: an explicit continuum of 5-body relative equilibria with one negative mass | Roberts, Physica D 127 (1999) 141-145; positivity is necessary |

## Rigorous counts (equal masses, planar, mod rotation + reflection + permutation)

| n | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|
| classes | 2 | 4 | 5 | 9 | 14 |

Moczurad-Zgliczynski, CMDA 2019 (arXiv:1812.07279; interval arithmetic + Krawczyk
operator; counts extracted by us from the paper's appendix report files, PDF read).
Every one has a reflection symmetry line; asymmetric CCs exist for $n = 8, 9, 10$
(existence proofs, same paper; full listing infeasible for $n \ge 8$ with their method:
the box count grows exponentially; $n = 7$ took about 100 hours).

Additional 4-body knowledge: 50 classes under rotation-only equivalence for equal masses
(Simo 1978, numerical); every 4-equal-mass CC has a reflection symmetry (Albouy 1995,
1996, computer-assisted classification); a convex noncollinear CC exists for every
ordering of any 4 positive masses (MacMillan-Bartky); degenerate CCs occur at
bifurcation masses (Palmore).

## Structural anchors

- **Shub 1970**: normalized CCs stay away from collisions (compactness); an infinite
  family must accumulate on a non-isolated CC inside the torus of positive distances.
- **Positivity is load-bearing**: Roberts' continuum shows the finiteness conjecture is
  a statement about positive masses specifically.
- **Every modern proof is an exclusion argument** over the Albouy-Chenciner polynomial
  system: see [03-method-machinery.md](03-method-machinery.md).
