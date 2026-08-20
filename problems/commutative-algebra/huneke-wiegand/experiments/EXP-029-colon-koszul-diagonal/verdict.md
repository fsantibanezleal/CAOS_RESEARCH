# EXP-029 verdict - CONFIRMED

Date: 2026-08-20. Backlog: HWB-035.

## Result

For every integer `p>=4` and every field,

```text
beta_(3,5)=binom(8p,2)=4p(8p-1).
```

If `H_p={a in G_p:a>=6p}`, then

```text
beta_(3,(5,b))=#{ {a,c} subset H_p:a<c and a+c=b-3p }.
```

The support is `[15p+1,39p-3] minus {33p-1}`. Integral relative matching gives a free basis
indexed by unordered pairs of the `8p` high cubic-colon variables, so there is no characteristic
exception.

Together with EXP-028 and the exact Hilbert numerator, this completes internal degree five:

```text
beta_(2,5)=p(2p-3),
beta_(3,5)=4p(8p-1),
beta_(4,5)=2p(5p-1)(10p-3)(100p^2-110p+13)/3,
beta_(i,5)=0 otherwise.
```

This is a new complete diagonal and a colon-Koszul mechanism. It does not complete the third
homological row, the full Betti table, or any broader classification.

## Evidence

- all-parameter integral relative-chain normal form with unit transient-triangle cancellations;
- primitive pair basis identified independently by the exact linear cubic colon;
- 297-row formula, support, and coefficient campaign;
- complete exact `H_2` profiles at `p=4,5,6`, totaling `496,780,1128`;
- two unrelated field characteristics for the complete `p=4` profile;
- independent rational ranks at the left boundary;
- arithmetic/Z3 interval and coefficient certificate through `p=10000`;
- frozen premises and adversarial mutation controls.

Canonical aggregates:

```text
campaign: 7564f15534e8a29f875a367d3a324b95041e8eef836d15deac3e35130e1ad37d
audit:    337854eef5d773c84cdd79c7734e63b295fa0337c5a1852e652559c334949b04
symbolic: 605733497d6fb0ead97bfd25e26daaa66d546c297751960e1c427f29ff69f279
```

The first `p<=10000` symbolic attempt crossed its route budget because it materialized every
integer in each support. It is preserved as `INCONCLUSIVE_BUDGET` and is not evidence. The
constant-memory affine-endpoint implementation passed the same obligations.

## How could this be wrong?

- The integral theorem depends on the exhaustive least-toggle interval classification in Lemma
  2.1. A missed endpoint family could invalidate completeness even though all finite profiles
  pass.
- The EXP-023 symbolic presentation retains its disclosed Z3 UNSAT trust boundary. EXP-029 freezes
  that premise rather than removing it.
- The result concerns this explicit conductor special-fiber family. It is not a theorem for all
  numerical semigroup rings or all Huneke-Wiegand counterexamples.

The independent rational route, two-field smoke, symbolic endpoint certificate, and mapping-cone
identification specifically attack the first two residual risks, but only the written integral
case analysis carries the all-parameter claim.

## Consequence and next gate

All declared gates pass, so EXP-029 is CONFIRMED. The result completes a second full diagonal and
adds a distinct colon-Koszul mechanism. It triggers a main-manuscript expansion and Zenodo new
version under the existing concept DOI. A separate manuscript remains deferred until a
substantial part of the remaining third row or a transferable theorem is proved.

