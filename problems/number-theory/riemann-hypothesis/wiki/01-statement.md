# 1. Statement, counting conventions, and history

## The hypothesis and the symmetry used by this program

For $\operatorname{Re}s>1$, the Riemann zeta function is
$\zeta(s)=\sum_{n\ge1}n^{-s}$. Its analytic continuation has a pole at $s=1$;
the nontrivial zeros lie in the critical strip. The Riemann hypothesis says
that every such zero $\rho=\beta+i\gamma$ has $\beta=1/2$. This chapter follows
the conventions of [Lamzouri, Section 1](https://arxiv.org/html/2609.02882v2).

The functional equation and complex conjugation imply that a nontrivial zero
$\rho$ and its reflection $1-\overline\rho$ have the same multiplicity. These
points have the same imaginary part. Consequently a height interval contains
both members of every reflected off-line pair, without enlarging its endpoints.
After the change of coordinates

$$z=\frac{i(\rho-1/2)\log T}{2\pi},$$

the reflection becomes ordinary complex conjugation:

$$\overline z=\frac{i(1-\overline\rho-1/2)\log T}{2\pi}.$$

The transformed point is real exactly when $\rho$ is on the critical line.
This elementary identity is the connection between the finite multiset theorem
and the zero-location problem. It is used in the
[full mechanism](03-mechanism.md), with multiplicity retained throughout.

## Six counts that must remain distinct

For a height interval $I=(T,T+H]$, sum below over distinct zero locations and
write $m_\rho$ for multiplicity. Define

$$
\begin{aligned}
N(I)&=\sum_{\gamma\in I}m_\rho,&
N^d(I)&=\sum_{\gamma\in I}1,\\
N_0(I)&=\sum_{\gamma\in I,\,\beta=1/2}m_\rho,&
N_s(I)&=\sum_{\gamma\in I,\,m_\rho=1}1,\\
N_0^s(I)&=\sum_{\gamma\in I,\,\beta=1/2,\,m_\rho=1}1,&
N_{s\cup0}(I)&=\sum_{\gamma\in I,\,m_\rho=1\ \mathrm{or}\ \beta=1/2}m_\rho.
\end{aligned}
$$

Thus a triple zero on the line contributes 3 to $N$ and $N_0$, 1 to $N^d$,
and 0 to $N_0^s$. A reflected pair of simple off-line zeros contributes 2 to
$N$, $N^d$, and $N_s$, but 0 to $N_0$. These examples explain why an old
critical-line record cannot be quoted as a simple-critical record. The
conventions and union count are explicit in
[Lamzouri, Theorem 1.1](https://arxiv.org/html/2609.02882v2).

Inclusion-exclusion holds with these multiplicities:

$$N_s+N_0=N_{s\cup0}+N_0^s.$$

An average lower bound for $(N_s+N_0)/(2N)$ therefore does not give that same
lower bound for each summand separately. Nor does a lower bound for $N_0^s/N$
alone determine the distinct-zero proportion: high multiplicities must be
controlled by a separate inequality. EXP-002 derives that companion from its
strong finite rank-trace estimate.

## Global density and a theorem in every short interval

Riemann-von Mangoldt gives

$$N(0,T]=\frac{T}{2\pi}\log\frac{T}{2\pi}-\frac{T}{2\pi}+O(\log T).$$

For fixed $0<\theta<1$ and $H=T^\theta$, subtraction yields

$$N(T,H)=\frac{H\log T}{2\pi}+O(H+\log T).$$

These formulas are the input conventions in
[Wang, equations (1.1) and (1.2)](https://arxiv.org/html/2609.07918v1).
The normalized interval length $H\log T/(2\pi)$ is therefore asymptotic to
the number of zero copies in that interval. EXP-002 uses this fact to turn a
bound on the total span of simple zeros into a positive density of short
consecutive triples.

The expression

$$\liminf_{T\to\infty}\frac{N_0^s(T,T^\theta)}{N(T,T^\theta)}\ge c_*$$

means that, for every $\varepsilon>0$, the ratio is at least $c_*-\varepsilon$
for all sufficiently large $T$. It concerns every interval at sufficiently
large height for that fixed exponent. A global average over $(0,T]$ cannot be
substituted for this conclusion. Conversely, even a density-one result would
allow an exceptional set of zero density; it would not by itself exclude every
off-line zero and hence would not prove RH.

## The update that changed this backlog item

The August result gives an unconditional simple-critical density of
$C_0=0.672500703679\ldots$ and a distinct density of
$C_1=0.836250351839\ldots$. Lamzouri's September argument supplied the main
Hilbert-space simplification before this research session. Wang then supplied
the analytic short-interval interface that makes the current experiment
possible. Their roles are separate. See the
[source review](../context/2026-09-12-original-and-successor-review.md).

| Primary source | Place in the argument | Date/version retained |
|---|---|---|
| [PRZZ](https://arxiv.org/abs/1802.10521v3) | Prior mollifier bounds distinguish critical and simple-critical counts | 2019 revision; 2020 journal publication |
| [BGSTB](https://arxiv.org/abs/2306.04799) | Unconditional complex-zero pair correlation | 2023 preprint; 2024 publication |
| [BGSTB correction](https://arxiv.org/abs/2501.14545v3) | Corrected uniform error statement; integrated applications retained | September 2026 v3 |
| [Anthropic original PDF](https://www-cdn.anthropic.com/564f962e60643842f5fcb4a17c9dbc8f608f1c37.pdf) | Finite Weil-matrix route and optimized two-thirds theorem | Supplied PDF dated August 10 |
| [Alpoge-Furman](https://arxiv.org/abs/2608.13637v2) | Current arXiv presentation and additional remarks | v2 submitted August 19 |
| [Lamzouri](https://arxiv.org/abs/2609.02882v2) | Finite Hilbert inequality and four counting conclusions | v2 submitted September 8 |
| [Wang](https://arxiv.org/abs/2609.07918v1) | Pair correlation and cosine bound for power-length intervals | v1 submitted September 7 |

Submission dates and dates printed on downloaded PDFs are not interchangeable.
For example, the retained Lamzouri v2 and Wang v1 PDF copies print September 9,
while their arXiv submissions have the dates above. The
[manifest](../context/source-manifest.json) pins bytes, versions, retrieval dates,
and these notes. A source archive is not a claim that every page of the
discovery transcript received the same level of mathematical review.

## Current theorem boundary

[D] EXP-002 treats $\theta_0<\theta<1$, where $\theta_0$ is the unique root of
$c(\theta)=2-\theta/2-\cot(\theta/\sqrt2)/\sqrt2$. It improves the value of
the proportion throughout that range. The argument does not reduce the
threshold exponent, produce a finite-height zero certificate, or solve RH.
The next chapter explains why its improvement comes from retained finite
geometry rather than another optimization of the same cosine functional.

[Next: known results and barriers](02-known-results.md) | [Wiki index](README.md)
