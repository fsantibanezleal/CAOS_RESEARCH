# Research lines and the multi-front execution plan (2026-07-24)

Per Felipe's directive (2026-07-24) and methodology/11 (new form): the program runs
MULTIPLE FRONTS concurrently: sequential deep reasoning on the active front while
heavy background tasks (long computations, multi-day runs) advance the others.
Results on any front can redirect or invalidate others; the fronts are re-evaluated
at every round close. Control stays single-threaded (one session, one verdict at a
time); only COMPUTE is parallel.

## Front A: the tropical lane (ACTIVE; Felipe's explicit GO for n = 6)

- A1 (EXP-004, running): valuation + equation-variant screening at n = 4/5.
  Interim signal (11/16 cells): powers-of-3 is the ONLY globally pointed valuation;
  squares/pow2/primes show exactly 2 positive unbounded directions each (comet-level
  analysis needed, as in JL25's squares case); arithmetic/repeated controls are
  junk-heavy; S2 (dropping the 10 dependent symmetric equations) is catastrophically
  unpointed everywhere (316+ positive directions): the symmetric equations do heavy
  tropical work.
- A2 (comet instrument): exact per-component pointedness (union-find over maximal
  cones; exact separating-hyperplane certificates in Fractions). gfan's _components
  app crashes on our output format (bad_alloc; recorded); we implement our own.
- A3 (EXP-005, NEXT; Felipe's GO received): the n = 6 prevariety attempt. Evidence
  so far says: system S1 (with symmetric equations), valuation family = powers of 3
  ((1, 3, 9, 27, 81, 243) first). ~2.8 wall-days background at JL25 scale; launched
  as a background run while other fronts advance; abort/redirect criteria declared
  in its hypothesis.
- A4 (n = 4 pure-polyhedral generic replication): falls out of EXP-004's n = 4 cells.

## Front B: the census engine (msolve)

- B1: build/install msolve in WSL (hashes recorded); B2: EXP-006-class: P2 completion
  on the capped samples + the n = 4 equal-mass PLANAR census (4 classes ground
  truth); sympy stays the independent verification layer (HM06's own
  Mathematica-checked-by-Macaulay2 pattern).

## Front C: the manuscript + Zenodo (evidence timestamping)

- C1: draft manuscript NOW (enough validated content exists): "Exact replication and
  screening of tropical finiteness certificates for central configurations"
  (working title): EXP-001/002 calibration story (dimension-blindness; enrichment
  law), EXP-003 exact JL25 reproduction, EXP-004 screening + the S2 finding.
  Honest replication framing; only [V]-tagged references; no invented data; every
  number traceable to a committed artifact. LaTeX in problems/.../manuscript/.
- C2: Zenodo upload per methodology/09 (CC-BY, API flow from _CAOS_MANAGE/tools/
  zenodo/; autonomous publish authorized, Felipe reviews after; updates as NEW
  VERSIONS). Timestamped priority evidence.

## Front D: the web surface + release

- D1: frontend problem page for central-configurations (structure per
  methodology/06; content transcribed from wiki/verdicts; EN/ES; claims verbatim).
- D2: the RELEASE step (version bump + CHANGELOG + bake + build + tag + PR
  develop -> main) per methodology/08: SERIALIZED: verify the jacobian session is
  not mid-release before starting; if in doubt, keep committing rounds.

## Front E: reads and lenses (the exploration stream)

- E1: Sun-Xie-You (arXiv:2510.25649) full read (gate for the Hessian instrument,
  CCB-014; treats our exact anchors). E2: AK12 full anatomy (CCB-023). E3:
  Chang-Chen tables (CCB-004). E4: Roberts continuum PDF (CCB-006, anatomy lens).

## Interaction rules (control)

- One verdict at a time; every front's results land as EXP records or dossiers
  before they steer another front.
- A front's negative result can invalidate another front's premise: recorded at
  round close in this file (dated addenda), RESUME, and the mirror.
- Statement-level claims, outreach, and multi-day compute beyond the standing GO
  (the n = 6 run is covered by Felipe's 2026-07-24 GO) go to Felipe first.
