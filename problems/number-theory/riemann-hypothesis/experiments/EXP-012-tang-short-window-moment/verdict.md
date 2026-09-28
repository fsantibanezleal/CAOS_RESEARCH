# EXP-012 verdict: inconclusive, route stopped at step 3

Date: 2026-09-28. Declaration `76c4439` fixed the statements and a five-step
proof plan before any proof was written.

**Verdict: inconclusive.** The declared plan cannot reach Prediction C. The
stop rule applies at step 3, before steps 1 and 2 were attempted, because the
value check shows that the dual term, bounded as planned, is too large. No
theorem is claimed. This is a `research-record` with its obstruction.

## The obstruction

Tang's identity (arXiv:2608.14852v1, Theorem 1) writes the short-window twisted
moment as a main term of size `H(pq)^(-1/2)log(T/pq)`, a dual moment, and an
error `O((T/H)(pqT)^eps((p/q)^(1/2)+(q/p)^(1/2)))`. The dual moment is

$$
\sum_{\chi\bmod p}\frac{\sqrt p}{p-1}\chi(q)\int G_{T,H}(\tfrac12+it)
\Bigl(\frac\pi q\Bigr)^{it}(\Gamma\hbox{-ratio})\,|L(\tfrac12+it,\chi)|^2\,dt .
$$

Step-3 value check ([`weight_size.py`](weight_size.py), mpmath at 30 digits;
[`artifacts/canonical/weight-size.json`](artifacts/canonical/weight-size.json)):

$$
|G_{T,H}(\tfrac12+it)|=\frac{H}{\sqrt T}\sqrt{\tfrac12}\,e^{-(tH/2T)^2}(1+o(1)),
$$

confirmed within 2% at `T=10^8,10^10,10^12` and `theta=0.6,0.55,0.7`. The dual
moment therefore has size about `sqrt(p)sqrt(T)log T` per pair (`phi(p)`
characters, a `t`-range of length `T/H`, the prefactor `sqrt(p)/(p-1)` and the
weight `H/sqrt(T)`), not `sqrt(p)(T/H)` as the declaration's heuristic assumed.
It can exceed the main term even inside Tang's range: for `H=T^0.6` and
`p,q` near `T^0.15`, dual over main is about `T^0.125`.

Summed with the mollifier weights `a_h=mu(h)h^(-1/2)P[h]` over `h,k<=M=T^nu`:

| Bound on the summed dual moments | Size | Admissible range for the moment |
|---|---|---|
| trivial (declared step 3) | `sqrt(T) M^(3/2)` | `nu<(2/3)(theta-1/2)`, worse than EXP-010 |
| hybrid large sieve and a fourth-moment bound over `q<=M`, `|t|<=T/H` [I, sketch] | `sqrt(T) M` | `nu<theta-1/2`, exactly EXP-010's range |

So with the planned tools the Tang route reproduces, at best, the range EXP-010
already proves. The earlier preflight value `nu<(2/3)(2theta-1)` came from the
wrong weight size and is withdrawn.

## What would be needed

A range beyond `theta-1/2` needs cancellation in
`sum_h a_h (sqrt h/phi(h)) sum_{chi mod h} int G(...) A_chi(t)|L(1/2+it,chi)|^2 dt`,
`A_chi(t)=sum_k a_k chi(k)k^(-it)`, beyond the large sieve: an asymptotic
evaluation of this dual family, as the Conrey-Iwaniec-Soundararajan asymptotic
large sieve does for critical zeros of Dirichlet `L`-functions. That is
recorded as a new route (RH-038), not as part of this experiment.

## Disposition

EXP-012 is closed as `research-record`. The route-preflight section RH-027 is
corrected, and the backlog records RH-038.
