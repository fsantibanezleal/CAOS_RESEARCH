# tau-conjecture: investigation log (append-only)

## 2026-08-01: problem opened; EXP-001 confirmed

- Full deep-research pass persisted
  (`context/2026-08-01-deep-research-dossier.md` + `context/references.md`):
  the conjecture statement pinned from the Buergisser 2024 survey (section
  4.6, eq. 4.5); Koiran 2004 read directly (tau conventions, easy/ultimately
  easy, DMS96/Moreira97 almost-all bounds, no nontrivial lower bound on
  tau(n!), Shamir division trick, VP0/VNP0 theorems); Markstroem 2014 read
  IN FULL (the experimental prior art: exhaustive census to length 11,
  exact tau'(n!) for n <= 28); 2024-2026 sweep (Buergisser 2024 survey,
  BBDM arXiv:2601.00387, Buergisser arXiv:2606.25121, ECCC tau tag) found
  no claimed resolution. Gap identified: no published census of
  z_max(tau) for the POLYNOMIAL side; adopted as the program's opening
  experimental surface.
- Program record written: plan (spine = census ladder; lenses 2/4/7/8/10
  active), backlog TCB-001..014, lenses pass file.
- **EXP-001 CONFIRMED** (hypothesis committed before run; 4.2 s wall):
  Stage A reproduces Markstroem's Figure 1 exactly at depths 1-7 (reached
  2, 4, 9, 26, 102, 562, 4363; intervals 2, 4, 6, 12, 40, 112, 310), so
  the enumerator is anchored to published ground truth. Stage B census is
  decision-complete for tau <= 4: z_max = 1, 2, 3, 3. New fact:
  **z_max(4) = 3**; no 4-gate constant-free program has 4 distinct integer
  roots. Depth-3 records are the sign/scale variants of x^3 - x; depth-4
  records add shifted consecutive triples (e.g. -x(x+1)(x+2)) and
  multiplicity-padded variants. 37 record polynomials at depth 4, all
  replay-verified.
- Exploration moment (methodology 11): recorded in
  `program/tau-conjecture/lenses-2026-08-01.md` (survey 4.6 as authority;
  Markstroem as method template; census-ladder analogy to the Jacobian
  program). New question minted: minimal tau with z_max = 4 (next census
  depth; candidate constructions at tau in {5,6}).
- Dead ends: none this round.
- State transition: scoped -> opened -> exploring (EXP-001 gate satisfied).

## 2026-08-01 (round 2): approaches evaluated; EXP-002 confirmed

- Rojas math/0304100 READ IN FULL: the p-adic Digit Conjecture (roots with
  first p-adic digit 1) implies the FULL tau conjecture (Thm 1); valuation
  spectrum s <= N_p(s) <= s(s+1)/2, p-independent, true growth open (Thm
  2, Newton-polygon proof transcribed); best additive-complexity root
  bound 1 + s^3(s+1)(7.5)^s s! (Thm 3); the real logistic root factory
  (2^j roots at tau O(j)) pinned [V]; its p-adic analogue recorded open.
- Approaches evaluation persisted (program/: approaches-evaluation file):
  six routes ranked; ADOPTED: census + dual set-function view (B1),
  p-adic valuation instrumentation (B2), composition-obstruction line
  (B3), addition-chain technique import (B4). Research-lines board RL-1..6
  written.
- tclib package created (enum cores, exact roots, 2-adic spectra) with a
  5-test suite anchored to Markstroem AND EXP-001 values; green.
- **EXP-002 CONFIRMED** (declared before run; 64 s): depth 5 exhausted
  (778,087 states); z_max(5) = 4; minimal tau for 4 distinct integer roots
  is exactly 5. Mechanism DISCOVERY: the 10 records are difference-of-
  squares splittings built on the Chebyshev-conjugate map x^2 - 2 (e.g.
  x^2 - (x^2-2)^2 = -(x-1)(x+1)(x-2)(x+2)), the integer shadow of the
  real-side root factory; the committed shifted-quadratic candidate ties
  but does not dominate. Observational: all records have 2-adic spectra
  {0,1} (roots pile into few valuation classes: the pressure sits on the
  digit-conjecture side at the bottom of the ladder).
- Wiki: 01-statement-and-history.md transcribed (dossier + Rojas read).
- Exploration moment: the two new views (dual set-function; valuation
  spectrum) plus the Chebyshev-shadow reading minted RL-4's concrete first
  question: how many iterations of the x^2-2 factory keep all roots
  integral, at what gate cost.
- Dead ends: none; the naive census is now compute-bound at depth 6
  (TCB-005 canonicalization is the declared prerequisite).
