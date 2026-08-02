# Huneke-Wiegand extensions - session handoff

Updated: 2026-08-02. Lifecycle: consolidating; EXP-005 proves Frobenius minimality at 181,
EXP-007 proves uniqueness of the normalized pair at that minimum, and expanded preprint v0.02 is
published at DOI `10.5281/zenodo.21764868`.

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

A 2026-08-02 deduction places the candidate strictly outside the generalized-arithmetic-sequence
positive family of Landeros et al. Multiplicity 56 and membership of 57 force step one, while
membership of 63 would force the actual gaps 59--62. All generator-deletion gcds are one, so the
paper's diagonal gcd obstruction is vacuous for shift 14.

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
| EXP-004 | Can two independent certified routes reproduce the published `F<69` frontier? | CONFIRMED | 48,954 semigroups, 1,503,391 gaps and 1,156 accepted DRAT proofs |
| EXP-005 | What is the least counterexample Frobenius value at or above 69? | CONFIRMED | exact minimum `F=181`; checked proofs below, exact model and tree cross-check |
| EXP-006 | Does the `m=4s`, `F=13s-1` block pattern extend to a family? | Route G REFUTED; Route K open | only the seed passes the fixed-offset sweep; constrained block SAT remains |
| EXP-007 | What are all normalized rigid pairs at the minimal value `F=181`? | CONFIRMED | exactly one: the public semigroup at shift 14; terminal proofs and fresh audit pass |

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
- positive-family exclusion: the candidate is provably not generalized arithmetic, and the
  associated deletion-gcd certificate is vacuous.

## 4. In flight

EXP-005 is CONFIRMED: every odd `F=69,...,179` has an accepted selector-CNF DRAT proof, while
`F=181` is SAT at `s=14` and decodes exactly to the public candidate. Together with EXP-004 and
oddness of the symmetric Frobenius number, this proves `F_min=181` in the two-generated monomial
ideal class. The full 228-file search audit passes. Independent theorem trees agree at
`F=69,71,73,75`. EXP-006 Route G refutes the naïve fixed-offset family: only `s=14` passes through
100; Route K remains open. The seven-page v0.01 preprint passed a warning-free two-pass build,
complete rendered-page inspection and exact remote-file hash verification. Zenodo version DOI
Preprint v0.02 is published at version DOI `10.5281/zenodo.21764868`; concept DOI
`10.5281/zenodo.21763582` resolves to it and v0.01 remains frozen at `10.5281/zenodo.21763583`.
The public v0.02 file matches the committed 350,524-byte PDF at SHA-256
`93a07d124c7b3f2cf144a5343d31ca40e312a80d99308b3ef567c7065f126bb9`. EXP-007 is CONFIRMED:
the support proof leaves only shift 14, and the fixed-shift proof leaves only the public membership
vector. The independent audit reconstructs all formulas and freshly accepts both proofs. This is
the complete minimum-layer classification, not a classification at higher Frobenius values.

## 5. Next actions

1. Execute EXP-006 Route K as a constrained block/Kunz search; require non-seed models before any
   renewed family claim.
3. Extend the surviving-variants matrix without weakening the proved scope.
4. Reduce the certificate trusted base or import accepted proofs into a smaller verified checker.

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
- Zenodo v0.01 is immutable. Any correction or extension requires the formal new-version flow;
  no silent replacement of the published PDF.
- PR `#142` passed `guards` and `test` and merged EXP-007, both terminal certificates, the
  reconstruction audit and published preprint v0.02 into `develop` at
  `136781d023752234697aaa1c86ce1f10dffff9c3`; this checkout remains on its product branch.

## Resume command

Read root `Entry_point.md`, this file, `plan.md`, `state.md`, `backlog.md`, the latest experiment
verdict, then continue the highest-priority unblocked HWB item. Never import or execute the
candidate repository's verifier as CAOS evidence.
