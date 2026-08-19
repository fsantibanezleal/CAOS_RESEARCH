# EXP-028 complete second Betti-row preflight

Date: 2026-08-19. Status: source-complete declaration preflight.

## Reconciled question

EXP-024 and EXP-027 determine

```text
beta_(2,3)=2p(500p^2-330p+31)/3,
beta_(2,4)=8p
```

for the conductor special fiber `C_p=P_p/J_p`, for every `p>=4` and every field. Since `C_p`
has no linear equations and `reg(C_p)=4`, the only unresolved entries in homological degree two
are `beta_(2,5)` and `beta_(2,6)`. Thus these two entries, rather than another isolated
high-dimensional resolution, are the smallest theorem-sized target that completes a whole Betti
row.

The offset-graded Koszul identification proved in EXP-027 remains the primary route. In total
degree `j`, the relative cell with vertex set `F subset G_p` is present exactly when

```text
b-sum(F) is in E_(j-|F|).
```

For `j=5`, first homology depends only on `E_4`, `E_3`, and `E_2`; for `j=6`, it depends only on
`E_5`, `E_4`, and `E_3`. These sets are already known exactly from EXP-021 and EXP-025.

## Fresh primary-source and novelty boundary

The method sweep retained the following primary sources:

- `https://arxiv.org/abs/1804.06632` (Autry et al.), for explicit squarefree-divisor-complex
  classification in numerical-semigroup families;
- `https://arxiv.org/abs/1801.00153` (Stamate), for semigroup Betti methods and the warning that
  characteristic dependence must be tested rather than assumed away;
- `https://arxiv.org/abs/0904.1683` (Reiner--Stamate), for affine-semigroup incidence and Koszul
  topology;
- `https://arxiv.org/abs/1009.4243` (Dalili--Kummini), for discrete-Morse and characteristic-
  dependence mechanisms in monomial resolutions; and
- `https://arxiv.org/abs/1410.6511` (Bolognini), for Betti splitting as a competing recursive
  route.

Fresh exact-family searches found no source computing these two entries or the complete second
Betti row of the present conductor special fibers. The cited sources justify methods and risk
controls; none is evidence for the family-specific formulas declared below.

## Ranked paths

1. **Integral relative-chain matching (selected).** Reduce each offset complex by unit
   coefficient matchings. In degree five, classify the surviving edge cycles and their Morse
   relations. In degree six, prove that every edge cycle is filled. This is exact over `Z` and
   directly controls characteristic dependence.
2. **Mapping cone and cubic colon (audit only).** The exact sequence for
   `J_p=(Q_p,f_p)` explains part of the nonlinear row, but a dimension check shows that new
   quadratic colon generators cannot account for the proposed quadratic-growth total by
   themselves. It remains useful as an independent local audit, not the main proof.
3. **Groebner degeneration and consecutive cancellation.** EXP-026 gives explicit initial data,
   but the transfer supplies upper bounds and possible cancellations rather than the exact row.
4. **Betti splitting.** Potentially useful after a natural decomposition of the relative
   complexes is found; no such decomposition currently improves the direct interval matching.
5. **Raw resolutions.** Rejected as proof machinery because the number of variables is `10p` and
   matrix growth obscures the all-parameter structure.

## Frozen premise ledger

| premise | SHA-256 | use |
|---|---|---|
| EXP-024 `proof.md` | `b7b654609cfca99e979b26741f7d2b6bbbfc0029d882c38e3c2932bfc9146088` | known first row, Hilbert numerator, and regularity |
| EXP-025 `proof.md` | `70c7838ce843252aba335d80ade105d1d1942c490530ea7770483be0dff9a61f` | exact cumulative offset sets `E_n` |
| EXP-026 `proof.md` | `765fa23534be9e534fd507dff0e447e967345e4d2a485f7da6fdf0383b04fb56` | degeneration boundary |
| EXP-027 `proof.md` | `355ff5c7e4bbc74fc8a1e346aac041d77b3fbc758051dbc729836db6a259e0bc` | integral offset-Koszul identification and matching method |
| EXP-027 `verdict.md` | `fa0553e067fceb3ad538136e769ec19c2498dcf123af0df22f281dd3643e9f80` | confirmed adjacent row entry |
| EXP-027 `artifacts/results.json` | `06c630fc74d3e630f4dfbf47736313e6e40ff4e65a30acabe1e1a505b40a123f` | canonical regression oracle |

Any mismatch stops the canonical run as `INCONCLUSIVE_PREMISE`.

## Pre-declaration invariant probe

A read-only probe built the total-degree-five relative chains and reduced their signed boundary
matrices over `GF(2)`. It found

```text
p=4: beta_(2,5)=20,
p=5: beta_(2,5)=35,
p=6: beta_(2,5)=54,
```

and `beta_(2,6)=0` at the smallest tested parameter. The degree-five values fit

```text
beta_(2,5)=p(2p-3).
```

The nonzero degree-five offset support consists of three intervals

```text
A_p=[3p+2,5p-2],
B_p=[6p+1,8p-3],
C_p=[9p,11p-4].
```

Writing `r=0,...,2p-4`, the observed multiplicities on `A_p` and `C_p` are

```text
m_out(r)=min(floor(r/2)+1, floor((2p-4-r)/2)+1),
```

and those on `B_p` are

```text
m_mid(r)=min(r+1, 2p-3-r, p-2).
```

Their sums are respectively `binom(p,2)`, `p(p-2)`, and `binom(p,2)`, giving the proposed total.
The first broad two-degree probe exceeded its 120-second exploratory limit without producing a
canonical artifact; the narrower offset implementation then produced the values above. These are
declaration evidence only. A few ranks over `GF(2)` do not prove an all-parameter formula,
integral freeness, or characteristic independence.

## Declared target and proof route

EXP-028 will test and seek an all-parameter proof that, for every field and every `p>=4`,

```text
beta_(2,5)=p(2p-3),
beta_(2,6)=0,
```

with the displayed complete offset support and multiplicity formulas. Combined with EXP-024 and
EXP-027, this would complete the entire second Betti row.

The proof must:

1. reuse but re-check the relative offset-Koszul identification;
2. give an integral unit matching and explicit critical-edge/Morse-boundary classification in
   total degree five;
3. prove the degree-six first homology vanishes integrally at every offset;
4. prove the support, multiplicity, reflection, and summation identities for arbitrary `p>=4`;
5. run independent signed-chain ranks over unrelated characteristics in the smallest cases; and
6. preserve premise hashes, deterministic artifacts, negative controls, and hard budgets.

## Manuscript gate

Confirmation completes a full homological row and is material enough for a main-manuscript
revision to v0.15. It does not yet justify a separate manuscript: the method and object are the
same as EXP-027. A split becomes appropriate only if the same machinery yields a substantial
portion of the remaining table or a transferable theorem for a wider semigroup family.

