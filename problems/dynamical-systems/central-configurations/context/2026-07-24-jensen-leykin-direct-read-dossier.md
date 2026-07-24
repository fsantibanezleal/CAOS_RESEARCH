# Direct-read dossier: Jensen-Leykin, Smale's 6th problem for generic masses

Date: 2026-07-24. Source: arXiv:2301.02305v2 (12 Aug 2025), 7 pages, READ IN FULL;
PDF archived at `E:\_Datos\caos-research\central-configurations\papers\` (copy of the
tool-fetched file; add SHA-256 at next artifact pass). Authors: Anders Jensen (Aarhus;
the Gfan author; HJ11 co-author) and Anton Leykin (Georgia Tech). Backlog CCB-024:
READ DONE; the actionable program it opens is recorded below.

## The method (complete)

1. **Conjecture 1**: for generic masses, the number of normalized central
   configurations of the n-body problem over ANY field of characteristic 0 is finite
   ("generic" = off a hypersurface in mass space).
2. **Equations** (their Section 2.2; matches our cclib inventory): the (n-1)n
   asymmetric Albouy-Chenciner equations $g_{i,j} = \sum_k m_k S_{i,k}(r_{jk}^2 -
   r_{ik}^2 - r_{ij}^2)$ with $S_{i,j} = r_{ij}^{-3} - 1$ (the asymmetric form is due
   to Roberts, PERSONAL COMMUNICATION 2009: this pins HJ11's "(Roberts, 2009)" [U]
   flag: not a paper, a communication); the (n-1)n/2 symmetric $f = g_{ij} + g_{ji}$;
   and the $\binom{n}{4}$ planar Cayley-Menger determinants. Distances-only,
   normalization S = r^{-3} - 1 (one representative per scaling orbit).
3. **The tropical move**: work over the Puiseux field $K = \mathbb{C}\{\{t\}\}$ and
   SPECIALIZE THE MASSES to elements with chosen VALUATIONS. Key facts: Bieri-Groves
   (dim T(X) = dim X); a tropical variety of positive dimension contains a balanced
   tropical curve; the recession cone of a component containing a tropical curve
   cannot be pointed (their Prop. 1); and fibers of tropicalization are Zariski dense
   (Payne), so ONE valuation point's conclusion spreads to almost all masses.
4. **The computation**: the tropical PREVARIETY of the system (which contains T(V(F)))
   is computed with gfan 0.7's dynamic decomposition (Jensen, ICMS 2024); the
   components ("comets") are inspected; if every recession cone is POINTED, there is
   no balanced curve, T(V(F)) is 0-dim, V(F) is 0-dim over K, and generic finiteness
   follows. ONLY POLYHEDRAL COMPUTATIONS; no Groebner elimination, no mass-eliminant
   ideals ("in contrast with [AK12, HJ11, HM06], no other polynomials than those in
   the original equations are derived").
5. **n = 5 proof**: system = 10 symmetric AC + 20 asymmetric AC + 5 Cayley-Menger;
   mass valuations (1, 4, 9, 16, 25): prevariety f-vector
   (3586, 12012, 18531, 15625, 7072, 1357), 257 connected components, ALL comets
   pointed: generic finiteness (confirming AK12 generically). 80 cpu-minutes
   (5 wall-clock minutes on 16 threads; overflow-checked integer rerun ~10x longer).
   Valuations (1, 3, 9, 27, 81): f-vector (1506, 4744, 8586, 8787, 4652, 993) with a
   GLOBALLY pointed recession cone (component analysis unnecessary). Valuations
   (0, 1, 2, 3, 4) FAIL (not all pointed).
6. **Reproducible commands (verbatim in the paper)**: `gfan _nbody -N5 --masses
   --alsosymmetric --cayleymenger2` piped through sed substitutions $m_i \mapsto
   t^{3^{i-1}}$ into `gfan _tropicalprevariety --usevaluation -j16 --mint --minx`
   (with --bits64 for speed). gfan ships a BUILT-IN _nbody generator. gfan at
   math.au.dk/~jensen/software/gfan/gfan.html.
7. **Special cases are HARDER for this method** (their 4.2): equal or symmetric
   valuations (e.g. (0,0,0,0) at n = 4, or (a,a,b,b,c) at n = 5) fail to conclude:
   the method's power comes from GENERIC (separated) valuations; "there is more hope
   for our methodology in the general case n = 6 than in special cases of n = 5".
8. **The n = 6 state (their 4.3)**: they ran the analogous prevariety for one
   valuation choice: ~100 cpu-days (about three days on 35 threads); the recession
   cones of the connected components were NOT all pointed: INCONCLUSIVE. Verbatim
   call to action: "more experimentation with different valuations or different
   versions of the Albouy-Chenciner equations is needed." They note Chang-Chen's
   symbolic attempt "for now ... fails as well".

## Why this matters to our program (recalibration)

- **A live, compute-shaped frontier**: generic Smale 6 at n = 6 currently hinges on
  (a) finding a valuation vector and (b) an equation-system variant for which the
  n = 6 prevariety comes out pointed, at ~100-cpu-day scale per try. Both knobs are
  exactly our kind of surface:
  - our EXP-002 P1 result (asymmetric-G enrichment collapses degenerate components at
    n = 3, and HM06 needed Dziobek enrichment at n = 4) is a small-scale instance of
    "different versions of the AC equations" shrinking tropical junk; quantifying
    which enrichments (G, Dziobek, e_IU) shrink the PREVARIETY at n = 4, 5 is a cheap,
    novel, publishable experiment with direct n = 6 leverage;
  - a systematic valuation-search at n = 5 (which valuation classes succeed/fail, and
    WHY, e.g. separation growth rates) is cheap (minutes per try) and would give a
    principled shortlist for n = 6 tries instead of blind 100-cpu-day shots.
- **Instrument decision reinforced**: wrap gfan (their exact commands) rather than
  hand-rolling prevariety code; validate on BOTH published f-vectors above and on
  HJ11's (1, 576, 1620, 1420, 450).
- **Novelty discipline**: generic-mass finiteness claims are Jensen-Leykin territory;
  our potential contributions there are valuation/equation-variant experiments and
  scale engineering, clearly attributed; the ALL-masses question (exceptional sets)
  remains the complementary lane (AK12/Chang-Chen/MZ26 style).

## New backlog rows

- CCB-029: install gfan 0.7 (WSL; record binary + hash), reproduce the JL25 n = 5
  one-liner, validate both published f-vectors; then HJ11's spatial prevariety.
- CCB-030: valuation-search experiment series at n = 5 (systematic families:
  powers, squares, primes, near-degenerate; map success/failure; hypothesis-first).
- CCB-031: equation-variant prevariety shrinking at n = 4, 5 (with/without G /
  Dziobek / e_IU; measure f-vectors and pointedness; the EXP-002 P1 phenomenon at
  prevariety level).

## Reference pins

Roberts asymmetric equations = personal communication (2009) [V: JL25 ref list];
Jensen, Dynamic decomposition of tropical prevarieties for celestial mechanics,
ICMS 2024, Springer, 313-321 [V]; Payne, Fibers of tropicalization, Math. Z. 262
(2009) 301 [V]; Groves-Bieri, J. reine angew. Math. 347 (1984) 168-195 [V];
Maclagan-Sturmfels GSM 161 [V]; Smale, Math. Intelligencer 20(2) (1998) 7-15
[V: pinned again by JL25's list].
