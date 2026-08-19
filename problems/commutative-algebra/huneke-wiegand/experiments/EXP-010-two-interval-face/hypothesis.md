# EXP-010 - two-interval Kunz-face search

Declared 2026-08-10 before implementation or solver queries. Renumbered before computation when
the earlier EXP-009 growing-interval construction landed concurrently. Phase HW-P4, Route A
redirection. Trigger: EXP-008 proves that fixed-width carried coverage fails uniformly from `q=9`
onward. EXP-010 is secondary to EXP-009 and runs only if the stronger explicit construction does
not close the family question.

## Question

Can the level-4 block remain a two-interval affine object if its widths are allowed to scale, while
the level-6 selector block is solved exactly?

## Structural ansatz

For integers `q>=9`, set `s=4q+2`. For an integer `a` with `0<=a<=q-1`, define

```text
A(q,a) = [0,a] union [2q+1,4q-2a].
```

This is not an arbitrary template. If `A=[0,a] union [b,c]`, symmetry defines
`C=[0,s-1] minus (s-1-A)`, and the low closure/rigidity layer asks

```text
(A+A) intersect [0,s-1] = C.
```

Matching the two interval components forces `b=s/2=2q+1` and `c=s-2-2a=4q-2a`.
Thus `A(q,a)` is the complete two-interval solution of that endpoint-matching architecture,
subject to later additive layers.

For each fixed `(q,a)`, keep the EXP-006 Route K conditions

```text
F=13s-1,
m=4s,
[5s,6s-1] contained in Gamma,
I=(1,t^s) rigid,
```

pin level-4 membership exactly to `A(q,a)`, and leave level 6 and all higher membership Boolean.

## Predictions and gates

- P1: at least three values `q>=9` admit a SAT model for some `a`, reopening an affine-ray
  extraction attempt after EXP-008.
- P2: every SAT model has the exact pinned `A(q,a)`, passes the independent semigroup/rigidity
  checker, and has the symmetry-forced `|B|=s/2` with `A intersect B` empty.
- P3: the smallest feasible `a` or largest feasible `a` across consecutive `q` follows an affine
  or residue-class law. This is exploratory and may be refuted.
- P4: if no `a` is feasible at a given `q`, that complete row requires accepted proofs for every
  `a`; solver absence without certificates is `UNKNOWN`.
- P5: even a recurrent feasible `a(q)` is not an infinite family until explicit `B(q)` rules and
  all four additive cover layers are proved.

## One-sidedness

- A decoded SAT model proves one exact finite two-interval instance.
- A complete row of checked UNSAT proofs excludes this two-interval architecture at that `q`.
- A finite sequence of SAT rows suggests, but does not prove, a family.
- Failure of this architecture does not contradict the broad Route K models already proved at
  the same shifts.

## Method

1. Sweep `q=9,...,24` in ascending order.
2. Sweep `a=0,...,q-1` in deterministic order, with invariant pruning recorded explicitly.
3. Build the full Route K CNF and pin every level-4 literal to `A(q,a)`.
4. Use CaDiCaL. Decode SAT with the independent exact checker. Retain and check DRAT proofs for
   every UNSAT result needed to close a row.
5. Stop a row after the first SAT model for recurrence discovery; revisit full feasible-`a`
   classification only if the boundary is mathematically load-bearing.
6. Compare normalized `B` blocks and additive cover intervals across SAT rows.

## Budget and stop rules

- Per query: 300 seconds. Total: two hours.
- Initial smoke row: `q=9`, with flushed progress and atomic checkpoint.
- Stop the entire campaign on an `UNKNOWN`; later rows are unresolved.
- Stop after three consecutive SAT rows for an extraction checkpoint, or after the first
  proof-complete all-UNSAT row for an obstruction verdict.
- CPU only, exact Boolean/integer arithmetic, no random seeds.

## Adversarial validation

- Reconstruct the `q=7,a=5` EXP-008 model as an out-of-range calibration before the declared
  search.
- Flip one pinned `A` literal in every SAT model and require rejection.
- Rebuild every load-bearing formula and freshly recheck every UNSAT proof in a separate audit.

## Exploration moment

EXP-008 showed that the correct invariant is not visual block similarity but endpoint coverage in
four additive layers. EXP-010 moves from one guessed ray to a classified low-dimensional Kunz
face: `A` is derived from the layer-8 identity, while SAT is used only to decide whether a
compatible `B` exists. The next recognition target is the feasible region in `(q,a)`.
