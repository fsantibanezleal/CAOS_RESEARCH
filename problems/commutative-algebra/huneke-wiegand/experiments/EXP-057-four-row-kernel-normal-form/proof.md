# EXP-057 proof record: four-row endpoint reduction and a sign refutation

Date: 2026-09-04. Scope: every integer `p>=8`. P1 is derived below. The declared P3 has the
wrong sign and is refuted symbolically, while its corrected identity is retained. Numerical
stress and independent verification belong to the artifact and verdict.

## 1. Original labels and grading

Use the original presentation `M_p` and

$$L_p=[1,p]\cup[3p,4p-2],\qquad
G_p(a,j;c)=[K,(L_p\setminus\{a,3p,3p+j\})\cup\{6p\};10p+c].$$

The offset after the semicolon in `G_p` is `10p+c`; `c` itself is only the small index used to
write it. These labels are original `K` rows, not coordinates in an HNF kernel basis. Let

$$q_p=[K,(L_p\setminus\{3p,3p+2\})\cup\{6p\};10p].$$

This is an original kernel-domain column: `10p` is a high coefficient, the exterior set has
`2p-2` variables, and its total offset is

$$\sum_{u\in L_p}u-2+10p=4p^2+6p-1.$$

The module and differential are those used in
[EXP-056](../EXP-056-uniform-low-source/proof.md), with the high and degree-two offset sets
defined by [EXP-036](../EXP-036-factor-two-torsion-anatomy/run.py). A `K`-column face contributes
precisely when the removed variable plus the coefficient belongs to the degree-two offset set.

## 2. Complete boundary of one column

There are three kinds of faces of `q_p`.

| Removed variable | Sign | Product offset | Outcome |
|---|---|---|---|
| `a` in `[1,p-2]` | `(-1)^(a-1)` | `10p+a` | degree-two offset, contributes `G_p(a,2;a)` |
| `a=p-1` or `a=p` | `(-1)^(a-1)` | `11p-1` or `11p` | high offset, hence zero |
| present second-low `v` | immaterial | `10p+v` | lies in `[13p+1,14p-2]`, all high, hence zero |
| `6p` | `(-1)^(2p-3)=-1` | `16p` | high offset, hence zero |

The two omitted second-low variables `3p,3p+2` are not faces. This covers every variable in
the exterior set and proves

$$M_pq_p=\sum_{a=1}^{p-2}(-1)^{a-1}G_p(a,2;a). \tag{1}$$

Every row in (1) is distinct and nonzero. Thus its support is exactly `p-2`; in particular,
`M_pq_p` is not the zero vector over the integers.

## 3. Cancellation of the long interval

EXP-056 gives

$$M_ps_p=b_p^A+b_p^B+\gamma_p$$

with

$$\begin{aligned}
\gamma_p={}&-\sum_{a=1}^{p-4}(-1)^{a+1}G_p(a,2;a)
-(-1)^{p+1}G_p(p-3,2;p-3)\\
&-2(-1)^{p+1}G_p(p-2,1;p-3)
-2(-1)^pG_p(p-3,1;p-4).
\end{aligned}$$

For every `1<=a<=p-4`, adding (1) cancels the `G_p(a,2;a)` coefficient exactly. The two
remaining `j=2` positions and the two `j=1` terms give

$$\begin{aligned}
\eta_p:=\gamma_p+M_pq_p=(-1)^p\bigl(&2G_p(p-3,2;p-3)
-G_p(p-2,2;p-2)\\
&+2G_p(p-2,1;p-3)-2G_p(p-3,1;p-4)\bigr). \tag{2}
\end{aligned}$$

The four rows are distinct for every `p>=8`, and every coefficient is nonzero. Their degree-two
offsets are `11p-3`, `11p-2`, `11p-3`, and `11p-4`, respectively, all in
`[10p+1,11p-2]`. This proves P1 and the all-parameter support statement underlying P2.

Exactly one coefficient is odd. Reduction of (2) modulo two therefore has the single-row form

$$\eta_p\bmod2=G_p(p-2,2;p-2)\bmod2. \tag{3}$$

Equation (3) is a statement about a vector. It does not prove that its image in a quotient is
nonzero.

## 4. Declared P3 is false; the plus identity is correct

Since `eta_p=gamma_p+M_pq_p`, linearity gives

$$M_p(s_p+q_p)=b_p^A+b_p^B+\eta_p. \tag{4}$$

The frozen hypothesis instead asserted the minus sign. Its exact error is

$$M_p(s_p-q_p)-(b_p^A+b_p^B+\eta_p)=-2M_pq_p. \tag{5}$$

By (1), (5) has `p-2` distinct nonzero rows with coefficients of absolute value two. Thus the
declared P3 is refuted for every `p>=8`, already at `p=8`, not merely insufficiently verified.
The hypothesis must remain unchanged. The correct replacement (4) is a separately identified
consequence of the retained P1 identity and EXP-056.

## 5. Integral consequence and exact remaining gates

Equations (2) and (4) give, in the full integral cokernel,

$$[\gamma_p]=[\eta_p],\qquad
[b_p^A+b_p^B]=-[\eta_p]. \tag{6}$$

Thus the displayed quadratic-size representative and the `p-1`-row representative from EXP-056
both reduce to an explicit four-row endpoint vector. The correcting source `s_p+q_p` has exactly
`p` distinct terms: `p-1` low-source terms and one kernel-domain term.

If, at a particular parameter, an original source `z_p` satisfies
`M_pz_p=2(b_p^A+b_p^B)`, then

$$M_p\bigl(2(s_p+q_p)-z_p\bigr)=2\eta_p. \tag{7}$$

This implication does not construct such a `z_p` uniformly. Nor does it prove that the class of
`eta_p` is nonzero. A generic dual obstruction, an integral order-two source, a second independent
class, and a torsion upper bound remain separate tasks. In particular, four displayed rows are
not a four-dimensional presentation or a normal form of the whole quotient. The experiment's
folder name must not be read as a claim of such a normal form.

## 6. Validation boundary

The derivation uses every face of the original single column and exact cancellation against the
already derived EXP-056 formula. No ranks, HNF, projected-column relabelling, or finite sequence
extrapolation occur. Independent multiplication must still attack the sign and endpoint logic.
The P3 refutation stops the initial smoke gate; any subsequent stress tests are an explicitly
recorded continuation of retained P1/P2 and corrected (4), not a retroactive confirmation of P3.

Possible errors remain in the imported coefficient-module description or the written face
classification. The separate left-to-right and right-to-left differential implementations and
deliberate coefficient mutations address the latter. They do not establish nonvanishing or a
full connecting-parity theorem. This endpoint reduction alone does not automatically trigger a
new manuscript or Zenodo version under the problem's stronger publication gate.
