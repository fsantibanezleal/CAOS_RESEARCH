# EXP-121 - Verdict: one shared exact chart closes both \(L\) and \(Q\)

## Decision

**CONFIRMED, with two quantitative predictions refuted.**

One row basis selected independently on the finite \(L\) and \(Q\) residual
schemes turns out to be the same 125-row basis. Its exact determinant closes
both residuals over \(\mathbb Q[X,B]\), where \(X=A^3\).

Together with EXP-118's complete \(d=0\) quotient-boundary cover and
EXP-120's \(G\)-component cover, this closes the complete three-parameter
\(T_B\) restriction.

It does **not** close the 24-parameter cyclic core, the full 51-parameter
family, the \((72,108)\) case, the planar degree floor, or \(JC(2)\).

## Exact result

The complete system is the 302-by-125 augmented matrix from EXP-115.
Modular selection found:

- on \(L\), 13 affine residual lifts at \(p=1013\), all with rank profile
  \(124/125\) for the coefficient/augmented systems;
- on \(Q\), 18 affine residual lifts at \(p=1033\), again with profile
  \(124/125\);
- the deterministic independent-row extraction returns the same 125-row
  basis on both components.

The selected basis differs from the pinned basis by 68 rows. At the rational
anchor \((A,B,d)=(1,0,1)\), its exact determinant is nonzero. The dependency
graph has one cyclic block of size 26 and 85 singleton blocks. Exact block
reconstruction gives a determinant with:

- total degree 108 in \(A,B\);
- 23 monomials;
- coordinate factor \(A^{87}\);
- exact semi-invariant descent
  \[
  D(A,B)=A^{87}R(A^3,B),
  \]
  where \(R(X,B)\) has \(X\)-degree 5, \(B\)-degree 18, and 23 monomials.

Five direct 125-by-125 determinant evaluations agree with the reconstructed
block product.

## \(L\)-component certificate

The exact graded-reverse-lexicographic basis of
\[
(L,\Delta_{LQ},D)
\subset\mathbb Q[X,B]
\]
is \([1]\). The computation took 4.71 seconds. Hence no point of the finite
\(L\) residual survives the new chart.

## \(Q\)-component certificate

A raw Gröbner basis for \((Q,\Delta_{LQ},D)\) exceeded the declared
240-second component gate and was stopped. The stopped output is retained as
attempt 3. The exact zero-set split is substantially smaller.

The first alternative determinant has coordinate multiplicity
\[
\Delta_{LQ}=B^{36}\Delta^\circ.
\]
Therefore its zero set is the union of \(B=0\) and
\(\Delta^\circ=0\).

On \(B=0\),
\[
Q(X,0)=256X^2-1024X+4096,\qquad D(X,0)=X^{32},
\]
and their exact univariate gcd is 1.

On \(\Delta^\circ=0\), reduce both \(\Delta^\circ\) and \(D\) modulo the
quadratic \(Q\). Both remainders are linear in \(X\):
\[
\overline{\Delta^\circ}=a(B)X+c(B),\qquad
\overline D=u(B)X+v(B).
\]
The exact checks are:

- \(\deg(a),\deg(c)=(69,72)\) and \(\gcd(a,c)=1\), so the exceptional case
  \(a=c=0\) is empty;
- substituting \(X=-c/a\) into \(Q\) gives a degree-144 compatibility
  polynomial with 145 monomials;
- compatibility with \(\overline D\) gives a degree-176 polynomial with
  176 monomials;
- the exact gcd of those two compatibility polynomials in
  \(\mathbb Q[B]\) is 1.

Thus the quotient branch is also empty. This proves
\[
(Q,\Delta_{LQ},D)=(1)
\]
set-theoretically and ideal-theoretically over the algebraic closure. The
split certificate took 0.70 seconds.

The persisted compatibility-polynomial hashes are:

- degree 144:
  `0822384E01F2DEE554143628C3604486AE9D932FC3CA8FD42986E07C15D9A206`;
- degree 176:
  `8737A127986AA5B5FB6B969967EF3F781B9C2D39F8F1079EA4AC3485EDFEA6EE`.

## Prediction adjudication

1. **Refuted as stated.** \(L\) has residual lifts among the first four
   primes, but \(Q\)'s first retained affine lifts occur at \(p=1033\), after
   the original four-prime list.
2. **Refuted.** The shared basis needs 68, not at most 10, row replacements.
3. **Confirmed.** The largest cyclic SCC is 26, below the gate 60.
4. **Confirmed.** The determinant descends exactly through \(X=A^3\) and has
   only 23 monomials.
5. **Confirmed more strongly.** Both components close after the first new
   chart.
6. **Superseded by closure.** No finite residual or smaller eliminant remains.

## Failed attempts retained

- Attempt 1 searched only the first four declared primes. It found no affine
  \(Q\)-lift and correctly failed before an exact claim.
- Attempt 2 added primes and found \(Q\)-lifts, but a global deduplication set
  incorrectly rejected the row basis already selected on \(L\). Componentwise
  deduplication exposed the shared-basis phenomenon.
- Attempt 3 reconstructed the exact determinant and closed \(L\), then the
  raw \(Q\) Gröbner calculation exceeded its 240-second gate. It was stopped
  and replaced by the exact \(B^{36}\) split certificate above.

## Reproduction

From this experiment directory:

```powershell
python run.py
```

The accepted run completed in 44.57 seconds and wrote
`artifacts/results.json` with SHA-256
`72C5AC79DE29D59E89D0D5AC5527EEA760C078B2E2D4FCA13568E2A6DB5F79CE`.

## Next direction

Do not add more charts to this three-parameter restriction: it is closed.
Return to the actual unresolved target, the 24-parameter cyclic core inside
the 51-parameter family. The strongest immediate reuse is structural:

1. treat the EXP-121 shared-basis phenomenon as evidence that finite-stratum
   row selection can jump across apparently different components;
2. search for a constructible cover on a higher-dimensional restriction of
   the 24-parameter core, with explicit proof that the restriction advances
   family coverage;
3. keep the complete \(T_B\) cover as a regression certificate, not as a
   substitute for all-parameter coverage.
