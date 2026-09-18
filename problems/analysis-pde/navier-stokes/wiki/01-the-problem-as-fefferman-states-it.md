# 1. The problem as Fefferman states it

Transcribed from the official Clay Mathematics Institute problem description by C. L. Fefferman,
*Existence and smoothness of the Navier-Stokes equation*
([claymath.org](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf), archived in this
problem at [`references/`](../references/)). Read in full.

## The system

$$\frac{\partial u_i}{\partial t} + \sum_{j=1}^{n} u_j \frac{\partial u_i}{\partial x_j}
  = \nu \Delta u_i - \frac{\partial p}{\partial x_i} + f_i(x,t), \qquad x\in\mathbb{R}^n,\ t\ge 0
\tag{1}$$

$$\operatorname{div} u = \sum_{i=1}^{n}\frac{\partial u_i}{\partial x_i} = 0,
\qquad u(x,0) = u^{\circ}(x).
\tag{2, 3}$$

Here $u^{\circ}$ is a given smooth divergence-free field, $f$ an externally applied force, and
$\nu>0$ the viscosity. Setting $\nu=0$ gives the Euler equations, which are not on the prize list.

## The admissibility conditions

Fefferman restricts to data that behave at infinity:

$$|\partial_x^{\alpha}u^{\circ}(x)| \le C_{\alpha K}(1+|x|)^{-K}
  \quad\text{on }\mathbb{R}^n,\ \text{for any }\alpha, K
\tag{4}$$

$$|\partial_x^{\alpha}\partial_t^{m}f(x,t)| \le C_{\alpha m K}(1+|x|+t)^{-K}
  \quad\text{on }\mathbb{R}^n\times[0,\infty),\ \text{for any }\alpha, m, K
\tag{5}$$

and accepts a solution as physically reasonable only if

$$p, u \in C^{\infty}(\mathbb{R}^n\times[0,\infty))
\tag{6}$$

$$\int_{\mathbb{R}^n}|u(x,t)|^2\,dx < C \quad\text{for all } t\ge 0 \qquad\text{(bounded energy).}
\tag{7}$$

The periodic variant replaces these with (8) to (11): periodicity of $u^{\circ}$ and $f$, time decay
of $f$, and periodicity plus smoothness of the solution. The energy condition (7) is **absent** in the
periodic case, because periodicity already rules out the problems at infinity that (7) exists to
exclude.

## The four alternatives

Fefferman writes, verbatim: "To give reasonable leeway to solvers while retaining the heart of the
problem, we ask for a proof of one of the following four statements."

| | statement | force |
|---|---|---|
| **(A)** | Existence and smoothness on $\mathbb{R}^3$ | $f \equiv 0$ |
| **(B)** | Existence and smoothness on $\mathbb{R}^3/\mathbb{Z}^3$ | $f \equiv 0$ |
| **(C)** | **Breakdown** on $\mathbb{R}^3$ | $f$ smooth, satisfying (5) |
| **(D)** | **Breakdown** on $\mathbb{R}^3/\mathbb{Z}^3$ | $f$ smooth, satisfying (9) |

Statement (C) in full:

> Take $\nu>0$ and $n=3$. Then there exist a smooth, divergence-free vector field $u^{\circ}(x)$ on
> $\mathbb{R}^3$ and a smooth $f(x,t)$ on $\mathbb{R}^3\times[0,\infty)$, satisfying (4), (5), for
> which there exist no solutions $(p,u)$ of (1), (2), (3), (6), (7) on $\mathbb{R}^3\times[0,\infty)$.

## The asymmetry that everything in September 2026 turns on

**(A) and (B) are unforced. (C) and (D) are not.** A solver of (A) or (B) must show the equations are
well behaved on their own; a solver of (C) or (D) may apply any admissible external drive and show
the equations break under it. Both count for the prize, by the sentence quoted above, and the
asymmetry is deliberate leeway rather than an oversight.

Two consequences we hold ourselves to throughout this problem.

1. **A forced breakdown result is a legitimate resolution of one of the four statements.** Dismissing
   it because it carries a force is not supported by the official text.
2. **It is not the sentence a non-specialist hears.** "The Navier-Stokes equations develop a
   singularity" without the word *forced* asserts something strictly stronger than (C), and closer to
   the negation of (A). Every surface we write carries the qualifier.

## What was already known when the September 2026 claims appeared

From Fefferman's own survey of partial results, plus the introductions of the two manuscripts:

- Two dimensions: the analogues of (A) and (B) have been known since Ladyzhenskaya, also for Euler.
  The three-dimensional difficulties are absent there.
- Three dimensions: (A) and (B) hold under a smallness condition on $u^{\circ}$, and hold on a short
  interval $[0,T)$ for arbitrary data. If a finite blowup time $T$ exists for Navier-Stokes, the
  velocity becomes unbounded near it.
- For Euler, the Beale-Kato-Majda criterion says a smooth solution continues past $T$ whenever
  $\int_0^T\lVert\operatorname{curl}u(t)\rVert_{L^{\infty}}dt<\infty$, so finite-time breakdown
  requires that integral to diverge.
- Leray (1934) constructed global finite-energy weak solutions satisfying an energy inequality;
  whether solutions from smooth data stay smooth was left open.
- Caffarelli, Kohn and Nirenberg bounded the singular set of a suitable weak solution in
  one-dimensional parabolic Hausdorff measure, which still permits isolated singularities.
- Escauriaza, Seregin and Sverak proved regularity for the unforced Cauchy problem under a bounded
  scale-invariant $L^{\infty}_t L^3_x$ norm.
- Tao constructed finite-time blowup for an *averaged* Navier-Stokes equation retaining the energy
  cancellation of the true nonlinearity ([arXiv:1402.0290](https://arxiv.org/abs/1402.0290)).
- Buckmaster and Vicol established non-uniqueness among finite-energy weak solutions by convex
  integration; Albritton, Brue and Colombo then constructed distinct suitable Leray-Hopf solutions
  with zero initial velocity and the same force, using an unstable vortex in similarity variables,
  with force in $L^1_t L^2_x$ singular at the initial time
  ([arXiv:2112.03116](https://arxiv.org/abs/2112.03116)).

The last item is the closest precedent to the September 2026 Navier-Stokes claim, and the difference
is exactly the two things the new claim adds: a force that is smooth and compactly supported rather
than singular at $t=0$, and actual blowup rather than non-uniqueness.

## Next

[2. The two September 2026 constructions](02-the-two-september-2026-constructions.md).
