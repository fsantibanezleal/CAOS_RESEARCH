# EXP-097: Direct intersection-21 transport fails its typing gate

## Result

The exact transformation audit confirmed the declared prediction. The
original-pair statement

\[
\deg_x\operatorname{Res}_y(P,Q)=21
\]

does not become an unconditional absolute-degree equation on the 51
coefficients of the final GGHV Laurent pair.

The obstruction is categorical, not computational. The verified reduction:

1. swaps the coordinate eliminant;
2. localizes \(x\), so \(x^s\) is a unit and an \(x=0\) resultant divisor is
   forgotten unless separately recorded;
3. applies \(x\mapsto x^{-1}\), \(y\mapsto x^4y\), which reflects the
   resultant exponent interval.

For \(R(x)=\operatorname{Res}_y(F,G)\), with \(y\)-degrees \(p,q\), the exact
final-inversion law is

\[
\operatorname{Res}_y(\phi_cF,\phi_cG)
=x^{cpq}R(x^{-1}).
\]

The final reduced polygons have \((p,q,c)=(16,24,4)\), hence \(cpq=1536\).
If the relevant pre-inversion resultant has exponent interval
\([\nu,21]\), the final interval is

\[
[1515,1536-\nu],
\]

of width \(21-\nu\). Width \(21\) follows only after proving
\(\nu=\operatorname{ord}_xR=0\). Neither EXP-096 nor the printed Proposition
4.3 reduction supplies that boundary order after the initial swap and
localization.

## Exact controls

All declared symbolic controls passed:

- a common Laurent translation preserved a nontrivial resultant exactly;
- the inversion/scaling formula had zero residual;
- multiplication by a Laurent unit shifted the exponent interval while
  preserving its width;
- the control resultant \(x\) became the unit \(1\) after localizing at \(x\),
  exhibiting loss of the \(x=0\) divisor;
- the coordinate-swap control changed the selected eliminant degree from
  \(1\) to \(0\).

The run completed in approximately 2.1 seconds and reproduced byte-for-byte.
The artifact is `artifacts/results.json`, SHA-256
`8FB92DDC507B1114B84C8F1193F6A49D21241C6BDCDDFAA9C68700C2EC21B42E`.

## Verdict and scope

**CONFIRMED:** do not impose “resultant degree \(21\)” directly on the 51
reduced coefficients. Absolute degree is not a typed invariant of the
Laurent/birational reduction without a boundary-divisor ledger.

A conditional replacement survives:

- Laurent resultant exponent width is invariant under multiplication by
  Laurent units and is reflected, not destroyed, by the final inversion;
- turning it into the value \(21\) requires a new proof of the missing
  original boundary order and compatibility through the coordinate swap.

This does not prove that such a boundary theorem is false. It proves that the
current source data are insufficient to use intersection \(21\) as a direct
reduced-coefficient rejection equation.

The seven Lee--Li inner vertices are likewise still original-pair gates; this
experiment did not transport the inner polynomial through the Laurent cuts.

## Route decision

Close the direct resultant-degree transport route. Do not compute a generic
resultant of the 51-parameter system for this purpose.

Two honest continuations remain:

1. a future boundary-divisor reconstruction of the complete GGHV map,
   retaining the swap, cut parameters, orders at \(x=0\), and the divisor sent
   to infinity;
2. the already-ranked small certificate-module/chart-cover experiment.

The second is lower-cost and does not depend on an unprinted inverse
transformation, so it becomes the immediate route. The intersection-\(21\)
and seven-vertex facts remain rejection gates for any candidate that is
actually reconstructed back to an original polynomial pair.

## Non-claims

- The open \((72,108)\) chain is not excluded.
- No inner-vertex candidate is proved realizable.
- No counterexample is constructed.
- The planar degree floor is not raised.

## How could this be wrong?

- A Keller-specific theorem could identify the relevant resultant with a
  coordinate-free intersection number and prove that no boundary contribution
  is lost in this exact reduction. No such theorem is present in the audited
  source record.
- A full reconstruction could restore the missing divisor orders. That would
  be additional data, not a contradiction of this typing verdict.
- The final-inversion arithmetic uses the verified reduced \(y\)-degrees
  \(16,24\) and \(c=4\); changing orientation changes notation but not the
  localization/boundary issue.
