# EXP-114 - Verdict: compact exact factors, a determinant-inert cycle direction, and a weighted residual geometry

Verdict: **confirmed exact factorization**, with one important prediction
refuted.

## Result

Both exact 36-by-36 determinants completed inside budget and passed five direct
determinant checks.

### Triple \(T_A\)

Let
\[
a=\varepsilon_{(0,1)},\quad
b=\varepsilon_{(0,7)},\quad
c=\varepsilon_{(2,9)}.
\]
Although these three directions make the 36-vertex dependency graph strongly
connected, the determinant is independent of \(c\). It factors as
\[
D_A(a,b)=2^{-54}F_3(a,b)F_{12}(a,b)F_6(a,b),
\]
where
\[
F_3=64a^3+336a^2b+588ab^2+343b^3+256,
\]
\[
F_{12}
=2213683584a^4b^8+9441116160a^2b^4
+5931980229ab^{11}+4932501504ab^2+1073741824,
\]
and
\[
\begin{aligned}
F_6={}&4096a^6-21504a^5b+75264a^4b^2-153664a^3b^3
-16384a^3\\
&+230496a^2b^4-86016a^2b-201684ab^5+301056ab^2\\
&+117649b^6-87808b^3+65536.
\end{aligned}
\]
The total degree is 21 and the expanded determinant has only 24 monomials.

This refutes the inference that graph participation implies determinant
dependence. The direction \((2,9)\) is an exact cancellation direction for
this selected minor on \(T_A\).

### Triple \(T_B\)

Let
\[
a=\varepsilon_{(0,1)},\quad
b=\varepsilon_{(0,5)},\quad
d=1+\varepsilon_{(1,0)}.
\]
The determinant factors as
\[
D_B(a,b,d)=2^{-42}G_{54}(a,b,d)H_{63}(a,b,d),
\]
with
\[
\begin{aligned}
G_{54}={}&30720000a^6b^4+48828125a^3b^{11}
+150000000a^3b^8d\\
&+64000000a^3b^5d^2-39321600a^3b^2d^3
+16777216d^6,
\end{aligned}
\]
and
\[
\begin{aligned}
H_{63}={}&4096a^9+184320a^6bd^2-1800000a^3b^5d^3
+1843200a^3b^2d^4\\
&+1953125b^9d^4+3000000b^6d^5+1536000b^3d^6
+262144d^7.
\end{aligned}
\]

These factors are weighted homogeneous for
\[
\operatorname{wt}(a,b,d)=(7,3,9),
\]
of weighted degrees 54 and 63. On the forced axis they recover
\[
D_B(0,0,d)=d^{13}.
\]
The expanded determinant has total degree 27 and 181 monomials, but the shifted
weighted form has only 18 and 39 monomials in its two factors.

## Main insight

The graph reduction and determinant reduction are distinct:

- SCC analysis reduces where dependence can occur;
- exact determinant computation can eliminate graph-active directions by
  cancellation;
- after the forced shift \(d=1+\varepsilon_{(1,0)}\), the surviving algebra is
  governed by a torus grading with weights \((7,3,9)\).

This gives a better next object than another raw coefficient slice. The residual
union
\[
V(G_{54})\cup V(H_{63})
\]
has a weighted-projective description. On \(d\ne0\), torus normalization can
reduce one dimension. The boundary \(d=0\) is explicit and must be covered by
an alternative augmented minor, using the complete 302-row system.

## What this proves

- The selected augmented minor is exactly nonzero away from the displayed
  factor loci on both declared triples.
- Full graph connectivity can coexist with complete determinant cancellation
  of one direction.
- \(T_B\)'s residual geometry is quasi-homogeneous after the forced shift.
- The 36-core reconnaissance passed decisively: exact factors are compact
  enough for chart selection.

## What this does not prove

- Neither triple closes the 24-parameter core or the full family.
- Factorization of one selected minor does not certify points on its factor
  loci.
- The weighted action must be verified on alternative minors before it is used
  as a chart-cover theorem.
- JC(2), \((72,108)\), and the floor remain open.

## Adversarial validation

- Each symbolic determinant agrees with five direct exact 36-by-36
  determinants.
- Both determinants equal one at the pinned origin.
- \(T_B\) independently recovers the forced-axis exponent 13 on the core.
- Factorization is over \(\mathbb Q\), with primitive factors persisted in the
  artifact.

## How could this be wrong?

- The factors belong to EXP-112's pinned selected minor, not the entire
  augmented determinantal ideal.
- The weighted-homogeneous reading uses the shifted coordinate
  \(d=1+\varepsilon_{(1,0)}\); it is not a grading of the original unshifted
  parameter ring.
- A graph-inert or determinant-inert direction for one chart may reappear in
  another chart.

## Strategy consequence

Prioritize a weighted residual-chart experiment on \(T_B\):

1. split \(d\ne0\) from \(d=0\);
2. use weights \((7,3,9)\) to normalize the open chart;
3. select alternative complete-row minors on each primitive factor;
4. test their gcd or residual ideals exactly.

The boundary-divisor route remains second priority. Blind coefficient-slice
enumeration remains demoted.
