# EXP-105: Exact \(\mu_9\)-graded Bézout certificate

## Verdict

**CONFIRMED**, with a compact exact certificate.

Both selected maximal-minor support graphs admit a connected row/column
\(\mathbb Z/9\)-grading. Every nonzero entry term satisfies

\[
e\equiv r_i+c_j\pmod9.
\]

The determinant residue is \(8\) for the EXP-102 chart and \(3\) for the
endpoint-safe chart, exactly matching their valuations \(1628\) and \(777\).

## Exact determinant pair

With \(z=u^9\), removal of the proved monomial valuations and integer contents
gives

\[
F(z)=21-96z-1024z^2
\]

and

\[
G(z)=(8z+1)^{14}.
\]

The second identity was reconstructed from 15 exact integer determinants and
verified independently at \(u=-1\) and \(u=16\).

The only zero of \(G\) is \(z=-1/8\), and

\[
F(-1/8)=17.
\]

Therefore \(F\) and \(G\) are coprime over \(\mathbb Q[z]\). The persisted
integer polynomials \(A,B\) verify

\[
A(z)F(z)+B(z)G(z)=17^{14}
=168377826559400929.
\]

Artifact SHA256:
`A688644B113DD9CDFF852B7113D61ED35E66A8715DBD4D13355E3EECC4BEE35F`.

## Mathematical consequence

The two normalized maximal minors generate the unit ideal over
\(\mathbb Q[u,u^{-1}]\). Hence the augmented matrix has rank \(125\) at every
point of the EXP-101 residual curve. Together with the first two EXP-101
charts, this is a fully exact exclusion of the declared
\(\{(0,1),(1,7)\}\) coefficient slice.

## Scope and next lift

This does not cover the remaining coefficient directions. The newly exposed
grading supplies a principled next filter: test which additional GGHV
coefficient directions admit a consistent variable weight relative to both
row/column gradings. Compatible directions can be added without destroying
the sparse \(u^9\) structure and should be attacked before generic
multivariate elimination.
