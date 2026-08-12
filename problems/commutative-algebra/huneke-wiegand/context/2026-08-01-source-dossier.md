# Huneke-Wiegand counterexample and extension dossier

## Priority and current public status

Discovery credit belongs to Son Pham. Public verification repository:
`https://github.com/sonpham-org/huneke-wiegand-candidate-verification`.
Professor Craig Huneke's independent note is archived externally with SHA-256
`367a48f83fa41971636e98b65311317405d228d6cced8f0993cfc3e7f54235d2`.
The note independently proves the colon equality and applies Huneke-Iyengar-Wiegand. This is
expert verification, not a substitute for later peer review.

## Primary sources used

- Leamer, `https://arxiv.org/abs/1211.2896`: for a two-generated fractional ideal L,
  tensor torsion is `(L^2)^-1/(L^-1)^2`.
- García-Sánchez--Leamer, `https://arxiv.org/abs/1211.4554`: complete-intersection numerical
  semigroups are positive for two-generated monomial ideals; reported exhaustive frontier F<69.
- Huneke--Iyengar--Wiegand, `https://arxiv.org/abs/1804.00939`: rigidity equivalence and the
  two-principal-colon criterion; positive multiplicity and generator bounds.
- Celikbas--Goto--Takahashi--Taniguchi, `https://arxiv.org/abs/1710.07398`: positive ideal classes.
- Celikbas--Le--Matsui--Sadeghi, `https://arxiv.org/abs/2202.04792`: periodic and
  complete-intersection routes.
- Dey--Kobayashi, `https://arxiv.org/abs/2201.01023`: Burch and weakly-m-full conditions.
- Landeros et al., `https://arxiv.org/abs/2404.12519`: generalized arithmetic-sequence
  numerical semigroups.
- Dey--Lyle, `https://arxiv.org/abs/2510.02210`: endomorphism-center/reflexivity criteria.
- Herzog--Kumashiro, DOI `10.1007/s00013-022-01764-8`: Proposition 3.1, Claim 1 identifies
  `length(R/(R:S))=length(S/R)` as one-dimensional Gorenstein local duality for finite birational
  extensions; this prevents treating EXP-013's balanced colength as a family-specific mechanism.
- Dey, `https://arxiv.org/abs/2212.09087`: Corollary 3.7 proves that the conductor of a finite
  birational extension of a one-dimensional Gorenstein local ring is stable exactly when the
  extension ring is Gorenstein; EXP-012 therefore forces nonstability in the explicit family.

Exact source archives and hashes live outside Git at
`E:/_Datos/caos-research/huneke-wiegand/sources/`.

## Candidate arithmetic imported only as a target

```text
F(Gamma)=181, conductor=182, genus=91
B={56,57,58,63,64,73,75,76,79,81,82,83}
C=[112,116] U [119,122] U [126,152] U [154,166]
B+B=C
```

EXP-001 must recompute the result without importing or executing upstream verification code.

## Open extension surface

The public package does not establish minimality, classify all examples, produce an infinite
family, or analyze the candidate against the 2025 endomorphism-ring criteria. Those are the
programme's novelty targets.
