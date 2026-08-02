# EXP-017c - Mod-p triage of the loci systems, then one long honest run

Declared: 2026-08-02, BEFORE any run. Successor to EXP-017/017b per their
verdicts.

## Method

SCREEN (mod-p, SCREEN-ONLY per the standing soundness rule; a mod-p
dimension is never verdict-carrying because unlucky primes can enlarge
leading ideals): take the EXACT archived Singular scripts of EXP-017's four
full loci systems (height formulation, integer-cleared) and EXP-017b's base
ideal, change ONLY the ring characteristic (primes 32003 and 1073741789),
run each at 300 s. Mod-p Groebner cost is a strong feasibility predictor
for characteristic zero: a rung that walls mod p is hopeless over QQ at any
human budget; a rung that flies mod p earns the long run.

DECISION RULE (declared now): if at least one loci rung completes mod p at
both primes, the cheapest such rung gets ONE detached QQ run at a 6-hour
declared cap (a NEW budget, not an extension); if NONE completes, the
Groebner route to the loci bounds is closed at human budgets in both
formulations, and the chain's remaining path is the Prop 7.2-style
sign-analysis lemma (Groebner-free) plus, for the k = 4 case, either the
witness hunt (EXP-018b, a less symmetric CC) or a declared multi-day run.

## Predictions

- P1: the screen itself completes (10 runs x 300 s worst case) and yields a
  clean feasibility table (complete / cap per cell, with mod-p dims recorded
  as screen data only).
- P2 (calibrated guess, honestly uncertain): the height-formulation Delta_4
  rung (13 minors, the smallest system) completes mod p; no confidence is
  attached to the others.

## Preflight

- Source-complete: reuses archived artifacts byte-for-byte except the ring
  line; the screen-only rule was pinned in EXP-012's hypothesis and binds
  here.
- Smoke: none needed beyond the reuse itself (the scripts ran syntactically
  clean over QQ in EXP-017 after the serializer fix).
- One-sidedness: an all-caps screen is a decisive negative with a declared
  consequence; a mixed screen picks the long-run target mechanically.
- Budget and kill: screen 10 x 300 s; then at most ONE 6-hour QQ run,
  detached, whose own verdict lands in a later round. No extensions.
