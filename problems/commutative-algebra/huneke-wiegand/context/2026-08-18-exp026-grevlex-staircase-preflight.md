# EXP-026 grevlex staircase preflight

Date: 2026-08-18. Status: source-complete declaration preflight.

## Question and redirection

EXP-025 identifies the conductor fiber cone as

```text
C_p = k[x y^a : a in G_p] inside k[x,y]/(y^(24p)).
```

Thus a degree-`n` monomial is determined by its total offset when that offset is below `24p`,
and is zero otherwise. This makes the previously deferred Groebner problem finite and
combinatorial: in each surviving bidegree there is a unique grevlex-smallest factorization, and
the complement of those factorizations is the initial ideal.

The selected question is:

> For grevlex with `X_a > X_b` when `a>b` (so `X_0` is last), does the reduced Groebner basis of
> `J_p` stop in degree four, with a uniform closed description of every higher-degree element?

This now ranks above the unresolved interior Betti table. It has a canonical order, exact finite
invariants, and a proof route through standard monomials and Hilbert functions. A successful
answer would also give a flat monomial degeneration and an independent Groebner proof of
Cohen--Macaulayness.

## Primary-source boundary

The following PDFs are archived outside Git under
`E:/_Datos/caos-research/huneke-wiegand/sources/exp026/`.

| source | role | bytes | SHA-256 |
|---|---|---:|---|
| Bhardwaj--Chau--Javadekar, *Projective monomial curves associated to numerical semigroups with multiplicity e, width e-1, and embedding dimension e-2*, arXiv:2511.06482v1 | recent explicit projective-monomial-curve Groebner bases; uses a last parameter variable, standard-monomial enumeration, and Hilbert-length comparison | 362,932 | `9cc838249082593685b00766a9b0a79a5a208621f932343b5d614d1e99894ebb` |
| Saha--Sengupta--Srivastava, *On the Associated Graded ring of Semigroup Algebras*, arXiv:2210.07520v1 | reverse-lex orders in which extremal-ray variables avoid all leading monomials, and the link with Cohen--Macaulayness | 208,973 | `b80ba9d70317e85d284aa2873be52d2694fa295b3982cd9708fb99c74da8843a` |

Stable source URLs:

- `https://arxiv.org/abs/2511.06482`
- `https://arxiv.org/abs/2210.07520`

These papers supply method and context, not a novelty proof for the CAOS conductor family. The
search found no exact match for its offset set, reduced basis, or the formulas declared below.

## Frozen premise ledger

| premise | SHA-256 | use |
|---|---|---|
| EXP-023 `proof.md` | `4f24c8bacf3ea4a7691142b6fbb2a79b40a1c200ec5051df3c79c3dc45bed084` | exact defining ideal, one primitive cubic minimal equation, and relation type three |
| EXP-024 `proof.md` | `b7b654609cfca99e979b26741f7d2b6bbbfc0029d882c38e3c2932bfc9146088` | projective dimension, regularity, and extremal Betti boundary |
| EXP-025 `proof.md` | `70c7838ce843252aba335d80ade105d1d1942c490530ea7770483be0dff9a61f` | truncated-monomial parametrization and freeness over `k[X_0]` |
| EXP-025 `run.py` | `42411e5f8a166bd4a4663b49dfa3c19808b283735d2d633517c632e876f0377d` | exact degree-one offset set and cumulative bases |

Any mismatch stops the experiment as `INCONCLUSIVE_PREMISE`; upstream changes are never silently
accepted.

## Pre-declaration invariant probe

A read-only dynamic-programming probe produced no committed experiment artifact. For each
`p=4,...,15`, it selected the grevlex-smallest monomial in each pair `(degree,total offset)`, then
identified minimal boundary monomials by requiring every one-variable divisor to remain standard.
It found:

| degree | minimal initial generators |
|---:|---:|
| 2 | `50p^2-17p` |
| 3 | `5p-1` |
| 4 | `p-2` |
| 5 | `0` |

No leading monomial involved `X_0`. For `p=4,...,6`, the degree-three and degree-four binomials
were inspected explicitly; the resulting formulas were then matched exactly for every
`p=7,...,15`. This supports declaration only. It does not confirm the theorem.

## Candidate reduced basis

Order the variables by decreasing offset and use graded reverse lexicographic order. For every
surviving pair `(n,s)`, let `N_(n,s)` be the grevlex-smallest degree-`n` monomial of total offset
`s`.

The quadratic part is predicted to contain, for every nonstandard quadratic monomial `M`:

```text
M-N_(2,s)  if its total offset s is below 24p,
M          if s is at least 24p.
```

The predicted higher-degree reduced-basis elements are the following six cubic families and one
quartic family. All displayed left monomials are leading terms.

```text
X_i X_p X_(12p-1) - T1_i                         (1 <= i <= p)
X_i X_p X_(15p-1) - T2_i                         (1 <= i <= p)
X_i X_p X_(18p-1) - T3_i                         (1 <= i <= p)
X_i X_(4p-2) X_(16p) - X_0 X_(3p) X_(17p+i-2)  (1 <= i <= p-2)
X_i X_(4p-2) X_(18p-1) - T5_i                    (1 <= i <= p)
X_p^3 - X_0^2 X_(3p)
X_i X_p^2 X_(4p-2) - X_0^3 X_(6p+i-2)           (2 <= i <= p-1)
```

where

```text
T1_1 = X_0 X_(3p) X_(10p),
T1_i = X_0^2 X_(13p+i-1)              for 2 <= i <= p-1,
T1_p = X_0 X_1 X_(14p-2);

T2_i = X_0 X_(i-1) X_(16p)            for 1 <= i <= p-1,
T2_p = X_0^2 X_(17p-1);

T3_i = X_0 X_(3p+i-1) X_(16p)         for 1 <= i <= p-1,
T3_p = X_0 X_(3p) X_(17p-1);

T5_i = X_0 X_(7p+i-2) X_(15p-1)       for i=1,2,
T5_i = X_0 X_(6p+i-3) X_(16p)         for 3 <= i <= p.
```

The cubic count is `p+p+p+(p-2)+p+1=5p-1`; the quartic count is `p-2`.

## Deductive route and falsification

1. Prove that each surviving bidegree has exactly one standard monomial and that multiplication
   by `X_0` preserves canonical representatives.
2. Characterize the minimal boundary of the standard staircase. The quadratic boundary is
   accepted in canonical set-comprehension form; the nonquadratic boundary must equal the seven
   displayed families.
3. Verify that every proposed tail is the canonical standard representative of the same offset.
4. Count standard monomials in every degree and recover the known Hilbert function
   `(1,10p,22p,24p-1,24p,...)`. Equality of Hilbert functions then certifies the entire initial
   ideal and avoids an exhaustive Buchberger campaign.
5. Fail immediately on an extra degree-five boundary element, a family mismatch, an `X_0`-divisible
   leading generator, or a Hilbert-function discrepancy.

## Manuscript gate

If confirmed, EXP-026 is a standalone Groebner theorem but studies exactly the algebra introduced
in the focused `curvilinear-fiber-cones` companion. The coherent action is therefore a substantive
v0.02 expansion of that companion and a new Zenodo version, not a third manuscript. A split is
reserved for a later complete interior Betti table or a method that applies beyond this family.

