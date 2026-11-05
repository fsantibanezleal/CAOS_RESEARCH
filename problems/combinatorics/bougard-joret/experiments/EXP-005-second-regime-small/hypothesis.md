# EXP-005 preflight: exact small values in the second regime (BJB-016)

Date: 2026-11-05. Status: frozen hypothesis before any computation. CPU only.

## The open window [V] [D]

Bougard-Joret Conjecture 1 (J. Graph Theory 58 (2008), Section 6; author PDF archived under the data root,
`caos-research/bougard-joret/sources/bougard-joret-2008-turan.pdf`, SHA-256
`6d1a1bd6290b56d0cab0080f70e414b34de958012fcc818c9e8cca09ab47608b`), for $n\ge2\alpha$, $n\ge\alpha+k$,
$\alpha\ge2$, $k\ge3$:

$$f(n,\alpha,k)=\begin{cases}\lceil nk/2\rceil & n\le k\alpha,\\ t(n,\alpha)+\lceil k\alpha/2\rceil & n>k\alpha,\end{cases}$$

with $t(n,\alpha)$ the size of the balanced union of $\alpha$ cliques on $n$ vertices. The upper bound
$f\le t(n,\alpha)+\lceil k\alpha/2\rceil$ in the second regime holds by their construction [V]. Das and Gupta
(arXiv:2608.18828v1) disprove the first line ($(7,3,4)$, and $f(2k-1,k-1,k)=k^2-1$) and leave the second regime
open [V].

What is proved in the second regime [V, page 11 of the author PDF, read from the rendered page]: Proposition 8
(a 2-connected graph with $n\ge3\alpha\ge9$ and at most $t(n,\alpha)+\lfloor n/\alpha\rfloor+\alpha-3$ edges has
a partition into $\alpha$ cliques) gives the conjecture whenever $\alpha\ge3$ and
$\lceil k\alpha/2\rceil-1\le\lfloor n/\alpha\rfloor+\alpha-3$, that is

$$\lfloor n/\alpha\rfloor\ge\lceil k\alpha/2\rceil-\alpha+2;$$

and for $\alpha=2$, $n\ge2k$, entirely. [D] So the open second-regime triples with $\alpha\ge3$ are exactly
$k\alpha<n$ with $\lfloor n/\alpha\rfloor\le\lceil k\alpha/2\rceil-\alpha+1$. The smallest:

| $(n,\alpha,k)$ | conjectured $t(n,\alpha)+\lceil k\alpha/2\rceil$ | degree lower bound $\lceil nk/2\rceil$ |
|---|---|---|
| (10,3,3) | 12+5 = 17 | 15 |
| (11,3,3) | 15+5 = 20 | 17 |
| (13,4,3) | 15+6 = 21 | 20 |
| (14,4,3) | 18+6 = 24 | 21 |
| (15,4,3) | 21+6 = 27 | 23 |
| (13,3,4) | 22+6 = 28 | 26 |
| (14,3,4) | 26+6 = 32 | 28 |

($t(10,3)=6+3+3$, $t(11,3)=6+6+3$, $t(13,4)=6+3+3+3$, $t(14,4)=6+6+3+3$, $t(15,4)=6+6+6+3$,
$t(13,3)=10+6+6$, $t(14,3)=10+10+6$.)

## Question and prediction

Determine $f$ exactly at these triples, in the order of the table, as far as the solver reaches.

Prediction: the conjecture's second line holds at every triple computed (no counterexample in the open
window). Confidence MODERATE: the first-regime disproof shows the formula is not safe near the boundary, but in
the second regime the clique-partition mechanism is close to its proved range here.

## Method

Exact SAT search (z3) per triple for a graph $G$ on $n$ labelled vertices with: at most $E$ edges; no
independent set of size $\alpha+1$ (one clause per $(\alpha+1)$-set); an independent $\alpha$-set (fixed on
vertices $0..\alpha-1$, by symmetry); minimum degree $\ge k$; and $k$-connectivity by lazy cuts: every model is
checked by exact vertex connectivity (networkx); for a cut $S$ with $|S|<k$, the components of $G-S$ split into
nonempty $U,W$ and the clause "some $U$-$W$ pair is an edge" is added. $f=E^\ast$ where $E=E^\ast$ is SAT (the
model passing the check is the witness) and $E=E^\ast-1$ is UNSAT. With $E$ one below the conjectured value,
SAT is a counterexample and UNSAT confirms the triple.

Known-answer gate before any open triple: the solver must reproduce proved values, the boundary counterexample
$f(7,3,4)=15$ (Das-Gupta) and the second-regime value at a triple inside the proved range, $(12,3,3)$:
$t(12,3)+5=18+5=23$.

## Stop conditions and scope

Each triple runs under a wall-clock cap; an unfinished triple is reported as open, not as evidence. Exact
finite values only; no general formula is claimed from them. A counterexample would be verified independently
(networkx: order, independence number, connectivity, edge count) before any claim.
