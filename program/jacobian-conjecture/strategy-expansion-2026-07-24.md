# Strategy expansion (2026-07-24, session 47): all paths that could help

Felipe's directive: explore ALL paths and strategies. The map, ranked by
expected information per unit cost; each candidate becomes a declared
experiment or a dossier before any claim.

## S1. The structural-theorem seeds (the only road to all-degrees statements)
- S1a. GENERALIZE THE ANNIHILATION LEMMA: J(m, P^k) = -kL(P^{k-1}m) and the
  dual identity (c kills all bracket images) both smell like one fact about
  the pairing between the bracket image and the cokernel across ALL windows.
  Hypothesis to declare: for every window system in the staircase transport,
  the cokernel pairs trivially with the ad-image; if provable in general, the
  obstruction theory becomes PURELY top-order for every configuration, a
  uniform lemma feeding any future termination argument.
- S1b. TERMINATION OVER CHAINS: the GGV chain machinery generates finitely
  many candidate chains per degree bound but infinitely many overall. Seek a
  well-quasi-order (Dickson/Higman style) on chain data under which the
  exclusion certificates are monotone: WQO + monotone exclusion = all-degrees
  theorem. Speculative; a dossier first (literature: tropical/valuation trees).
- S1c. THE OBSTRUCTION-MOTION LAW: degrees 1/2/3 show obstructions MOVING
  (diagonal 8-set, then a mixed triple, then nothing through triples).
  Measure WHERE obstructions live as functions of degree on small analog
  systems (toy polygons): an empirical law could reveal the generating
  mechanism and predict whether some finite degree always closes.

## S2. The (72,108) endgame (current thread, continued)
- S2a. Quadruple sweep (EXP-075, running). S2b. Constructive GF(p) solve (R2).
- S2c. CHART COVERS (R4): formalize the axis-chart certificates (EXP-063/065)
  into a finite cover statement: the missing piece is the gluing condition;
  declare the two-chart toy first.

## S3. The [125,150] frontier (C13 thread, continued)
- S3a. EXP-077: the en-point/q1 computation + Prop 3.29 numbering match.
- S3b. The Theorem 5.1 template cases (C08/C09/C14/C15) after C13.

## S4. Independent leverage from the GGV toolbox (unmined)
- S4a. APPROXIMATE ROOTS / SUBRESULTANTS (arXiv 1708.09367): intersection-
  number formulas give INDEPENDENT constraints on the same candidate pairs;
  cross-checking our polygon exclusions against intersection-number
  obstructions could kill cases cheaper or catch errors.
- S4b. Orevkov's methods (flagged by GGHV17 for sporadic chains): literature
  pass; his Lemma 4.1(a) analyzed an F13 sibling extensively.
- S4c. CHAR-P TRANSFER: our EXP-0xx char-p certificates for 3D; is there a
  mod-p shadow of the planar chain machinery giving fast necessary filters?

## S5. Engineering multipliers
- S5a. Port the subsystem sweeps to a compiled GF(p) kernel (galois/numpy
  batched or a small C extension): 100x on sweeps unlocks quadruple+ tiers.
- S5b. SAT/ILP encodings of feasibility sweeps for independent verification.
- S5c. Lean formalization of the theorem ladder (JCB-018, parked): revisit
  once the truncation story stabilizes.

## S6. Community and record
- S6a. GGHV outreach (draft ready; Felipe sends). S6b. Paper B truncation
  chapter + Zenodo republish (authorized). S6c. A methods note on the
  declared-gate discipline (the retraction story) as its own short paper.

Execution order (sessions 47+): S3a and S2a continue now; S1a is the next
DECLARED experiment after EXP-077 (it is cheap: test the dual annihilation on
3 other window systems); S5a lands when the quadruple sweep's cost justifies
it; S4a opens as a dossier in parallel rounds.
