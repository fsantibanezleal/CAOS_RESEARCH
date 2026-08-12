# EXP-015 - exact conductor-stability defect

Declared: 2026-08-12, after EXP-014 and before implementation or execution. Phase HW-P5.
Backlog HWB-016.

## Question and prediction

For every integer `p>=4`, put `s=6p`, retain the exact EXP-013 conductor `T_p`, and set
`x=t^(4s)`. Predict

```text
v(T_p^2)=(8s+C_p) union [9s,infinity).
```

Consequently the complete stability-defect set is

```text
v(T_p^2) minus v(xT_p)
 = 8s+([p+1,2p] union [4p-1,5p-2])
   union 9s+({2p-1,4p-1} union [4p+1,5p-2])
   union 10s+([0,p] union {2p-1} union [3p,4p-1]
               union [4p+1,5p-2])
   union 11s+[0,s-1]
   union 12s+([2p+1,3p-1] union [5p-1,s-2])
   union {17s-1}.
```

The predicted length is

```text
length(T_p^2/xT_p)=14p.
```

## Premise dependencies

- EXP-013 proves the exact value-set blocks of `T_p`.
- EXP-014 proves the quotient is decided below `17s`, proves nonstability independently, and
  supplies finite evidence for the displayed formula.

The formula and length `14p` are new hypotheses. EXP-014's finite pattern is not treated as their
proof.

## Symbolic proof route

Let `U_p=A_p union B_p`, and for residue sets `X,Y subset [0,s-1]` write

```text
low(X+Y)={x+y<s},
high(X+Y)={x+y-s:x+y>=s}.
```

The load-bearing prediction reduces to five affine interval identities:

```text
low(A+A)=C,
high(A+A) union low(A+U)=[0,s-1],
high(A+U) union low(A+B) union low(U+U)=[0,s-1],
high(A+B) union high(U+U) union low(U+B)=[0,s-1],
high(U+B) union low(B+B) union low(A+C)=[0,s-2].
```

They determine levels 8 through 12 of `T_p^2`. Levels 13 onward follow from the EXP-013 full
blocks and the additional endpoint identity

```text
17s-1=(4s+1)+(13s-2).
```

## What PASS and FAIL prove

- A complete interval proof of all five identities plus the tail argument proves the displayed
  square and defect formulas for every `p>=4`.
- Exact computational agreement through `p=300` supports the implementation but cannot replace
  that proof.
- Any missing residue, extra residue, or count mismatch refutes the formula at that parameter.
- Failure of an interval identity stops the theorem claim even if the campaign passes.

## Adversarial validation

1. Route A reconstructs `T_p^2` by pairwise Boolean Minkowski sums.
2. Route B evaluates the five low/high identities independently.
3. The auditor reconstructs selected complete defects without importing either route.
4. Controls delete `17s-1`, inject `13s-1` into `xT_p`, and alter one endpoint of `C_p`; each
   must be rejected.

## Invariant-first note

The level structure, not a larger parameter sweep, decides the problem. Once the five residue
identities are proved, the quotient length is the sum `2p+p+3p+6p+(2p-1)+1=14p`.

## Compute budget and kill criterion

CPU only, exact integer and bitset arithmetic, no randomness. Smoke budget: 10 seconds at
`p=4,5`. Full budget: two minutes through `p=300`. Abort on the first identity, formula, control,
or budget failure. A budget hit is `INCONCLUSIVE` computationally and does not affect a completed
symbolic proof.

## Success and failure criteria

Success requires the all-parameter interval proof, exact square and defect formulas, both finite
routes through all 297 parameters, stable hashes, an independent audit, and all corruptions
rejected. Any mismatch is preserved in the verdict and blocks manuscript promotion.
