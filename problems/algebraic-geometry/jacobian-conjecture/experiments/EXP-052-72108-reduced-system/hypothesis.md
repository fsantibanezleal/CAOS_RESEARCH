# EXP-052 - First contact with the REDUCED (72, 108) system (route N2)

- **Question.** JCB-040. The GGHV dossier (context/2026-07-22-gghv-72108-dossier.md)
  transcribes Prop 4.3: the open (72, 108) case reduces to the existence of a pair
  P, Q with [P, Q] = x^2 and supports in the REDUCED polygons
  N(P) = conv{(0,0), (1,0), (8,14), (8,16), (0,8)} and
  N(Q) = conv{(0,0), (2,1), (12,21), (12,24), (0,12)}. Can the machine engage this
  reduced object directly?
- **Motivation (derivation, declared).** The bracket [P, Q] = x^2 is LINEAR in Q given
  P: for each sampled P on its polygon, solvability of the full Q-polygon system is one
  exact linsolve (a few hundred unknowns), and inconsistency across samples is evidence
  toward the case's closure (whose full form is an elimination over all P: the system
  GGHV could not solve, never printed). This is the sampled first contact; the
  parametrized elimination with our certificate/transport instruments is the follow-on.
- **Falsifiable predictions.**
  1. [MV] (Sizes) The lattice-point counts of both reduced polygons are computed; the
     Q-side system is a few hundred unknowns (tractable).
  2. [MV] (Sampled emptiness) For random rational P samples on N(P) (corners forced
     nonzero) and one structured sample honoring the (0,8)-(8,16) top edge form, the
     Q-system [P, Q] = x^2 is INCONSISTENT: no partner exists for any tested P.
  3. [D] (Framing) A consistent sample would be a candidate route to a JC(2)
     counterexample and is escalated immediately (adjudicate, then verify the
     GGHV chain backwards); sampled emptiness is evidence, not closure: the
     parametrized certificate over all P is the declared next step.
- **Method.** sympy over QQ; exact hull lattice enumeration; linsolve per sample; caps
  570 s.
- **Success criterion.** 1-2 verified with timings; the reduced object is on the
  machine's bench.
- **Failure criterion.** A consistent sample (escalate per prediction 3); polygon
  enumeration disagreeing with the dossier's corner data.

Declared 2026-07-22 before the run.
