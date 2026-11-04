# Proof: the upper endpoint of the Bougard bracket

Date: 2026-11-04. Status: [D], complete derivation submitted for independent audit before the
finite corroboration is run. The experiment verdict owns the validation status. Post-audit
(2026-11-04) wording edits only: the helper lemma renamed Lemma H, the equality step of 4.2 stated
explicitly, and the use of $d\ge5$ in 4.3 listed in Section 5.

## 1. Statement

**Theorem 1.** For every integer $d\ge7$,

$$
f(2d+3,2,d+2)=d^2+4d+2 .
$$

Here $f(n,a,k)$ is the minimum number of edges of a $k$-connected graph of order $n$ with
independence number exactly $a$. EXP-003 (Theorem 6) proved
$d^2+4d+1\le f(2d+3,2,d+2)\le d^2+4d+2$; the upper bound is attained by the complement of the
subdivided crown. It remains to exclude the lower value.

**Theorem 2 (equivalent form).** Let $d\ge7$ and let $F$ be a triangle-free graph on $n=2d+3$
vertices with $\Delta(F)\le d$ and $e(F)=d^2+d+2$. Then $F$ contains a complete bipartite subgraph
$K_{U,W}$ ($U,W$ nonempty and disjoint, every $U$-$W$ pair an edge) with $|U|+|W|\ge d+2$.

**Theorem 2 implies Theorem 1.** Suppose $G$ has order $2d+3$, independence number two, is
$(d+2)$-connected and has $d^2+4d+1$ edges. Its complement $F$ is triangle-free, has
$\Delta(F)\le (n-1)-(d+2)=d$ and $e(F)=\binom{2d+3}{2}-(d^2+4d+1)=d^2+d+2$. Theorem 2 gives
$K_{U,W}\subseteq F$ with $|U|+|W|\ge d+2$; deleting the other at most $d+1$ vertices from $G$
leaves $U$ and $W$ with no $G$-edge between them, so $G$ is not $(d+2)$-connected, a
contradiction. A graph with fewer edges is excluded by EXP-003 Theorem 6. $\square$

In each case below the subgraph found is a $K_{2,d}$: two vertices with the same $d$ neighbours.

## 2. The five-type structure with defects

Fix $F$ as in Theorem 2 and write $D(F)=\sum_v (d-\deg v)=nd-2e(F)=d-4$.

$F$ is not bipartite: a bipartite $F$ has a side with at most $d+1$ vertices and at most
$d(d+1)<e(F)$ edges. Let $C$ be a shortest odd cycle, of length $\ell$. By EXP-003 Lemma 3, $C$ is
chordless, $\ell\ge5$, every outside vertex has at most two neighbours on $C$, and
$D(F)\ge \ell d-2n$. If $\ell\ge7$ then $D(F)\ge 7d-4d-6=3d-6>d-4$. Hence $\ell=5$; write
$C=c_0\cdots c_4$, indices mod 5.

For an outside vertex $x$ put $\sigma(x)=2-|N(x)\cap C|\ge0$, and let
$a=\sum_{x\notin C}\sigma(x)$, $b=\sum_{x\notin C}(d-\deg x)$. Since $C$ is chordless,
$\sum_{v\in C}\deg v=10+\sum_{x\notin C}|N(x)\cap C|=10+2(n-5)-a$, so

$$
\sum_{v\in C}(d-\deg v)=5d-2n+a=d-6+a,\qquad D(F)=d-6+a+b,\qquad a+b=2. \tag{1}
$$

As in EXP-003, an outside vertex with two $C$-neighbours has them at a nonadjacent pair, uniquely
$\{c_{i-1},c_{i+1}\}$. Let $V_i$ consist of $c_i$ and the outside vertices with that pair, and
$n_i=|V_i|\ge1$. Let $X$ be the set of outside vertices with at most one $C$-neighbour, $r=|X|$.
Each contributes at least one to $a$, so $r\le a\le2$, and $\sum_i n_i=2d+3-r$.

