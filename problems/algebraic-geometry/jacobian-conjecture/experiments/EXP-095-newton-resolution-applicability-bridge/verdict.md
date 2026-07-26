# EXP-095: Applicability confirmed at the original pair; the open branch is retained

## Result

The exact crosswalk passed. The Makar-Limanov--Trakhtenberg hypotheses do not
apply directly to the final GGHV Laurent pair, but they do apply to the
hypothetical original polynomial Keller pair. At that original stage, the
degree-72 component is exactly the first retained \(D=72\) candidate printed in
*Properties of a Jacobian mate*.

| Datum | GGHV open component | First printed \(D=72\) branch | Decision |
|---|---:|---:|---|
| \(D\) | \(72\) | \(72\) | match |
| \(v_0=2A_0\) | \((16,56)\) | \((16,56)\) | match |
| \(v'_1=2A'_0\) | \((2,0)\) | \((2,0)\) | match |
| \(v_1=2A_1\) | \((11/2,14)\) | \(2(11/4,7)\) | match |

The corresponding source leading form is
\(\phi_0=cx(xy^4-r_1)^7\). After the GGHV coordinate swap, this is the same
edge pattern as \(y(x^4y-\alpha)^7\), which GGHV records before its Laurent
edge cut. This leading-form observation is corroborative; the verdict rests on
the exact signature table.

## Applicability decision

The source algorithm starts from \(f,g\in\mathbb C[x,y]\) with \(J(f,g)=1\)
and repeatedly uses transformed identities \(J(f_i,g_i)=1\). The final GGHV
objects instead lie in \(K[x,x^{-1},y]\) and satisfy \([P,Q]=x^2\).
Consequently:

- direct use on the final reduced pair is invalid;
- visual comparison with
  \(P_T=y^8(xy-1)^8+x\) cannot yield an exclusion;
- use on the original degree-72 polynomial component is valid under the
  hypothetical counterexample premise.

The GGHV reductions do not need to preserve all Newton-resolution invariants
for this comparison: the valid bridge returns to the original pair before the
non-polynomial changes of variables.

## Adversarial validation

Five exact controls passed:

1. a polynomial pair with bracket \(1\) passed the source-hypothesis gate;
2. a Laurent pair with bracket \(x^2\) failed it;
3. changing \(A'_0\) broke the first-branch match;
4. changing \(A_1\) to \((5/2,6)\) broke the first-branch match;
5. that altered final corner matched the second printed \(D=72\) signature,
   confirming that the classifier distinguishes the two source branches.

The artifact is `artifacts/results.json`, SHA-256
`FE0848E4BDB1A01BD209D7CD9C9DCCB8B457219C70CDBF83C177369876978F6B`.

## Verdict and scope

**CONFIRMED:** Newton resolution is applicable to the original degree-72
component, and its published \(D\le100\) candidate list retains rather than
excludes the GGHV open case.

This is an independent source consistency check, not a solution of the
\((72,108)\) case. It does not prove that the retained branch is realizable,
construct a counterexample, or raise the planar degree floor.

## Route decision

The direct reduced-pair Newton comparison is closed. Re-running the published
\(D\le100\) candidate enumeration has no expected value for the open case
because its exact branch is already present.

The Newton route can advance only through restrictions beyond the published
candidate classification: a new derivation specialized to the retained first
\(D=72\) branch, with every integrality and polynomiality condition typed on
the original Keller pair. Before undertaking that larger derivation, the
lower-cost next experiment is the persisted Lee--Li plus GGHV
approximate-root/intersection applicability audit. The independent
certificate-module/chart-cover analog remains next after that source gate.

## How could this be wrong?

- The crosswalk depends on the GGHV17 transcription
  \(A_0=(8,28)\), \(A'_0=(1,0)\), \(A_1=(11/4,7)\), and component factor
  \(2\). These values were already verified against the primary TeX source.
- The Newton-resolution row was reread from the primary PDF, but the paper's
  complete enumeration code was not independently reproduced.
- Membership in a necessary-condition list is not sufficiency. The matching
  row may still be impossible for reasons not developed in that paper.

