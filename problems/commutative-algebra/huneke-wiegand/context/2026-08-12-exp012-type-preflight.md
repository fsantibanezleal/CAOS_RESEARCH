# EXP-012 pseudo-Frobenius and reduced-type preflight

Date: 2026-08-12. This preflight was completed before EXP-012 implementation or execution.

## Exact question

For the EXP-011 endomorphism semigroup `Lambda_p`, determine the complete pseudo-Frobenius set,
the Cohen-Macaulay type, the reduced type, and the almost-symmetric status uniformly for every
integer `p>=4`.

This is narrower and more decision-bearing than a nearby-Kunz-face search. It quantifies how far
the endomorphism ring is from Gorenstein and tests a current positive-theorem boundary using one
semigroup invariant.

## Primary-source pass

The following primary records were checked through their relevant theorem, proof, closing, and
open-question sections. PDFs and extracted text are archived outside Git under
`E:/_Datos/caos-research/huneke-wiegand/sources/`.

| source | load-bearing point | archived SHA-256 |
|---|---|---|
| S. Maitra and V. Mukundan, *Extremal behavior of reduced type of one dimensional rings*, arXiv:2306.17069v1 | Theorem 2.13 counts reduced type as the gaps in `[c-m,c-1]`; Proposition 3.7 characterizes maximal reduced type by the location of `PF(H)` | `082f9daab679f2c6d38458b27f4d7fa85d536bb33fecfad051b7b20f92ee1863` |
| O. P. Bhardwaj, *Reduced type of certain numerical semigroup rings*, arXiv:2406.15923v1 | Confirms the pseudo-Frobenius/type dictionary and treats exact parametric PF descriptions as the appropriate proof surface | `fccba6391789fcf4dc0db88dca7829cb949d233ffc97c68795728187ebee3121` |
| S. Dey and J. Lyle, *Centers of endomorphism rings and reflexivity*, arXiv:2510.02210v2 | A Gorenstein endomorphism center would force a positive Huneke-Wiegand conclusion; EXP-011 already proves the family centers are not Gorenstein | `2f1521f79510ef50fb81d5f029935d5a2c9b7e4c030bc698b7e4f5caacf56fad` |
| H. Lindo, S. Maitra, and W. Zhang, *Trace does not preserve reflexivity*, arXiv:2509.12576v1; version of record DOI 10.1007/s13348-026-00515-0 | Corollary 5.6 supplies a separate future trace/endomorphism criterion; it does not decide the present PF computation | `9060c45e4d53b0617c7ad95d77f2b9c3df6662451643890dc6858d012fe5bbcf` |

Fresh searches for the exact formulas `24p`, `54p-1`, and `38p-1`, and for a parametric
Huneke-Wiegand pseudo-Frobenius calculation found no matching primary record. That negative search
is a novelty-risk check, not proof of novelty.

## Invariant-first derivation

EXP-011 gives multiplicity `m=4s`, conductor `c=9s`, and residue blocks

```text
L_4=A, L_5=[0,s-1], L_6=B, L_7=Q, L_8=C,
L_k=[0,s-1] for k>=9.
```

Every gap in `[c-m,c-1]=[5s,9s-1]` is automatically pseudo-Frobenius because adding any positive
semigroup element crosses the conductor. These are exactly the complements of `B`, `Q`, and `C`
at levels 6, 7, and 8, totaling `3p+5p+2p=10p`.

The only remaining question is whether a pseudo-Frobenius number occurs below `5s`. The full
level-5 generator block and the level-4 block containing residues zero through `p` provide cheap
candidate witnesses against every lower gap. EXP-012 will make this hand derivation exact and
audit it by two independent finite routes.

## Lenses and redirection

- Exclusion: exclude every lower gap from `PF(Lambda_p)` with an explicit minimal-generator witness.
- Anatomy: describe the complete top-window PF blocks.
- Invariant: type and reduced type replace a nearby-face SAT sweep.
- Recognition: test maximal reduced type and almost symmetry using current classification criteria.
- External dialogue: the 2026 trace/reflexivity result opens a separate trace-ideal route after this
  invariant is settled.

The current spine remains exact block analysis. Unconstrained SAT classification is not justified
because it cannot deliver a uniform theorem more cheaply than the present invariant.
