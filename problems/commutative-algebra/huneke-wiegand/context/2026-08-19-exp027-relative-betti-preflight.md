# EXP-027 relative Betti-strand preflight

Date: 2026-08-19. Status: source-complete declaration preflight.

## Reconciled question

For every `p>=4`, EXP-021--EXP-026 identify the conductor special fiber as

```text
C_p=P_p/J_p,
P_p=k[X_a : a in G_p],
X_a maps to x y^a in k[x,y]/(y^(24p)),
|G_p|=10p.
```

The Hilbert numerator and the first and last edges of the minimal `P_p`-resolution are known, but
the interior remains undetermined. The next unresolved entries are `beta_(2,4)` and
`beta_(3,4)`. They cannot be separated by the Hilbert numerator alone.

The selected redirection is to retain the offset grading. Put

```text
H_p = <(1,a) : a in G_p> subset N^2,
S_p = k[H_p],
M_p = (t^(n,s) : s>=24p) subset S_p.
```

Then `C_p=S_p/M_p`. For a bidegree `u=(j,b)`, define the squarefree divisor pair

```text
Delta_u = {F subset G_p : u-(|F|,sum(F)) is in H_p},
Gamma_u = {F in Delta_u : the residual offset is at least 24p}.
```

The offset-`u` part of the Koszul complex of `C_p` has exactly the relative simplicial chain
basis of `(Delta_u,Gamma_u)`. Hence

```text
beta_(i,u)(C_p) = dim_k H~_(i-1)(Delta_u,Gamma_u;k).
```

This converts every interior entry into finite relative homology while preserving the offset
support that the standard grading discards.

## Fresh primary-source and novelty boundary

The following sources are archived outside Git under
`E:/_Datos/caos-research/huneke-wiegand/sources/exp027/`.

| source | role | bytes | SHA-256 |
|---|---|---:|---|
| Stamate, *Betti Numbers for Numerical Semigroup Rings*, arXiv:1801.00153v2 | squarefree-divisor complex formula, computational methods, and characteristic-dependence warning | 256,445 | `6d7809efa8dcf172e2d1b79e30b9ecb7bf89af206997fff93670df8dc3c5a86e` |
| Autry et al., *Numerical Semigroups, Polyhedra, and Posets II: Locating Certain Families of Semigroups*, arXiv:1804.06632v1 | explicit construction and classification of squarefree divisor complexes | 331,173 | `6e61ffb4ea916b1c7b6b4bb04988f631c20ef0eab6ccda3cae67fb77d2b9b049` |
| Rossi--Sharifan, *Minimal Free Resolution of a Finitely Generated Module over a Regular Local Ring*, arXiv:0904.1086v1 | consecutive cancellations as a competing transfer route and its information loss | 201,261 | `3348aae3e30567d77568a98f04dac7a357705d31a1f805353bff1e2c030f0f28` |
| Gonzalez-Sanchez--Srinivasan, *KW Semigroups -- Their Betti Numbers, Apéry Posets and Tangent Cones*, arXiv:2605.27035v1 | recent example of a family-wide Betti formula proved through combinatorial invariance | 474,573 | `a872569aebe1aa8ba27b6c8b43b86dbd39af1272a4ba2046e3b25fd317989d6f` |

Stable source URLs:

- `https://doi.org/10.1016/S0022-4049(97)00051-0` (Bruns--Herzog, the general monomial-ideal
  relative squarefree-divisor theorem);
- `https://arxiv.org/abs/1801.00153`;
- `https://arxiv.org/abs/1804.06632`;
- `https://arxiv.org/abs/0904.1086`;
- `https://arxiv.org/abs/2605.27035`.

The publisher abstract for Bruns--Herzog was accessible but its full publisher PDF was not. The
experiment therefore does not rely on an inaccessible proof: it derives the chain identification
directly from the offset pieces of the Koszul complex. The archived sources supply method and
context, not the family-specific formulas below.

Fresh exact-family searches found no source computing the interior Betti table of these conductor
special fibers. The 2026 KW theorem concerns different numerical semigroup rings and ordinary
Betti totals. Its relevant lesson is methodological: a family-wide combinatorial classification can
replace isolated computer resolutions. It is not evidence for the claimed formulas here.

## Ranked paths

1. **Relative offset-Koszul complexes (selected).** Exact, finite in every bidegree, compatible
   with the truncated-monomial model, and able to locate rather than merely count syzygies.
