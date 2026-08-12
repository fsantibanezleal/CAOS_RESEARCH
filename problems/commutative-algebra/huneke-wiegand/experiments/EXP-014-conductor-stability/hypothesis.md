# EXP-014 - duality audit and conductor stability

Declared: 2026-08-12, before implementation or execution. Phase HW-P5. Backlog HWB-015 and
HWB-016.

## Question and prediction

For every integer `p>=4`, retain the EXP-009 base ring `R_p`, the EXP-011 finite birational
extension `E_p`, and the EXP-013 common conductor/trace ideal

```text
T_p=R_p:E_p=tr_(R_p)(J_p)=tr_(R_p)(E_p).
```

The predictions are:

1. the length equality `length(R_p/T_p)=length(E_p/R_p)` is a specialization of the general
   Gorenstein local-duality identity, not a family-specific novelty claim;
2. `T_p` is not a stable ideal for any `p>=4`;
3. with `x=t^(4s)`, the explicit value `8s+p+1` lies in `T_p^2` but not in `xT_p`;
4. exact finite arithmetic can determine the complete defect set
   `v(T_p^2) minus v(xT_p)` at each tested parameter and test whether its colength has an affine
   or quasipolynomial pattern worth a separately declared theorem experiment.

## Premise dependencies

- EXP-009: `R_p` is one-dimensional Gorenstein.
- EXP-011: `E_p` is a finite birational extension with exact value semigroup.
- EXP-012: `type(E_p)=10p>1`, so `E_p` is not Gorenstein.
- EXP-013: `T_p=R_p:E_p` with an exact value-set formula.
- Herzog-Kumashiro Proposition 3.1 Claim 1: the colength balance follows from local duality.
- Dey Corollary 3.7: over the Gorenstein base, conductor stability is equivalent to the extension
  being Gorenstein.

## Method

1. Write the general duality specialization with its primary citation and verify every hypothesis.
2. Derive nonstability by Dey's criterion and independently by the displayed monomial witness.
3. Implement exact bounded value-set sums for `T_p^2` and `t^(4s)T_p`; prove the finite truncation
   bound from the conductor tails.
4. Run `p=4,...,300`, emitting deterministic row and campaign hashes.
5. Independently reconstruct selected rows and reject a false stable control.

## What PASS and FAIL prove

- The two deductive routes prove nonstability for every `p>=4` if their cited hypotheses and the
  explicit witness are correct.
- A computational PASS supports the finite defect sets only for tested parameters. It cannot by
  itself prove any fitted all-`p` formula.
- If `8s+p+1` belongs to `t^(4s)T_p` at any parameter, the direct witness prediction is refuted.
- If `T_p^2=t^(4s)T_p` at any parameter, both the stability prediction and at least one premise
  application are refuted and the experiment stops.

## Invariant-first note

The type of `E_p` and the single value `8s+p+1` decide nonstability without a sweep. The campaign
is justified only to expose the complete stability defect and formulate the next theorem-level
question. No SAT or symbolic elimination is warranted.

## Compute budget and kill criterion

CPU only, exact integer/set arithmetic, no randomness. Smoke budget: 10 seconds at `p=4,5`.
Full budget: two minutes for `p=4,...,300`. The expected run is below five minutes, so no
checkpoint is required. Abort on a premise or witness mismatch, or at two minutes. A budget hit is
`INCONCLUSIVE` for the defect pattern and does not weaken the deductive nonstability proof.

## Success and failure criteria

Success requires the source-derived duality correction, both all-parameter nonstability routes,
exact finite-tail justification, deterministic artifacts, an independent reconstruction, and a
rejected false-stability control. Any conflict with a primary theorem or prior experiment is
preserved and reconciled before further claims.
