# Huneke-Wiegand extensions - session handoff

Updated: 2026-08-01. Lifecycle: opened; EXP-001 declared but not yet run.

## Exact scope

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

Known external facts: Frobenius 181, conductor 182, genus 91, Gamma symmetric; I is
nonprincipal; the principal-colon equality makes I rigid and therefore `I tensor I*`
torsion-free. Treat these as external claims until EXP-001 closes.

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

## Resume command

Read root `Entry_point.md`, this file, `plan.md`, `state.md`, `backlog.md`, the latest experiment
verdict, then continue the highest-priority unblocked HWB item. Never import or execute the
candidate repository's verifier as CAOS evidence.
