# The monic stall theorem: single-map towers never refute the tau conjecture

Derivation note, 2026-08-01 round 4 (TCB-020, generalizing the
Chebyshev-tower note of the same date). All [D]: our own proofs,
elementary; machine spot-checks in `code/tclib/test_tclib.py`
(test_monic_stall_spotcheck).

## Setting

Fix a monic $h \in \mathbb{Z}[x]$, $\deg h = d \ge 2$. The tower family
over $h$ is any sequence of polynomials whose integer roots are, level by
level, constrained through iterates of $h$: the model cases are
$h^{\circ k}(x) - x$ (fixed-point towers) and the difference-of-squares
towers $G_k = h^{\circ(k-1)}(x)^2 - h^{\circ k}(x)^2$, both computable by
SLPs of length $O(k + \tau(h))$.

## Lemma 1 (escape radius). Let $R := 1 + \sum_{i<d} |a_i|$ where
$h = x^d + \sum_{i<d} a_i x^i$. Then $|x| \ge R + 1$ implies
$|h(x)| \ge |x| + 1$.

Proof: since $\sum_{i<d} |a_i| |x|^i \le (R-1)\,|x|^{d-1}$ for
$|x| \ge 1$, we get $|h(x)| \ge |x|^d - (R-1)|x|^{d-1} =
|x|^{d-1}\,(|x| - (R-1)) \ge 2\,|x|^{d-1} \ge 2|x| \ge |x| + 1$ whenever
$|x| \ge R + 1$ (using $d \ge 2$).

## Lemma 2 (finite stable core). For any finite $A \subset \mathbb{Z}$,
the increasing union $K(A) := \bigcup_{k \ge 0} (h^{\circ k})^{-1}(A)
\cap \mathbb{Z}$ is contained in $[-M, M]$ with
$M := \max(R + 1, \max_{a \in A} |a|)$, hence finite, and the union
stabilizes after finitely many levels.

Proof: if $|x| > M$ then by Lemma 1 and induction
$|h^{\circ k}(x)| \ge |x| + k > M \ge \max_{a\in A}|a|$ for all
$k \ge 0$, so $x \notin K(A)$. $K(A)$ is thus an increasing union of
subsets of the fixed finite set $[-M, M] \cap \mathbb{Z}$, so it
stabilizes.

## Theorem (stall). For every monic $h$ of degree $\ge 2$ there is a
constant $Z(h)$ such that for ALL $k$:
(a) $h^{\circ k}(x) - x$ has at most $Z(h)$ distinct integer roots;
(b) $G_k = h^{\circ(k-1)}(x)^2 - h^{\circ k}(x)^2$ has at most $Z(h)$
distinct integer roots.
One may take $Z(h) = \#([-M, M] \cap \mathbb{Z})$ with the $M$ of
Lemma 2 for $A$ = the integer solution sets of $h(y) = y$ and
$h(y) = -y$ (both of size $\le d$).

Proof: (a) integer roots are periodic points of $h$; by Lemma 1 all
periodic points lie in $[-R-1, R+1]$. (b) $G_k$ factors as
$(h^{\circ(k-1)} - h^{\circ k})(h^{\circ(k-1)} + h^{\circ k})$, so an
integer root $x$ has $y = h^{\circ(k-1)}(x)$ solving $h(y) = \pm y$;
hence $x \in (h^{\circ(k-1)})^{-1}(A) \subseteq K(A) \subseteq [-M, M]$.

## Consequence for the program

Towers built by iterating ONE fixed monic map, at ANY depth, have integer
root counts bounded by a constant depending only on the map, while their
SLP cost grows linearly in the depth and their REAL root counts can grow
exponentially (the $h = x^2 - 2$ case: $2^k$). Therefore no
single-inner-map tower family can ever witness superpolynomial growth of
$z$ versus $\tau$: a refutation of the tau conjecture, if it exists, must
use MULTI-map or shifted constructions whose constants are built along
the way, i.e. exactly the regime where constant-building cost competes
against root yield. This sharpens the census's anatomy question: measure
the root yield per gate of constant-building.

Spot-check (machine, in the test suite): $h = x^2 - 6$. Fixed points
$h(y) = y$: $\{3, -2\}$; anti-fixed $h(y) = -y$: $\{2, -3\}$; integer
preimages: $h^{-1}(3) = \{\pm 3\}$, $h^{-1}(-2) = \{\pm 2\}$,
$h^{-1}(2) = \emptyset$ ($x^2 = 8$), $h^{-1}(-3) = \emptyset$
($x^2 = 3$), so the stable core is $\{\pm 2, \pm 3\}$ and every tower
level $G_k$ has integer-root set exactly $\{\pm 2, \pm 3\}$ (4 roots,
all $k \ge 1$), against $2^k$-scale real-root growth.
