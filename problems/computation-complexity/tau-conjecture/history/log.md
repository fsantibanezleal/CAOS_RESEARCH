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

## 2026-08-01 (round 3): tower lemma proved; last-gate scan; z_max(6) = 5

- **Chebyshev-tower obstruction PROVED** (context derivation note,
  machine-checked in tclib tests): integer periodic points of C = x^2-2
  are exactly {2,-1}; C^k(x) - x keeps 2 integer roots against 2^k real
  roots at tau <= 2k+2; the DOS tower G_k stalls at root set {0,+-1,+-2}
  for all k >= 2 (the integer preimage tree of C stabilizes: the escape
  bound |C(x)| >= |x|+1 for |x| >= 3 forces a finite stable core). The
  first RL-4 deliverable: the real-side factory formally contributes only
  a constant over Z.
- **Method: the last-gate lemma** (EXP-003 hypothesis): every tau = d+1
  polynomial is one gate over a normalized depth-d state; so z_max(d+1)
  is computable without storing the depth-(d+1) frontier. Its smoke gate
  caught a real accounting artifact (op-results equal to the free inputs
  counted as new; fixed, z-values unaffected).
- **EXP-003: census CONFIRMED, our prediction REFUTED.** Depth-5 frontier
  (778,087 states) scanned completely in 295 s: 134,494 new depth-6
  polynomials; z_max(6) = 5 (four records), NOT the predicted 4. The
  records are +-x^{1,2}(x^2-1)(x^2-4): the depth-5 DOS record times the
  input x: multiplying by x costs one gate and adjoins the root 0,
  reaching the stable core {0,+-1,+-2} at 6 gates (the tower needed 7).
  Minimal tau for 5 distinct integer roots = 6. Growth now z = tau - 1
  from tau = 3 on; whether depth 7 continues the law is the standing
  question, and it is BLOCKED on TCB-005 canonicalization (the depth-6
  frontier, ~20M states, is not stored).
- Audit: tclib vs sympy cross-check on 284 polynomials (all tau <= 3 +
  every stored record): zero mismatches.
- Wiki 02 (implication ladder) and 03 (census) transcribed; references
  updated (Rojas READ in full; Duke access attempt failed: paywall,
  logged; Malajovich UP added).
- Dead ends: the Shub-Smale Duke PDF remains inaccessible without a
  library credential (statement triply confirmed through Rojas, the
  survey, and Koiran).

## 2026-08-01 (rounds 4-5): monic stall theorem; family towers; z_max(7) = 5

- Sweeps: Cheng 2004 pinned (conditional subexponential tau'(n!) with a
  randomized construction); SAT-based exact synthesis identified as a
  new lane (Fuhs-Schneider-Kamp, linear/GF(2); integer model untried);
  adelic tau conjecture (Phillipson-Rojas arXiv:1011.4128) pinned; the
  ARITHMETIC-DYNAMICS view minted (V8: stall cores are preperiodic-type
  sets; Morton-Silverman / Doyle-Poonen uniform boundedness is the
  mature frame; no prior application to tau mechanisms found). New
  views V5-V8; research lines RL-7 (SAT), RL-8 (moves calculus), RL-9
  (parameterized towers).
- **Monic stall theorem PROVED** (TCB-020 note + machine spot-check):
  for ANY monic h of degree >= 2, single-map towers have depth-
  independent integer root counts (escape radius + stabilizing preimage
  core): no such family can ever witness superpolynomial z vs tau.
- **EXP-005 CONFIRMED** (load-bearing claim; 3.4 s after a root-finder
  fix: divisor counting is infeasible on c^{2^k}-scale constants; the
  independently proved escape bound |r| <= c+1 gives exact direct
  evaluation, cross-checked vs the divisor method at small c): across
  h_c = x^2 - c, c <= 200, max tower yield = 5, ONLY at c = 2: the
  family loophole is EMPTY. DISCOVERY where the hypothesis flagged
  uncertainty: a second series c = m^2+m+1 yields 4 via genuine integer
  2-CYCLES (m -> -m-1 -> m); explained and closed by the classical
  cycle-length <= 2 divisibility argument: fixed, anti-fixed and
  2-cycles are the COMPLETE harvestable inventory over Z.
- **EXP-004 CONFIRMED** (86.5 min: 17 min to build the depth-6 frontier
  EXACTLY: 25,844,905 states, all gates green; 69 min to scan it):
  z_max(7) = 5. The bottom law z = tau - 1 BREAKS at 7 (second plateau;
  sequence 1,2,3,3,4,5,5). 2,013,706 depth-7 polynomials; 63 have five
  roots, none more. Minimal tau for 6 roots is in [8, 9]. This was our
  committed prediction (made after the EXP-003 humiliation), now
  machine-decided.
- Wiki: 04 mechanisms transcribed (+ family/cycle-ceiling section);
  03 census updated with the full table and plateaus reading.
- Exploration yield of the rounds: the plateaus phenomenon (constant-
  building friction is now VISIBLE in the growth function); the [8,9]
  window as the first SAT-lane target; RL-9 resolved for quadratics.
- Dead ends: naive census at depth 8 is out of single-machine reach
  (frontier ~10^9 states); declared routes: proved canonicalization,
  compiled/parallel backend, or SAT-lane targeted decisions.

## 2026-08-01 (round 6): the census manuscript, published

- Manuscript gate (TCB-022) judged PASSED and executed per the standing
  rule: the census paper was written (manuscripts/tau-conjecture/census/,
  8 pages, transcribed from the EXP-001..005 verdicts and the two
  derivation notes, front-matter per methodology 05), built (two-pass
  pdflatex, page-1 + interior visually checked), and PUBLISHED on Zenodo
  via the DOI-prereserve flow: version DOI 10.5281/zenodo.21753439,
  concept DOI 10.5281/zenodo.21753438, CC-BY-4.0, v0.01, record live
  (HTTP 200 verified). Both refuted predictions and the EXP-005 tooling
  incident are disclosed in the paper; every claim is labeled MV/D/C
  with a verdict trace.
- Ledger: vault manuscripts/tau-conjecture/ (zenodo.json, sources.json,
  deposits.json) + both manuscripts READMEs updated.
- Next: the [8,9] window (TCB-021).
