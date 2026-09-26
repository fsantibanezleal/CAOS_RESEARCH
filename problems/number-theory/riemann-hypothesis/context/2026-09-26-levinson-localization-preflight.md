# Localized Levinson-Conrey detector: EXP-010 preflight

Date: 2026-09-26. Online search window: 2026-09-20 12:40 UTC to 2026-09-26.
Status: primary-source preflight for EXP-010. Every number below is an
exploratory scratch value unless it is attributed to a source; the canonical
values belong to the EXP-010 artifacts and verdict.

## 1. Why the odd-support detector is the lever

The current onset solves `A(theta)(1-k(theta))=2`, where `A=2-c` is Wang's
short-interval pair constant and `k` is the odd-support density fed into the
EXP-006 product. At the EXP-008 root the sensitivities are:

| Input | Onset response |
|---|---|
| Selberg constant `C_q` | `+0.00599` per unit of `C`; the rank-three to rank-six change moved the onset by `-8.46e-7` |
| Additive change of `k` | `-0.612` per unit of `k` |
| Pair-correlation support | `-0.914` per unit, nearly one-for-one |
| Pair constant `A` at fixed support | `-0.302` per unit |

The localized Selberg detector has `k_6(theta)=(theta-1/2)/(4eC_6)`, a slope of
about `0.140`. A detector with slope `s` gives onset `0.5418` for `s=0.3`,
`0.5376` for `s=0.5` and `0.5342` for `s=0.7`. Improving `C_q` (RH-021) cannot move
the onset by more than about `1e-5` for any plausible profile, although it
remains an integrity task. Pair-correlation support beyond `lambda<theta` is
blocked by an off-diagonal of the same order as the main term.

## 2. Online sweep since the 2026-09-20 cutoff

No pinned source has a new version: arXiv:2608.13637 is still v2,
arXiv:2609.02882 v2, arXiv:2609.07918 v1 and arXiv:2609.15329 v1; the pinned Lean
repositories are unchanged. Relevant new items:

| Item | Content | Effect |
|---|---|---|
| Biao Wang, arXiv:2609.24167v1 | Global `C_0+delta_0`, `delta_0=6.66624e-8`, with the same Gram defect as EXP-007 | Covered by `2026-09-24-wang-global-refinement.md` and EXP-009; no onset effect |
| arXiv:2609.22624v1 | Explicit zero-density in bounded windows away from the edge of the strip | No critical-line or simplicity input |
| arXiv:2608.16034v2 and arXiv:2609.27808v1 | Montgomery-Taylor constants for a prime-modulus Dirichlet family | Family analogue; no zeta short-interval effect |
| Zenodo 22287432, 22066689 (and concept 21940706) | Unreviewed global claims up to `0.673399`, with a stated ceiling `0.6736` for the fixed Montgomery-Taylor kernel with pure Gram machinery | Global only |
| GitHub `MichaelMobius/simple_zeros_of_the_riemann_zeta_function`, `RakitinD/zeta-xi-zero-results` | Unreviewed global claims `0.6731175` and `0.6734776` | Global only |
| arXiv:2609.20367v2 | Unrefereed claimed proof of RH through Weil positivity | Quarantined; not evidence |

No located source gives a short-interval simple-critical onset below the
record's `0.5458838`, an improved Selberg constant, or Pearce-Crump's rank-six
coefficient matrix.

## 3. The short-interval moment (gate 1)

The Levinson inequality needs, uniformly for shifts `alpha,beta<<1/L`, the
mollified shifted second moment on a window of length `H=T^theta`. Sources
inspected, with their exact reach:

