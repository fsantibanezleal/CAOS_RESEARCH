# EXP-002 verdict: CONFIRMED ($z_{\max}(5) = 4$; both predictions verified)

Run 2026-08-01, `run.py` (tclib tests green first, smoke gate matched
EXP-001, then full), repo venv Python 3.13.0, CPU only, deterministic,
64 s wall (budget 45 min; kill never approached). Raw output:
`artifacts/census5.json`.

## Results

Depth 5 EXHAUSTED: 778,087 reached-set states; 11,377 new polynomials
first seen at depth 5.

| $\tau$ | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| $z_{\max}$ | 1 | 2 | 3 | 3 | **4** |

- Prediction 1 CONFIRMED: $z_{\max}(5) = 4$: no 5-gate program attains 5
  distinct integer roots, and 4 is attained.
- Prediction 2 CONFIRMED: the minimal $\tau$ with 4 distinct integer roots
  is exactly 5.
- Exactly 10 record polynomials at depth 5 (sign/reflection variants of
  three root patterns): roots $\{-2,-1,1,2\}$, four consecutive integers
  $\{k, k+1, k+2, k+3\}$ for $k \in \{-3,-2,-1,0\}$.

## Mechanism discovery (unpredicted; feeds RL-4 and the wiki)

The committed candidate (shifted-quadratic product, 5 gates) is TIED but is
NOT how the enumerated records are built. All three reconstructed witnesses
use a DIFFERENCE-OF-SQUARES factory: compute a cheap quadratic $A$, square
it, and subtract from another square, splitting as
$B^2 - A^2 = (B-A)(B+A)$:

- $x^2 - (x^2-2)^2 = -(x-1)(x+1)(x-2)(x+2)$ (5 gates: $-2$, $x^2$,
  $x^2-2$, square, subtract);
- $1 - ((x+1)^2 + x)^2 = -x(x+1)(x+2)(x+3)$ (5 gates);
- $((x-1)^2 - x)^2 - 1 = (x^2-3x)(x^2-3x+2) = x(x-3)(x-1)(x-2)$ variant.

Structural reading [D]: the inner map $x \mapsto x^2 - 2$ is the
Chebyshev-conjugate doubling map (under $h(z) = z + 1/z$,
$h(z)^2 - 2 = h(z^2)$), i.e. the depth-5 records are the INTEGER SHADOW of
exactly the iteration mechanism that makes the REAL analogue of the
conjecture false (Rojas Example 1). Over $\mathbb{Z}$ the factory survives
one squaring step (4 roots) because the relevant integer points
($|x| \le 2$, where the conjugacy has integer orbits) exist; the RL-4
composition-obstruction line now has a concrete first target: how many
iterations of the $x^2-2$ factory keep ALL roots integral, and at what
gate cost.

## Observational (question 3, no prediction committed)

Every depth-5 record has 2-adic valuation spectrum $\{0, 1\}$ on its
nonzero roots (plus possibly the root 0): the records PILE roots into few
valuation classes rather than spreading them. First data point for the
Rojas-view dichotomy: at the bottom of the ladder, the pressure sits on
the digit-conjecture side (many roots sharing a valuation), not on the
valuation-spectrum side ($N_2$). To be re-measured at each depth.

## Adversarial validation record

- tclib test suite (5 tests) green before the run: polynomial arithmetic
  against hand-expanded products; root counting on known factorizations;
  Markstroem integer anchors (depths 1-5); EXP-001 polynomial anchors
  (depths 1-3, states 9/98/1462 and $z_{\max}$ 1/2/3).
- Smoke gate inside the run re-matched EXP-001 states at depths 1-4
  (9/98/1462/29506).
- The three reconstructed witnesses replay to exactly the record
  polynomials (tuple equality asserted) and every claimed root evaluates
  to 0 exactly; root COUNTS certified by the divisor argument.
- The committed 5-gate construction independently proves
  $z_{\max}(5) \ge 4$ without the enumerator; the enumerator adds only the
  upper side.

## How could this be wrong?

Same failure surface as EXP-001 (reached-set lemma, free-0 lemma, kernel
arithmetic), now additionally covered by the test suite and the
independent lower-bound construction; the single uncovered risk remains a
systematic blind spot shared by enumerator and witness DFS (they share
tclib code paths). Mitigation queued in TCB-005: a sympy cross-check of a
random sample of depth-5 states.

## Consequences for the strategy

- Growth data now $1, 2, 3, 3, 4$: consistent with the linear-rate world
  (records track roughly $z \approx \tau - 1$); no superlinear mechanism
  below depth 6.
- Next census depth (~30x states, ~25M state-ops) exceeds comfortable
  naive-Python budget: TCB-005 canonicalization (sign/reflection orbit
  reduction alone should cut ~4x, dominated-state pruning more) or a
  compiled/parallel backend before EXP on depth 6.
- RL-4 gains its concrete question (iterated $x^2 - 2$ over $\mathbb{Z}$);
  RL-2 gains its first observation (spectra $\{0,1\}$ at the records).
