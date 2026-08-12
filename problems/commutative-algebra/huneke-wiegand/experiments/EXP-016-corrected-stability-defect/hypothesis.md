# EXP-016 - corrected exact conductor-stability defect

Declared: 2026-08-12, after EXP-015 was refuted and before this experiment's implementation or
execution. Phase HW-P5. Backlog HWB-016.

## Correction and prediction

EXP-015 incorrectly filled the inherited Frobenius gap `13s-1`. For every integer `p>=4`, the
corrected square prediction is

```text
v(T_p^2)=(8s+C_p) union [9s,13s-2] union [13s,infinity).
```

Equivalently, the square retains exactly the old gap at `13s-1` between its level-eight block and
its eventual tail.

For `x=t^(4s)`, predict the complete defect

```text
v(T_p^2) minus v(xT_p)
 = 8s+([p+1,2p] union [4p-1,5p-2])
   union 9s+({2p-1,4p-1} union [4p+1,5p-2])
   union 10s+([0,p] union {2p-1} union [3p,4p-1]
               union [4p+1,5p-2])
   union 11s+[0,s-1]
   union 12s+([2p+1,3p-1] union [5p-1,s-2])
   union {17s-1},
```

and hence

```text
length(T_p^2/xT_p)=14p.
```

## Premise dependencies

- EXP-013 proves the exact value-set blocks of `T_p`.
- EXP-014 proves nonstability, the finite cutoff below `17s`, and the complete 297-parameter
  supporting pattern.
- EXP-015 refutes the overbroad tail precisely at `13s-1` and supplies no positive premise.

## Symbolic proof route

Let `U_p=A_p union B_p`. With `low` and `high` denoting the no-carry and carry residue parts, the
same five affine interval identities declared in EXP-015 determine levels 8 through 12:

```text
low(A+A)=C,
high(A+A) union low(A+U)=[0,s-1],
high(A+U) union low(A+B) union low(U+U)=[0,s-1],
high(A+B) union high(U+U) union low(U+B)=[0,s-1],
high(U+B) union low(B+B) union low(A+C)=[0,s-2].
```

The last identity proves the exclusion of `13s-1`. Multiplication by the minimum value `4s`
copies `[9s,13s-2]` to `[13s,17s-2]`, and

```text
17s-1=(4s+1)+(13s-2)
```

fills the only endpoint missing from `xT_p`; all larger values follow from the tail.

## What PASS and FAIL prove

- A complete affine interval proof plus the tail argument proves the corrected square, defect, and
  length formulas for every `p>=4`.
- Exact agreement through `p=300` is supporting validation only.
- Inclusion of `13s-1`, exclusion of `17s-1`, or any residue/count mismatch refutes the corrected
  theorem.

## Adversarial validation

Two exact routes must agree. The independent auditor reconstructs selected rows. Controls must
reject the EXP-015 false tail, deletion of `17s-1`, and alteration of the level-eight `C_p` block.

## Invariant-first note

The five residue identities and two endpoints decide the all-parameter theorem. No larger search,
SAT model, or symbolic elimination is justified.

## Compute budget and kill criterion

CPU only, exact integer and bitset arithmetic, no randomness. Smoke budget: 10 seconds at
`p=4,5`. Full budget: two minutes through `p=300`. Abort on the first formula, identity, control,
or budget failure. A budget hit is `INCONCLUSIVE`, never theorem evidence.

## Success and failure criteria

Success requires the symbolic proof, the corrected `13s-1` exclusion, exact campaign and audit,
stable hashes, and all corruptions rejected. Any mismatch blocks manuscript promotion.
