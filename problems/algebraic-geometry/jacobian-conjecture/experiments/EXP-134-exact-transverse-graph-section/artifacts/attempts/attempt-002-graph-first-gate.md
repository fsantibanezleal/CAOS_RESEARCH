# Attempt 002 - graph-first cleared determinant reached the gate

Date: 2026-08-01

The worker substituted

`C = -R(A^3,B)/(A^2 S(A^3,B))`

before determinant expansion, retained `A*S != 0` as an explicit chart
condition, and cleared the denominator separately on every cyclic block. The
exact component ledger again contains one block of size 33 and 86 singleton
blocks.

The cleared size-33 determinant over `QQ[A,B,T]` did not complete within the
declared gate. No determinant, `T` coefficient, quotient identity, or graph
coverage statement was produced. The checkpoint and empty/error-free run
logs are retained as null evidence.

The route is retired in favor of the exact rank/root certificate: transverse
rank 7 bounds the determinant degree by 7, so eight exact fixed-`T`
determinants decide constancy without a multivariate `T` expansion.
