# EXP-021 preflight - conductor fiber cone and canonical quotient

Date: 2026-08-12.

## Path selection

The strongest untested structural object left by EXP-018--020 is the special fiber

```text
C_p=F(T_p)=direct-sum_(n>=0) T_p^n/(m_p T_p^n).
```

This is a sharper target than another parameter sweep. The tangent cone `G_p=gr_(T_p)(R_p)` is
depth-zero Buchsbaum, while its quotient by `H^0` is Cohen--Macaulay. There is always a natural
surjection

```text
G_p -> C_p
```

because `T_p^(n+1)` is contained in `m_p T_p^n`. Exact exploratory profiles suggest the stronger
identity `T_p^2=m_pT_p`; if true, the map has no positive-degree kernel and EXP-019 identifies its
degree-zero kernel as `m_p/T_p=H^0(G_p)`. Thus the fiber cone would be the canonical graded-algebra
Cohen--Macaulayization `G_p/H^0(G_p)`, not merely an abstract module with the same Hilbert series.

## Primary-source audit

The directly applicable source is:

- T. Cortadellas Benitez and S. Zarzuela Armengou, *On the structure of the fiber cone of ideals
  with analytic spread one*, Journal of Algebra 317 (2007), 759--785,
  `https://doi.org/10.1016/j.jalgebra.2007.02.044`, preprint
  `https://arxiv.org/abs/math/0603042`.

The source proves the graded `k[x]` structure theorem for analytic-spread-one fiber cones and the
Cohen--Macaulay criterion used to interpret the exact decomposition. The PDF was downloaded
outside Git to
`E:/_Datos/caos-research/huneke-wiegand/sources/exp021/cortadellas-zarzuela-math0603042.pdf`.
It has 301,730 bytes and SHA-256
`328f9c90ba019b54e5bc10c5aa847aa7ed3f0c18252688f869c374cc416fb1ae`.

A later defining-ideal route was also checked in:

- M. Abdolmaleki and S. Kumashiro, *Defining ideals of Cohen--Macaulay fiber cones*,
  `https://arxiv.org/abs/2405.18041`.

Its downloaded PDF has 149,637 bytes and SHA-256
`cdc9b38057207c457f8c9dc87d80c321207eeeaff5829e8f046a4e4af153096d`. That route is deferred:
first prove that the present fiber cones are Cohen--Macaulay and determine their exact anatomy.

## Confirmed premises

1. EXP-013 gives the exact common trace/conductor ideal `T_p`.
2. EXP-016--017 give its power profiles, minimal reduction `Q_p=t^(4s)R_p`, reduction number four,
   and Hilbert coefficients.
3. EXP-018 gives the Hilbert series of `G_p`.
4. EXP-019 proves `H^0(G_p)=k^p` in degree zero and identifies the Cohen--Macaulay quotient.
5. EXP-020 gives the complete `k[x_p]`-module decomposition of that quotient.

No infinite-family conclusion will rest on the finite campaign. The block proof of
`T_p^2=m_pT_p`, the natural-kernel argument, and the closed socle calculation are load-bearing.

## Exact predictions

For every `p>=4`, with `s=6p`, `q=4s=24p`, and `F_p=k[x_p]`:

1. `T_p^2=m_pT_p`, hence `T_p^(n+1)=m_pT_p^n` for every `n>=1`.
2. The natural map induces a graded-algebra isomorphism
   `G_p/H^0(G_p) isomorphic to C_p`.
3. As an `F_p`-module,

```text
C_p isomorphic to F_p
  direct-sum F_p(-1)^(10p-1)
  direct-sum F_p(-2)^(12p)
  direct-sum F_p(-3)^(2p-1)
  direct-sum F_p(-4).
```

4. `C_p` is one-dimensional Cohen--Macaulay of multiplicity and rank `24p`, reduction number and
   regularity four, and `a(C_p)=3`. Its Hilbert function is

```text
1, 10p, 22p, 24p-1, 24p, 24p, ...
```

and its Hilbert series numerator is

```text
1+(10p-1)z+12p z^2+(2p-1)z^3+z^4.
```

5. The Artinian reduction `B_p=C_p/(x_p)` has h-vector
   `(1,10p-1,12p,2p-1,1)` and socle dimensions `(0,0,10p,0,1)`. Therefore `C_p` has type
   `10p+1` and is neither level nor Gorenstein.

## Alternatives and redirect criteria

- A defining-ideal calculation is potentially stronger presentation data, but it should follow
  rather than precede the Cohen--Macaulay and socle theorem.
- A Rees-algebra calculation has a larger proof surface and no equally sharp invariant-first
  target yet.
- Nearby Kunz-face classification remains open, but it would broaden the search instead of
  explaining why positivity is restored after killing tangent-cone torsion.
- If the mandatory `p=4` smoke gate refutes `T_p^2=m_pT_p`, stop and redirect to a precise kernel
  description. If the identity holds but the socle formula fails, preserve the canonical quotient
  theorem and redesign only the Artinian-anatomy part.

## Validation design

Route A will reconstruct value sets, ideal powers, minimal monomial generators, multiplication by
`t^q`, and the Artinian socle directly. Route B will use the closed block formulas and the natural
kernel proof. The campaign covers `p=4,...,300`, beginning with `p=4`. An independent audit will
recompute `p=4,5,17,73,151,300`, rehash every row, and reject corruptions of the square identity,
positive-degree kernel, Hilbert function, degree-two socle, and Gorenstein claim. CPU-only budgets
are two minutes for the campaign and one minute for the audit.
