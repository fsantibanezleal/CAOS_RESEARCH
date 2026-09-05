# EXP-058 proof record: an exact local-source obstruction

Date: 2026-09-05. Status: P1 is **REFUTED at p=8** in the complete declared radius-two source
span. P2 is **NOT APPLICABLE**, because no integral witness was retained. No claim about the
full original source span or an all-parameter torsion theorem follows.

## 1. Target and finite scope

EXP-057 defines

$$G_p(a,j;c)=[K,(L_p\setminus\{a,3p,3p+j\})\cup\{6p\};10p+c]$$

and the four-row endpoint vector

$$\eta_p=(-1)^p\bigl(
2G_p(p-3,2;p-3)-G_p(p-2,2;p-2)
+2G_p(p-2,1;p-3)-2G_p(p-3,1;p-4)\bigr).$$

Here `L_p=[1,p] union [3p,4p-2]`. Its uniform original-cokernel identity is
`[b_p^A+b_p^B]=-[eta_p]`, as proved in
[EXP-057](../EXP-057-four-row-kernel-normal-form/proof.md). The present target is `t_p=2eta_p`.

Let `C_0` be empty and let `F_0` be the four target rows. At radius `r=1,2`, enumerate every
original source column incident to the current frontier `F_(r-1)`, add it to the cumulative
column set `C_r`, and retain its entire original boundary. The next frontier consists of all
boundary rows seen so far except the rows already expanded. This is the frozen row-column-row
radius convention, not a restriction to the four target equations.

All rows outside the target support have right-hand side zero. Thus exact image membership is
tested in the complete row space reached by the chosen source columns.

## 2. Why the inverse incidence enumeration is complete

For an original target row with exterior set `E` and offset `b`, any source incident to it
must have exterior set `E union {v}` for a nonzero generator `v` outside `E`. Its coefficient
must be `c=b-v`, by preservation of total offset.

- For a `K` row, the source is a `K` source when `c` is high. It is an `S` source when `v`
  is high and `c` is low.
- For a `D` row of coefficient kind `A` or `B`, both `v` and `c` are low, and their low
  product must have precisely that kind and offset.

These alternatives exhaust the original differential. The face sign is
`(-1)^(number of elements of E smaller than v)`. The coefficient `c` is allowed to occur in
the exterior; only an exterior variable may not be repeated.

The producer enumerates `v` first. The independent auditor enumerates allowable coefficients
`c` first and recovers `v=b-c`, then independently compares all resulting source labels and
complete boundary coefficients. The difference in enumeration direction is deliberate.

## 3. Completed neighborhoods and separating certificates

Only `p=8` was evaluated. Both prescribed neighborhoods completed without reaching a size or
resource cap:

| Radius | Cumulative source columns | Full boundary rows | Nonzero incidences | Integer dual support | Pairing with `2eta_8` |
|---:|---:|---:|---:|---:|---:|
| 1 | 47 | 240 | 306 | 14 | 4 |
| 2 | 330 | 1803 | 2669 | 40 | 4 |

Write `M_(8,r)` for the original matrix restricted only in its source columns to `C_r`, with
all their boundary rows retained. Each artifact contains an integer row functional `lambda_r`
with coefficients in `{-1,1}` satisfying

$$\lambda_r M_{8,r}=0,\qquad \lambda_r(2\eta_8)=4. \tag{1}$$

If a rational source `v` in this local span solved `M_(8,r)v=2eta_8`, applying `lambda_r`
would give `0=4`. Hence the target is outside the local rational image, and therefore outside
the local integral image. Radius one alone would not refute the declared radius-two prediction;
the complete radius-two certificate does. The runner stopped there as required, without testing
`p=9` or `p=10`.

The radius-two dual consists of 35 `D` rows and five `K` rows. Its sole nonzero target pairing
comes from

$$G_8(5,1;4)=[K,\{1,2,3,4,6,7,8,26,27,28,29,30,48\};84].$$

This row has coefficient `-4` in `2eta_8` and coefficient `-1` in the dual, giving the pairing
four in (1). The other three target rows pair to zero. This is a rational image obstruction,
not a mod-two detector of the intended torsion class.

## 4. Provenance and the independent validation boundary

The exact rational producer uses unit-first pivots and retains source provenance for every
reduced vector. A stored partial source `v_0` and residual `r_0` have the literal meaning

$$r_0=2\eta_8-M_{8,r}v_0$$

in original row coordinates, not in an opaque transformed coordinate system. Both completed
neighborhoods have four-term partial sources and four-row nonzero residuals.

The independent audit reconstructs all 47 and 330 source columns, all 306 and 2669 incidences,
both complete frontiers, both original-coordinate residuals, and both integer duals. It verifies
(1) directly against every selected column and the independently reconstructed four-term
target. Perturbing a nonzero dual coefficient by one is rejected in both neighborhoods.

No independent rank computation is claimed. It is unnecessary for the conclusion: a verified
annihilating functional with nonzero target pairing already proves rational inconsistency.
There is no retained integral witness, so the P2 witness-mutation test is not applicable. A
successful independent audit of the refutation must not be reported as a successful P2 witness.

The source and audit scripts, pinned premises, complete labels, integer certificates, and hashes
are in [results.json](artifacts/results.json) and
[audit-results.json](artifacts/audit-results.json).

## 5. Escaping-column necessary condition

The local dual gives a precise constraint on any future larger source construction.

**Lemma.** Let `C` be a selected source set in an original presentation `M`, and let an integer
functional `lambda`, extended by zero to all other original target rows, satisfy
`lambda M_C=0` and `lambda t != 0`. If a finitely supported source `v` anywhere in the full
original domain satisfies `Mv=t`, then its support contains a column `c` outside `C` such that
`lambda M(c) != 0`.

**Proof.** Write `v=sum_c v_c c`. Linearity gives

$$0\ne\lambda t=\sum_c v_c\lambda M(c)
=\sum_{c\notin C}v_c\lambda M(c).$$

At least one summand in the final sum is nonzero, proving the assertion. This works over both
the integers and the rationals. The existence of such a column alone does not suffice to solve
the full system.

For EXP-058, any full source for `2eta_8` must therefore include a column outside the complete
radius-two set with nonzero pairing against the persisted 40-row dual. A new column with zero
pairing cannot by itself remove this obstruction. This suggests prioritizing inverse neighbors
of the dual support in a separately declared search, checking the pairing before elimination.

No such escaping column or third-radius neighborhood was computed here. The lemma does not
force a particular coefficient type or semantic atom, and the finite dual has no proved
all-parameter formula.

## 6. What is and is not established

The universal training prediction P1 fails at its first parameter because the prescribed
radius-two span excludes the target even over the rationals. This does not exclude an integral
source using more distant original columns. It does not disprove the earlier uniform endpoint
identities, prove nonzero full-cokernel class, or decide the global order of that class. The
all-parameter connecting-parity problem remains open.

The declared budget remains one CPU process, at most 60 seconds and 1 GiB private memory,
1200 source columns and 20000 incidences per parameter. Both completed neighborhoods were well
inside the size caps. No HNF, Smith form, global basis enumeration, old HNF source, or original
`p=11` source data were used. Twelve focused producer tests and Ruff passed; tests write only
temporary outputs. The publication gate is unchanged: this local refutation is not by itself a
new manuscript or Zenodo trigger.