| Source | Statement | Reach |
|---|---|---|
| Young, arXiv:1002.4403v1, Lemma 3 and Theorem 2 | `I(alpha,beta)=c(alpha,beta)w-hat(0)+O(T/L)` with smoothing scale `Delta=T/L` | Global; the proof template |
| Young, Lemma 5 | Twisted formula for `hk<=T^(2 theta)`, off-diagonal killed by `abs(log(hm/kn))>=1/(2 sqrt(hkmn))` | The only step that uses the window length |
| Conrey 1989, Theorem 2 and eq. (39) | `int_2^T abs(VB)^2 ~ c(P,Q,R)T` for mollifier exponent `<4/7` | Global asymptotic, no error term |
| Conrey 1989, Proposition, p. 11, and eq. (75) | Gaussian windows `T^(1-delta)`, uniform shifts | Needs `delta<1/7-nu/4`, i.e. windows only for `theta>6/7+nu/4` |
| Balasubramanian-Conrey-Heath-Brown 1985, Theorems 1 and 2 | Critical-line twisted mean squares; Gaussian windows with error `Delta^(-7/2)T^(5/2+eps)M^2` | No shifts |
| Steuding 1999 dissertation, Theorem 2.1 (printed p. 11) | Short-interval mollified moment for `zeta+zeta'/L` with error `O(T^(1/3+eps)M^(4/3))` | Degree-one `Q` and fixed shifts only; the 2002 journal version was not accessed |
| Motohashi 1986, Note V | Global `E(T,A)<<T^(1/3)M^(4/3)T^eps` | Announcement, unshifted |
| Bettin-Chandee-Radziwill 2017; Hughes-Young 2010; Tang arXiv:2608.14852v1 | Long mollifiers, fourth moments, or prime-twist reciprocity | Not usable here |

No published theorem states the needed short-interval shifted moment, and no
global formula with a power-saving error uniform in twist and shifts can be
differenced. The gap is closed by rerunning Young's argument with a weight of
support `[T-Delta,T+H+Delta]`, `Delta=H/L`: integration by parts bounds each
off-diagonal term by `H(1+mn/T)^(-A)(2 sqrt(hkmn)/Delta)^j`, which is `T^(-A)`
whenever `hk<=Delta^2T^(-1-eps)`; for `h,k<=T^nu` this is exactly
`nu<theta-1/2`. The reflected term, the contour shift (error
`O(H T^(-delta(1-2nu)+eps))`) and the arithmetic lemmas carry over with
`w-hat(0)` in place of `T`. This is EXP-010 Prediction A. A Steuding-type range
`nu<(3theta-1)/4` for general `Q` would need a two-shift Atkinson analysis far
beyond a few pages.

## 4. What the method counts (gate 2)

The classical sources differ only in the weight given to zeros of the Levinson
function on the critical line:

| Weight on on-line zeros | Source convention | Count obtained |
|---|---|---|
| 0 | zeros with `sigma>1/2` only | critical zeros with multiplicity |
| 1/2 | Conrey 1989 eq. (32) | distinct critical zeros |
| 1 | Conrey 1989 eqs. (40)-(41); Conrey-Iwaniec-Soundararajan (A.16)-(A.18) | points where the detector's real part vanishes and the detector does not |

Conrey's eq. (43) and Bui-Conrey-Young restrict simple-zero conclusions to
`deg Q=1`. CFKL state nothing about odd or simple zeros for high degree. The
preflight proof, recorded as EXP-010 Prediction B, shows that at weight one the
level-crossing count of a continuous argument gives distinct sign changes of
`Z`, i.e. distinct odd-order critical zeros, for every admissible `Q` with
`beta=Q(0)+Q(1)` nonzero. Two corrections to the first sketch were found: the
error must be normalized as `E_beta=beta zeta-V-chi V(1-s)` (published `Q` have
`beta` between `0.967` and `0.984`, for which the unnormalized `E` is not small),
and on-line zeros must carry full weight (the `sigma>1/2` variant is false).
Scratch checks at `T=10^4,10^5,10^6` confirmed the exact identity
`beta Z=2Re(omega Vt)` to relative error below `1e-24`, matched sign changes of
`Z` to level crossings for `Q` of degree `1`, `3` and `5`, and showed on toy
functions with planted double and triple zeros that the bound is tight, that
double zeros are never counted, and that simplicity does not transfer for
degree at least three.

## 5. The detector constant (gate 3)

