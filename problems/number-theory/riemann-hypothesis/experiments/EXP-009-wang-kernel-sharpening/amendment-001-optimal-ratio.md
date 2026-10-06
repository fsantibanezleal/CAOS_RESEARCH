# EXP-009 amendment 001: exact optimal ratio target

Declared: 2026-09-24, after the original declaration commit `123eee0d` and
before downstream constant optimization or certificate implementation.

## Discovery that triggers the amendment

A floating exploratory search performed after the original declaration found
values approaching `sqrt(2)` near `(alpha,beta)=(0,1)` and its transpose, with
no value near the original ceiling `3/2`. The boundary value is exact:

$$
R(0,1)=R(1,0)=\sqrt2.
$$

A symbolic reduction suggests that `sqrt(2)` is the global optimum, so the
experiment is strengthened rather than weakened.

## Amended Prediction A

Prove the sharp inequality

$$
\boxed{R(alpha,beta)\le\sqrt2\quad(alpha,beta\ge0),}
\tag{A+}
$$

with equality exactly at `(0,1)` and `(1,0)`.

The proposed proof sets `alpha=sinh(u)`, `beta=sinh(v)`, then

$$
X=\cosh(u+v),\qquad Y=\cosh(u-v),\qquad X\ge Y\ge1.
$$

Writing `S=sqrt(X^2-1)`, the quotient becomes

$$
R=\frac{X/2+Y(S+1/2)}{X/2+Y(X-1/2)}.
$$

For fixed `X>1` this is strictly increasing in `Y` because its derivative has
the sign of `1+S-X>0`. Hence `Y=X`, which means `u=0` or `v=0`. The remaining
one-variable quotient is

$$
\frac{1+\sqrt{X^2-1}}X\le\sqrt2,
$$

with equality only at `X=sqrt(2)`. The case `X=1` is handled directly.

## Amended kernel constant

The exact consequence of Wang's preceding inequalities is

$$
(1-d)^2\le\sqrt2\,d(1+d).
$$

Define `d_dagger` as the positive root

$$
d_\dagger=
\frac{\sqrt{2+8\sqrt2}-(2+\sqrt2)}{2(\sqrt2-1)}.
$$

The amended energy target is

$$
e_\dagger(H)=\frac{d_\dagger^2}{(1+2\pi^2H^2)^2}.
$$

All global and short-interval predictions in the original declaration remain,
with `e_*` replaced by the strictly stronger `e_dagger`. The experiment must
also certify `d_dagger>(sqrt(57)-7)/2>sqrt(5)-2`.

## Validation boundary

The exploratory optimizer is not evidence for (A+). The symbolic proof,
finite algebra checks, exact equality classification, and independent
high-precision replay are required. If any step fails, the original committed
`3/2` target remains the only declared fallback; a weaker ceiling requires a
new amendment.
