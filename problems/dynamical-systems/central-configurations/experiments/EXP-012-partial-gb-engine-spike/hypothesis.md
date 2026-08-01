# EXP-012 - The partial-GB engine spike (CCB-037 v2): Singular over QQ against the measured wall

Declared: 2026-08-01, BEFORE any run. Backlog: CCB-037 v2, gating the n = 6
symmetric-strata campaign and the n = 5 retry.

## Question

Is EXP-011's instrument wall an engine artifact? Concretely: does Singular
over QQ complete the SAME subideal Groebner computations that sympy walled on
(1 of 15 at 120 s), and does an enlarged-but-lighter subideal menu then push
the union leading-term bound for the n = 5 spatial Dziobek cut to the expected
d_pgb <= 4?

## Engines, with the soundness subtlety stated up front

- Singular 4.3.2 (Ubuntu 24.04 package; binary SHA-256
  90ab699b7a28486944a167e797d7c8dd38f8f949960b93ee7a6d08ff1c7c46f4) over QQ,
  degrevlex (`dp`), `lead(std(I))`. VERDICT-GRADE: leading monomials of a QQ
  Groebner basis of a subideal are members of the full ideal's leading-term
  ideal (Dias-Pan Lemma 6.4 logic), so the union bound is rigorous.
- msolve `-g 1` prints the leading ideal "for first prime characteristic",
  i.e. MOD P. An unlucky prime can ENLARGE the leading ideal, which would fake
  a LOWER dimension bound. Therefore msolve's mod-p leading ideals are
  SCREEN-ONLY in this program (cross-checks, menu triage), never
  verdict-carrying. This is recorded here before any run so the rule cannot
  bend later.
- sympy stays the verification layer: control agreement plus exponent-level
  parsing checks of every harvested lead.

## Predictions

- P1 (controls): (a) on the toy ideal {x^2 - y, y^2 - x} the three engines
  (sympy QQ, Singular QQ, msolve mod a recorded large prime) agree on the
  leading ideal {x^2, y^2}; (b) on EXP-011's ONLY completing subideal (job 3,
  whose 16 QQ leading monomials are archived in pgb-union.json), Singular
  reproduces EXACTLY the same 16 exponent vectors. Any mismatch stops the
  experiment.
- P2 (the A/B engine test, the heart of the spike): Singular over QQ, fed the
  IDENTICAL 15 subideal jobs archived by EXP-011 (loaded from the pgb-job
  files, no rebuild), completes AT LEAST 12 of 15 within 120 s each. sympy's
  measured baseline is 1 of 15. Per-subideal wall times are recorded; the
  speedup is the experiment's headline number.
- P3 (menu v2, lighter and wider): sixteen new subideals, all in Singular at
  120 s caps: five "local Dziobek" subideals (the three pairings of ONE
  quadruple + saturation, no Cayley-Menger), ten "adjacent pair" subideals
  (the _ab products of two quadruples sharing three bodies + saturation), and
  one {Cayley-Menger, saturation} subideal. At least 12 of 16 complete.
- P4 (the target): the union of ALL completing harvests (P2 + P3) yields
  d_pgb <= 4 for the n = 5 spatial Dziobek cut. Declared thresholds: <= 4 is
  the deterministic match of the expected dimension; 5 to 8 is
  informative-weak (recorded, menu grows to triples next); anything above 8
  means the menu structure, not the engine, is the obstruction.

## Preflight (methodology/12)

- Source-complete: Dias-Pan read in full (their Singular usage and Lemma 6.4);
  msolve -g semantics read from its own help text today; Singular validated on
  the toy control this morning. No [U] premise.
- Smoke: P1 IS the gate; no menu time is spent if either control fails.
- One-sidedness: P2 can refute (Singular capping too would kill the engine
  hypothesis and push the deterministic rung entirely to witness sets or
  out-of-scope engines); P4 can land weak, which is an honest menu
  measurement.
- Invariant-first: per-subideal wall time per engine, and d_pgb; these are the
  cost forecasters for the 9-variable strata quotients.
- Budget and kill: 31 subideal runs x 120 s = 62 min worst case, plus
  controls; no cap extensions. If BOTH controls pass but fewer than 6 of the
  31 runs complete, the spike is REFUTED-BY-CAP and CCB-034 carries the lane
  alone.

## Consequence ladder

- P2 + P4 land: CCB-037 v2 is the working deterministic upper-bound
  instrument; the k = 2, p = 2 stratum campaign (9-variable quotients) and
  the Chang-Chen n = 4 relation re-derivation get declared next, in that
  order.
- P2 lands, P4 weak: menu grows (triples, mixed pairings) in a follow-up with
  its own declaration; the strata campaign can still proceed on Dias-Pan's
  precedent since their workload is the 11-variable analogue of our quotients.
- P2 refuted: the engine story ends here; witness sets only.
