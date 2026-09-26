# EXP-010 adversarial validation record

Date: 2026-09-26. Declaration commit:
`2f7aaa6b` (baseline `7a0711adb7e0f93b3a9429f6304f74f8951f8d69`).
Canonical execution commit: `3dba086fed900d5a828bb78182fc68541b641d8a`.
Controls execution commit: `770003367350b04be70e672d076ba0e5d3d99ecf`. This is an
internal proof, source-interface and interval audit with two independent
referee passes. It is not external peer review.

## Source audit

Young's arXiv:1002.4403v1 TeX source (SHA-256 pinned in
`context/source-manifest-exp010.json`) was compiled and its rendered numbering
checked: Theorem 1 (1.2)-(1.3), Theorem 2 (2.4), Lemma 3 (3.2)-(3.4), Lemma 4
(approximate functional equation, (4.1)-(4.3)), Lemma 5 (twisted integral,
(4.4)), Section 5 ((5.1), Lemma 6, (5.2)-(5.3)), Section 6 ((6.1)-(6.3),
Lemma 7) and Section 7 (arithmetic factor). The first proof draft cited
Lemmas 1, 2, 4 and 5 and equations (4.5), (5.1)-(5.3) for these objects; every
citation was corrected before the proof was committed. Young's printed (4.3)
has the decay factor `(1+|t/x|)^(-A)`; the Mellin representation (4.1) and his
own proof of Lemma 5 use `(1+x/t)^(-A)`, which is what the proof uses.

Conrey 1989 (local scan, SHA-256 in the preflight dossier) supplies the
constant `c(P,Q,R,theta)` of Theorem 2 and the counting conventions of eqs.
(32) and (40)-(41). CFKL arXiv:2508.11108v1 supplies only the motivation for
high-degree `Q`; no CFKL theorem is a premise. Wang arXiv:2609.07918v1 and the
EXP-006 product enter only Theorem D.

## Mandatory attacks

