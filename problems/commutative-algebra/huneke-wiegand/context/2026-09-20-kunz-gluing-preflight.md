# Kunz-face and simple-gluing preflight

Date: 2026-09-20. This is a focus-selection record, not an experiment verdict
or a novelty certificate.

## Source review

The following primary sources were reviewed before declaring EXP-067:

- Son Pham, *A Counterexample to the Huneke-Wiegand Conjecture*,
  <https://arxiv.org/abs/2609.07615>. The rigidity proof is reduced to a finite
  sumset identity and the two-generated colon criterion.
- Borevitz et al., *On faces of the Kunz cone and the numerical semigroups
  within them*, <https://arxiv.org/abs/2309.07793>. A Kunz face belongs to one
  fixed multiplicity cone and is indexed by a Kunz nilsemigroup.
- Brower, McDonough, and O'Neill, *Numerical semigroups, polyhedra, and posets
  IV: walking the faces of the Kunz cone*,
  <https://arxiv.org/abs/2401.06025>. This supplies the face-walking and Kunz
  fan setting.
- Casabella, D'Anna, and Garcia-Sanchez, *Apery sets and the ideal class monoid
  of a numerical semigroup*, <https://arxiv.org/abs/2302.09647>. This connects
  normalized semigroup ideals to Apery sets and Kunz coordinates.
- Gimenez and Srinivasan, *On gluing semigroups in N^n and the consequences*,
  <https://arxiv.org/abs/2202.01189>. Simple numerical-semigroup gluings and
  inheritance of the Gorenstein property are established there.
- Landeros et al., *Families of numerical semigroups and a special case of the
  Huneke-Wiegand conjecture*, <https://arxiv.org/abs/2404.12519>. This is a
  positive-family boundary, not an overlap with the proposed transfer.

No reviewed source states the proposed transfer of a two-generated rigidity
identity through the simple gluing `m*N + q*Gamma`. That negative search is not
proof of novelty; specialist confirmation remains required.

## Correction to the first Kunz-face formulation

The EXP-009 family has multiplicity `m_p=24p`. Its members therefore lie in
different cones `C_(24p)`, so no single fixed-multiplicity Kunz face can contain
the whole family. The original singular-face formulation of `HW-F6` was
ill-posed.

A bounded diagnostic computed the active Kunz equalities for `p=4,...,8`.
Their coefficient ranks over two independent large primes were
`m_p-2`, so every tested point lies on a one-dimensional face. The active
equality counts were `534, 828, 1185, 1605, 2088`, matching
`(63p^2+21p-24)/2`. These exploratory counts motivated the next question but
are not used as theorem evidence.

## Stronger redirect

The ray-like Apery behavior exposes a standard simple gluing. For a numerical
semigroup `Gamma` of multiplicity `m` and an integer `q` coprime to `m`, put

```text
Gamma^(q) = m*N + q*Gamma = <m, q*g : g in a generating set of Gamma>.
```

If `s` is the normalized two-generator shift, the natural new shift is `q*s`.
The decisive question is whether the exponent sets

```text
E = {a in Gamma : a+s in Gamma},
D = {a in Gamma : a+s and a+2s are in Gamma}
```

obey exact transfer formulas

```text
E^(q) = m*N + q*E,
D^(q) = m*N + q*D.
```

If so, `D=E+E` transfers formally to
`D^(q)=E^(q)+E^(q)`. This would amplify any symmetric two-generated monomial
counterexample into infinitely many simple-gluing descendants and give a
two-parameter extension of the CAOS family. This is more direct and valuable
than classifying active equalities alone, so the Kunz-face route is redirected
to EXP-067.
