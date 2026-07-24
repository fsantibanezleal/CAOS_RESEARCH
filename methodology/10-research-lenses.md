# 10 - Research lenses: complementary approaches for every problem

Adopted 2026-07-24 (Felipe's directive). Our systematic path is an EXCLUSION
engine: constrain a hypothetical object until it contradicts itself, degree by
degree, with declared hypotheses and exact verification. That spine is not
replaced. But every problem is attacked more powerfully when the spine is
complemented by several other LENSES. This file is a reusable toolkit: at a
problem's plan stage, enumerate which lenses apply, run the spine plus at least
two others, and record in the problem's RESUME which lenses were tried and what
each produced.

The organising insight (from the Jacobian program, 2026-07-24): a problem's
"does X exist / is Y true" almost always has a dual pair of attacks - EXCLUSION
(prove the object cannot exist / the property must hold) and ANATOMY +
RECOGNITION (understand the one known object and decide whether its class can
occur in the target regime). Running both, and letting each inform the other, is
the multiplier. Our Jacobian exclusion sweeps and the Tao-style incidence /
recognition-of-affine-space derivation are the two faces; combined, they gave a
one-line exclusion (EXP-089) that neither alone would have found.

## The lens catalog

Each lens: what it is, when to reach for it, what it produces.

1. EXCLUSION / OBSTRUCTION (the spine). Assume the object, derive constraints
   (invariants, gradings, certificates) until contradiction. When: always, as the
   backbone. Produces: verifiable floor progress, exclusion theorems, decidable
   per-case results. Limit: an unbounded ladder; rarely an all-degrees theorem.

2. ANATOMY / CONSTRUCTION. Take the ONE known example/counterexample/extremal
   object and reverse-engineer its intrinsic structure (its mechanism, its
   invariant description). When: whenever an example exists. Produces: the "why it
   exists", the mechanism, the class the example belongs to - which the exclusion
   lens can then target.

3. RECOGNITION / CLASSIFICATION. Reframe "does X exist" as "is this object in a
   CLASSIFIED family / isomorphic to a known model?" (affine-space recognition,
   surface classification, ADE, finite simple groups, holonomy lists). When: when
   a direct search is unbounded but the ambient objects are classified. Produces:
   DECIDABILITY where the spine only gives per-case results (in the Jacobian: dim
   2 surface recognition is a theorem; dim 3 is the open miracle).

4. INVARIANT. Compute one distinguishing/forcing invariant - units, class group,
   Picard, Betti/Euler, weights, discriminant, degree, MakarLimanov. When: to kill
   or force a class in one line. Produces: one-line exclusions (units killed the
   dim-2 incidence variety, EXP-089). Cheapest high-leverage move; try FIRST.

5. SYMMETRY / REPRESENTATION THEORY. Find the group acting (torus, SL2, Weyl,
   Galois), decompose into weights/orbits, use equivariance and normal forms.
   When: when the objects carry a natural group action. Produces: "why these
   coefficients", reductions to normal forms, rigidity theorems (our
   G_m-equivariant rigidity is exactly this lens).

6. THE TWO-SIDED READING. Every exclusion computation is a construction attempt
   read backwards: finding the certificate excludes; PROVING none exists is
   evidence the object is consistent - a construction skeleton. When: always ask
   "what does the FAILURE of my exclusion build?" Produces: a Bayesian signal on
   which way the answer goes, and a bridge to the anatomy lens.

7. REFORMULATION / DICTIONARY. Translate into an equivalent problem in another
   field and import its tools (Jacobian <-> Dixmier/Weyl algebra;
   non-properness <-> Jelonek set; a recursion <-> a flat connection / regularity
   type; a count <-> a cohomology). When: when the native tools stall. Produces:
   whole toolkits from the target field; sometimes decidability.

8. DIMENSION / PARAMETER LADDER. Study the family across n (or degree, genus,
   rank...) and locate WHERE the phenomenon is exceptional and WHY. When: to
   understand what is special about the target case. Produces: the structural
   reason the target differs (Jacobian: n=3 is the unique unimodular / linear-core
   dimension; dim 2 is below it).

9. AT-INFINITY / BOUNDARY. For many problems the difficulty concentrates at a
   compactification boundary / asymptotic locus / place at infinity. Study the
   compactification and its boundary divisor (log geometry, Berkovich, Newton
   polygons as tropicalization). When: when local/interior analysis misses the
   obstruction. Produces: uniform (all-parameter) statements where local fails.

10. ADVERSARIAL / AUDIT (our discipline, a lens in itself). Declare hypotheses
    BEFORE runs; regression-gate every new arithmetic path against a known exact
    decision; commission audits; keep refutations and retractions in the record.
    When: always. Produces: trust; catches premise errors before they compound
    (it caught the EXP-070 retraction and the EXP-076 error).

11. EXTERNAL DIALOGUE. Engage expert reasoning - primary papers, other
    mathematicians', other models' derivations - and CROSS-CHECK against our own
    machinery. The goal is not to adopt but to SEPARATE genuinely new leads from
    validation, and verify every borrowed claim in-repo. When: whenever strong
    external analysis is available. Produces: new lenses and leads (the Tao-ChatGPT
    exchange gave us anatomy + recognition + the EXP-089 exclusion), always
    re-derived exactly before use.

## The workflow (every problem)

- PLAN STAGE: list which lenses apply; commit to the spine (1) plus at least two
  others (usually 2/anatomy + 4/invariant, and 3/recognition or 7/reformulation).
- EACH ROUND: the spine runs; when it stalls or a known example appears, switch
  lens deliberately rather than pushing the spine harder.
- INVARIANTS FIRST: before a heavy sweep, ask whether a single invariant (lens 4)
  decides the case cheaply.
- RECORD: the problem's RESUME carries a short "lenses tried / what each gave"
  ledger, so a stall in one lens routes to the next instead of to more of the
  same.
- COMPLEMENTARITY: exclusion (1) <-> two-sided (6) <-> anatomy (2) <-> recognition
  (3) form a cycle; a result in any one feeds the next.

## Honest scope

These lenses do not manufacture theorems; they multiply the angles of attack and
prevent tunnel vision on the spine. The spine remains where verifiable, persisted
progress comes from; the other lenses are where the conceptual breakthroughs and
the cheap one-line exclusions come from. Use both.
