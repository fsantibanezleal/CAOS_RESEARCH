# EXP-068 proof: tensor factorization of extension ideals under gluing

Written 2026-10-30 from the frozen hypothesis, before the computational run is read.

## Setting

`Gamma1`, `Gamma2` are numerical semigroups and `Gamma = a1*Gamma1 + a2*Gamma2` is a gluing: `a1` lies
in `Gamma2`, `a2` lies in `Gamma1` and `gcd(a1,a2) = 1` (García-Sánchez and Leamer, Section 2). `k` is a
field, `R_i = k[Gamma_i]`, `R = k[Gamma]`, all graded by the exponent. `S = k[y]` acts on `R1` through
`y -> t^a2` and on `R2` through `y -> t^a1`. A relative ideal `B` of a numerical semigroup `Lambda` gives
the fractional ideal `I_B` spanned by `t^b`, `b` in `B`; its dual is `B* = Lambda - B` and
`I_(B*) = Hom(I_B, k[Lambda])` (Leamer, Remark 1.7). For `B` non-principal, `B` is Huneke-Wiegand iff
`I_B (x) I_(B*)` has non-zero torsion (Leamer, Theorem 1.4; García-Sánchez and Leamer, Theorem 6).
`mu(B)` is the number of minimal generators of `B`. For relative ideals `A_i` of `Gamma_i` put
`A = a1*A1 + a2*A2`, `T_i = I_(A_i) (x)_(R_i) I_(A_i*)` and `T = I_A (x)_R I_(A*)`. For a module `M`,
`tau(M)` is its torsion submodule and `l` is length; for graded modules of finite length over these
rings, `l = dim_k`.

## Lemma A (Apéry bases)

Let `B` be a relative ideal of `Lambda` and `c > 0` in `Lambda`. Then `I_B` is a free
`k[t^c]`-module with basis `t^b`, `b` in `Ap(B,c) = {b in B : b - c not in B}`, and `Ap(B,c)` has
exactly one element in each residue class modulo `c`.

*Proof.* In each residue class `r` modulo `c` the set `B` is non-empty (it contains every large
integer), bounded below, and closed under adding `c` (because `c` is in `Lambda` and
`B + Lambda` is contained in `B`). With `b_r` its minimum, the class is `b_r + c*N`, so
`I_B = sum_r t^(b_r) k[t^c]` and the sum is direct because the classes are disjoint. QED

## Proposition 1 (extensions are tensor products)

The map `I_(A1) (x)_S I_(A2) -> I_A`, `t^x (x) t^z -> t^(a1*x + a2*z)`, is a well-defined isomorphism of
`R1 (x)_S R2`-modules. For `A_i = Gamma_i` it is a ring isomorphism `R1 (x)_S R2 -> R`.

*Proof.* The map is `S`-balanced: `(t^a2 t^x) (x) t^z` and `t^x (x) (t^a1 t^z)` both go to
`t^(a1*x + a1*a2 + a2*z)`, and it is compatible with the `R1`- and `R2`-actions. By Lemma A
(`a2` in `Gamma1`, `a1` in `Gamma2`), the source is a free `S`-module with basis
`t^x (x) t^z`, `x` in `Ap(A1,a2)`, `z` in `Ap(A2,a1)`, so it has the `k`-basis
`y^n (t^x (x) t^z)`, which maps to `t^(a1*x + a2*z + n*a1*a2)`. Surjectivity: an element of `A` is
`a1*x' + a2*z'` with `x' = x + i*a2`, `z' = z + j*a1` for Apéry elements `x, z` and `i, j >= 0`, hence
equals `a1*x + a2*z + (i+j)*a1*a2`. Injectivity: if `a1*x + a2*z + n*a1*a2 = a1*x' + a2*z' + n'*a1*a2`,
reducing modulo `a1` and using `gcd(a1,a2)=1` gives `z = z' (mod a1)`, so `z = z'` by Lemma A;
likewise `x = x'`, and then `n = n'`. Distinct basis vectors therefore go to distinct monomials. QED

By Lemma 8(9) of García-Sánchez and Leamer, `A* = a1*A1* + a2*A2*`, so Proposition 1 also gives
`I_(A*) = I_(A1*) (x)_S I_(A2*)`.

## Proposition 2 (tensor factorization)

`T = T1 (x)_S T2` as `R = R1 (x)_S R2`-modules.

*Proof.* For commutative `S`-algebras `R_i` and `R_i`-modules `M_i`, `N_i` there is a natural
isomorphism `(M1 (x)_S M2) (x)_(R1 (x)_S R2) (N1 (x)_S N2) = (M1 (x)_(R1) N1) (x)_S (M2 (x)_(R2) N2)`,
`(m1 (x) m2) (x) (n1 (x) n2) <-> (m1 (x) n1) (x) (m2 (x) n2)`: both sides are the quotient of
`M1 (x)_S M2 (x)_S N1 (x)_S N2` by the relations `r1 m1 (x) n1 = m1 (x) r1 n1` and
`r2 m2 (x) n2 = m2 (x) r2 n2`, and the displayed maps are mutually inverse and well defined on
those relations. Apply it with `M_i = I_(A_i)`, `N_i = I_(A_i*)` and Proposition 1. QED

## Lemma B (torsion over `S` and over `R`)

`S` embeds in `R` through `y -> t^(a1*a2)` (the image of `y (x) 1 = 1 (x) y`), and `R` is a finite
`S`-module; likewise `R1` is free of rank `a2` and `R2` free of rank `a1` over `S` (Lemma A). For a
finitely generated module `M` over one of these domains, its torsion submodule equals its
`S`-torsion submodule.

