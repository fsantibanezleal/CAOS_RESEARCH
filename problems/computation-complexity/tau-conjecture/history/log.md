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
