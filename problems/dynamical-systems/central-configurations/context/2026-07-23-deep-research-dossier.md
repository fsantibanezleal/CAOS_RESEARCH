# Deep research dossier: finiteness of central configurations (Smale's 6th problem)

Date: 2026-07-23. Status: opening pass for the problem (scoped -> exploring).
Verification discipline: every claim below is tagged. [V] = verified against the primary
source listed (fetched and read during this pass), [Vs] = verified against two or more
independent secondary sources including at least one paper PDF read directly, [U] =
UNVERIFIED (recalled or single-source; must be re-verified before any conclusion depends
on it). Full bibliography with per-item flags: `references.md`.

## 1. The problem

**Statement (Smale's 6th problem).** Given $n$ point masses $m_1, \dots, m_n > 0$, is the
number of planar central configurations (equivalently, relative equilibria of the Newtonian
$n$-body problem), up to the symmetries of rotation, translation, scaling (and optionally
reflection and relabeling), finite for every choice of the masses? [Vs: Smale,
Math. Intelligencer 20 (1998) 7-15, cited as [Sm98] in Moczurad-Zgliczynski (CMDA 2019,
arXiv:1812.07279, PDF read) and in Chang-Chen (arXiv:2303.02853); the verbatim wording of
Smale's problem 6 text is [U] until we read the Intelligencer paper itself.]

A **central configuration (CC)** for masses $m_1,\dots,m_n$ is a configuration
$x = (x_1, \dots, x_n)$, $x_i \in \mathbb{R}^d$, satisfying

$$\lambda\,(x_i - c) = \sum_{j \ne i} \frac{m_j (x_j - x_i)}{r_{ij}^3}, \qquad i = 1, \dots, n$$

for some constant $\lambda$, where $c$ is the center of mass and $r_{ij} = |x_i - x_j|$.
[V: Moczurad-Zgliczynski 2019, eq. (2), PDF read; Moeckel, Lectures on Central
Configurations, Definition 1, PDF read; sign conventions differ across sources.]
Equivalently $\nabla U(x) + \lambda M (x - c) = 0$ with $U = \sum_{i<j} m_i m_j / r_{ij}$,
and then $\lambda = U(x)/I(x) > 0$ with $I$ the moment of inertia about $c$;
$I(x) = \frac{1}{m}\sum_{i<j} m_i m_j r_{ij}^2$ when $\sum m_i x_i = 0$ [V: Moeckel notes
eqs. (8)-(10); MZ19 Lemma 3]. In the plane every CC generates a relative equilibrium (the
configuration rotating rigidly at angular velocity $\omega = \sqrt{\lambda}$) and
homographic/elliptic families; released from rest a CC collapses homothetically [V: MZ19
Section 1 and 2; Moeckel notes Section 3].

History of the finiteness question: raised by Chazy (Bull. Astron. 35 (1918) 321-389
[Vs: cited in Moeckel notes references]) and Wintner (The Analytical Foundations of
Celestial Mechanics, Princeton 1941 [Vs: cited in MZ19 as [W41] and in Moeckel notes]);
Smale made it problem 6 of his 18 problems for the 21st century [Vs].

Why finiteness is the right question: the CC equations are polynomial (after clearing
denominators), so the solution set is an algebraic variety; failure of finiteness means a
positive-dimensional component of physically admissible solutions, which would be a
degenerate continuum of steady motions. Morse-theoretic and topological-lower-bound
programs (Smale, Palmore, Pacella) need nondegeneracy or at least finiteness to count
[V: Moeckel notes Section 11].

## 2. The known-results ladder (verified state of the art, July 2026)

| n / setting | Result | Source | Tag |
|---|---|---|---|
| n = 3, planar | Exactly 5 CCs for all positive masses: 3 collinear (Euler 1767, one per ordering) + 2 equilateral (Lagrange 1772, two orientations). In unlabeled mutual-distance space: 1 equilateral class + 3 collinear classes. | Euler, Lagrange; uniqueness per ordering: Moulton's theorem covers the collinear count | [V: Moeckel notes Sections 9-10 (shape sphere: "five critical points"); Hampton-Jensen CMDA 109 (2011), intro, PDF read] |
| collinear, any n | Exactly one normalized collinear CC per ordering of the masses: $n!/2$ collinear classes. Moulton 1910. | Moulton, Ann. of Math. 1910 (cited); proof in Moeckel notes Prop. 18 | [V: Moeckel notes, PDF read] |
| n = 4, planar | FINITE for ALL positive masses; the number is between 32 and 8472. Computer-assisted proof, exact symbolic/integer computations, BKK (Bernstein-Khovanskii-Kushnirenko) theory over the Albouy-Chenciner equations. THE machine-assisted precedent for this program. | Hampton-Moeckel, Invent. Math. 163 (2006) 289-312, DOI 10.1007/s00222-005-0461-0 | [Vs: abstract quoted by Springer landing page via search; "finite for all positive masses, at most 8472" confirmed in Moeckel notes, PDF read; MZ19 intro confirms "for any system of positive masses ... with computer assistance". Bound pair (32, 8472) [Vs]; we have not yet read the Inventiones PDF itself: full method transcription in the companion method dossier, from Hampton-Jensen 2011 which states "Our proof strategy will be the same as that of Hampton and Moeckel (2006)"] |
| n = 4, planar, second proof | Finiteness reproved WITHOUT computer assistance. | Albouy-Kaloshin, Ann. of Math. 176 (2012), same paper as n = 5 | [V: MZ19 intro, PDF read] |
| n = 5, planar | FINITE except perhaps if the 5-tuple of positive masses belongs to an explicitly given codimension-2 subvariety of mass space. | Albouy-Kaloshin, Ann. of Math. 176 (2012) 535-588, DOI 10.4007/annals.2012.176.1.10 | [V: Annals abstract fetched verbatim 2026-07-23] |
| n = 5, the exceptional set | EQUAL MASSES BELONG to the Albouy-Kaloshin exceptional subvariety (so AK12 does not cover the equal-mass quintuple); the equal-mass case is settled separately (finite, fully listed) by MZ19. Several more exceptional mass sets settled 2026. | MZ19 intro ("It is interesting to notice that the equal masses case treated in our paper belongs to this subvariety"); Moczurad-Zgliczynski, arXiv:2601.01165 (Jan 2026) | [V: MZ19 PDF read; 2601.01165 abstract fetched] |
| n = 5, spatial (Dziobek) | Moeckel 2001: generic finiteness for Dziobek configurations (nonplanar spatial 5-body CCs). Hampton-Jensen 2011: finiteness for all positive masses EXCEPT an explicitly listed finite set of polynomial mass conditions (their Table 1), via tropical geometry (Gfan) + exact computations (Singular, Sage). | Moeckel, Trans. AMS 353 (2001) 4673-4686; Hampton-Jensen, Cel. Mech. Dyn. Astron. 109 (2011) 321-332 | [V: HJ11 PDF read in full front matter; Moeckel 2001 cited consistently in MZ19 + HJ11 + Moeckel notes] |
| n = 5, negative mass | Roberts 1999: a CONTINUUM of relative equilibria exists in the 5-body problem if one mass is allowed to be negative (four unit masses plus one negative mass; the family persists for similar potentials including the vortex logarithmic potential). Mass positivity is NECESSARY for finiteness. | Roberts, Physica D 127 (1999) 141-145 | [Vs: abstract summary via ADS/scispace search + cited in HJ11 intro and Moeckel notes ("Roberts has an example involving masses of different signs"); the exact negative value (recalled as -1/4) is [U]] |
| n = 6, planar | OPEN. Chang-Chen 2023-2025 (symbolic computation program on the Albouy-Kaloshin zw-diagram framework): at most 117 zw-diagrams could carry a failure of finiteness; their algorithms eliminate 31, then 62 more except for masses satisfying explicit relations; 24 diagram cases remain unresolved, involving masses in codimension >= 2 subvarieties. Two published parts: (I) J. Symbolic Computation 2024 (diagrams and orders); (II) SIAM J. Appl. Dyn. Syst. 24(3) (2025) 2369-2404 (mass relations). | Chang-Chen, arXiv:2303.02853; JSC (DOI: S0747717123000913); SIADS 24(3):2369-2404 | [V: arXiv abstract + fetch summary (117/31/62/24); journal split confirmed by search results; the per-diagram detail is [U] until we read the two published parts in full] |
| n = 6, 7 planar equal masses | FINITE and fully listed (computer-assisted, interval arithmetic + Krawczyk operator): n = 5: 5 classes, n = 6: 9 classes, n = 7: 14 classes (up to rotation, reflection, permutation; masses equal). Every one has a reflection symmetry line. For n = 3: 2 classes, n = 4: 4 classes (same equivalence). | Moczurad-Zgliczynski, CMDA 2019 (arXiv:1812.07279) | [V: counts extracted directly from the paper's appendix report files, PDF read: "Number of different cc" = 2, 4, 5, 9, 14 for n = 3, 4, 5, 6, 7] |
| n = 8, 9, 10 equal masses | Existence of CCs WITHOUT any reflection symmetry (asymmetric CCs exist; Simo had found 2 asymmetric families for n = 9 numerically). Full rigorous listing INFEASIBLE for n >= 8 with their method (dimensionality curse; n = 7 took ~100 h, each added body multiplies boxes by ~4e4). | MZ19 Theorem 2 + Section 1 | [V: PDF read] |
| n = 5, 6 spatial equal masses | Full rigorous listing (same toolchain, spatial). | Moczurad-Zgliczynski, arXiv:2006.06768 | [Vs: abstract via search; details [U]] |
| n >= 7, general masses | FULLY OPEN, even generic finiteness ("But for n > 5 even generic finiteness is open", Moeckel notes; Chang-Chen partial program covers n = 6 only). | Moeckel notes Section 14-15 | [V: PDF read] |
| Dziobek CCs, any n, homogeneous potentials | Generic finiteness + uniform upper bound $2^{O(n^2)}$; for n = 4 the bound improves 8472 to 8192. Veronese/determinantal geometry, Bezout-type counts. | Thiago Dias, arXiv:2601.07962 (Jan 2026) | [V: abstract fetched] |
| n = 4 counts (finer) | Simo 1978: numerical census of 4-body CC counts across mass space (equal masses: 50 classes up to rotation only; 4 classes adding reflections + permutations). Albouy 1995/1996: every CC of 4 EQUAL masses has a reflection symmetry; complete computer-assisted classification. MacMillan-Bartky: existence of a convex noncollinear CC for every ordering of 4 arbitrary positive masses. Palmore: degenerate CCs occur for some 4-body masses (bifurcations of the count). | Simo, Cel. Mech. 18 (1978) 165-184; Albouy, C. R. Acad. Sci. 320 (1995) 217-220; Albouy, Contemp. Math. 198 (1996) 131-135; MacMillan-Bartky (cited in Moeckel notes [23]); Palmore (Moeckel notes Section 10) | [V: the 50-vs-4 statement and citations from MZ19 PDF; MacMillan-Bartky + Palmore from Moeckel notes PDF] |
| n = 4 convex uniqueness | Uniqueness of the convex CC per ordering: long-conjectured; a 2023 Regular and Chaotic Dynamics paper claims a proof ("On the Uniqueness of Convex Central Configurations in the Planar 4-Body Problem"). | RCD 2023, DOI 10.1134/S1560354723520076 | [U: search hit only; must read before use] |

Structural facts that gate any attack:

- **Shub's compactness lemma**: normalized CCs stay away from collisions; the set of
  normalized CCs for fixed masses is compact. So an infinite family would have to
  accumulate on a non-isolated CC, not escape to a collision or to infinity.
  [Vs: Shub 1970, "Diagonals and relative equilibria", Springer LNM 197, 199-201, cited
  in MZ19 as [Sh70]; mechanism restated in Moeckel notes Section on finiteness.]
- **Mutual-distance formulation**: CCs are characterized among distance vectors by the
  Albouy-Chenciner equations (polynomial in $r_{ij}$ after clearing denominators), plus
  Cayley-Menger realizability/rank conditions for the target dimension. This is the
  formulation every finiteness proof since 2005 uses. [V: HJ11 Section 3 gives the exact
  polynomial forms; see the method dossier.]
- **Dziobek configurations** (dim = n - 2: collinear 3-body, planar noncollinear 4-body,
  spatial nonplanar 5-body) admit a special determinantal structure; this is why n = 4
  planar and n = 5 spatial fell first and why Dias 2026 can bound them uniformly.
  [V: Moeckel notes Definition 6 + Section 12.]
- **Degeneracy is real**: Palmore showed degenerate CCs occur for open sets of 4-body
  masses at bifurcation values, so naive Morse counting fails at exceptional masses; any
  exact-count claim must handle mass-dependence. [V: Moeckel notes Section 10.]

## 3. Certification and computation stack (for our pipeline)

- **BKK bounds / mixed volumes**: the HM06 instrument; bound the number of isolated
  toric solutions by the mixed volume of Newton polytopes; finiteness follows if no
  positive-dimensional components survive in the torus. [Vs: HM06 via HJ11 + Moeckel notes.]
- **Tropical geometry**: HJ11's reformulation: a positive-dimensional component in the
  torus forces a nonzero vector in the tropical variety with $\sum \omega_i \ge 0$;
  compute the tropical prevariety (Gfan) and kill every candidate ray/cone by exact
  initial-ideal computations (Singular/Sage, saturation, Groebner over $\mathbb{Q}(m)$).
  f-vector for their 42-equation spatial 5-body system: (1, 576, 1620, 1420, 450);
  44 cases after symmetry; two "troublesome rays" needed bespoke elimination.
  [V: HJ11 PDF read.]
- **Krawczyk operator + interval arithmetic**: MZ19's instrument for rigorous full
  listings at fixed masses: compact search region from a priori bounds (lower bound on
  distances, upper bound on configuration size), binary search with exclusion tests,
  Krawczyk for existence + local uniqueness on the surviving boxes. Cost grows
  exponentially with n. [V: MZ19 PDF read, Sections 3-7.]
- **Smale's alpha theory**: certified Newton convergence from data at a point; the
  certification route for homotopy-continuation output. alphaCertified implements it in
  exact rational arithmetic (Hauenstein-Sottile, ACM TOMS 38(4) 2012, Algorithm 921,
  arXiv:1011.1091). Note the aesthetic: Smale's own machinery certifying computations on
  Smale's problem. [Vs: arXiv + TOMS listing via search.]
- **Interval/Krawczyk certification in HomotopyContinuation.jl**: Breiding-Rose-Timme,
  "Certifying zeros of polynomial systems using interval arithmetic" (arXiv:2011.05000;
  ACM TOMS 2023): the modern default for certifying nonsingular solutions of square
  systems; certified homotopy tracking via Krawczyk: arXiv:2402.07053. [Vs: search hits
  + docs pages; not yet exercised by us.]
- **MZ19 source code** is published (C++ with their own interval tools; version 1.1,
  link in the paper: ww2.ii.uj.edu.pl/~zgliczyn/papers/publ.htm). [V: reference [MZ19]
  in the paper's bibliography, PDF read.]
- **Normalization-free comparator**: $J = U I^{1/2} / (\sum m_i)^{5/2}$ is scale- and
  normalization-invariant; MZ19 use it (their eq. (66)) to match CCs across papers with
  different normalizations. Adopt it in our artifacts. [V: MZ19 PDF read.]

## 4. Gaps, opportunities, and where a machine-first program can move

1. **Reproduction rung (calibration)**: nobody's exact pipeline is public end-to-end for
   the HM06 planar 4-body certificate in open tooling (their computations were bespoke;
   HJ11's Sage worksheet exists for the spatial 5-body). Reproducing HM06's certificate
   objects (the AC polynomial system, its Newton polytopes, the BKK count, the
   torus-component exclusions) in an exact, replayable, CI-guarded pipeline is a real
   contribution and the toolchain shakedown. Target artifacts are all known in advance
   (finite, between 32 and 8472), so every step is checkable.
2. **The n = 6 frontier is 24 named cases**: Chang-Chen have reduced planar n = 6
   finiteness to 24 zw-diagram cases with explicit mass relations (codim >= 2). This is
   exactly the shape of problem our jacobian program handles well: a finite, explicit
   list of exclusion targets, each a polynomial elimination problem, attackable with
   exact Groebner/resultants + modular (mod p) preprocessing (the modfrac instrument)
   + GPU-parallel numerical landscaping certified a posteriori. The list must first be
   transcribed exactly from the two published parts.
3. **Equal masses first on every rung**: equal masses are simultaneously (a) the
   physically canonical case, (b) INSIDE the AK12 exceptional variety for n = 5 (so
   genuinely delicate), and (c) fully certified for n <= 7 planar (MZ19), giving us
   ground truth to calibrate against at n = 5, 6, 7.
4. **The spatial ladder** (Dziobek route): Moeckel 2001 generic; HJ11 explicit for
   n = 5; Dias 2026 uniform bounds for homogeneous potentials. A machine reproduction
   of HJ11's tropical certificate (their Sage worksheet is published) is a second
   calibration target, and the Dziobek determinantal structure is the natural wedge for
   any new n = 6 spatial statement.
5. **Null results are publishable here**: the program's methodology (append-only record,
   adversarial refutation, honest verdicts) fits a problem whose modern history is
   precisely a sequence of machine-checked exclusions.

## 5. Risks and honesty constraints

- The heavy rungs (BKK mixed volumes in 6+ variables, tropical prevarieties of
  40-equation systems) need instruments we have not built in Python; budget rungs
  explicitly (mixed volume: exact convex geometry over $\mathbb{Q}$; prevariety:
  polyhedral computation; both feasible but nontrivial; external binaries like Gfan are
  a fallback that must then be wrapped reproducibly in the repo toolchain).
- Several load-bearing literature items are still [U] at open time: the verbatim Smale
  problem text, the Roberts mass values, the HM06 internals (we work from HJ11's
  restatement until the Inventiones PDF is read), the Chang-Chen per-diagram tables, the
  2023 convex-uniqueness claim. Each gets re-verified before any conclusion depends on it.
- Equal-mass results (MZ19) rely on directed rounding in C++; our reproduction must
  either re-implement rigorous rounding or use exact rational Krawczyk (slower, smaller
  boxes) and say which.
