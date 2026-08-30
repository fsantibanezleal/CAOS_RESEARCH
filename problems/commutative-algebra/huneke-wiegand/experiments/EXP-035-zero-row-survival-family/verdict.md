# EXP-035 verdict - CONFIRMED WITH P3 MECHANISM REFUTED

Date: 2026-08-30. Backlog: HWB-035 and HWB-058.

## Decision

**CONFIRMED for P1/P2 and for a stronger exact finite target; P3's declared coordinatewise
survival mechanism is REFUTED.**

For every `p>=4`, all primitive zero rows of the EXP-034 incidence cokernel are classified by

```text
R_b subset F.
```

Their exact coordinate-summand rank in homological degree `i` is

```text
z_(p,i)=sum_(b in B_p, |R_b|<=i) binom(10p-1-|R_b|,i-|R_b|).  (1)
```

The block

```text
b=10p+t,
F=[3p,4p-2] union {t} union [t+2,p],
2<=t<=p-2                                                     (2)
```

gives a primitive `K_p` class in every homological degree `p+1,...,2p-3`.

The first connecting smoke case contains an explicit integral source cycle, so the selected
coordinate itself is hit. However, the complete multidegree contains other classes and yields the
strongest finding of the round:

```text
beta_(5,(7,87))(K_4)=5 over GF(2),  4 over GF(3),
beta_(5,(7,87))(A_4)=4 over GF(2),  3 over GF(3),
beta_(5,(7,87))(C_4)=4 over GF(2),  3 over GF(3).              (3)
```

Thus all three lower multigraded Betti tables are characteristic-dependent. The integral kernel
cokernel is `Z^4 direct-sum Z/2Z` in this component.

## What changed

EXP-034 found one characteristic-free class by a unique unit pivot. EXP-035 shows that this
mechanism is exceptional: the next zero row is reached by an integral connecting cycle. A full
quotient calculation nevertheless leaves three odd-characteristic classes and four
characteristic-two classes. The failed extrapolation exposed genuine `2`-torsion rather than
eliminating the target.

## Gate record

| gate | result |
|---|---|
| declaration before implementation | PASS; declaration commit `4c43344` precedes all EXP-035 code |
| frozen premises | PASS; EXP-032/033/034 hashes match |
| canonical zero-row campaign | PASS for all 297 parameters in 51.889 seconds |
| mandatory smoke | P3 mechanism REFUTED at `(p,t)=(4,2)` by a persisted ten-term integral cycle |
| complete target quotient | PASS; all `79` cokernel rows, `119` kernel columns, and `710` source columns included |
| exact field ranks | PASS over `GF(2)`, `GF(3)`, `GF(5)`, and `GF(1000003)` |
| Smith certificate | PASS; free rank four and one invariant factor `2` |
| independent reconstruction | PASS; semigroup-derived bases, reversed pivots, all hashes and ranks agree |
| symbolic route | PASS; nine interval obligations UNSAT and all formulas exact |
| cubic-cone transfer | PASS; the shifted diagonal begins at offset `102>75` |

Aggregates and artifact hashes:

```text
classification  cc98154e60bdc00fe1f503020aa7d5c66b53ff0cc4ce2158f199d03c2a5fda8b
target          4072a9fb7844d07763fae1b08e99da3d94d38cf3a40f980316c38f0931091276
independent     b92e787bc120b5fa12aac1fc4a10792883e699ed7315055958f3916e8d10b60b
symbolic        b1bfc105f3e9ace368f181ccf10f367fe1f4d23199e49c14275bd8e9b941569e
```

## How could this be wrong?

- The connecting quotient uses the reduced exact sequence and the EXP-034 multiplication model.
  A defect in those frozen premises would invalidate the interpretation, although their hashes,
  earlier independent reconstruction, and current semigroup audit all pass.
- The ranks are exact, not floating point. The independent route changes basis construction,
  iteration order, and pivot order, but both implementations are Python. The Smith form supplies
  a third integral check for the kernel torsion.
- Equation (3) is proved only for `p=4`. The all-parameter result is the zero-row family (1)-(2),
  not characteristic dependence for every family member.
- The result is multigraded. No complete ordinary lower strand or full resolution is claimed.

## Strategy consequence

The next strongest path is torsion anatomy, not another coordinatewise pivot sweep:

1. determine whether the `Z/2` class extends to `p>4` or other zero-row multidegrees;
2. construct a compact integral cycle/cocycle certificate for the `p=4` torsion class;
3. separate free zero-row summands from torsion-producing incidence subcomplexes;
4. retain full target quotient ranks whenever connecting cycles occur.

The naive maximal-rank model remains refuted. The consecutive all-parameter survival statement is
not claimed.

## Publication decision

The publication trigger is crossed. Equation (3) changes the published lower-strand boundary and
identifies characteristic dependence in the first family member, while (1)-(2) add a reusable
integral incidence theorem. Incorporate both in the existing main manuscript as v0.22, with the
refuted P3 mechanism stated explicitly. A separate manuscript remains deferred until torsion is
classified beyond `p=4` or the incidence method completes a strand.

