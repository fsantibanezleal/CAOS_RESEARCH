# EXP-007 projected-enumeration proof boundary

## Mathematical variables

For fixed odd `F`, `h_n` is true exactly when `n` belongs to the numerical semigroup for
`0 <= n <= F`. In the selector formula, `q_s` is true exactly for the selected normalized shift.
All `E`, `D` and `P` variables are definitional auxiliaries.

EXP-005's encoding proof establishes that a selector model projects to a rigid pair `(Gamma,s)`
and that a fixed-shift model projects to a semigroup `Gamma` rigid at `s`. EXP-007 does not alter
those base constraints; it adds only projected blocking clauses.

## Lemma 1 - full-assignment blocker

Let `x_1,...,x_k` be distinct Boolean variables with complete assignment `a`. Define

```text
B(a) = OR_i (not x_i if a_i=true, else x_i).
```

Every literal in `B(a)` is false under `a`, so `B(a)` rejects `a`. If another complete assignment
`b` differs from `a` at coordinate `j`, the `j`-th literal is true under `b`, so `B(a)` accepts
`b`. Therefore `B(a)` excludes exactly one assignment of the projected variables. Variables not
listed in the clause cannot affect that conclusion.

This is why a membership blocker contains one signed literal for every `h_0,...,h_F`. Omitting
either member or gap coordinates could reject multiple semigroups and invalidate completeness.

## Lemma 2 - complete shift support

The selector formula has exactly one true `q_s`. After a validated model at shift `s`, adding the
unit clause `not q_s` removes every model at that shift and no model at another shift. Repeating
this operation discovers one witness for every feasible shift. Once the resulting formula is
UNSAT, no unblocked feasible shift exists. A checked proof of that terminal UNSAT formula makes
the discovered shift set exhaustive.

## Lemma 3 - complete fixed-shift class

Fix a feasible shift `s`. Each SAT model supplies a complete assignment of `h_0,...,h_F`. By
Lemma 1, its blocker removes that semigroup and no other projected semigroup. Auxiliary
assignments for the same semigroup are removed with it because the blocker is already false at
the `h` projection. Once the base formula plus every accumulated blocker is UNSAT, the retained
membership vectors are exactly all semigroups rigid at `s`.

## Theorem - EXP-007 completeness

Assume:

1. every retained SAT projection passes the independent exact semantic checker;
2. the terminal shift-support DRAT proof is accepted against its recorded CNF;
3. for every supported shift, the terminal fixed-shift DRAT proof is accepted against its
   recorded CNF; and
4. the auditor reconstructs every blocker and reproduces the recorded CNF hashes.

Then the union of the retained `(membership vector, shift)` records is exactly the set of
normalized rigid pairs at `F`. Counts, shift support and uniqueness follow directly. If any
assumption is absent, only the individually validated positive models may be claimed.

## Trusted base

The classification trusts the mathematical encoding, Python's deterministic CNF serialization,
the exact semantic checker, DRAT-trim and ordinary file hashing. CaDiCaL is a model finder and
proof producer, not a trusted UNSAT oracle. Reducing the proof checker or importing certificates
into a formally verified kernel is a separate backlog item.
