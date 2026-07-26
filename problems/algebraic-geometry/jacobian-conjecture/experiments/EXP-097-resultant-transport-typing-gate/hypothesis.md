# EXP-097: Type the intersection-21 gate through the GGHV reduction

## Question

Does the exact original-pair condition

\[
I(P,Q)=\deg_x\operatorname{Res}_y(P,Q)=21
\]

transport to a well-defined exact condition on the 51 coefficients of the
final GGHV Laurent pair, before any large coefficient computation?

## Motivation

EXP-096 supplied intersection number \(21\) as an original polynomial-pair
rejection gate. The next ranked action is to transport it to the reduced
system, but the verified GGHV pipeline changes categories:

1. it swaps \(x\) and \(y\);
2. it cuts edges with \(y\mapsto y+\lambda x^{-k}\) in
   \(K[x,x^{-1},y]\);
3. it applies \(x\mapsto x^{-1}\), \(y\mapsto x^4y\).

An absolute polynomial degree is not automatically an invariant of this
Laurent/birational category. This typing gate must be decided before building
any equation in the reduced coefficients.

## Exact transformation laws under test

Let \(R(x)=\operatorname{Res}_y(F,G)\), with
\(\deg_y F=p\), \(\deg_y G=q\).

1. A common translation \(y\mapsto y+h(x)\) preserves \(R(x)\) over
   \(K(x)\).
2. Under
   \[
   \phi_c:\quad x\mapsto x^{-1},\qquad y\mapsto x^cy,
   \]
   one has
   \[
   \operatorname{Res}_y(\phi_cF,\phi_cG)
   =x^{cpq}R(x^{-1}).
   \]
3. In \(K[x,x^{-1}]\), a resultant is defined only up to a unit \(cx^s\)
   unless a boundary normalization is retained. Multiplication of one input
   by \(x^u\) shifts the resultant by \(x^{uq}\).
4. The initial coordinate swap replaces
   \(\operatorname{Res}_y\) by the other coordinate eliminant
   \(\operatorname{Res}_x\); equality of their absolute degrees requires a
   separate intersection/boundary theorem.

## Falsifiable prediction

The direct transport will fail its typing gate:

- the absolute number \(21\) is not a well-defined invariant of the final
  Laurent pair by itself;
- the exponent width of a Laurent resultant survives unit shifts and is
  reflected by the final inversion, but the original statement
  \(\deg R=21\) fixes that width only if
  \(\operatorname{ord}_xR=0\);
- the source record does not supply that boundary order after the initial
  swap and Laurent localization.

For the final inversion, the reduced polygon bounds give
\((p,q,c)=(16,24,4)\), hence \(cpq=1536\). If the pre-inversion resultant has
support interval \([\nu,21]\), its transformed interval is
\([1515,1536-\nu]\), of width \(21-\nu\), not unconditionally \(21\).

## Premise dependencies

- The transformation sequence and final map are the verified transcription in
  `context/2026-07-22-gghv-72108-dossier.md`, Proposition 4.3 pipeline.
- The final reduced polygon has \(y\)-degrees \(16\) and \(24\).
- EXP-096 proves the original-pair degree \(21\), but does not state
  \(\operatorname{ord}_xR=0\) or a boundary divisor ledger.
- This experiment does not assume that every arbitrary polynomial control is
  a Keller pair; the controls test functorial resultant identities that must
  hold before Keller-specific hypotheses can help.

## What a PASS or FAIL proves

- Prediction confirmed: no equation imposing absolute resultant degree \(21\)
  may be written directly in the 51 reduced coefficients. A future transport
  must reconstruct the missing boundary valuation/divisor data, or prove a
  Keller-specific theorem that fixes it.
- Prediction refuted: if absolute degree survives all verified operations,
  derive the exact reduced-coefficient condition and declare a separate
  reconstruction experiment.

Neither outcome excludes \((72,108)\), realizes an inner vertex, constructs a
counterexample, or raises the degree floor.

## Adversarial controls

Use exact SymPy algebra to verify:

1. common Laurent translation preserves a nontrivial resultant;
2. the final-inversion formula holds exactly;
3. a Laurent unit shifts absolute exponents but preserves width;
4. localization can erase an \(x=0\) resultant divisor;
5. a coordinate swap can change the selected eliminant's degree when boundary
   degree drops occur.

## Compute budget and kill criterion

CPU only, exact symbolic arithmetic, expected runtime below one second.
Budget: 10 seconds. If any transformation identity fails, stop and record a
transcription or implementation failure; do not draw a transport conclusion.

Declared 2026-07-26 before running `run.py`.
