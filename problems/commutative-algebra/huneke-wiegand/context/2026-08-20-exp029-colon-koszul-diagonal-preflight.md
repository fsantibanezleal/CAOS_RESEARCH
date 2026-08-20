# EXP-029 colon-Koszul diagonal preflight

Date: 2026-08-20. Status: source-complete declaration preflight.

## Reconciled question

EXP-028 completes homological degree two for the conductor special fiber

```text
C_p=P_p/J_p,                 J_p=(Q_p,f_p),
f_p=X_0^2X_(3p)-X_p^3.
```

The next persisted target was a higher homological row. A smallest-case relative-homology probe
shows that attacking the entire third row at once is poorly conditioned: the degree-five and
degree-six offset profiles are large, while the top allowed entry vanishes in the two smallest
cases. Retaining the offset grading reveals a much sharper invariant. The complete observed
degree-five second-homology profile is the shifted unordered pair-sum distribution of the `8p`
high variables already identified by EXP-027 in `(Q_p:f_p)_1`.

Put

```text
H_p={a in G_p : a>=6p},      |H_p|=8p.
```

The selected target is therefore the complete internal-degree-five diagonal, not an unstructured
third-row sweep.

## Fresh primary-source and novelty boundary

The 2026-08-20 search rechecked the sources archived for EXP-027 and EXP-028 and searched recent
work on semigroup Betti numbers, relative squarefree-divisor complexes, algebraic discrete Morse
theory, toric splittings, and monomial lcm lattices. The primary method sources retained are:

- `https://arxiv.org/abs/1801.00153`, for numerical-semigroup Betti numbers, squarefree-divisor
  complexes, and characteristic-dependence risks;
- `https://arxiv.org/abs/1804.06632`, for explicit family-wide squarefree-divisor-complex
  classification;
- `https://arxiv.org/abs/math/0501179`, for algebraic discrete Morse cancellation over a ring;
- `https://arxiv.org/abs/1909.12820`, for toric-ideal splittings and the hypotheses needed before
  Betti numbers can be reconstructed recursively;
- `https://arxiv.org/abs/1407.5702`, for Betti-poset recognition in monomial resolutions;
- `https://arxiv.org/abs/2405.01700`, for recent Kunz-face specialization of infinite
  resolutions over numerical semigroup algebras; and
- `https://arxiv.org/abs/2605.27035`, for a recent family-wide Betti computation by combinatorial
  invariance in a different semigroup class.

No located source computes the family-specific diagonal below. The recent specialization theorem
concerns resolutions of the residue field over numerical semigroup algebras, while the current
object is the defining-ring resolution of a truncated affine-semigroup quotient. Toric splitting
also does not apply without a proved splitting of `Q_p`. These papers supply methods and scope
controls, not evidence for the declared formula.

## Ranked paths and redirection

1. **Colon-Koszul anatomy plus integral relative matching (selected).** EXP-027 proves that
   `(Q_p:f_p)_1` is spanned by exactly the `8p` variables indexed by `H_p`. The second Koszul
   wedges on this linear space give a primitive mapping-cone lower bound in bidegree five. An
   integral matching can test whether these are all classes.
2. **Whole third-row enumeration.** Demoted. Exact `p=4,5` probes give nontrivial degree-five and
   degree-six profiles, but only the degree-five profile has an immediately recognizable
   all-parameter mechanism.
3. **Grevlex degeneration.** EXP-026 remains a useful upper-bound and cancellation model. A new
   read-only check shows that its monomial initial ideal is neither stable nor strongly stable in
   either natural variable order, so an Eliahou-Kervaire shortcut is unavailable.
4. **Betti or toric splitting.** Retained as a future path only after a natural decomposition with
   the required intersection control is proved.
5. **Raw full resolutions.** Rejected as proof machinery because `P_p` has `10p` variables and the
   multigraded mechanism is lost.

## Frozen premise ledger

