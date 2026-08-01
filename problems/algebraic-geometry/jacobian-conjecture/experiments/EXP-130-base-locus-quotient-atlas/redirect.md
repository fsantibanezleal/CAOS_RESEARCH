# EXP-130 redirect after the generic Groebner gate

## Trigger

The first exact worker reached its declared 300-second gate after completing
both projection resultants but before completing the generic rational Groebner
basis. The orchestrator recorded
`stopped_at_algebra_worker_timeout`. No quotient-dimension or radical claim is
promoted from that attempt.

## Exact information retained

Both projection resultants have degree 117. Their exact factorizations have the
same degree and multiplicity pattern:

\[
B^{27}P_3(B)P_6(B)P_{12}(B)P_{69}(B),
\]

and

\[
X^{27}Q_3(X)Q_6(X)Q_{12}(X)Q_{69}(X).
\]

The four non-coordinate factors are squarefree and have total degree 90. This
is exact projection evidence, not yet a same-point or quotient-algebra proof.

## Redirect

Do not retry the same generic Groebner computation. Compute the subresultant
sequence in \(X\) once, then reduce it independently modulo each of
\(P_3,P_6,P_{12},P_{69}\). On a block where the specialized gcd is linear in
\(X\), reconstruct the exact \(X\)-class in \(\mathbb Q[B]/(P_d)\). Verify it
by direct substitution into both \(R\) and \(S\), then compare its norm and
minimal polynomial with the corresponding \(Q_d\) block.

The coordinate block is checked separately by direct \(X=0\) and \(B=0\)
specialization. If all four principal-open blocks reconstruct, their CRT
product is the saturated finite algebra of dimension 90 without a generic
ambient basis computation.

## Proof boundary

The factor pattern alone does not prove that the scheme is reduced, that the
degree-matched factors describe the same points, or that the maximal-minor
atlas covers them. Those are the next exact gates.

