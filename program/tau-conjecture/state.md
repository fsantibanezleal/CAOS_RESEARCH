# Shub-Smale tau conjecture: state (heartbeat)

- **State:** exploring (opened 2026-08-01; scoped 2026-07-20).
- **Done (2026-08-01, opening round):** deep-research pass; program record;
  **EXP-001 CONFIRMED** (Markstroem anchor 14/14; z_max(1..4) = 1,2,3,3).
- **Done (2026-08-01, round 2):** Rojas read in full; approaches
  evaluation + research lines RL-1..6; tclib + tests; **EXP-002
  CONFIRMED** (z_max(5) = 4; DOS/Chebyshev-shadow mechanism; spectra
  {0,1}); wiki 01.
- **Done (2026-08-01, round 3):** **Chebyshev-tower lemma PROVED** (RL-4:
  C^k(x)-x keeps 2 integer roots vs 2^k real; DOS towers stall at
  {0,+-1,+-2}; machine-checked). **Last-gate lemma** shipped in tclib
  (z_max one depth past any exhausted frontier, memory-light; its smoke
  gate caught and fixed an input-accounting artifact). **EXP-003: census
  CONFIRMED, prediction REFUTED**: z_max(6) = 5 via
  +-x(x^2-1)(x^2-4) (the depth-5 record times x: one gate adjoins root
  0); minimal tau for 5 roots = 6; 134,494 depth-6 polynomials; growth
  law so far z = tau - 1 from tau = 3. sympy cross-check 284/284. Wiki
  02/03 transcribed; references updated (Duke original still paywalled).
- **Now:** round closed; nothing running.
- **Next:** TCB-005 canonicalization (sign/reflection orbit quotient +
  dominated-state pruning, proofs first) or a compiled backend: the
  depth-7 question (does z_max(7) = 6?) is BLOCKED on it; TCB-016
  generalization (single-inner-map stall lemma for x^2 - c); RL-3 T(S)
  structure lemmas; wiki 04.
