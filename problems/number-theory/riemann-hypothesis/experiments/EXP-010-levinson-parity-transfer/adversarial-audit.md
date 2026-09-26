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
Theorem A and one on Theorems B and D, with instructions to break it. Each
wrote its own code. Neither found a fatal or major mathematical error; both
returned "sound with fixes". Every fix below is applied in the final proof,
whose SHA-256 is bound by the rerun audit.

### Theorem A referee

| Finding | Severity | Disposition |
|---|---|---|
| Prediction A extends `c(P,Q,R,nu)`, whose constant term is `1`, to every real `Q`. The operator maps that term to `Q(0)^2`, so the declared statement is false when `Q(0)^2!=1` (`P=0.7x+0.3x^2`, `Q=2-0.9x+0.4x^2`, `R=1.1`, `nu=0.2`: `61.0999...` against `58.0999...`, rechecked here) | major for declaration compliance, not a gap | Recorded as a scope correction in the verdict; the proof now states the general constant `Q(0)^2+...`. Every polynomial used has `Q(0)=1` |
| Stirling (4.2) is uniform only for `abs(s)=o(t^(1/2))` | minor | Added: for `abs(Im s)>=T^(1/3)` the Gaussian decay of `G` beats the crude bound on `g` |
| The remark on where `theta<1` enters was incomplete | minor | Reworded: `H=o(T)` also places the support in `[T/2,2T]` |
| `epsilon` used twice; `M` must also become `y` in (3.3); dependence on `R`; the invariance applies to the annulus region | minor | Fixed (`epsilon_1` for the contour offset) |
| The declaration's "Young, Lemmas 1-6" should read Theorem 2 and Lemmas 3-7 | minor | Recorded in the verdict; every citation inside the proof matched the TeX |
| Section 2.3 is tighter than Young's own global step, which would need Lemma 6 rerun with a modified weight | informational | Noted |
| At `eta=1e-4` the factor `2L T^(-3eta/4)` is below one only for `log T` above about `1.7e5` | informational | Added to the remark on constants |

The referee also sampled 655,346 values of `zeta` and `zeta'` at `T=1e6`,
`theta=0.75`, and found the smoothed short-window moment equal to the
finite-`y` residue predictor to relative `2e-4` for `nu<=0.4` in four disjoint
windows; the off-diagonal and contour remainders are negligible even at this
height. The gap to the asymptotic constant is `O(1/L)` with a large constant.
This is exploratory evidence, not part of the proof.

### Theorems B and D referee

| Finding | Severity | Disposition |
|---|---|---|
| The perturbation clause of Lemma 3.1 was garbled; `L` must stay fixed while endpoints move, and the endpoints must also avoid critical zeros and zeros of `psi` | minor | Restated with `L=log T_0` fixed, endpoints moved inward by less than one unit, cost `O(L)` by Jensen |
| Enlarging the factors in Theorem D needs `q_T>=s_T` and `C(f)+epsilon-s_T>=0` | minor | Added EXP-006's case split (`O=N` gives `s_T=1`) |
| The declaration's premise table cites CIS (A.16)-(A.18) for weight one, but CIS pass on-line zeros from the east (weight zero) | minor (citation) | Recorded in the verdict and in a dated correction to the preflight; Conrey (32) with (40)-(41) is the precedent; the proof never used CIS |
| `w>=1` should read `w=1` with `w>=0`; Backlund for `psi Vt` should be stated for both factors | minor | Fixed |
| "At most `k-1` further factors" was loose | minor | Replaced by the normal-ordered coefficient bound `O(L^(k-m-1))` |
| The constants are astronomically large for the frozen `Q` | minor | Remark on constants added |
| `J` can be replaced by the number of odd `k_j` | optional | Noted |

This referee reproduced the identities to relative `3e-35` at `T=1e4,1e5,1e6`,
confirmed that `epsilon_j L` stays bounded from `T=1e4` to `1e30`, tested
Lemma 3.1 on toys with an off-line pair, a clustered on-line pair and a double
zero, recomputed `kappa` and `h` by Gauss-Legendre quadrature from the
Chebyshev form (agreement to all printed digits), confirmed that
`h(theta;kappa(0.0339))` increases on 4001 points of `[0.534,0.9999]`, and
recomputed the cosine limit `C(f)=2-c(lambda)`.