2. **The mapping cone for `J_p=(Q_p,f_p)`.** EXP-023 gives the quadratic ideal `Q_p` and the unique
   cubic `f_p=X_0^2X_(3p)-X_p^3`. The linear colon `(Q_p:f_p)_1` explains the proposed
   `beta_(2,4)` support and supplies an independent audit.
3. **Apéry/Kunz-face invariance.** The new KW result makes this attractive for a later full-table
   theorem, but the present truncated affine semigroup quotient is not a KW semigroup ring and no
   suitable invariance theorem is known.
4. **Groebner degeneration plus consecutive cancellations.** EXP-026 supplies the degeneration,
   but cancellation theory gives bounds, not the actual interior cancellations.
5. **Raw full resolutions.** Rejected as the primary route: `P_p` has `10p` variables and the
   matrices grow too quickly to support an all-parameter claim.

## Frozen premise ledger

| premise | SHA-256 | use |
|---|---|---|
| EXP-021 `proof.md` | `463e609b256fc2e39a7f0056a5aa92d17e20d16c1f6861692a1ce7a18f88fe38` | exact conductor fiber cone and Artinian basis |
| EXP-023 `proof.md` | `4f24c8bacf3ea4a7691142b6fbb2a79b40a1c200ec5051df3c79c3dc45bed084` | `J_p=(Q_p,f_p)` and the unique cubic equation |
| EXP-024 `proof.md` | `b7b654609cfca99e979b26741f7d2b6bbbfc0029d882c38e3c2932bfc9146088` | Hilbert numerator and known Betti edges |
| EXP-025 `proof.md` | `70c7838ce843252aba335d80ade105d1d1942c490530ea7770483be0dff9a61f` | truncated-monomial presentation and cumulative offset sets |
| EXP-025 `run.py` | `42411e5f8a166bd4a4663b49dfa3c19808b283735d2d633517c632e876f0377d` | independent construction of `G_p` and `E_n` |
| EXP-026 `proof.md` | `765fa23534be9e534fd507dff0e447e967345e4d2a485f7da6fdf0383b04fb56` | explicit standard staircase and Groebner degeneration |

Any mismatch stops the canonical run as `INCONCLUSIVE_PREMISE`.

## Pre-declaration invariant probe

A read-only, uncommitted probe decomposed the Koszul complex by offset and performed sparse row
reduction over `GF(2)`. It reproduced the known `beta_(2,3)` for `p=4,...,7`. For `p=4,...,10`
it found values of `beta_(3,4)` interpolating exactly to

```text
p(5p-1)(500p^2-440p+47)/2.
```

The coefficient of `z^4` in the frozen Hilbert numerator then forces

```text
beta_(2,4)=8p.
```

The probe located exactly `8p` one-dimensional offset components. Their support is

```text
[9p,11p-2]
union [11p,13p-2]
union {13p}
union [14p-1,15p-1]
union [16p+1,17p-2]
union [17p,18p-1]
union {19p}
union [20p-1,21p-1].
```

Equivalently, it is `{3p+a : a in G_p and a>=6p}`. A separate quadratic-fiber graph probe found
that `X_a f_p` lies in `Q_p` exactly for the same `8p` high offsets. These observations justify
the declaration; they do not prove it. In particular, agreement over `GF(2)` alone cannot exclude
characteristic dependence.

## Declared target and proof route

EXP-027 will test and seek an all-parameter proof of:

```text
beta_(2,4)(C_p)=8p,
beta_(3,4)(C_p)=p(5p-1)(500p^2-440p+47)/2,
```

with `beta_(2,(4,b))=1` precisely on the displayed support and zero elsewhere, over every field.

The proof must:

1. derive the relative-chain formula directly from the offset-graded Koszul differential;
2. classify the degree-four relative complexes by interval arithmetic;
3. give unit-coefficient collapses, or an equivalent integral certificate, proving that the
   surviving first homology is free of rank one on exactly the claimed support;
4. audit that support through `(Q_p:f_p)_1` without importing the relative-complex ranks; and
5. derive `beta_(3,4)` from the coefficient identity only after `beta_(2,4)` is established.

The Hilbert numerator gives only the difference `beta_(2,4)-beta_(3,4)` and is not an independent
proof of both entries.

## Manuscript gate

If confirmed, this is the first genuine interior Betti-strand theorem and a reusable method, but
not a complete resolution. It should expand the main conductor-fiber manuscript to v0.14. A new
standalone manuscript is justified only if the method subsequently determines a substantial
portion of the remaining table or proves a transferable theorem beyond this family.
