# EXP-006 Route K specification

Frozen: 2026-08-10, before the first Route K SAT query.

## Decision question

For each even `s=16,18,...,40`, does there exist a symmetric numerical semigroup `Gamma` and a
rigid nonprincipal two-generated monomial ideal represented by the normalized shift `s`, subject
to

```text
F(Gamma) = 13s-1,
m(Gamma) = 4s,
[5s,6s-1] is contained in Gamma?
```

This is the least restrictive exact interpretation of the block hypothesis declared in
`hypothesis.md`. Membership in the level-4 block `[4s,5s-1]` and level-6 block `[6s,7s-1]` is
Boolean. Membership outside those blocks is not fixed: it is determined only by the semigroup,
symmetry and rigidity constraints. In particular, the encoding does not assume that every
minimal generator lies below `7s`.

## Exact encoding

For `F=13s-1`, the base CNF from `hwcert.build_rigidity_cnf(F,s)` imposes:

1. zero membership, exclusion of `F` and exclusion of the selected shift `s`;
2. symmetry `h(n) = not h(F-n)` for `0<=n<=F`;
3. additive closure through `F`;
4. the finite inverse-ideal equality `D=E+E` through `2F+1`, with the existing proved conductor
   tail.

Route K adds unit clauses

```text
not h(n), 1 <= n < 4s,
h(4s),
h(n), 5s <= n < 6s.
```

The first line and `h(4s)` impose multiplicity exactly `4s`. The final line retains the full
middle generator block seen in the seed while allowing both adjacent blocks to move.

## Invariant-first deduction

The level-6 density is not an optimization variable. Reflection around `F=13s-1` maps

```text
6s+r  <->  7s-1-r,  0 <= r < s.
```

Both entries lie in the same length-`s` block and symmetry makes exactly one entry in each pair a
member. Since `s` is even, every feasible model therefore has exactly `s/2` level-6 members. The
seed's count `7` at `s=14` is forced by symmetry, not an independently scalable pattern.

For level 4, the seed density is `5/14`. After the existence query, Route K selects a diagnostic
model whose level-4 count minimizes

```text
abs(14 * count(level 4) - 5s).
```

Counts are queried in deterministic increasing score order, with the smaller count first on a
tie. This optimization chooses a representative; it does not alter the existence decision.

## One-sidedness and certificates

- A semantically checked SAT model proves existence for that finite parameter inside the declared
  Route K class. It does not prove a recurrence or an infinite family.
- An accepted DRAT proof for the unconstrained-count CNF proves nonexistence for that finite
  parameter inside the declared Route K class.
- A timeout or resource cap proves nothing and records the parameter as `UNKNOWN`.
- Three non-seed models are necessary but not sufficient for Route A. A symbolic interval or
  residue proof remains mandatory for an infinite-family claim.

Every SAT model is decoded by the standard-library checker for symmetry, closure, exact
multiplicity, the full middle block and full-window/tail rigidity. The adversarial corruption
clears `h(4s)` and must be rejected as a multiplicity failure. Every UNSAT proof is checked by the
pinned independent `drat-trim` executable.

## Budget and deterministic order

- Calibration: `s=14`, where the public seed must satisfy the Route K constraints.
- Campaign: even `s=16,...,40` in increasing order.
- Per unconstrained existence query: 1,200 seconds.
- Total campaign solver budget: 14,400 seconds.
- Optimization queries run only after SAT and share the same total campaign cap.
- A checkpoint and flushed progress line are required after every solver call.

The heavy CNF, solver logs and proofs live outside Git under
`E:/_Datos/caos-research/huneke-wiegand/EXP-006-block-family/route-k/`. Git stores the deterministic
code, compact results, hashes and manifest.

## Source and viewpoint preflight

A fresh 2026-08-10 primary-source sweep found no source that settles this rigidity-constrained
block question. Kunz-cone work confirms that fixed-multiplicity numerical semigroups are integer
points in a rational polyhedral cone and that faces encode shared semigroup structure:

- Kaplan and O'Neill, *Numerical semigroups, polyhedra, and posets I*,
  `https://arxiv.org/abs/1912.03741`.
- Borevitz et al., *On faces of the Kunz cone and the numerical semigroups within them*,
  `https://arxiv.org/abs/2309.07793`.
- Brower, McDonough and O'Neill, *Numerical semigroups, polyhedra, and posets IV*,
  `https://arxiv.org/abs/2401.06025`.

These sources motivate a later face-recognition route if several models occupy a recurrent Kunz
face. They do not validate any rigidity claim and are not used as premises of the SAT decision.

## Stop and redirection rules

- Zero non-seed models closes Route K negatively on the declared range and redirects from direct
  family construction to an obstruction analysis of the failed block premise.
- One or two non-seed models produce isolated examples only and do not open Route A.
- At least three non-seed models open Route A, where residue patterns and Kunz-face data are
  inferred and then proved symbolically.
- No constraint may be tuned after campaign results under EXP-006. A changed block premise is a
  new experiment.
