# EXP-131 - Direct exact atlas on the A=0 boundary

Declared 2026-07-31 before the verdict-bearing run.

## Question

After specializing the original complete 302-by-125 augmented system directly
at \(A=0\), before dividing by \(A\) or introducing \(X=A^3\) and
\(Y=A^2C\), do finitely many exact maximal minors cover the complete
\((B,C)\)-plane?

## Premise dependencies

1. [MV] EXP-111 identifies the structurally zero constant \(Q\)-column and
   makes rank 125 of the reduced augmented matrix the inconsistency target.
2. [MV] EXP-112 reconstructs the complete 302-row system and its 125 reduced
   augmented columns exactly.
3. [MV] EXP-123 defines the four-coefficient restriction
   \(\{(0,1),(0,5),(1,0),(2,9)\}\) and works on the normalized \(d=1\)
   chart.
4. [MV] EXP-118 closes the separate \(d=0\) quotient boundary.
5. [MV] EXP-123/129/130 close the normalized \(d=1\) sector on \(A\ne0\).

## Falsifiable predictions

1. The direct \(A=0\) system has generic augmented rank 125.
2. A sparse exact pivot selected at \((B,C)=(0,0)\) has a determinant
   independent of \(C\) whose zero divisor has only the linear fibre
   \(5B+4=0\) and the quadratic fibre
   \(25B^2-20B+16=0\).
3. One alternative exact pivot selected on the linear fibre is also
   independent of \(C\) and is nonzero on both residual fibres.
4. The two exact determinant sections have unit gcd over \(\mathbb Q[B]\).

## Method and controls

1. Hash the accepted source scripts and rebuild the complete matrix from the
   original bracket equations.
2. Specialize \(A=0,d=1\) before every normalization. The exact family is
   \(M_0(B,C)=M_{\rm forced}+B M_{(0,5)}+C M_{(2,9)}\).
3. Use modular row selection at two good primes only to choose affordable row
   bases. Reconstruct both 125-by-125 determinants exactly over
   \(\mathbb Q[B,C]\).
4. Factor both determinants, verify their \(C\)-degree is zero, compute the
   exact gcd, and persist an explicit Bezout identity for their squarefree
   divisors.
5. Check both determinant formulas against direct exact determinants at
   rational controls and direct modular ranks on the residual fibres.

## Interpretation gate

If the two exact sections generate the unit ideal, EXP-131 closes the
\(A=0,d=1\) boundary. Together with EXP-118 and EXP-123/129/130 this closes
the declared four-coefficient restriction only. It does not close the
24-parameter cyclic core, the full 51-parameter GGHV family, the complete
\((72,108)\) case, the planar degree floor, or JC(2).

A rank defect, nonunit gcd, or exact-compute stop leaves the boundary open.
Modular ranks alone can never support the verdict.

