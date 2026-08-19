# RL-3: structure lemmas for the dual set-function $T(S)$

Derivation note, 2026-08-19 (round 9). All lemmas [D], elementary,
self-contained; the exact values [MV] from the census verdicts. $T(S) :=
\min\{\tau(f) : f \ne 0,\ S \subseteq \text{roots}_{\mathbb{Z}}(f)\}$
for finite $S \subset \mathbb{Z}$ (vanishing on a SUPERSET is allowed).
The tau conjecture is equivalent to $T(S) \ge |S|^{1/\kappa} - 1$ for
all $S$.

## Lemma 1 (anti-monotonicity). $S' \subseteq S \Rightarrow T(S') \le T(S)$.
Any witness for $S$ vanishes on $S'$. Immediate.

## Lemma 2 (union subadditivity). $T(S_1 \cup S_2) \le T(S_1) + T(S_2) + 1$.
If $f_i$ witnesses $S_i$, one program computes both (concatenate;
$T(S_1) + T(S_2)$ gates suffice, sharing can only help) and one product
gate gives $f_1 f_2 \ne 0$ vanishing on the union.

## Lemma 3 (translation). $T(S + 1) \le T(S) + 1$ and symmetrically
$T(S - 1) \le T(S) + 1$; hence $|T(S + a) - T(S)| \le \tau(|a|) + 1$-ish
costs for any shift $a$ (build the constant, one gate to shift the
input).
Proof for $+1$: take a witness program for $S$; prepend the gate
$u = x - 1$ and run the program with input $u$ in place of $x$ (the
free constants are unchanged by substitution). The output is
$f(x - 1)$, which vanishes on $S + 1$. For general $a$: prepend the
build of $a$ ($\tau(a)$ gates) and one subtraction.

## Lemma 4 (reflection). $T(-S) \le T(S) + 1$, via $u = (-1) \cdot x$
and substitution as in Lemma 3. Combined with its converse direction,
$|T(S) - T(-S)| \le 1$.

## Remark (scaling is NOT elementary). For $T(2S)$ the naive substitute
would need $x/2$: not available. Vanishing on $2S$ via $f$ with
$f(2x)$-type tricks changes the polynomial, not the input, and costs
depend on $f$'s structure. No elementary bound; recorded as open (it is
exactly the constant-cost friction the census measures: e.g.
$T(\{0,\pm1,\pm2\}) = 6$ but $T(\{0,\pm2,\pm4\})$ is not obviously
$\le 7$).

## The exact table (census verdicts, decision-complete)

| $|S|$ | cheapest sets | $T$ | witness |
|---|---|---|---|
| 1 | $\{0\}, \{1\}, \{-1\}$ | 1 (exactly these, per the depth-1 census) | $x$; $x \mp 1$ |
| 1 | general $\{a\}$ | $\le \tau(a) + 1$ (e.g. $T(\{2\}) = 2$) | build $a$, subtract |
| 2 | $\{-1, 1\}$ | 2 | $x^2 - 1$ |
| 3 | $\{0, \pm 1\}$ | 3 | $x^3 - x$ |
| 4 | $\{\pm1, \pm2\}$ and consecutive 4-blocks | 5 | $x^2 - (x^2-2)^2$ |
| 5 | $\{0, \pm1, \pm2\}$ | 6 | $\mp x(x^2-1)(x^2-4)$ |
| 6 | $\{-2..3\}$-type blocks | 8 | $q(q-2)(q-6)$, $q = x(x-1)$ |

Sharpness observations the lemmas explain: consecutive blocks are
cheapest at every size measured (translation is 1 gate, so all
same-size blocks near 0 tie within 1); the jump $6 \to 8$ at size 6
(skipping 7) is the census's second plateau seen dually; Lemma 2 with
the table gives e.g. $T(S) \le 12$ for any 8-element union of two
4-blocks, far above the (unknown) truth: the union bound is weak
because it ignores sharing, which the census shows is the entire game.

## Where this goes

Wiki 04 gains the lemma block; the moves calculus (RL-8) uses Lemmas
1-4 as its certified move set; the scaling gap is a concrete question
for the next anatomy round (TCB-031).