Exactly as in EXP-003: each $V_i$ is independent, and there is no edge between $V_i$ and
$V_{i\pm2}$ (members would share a $C$-neighbour). The vertex $c_i$ is adjacent to every vertex of
$W_i:=V_{i-1}\cup V_{i+1}$, to none of $V_i\cup V_{i\pm2}$, and possibly to vertices of $X$. Write
$\varepsilon_i=|N(c_i)\cap X|$ and $b_i=n_{i-1}+n_{i+1}=|W_i|$. Then

$$
\deg c_i=b_i+\varepsilon_i\le d. \tag{2}
$$

A vertex $x\in X$ adjacent to $c_j$ has no neighbour in $V_{j\pm1}$ (all of which are adjacent to
$c_j$).

**Lemma H (helpers).** Let $v\in V_i$ be an outside vertex with $\deg v=d$. If no vertex of
$N(v)\cap X$ lies outside $N(c_i)$, then $F\supseteq K_{2,d}$ with sides $\{c_i,v\}$ and $N(v)$.

*Proof.* $N(v)\subseteq W_i\cup X$ because $v$'s typed neighbours lie in consecutive types. By
hypothesis $N(v)\cap X\subseteq N(c_i)$, and $W_i\subseteq N(c_i)$, so $N(v)\subseteq N(c_i)$.
Both $c_i$ and $v$ are adjacent to all $d$ vertices of $N(v)$, and $c_i\notin N(v)$ ($V_i$ is
independent). $\square$

Call $x\in X$ a *helper* of $v\in V_i$ when $x\sim v$ and $x\not\sim c_i$. From now on assume, for
contradiction, that $F$ contains no complete bipartite subgraph on $d+2$ vertices. Then every
outside typed vertex of degree $d$ has a helper. The number of outside typed vertices is
$2d+3-5-r=2d-2-r$.

## 3. At most one defective vertex

**$r=0$.** Then $a=0$, $b=2$, so at most two outside vertices have degree below $d$, while there
are $2d-2\ge12$ outside typed vertices and no helpers at all. Contradiction.

**$r=1$, $X=\{x\}$.** If $x$ has no $C$-neighbour then $a\ge2$, so $b=0$: all $2d-3$ outside typed
vertices have degree $d$ and need $x$ as a helper, so $\deg x\ge2d-3>d$. If $x$ has one
$C$-neighbour then $a=1$, $b=1$: at least $2d-4$ outside typed vertices have degree $d$ and are
adjacent to $x$, and $\deg x\ge 2d-3>d$. Contradiction.

## 4. Two defective vertices

Now $r=2$, so $a=2$, $b=0$: $X=\{x_1,x_2\}$, each $x_k$ has exactly one $C$-neighbour, say
$c_p\sim x_1$ and $c_q\sim x_2$, and every outside vertex (typed or in $X$) has degree exactly $d$.
Also $\sum_i n_i=2d+1$ and $\sum_i\varepsilon_i=2$.

The helpers available to $V_i$: $x_1$ is never adjacent to $V_{p\pm1}$ and is in $N(c_p)$, so it
can help only vertices of $V_{p+2}\cup V_{p+3}$; likewise $x_2$ only $V_{q+2}\cup V_{q+3}$. A type
none of whose outside vertices can be helped is a singleton.

For an outside $v\in V_i$ let $\xi(v)=|N(v)\cap X|\in\{1,2\}$. Since $\deg v=d$,

$$
|N(v)\cap W_i|=d-\xi(v). \tag{3}
$$

**(T) Triangle rule.** If a vertex $x\in X$ is adjacent to $u\in V_i$ and $w\in V_{i+1}$, then
$u\not\sim w$.

Up to rotation and reflection, $q-p\in\{0,1,2\}$.

### 4.1. $q=p$

