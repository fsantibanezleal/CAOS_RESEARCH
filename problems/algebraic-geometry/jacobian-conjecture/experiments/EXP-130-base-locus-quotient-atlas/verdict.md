# EXP-130 verdict - the complete principal-open base locus is closed

**Verdict:** confirmed, within the declared four-parameter restriction.

**Decision:** the reduced finite cylinder

\[
V(R,S)\cap D(X),\qquad X=A^3,
\]

is covered by a finite exact maximal-minor atlas, uniformly in
\(Y=A^2C\). Together with EXP-123 and EXP-129, this closes the complete
\(A\ne0\) part of the restriction. It does not close the \(A=0\) boundary or
any larger parameter family.

## What happened

The generic rational Groebner route reached its declared 300-second gate, but
both projection resultants completed first. They have degree 117 and factor as
a coordinate factor of multiplicity 27 followed by squarefree irreducible
blocks of degrees 3, 6, 12, and 69. A factorwise subresultant/CRT redirect then
proved that the principal-open coordinate algebra is a reduced product of four
fields of total dimension

\[
3+6+12+69=90.
\]

In every block the specialized gcd of \(R\) and \(S\) is linear in \(X\); its
reconstructed \(X\)-class annihilates both polynomials and has the matching
projection minimal polynomial. The discarded coordinate support is
\(X=B=0\): directly, \(\gcd(R(0,B),S(0,B))=B^{12}\) and
\(\gcd(R(X,0),S(X,0))=X^3\). This support belongs to the separate \(A=0\)
boundary. The resultant multiplicity 27 is not asserted to be its local
length.

Existing sections cover the degree-69 block by the constant EXP-124 section
and the degree-12 block by the EXP-125-h36 / EXP-129-atlas-1 affine pair. The
degree-3 and degree-6 blocks required a new section. A generic new row basis
left one common quadratic in \(K[Y]\) on each block. Targeted modular probes at
the roots of those quadratics had full augmented rank at two primes per block,
but direct reconstruction of the default targeted basis reached its gate.

The accepted redirect searched equivalent full-rank bases while minimizing
the exact determinant's strongly connected component. Starting from the
EXP-125-F3 basis and replacing one row reduced the largest component to 33.
Its reconstructed determinant is

\[
A^{86}H(X,B,Y),\qquad \deg_Y H=2,
\]

and passed an independent direct 125-by-125 determinant control. On each of
the degree-3 and degree-6 fields, this section breaks the persisted common
quadratic. Exact extended Bezout identities in \(K[Y]\), independent
\(Y\)-resultants, and multiplication-matrix norms all certify that the final
section pairs generate the unit ideal.

## Exact evidence

- `artifacts/algebra-checkpoint.json`: generic-elimination checkpoint, SHA-256
  `9C3E1212CE6D7FC8296DD732E7488F74731BD333446A10817F9BFAF1C41A6179`.
- `artifacts/crt-worker.json`: factorwise algebra and existing-atlas tests,
  SHA-256 `7189D6C9DBD6CF3E006B937A9DE1547A43155985BEF6716FE544F58A0EE65CB2`.
- `artifacts/selection.json`: first generic degree-3/6 row selection, SHA-256
  `77FFCD863B06141C8E95108D130869227D4D7532B4470B58ABB5A9CED959C418`.
- `artifacts/exact-worker.json`: first exact section, SHA-256
  `CF305B272DFB26A223F0BDFDD93E879B04488B5FC2981418582ACC5DAAD9AA17`.
- `artifacts/certificate.json`: common-quadratic isolation, SHA-256
  `645CB57F9AB6BFA7120C5163388930322CE128E6FB324D22DD5B0364F0CEF39D`.
- `artifacts/targeted-selection.json`: targeted full-rank probes, SHA-256
  `605B8E29E9694D7249C69E5E1C92680D349E503D37725F105A6F3EDF95AD129C`.
- `artifacts/structural-selection.json`: minimum-SCC basis choice, SHA-256
  `7EA09CB31314797859CF2EE8A02C984C2066FAD809DAE096F1242F60B24C347E`.
- `artifacts/structural-exact-worker.json`: accepted exact section, SHA-256
  `0C6DF9F97BC10F8462C37122B5C47F108A8F8CAE81EBAB80D07CF5304E487961`.
- `artifacts/final-certificate.json`: final characteristic-zero certificate,
  SHA-256 `6742648B5CAB7E795B7D680776BA50ACE5F5E4810D6D050CBD50CCDB06BF1DE0`.
- `artifacts/results.json`: deterministic release summary, SHA-256
  `DE68F61E5E9B650B7C0C00679DD0F69360A4871205C0DBB059E78AF4307066FD`.

Re-running `run.py` verifies the accepted source hashes, reconstructs the
alternative determinant from invariant coordinates, repeats the direct
determinant control, verifies both Bezout identities and both independent
resultant norms, and reproduces the final hashes.

## Adversarial validation

The result survived the strongest applicable route: exact re-derivation by
independent algorithms.

1. Projection resultants and factorwise subresultants agree on the four
   principal-open blocks and their same-point \(X\)-classes.
2. The structural determinant reconstructed by SCC factorization agrees with
   a direct determinant of the same 125-by-125 specialization at an independent
   control point.
3. Coverage is certified first by explicit extended Bezout identities in
   each finite field polynomial ring \(K[Y]\), then independently by
   \(Y\)-resultants and multiplication-matrix norms.
4. The modular probes are reconnaissance only. Every verdict-bearing coverage
   claim is repeated in characteristic zero.
5. Failed routes were retained: generic Groebner timeout, coefficient
   extraction defect, refuted single-chart prediction, incomplete existing
   atlas, generic-section common quadratics, and targeted exact timeout.

## Consequence for the restriction

For \(A\ne0\), EXP-123 writes the selected maximal minor as

\[
A^{87}(R+YS).
\]

- If \(R+YS\ne0\), that selected chart covers the point.
- If \(R+YS=0\) and \(S\ne0\), EXP-129 covers the complete rational graph.
- If \(R+YS=0\) and \(S=0\), then \(R=S=0\), and EXP-130 covers the complete
  principal-open base locus.

These cases exhaust \(A\ne0\). The next decisive experiment is therefore the
separate \(A=0\) rank problem, not more sampling of the rational graph or base
locus.

## Scope and non-claims

This experiment proves neither the Jacobian conjecture in dimension two nor a
counterexample. It does not settle the 24-parameter core, the complete
51-parameter family, the degree-\((72,108)\) case, or the planar degree floor.
It closes only the complete \(A\ne0\) part of one declared four-parameter
restriction.

## How could this be wrong?

The certificate depends on the accepted EXP-123 matrix specialization and its
parameter-to-matrix transcription. The source hashes exclude silent artifact
drift, and the direct determinant controls exclude an internal mismatch in the
new section, but neither independently reconstructs the entire 302-by-125
system from the original Jacobian equations. A defect shared by that upstream
transcription and all dependent experiments would survive. The result also says
nothing about \(A=0\), where division by \(A\), \(X\), or the invariant
normalizations used here is unavailable.
