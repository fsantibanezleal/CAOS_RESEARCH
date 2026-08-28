# EXP-034 verdict - CONFIRMED

Date: 2026-08-27. Backlog: HWB-035 and HWB-055.

## Decision

**CONFIRMED.** For every integer `p>=4` and every field, put

```text
tau_p=8p-1+p(p+1)/2.
```

Then the previously unresolved regularity-two strand contains the exact multigraded class

```text
beta_(p,(p+2,tau_p))(K_p)
=beta_(p,(p+2,tau_p))(A_p)
=beta_(p,(p+2,tau_p))(C_p)
=1.                                                           (1)
```

Consequently

```text
beta_(p,p+2)(A_p)>=1,
beta_(p,p+2)(C_p)>=binom(8p,p-1)+1.                           (2)
```

This is a relevant new result and refutes the naive maximal-rank model for the two-layer kernel.
It does not complete either lower strand or the full Betti table.

## Why it works

Killing the common regular element `X_0` turns the EXP-033 kernel into a two-layer module with
degree-one basis the `8p` high variables and degree-two basis the `10p` missing offsets in
`[6p,24p-1]`. Its Betti numbers are kernels and cokernels of explicit signed incidence maps.

The first degree-two offset is `8p-1`, while the `p` smallest positive variables are
`1,...,p`. Their total gives the unique codomain cell in multidegree `(p+2,tau_p)`. The only
representations of `8p-1` as a high offset plus a variable use precisely those same `p` variables,
so there is no extra exterior variable from which a boundary could enter. The kernel class is
therefore primitive and rank one.

For the connecting map from `D_p`, each possible contribution factors off one high variable and
leaves the low chain `e_{1,...,p} tensor X_l`. It is the only chain in its low multidegree, and its
boundary has the unit coordinate `X_pX_l` at offset `p+l`. Thus no `D_p` cycle can carry the
required coefficient. The `D_p` row-two strand begins at homological degree `2p-2>p`, so the long
exact Tor sequence makes the surviving `A_p` component exactly one. The shifted cubic diagonal
starts `(p-2)(6p-1)` offsets above `tau_p`, giving the exact `C_p` value.

## Gate record

| gate | result |
|---|---|
| declaration before implementation | PASS; declaration commit `c132d54` precedes implementation commit `d6924fd` |
| frozen premises | PASS; all EXP-030/032/033 hashes match |
| canonical campaign | PASS for all 297 parameters in 1.305 seconds |
| exact finite-field ranks | PASS through `p=8` over `GF(2)` and `GF(1000003)` |
| independent reconstruction | PASS from numerical-semigroup ideal powers through `p=25` |
| rational literal sources | PASS through `p=9`; each has dimension one and boundary rank one |
| symbolic certificate | PASS; eight negations UNSAT, 299 arithmetic rows pass, shifted gap factors exactly |
| adversarial controls | PASS; gap, variable, target, exterior, shift, and partition mutations are rejected |
| all-parameter proof | PASS; regular reduction, incidence cokernel, unit source pivot, and Tor exactness are deductive |

Aggregates:

```text
canonical       65ef176dcd9f5bd5467c09e763fdb20c67798de9743443ce5d0e34958c1645ce
finite ranks    31d70c09d251bb6009b610be05c33a42ccd50e417b84aff2c0db561018e6acc5
independent     31479abd3c7247fe0ba464eefe06e437a595812c3d6055d0de8d0ced25d12794
symbolic        b3f461298706a394cc0f1a296557e10f52435f78d2f1039452fb726871b79a4d
```

## Scope and next frontier

The broad Huneke--Wiegand conjecture was already disproved by Son Pham's public counterexample.
EXP-034 neither claims that discovery nor resolves the conjecture anew. It proves an exact
previously unknown Betti class for every member of the CAOS infinite family.

The two-layer incidence formula is now the strongest route to the remaining table. The next
experiment should classify the other cokernel cells `e_(R_b) tensor v_b`, determine which survive
the connecting map, and test whether their unit-pivot intervals tile a complete lower strand.

## Publication decision

The publication trigger is crossed because (1) changes the published lower-strand boundary and
adds a characteristic-free theorem for every family member. Incorporate it in the existing main
manuscript as v0.21 and create a Zenodo new version after all claim/build/render/authorship gates.
A separate manuscript remains premature until the incidence method determines a complete strand
or yields a transferable theorem beyond this family.

