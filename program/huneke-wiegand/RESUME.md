# Huneke-Wiegand extensions - session handoff

Updated: 2026-08-02. Lifecycle: analyzing; EXP-004 declared before tooling or computation.

## 1. State in one screen

Son Pham has priority for the public candidate counterexample. Professor Craig Huneke supplied an
independent verification. This programme does not compete for discovery priority. It asks:

1. Can CAOS reproduce the decisive colon equality through an independent computer-algebra route?
2. Is the example minimal under natural measures, especially Frobenius number?
3. Does it lie in an infinite family?
4. What structural defect permits rigidity, and which stronger conjectures survive?

Candidate:

```text
Gamma = <56,57,58,63,64,70,71,72,73,74,75,76,77,78,79,80,81,82,83,
         87,89,90,93,95,96,97>
R = Q[t^Gamma] localized at the positive-degree maximal ideal
I = (t^56,t^70)R
```

CAOS EXP-001 independently confirms Frobenius 181, conductor 182, genus 91, symmetry, both
principal colon generator sets and the decisive intersection-product equality. Singular/4ti2
uses a 322-generator toric standard basis of dimension one; the finite route agrees. The
`<4,5>` hypersurface control rejects equality with residues `x5^3` and `x4^4`.

CAOS EXP-002 independently computes
`v(End_R(I))=Gamma union {101,107,181}`. The overring semigroup has Frobenius 125, genus 88,
type 24 and new minimal generators 101 and 107. Dey--Lyle Proposition 4.1(2) and Theorems
4.2--4.4 show the precise escape mechanism: `I` stays rigid over `End_R(I)` but is not reflexive
there, while `Ext^1_E(I,E)`, `Ext^2_E(I,I)` and `Tor^R_1(I,E)` are nonzero.

CAOS EXP-003 calibrates a finite SAT encoding at `(181,14)`. Z3 recovers the pinned candidate,
and a separate standard-library checker validates the model through `2F+1` plus a proved tail.
Every gap of the `<4,5>` control has an explicit failed rigidity witness. This validates the
instrument but is not a minimality result.

## 2. The objects table

| object | definition | evidence owner |
|---|---|---|
| Gamma | candidate numerical semigroup on 26 displayed generators | EXP-001 target |
| R | `Q[t^Gamma]` localized at the positive-degree maximal ideal | source dossier |
| I | `(t^56,t^70)R`, normalized shift 14 | source dossier |
| E and D | exponent sets for `J^-1` and `(J^2)^-1`; rigidity asks `D=E+E` | EXP-001 |
| End overring | `End_R(I)`; desk value-semigroup prediction adds 101, 107, 181 | EXP-002 |
| minimality frontier | least Frobenius value admitting symmetric Gamma and a rigid nonprincipal two-generator monomial ideal | EXP-003 onward |

## 3. Experiment index

| EXP | question | status | load-bearing output |
|---|---|---|---|
| EXP-001 | Can Singular/4ti2 independently reproduce the colon equality and reject a known-positive control? | CONFIRMED | 322-generator dimension-one toric basis; zero differences; control residues |
| EXP-002 | What is the exact endomorphism overring and why do modern positive criteria miss I? | CONFIRMED | exact semigroup, type 24, and forced Ext/Tor escape map |
| EXP-003 | Can SAT recover `(F,s)=(181,14)` and calibrate exact controls? | CONFIRMED | independently checked finite SAT machinery |
| EXP-004 | Can two independent certified routes reproduce the published `F<69` frontier? | declared | Blanco--Rosales tree plus CaDiCaL/DRAT proof suite |

## Strongest routes

- R1 independent quotient-ring computation: Singular 4.3.2 + 4ti2 toric ideal, then compute
  `((a):b)`, `((b):a)`, their intersection and product.
- R2 endomorphism anatomy: test the desk prediction
  `v(End_R(I)) = Gamma union {101,107,181}` and its non-Gorenstein consequences.
- R3 certified minimality: Boolean/SAT encoding of symmetric semigroups and `D=E+E`; calibrate
  at `(F,s)=(181,14)`, reproduce the published no-example frontier `F<69`, then extend it.
- R4 additive family: explain the pattern `B+B=C` and test affine/Kunz-ray families.
- R5 surviving variants: hypersurface, complete-intersection, low-multiplicity, Burch,
  weakly-m-full, periodic, generalized-arithmetic-sequence and endomorphism-ring hypotheses.

## Lenses tried

- exclusion: positive theorems rule out low multiplicity, complete intersections and small duals;
- anatomy: additive bases B and C, plus the endomorphism overring;
- invariant: symmetry defect of `End_R(I)`;
- reformulation: colon equality, inverse-ideal equality and SAT membership constraints;
- two-sided validation: Singular quotient ring versus finite semigroup checker;
- recognition: search for affine families in Kunz coordinates.

## 4. In flight

EXP-004 is declared before tool installation, implementation or computation. Route A will enumerate
all symmetric semigroups using Blanco--Rosales Theorem 9 and attach a failed-rigidity witness to
every gap. Route B will generate independent CNFs and require CaDiCaL DRAT proofs accepted by
DRAT-trim. EXP-001 through EXP-003 remain closed.

## 5. Next actions

1. Install the pinned proof tools only after the EXP-004 declaration commit.
2. Implement and smoke-test the theorem-complete tree at `F<=11`.
3. Implement DIMACS generation, CaDiCaL proof output and DRAT-trim checking; calibrate at 181.
4. Reproduce `F<69`; only then declare a separately budgeted frontier extension.
5. Compare any new frontier with the additive-family and surviving-variant routes.

## 6. Where everything lives

| what | path |
|---|---|
| problem tree | `problems/commutative-algebra/huneke-wiegand/` |
| programme record | `program/huneke-wiegand/` |
| source dossier | `problems/commutative-algebra/huneke-wiegand/context/` |
| experiments | `problems/commutative-algebra/huneke-wiegand/experiments/` |
| external sources | `E:/_Datos/caos-research/huneke-wiegand/sources/` |
| management mirror | `_CAOS_MANAGE/plans/caos-research/huneke-wiegand/` |

## 7. Gotchas

- Discovery priority belongs to Son Pham; never call a CAOS reproduction the discovery.
- Expert verification is not journal peer review.
- Never import or execute upstream verifier code as independent CAOS evidence.
- Equality in a truncated window needs a proved conductor/tail argument.
- Solver SAT models need independent extraction checks; UNSAT needs certificates or an
  independent exhaustive route.
- EXP-004 external proof root is
  `E:/_Datos/caos-research/huneke-wiegand/EXP-004-certified-f69-frontier/`; Git carries only its
  deterministic manifest and compact summaries.
- A validated finite counterexample does not automatically classify or minimize all examples.
- No manuscript, Zenodo version, bake, tag or release without the corresponding methodology gate.

## Resume command

Read root `Entry_point.md`, this file, `plan.md`, `state.md`, `backlog.md`, the latest experiment
verdict, then continue the highest-priority unblocked HWB item. Never import or execute the
candidate repository's verifier as CAOS evidence.