*Proof.* If `s*m = 0` with `0 != s` in `S`, then `s` is non-zero in the domain, so `m` is torsion.
Conversely, if `r*m = 0` with `r != 0`, `r` is integral over `S`; take a monic relation
`r^d + s_(d-1) r^(d-1) + ... + s_0 = 0` of least degree. Then `s_0 != 0` (otherwise divide by `r` in the
domain), and `s_0 m = -(r^(d-1) + ... + s_1) r m = 0`. QED

## Theorem (torsion-length law and characterization)

1. `l(tau(T)) = a1*l(tau(T1)) + a2*l(tau(T2)) + l(tau(T1) (x)_S tau(T2))`, and
   `l(tau(T1) (x)_S tau(T2)) = sum_(j>=1) b1(j)*b2(j)`, where `b_i(j)` is the number of Jordan blocks of
   size at least `j` of `y` acting on `tau(T_i)`.
2. `mu(A) = mu(A1)*mu(A2)`; in particular `A` is principal iff both `A_i` are.
3. `A` is Huneke-Wiegand iff `A1` or `A2` is a non-principal Huneke-Wiegand ideal. Equivalently, `A` is
   a counterexample (non-principal with `T` torsion-free) iff `A` is non-principal and each `A_i` is
   either principal or a counterexample.

*Proof of 1.* `T_i` is finitely generated over `R_i`, hence over `S`, and has `R_i`-rank one (it is the
tensor product of two rank-one modules). Over the graded principal ideal domain `S`,
`T_i = F_i (+) tau_S(T_i)` with `F_i` free, and `tau_S(T_i) = tau(T_i)` by Lemma B. Ranks multiply,
so `F1 = S^a2` and `F2 = S^a1`. By Proposition 2,

`T = (S^a2 (+) tau1) (x)_S (S^a1 (+) tau2) = S^(a1*a2) (+) tau1^a1 (+) tau2^a2 (+) (tau1 (x)_S tau2)`,

with `tau_i = tau(T_i)`. The last three summands are `S`-torsion (each `tau_i` is a finite-dimensional
`k`-space, killed by a non-zero polynomial in `y`) and the first is free, so `tau_S(T)` is their sum,
which equals `tau(T)` by Lemma B. Each `tau_i` has finite length and `y` raises degree, so `y` acts
nilpotently: `tau1 = (+)_i S/(y^(e_i))`, `tau2 = (+)_j S/(y^(f_j))` up to degree shifts, and
`S/(y^e) (x)_S S/(y^f) = S/(y^min(e,f))`. Hence `l(tau1 (x) tau2) = sum_(i,j) min(e_i,f_j)`, which is
`sum_(j>=1) b1(j) b2(j)`. QED

*Proof of 2.* With `m` the graded maximal ideal, `R/m = k = (R1/m1) (x)_S (R2/m2)` with `y` acting by
zero on both factors. By Proposition 2 applied to `M_i = I_(A_i)`, `N_i = k`,
`I_A (x)_R k = (I_(A1) (x)_(R1) k) (x)_S (I_(A2) (x)_(R2) k) = k^(mu(A1)) (x)_k k^(mu(A2))`. QED

*Proof of 3.* If `A_i` is principal, `I_(A_i)` is free of rank one and `T_i = R_i` is torsion-free. If
`A_i` is non-principal, `tau(T_i) != 0` exactly when `A_i` is Huneke-Wiegand. Since `a1, a2 >= 1`,
item 1 gives `tau(T) != 0` iff `tau(T1) != 0` or `tau(T2) != 0`, and item 2 gives that `A` is
non-principal iff some `A_i` is. QED

## Corollaries

- Proposition 9 of García-Sánchez and Leamer is the case "`A1` non-principal Huneke-Wiegand" of item 3;
  their Proposition 10 is the case `A2 = Gamma2`. The case they leave open, both factors non-principal
  and not Huneke-Wiegand, gives a counterexample.
- EXP-067 is the case `Gamma2 = N`, `A2 = N`, `a1 = q`, `a2 = m`.
- Counterexamples with `2^r` minimal generators. If `A1`, `A2` are two-generated counterexample ideals
  over symmetric semigroups, then `a1*A1 + a2*A2` is a four-generated counterexample over the
  symmetric semigroup `a1*Gamma1 + a2*Gamma2` (gluings of symmetric semigroups are symmetric, Delorme;
  Rosales and García-Sánchez, Numerical Semigroups, Chapter 8). Iterating gives `2^r` generators.
- Every non-principal extension ideal of a gluing of two semigroups all of whose non-principal ideals
  are Huneke-Wiegand is Huneke-Wiegand. This answers the third Future Work question of García-Sánchez
  and Leamer for extension ideals; ideals of `Gamma` that are not extensions are not covered.
- For monomial ideals, item 3 answers their ring-level question: the module
  `(I_(A1) (x)_k I_(A2)) / (t^a2 (x) 1 - 1 (x) t^a1)` is `I_(A1) (x)_S I_(A2)`, and it satisfies the
  conclusion of the conjecture for every `A2` once `I_(A1)` does (non-principal Huneke-Wiegand), and
  fails it exactly in the described case. A version for arbitrary modules would need `Hom` to factor
  over `S`; it is not claimed.

## Scope

The statements hold over every field `k` and for the graded rings; the local (completed) rings have
the same torsion, since torsion here is a finite-length graded module.