Only $V_{p+2},V_{p+3}$ can be helped, so $n_{p-1}=n_p=n_{p+1}=1$ and $n_{p+2}+n_{p+3}=2d-2$.
Since $\varepsilon_{p\pm1}=0$, (2) at $c_{p+1}$ and $c_{p-1}$ gives $1+n_{p+2}\le d$ and
$1+n_{p+3}\le d$, so $n_{p+2}=n_{p+3}=d-1$. Put $A=V_{p+2}$, $B=V_{p+3}$, $A^\circ,B^\circ$ their
outside vertices ($d-2$ each). For $v\in A^\circ$, $W_{p+2}=\{c_{p+1}\}\cup B$ has size $d$ and
$v\sim c_{p+1}$, so by (3) $v$ misses exactly $\xi(v)\le2$ vertices of $B$; symmetrically for
$B^\circ$.

The typed neighbours of $x_k$ other than $c_p$ lie in $A^\circ\cup B^\circ$ (it has no other
$C$-neighbour, and $V_p=\{c_p\}$). If $x_k$ had neighbours in both $A^\circ$ and $B^\circ$, by (T)
each of its $A^\circ$-neighbours misses all its $B^\circ$-neighbours, so it has at most two of the
latter, and symmetrically at most two of the former: at most four typed outside neighbours. But
$\deg x_k=d$ gives at least $d-2\ge5$ of them. So each $x_k$ has all its typed outside neighbours on
one side. Both sides need helpers, so (say) $x_1$ covers $A^\circ$ and $x_2$ covers $B^\circ$, and
$d=\deg x_1=1+|N(x_1)\cap A^\circ|+[x_1\sim x_2]\le 1+(d-2)+[x_1\sim x_2]$ forces
$x_1\sim x_2$. Then $x_1x_2c_p$ is a triangle. Contradiction.

### 4.2. $q=p+1$

Here $x_1$ helps only $V_{p+2}\cup V_{p+3}$ and $x_2$ only $V_{p+3}\cup V_{p+4}$; also $x_1$ is not
adjacent to $V_{p+4}$ and $x_2$ is not adjacent to $V_{p+2}$. So $n_p=n_{p+1}=1$,
$\varepsilon_p=\varepsilon_{p+1}=1$, and $n_{p+2}+n_{p+3}+n_{p+4}=2d-1$. By (2):
$n_{p+4}+1\le d-1$ (at $c_p$), $1+n_{p+2}\le d-1$ (at $c_{p+1}$), $1+n_{p+3}\le d$ (at $c_{p+2}$),
$n_{p+2}+n_{p+4}\le d$ (at $c_{p+3}$). Since $n_{p+3}+(n_{p+2}+n_{p+4})=2d-1$ while the last two give $n_{p+3}\le d-1$ and
$n_{p+2}+n_{p+4}\le d$, both hold with equality:
$n_{p+3}=d-1$, $n_{p+2}+n_{p+4}=d$, and $n_{p+2},n_{p+4}\le d-2$; hence both are at least two.

An outside $v\in V_{p+2}$ can only be adjacent to $x_1$ in $X$, and needs it, so $\xi(v)=1$; with
$|W_{p+2}|=1+n_{p+3}=d$ and $v\sim c_{p+1}$, (3) says $v$ misses exactly one vertex of $V_{p+3}$.
All of $V_{p+2}^\circ\ne\emptyset$ is adjacent to $x_1$, so by (T) $x_1$ has at most one neighbour
in $V_{p+3}^\circ$. Symmetrically ($V_{p+4}^\circ\neq\emptyset$, all adjacent to $x_2$) $x_2$ has at
most one neighbour in $V_{p+3}^\circ$. But all $d-2\ge5$ vertices of $V_{p+3}^\circ$ need a helper.
Contradiction.

### 4.3. $q=p+2$

