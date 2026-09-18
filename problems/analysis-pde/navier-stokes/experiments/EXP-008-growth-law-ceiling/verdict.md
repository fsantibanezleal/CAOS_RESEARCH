# EXP-008 verdict: CONFIRMED, the critical exponent is gamma/(2p) for both growth laws

Date: 2026-09-17. Runner [`code/run_exp008.py`](../../code/run_exp008.py). Raw
[`result.json`](result.json).

> **Reproduction.** The settings are the `args` block of the result file, and
> `code/reproduce_all.py` rebuilds the command line from it:
>
> ```
> python run_exp008.py --g 1.0 --nu 1e-10 --stages 200 --tolerance 1e-05
> ```

## The prediction, registered before the run

Theorem 3.1 of the paper, published as v0.04 ([10.5281/zenodo.22821790](https://doi.org/10.5281/zenodo.22821790))
before this experiment: a layer cascade with frequencies `lambda = A^p`, whose layers grow at rate
`A^gamma` and are damped at `nu lambda^(2 alpha)`, can carry dissipation only up to

    alpha_c = gamma / (2p).

The pendulum case `gamma = 1/2` had been measured by EXP-003. The stretching case `gamma = 1`, which
is the growth law of the hypodissipative Navier-Stokes construction, had not.

## Result

| `gamma` | `p` | measured `alpha_c` | predicted, horizon-corrected | relative error |
|---|---|---|---|---|
| 0.5 | 1.5 | 0.205236 | 0.205236 | 1.11e-07 |
| 0.5 | 2.0 | 0.153927 | 0.153927 | 1.11e-07 |
| 0.5 | 3.0 | 0.102618 | 0.102618 | 1.11e-07 |
| 0.5 | 5.0 | 0.061571 | 0.061571 | 1.11e-07 |
| 1.0 | 1.5 | 0.371903 | 0.371903 | 1.84e-09 |
| 1.0 | 2.0 | 0.278927 | 0.278927 | 1.84e-09 |
| 1.0 | 3.0 | 0.185951 | 0.185951 | 1.84e-09 |
| 1.0 | 5.0 | 0.111571 | 0.111571 | 1.84e-09 |

All three gates pass: the pendulum law matches, the stretching law matches, and the asymptotic ratio
between the two at equal `p` is exactly two, which is the whole content of the difference between the
classes.

The measured thresholds sit above `gamma/(2p)` by the finite-horizon factor
`1 + 2 log(1/nu) / (g (Q - 1) gamma)`, as established for the pendulum case in EXP-003; the comparison
is against that corrected value, and the agreement to between `1e-7` and `2e-9` is the bisection's own
resolution.

## What it establishes

Theorem 3.1 now has numerical support in both of its cases, not only in the one this problem was built
for. Together with the proof, which uses only the growth law, the amplification identity and the
requirement that the gradients grow, this makes the class ceilings `1/4` and `1/2` in the
`(-Laplacian)^alpha` convention, `1/2` and `1` in the `|grad|^alpha` convention, the firmest statement in
the paper: neither mechanism reaches classical viscosity.

## Scope

This measures the cascade bookkeeping, not the partial differential equations: the pendulum growth law
itself was validated against the nonlinear equations by EXP-002, and the stretching law is taken from
the construction whose dissipation constraint it reproduces exactly (`a = alpha R`). The model's default
`gamma = 1/2` is unchanged, so EXP-003 reproduces as before.
