# EXP-104: The complete residual curve is covered

## Verdict

**CONFIRMED: complete two-parameter slice exclusion.**

The EXP-102 determinant was evaluated exactly at 100 integer points. After
division by the proved assignment monomial \(u^{1547}\), exact interpolation
gave a degree-99 integer polynomial whose coefficients 0 through 80 vanish
and whose coefficient 81 is nonzero. Independent evaluations at \(u=101\) and
\(u=-1\) agree.

Therefore the exact determinant support is

\[
[1628,1646].
\]

Its primitive normalized polynomial is the trinomial

\[
21-96u^9-1024u^{18}.
\]

## Determinantal-divisor certificate

An independently selected \(u=2\) row chart has exact assignment and modular
support \([777,903]\). After the proved monomial valuations are removed, the
two determinants have gcd \(1\) modulo both

\[
998244353\quad\text{and}\quad1004535809.
\]

For the first determinant, exact interpolation supplies the endpoint proof.
For the second, both assignment endpoints are attained modulo each prime.
Thus neither a leading-degree drop nor an artificial modular monomial can
hide a characteristic-zero common divisor. The exact gcd of these two minors
over \(\mathbb Q[u]\) is \(1\).

Consequently the augmented matrix has rank \(125\) for every \(u\ne0\) on the
EXP-101 residual curve. Together with EXP-101's first two charts, the entire
declared coefficient slice \(\{(0,1),(1,7)\}\) is
inconsistency-certified.

Artifact SHA256:
`99761ED83060E6337420CE6E696ACBF8E7081E584C9967396C8693B7954942D5`.

## Scope

This closes one exact two-coefficient slice. It does not cover the other GGHV
coefficient directions, exclude the full \((72,108)\) family, raise the
literature floor, or decide \(JC(2)\).

## New structural clue

Both reconstructed determinant supports lie in one residue class modulo 9.
The first primitive factor is quadratic in \(z=u^9\), while the second modular
minor has degree 14 in \(z\). EXP-105 tests and exploits the corresponding
row/column \(\mathbb Z/9\)-grading to replace the modular proof with a compact
exact Bézout identity.