Now $x_1$ helps only $V_{p+2}\cup V_{p+3}$, $x_2$ only $V_{p+4}\cup V_p$; $x_1$ is not adjacent to
$V_{p+1}\cup V_{p+4}$ and $x_2$ not to $V_{p+1}\cup V_{p+3}$. So $n_{p+1}=1$,
$\varepsilon_p=\varepsilon_{p+2}=1$. Write $\alpha=n_p$, $\beta=n_{p+2}$, $\gamma=n_{p+3}$,
$\delta=n_{p+4}$, with $\alpha+\beta+\gamma+\delta=2d$. By (2): $\delta\le d-2$ (at $c_p$),
$\alpha+\beta\le d$ (at $c_{p+1}$), $\gamma\le d-2$ (at $c_{p+2}$), $\beta+\delta\le d$
(at $c_{p+3}$), $\gamma+\alpha\le d$ (at $c_{p+4}$). From $\alpha+\beta\le d$, $\gamma+\delta\ge d$,
so $\gamma,\delta\ge2$.

*Vertices of $V_{p+3}^\circ$ (nonempty).* Their only possible $X$-neighbour is $x_1$, which they
need, so $\xi=1$ and by (3) each has $d-1$ neighbours in $W_{p+3}=V_{p+2}\cup V_{p+4}$.
Symmetrically each vertex of $V_{p+4}^\circ$ (nonempty) has $x_2$ as its only $X$-neighbour and
$d-1$ neighbours in $V_{p+3}\cup V_p$.

*If $\beta=1$:* a vertex of $V_{p+3}^\circ$ has $d-1\le |V_{p+2}\cup V_{p+4}|=1+\delta$, so
$\delta=d-2$ and $\alpha+\gamma=2d-1-\delta=d+1>d$. Contradiction.

*If $\beta\ge2$:* all of $V_{p+2}^\circ$ and $V_{p+3}^\circ$ are adjacent to $x_1$ (their only
possible helper), so by (T) no edge joins them. A vertex of $V_{p+3}^\circ$ then has its $d-1$
$W$-neighbours in $\{c_{p+2}\}\cup V_{p+4}$, so $\delta=d-2$.
- If $\alpha=1$: a vertex of $V_{p+4}^\circ$ has $d-1\le\gamma+1$, so $\gamma=d-2$ and
  $\beta=2d-1-2(d-2)=3$, giving $\beta+\delta=d+1>d$. Contradiction.
- If $\alpha\ge2$: as above $V_{p+4}^\circ$ and $V_p^\circ$ are all adjacent to $x_2$, no edge joins
  them, and a vertex of $V_{p+4}^\circ$ has its $d-1$ neighbours in $V_{p+3}\cup\{c_p\}$, so
  $\gamma=d-2$. Then $\alpha+\beta=4$ and $\beta\le d-\delta=2$, so $\alpha=\beta=2$. The single
  vertex $v\in V_{p+2}^\circ$ has $W_{p+2}=\{c_{p+1}\}\cup V_{p+3}$ and no neighbour in
  $V_{p+3}^\circ$, so $\deg v\le|\{c_{p+1},c_{p+3}\}|+|X|=4<d$. Contradiction.

All cases are excluded, which proves Theorem 2 and hence Theorem 1. $\square$

## 5. Consequences and scope

- $f(2d+3,2,d+2)=d^2+4d+2$ for every $d\ge7$; for example $f(19,2,10)=98$. It exceeds the
  degree-sum value $\lceil(2d+3)(d+2)/2\rceil$ by $\lfloor d/2\rfloor-1$.
- Every triangle-free graph on $2d+3$ vertices with $\Delta\le d$ and $d^2+d+2$ edges has two
  vertices with the same $d$ neighbours (a $K_{2,d}$), as the BET graph $Q_d$ does with $A_0,A_1$.
  This is a structural statement about all extremal graphs of EXP-003 Theorem 1, without
  classifying them.
- Not claimed: the full Bougard-Joret problem, the second regime $n>k\alpha$ (BJB-016), or other
  matching levels of the AEY conjecture (BJB-015).
- The degree hypothesis $d\ge7$ is used in Section 3 ($2d-2\ge12$, $2d-3>d$), in 4.1 ($d-2\ge5$)
  in 4.2 ($d-2\ge5$) and in 4.3 (the final degree bound $4<d$ needs $d\ge5$). Smaller $d$ are
  not treated.