| Possible failure | Attack and outcome |
|---|---|
| The off-diagonal of the short-window twisted integral might need a stronger restriction than `nu<theta-1/2` | Rejected. With `Delta=H/L`, `2 sqrt(hkmn)/Delta<=2L T^(-3eta/4)` for `mn<=T^(1+eps)`, `eta=theta-1/2-nu`, `eps=eta/2`; `j>4(A+5)/(3 eta)` integrations by parts give `O(T^-A)`. |
| The tail `mn>T^(1+eps)` might not be summable after integration by parts | The first draft chose the decay exponent `A'>=j+A+3`, which does not make the tail `O(T^-A)` (the sum is about `T^((1+eps)(j+1)/2-eps A')`). Fixed: no integration by parts in the tail; the trivial bound with `A'>=(A+3)/eps` gives `O(T^-A)`. |
| Replacing `X_{alpha,beta,t}` by `T^(-alpha-beta)(1+O(1/L))` inside the `t`-integral cannot be factored out of `I_2` | Correct objection to the first draft (Young's global text is equally terse). Fixed: on the window `X=(T/2pi)^(-alpha-beta)(1+rho)`, `rho<<H/T`; the absolute diagonal sum is `<<L^4`, so the `rho`-part is `<<H(H/T)L^6=o(H/L)`. This is the only use of `theta<1`. |
| The contour shift might lose the saving on a short weight | The only `w`-dependent factor is `int w g(s,t)dt<<H T^(-delta+eps)(1+abs(s)^2)`; the new contour gives `H T^(-delta(1-2nu)+eps)=o(H/L)`. The pole of `zeta(1+alpha+beta+2s)` is cancelled by `G`. |
| `G(s)` depends on `alpha+beta` and could make the bounds non-uniform | On the annuli `abs(alpha+beta)>>1/L`, `p(s)<<L^2(1+abs(s)^2)`; the extra `L^2` is absorbed. Maximum modulus extends the result to discs. |
| Theorem A for the monomials `Q=x^j` violates `Q(0)=1` | Fixed: `L^(-j)zeta^(j)=(-1)^j(V_(1+x^j)-zeta)`, and Theorem A applies to `1` and `1+x^j`. |
| The literal error `zeta-V-chi V(1-s)` is not small for published `Q` | Correct; published `Q` have `beta` between `0.967` and `0.984`. The proof uses `E_beta=beta zeta-V-chi V(1-s)`, whose realness is exact and whose size is `<<1/L` per derivative. |
| With `L=log T`, `E_beta` is only `O(1/L)` relative to `V` | True (controls: up to `0.31` at `T=1e4`, against `0.003` with `L=log(T/2pi)`). Sufficient: the mean square is `O(H/L^2)` and the split `(1+L^(-1/2),1+L^(1/2))` costs `O(H L^(-1/2))`. |
| On-line zeros of `Vt` might be charged at weight zero | Then the lemma is false: toy A with `Q=1-x` has 24 sign changes against a strict bound `36.36`. The proof charges them at full weight; Littlewood's lemma pays `R/L` for each. |
| Double zeros of `Z` might be counted as sign changes | They are not sign changes. Toy A (seven planted double zeros): 24 sign changes, equal to `N_f-2N_Vt=38-14` for `Q=1-x` and `38-2*7` for the cubic, where the seven charges are zeros of `Vt` right of the line. |
| Simplicity might be claimed for `deg Q>=3` | Not claimed. Toy B (three planted triple zeros) with the cubic has 31 sign changes but 28 simple zeros. Simplicity comes only from the parity product. |
| The level-crossing step might merge crossings or miscount at the zeros of `Vt` | The written proof uses first-hitting points of `c_i+pi/2`, where `cos phi` alternates, and loses at most `J` intervals where `p` changes sign. Controls: sign changes equal level crossings on all zeta windows. |
| The horizontal-side and `sigma_1` bounds for `Vt` might fail because `Vt` contains `chi V(1-s)` | `Vt=sum a_j(s)zeta^(j)(s)` with `a_j` polynomials in `1/L`, `lambda` and its derivatives: holomorphic and polynomially bounded near the window, `Re Vt>=1/2` at `sigma_1`. |
| The parity transfer might need a different order of limits | Identical to EXP-006: fixed test function, height limit, cosine limit at fixed `lambda`, then `lambda->theta`. The detector enters only through `liminf o_T>=k`. |
| `h_L` might be presented as an improvement where Wang's `c(theta)` is larger | At `theta=0.60`, `c=0.13455>h_L=0.09295`. The claim is the maximum of four terms; `h_L` is the largest term only below about `0.567` (exploratory, not certified). All certified gains are at `theta<=0.55`, where `c<0`. |
| The frozen detector might be inadmissible at the target exponent | Each set uses `nu=theta-1/2-10^-4<theta-1/2`; the extension to `[0.534,1)` uses the single admissible `nu=0.0339`. |
| The exact reduction `c=A e^(2R)+B` might hide an algebra error | The auditor never forms moments: it evaluates `Q` from its Chebyshev coefficients, separates the double integral by Fubini, integrates by validated Arb quadrature and overlaps every enclosure. Focused test: direct 2-D quadrature equals the exact form for Young's parameters. |
| The published anchors might not be reproduced | Young `c=2.35006777611844...` and Conrey `kappa>0.4088` are reproduced by the canonical run. |
| A dirty worktree might contaminate the outputs | Both receipts record a clean tracked tree; the auditor refuses a producer result whose declaration, runner or frozen-file hash differs. |
| The result might imply RH, an effective height, or universal simplicity | It implies none of them. Theorem D uses Wang's recent unreviewed preprint for the pair term. |

## Independent referee passes

Two independent referee passes were run on the committed proof, one on
Theorem A and one on Theorems B and D, with instructions to break the proof.
Their findings and dispositions are recorded below.

(pending)
