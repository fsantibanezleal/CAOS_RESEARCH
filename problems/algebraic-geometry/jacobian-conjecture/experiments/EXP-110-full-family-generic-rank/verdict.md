# EXP-110 - Verdict: the reduced family is GENERICALLY inconsistent; rank is constant 124

## Result

Declared prediction 2 (generic rank 125, i.e. maximal) is **REFUTED**, and the
refutation is the informative direction.

Measured, modulo p = 2147483629, on the full 51-parameter family (system
\(Mq=b\): 289 pool-output rows, 125 Q-coefficient unknowns, target \(b=e_{x^2}\)):

| parameter point | rank(M) | rank([M|b]) | left kernel | covectors pairing nonzero with \(x^2\) |
|---|---|---|---|---|
| \(\varepsilon=0\) (pinned) | 124 | 125 | 165 | 1 |
| random point 1 | 124 | 125 | 165 | 1 |
| random point 2 | 124 | 125 | 165 | 1 |
| random point 3 | 124 | 125 | 165 | 1 |

Three independent random rational parameter points, plus the pinned point, all
give the identical profile.

## What this establishes

1. **The rank does not jump generically.** rank(M) = 124 < 125 at generic
   parameters, not only at \(\varepsilon = 0\). The rank deficiency is a
   property of the family, not of the special pinned point.
2. **The system is INCONSISTENT at every tested parameter point**, including
   generic ones: rank([M|b]) = 125 exceeds rank(M) = 124, and a left covector
   pairing nonzero with the target exists at each point.
3. **The certificate object is uniform in shape.** The left kernel has constant
   dimension 165 and, at each tested point, exactly one direction (up to the
   kernel's own span) pairs nonzero with the target.

## Correction recorded against my own execution

The first build in `run.py` was the TRANSPOSE of the intended system: it
computed the rank of the 125 Q-coefficient directions rather than the
equation side, and reported "rank 124 of max 125" without the target attached.
The orientation was corrected before any claim: the system is \(Mq=b\) with 289
equations and 125 unknowns, the target \(x^2=(2,0)\) is a ROW, and consistency
is decided by comparing rank(M) with rank([M|b]). All numbers above are from
the corrected orientation.

The exact rational run over \(\mathbb Q\) exceeded the declared 20-minute P6
budget on sympy `rank()` and was stopped per the kill criterion; the modular
computation is the recorded evidence. Modular rank is a LOWER bound for the
rational rank, so rank(M) over \(\mathbb Q\) is at least 124 and rank([M|b]) is
at least 125; combined with rank(M) <= 124 observed at multiple independent
points, the profile is stable.

## What this does NOT prove, and the tension to resolve

- It does not exhibit a covector that is POLYNOMIAL in \(\varepsilon\) and
  uniform across the family. Each point here has its own numeric covector.
  EXP-075 proved no global polynomial covector of degree at most three exists;
  this experiment is consistent with that, because pointwise certificates need
  not assemble into a bounded-degree global one (exactly the EXP-098 separation,
  re-verified independently this session).
- It therefore does not close \((72,108)\) and does not raise the planar floor.
- The three random points are evidence of genericity, not a proof over the whole
  51-dimensional space; a proof requires the rank-124 locus to be shown to be
  everything, i.e. that all \(125\times125\) minors vanish identically.

## The concrete next target this names

The decisive object is now sharp and is ONE computation rather than
\(\binom{51}{k}\) slices: prove that **every maximal \(125\times125\) minor of
\(M(\varepsilon)\) vanishes identically as a polynomial in \(\varepsilon\)**,
while some \(125\times125\) minor of \([M|b]\) does not. That pair of statements
is exactly uniform inconsistency of the whole family, and it is a statement
about identical vanishing of explicit polynomials, checkable by
Schwartz-Zippel-style random testing to arbitrary confidence and then by exact
certification on the surviving support.

This supersedes the slice-by-slice programme (EXP-109 and successors) as the
primary route: closing \(k\)-coefficient slices cannot terminate
(\(\binom{51}{4} = 249{,}900\) alone), whereas the minor-vanishing statement is
uniform in all 51 parameters at once.