| premise | SHA-256 | use |
|---|---|---|
| EXP-023 `proof.md` | `4f24c8bacf3ea4a7691142b6fbb2a79b40a1c200ec5051df3c79c3dc45bed084` | `J_p=(Q_p,f_p)` and the unique cubic |
| EXP-024 `proof.md` | `b7b654609cfca99e979b26741f7d2b6bbbfc0029d882c38e3c2932bfc9146088` | Hilbert numerator, regularity, and minimal-shift bounds |
| EXP-025 `proof.md` | `70c7838ce843252aba335d80ade105d1d1942c490530ea7770483be0dff9a61f` | truncated-monomial model and cumulative offset sets |
| EXP-026 `proof.md` | `765fa23534be9e534fd507dff0e447e967345e4d2a485f7da6fdf0383b04fb56` | exact monomial degeneration boundary |
| EXP-027 `proof.md` | `355ff5c7e4bbc74fc8a1e346aac041d77b3fbc758051dbc729836db6a259e0bc` | relative chains and exact linear cubic colon |
| EXP-028 `proof.md` | `7c382237b8ab87d6c8ff6e0ff8b37ccfd586fcc0f8ea4e7c9c9acb3ab0297ace` | complete second row and integral matching method |
| EXP-028 `verdict.md` | `2bdbd96cb37d6891ca4f3fc0d5796a7c016e398f7ddfc5cbc00d0b26d0cac1ff` | confirmed scope boundary |
| EXP-028 `results.json` | `d7ecf4078907d427e6641eeec359dd007bc0411ee1e77018e5b3a19306bfe96d` | canonical regression oracle |

Any mismatch stops a canonical run as `INCONCLUSIVE_PREMISE`.

## Pre-declaration invariant probe

A read-only sparse relative-chain probe computed `H_2` in the unresolved third-row degrees. It
used exact finite-field arithmetic and produced no canonical artifact.

```text
             beta_(3,5)   beta_(3,6)   beta_(3,7)
p=4              496           704            0
p=5              780          1560            0
```

At `p=4`, both `GF(2)` and `GF(1000003)` give the same complete profiles. At `p=5`, the
discriminating probe used `GF(2)`. The degree-five values equal

```text
binom(8p,2)=4p(8p-1).
```

More strongly, every degree-five offset multiplicity equals the number of unordered distinct
pairs `a<c` in `H_p` with `a+c=b-3p`. The support is

```text
[15p+1,39p-3] minus {33p-1}.
```

For `p=4,5`, these pair profiles reproduce all observed multiplicities, totals, endpoints, and
the unique hole. Greedy integral matching leaves the pair-indexed critical triangles
`{p,a,c}`; at some low offsets it also leaves transient triangles that must be cancelled by unit
Morse boundaries from critical tetrahedra. Thus the raw critical-cell count is deliberately not
treated as homology.

The probe also tested the EXP-026 initial ideal for stability and strong stability in both natural
orders. All four tests fail already at a quadratic generator, so the degeneration cannot replace
the relative-chain proof.

## Declared proof route

EXP-029 will seek an all-parameter integral proof that the pair-indexed classes are the complete
degree-five `H_2`. The mapping cone supplies primitive lower-bound classes. The relative complex
must supply the matching upper bound by unit cancellations, including every transient triangle.
Once `beta_(3,5)` is proved, the coefficient of degree five in the frozen Hilbert numerator and
EXP-028 determine `beta_(4,5)`, completing that internal-degree diagonal.

Finite-field agreement cannot establish characteristic independence. That conclusion requires
the integral unit matching and primitive mapping-cone classes.

## Manuscript gate

Confirmation would complete a second full diagonal and expose a new colon-Koszul mechanism, so it
is material enough to expand the main manuscript. A separate manuscript remains deferred until a
substantial portion of the remaining third row or a transferable theorem beyond this family is
proved.

