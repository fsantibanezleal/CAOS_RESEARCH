# EXP-035 preflight - zero-row incidence families and survival

Date: 2026-08-30

## Scope and premise reconciliation

EXP-034 reduces the regularity-two kernel to the two-layer module

```text
M_p=K_p/X_0K_p,
(M_p)_1={u_h:h in H_p},
(M_p)_2={v_b:b in B_p}.
```

Its remaining nonlinear Betti strand is the cokernel of the signed incidence maps

```text
delta_(i+1): exterior^(i+1)(V_p) tensor (M_p)_1
             -> exterior^i(V_p) tensor (M_p)_2.
```

The following premise hashes were recomputed from the current repository state:

```text
EXP-032 proof    4dc37605c012b7f6a70ec5d383897c45a34e1dd5d5e4bb32a0582b7a6d651d1c
EXP-033 proof    e27cd386ad47da7ad5282e88a095d82f2b1156f76546e934b287e911da2c7b1c
EXP-034 proof    0d0a87b0a5fd4e3bbb5570e3e664eb59fcf8d07222abd62c48bdae9d20d61b4a
EXP-034 verdict  ebbf52a0b2d85b0bb5c71ca6fb48846d17b1d91644e48e69dbc3a5e8a5f81304
```

The programme state, backlog, RESUME, history, and EXP-034 verdict agree: one multigraded
regularity-two class is known, while both complete lower strands remain open. The active work is
in CAOS_RESEARCH on `work/huneke-wiegand/open`. CAOS_MANAGE is outside this experiment and remains
untouched on `develop`.

## Fresh primary-source sweep

The source pass rechecked the Tor-map formulation of Betti splitting and recent partial and
multigraded extensions:

1. Francisco, Ha, and Van Tuyl, *Splittings of monomial ideals*, arXiv:0807.2185.
2. Bolognini, *Betti splitting via componentwise linear ideals*, arXiv:1410.6511.
3. Jayanthan, Sivakumar, and Van Tuyl, *Partial Betti splittings with applications to binomial
   edge ideals*, arXiv:2412.04195.
4. Murai and Shiina, *Betti splittings and multigraded Betti numbers of cover ideals of bipartite
   graphs*, arXiv:2312.08575.

These sources confirm that vanishing of the relevant Tor maps is the decisive splitting datum.
They do not classify the family-specific incidence rows or prove vanishing of the connecting map
for `0 -> K_p -> A_p -> D_p -> 0`. The exact offset model remains strictly stronger for this
question. No cited source settles the proposed cell family.

## Invariant-first redirection

For `b in B_p`, define the representation set

```text
R_b={g in G_p minus {0}:b-g in H_p}.
```

The row of `delta_(i+1)` labelled by `e_F tensor v_b` can receive a nonzero coefficient only by
adjoining an element of `R_b minus F`. Therefore its zero-row status is decided by the single
set-containment invariant `R_b subset F`. This is cheaper and stronger than constructing a full
incidence matrix.

The next block after the EXP-034 cell is

```text
b_(p,t)=10p+t,             2<=t<=p-2,
R_(p,t)=[3p,4p-2] union {t} union [t+2,p].
```

Its predicted size is `r_(p,t)=2p-t-1`, which lies strictly below the first row-two homological
degree `2p-2` of `D_p`. If its connecting coordinate is also killed by exact low-complex pivots,
these cells fill every homological position `p+1,...,2p-3` next to the EXP-034 class at `p`.

## Redirection and guardrails

- Classify zero rows by `R_b subset F` before any full-rank computation.
- Treat a primitive class in `K_p` separately from survival in `A_p`.
- Use exact integer and finite-field boundary ranks only as implementation checks; the
  all-parameter theorem requires interval and unit-pivot arguments.
- Preserve collisions in total offset. A zero coordinate gives a direct cokernel summand even
  when its multidegree contains other rows.
- Stop the proposed consecutive-survival claim immediately if one exact connecting source admits
  a cycle with a nonzero selected coefficient.
- Do not launch a raw full resolution or a GPU calculation.

## Exploration moment

The new viewpoint is a forbidden-neighbor or zero-row decomposition: the incidence cokernel
contains a canonical free coordinate summand indexed by pairs `(b,F)` satisfying `R_b subset F`.
This converts a matrix-rank search into a representation-set classification and produces an
explicit ordinary lower-bound polynomial. The two-sided question is whether the connecting map
systematically cancels any of this summand. EXP-035 tests the first nontrivial consecutive block.