CFKL (arXiv:2508.11108v1) eqs. (15)-(16) state
`c=1+(1/theta) int int (w(y)P'(x)+theta w'(y)P(x))^2`, `w=e^(Ry)Q`, with
`Q(0)=1`, `Q(y)+Q(1-y)=1` (their (18)), citing Conrey 1989 Theorem 2. The formula
agrees with Young (1.3) and Bui-Conrey-Young (3.2) and was re-derived
symbolically. Scratch replays reproduced Young's `c=2.3500678` (`kappa=0.34274`),
Conrey's `0.4013` and his note-added-in-proof `0.4088`. Two errata in CFKL were
found: the Section 6 table entries at `theta=1/2` and `2/3` (`0.334`, `0.364`)
come from a large-`R` approximation (the exact values for their parameters are
`0.358437` and `0.446367`), and eq. (64) has a sign typo in the third parameter.

With `c=A e^(2R)+B` for exact rationals `A,B`, a certified `kappa` needs one Arb
exponential and one logarithm. Scratch certificates for degree-201 `Q` and a
truncated-`sinh` `P` gave `kappa/nu=0.71733` for `nu` in `[0.03,0.10]`, close to
the Euler-Lagrange ceiling `0.7173` of the single-piece mollifier; CFKL's own
parameters give `0.6824nu`. Keeping the loss below `0.1%` needs roughly
`deg Q>=4/nu`. Degree-one `Q` needs `nu>0.1928` (`Q=1-x`, `P=x`) or `nu>0.1635`
(best linear `Q`), so the gain requires high degree and therefore goes through
the parity product rather than a direct simple-zero count.

## 6. Route decision

EXP-010 localizes the Levinson-Conrey detector as a distinct sign-change count
and substitutes it for the Selberg detector in the unchanged EXP-006 product.
Scratch values place the onset near `0.53399`, give about `0.0178` at
`theta=0.5459` (EXP-008: `1.78e-5`), and exceed the Selberg density by a factor
of about `5.11` at every tested exponent.

Routes set aside, with reasons:

- Improving `C_q`: at most about `1e-5` of onset; RH-021 stays an integrity task.
- Scalar or geometric sharpening of `(Q-S)(N-O)>=2(N-S)^2` at `S=0`: periodic
  chains of real triples with nearby off-line pairs nearly saturate it under the
  actual Montgomery-Taylor kernel.
- Pair-correlation support beyond `lambda<theta`: the prime-pair off-diagonal is
  of the order of the main term.
- Spectral or Gram defects: they vanish in the onset-extremal configuration.

Next routes after EXP-010: a Steuding-type moment range for general `Q`, which
scratch sensitivities place near an onset of `0.496`, below `1/2`, and a
two-piece mollifier in short windows.

## 7. Note on the EXP-005 and EXP-008 detour step

Pearce-Crump's rectangle-sign lemma, imported by EXP-005 and EXP-008, says the
argument moves by at most `pi` between sign changes "with the usual infinitesimal
detours". At on-line zeros of the detector this is not literally true, for the
same reason as in section 4. The final inequality survives, because the defect
is dominated by those zeros' own nonnegative Littlewood contribution, which the
proof discards. This is a proof-hygiene remark for a future revision, not a
change of any verdict.

## 8. Local-only sources

The Crelle scans used for page references are retained locally under research
use terms and are not redistributed: Conrey 1989 (SHA-256
`dca940c13c721df8569c8cc66cdcdb745cb413dea2730dc51daf2e7bb091b8e9`) and
Balasubramanian-Conrey-Heath-Brown 1985 (SHA-256
`27b7e4818e85c5b1b83cf8a2001d448851027ff9c0bb6470f591de9eda449ad3`). Steuding's
dissertation is already pinned in `source-cache/critical-mass-source-downloads.json`.
The arXiv sources Young, CFKL and Bui-Conrey-Young are pinned in
[`source-manifest-exp010.json`](source-manifest-exp010.json).

## 9. Correction after the EXP-010 referee pass

The table in Section 4 lists Conrey-Iwaniec-Soundararajan (A.16)-(A.18) beside
Conrey's eqs. (40)-(41) as weight-one precedents. That is not accurate. CIS
pass the zeros of their detector on the critical line "from the east side",
which gives those zeros weight zero, and then read (A.16) as a count of simple
zeros; with weight zero that reading is the strict variant that EXP-010's
controls show to fail at double zeros. The correct precedent for the
full-weight convention is Conrey's eq. (32) together with eqs. (40)-(41). The
EXP-010 proof does not use CIS. The same citation appears in the frozen
EXP-010 premise table; the verdict records the correction.
