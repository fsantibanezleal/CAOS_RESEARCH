# EXP-001 - independent quotient-ring colon certificate

Declared 2026-08-01 before experiment code was written or run. Phase HW-P1. Backlog HWB-001.

## Question

Can a computer-algebra calculation that shares no verifier code with the public candidate package
reproduce the decisive colon equality, while rejecting a known-positive control?

## Fixed objects

Let `G` be the 26 displayed candidate generators, `A=Q[t^Gamma]`, `a=t^56`, `b=t^70`,
and `I=(a,b)`. Construct A independently as a quotient of a 26-variable polynomial ring by the
toric ideal computed by 4ti2/Singular.

The control is `Gamma0=<4,5>`, `A0=Q[t^4,t^5]`, `I0=(t^4,t^5)`. This is a hypersurface
numerical-semigroup ring and I0 is nonprincipal, so the Huneke-Wiegand positive theorem predicts
that I0 is not rigid and the decisive colon equality must fail.

## Falsifiable predictions

- P1: the candidate toric quotient is a one-dimensional domain and the independent finite
  semigroup audit returns Frobenius 181, conductor 182, genus 91 and symmetry.
- P2: the candidate principal colons have minimal exponent generators
  `{56,57,58,63,64,73,75,76,79,81,82,83}` and that set shifted by 14.
- P3: for the candidate, `((a):b) intersect ((b):a)` equals their product in the graded ring;
  therefore localization preserves the equality.
- P4: for the control `<4,5>, (t^4,t^5)`, intersection and product are unequal. The run must
  exhibit a reduced witness in the difference.
- P5: a second, standard-library-only finite semigroup implementation agrees with the Singular
  result but does not read upstream certificate data or code.
- P6: changing any expected candidate colon generator before comparison causes the test harness
  to fail, demonstrating that the expected-data gate is active.

## Independence boundary

Allowed inputs: only the displayed generator lists, ideal generators and published theorem
statements. Forbidden: importing, copying or executing any script or certificate from the candidate
repository. Singular/4ti2 quotient-ring operations are the primary route; the Python finite-set
checker is the cross-check, not a transcription of upstream code.

## Method and budget

1. Generate the toric ideal through Singular `toric.lib` and 4ti2.
2. Form the quotient ring and compute the two principal colons, intersection and product.
3. Compare reduced standard bases in both directions and record a control witness.
4. Independently enumerate semigroup membership to a theorem-backed conductor tail and compare
   minimal monomial generators.

Wall cap: 10 minutes per computer-algebra stage, 25 minutes total. Print flushed stage progress.
Kill on a silent stage beyond its cap. CPU only.

## Verdict rules

- CONFIRMED only if P1-P6 all pass.
- REFUTED if the candidate equality fails under a validated representation.
- INCONCLUSIVE if Singular cannot finish inside the cap or route independence is compromised.
- A control failure invalidates the verifier; it is never evidence against the theorem.
